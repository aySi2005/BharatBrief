"""OpenAlex-backed external verification for generated summary claims."""

from __future__ import annotations

import re
from difflib import SequenceMatcher
from typing import Any

import httpx

from app.config import get_settings


STOPWORDS = {
    "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "can", "about", "into", "from", "with", "this",
    "that", "these", "those", "their", "there", "them", "they", "his", "her",
    "your", "you", "we", "our", "i", "me", "my", "he", "she", "it", "its",
    "for", "of", "on", "in", "at", "by", "to", "and", "or", "but", "if",
    "as", "also", "not", "no", "nor", "than", "too", "very", "just", "out",
}


class ExternalFactCheckService:
    """Perform best-effort external fact-checking using OpenAlex."""

    def __init__(self) -> None:
        self.settings = get_settings()

    def verify_claim(self, claim_text: str) -> dict[str, Any]:
        """Return an external support result for a claim."""
        if not self.settings.EXTERNAL_FACT_CHECK_ENABLED:
            return {
                "verified": False,
                "provider": None,
                "external_match_score": 0.0,
                "evidence": "External fact-checking is disabled.",
            }

        claim = (claim_text or "").strip()
        if len(claim) < 20:
            return {
                "verified": False,
                "provider": self.settings.EXTERNAL_FACT_CHECK_PROVIDER,
                "external_match_score": 0.0,
                "evidence": "Claim is too short for external verification.",
            }

        query = self._build_query(claim)

        try:
            with httpx.Client(timeout=self.settings.EXTERNAL_FACT_CHECK_TIMEOUT_SECONDS) as client:
                search_response = client.get(
                    "https://api.openalex.org/works",
                    params={
                        "search": query,
                        "per-page": 5,
                        "select": "id,display_name,abstract_inverted_index",
                    },
                )
                search_response.raise_for_status()
                search_data = search_response.json()
                results = search_data.get("results", [])

                if not results:
                    return {
                        "verified": False,
                        "provider": self.settings.EXTERNAL_FACT_CHECK_PROVIDER,
                        "external_match_score": 0.0,
                        "evidence": "No external OpenAlex match was found for this claim.",
                    }

                best_result = None
                best_score = 0.0

                for result in results:
                    evidence_text = self._build_external_text(result)
                    score = self._score_claim_against_text(claim, evidence_text)
                    if score > best_score:
                        best_score = score
                        best_result = result

                if not best_result or best_score < 0.25:
                    return {
                        "verified": False,
                        "provider": self.settings.EXTERNAL_FACT_CHECK_PROVIDER,
                        "external_match_score": round(best_score, 2),
                        "evidence": "External source did not provide strong support for this claim.",
                    }

                evidence = self._build_external_text(best_result)
                title = best_result.get("display_name") or "OpenAlex source"
                return {
                    "verified": True,
                    "provider": self.settings.EXTERNAL_FACT_CHECK_PROVIDER,
                    "external_match_score": round(best_score, 2),
                    "evidence": (
                        f"Matched external source '{title}' with a similarity score of {round(best_score, 2)}. "
                        f"Context: {self._clean_excerpt(evidence)}"
                    ),
                }
        except Exception as exc:
            return {
                "verified": False,
                "provider": self.settings.EXTERNAL_FACT_CHECK_PROVIDER,
                "external_match_score": 0.0,
                "evidence": f"External verification temporarily unavailable ({exc.__class__.__name__}).",
            }

    def _build_query(self, claim_text: str) -> str:
        tokens = self._tokenize(claim_text)
        filtered = [token for token in tokens if token not in STOPWORDS and len(token) > 2]
        if len(filtered) >= 2:
            return " ".join(filtered[:6])
        return claim_text[:120].strip()

    def _build_external_text(self, result: dict[str, Any]) -> str:
        chunks = []

        title = result.get("display_name")
        if title:
            chunks.append(title)

        abstract_inverted_index = result.get("abstract_inverted_index")
        if isinstance(abstract_inverted_index, dict):
            abstract_text = self._reconstruct_abstract(abstract_inverted_index)
            if abstract_text:
                chunks.append(abstract_text)

        return " ".join(chunks)

    def _reconstruct_abstract(self, abstract_inverted_index: dict[str, list[int]]) -> str:
        positions: dict[int, str] = {}

        for word, indices in abstract_inverted_index.items():
            for idx in indices:
                positions[idx] = word

        if not positions:
            return ""

        ordered_words = [positions[index] for index in sorted(positions)]
        return " ".join(ordered_words)

    def _score_claim_against_text(self, claim_text: str, source_text: str) -> float:
        claim_tokens = set(self._tokenize(claim_text))
        source_tokens = set(self._tokenize(source_text))

        if not claim_tokens or not source_tokens:
            return 0.0

        overlap = len(claim_tokens & source_tokens) / max(len(claim_tokens), 1)
        lexical_similarity = SequenceMatcher(
            None,
            self._normalize_text(claim_text),
            self._normalize_text(source_text),
        ).ratio()
        return min(1.0, (overlap * 0.7) + (lexical_similarity * 0.3))

    def _clean_excerpt(self, text: str) -> str:
        cleaned = re.sub(r"\s+", " ", text or "").strip()
        if len(cleaned) <= 220:
            return cleaned
        return f"{cleaned[:217]}..."

    def _normalize_text(self, text: str) -> str:
        text = text.lower()
        text = re.sub(r"[^\w\s]", " ", text, flags=re.UNICODE)
        return re.sub(r"\s+", " ", text).strip()

    def _tokenize(self, text: str) -> list[str]:
        return [
            token
            for token in re.findall(r"\w+", self._normalize_text(text), flags=re.UNICODE)
            if token and token not in STOPWORDS and len(token) > 2
        ]


external_fact_check_service = ExternalFactCheckService()
