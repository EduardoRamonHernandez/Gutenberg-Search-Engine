# evaluate.py — MRR evaluation for the Gutenberg search engine
import pickle
from src.preprocess import normalize
from src.search import search

# All correct book IDs verified to be in the index before running.
# Phrase queries marked [stopword] contain a stopword between content words
# and are specifically testing the positional-index stopword fix.
TEST_QUERIES = [
    # --- keyword queries ---
    ("raskolnikov",  {2554}),     # Crime and Punishment
    ("gatsby",       {64317}),    # The Great Gatsby
    ("karamazov",    {28054}),    # The Brothers Karamazov
    ("zarathustra",  {1998}),     # Thus Spake Zarathustra
    ("huckleberry",  {76}),       # Adventures of Huckleberry Finn
    ("dracula",      {345}),      # Dracula
    ("beowulf",      {16328}),    # Beowulf
    ("odysseus",     {1727}),     # The Odyssey
    ("leviathan",    {3207}),     # Leviathan
    ("gregor",       {5200}),     # Metamorphosis (Gregor Samsa)

    # --- phrase queries (no stopwords between content words) ---
    ('"dorian gray"',       {174}),           # The Picture of Dorian Gray
    ('"sherlock holmes"',   {1661, 244, 2852}),# any Doyle book
    ('"great expectations"',{1400}),           # Great Expectations

    # --- phrase queries testing stopword fix ---
    ('"war and peace"',     {2600}),  # [stopword] "and" between war/peace
    ('"jekyll and hyde"',   {43}),    # [stopword] "and" between jekyll/hyde

    # --- wildcard queries ---
    ("dracul*",     {345}),       # Dracula
    ("karamaz*",    {28054}),     # The Brothers Karamazov
    ("zarathustr*", {1998}),      # Thus Spake Zarathustra
    ("huckleberr*", {76}),        # Adventures of Huckleberry Finn
    ("raskolnik*",  {2554}),      # Crime and Punishment
]


def evaluate():
    with open("data/indexes/inverted.pkl", "rb") as f:
        inverted = pickle.load(f)
    with open("data/indexes/permuterm.pkl", "rb") as f:
        permuterm = pickle.load(f)
    with open("data/indexes/positional.pkl", "rb") as f:
        positional = pickle.load(f)

    rows = []
    for query, correct_ids in TEST_QUERIES:
        results = search(query, inverted, permuterm, positional)
        result_ids = {r["id"] for r in results}
        found = bool(correct_ids & result_ids)
        rr = 1.0 if found else 0.0
        correct_title = inverted.metadata.get(next(iter(correct_ids)), {}).get("title", "?")
        rows.append({
            "query":   query,
            "correct": correct_title,
            "found":   found,
            "n":       len(results),
            "rr":      rr,
        })

    mrr = sum(r["rr"] for r in rows) / len(rows)
    return mrr, rows


if __name__ == "__main__":
    mrr, rows = evaluate()
    n_correct = sum(r["found"] for r in rows)

    print(f"\n{'Query':<30} {'Expected':<35} {'Found':<6} N")
    print("-" * 80)
    for r in rows:
        mark = "YES" if r["found"] else "NO "
        print(f"{r['query']:<30} {r['correct'][:33]:<35} {mark:<6} {r['n']}")

    print("-" * 80)
    print(f"\nMRR: {mrr:.3f}  ({n_correct}/{len(rows)} queries retrieved correct book)\n")
