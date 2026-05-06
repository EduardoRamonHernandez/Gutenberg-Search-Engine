import pickle
inv = pickle.load(open('data/indexes/inverted.pkl', 'rb'))
ids_to_check = [28054, 64317, 84, 1342, 2554, 345, 76, 1998, 3207, 1727, 16328, 174, 1400, 2600, 98, 11, 43, 100, 5200]
for book_id in ids_to_check:
    if book_id in inv.metadata:
        print(f"IN  {book_id} | {inv.metadata[book_id]['title'][:50]}")
    else:
        print(f"OUT {book_id}")
