"""Summary verification utilities.

This lightweight checker provides a first-pass hallucination-detection workflow by
comparing each summary sentence against the source text using lexical overlap,
sentence similarity, and numeric consistency checks. It remains dependency-free so
it can run even when the model is offline.
"""

import re
from difflib import SequenceMatcher
from typing import Any

from app.services.embedding_service import embedding_service
from app.services.external_fact_check_service import external_fact_check_service


STOPWORDS = {
    "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "can", "about", "into", "from", "with", "this",
    "that", "these", "those", "their", "there", "them", "they", "his", "her",
    "your", "you", "we", "our", "i", "me", "my", "he", "she", "it", "its",
    "for", "of", "on", "in", "at", "by", "to", "and", "or", "but", "if",
    "as", "also", "not", "no", "nor", "than", "too", "very", "just", "out",
}


def _normalize_text(text: str) -> str:
    """Normalize text for robust sentence matching."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _split_sentences(text: str) -> list[str]:
    """Split text into sentences while preserving the original text."""
    return [segment.strip() for segment in re.split(r"(?<=[.!?])\s+", text) if segment.strip()]


def _content_tokens(text: str) -> list[str]:
    """Extract content-bearing tokens from a sentence."""
    return [token for token in re.findall(r"[a-z0-9]+", _normalize_text(text)) if token not in STOPWORDS and len(token) > 2]


def _extract_numbers(text: str) -> list[str]:
    """Return numeric-like values from a sentence."""
    return re.findall(r"\d[\d,\.\-]*", text)


def _sentence_support_score(summary_sentence: str, source_sentences: list[str]) -> tuple[float, str, str, bool]:
    """Score a summary sentence against the source and return evidence."""
    summary_tokens = set(_content_tokens(summary_sentence))
    summary_numbers = _extract_numbers(summary_sentence)

    if not summary_tokens:
        return 0.0, "unsupported", "The sentence did not contain enough meaningful content to verify.", False

    best_source = None
    best_score = 0.0
    best_numbers = []

    for source_sentence in source_sentences:
        source_tokens = set(_content_tokens(source_sentence))
        if not source_tokens:
            continue

        overlap = len(summary_tokens & source_tokens) / max(len(summary_tokens), 1)
        lexical_similarity = SequenceMatcher(None, _normalize_text(summary_sentence), _normalize_text(source_sentence)).ratio()
        semantic_similarity = embedding_service.semantic_similarity(summary_sentence, source_sentence)
        score = (overlap * 0.5) + (lexical_similarity * 0.2) + (semantic_similarity * 0.3)

        if score > best_score:
            best_score = score
            best_source = source_sentence
            best_numbers = _extract_numbers(source_sentence)

    has_conflicting_numbers = bool(summary_numbers and best_numbers and summary_numbers != best_numbers)

    if has_conflicting_numbers:
        adjusted_score = best_score * 0.35
        return (
            round(adjusted_score, 2),
            "unsupported",
            f"The claim overlaps with the source text, but numeric details differ from the source (summary: {summary_numbers}, source: {best_numbers}).",
            True,
        )

    if best_score >= 0.45:
        return (
            round(best_score, 2),
            "supported",
            f"Strong overlap with the source sentence: \"{best_source}\"",
            False,
        )

    return (
        round(best_score, 2),
        "unsupported",
        f"Only weak overlap with the source text. This claim may be inferred rather than directly supported.",
        False,
    )


def verify_summary_claims(
    source_text: str,
    summary_text: str,
    external_fact_check_enabled: bool | None = None,
) -> dict[str, Any]:
    """
    Compare summary sentences against the source text and report claim support.

    This is a lightweight verification pass rather than a full claim-extraction
    system. It scores each summary sentence by lexical overlap with the source,
    then flags conflicts in numeric details or weak support as needing review.
    """
    source_sentences = _split_sentences(source_text)
    summary_sentences = _split_sentences(summary_text)
    external_fact_check_enabled = (
        external_fact_check_enabled
        if external_fact_check_enabled is not None
        else external_fact_check_service.settings.EXTERNAL_FACT_CHECK_ENABLED
    )

    if not summary_sentences:
        return {
            "supported_claims": 0,
            "unsupported_claims": 0,
            "reliability_score": 1.0,
            "claims": [],
            "external_fact_check_enabled": external_fact_check_enabled,
        }

    claims = []
    supported = 0

    for sentence in summary_sentences:
        score, status, evidence, _ = _sentence_support_score(sentence, source_sentences)
        if status == "supported":
            supported += 1

        external_result = (
            external_fact_check_service.verify_claim(sentence)
            if external_fact_check_enabled
            else {
                "verified": False,
                "provider": None,
                "external_match_score": 0.0,
                "evidence": "External fact-checking is disabled.",
            }
        )

        claims.append(
            {
                "text": sentence,
                "status": status,
                "support_score": score,
                "evidence": evidence,
                "external_verified": external_result.get("verified", False),
                "external_provider": external_result.get("provider"),
                "external_match_score": external_result.get("external_match_score"),
                "external_evidence": external_result.get("evidence"),
            }
        )

    total_claims = len(claims)
    reliability_score = round(supported / total_claims, 2) if total_claims else 1.0

    return {
        "supported_claims": supported,
        "unsupported_claims": total_claims - supported,
        "reliability_score": reliability_score,
        "claims": claims,
        "external_fact_check_enabled": external_fact_check_enabled,
    }
