# src/preprocess.py
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

stemmer = PorterStemmer()
STOPWORDS = set(stopwords.words("english"))

def normalize(text: str) -> list[str]:
    """
    Full pipeline: tokenize → lowercase → remove punctuation 
    → remove stopwords → stem.
    Returns list of normalized tokens WITH their positions preserved.
    """
    tokens = word_tokenize(text.lower())
    return [
        stemmer.stem(tok)
        for tok in tokens
        if tok.isalpha() and tok not in STOPWORDS
    ]

def tokenize_with_positions(text: str) -> list[tuple[str, int]]:
    """
    Returns (normalized_token, position) pairs.
    Position is the original word index — critical for phrase search.
    """
    tokens = word_tokenize(text.lower())
    result = []
    pos = 0
    for tok in tokens:
        if tok.isalpha():
            if tok not in STOPWORDS:
                result.append((stemmer.stem(tok), pos))
            pos += 1  # count ALL words for position, even stopwords
    return result