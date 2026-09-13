"""Translation helpers for multilingual summaries."""

import logging
from typing import Dict

from deep_translator import GoogleTranslator

logger = logging.getLogger(__name__)


LANGUAGE_CODES: Dict[str, str] = {
    "english": "en",
    "hindi": "hi",
    "french": "fr",
    "spanish": "es",
    "arabic": "ar",
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
    """Provides lightweight multilingual translation."""

    def __init__(self):
        self._translators = {}

    def normalize_target_language(
        self,
        target_language: str | None,
    ) -> str | None:

        if not target_language:
            return None

        normalized = target_language.strip().lower()

        return LANGUAGE_ALIASES.get(normalized)

    def _get_translator(
        self,
        language: str,
    ):

        if language not in self._translators:

            target_code = LANGUAGE_CODES[language]

            self._translators[language] = GoogleTranslator(
                source="auto",
                target=target_code,
            )

        return self._translators[language]

    def translate_text(
        self,
        text: str,
        target_language: str | None,
    ) -> str:

        if not text or not text.strip():
            return text

        normalized_language = (
            self.normalize_target_language(
                target_language
            )
        )

        if (
            not normalized_language
            or normalized_language == "english"
        ):
            return text

        if normalized_language not in LANGUAGE_CODES:

            logger.warning(
                "Unsupported target language: %s",
                target_language,
            )

            return text

        try:

            translator = self._get_translator(
                normalized_language
            )

            translated = translator.translate(
                text
            )

            return translated.strip() if translated else text

        except Exception as exc:

            logger.warning(
                "Translation failed for %s: %s",
                normalized_language,
                exc,
            )

            return text

    def translate_response_fields(
        self,
        response,
        target_language: str | None,
    ):
        """Translate summary fields while preserving verification data."""

        normalized = self.normalize_target_language(
            target_language
        )

        if (
            not normalized
            or normalized == "english"
        ):
            return response

        try:

            response.summary = self.translate_text(
                response.summary,
                normalized,
            )

            if response.headline:
                response.headline = self.translate_text(
                    response.headline,
                    normalized,
                )

            if response.key_points:
                response.key_points = [
                    self.translate_text(
                        point,
                        normalized,
                    )
                    for point in response.key_points
                ]

            if response.bullet_summary:
                response.bullet_summary = self.translate_text(
                    response.bullet_summary,
                    normalized,
                )

        except Exception as exc:

            logger.warning(
                "Translation failed for %s: %s. "
                "Returning English output.",
                normalized,
                exc,
            )

        return response


translation_service = TranslationService()