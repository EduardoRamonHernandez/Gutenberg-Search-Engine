# src/search.py

from src.preprocess import normalize, tokenize_with_positions
from src.index.inverted import InvertedIndex
from src.index.permuterm import PermutermTrie
from src.index.proximity import PositionalIndex

def _detect_query_type(query):
    if query.startswith('"') and query.endswith('"'):
        return "phrase"
    if "*" in query:
        return "wildcard"
    return "keyword"

def search(query, inverted, permuterm, positional):
    qtype = _detect_query_type(query)

    if qtype == "phrase":
        raw = query.strip('"')
        terms = normalize(raw)
        doc_ids = positional.phrase_search(terms)
        return [{"score": None, **inverted.metadata[d]} for d in doc_ids]

    elif qtype == "wildcard":
        matching_terms = permuterm.wildcard_search(query.lower())
        doc_ids = inverted.search_or(list(matching_terms))
        return [{"score": None, **inverted.metadata[d]} for d in doc_ids]

    else:
        terms = normalize(query)
        scored = inverted.score_and(terms)[:15]
        return [{"score": round(score, 4), **inverted.metadata[d]} for d, score in scored]
