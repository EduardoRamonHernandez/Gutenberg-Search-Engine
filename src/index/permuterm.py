# src/index/permuterm.py
import bisect

class PermutermIndex:
    def __init__(self):
        # sorted list of (rotation, original_term) pairs
        self._rotations: list[tuple[str, str]] = []

    def add_term(self, term: str):
        """Generate all rotations of term$ and store them."""
        s = term + "$"
        for i in range(len(s)):
            rotation = s[i:] + s[:i]
            bisect.insort(self._rotations, (rotation, term))

    def wildcard_lookup(self, pattern: str) -> set[str]:
        """
        Convert wildcard to rotation prefix and search.
        Only handles single * for now.
        """
        if "*" not in pattern:
            return {pattern}
        
        left, right = pattern.split("*", 1)
        # Rotate so the prefix we want is at the start
        # hel* → search prefix "hel$"  (left + "$")
        # *ing → search prefix "ing$"  (right + "$")  
        # hel*o → search prefix "o$hel" (right + "$" + left)
        if not left:
            prefix = right + "$"
        elif not right:
            prefix = left + "$"
        else:
            prefix = right + "$" + left

        return self._prefix_search(prefix)

    def _prefix_search(self, prefix: str) -> set[str]:
        """Binary search for all rotations starting with prefix."""
        lo = bisect.bisect_left(self._rotations, (prefix,))
        results = set()
        for rot, term in self._rotations[lo:]:
            if not rot.startswith(prefix):
                break
            results.add(term)
        return results