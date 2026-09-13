"""BharatBrief T5 Model Service - CTranslate2 INT8 inference."""

import hashlib
import logging
import os

import ctranslate2
from cachetools import LRUCache
from transformers import AutoTokenizer

from app.config import get_settings

logger = logging.getLogger(__name__)

LENGTH_PRESETS = {
    "short": {
        "max_length": 60,
        "min_length": 15,
    },
    "medium": {
        "max_length": 128,
        "min_length": 30,
    },
    "detailed": {
        "max_length": 128,
        "min_length": 60,
    },
}

HF_MODEL_ID = "Ayush1082/BharatBrief-T5-CT2-INT8"


class ModelService:
    """Manages BharatBrief CTranslate2 model."""

    def __init__(self):
        self.model = None
        self.tokenizer = None
        self._cache = LRUCache(maxsize=128)
        self._is_loaded = False

    def load_model(self):
        """Load BharatBrief CTranslate2 INT8 model."""

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
                f"Loading CTranslate2 INT8 model from "
                f"Hugging Face: {HF_MODEL_ID}"
            )

            from huggingface_hub import snapshot_download

            model_path = snapshot_download(
                repo_id=HF_MODEL_ID,
                allow_patterns=[
                    "model.bin",
                    "config.json",
                    "shared_vocabulary.json",
                ],
            )

            tokenizer_path = snapshot_download(
                repo_id="Ayush1082/BharatBrief-T5",
                allow_patterns=[
                    "tokenizer.json",
                    "tokenizer_config.json",
                    "special_tokens_map.json",
                    "spiece.model",
                ],
            )

        else:

            model_path = os.path.abspath(
                os.path.join(
                    settings.MODEL_PATH,
                    "..",
                    "bharatbrief_ct2_int8",
                )
            )

            tokenizer_path = os.path.abspath(
                settings.MODEL_PATH
            )

            logger.info(
                f"Loading CTranslate2 model from: "
                f"{model_path}"
            )

        self.tokenizer = AutoTokenizer.from_pretrained(
            tokenizer_path,
            local_files_only=not use_huggingface,
        )

        self.model = ctranslate2.Translator(
            model_path,
            device="cpu",
            inter_threads=1,
            intra_threads=1,
        )

        self._is_loaded = True

        logger.info(
            "BharatBrief CTranslate2 INT8 model loaded successfully"
        )

    def warmup(self):
        """Run a tiny inference to initialize the model."""

        if not self._is_loaded:
            raise RuntimeError(
                "Model not loaded. Call load_model() first."
            )

        logger.info("Warming up model...")

        tokens = self.tokenizer.convert_ids_to_tokens(
            self.tokenizer(
                "summarize: This is a short warmup.",
                add_special_tokens=True,
            )["input_ids"]
        )

        self.model.translate_batch(
            [tokens],
            beam_size=1,
            max_decoding_length=20,
            min_decoding_length=1,
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

        encoded = self.tokenizer(
            input_text,
            max_length=min(
                settings.MODEL_MAX_INPUT_LENGTH,
                512,
            ),
            truncation=True,
            add_special_tokens=True,
        )

        tokens = self.tokenizer.convert_ids_to_tokens(
            encoded["input_ids"]
        )

        # CTranslate2 generation.
        results = self.model.translate_batch(
            [tokens],
            beam_size=max(1, min(num_beams, 2)),
            max_decoding_length=preset["max_length"],
            min_decoding_length=preset["min_length"],
            repetition_penalty=1.2,
            no_repeat_ngram_size=no_repeat_ngram_size,
        )

        output_tokens = results[0].hypotheses[0]

        output_ids = (
            self.tokenizer.convert_tokens_to_ids(
                output_tokens
            )
        )

        summary = self.tokenizer.decode(
            output_ids,
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