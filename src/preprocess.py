# src/preprocess.py
import nltk
import pickle
from pathlib import Path
import collections
import json
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from src.index.inverted import InvertedIndex
from src.index.permuterm import PermutermTrie
from src.index.proximity import PositionalIndex

# inverted index, Permuterm B-Tree, and proximity index

stemmer = PorterStemmer()
STOPWORDS = set(stopwords.words("english"))

def normalize(text):
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

def tokenize_with_positions(text):
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

def build_inverted_index(files, meta):
    inverted_index = InvertedIndex()
    keys = list(meta)
    for i in range(len(files)):
        inverted_index.add_document(keys[i], files[i], meta[keys[i]])
    return inverted_index

def build_perm_trie(tokens):
    vocab = set()
    for key in tokens.keys():
        for token in tokens[key]:
            vocab.add(token)

    permuterm_trie = PermutermTrie()
    for term in vocab:
        permuterm_trie.insert(term)
    return permuterm_trie

def build_positional_index(tok_pos):
    pos_idx = PositionalIndex()
    for key in tok_pos.keys(): 
        pos_idx.add_document(key, tok_pos[key])
    return pos_idx

def build_indexes(tokens_by_book_id, tok_pos, meta):
    # set of all document ids
    inv_idx = build_inverted_index(tokens_by_book_id, meta)
    perm_trie = build_perm_trie(tokens_by_book_id)
    pos_idx = build_positional_index(tok_pos)
    return [inv_idx, perm_trie, pos_idx]
    
def main():
    directory = Path('data/books')
    txt_files = list(directory.glob('*.txt'))
    json_files = list(directory.glob('*.json'))

    metas_by_ids = {}
    files_tokens = {}
    files_tok_pos = {}
    for i in range(len(json_files)):
        book_id = None
        with open(json_files[i], 'r') as file:
            data = json.load(file)
            book_id = data["id"]
            metas_by_ids[book_id] = data
        with open(txt_files[i], 'r') as f:
            text = f.read()
            tokens = normalize(text)
            files_tokens[book_id] = tokens
            tok_pos = tokenize_with_positions(text)
            files_tok_pos[book_id] = tok_pos

    indexes = build_indexes(files_tokens, files_tok_pos, metas_by_ids)
    Path("data/indexes").mkdir(parents=True, exist_ok=True)

    names = ["inverted", "permuterm", "positional"]
    for name, idx in zip(names, indexes):
        with open(f"data/indexes/{name}.pkl", "wb") as f:
            pickle.dump(idx, f)

if __name__ == "__main__":
    main()
