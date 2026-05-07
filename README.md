# Gutenberg Search Engine

A search engine over public domain books from [Project Gutenberg](https://www.gutenberg.org/), built using the [Gutendex API](https://gutendex.com/). Supports keyword, wildcard, and phrase search across a corpus of downloaded books. Keyword results are ranked by TF-IDF with field-weighted title boosting.

---

## Requirements

- Python 3.10+
- Node.js 18+
- pip packages listed in `requirements.txt`

---

## Setup

**1. Install dependencies**

```bash
pip install -r requirements.txt
```

NLTK data (stopwords, tokenizer) is downloaded automatically on first run.

---

## Running the Search Engine

### Step 1 — Download books

Fetch books from the Gutendex API and save them to `data/books/`. Use `--count` to set how many books to download.

```bash
python -m src.download --count 100
```

Books are saved as `data/books/<id>.txt` and `data/books/<id>.json` (metadata).

> Note: `data/` is gitignored — books and indexes must be generated locally.

### Step 2 — Build indexes

Tokenize all books and build the three search indexes (inverted, permuterm, positional). Indexes are saved to `data/indexes/`.

```bash
python -m src.preprocess
```

### Step 3 — Search

**Option A — Browser UI**

Start the API backend (from project root):
```bash
uvicorn src.api:app --reload --port 8000
```

In a second terminal, start the frontend:
```bash
cd frontend
npm install   # first time only
npm run dev
```

Open `http://localhost:5173` in your browser.

**Option B — CLI**

```bash
python -m src.main
```

Enter your query and press Enter. Type `exit` to quit.

---

## Query Types

The search engine auto-detects the query type based on syntax:

| Type | Syntax | Example | Ranking |
|------|--------|---------|---------|
| Keyword | Plain text (AND across all terms) | `whale ocean` | TF-IDF scored, top 15 returned |
| Wildcard | Contains `*` | `wom*n` or `*ing` | Unranked |
| Phrase | Wrapped in double quotes | `"crime and punishment"` | Unranked |

---

## Project Structure

```
src/
  download.py      # Gutendex API fetcher
  preprocess.py    # Tokenization, stemming, index building
  search.py        # Query parser and search dispatcher
  api.py           # FastAPI backend
  main.py          # Interactive CLI entry point
  index/
    inverted.py    # Inverted index with TF-IDF scoring and title boosting
    permuterm.py   # Permuterm trie (wildcard search)
    proximity.py   # Positional index (phrase search)
frontend/
  src/App.jsx      # React search UI
data/
  books/           # Downloaded .txt and .json files (gitignored)
  indexes/         # Serialized .pkl index files (gitignored)
tests/             # pytest unit tests
```

---

## Running Tests

```bash
pytest tests/ -v
```
