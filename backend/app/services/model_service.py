"""BharatBrief T5 Model Service - low-memory ONNX inference."""

import hashlib
import logging
import os

import numpy as np
import onnxruntime as ort
from cachetools import LRUCache
from transformers import AutoTokenizer

from app.config import get_settings

logger = logging.getLogger(__name__)

LENGTH_PRESETS = {
    "short": {
        "max_length": 60,
        "min_length": 15,
        "length_penalty": 1.0,
    },
    "medium": {
        "max_length": 128,
        "min_length": 30,
        "length_penalty": 1.0,
    },
    "detailed": {
        "max_length": 256,
        "min_length": 60,
        "length_penalty": 0.8,
    },
}

HF_MODEL_ID = "Ayush1082/BharatBrief-T5-INT8"


class ModelService:
    """Low-memory ONNX Runtime inference service."""

    def __init__(self):
        self.encoder = None
        self.decoder = None
        self.tokenizer = None

        self._cache = LRUCache(maxsize=128)
        self._is_loaded = False

    def _session_options(self):
        """Create memory-efficient ONNX Runtime settings."""

        options = ort.SessionOptions()

        options.graph_optimization_level = (
            ort.GraphOptimizationLevel.ORT_ENABLE_BASIC
        )

        options.enable_mem_pattern = False
        options.enable_cpu_mem_arena = False

        options.intra_op_num_threads = 1
        options.inter_op_num_threads = 1

        return options

    def load_model(self):
        """Load only encoder and decoder ONNX models."""

        settings = get_settings()

        use_huggingface = (
            os.getenv(
                "USE_HUGGINGFACE_MODEL",
                "false",
            ).lower()
            == "true"
        )

        if use_huggingface:
            logger.info(
                f"Loading low-memory INT8 model from Hugging Face: "
                f"{HF_MODEL_ID}"
            )

            from huggingface_hub import hf_hub_download

            tokenizer_path = HF_MODEL_ID

            encoder_path = hf_hub_download(
                repo_id=HF_MODEL_ID,
                filename="encoder_model.onnx",
            )

            decoder_path = hf_hub_download(
                repo_id=HF_MODEL_ID,
                filename="decoder_model.onnx",
            )

        else:
            model_path = os.path.abspath(
                os.path.join(
                    settings.MODEL_PATH,
                    "..",
                    "bharatbrief_onnx_int8",
                )
            )

            logger.info(
                f"Loading low-memory INT8 model from: "
                f"{model_path}"
            )

            tokenizer_path = model_path
            encoder_path = os.path.join(
                model_path,
                "encoder_model.onnx",
            )
            decoder_path = os.path.join(
                model_path,
                "decoder_model.onnx",
            )

        logger.info("Loading tokenizer...")

        self.tokenizer = AutoTokenizer.from_pretrained(
            tokenizer_path
        )

        options = self._session_options()

        logger.info("Loading encoder session...")

        self.encoder = ort.InferenceSession(
            encoder_path,
            sess_options=options,
            providers=["CPUExecutionProvider"],
        )

        logger.info("Loading decoder session...")

        self.decoder = ort.InferenceSession(
            decoder_path,
            sess_options=options,
            providers=["CPUExecutionProvider"],
        )

        self._is_loaded = True

        logger.info(
            "BharatBrief low-memory INT8 ONNX model loaded"
        )

    def warmup(self):
        """Run a very small inference to initialize ONNX Runtime."""

        if not self._is_loaded:
            raise RuntimeError(
                "Model not loaded. Call load_model() first."
            )

        logger.info("Warming up model...")

        inputs = self.tokenizer(
            "summarize: This is a short warmup.",
            return_tensors="np",
            max_length=32,
            truncation=True,
        )

        encoder_inputs = {
            "input_ids": inputs["input_ids"].astype(np.int64),
            "attention_mask": inputs["attention_mask"].astype(np.int64),
        }

        encoder_outputs = self.encoder.run(
            None,
            encoder_inputs,
        )

        logger.info(
            f"Encoder warmup complete. "
            f"Output shape: {encoder_outputs[0].shape}"
        )

        logger.info("Model warmup complete")

    def _get_cache_key(
        self,
        text: str,
        length: str,
    ) -> str:

        content = f"{text}::{length}"

        return hashlib.md5(
            content.encode()
        ).hexdigest()

    def summarize(
        self,
        text: str,
        length: str = "medium",
        num_beams: int = 1,
        no_repeat_ngram_size: int = 3,
    ) -> str:

        if not self._is_loaded:
            raise RuntimeError(
                "Model not loaded. Call load_model() first."
            )

        cache_key = self._get_cache_key(
            text,
            length,
        )

        if cache_key in self._cache:
            return self._cache[cache_key]

        settings = get_settings()

        preset = LENGTH_PRESETS.get(
            length,
            LENGTH_PRESETS["medium"],
        )

        input_text = (
            f"{settings.MODEL_PREFIX} {text}"
        )

        inputs = self.tokenizer(
            input_text,
            return_tensors="np",
            max_length=min(
                settings.MODEL_MAX_INPUT_LENGTH,
                512,
            ),
            truncation=True,
            padding=False,
        )

        input_ids = inputs["input_ids"].astype(np.int64)
        attention_mask = inputs["attention_mask"].astype(np.int64)

        # -------------------------------------------------
        # Encoder
        # -------------------------------------------------

        encoder_inputs = {
            "input_ids": input_ids,
            "attention_mask": attention_mask,
        }

        encoder_outputs = self.encoder.run(
            None,
            encoder_inputs,
        )

        encoder_hidden_states = encoder_outputs[0]

        # -------------------------------------------------
        # Decoder
        # -------------------------------------------------

        decoder_inputs_info = self.decoder.get_inputs()

        decoder_input_names = {
            item.name for item in decoder_inputs_info
        }

        # T5 decoder starts with PAD token.
        decoder_start_token_id = (
            self.tokenizer.pad_token_id
        )

        if decoder_start_token_id is None:
            decoder_start_token_id = 0

        generated = [
            decoder_start_token_id
        ]

        max_length = preset["max_length"]

        # Keep generation bounded for low RAM.
        max_length = min(max_length, 128)

        for _ in range(max_length - 1):

            decoder_input_ids = np.array(
                [generated],
                dtype=np.int64,
            )

            decoder_attention_mask = np.ones(
                decoder_input_ids.shape,
                dtype=np.int64,
            )

            decoder_inputs = {}

            if "input_ids" in decoder_input_names:
                decoder_inputs["input_ids"] = (
                    decoder_input_ids
                )

            if "decoder_input_ids" in decoder_input_names:
                decoder_inputs["decoder_input_ids"] = (
                    decoder_input_ids
                )

            if "attention_mask" in decoder_input_names:
                decoder_inputs["attention_mask"] = (
                    attention_mask
                )

            if "encoder_attention_mask" in decoder_input_names:
                decoder_inputs["encoder_attention_mask"] = (
                    attention_mask
                )

            if (
                "encoder_hidden_states"
                in decoder_input_names
            ):
                decoder_inputs[
                    "encoder_hidden_states"
                ] = encoder_hidden_states

            outputs = self.decoder.run(
                None,
                decoder_inputs,
            )

            logits = outputs[0]

            next_token = int(
                np.argmax(
                    logits[0, -1, :]
                )
            )

            generated.append(next_token)

            if next_token == (
                self.tokenizer.eos_token_id
            ):
                break

        summary = self.tokenizer.decode(
            generated,
            skip_special_tokens=True,
        )

        self._cache[cache_key] = summary

        logger.debug(
            f"Generated summary ({length}): "
            f"{len(summary)} chars"
        )

        return summary

    def get_token_count(
        self,
        text: str,
    ) -> int:

        if not self._is_loaded:
            return len(text.split())

        tokens = self.tokenizer.encode(
            text,
            add_special_tokens=False,
        )

        return len(tokens)

    @property
    def is_loaded(self) -> bool:
        return self._is_loaded


model_service = ModelService()