# evaluate.py
import pickle
from src.preprocess import normalize
from src.search import search

# Keyword queries: (query, correct_book_ids)
# Results are now TF-IDF ranked — we measure P@1 (is #1 result correct?)
# and MRR (rank of first correct result).
KEYWORD_QUERIES = [
    ("raskolnikov",  {2554}),
    ("gatsby",       {64317}),
    ("karamazov",    {28054}),
    ("zarathustra",  {1998}),
    ("huckleberry",  {76}),
    ("dracula",      {345}),
    ("beowulf",      {16328}),
    ("odysseus",     {1727}),
    ("leviathan",    {3207}),
    ("gregor",       {5200}),
]

# Phrase queries: unranked, measure retrieval only (found yes/no)
PHRASE_QUERIES = [
    ('"dorian gray"',        {174}),
    ('"sherlock holmes"',    {1661, 244, 2852}),
    ('"great expectations"', {1400}),
    ('"war and peace"',      {2600}),   # stopword test
    ('"jekyll and hyde"',    {43}),     # stopword test
]

# Wildcard queries: unranked, measure retrieval only
WILDCARD_QUERIES = [
    ("dracul*",     {345}),
    ("karamaz*",    {28054}),
    ("zarathustr*", {1998}),
    ("huckleberr*", {76}),
    ("raskolnik*",  {2554}),
]


def load_indexes():
    with open("data/indexes/inverted.pkl", "rb") as f:
        inverted = pickle.load(f)
    with open("data/indexes/permuterm.pkl", "rb") as f:
        permuterm = pickle.load(f)
    with open("data/indexes/positional.pkl", "rb") as f:
        positional = pickle.load(f)
    return inverted, permuterm, positional


def evaluate():
    inverted, permuterm, positional = load_indexes()

    # --- Keyword: P@1 and MRR ---
    kw_rows = []
    for query, correct_ids in KEYWORD_QUERIES:
        results = search(query, inverted, permuterm, positional)
        p_at_1 = len(results) > 0 and results[0]["id"] in correct_ids
        rr = 0.0
        for rank, r in enumerate(results, start=1):
            if r["id"] in correct_ids:
                rr = 1.0 / rank
                break
        title = inverted.metadata.get(next(iter(correct_ids)), {}).get("title", "?")
        top = results[0]["title"][:30] if results else "—"
        kw_rows.append({"query": query, "correct": title, "p1": p_at_1, "rr": rr,
                        "n": len(results), "top": top})

    # --- Phrase + Wildcard: retrieval only ---
    other_rows = []
    for query, correct_ids in PHRASE_QUERIES + WILDCARD_QUERIES:
        results = search(query, inverted, permuterm, positional)
        result_ids = {r["id"] for r in results}
        found = bool(correct_ids & result_ids)
        title = inverted.metadata.get(next(iter(correct_ids)), {}).get("title", "?")
        other_rows.append({"query": query, "correct": title, "found": found, "n": len(results)})

    p_at_1 = sum(r["p1"] for r in kw_rows) / len(kw_rows)
    mrr     = sum(r["rr"] for r in kw_rows) / len(kw_rows)
    retrieval = sum(r["found"] for r in other_rows) / len(other_rows)

    return kw_rows, other_rows, p_at_1, mrr, retrieval


if __name__ == "__main__":
    kw_rows, other_rows, p_at_1, mrr, retrieval = evaluate()

    print("\n=== KEYWORD QUERIES (TF-IDF ranked) ===")
    print(f"{'Query':<20} {'Expected':<30} {'Top Result':<32} P@1   RR    N")
    print("-" * 100)
    for r in kw_rows:
        print(f"{r['query']:<20} {r['correct'][:28]:<30} {r['top']:<32} "
              f"{'YES' if r['p1'] else 'NO ':<6}{r['rr']:.2f}  {r['n']}")
    print(f"\nP@1: {p_at_1:.3f}   MRR: {mrr:.3f}")

    print("\n=== PHRASE + WILDCARD QUERIES (unranked retrieval) ===")
    print(f"{'Query':<30} {'Expected':<35} {'Found':<6} N")
    print("-" * 80)
    for r in other_rows:
        print(f"{r['query']:<30} {r['correct'][:33]:<35} {'YES' if r['found'] else 'NO ':<6} {r['n']}")
    print(f"\nRetrieval rate: {retrieval:.3f}  ({sum(r['found'] for r in other_rows)}/{len(other_rows)})")
