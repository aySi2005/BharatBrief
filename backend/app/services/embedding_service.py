"""Lightweight embedding helpers for semantic similarity checks."""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class EmbeddingService:
    """Provide simple semantic similarity computations for text pairs."""

    def semantic_similarity(self, text_a: str, text_b: str) -> float:
        """Return a cosine similarity score between two text snippets."""
        a = (text_a or "").strip()
        b = (text_b or "").strip()

        if not a or not b:
            return 0.0

        vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        vectors = vectorizer.fit_transform([a, b])
        score = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
        return float(score)


embedding_service = EmbeddingService()
