"""NLP utilities: sentiment, keywords, readability, key points."""
import re
import math
import logging
from collections import Counter

logger = logging.getLogger(__name__)


def analyze_sentiment(text: str) -> tuple[str, float]:
    """
    Analyze sentiment of text. Returns (label, score).
    Uses TextBlob for simple polarity analysis.
    """
    try:
        from textblob import TextBlob
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity  # -1 to 1
        
        if polarity > 0.1:
            label = "positive"
        elif polarity < -0.1:
            label = "negative"
        else:
            label = "neutral"
        
        return label, round(polarity, 3)
    except Exception as e:
        logger.warning(f"Sentiment analysis failed: {e}")
        return "neutral", 0.0


def extract_keywords(text: str, top_n: int = 8) -> list[str]:
    """Extract top keywords using TF-based scoring (no external models needed)."""
    # Simple stopwords
    stopwords = {
        "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
        "have", "has", "had", "do", "does", "did", "will", "would", "could",
        "should", "may", "might", "shall", "can", "need", "dare", "ought",
        "used", "to", "of", "in", "for", "on", "with", "at", "by", "from",
        "as", "into", "through", "during", "before", "after", "above", "below",
        "between", "out", "off", "over", "under", "again", "further", "then",
        "once", "here", "there", "when", "where", "why", "how", "all", "both",
        "each", "few", "more", "most", "other", "some", "such", "no", "nor",
        "not", "only", "own", "same", "so", "than", "too", "very", "just",
        "don", "now", "and", "but", "or", "if", "while", "that", "this",
        "these", "those", "it", "its", "he", "she", "they", "them", "his",
        "her", "their", "what", "which", "who", "whom", "said", "also",
        "new", "one", "two", "first", "last", "many", "much", "well",
        "i", "me", "my", "we", "our", "you", "your", "up", "about",
    }

    # Tokenize and clean
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
    filtered = [w for w in words if w not in stopwords]
    
    # Count frequencies
    freq = Counter(filtered)
    
    # Get top keywords
    keywords = [word for word, _ in freq.most_common(top_n)]
    return keywords


def calculate_readability(text: str) -> float:
    """
    Calculate Flesch-Kincaid readability score.
    Higher score = easier to read. Range: 0-100.
    """
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    words = re.findall(r'\b\w+\b', text)
    
    if not sentences or not words:
        return 50.0
    
    # Count syllables (simple heuristic)
    syllable_count = sum(_count_syllables(w) for w in words)
    
    word_count = len(words)
    sentence_count = len(sentences)
    
    if word_count == 0 or sentence_count == 0:
        return 50.0
    
    # Flesch Reading Ease formula
    score = 206.835 - 1.015 * (word_count / sentence_count) - 84.6 * (syllable_count / word_count)
    return round(max(0, min(100, score)), 1)


def _count_syllables(word: str) -> int:
    """Estimate syllable count for a word."""
    word = word.lower().strip()
    if len(word) <= 3:
        return 1
    
    vowels = "aeiou"
    count = 0
    prev_vowel = False
    
    for char in word:
        is_vowel = char in vowels
        if is_vowel and not prev_vowel:
            count += 1
        prev_vowel = is_vowel
    
    # Adjust for silent 'e'
    if word.endswith("e") and count > 1:
        count -= 1
    
    return max(1, count)


def estimate_reading_time(word_count: int, wpm: int = 238) -> int:
    """Estimate reading time in seconds."""
    return max(1, round(word_count / wpm * 60))


def extract_key_points(text: str, max_points: int = 5) -> list[str]:
    """
    Extract key points from text using sentence scoring.
    Uses a simple extractive approach based on keyword density.
    """
    # Split into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
    
    if len(sentences) <= max_points:
        return sentences
    
    # Score sentences by keyword density
    keywords = set(extract_keywords(text, top_n=15))
    
    scored = []
    for i, sent in enumerate(sentences):
        words = set(re.findall(r'\b[a-zA-Z]{3,}\b', sent.lower()))
        keyword_overlap = len(words & keywords)
        
        # Boost first and last sentences (typically important)
        position_bonus = 0
        if i < 2:
            position_bonus = 2
        elif i >= len(sentences) - 2:
            position_bonus = 1
        
        score = keyword_overlap + position_bonus
        scored.append((score, i, sent))
    
    # Sort by score, take top N, then sort by position
    scored.sort(key=lambda x: x[0], reverse=True)
    top = scored[:max_points]
    top.sort(key=lambda x: x[1])  # Restore original order
    
    return [s[2] for s in top]


def generate_headline(text: str, summary: str = None) -> str:
    """Generate a headline from text or summary."""
    source = summary if summary else text
    
    # Take first sentence
    sentences = re.split(r'[.!?]', source)
    first = sentences[0].strip() if sentences else source[:100]
    
    # Truncate if too long
    if len(first) > 100:
        words = first.split()
        first = " ".join(words[:12])
        if not first.endswith((".", "!", "?")):
            first = first.rstrip(",;:") + "..."
    
    return first


def create_bullet_summary(key_points: list[str]) -> str:
    """Format key points as a bullet-point summary."""
    return "\n".join(f"• {point}" for point in key_points)


def calculate_confidence(original_length: int, summary_length: int) -> float:
    """
    Estimate confidence score based on compression ratio and length.
    This is a heuristic — not a true model confidence.
    """
    if original_length == 0:
        return 0.5
    
    ratio = summary_length / original_length
    
    # Sweet spot: 10-30% compression
    if 0.05 <= ratio <= 0.35:
        confidence = 0.85 + (0.15 * (1 - abs(ratio - 0.15) / 0.2))
    elif ratio > 0.35:
        confidence = max(0.5, 0.85 - (ratio - 0.35))
    else:
        confidence = max(0.5, 0.7 + ratio * 2)
    
    return round(min(0.98, confidence), 2)
