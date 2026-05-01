# src/search.py

from src.preprocess import normalize, tokenize_with_positions
from src.index.inverted import InvertedIndex
from src.index.permuterm import PermutermIndex
from src.index.proximity import PositionalIndex

def detect_query_type(query: str) -> str:
    if query.startswith('"') and query.endswith('"'):
        return "phrase"
    if "*" in query:
        return "wildcard"
    return "keyword"

def search(query: str, inverted: InvertedIndex, 
           permuterm: PermutermIndex, positional: PositionalIndex) -> list[dict]:
    
    qtype = detect_query_type(query)
    
    if qtype == "phrase":
        # Strip quotes, normalize each term, use positional index
        raw = query.strip('"')
        terms = normalize(raw)
        doc_ids = positional.phrase_search(terms)
    
    elif qtype == "wildcard":
        # Expand wildcard → matching vocab terms → inverted index
        matching_terms = permuterm.wildcard_lookup(query.lower())
        doc_ids = inverted.search_or(list(matching_terms))
    
    else:
        # AND search on all normalized terms
        terms = normalize(query)
        doc_ids = inverted.search_and(terms)

    return [inverted.metadata[d] for d in doc_ids]