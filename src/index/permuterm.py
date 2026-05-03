# src/index/permuterm.py

class TrieNode:
    def __init__(self):
        self.children: dict[str, TrieNode] = {}
        self.terms: set[str] = set()  # original terms that produced this rotation

class PermutermTrie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, term):
        """Generate all rotations of term$ and insert into trie."""
        s = term + "$"
        for i in range(len(s)):
            rotation = s[i:] + s[:i]
            self._insert_rotation(rotation, term)

    def _insert_rotation(self, rotation, original_term):
        node = self.root
        for char in rotation:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.terms.add(original_term)

    def prefix_search(self, prefix):
        """Find all original terms whose rotation starts with prefix."""
        node = self.root
        for char in prefix:
            if char not in node.children:
                return set()  # no matches
            node = node.children[char]
        # collect all terms in this subtree
        return self._collect(node)

    def _collect(self, node):
        """DFS to gather all terms stored in this subtree."""
        results = node.terms.copy()
        for child in node.children.values():
            results |= self._collect(child)
        return results

    def wildcard_search(self, pattern):
        """
        Convert wildcard pattern to rotation prefix, then search.
        Handles: hel* / *ing / hel*o
        """
        if "*" not in pattern:
            return self.prefix_search(pattern + "$")

        left, right = pattern.split("*", 1)

        if not left:
            prefix = right + "$"        
        elif not right:
            prefix = left + "$"         
        else:
            prefix = right + "$" + left 

        return self.prefix_search(prefix)