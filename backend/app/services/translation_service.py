"""Translation helpers for multilingual summaries."""
import logging
from typing import Dict, Tuple

import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

logger = logging.getLogger(__name__)

SUPPORTED_LANGUAGE_MODELS: Dict[str, str] = {
    "hindi": "Helsinki-NLP/opus-mt-en-hi",
    "french": "Helsinki-NLP/opus-mt-en-fr",
    "spanish": "Helsinki-NLP/opus-mt-en-es",
    "arabic": "Helsinki-NLP/opus-mt-en-ar",
}

LANGUAGE_ALIASES = {
    "en": "english",
    "english": "english",
    "hi": "hindi",
    "hindi": "hindi",
    "fr": "french",
    "french": "french",
    "es": "spanish",
    "spanish": "spanish",
    "ar": "arabic",
    "arabic": "arabic",
}


class TranslationService:
    """Lazy-load translation models for requested output languages."""

    def __init__(self):
        self._loaded_models: Dict[str, Tuple[AutoTokenizer, AutoModelForSeq2SeqLM, torch.device]] = {}

    def normalize_target_language(self, target_language: str | None) -> str | None:
        if not target_language:
            return None

        normalized = target_language.strip().lower()
        if normalized in LANGUAGE_ALIASES:
            return LANGUAGE_ALIASES[normalized]

        return None

    def translate_text(self, text: str, target_language: str | None) -> str:
        if not text:
            return text

        normalized_language = self.normalize_target_language(target_language)
        if not normalized_language or normalized_language == "english":
            return text

        if normalized_language not in SUPPORTED_LANGUAGE_MODELS:
            logger.warning(
                "Unsupported target language requested: %s. Returning original text.",
                target_language,
            )
            return text

        if normalized_language not in self._loaded_models:
            self._load_model(normalized_language)

        tokenizer, model, device = self._loaded_models[normalized_language]

        inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
        inputs = {key: value.to(device) for key, value in inputs.items()}

        with torch.no_grad():
            generated = model.generate(
                **inputs,
                max_new_tokens=200,
                num_beams=4,
                do_sample=False,
                early_stopping=True,
            )

        translated = tokenizer.decode(generated[0], skip_special_tokens=True)
        return translated.strip()

    def _load_model(self, language: str) -> None:
        model_name = SUPPORTED_LANGUAGE_MODELS[language]
        logger.info("Loading translation model for %s: %s", language, model_name)

        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        model.to(device)
        model.eval()

        self._loaded_models[language] = (tokenizer, model, device)
        logger.info("Translation model loaded for %s", language)

    def translate_response_fields(self, response, target_language: str | None):
        """Translate summary response fields while preserving verification data."""
        normalized = self.normalize_target_language(target_language)
        if not normalized or normalized == "english":
            return response

        try:
            response.summary = self.translate_text(response.summary, normalized)
            if response.headline:
                response.headline = self.translate_text(response.headline, normalized)
            if response.key_points:
                response.key_points = [self.translate_text(point, normalized) for point in response.key_points]
            if response.bullet_summary:
                response.bullet_summary = self.translate_text(response.bullet_summary, normalized)
        except Exception as exc:
            logger.warning("Translation failed for %s: %s. Returning English output.", normalized, exc)

        return response


translation_service = TranslationService()
