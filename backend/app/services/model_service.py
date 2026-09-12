"""T5 Model Service - Core inference engine."""

import hashlib
import logging
import os

import torch
from cachetools import LRUCache
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

from app.config import get_settings

logger = logging.getLogger(__name__)

LENGTH_PRESETS = {
    "short": {"max_length": 60, "min_length": 15, "length_penalty": 1.0},
    "medium": {"max_length": 128, "min_length": 30, "length_penalty": 1.0},
    "detailed": {"max_length": 256, "min_length": 60, "length_penalty": 0.8},
}

HF_MODEL_ID = "Ayush1082/BharatBrief-T5"


class ModelService:
    """Manages T5 model loading, inference, and caching."""

    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.device = None
        self._cache = LRUCache(maxsize=256)
        self._is_loaded = False

    def load_model(self):
        """Load the fine-tuned BharatBrief model."""

        settings = get_settings()

        # Use local model if it exists.
        local_path = settings.MODEL_PATH

        # On Render, use the Hugging Face model.
        use_huggingface = os.getenv("USE_HUGGINGFACE_MODEL", "false").lower() == "true"

        if use_huggingface:
            model_path = HF_MODEL_ID
            logger.info(f"Loading model from Hugging Face: {model_path}")
        else:
            model_path = local_path
            logger.info(f"Loading model from local path: {model_path}")

        # Detect device.
        if torch.cuda.is_available():
            self.device = torch.device("cuda")
            logger.info("Using CUDA GPU for inference")
        else:
            self.device = torch.device("cpu")
            logger.info("Using CPU for inference")

        # Load tokenizer and model.
        if use_huggingface:
            self.tokenizer = AutoTokenizer.from_pretrained(model_path)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
        else:
            self.tokenizer = AutoTokenizer.from_pretrained(
                model_path,
                local_files_only=True,
            )
            self.model = AutoModelForSeq2SeqLM.from_pretrained(
                model_path,
                local_files_only=True,
            )

        self.model.to(self.device)
        self.model.eval()

        self._is_loaded = True
        logger.info("Model loaded successfully")

    def warmup(self):
        """Run a small inference to warm up the model."""

        if not self._is_loaded:
            raise RuntimeError("Model not loaded. Call load_model() first.")

        logger.info("Warming up model...")

        dummy_text = (
            "summarize: This is a warmup text used to initialize "
            "the BharatBrief summarization model."
        )

        inputs = self.tokenizer(
            dummy_text,
            return_tensors="pt",
            max_length=64,
            truncation=True,
        )

        inputs = {key: value.to(self.device) for key, value in inputs.items()}

        with torch.no_grad():
            self.model.generate(
                inputs["input_ids"],
                max_length=20,
            )

        logger.info("Model warmup complete")

    def _get_cache_key(self, text: str, length: str) -> str:
        content = f"{text}::{length}"
        return hashlib.md5(content.encode()).hexdigest()

    def summarize(
        self,
        text: str,
        length: str = "medium",
        num_beams: int = 4,
        no_repeat_ngram_size: int = 3,
    ) -> str:

        if not self._is_loaded:
            raise RuntimeError("Model not loaded. Call load_model() first.")

        cache_key = self._get_cache_key(text, length)

        if cache_key in self._cache:
            logger.debug("Cache hit for summary request")
            return self._cache[cache_key]

        settings = get_settings()
        preset = LENGTH_PRESETS.get(length, LENGTH_PRESETS["medium"])

        input_text = f"{settings.MODEL_PREFIX} {text}"

        inputs = self.tokenizer(
            input_text,
            return_tensors="pt",
            max_length=settings.MODEL_MAX_INPUT_LENGTH,
            truncation=True,
            padding=False,
        )

        inputs = {key: value.to(self.device) for key, value in inputs.items()}

        with torch.no_grad():
            outputs = self.model.generate(
                inputs["input_ids"],
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
            f"Generated summary ({length}): {len(summary)} chars"
        )

        return summary

    def get_token_count(self, text: str) -> int:

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