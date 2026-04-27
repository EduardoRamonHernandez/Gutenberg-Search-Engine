# CLAUDE.md — Gutenberg Search Engine

## Project Overview

Undergraduate class project: a search engine over ~1,000 public domain books from Project Gutenberg. Users can search by keyword, wildcard, and phrase, getting results with title and author.

**This is a class project, not production software.** Keep things simple, readable, and well-commented. Prefer clarity over cleverness. No over-engineering.

## Architecture

```
gutenberg-search/
├── CLAUDE.md
├── README.md
├── requirements.txt
├── .gitignore
│
├── src/                    # All Python backend code
│   ├── __init__.py
│   ├── download.py         # Gutendex API fetcher → saves raw texts
│   ├── preprocess.py       # NLTK tokenization & normalization
│   ├── index/
│   │   ├── __init__.py
│   │   ├── inverted.py     # Inverted index (keyword search)
│   │   ├── permuterm.py    # Permuterm B-Tree (wildcard search)
│   │   └── proximity.py   # Positional/proximity index (phrase search)
│   ├── search.py           # Query parser + search dispatcher
│   └── cli.py              # Terminal interface (entry point)
│
├── data/                   # Gitignored — regenerable
│   ├── books/              # Raw .txt files from Gutenberg
│   └── indexes/            # Serialized index files (.pkl)
│
├── tests/                  # pytest unit tests
│   ├── test_preprocess.py
│   ├── test_inverted.py
│   ├── test_permuterm.py
│   ├── test_proximity.py
│   └── test_search.py
│
└── frontend/               # Optional React UI (phase 2)
    ├── package.json
    ├── src/
    │   └── App.jsx         # Single page: search bar + results list
    └── public/
```

## Tech Stack

### Backend (core)
- **Python 3.10+**
- **NLTK** — tokenization, stemming, stopword removal
- **requests** — Gutendex API calls
- **pickle** — index serialization
- **argparse** — CLI interface

### Frontend (optional, phase 2)
- **React** (Vite) — single-page search UI
- **Flask** or **FastAPI** — thin API wrapper over search.py

### Dev/Test
- **pytest** — unit tests
- **ruff** — linting

## Key Data Structures

### Inverted Index
Standard `dict[str, set[int]]` mapping normalized tokens → set of book IDs. Supports basic keyword search (AND/OR).

### Permuterm Index
A permuterm index over the vocabulary for wildcard queries. Append `$` sentinel, generate all rotations, store in a sorted structure (B-Tree or sorted dict). Wildcard like `hel*o` → rotate to `o$hel*` → prefix search.

### Proximity/Positional Index
`dict[str, dict[int, list[int]]]` mapping token → book_id → list of positions. Enables phrase search by checking consecutive positions and proximity queries.

## Conventions

### Code Style
- Use type hints on all function signatures
- Docstrings on every public function (one-liner is fine)
- snake_case everything
- Keep functions short — if it's over 40 lines, split it
- Comments should explain *why*, not *what*

### Naming
- Book IDs are Gutenberg IDs (ints)
- A "document" or "doc" always means one book
- "token" = normalized word (lowercased, stemmed)
- "term" = raw word before normalization

### Error Handling
- Fail loud during indexing (crash with clear message)
- Fail gracefully during search (return empty results + warning)
- Always log download failures, never silently skip

### Git
- Commit messages: imperative mood, <72 chars (`Add inverted index builder`)
- Branch per feature: `feature/inverted-index`, `feature/wildcard-search`
- Never commit data/ or indexes/ — they're regenerable
- requirements.txt stays up to date

## CLI Interface

```bash
# Download books
python -m src.download --count 1000

# Build indexes
python -m src.preprocess
# (this tokenizes + builds all three indexes)

# Search
python -m src.cli "shakespeare"                  # keyword
python -m src.cli "wom*n"                         # wildcard
python -m src.cli '"to be or not to be"'          # phrase (quoted)
```

Output format:
```
Found 3 results for "shakespeare":

1. The Sonnets — William Shakespeare (ID: 1041)
2. Hamlet — William Shakespeare (ID: 1524)
3. A Midsummer Night's Dream — William Shakespeare (ID: 1514)
```

## API Reference

### Gutendex API
- Base URL: `https://gutendex.com/books/`
- No auth required
- Paginated: use `?page=N` to iterate
- Response includes `results[].id`, `results[].title`, `results[].authors[].name`
- Full text URL pattern: `https://www.gutenberg.org/files/{id}/{id}-0.txt` (try this first, fall back to other formats)
- Rate limit: be polite, add a small delay between requests

### Search API (if frontend is added)
```
GET /api/search?q=<query>&type=<keyword|wildcard|phrase>

Response:
{
  "query": "shakespeare",
  "type": "keyword",
  "results": [
    {"id": 1041, "title": "The Sonnets", "author": "William Shakespeare"}
  ]
}
```

## Testing

```bash
pytest tests/ -v
```

Test priorities:
1. Tokenizer produces expected output for edge cases (punctuation, unicode, hyphens)
2. Inverted index returns correct doc sets for known tokens
3. Wildcard permuterm rotations are generated correctly
4. Phrase search finds exact sequences and rejects near-misses
5. Integration: download 5 books → build index → run queries → verify results

Use small fixture data (3-5 tiny docs) for unit tests, not the full corpus.

## Scope Boundaries

**In scope:**
- Download and store ~1,000 books from Gutenberg
- NLTK preprocessing (tokenize, lowercase, stem, remove stopwords)
- Three index types: inverted, permuterm, proximity
- CLI for all three search modes
- Unit tests for core logic
- Optional: single-page React frontend with search bar + results

**Out of scope (do not build):**
- Ranking/relevance scoring (TF-IDF, BM25)
- Spell correction or "did you mean"
- User accounts or saved searches
- Database storage (use pickle files)
- Deployment or containerization
- Full-text display of books
- Concurrent/async indexing
