"""BharatBrief T5 Model Service - ONNX Runtime inference engine."""

import hashlib
import logging
import os

from cachetools import LRUCache
from transformers import AutoTokenizer
from optimum.onnxruntime import ORTModelForSeq2SeqLM

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
    """Manages BharatBrief ONNX model loading and inference."""

    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.device = "cpu"
        self._cache = LRUCache(maxsize=256)
        self._is_loaded = False

    def load_model(self):
        """Load BharatBrief ONNX INT8 model."""

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
                f"Loading INT8 model from Hugging Face: "
                f"{HF_MODEL_ID}"
            )

            model_path = HF_MODEL_ID

            self.tokenizer = AutoTokenizer.from_pretrained(
                model_path
            )

            self.model = ORTModelForSeq2SeqLM.from_pretrained(
                model_path,
                encoder_file_name="encoder_model.onnx",
                decoder_file_name="decoder_model.onnx",
                decoder_with_past_file_name=(
                    "decoder_with_past_model.onnx"
                ),
                provider="CPUExecutionProvider",
                use_io_binding=False,
            )

        else:

            model_path = os.path.join(
                settings.MODEL_PATH,
                "..",
                "bharatbrief_onnx_int8",
            )

            model_path = os.path.abspath(model_path)

            logger.info(
                f"Loading INT8 model from local path: "
                f"{model_path}"
            )

            self.tokenizer = AutoTokenizer.from_pretrained(
                model_path,
                local_files_only=True,
            )

            self.model = ORTModelForSeq2SeqLM.from_pretrained(
                model_path,
                encoder_file_name="encoder_model.onnx",
                decoder_file_name="decoder_model.onnx",
                decoder_with_past_file_name=(
                    "decoder_with_past_model.onnx"
                ),
                provider="CPUExecutionProvider",
                use_io_binding=False,
            )

        self._is_loaded = True

        logger.info(
            "BharatBrief INT8 ONNX model loaded successfully"
        )

    def warmup(self):
        """Run a small inference to warm up the model."""

        if not self._is_loaded:
            raise RuntimeError(
                "Model not loaded. Call load_model() first."
            )

        logger.info("Warming up model...")

        dummy_text = (
            "summarize: This is a warmup text used "
            "to initialize the BharatBrief model."
        )

        inputs = self.tokenizer(
            dummy_text,
            return_tensors="pt",
            max_length=64,
            truncation=True,
        )

        self.model.generate(
            **inputs,
            max_length=20,
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
        num_beams: int = 4,
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

            logger.debug(
                "Cache hit for summary request"
            )

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
            return_tensors="pt",
            max_length=settings.MODEL_MAX_INPUT_LENGTH,
            truncation=True,
            padding=False,
        )

        outputs = self.model.generate(
            **inputs,
            max_length=preset["max_length"],
            min_length=preset["min_length"],
            num_beams=num_beams,
            length_penalty=preset["length_penalty"],
            no_repeat_ngram_size=no_repeat_ngram_size,
            do_sample=False,
            early_stopping=True,
        )

        summary = self.tokenizer.decode(
            outputs[0],
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