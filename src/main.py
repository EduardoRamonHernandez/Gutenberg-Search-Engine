# main.py
# simple driver
import pickle
from src.search import search

def load_indexes():
    inv_idx = None
    perm_trie = None
    pos_idx = None
    with open("data/indexes/inverted.pkl", "rb") as f:
        inv_idx = pickle.load(f)

    with open("data/indexes/permuterm.pkl", "rb") as f:
        perm_trie = pickle.load(f)

    with open("data/indexes/positional.pkl", "rb") as f:
        pos_idx = pickle.load(f)
    
    return [inv_idx, perm_trie, pos_idx]

def main():
    idx_loaded = False
    indexes = []
    while True:
        print("\nMENU\n QUERY TYPE: phrase, wildcard, simple\n USAGE: {query}\n")

        inp = input("Type 'exit' to quit\n")
        if inp == "exit":
            break

        if not idx_loaded:
            indexes = load_indexes()
            idx_loaded = True
        
        result = search(inp, indexes[0], indexes[1], indexes[2])
        print(result)


if __name__ == "__main__":
    main()
