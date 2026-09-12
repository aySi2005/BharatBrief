"""T5 Model Service — Core inference engine.

Converts notebook inference logic into a production-ready service with:
- Automatic CPU/GPU detection
- Configurable generation parameters
- Input truncation handling
- Model warmup
- In-memory caching for repeated inputs
"""
import logging
import hashlib
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from cachetools import LRUCache
from app.config import get_settings

logger = logging.getLogger(__name__)

# Summary length presets: (max_length, min_length, length_penalty)
LENGTH_PRESETS = {
    "short": {"max_length": 60, "min_length": 15, "length_penalty": 1.0},
    "medium": {"max_length": 128, "min_length": 30, "length_penalty": 1.0},
    "detailed": {"max_length": 256, "min_length": 60, "length_penalty": 0.8},
}


class ModelService:
    """Manages T5 model loading, inference, and caching."""

    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.device = None
        self._cache = LRUCache(maxsize=256)
        self._is_loaded = False

    def load_model(self):
        """Load model and tokenizer from disk. Called once at startup."""
        settings = get_settings()
        model_path = settings.MODEL_PATH

        logger.info(f"Loading model from {model_path}...")

        # Detect device
        if torch.cuda.is_available():
            self.device = torch.device("cuda")
            logger.info("Using CUDA GPU for inference")
        else:
            self.device = torch.device("cpu")
            logger.info("Using CPU for inference")

        # Load model and tokenizer (matches notebook logic)
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_path, local_files_only=True)
        self.model.to(self.device)
        self.model.eval()  # Set to evaluation mode

        self._is_loaded = True
        logger.info("Model loaded successfully")

    def warmup(self):
        """Run a dummy inference to warm up the model pipeline."""
        if not self._is_loaded:
            raise RuntimeError("Model not loaded. Call load_model() first.")

        logger.info("Warming up model...")
        dummy_text = "summarize: This is a warmup text to initialize the model pipeline."
        inputs = self.tokenizer(dummy_text, return_tensors="pt", max_length=64, truncation=True)
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        with torch.no_grad():
            self.model.generate(inputs["input_ids"], max_length=20)
        
        logger.info("Model warmup complete")

    def _get_cache_key(self, text: str, length: str) -> str:
        """Generate cache key from input text and parameters."""
        content = f"{text}::{length}"
        return hashlib.md5(content.encode()).hexdigest()

    def summarize(
        self,
        text: str,
        length: str = "medium",
        num_beams: int = 4,
        no_repeat_ngram_size: int = 3,
    ) -> str:
        """
        Generate a summary for the given text.
        
        Args:
            text: Article text to summarize.
            length: 'short', 'medium', or 'detailed'.
            num_beams: Beam search width. Higher = better quality, slower.
            no_repeat_ngram_size: Prevent repeated n-grams.
        
        Returns:
            Generated summary text.
        """
        if not self._is_loaded:
            raise RuntimeError("Model not loaded. Call load_model() first.")

        # Check cache
        cache_key = self._get_cache_key(text, length)
        if cache_key in self._cache:
            logger.debug("Cache hit for summary request")
            return self._cache[cache_key]

        settings = get_settings()
        preset = LENGTH_PRESETS.get(length, LENGTH_PRESETS["medium"])

        # Prepend the T5 prefix (from notebook: prefix = 'summarize:')
        input_text = f"{settings.MODEL_PREFIX} {text}"

        # Tokenize with truncation (matches notebook: max_length=1024)
        inputs = self.tokenizer(
            input_text,
            return_tensors="pt",
            max_length=settings.MODEL_MAX_INPUT_LENGTH,
            truncation=True,
            padding=False,
        )
        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        # Generate summary (matches notebook logic with enhanced params)
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

        # Decode (matches notebook: skip_special_tokens=True)
        summary = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Cache result
        self._cache[cache_key] = summary
        logger.debug(f"Generated summary ({length}): {len(summary)} chars")

        return summary

    def get_token_count(self, text: str) -> int:
        """Count tokens in the input text."""
        if not self._is_loaded:
            return len(text.split())  # Fallback to word count
        tokens = self.tokenizer.encode(text, add_special_tokens=False)
        return len(tokens)

    @property
    def is_loaded(self) -> bool:
        return self._is_loaded


# Global singleton
model_service = ModelService()
