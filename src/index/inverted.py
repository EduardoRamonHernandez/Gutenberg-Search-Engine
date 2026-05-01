# src/index/inverted.py
from collections import defaultdict

class InvertedIndex:
    def __init__(self):
        self.index: dict[str, set[int]] = defaultdict(set)
        self.metadata: dict[int, dict] = {}  # id → {title, author}

    def add_document(self, book_id: int, tokens: list[str], meta: dict):
        self.metadata[book_id] = meta
        for token in tokens:
            self.index[token].add(book_id)

    def search_and(self, terms: list[str]) -> set[int]:
        """Intersect postings lists — all terms must appear."""
        if not terms:
            return set()
        sets = [self.index.get(t, set()) for t in terms]
        return set.intersection(*sets)

    def search_or(self, terms: list[str]) -> set[int]:
        """Union postings lists — any term matches."""
        result = set()
        for t in terms:
            result |= self.index.get(t, set())
        return result