# src/index/proximity.py

class PositionalIndex:
    def __init__(self):
        # token → {book_id → [position, position, ...]}
        self.index = {}

    def add_document(self, book_id, token_positions: list[tuple[str, int]]):
        for token, pos in token_positions:
            if token not in self.index:
                self.index[token] = {}
            if book_id not in self.index[token]:
                self.index[token][book_id] = []
            self.index[token][book_id].append(pos)

    def phrase_search(self, terms: list[str]) -> set[int]:
        """
        Find books where terms appear consecutively.
        Core algorithm: for each candidate doc, check if any 
        position p exists where terms[0]@p, terms[1]@p+1, ...
        """
        if not terms:
            return set()
        
        # Start with docs containing the first term
        candidate_docs = set(self.index.get(terms[0], {}).keys())
        for term in terms[1:]:
            candidate_docs &= set(self.index.get(term, {}).keys())

        results = set()
        for doc_id in candidate_docs:
            if self._consecutive_positions(doc_id, terms):
                results.add(doc_id)
        return results

    def _consecutive_positions(self, doc_id: int, terms: list[str]) -> bool:
        """Check if terms appear in sequence at any position in this doc."""
        first_positions = self.index[terms[0]][doc_id]
        for start_pos in first_positions:
            if all(
                start_pos + i in self.index[terms[i]].get(doc_id, [])
                for i in range(1, len(terms))
            ):
                return True
        return False