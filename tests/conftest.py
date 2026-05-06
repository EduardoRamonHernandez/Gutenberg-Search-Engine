import sys
import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from src.index.inverted import InvertedIndex
from src.index.permuterm import PermutermTrie
from src.index.proximity import PositionalIndex
from src.preprocess import normalize, tokenize_with_positions

BOOKS = {
    1: {"id": 1, "title": "Moby Dick", "author": "Melville, Herman"},
    2: {"id": 2, "title": "Dracula",   "author": "Stoker, Bram"},
    3: {"id": 3, "title": "Gatsby",    "author": "Fitzgerald"},
}

TEXTS = {
    1: "captain ahab hunted the white whale across the ocean",
    2: "dracula the vampire lived in a castle in transylvania",
    3: "gatsby threw lavish parties near the green light",
}

def _build_indexes():
    inverted = InvertedIndex()
    permuterm = PermutermTrie()
    positional = PositionalIndex()
    for book_id, text in TEXTS.items():
        tokens = normalize(text)
        tok_pos = tokenize_with_positions(text)
        inverted.add_document(book_id, tokens, BOOKS[book_id])
        positional.add_document(book_id, tok_pos)
    inverted.compute_idf()
    for term in inverted.index:
        permuterm.insert(term)
    return inverted, permuterm, positional


@pytest.fixture(scope="session")
def client():
    inv, perm, pos = _build_indexes()
    # Evict any cached import of src.api so our patches apply at import time
    sys.modules.pop("src.api", None)
    fake_open = MagicMock()
    pickle_loads = [inv, perm, pos]
    with patch("builtins.open", fake_open), \
         patch("pickle.load", side_effect=pickle_loads):
        import src.api as api_module
        api_module.inverted  = inv
        api_module.permuterm = perm
        api_module.positional = pos
        yield TestClient(api_module.app)
