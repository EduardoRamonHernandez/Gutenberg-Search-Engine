# src/index/inverted.py
import math
from collections import defaultdict, Counter

class InvertedIndex:
    def __init__(self):
        self.index: dict[str, dict[int, int]] = defaultdict(dict)  # term → {doc_id → tf}
        self.metadata: dict[int, dict] = {}
        self.doc_lengths: dict[int, int] = {}  # doc_id → total token count
        self.idf: dict[str, float] = {}

    def add_document(self, book_id, tokens, meta):
        self.metadata[book_id] = meta
        self.doc_lengths[book_id] = len(tokens)
        freq = Counter(tokens)
        for token, count in freq.items():
            self.index[token][book_id] = count

    def compute_idf(self):
        """Call once after all documents are added."""
        N = len(self.metadata)
        for term, postings in self.index.items():
            df = len(postings)
            self.idf[term] = math.log((N + 1) / (df + 1))

    def score_and(self, terms) -> list[tuple[int, float]]:
        """Intersect postings, score each doc by TF-IDF, return ranked list."""
        if not terms:
            return []
        sets = [set(self.index.get(t, {}).keys()) for t in terms]
        doc_ids = set.intersection(*sets)
        scored = []
        for doc_id in doc_ids:
            doc_len = self.doc_lengths.get(doc_id, 1)
            score = 0.0
            for term in terms:
                tf = self.index[term].get(doc_id, 0) / doc_len
                score += tf * self.idf.get(term, 0.0)
            scored.append((doc_id, score))
        return sorted(scored, key=lambda x: x[1], reverse=True)

    def search_and(self, terms) -> set:
        """Intersect postings lists — used by phrase/wildcard paths."""
        if not terms:
            return set()
        sets = [set(self.index.get(t, {}).keys()) for t in terms]
        return set.intersection(*sets)

    def search_or(self, terms) -> set:
        """Union postings lists — used by wildcard path."""
        result = set()
        for t in terms:
            result |= set(self.index.get(t, {}).keys())
        return result
