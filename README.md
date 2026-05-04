# Gutenberg Search Engine

A search engine over public domain books from [Project Gutenberg](https://www.gutenberg.org/), built using the [Gutendex API](https://gutendex.com/). Supports keyword, wildcard, and phrase search across a corpus of downloaded books.

---

## Requirements

- Python 3.10+
- Node.js 18+
- pip packages: `nltk`, `requests`, `fastapi`, `uvicorn`

---

## Setup

**1. Install dependencies**

```bash
pip install -r requirements.txt
```

**2. Download required NLTK data**

```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab'); nltk.download('stopwords')"
```

---

## Running the Search Engine

### Step 1 — Download books

Fetch books from the Gutendex API and save them to `data/books/`. Use `--count` to set how many books to download (default: 5).

```bash
python -m src.download --count 5
```

Books are saved as `data/books/<id>.txt` and `data/books/<id>.json` (metadata).

> Note: The `data/` directory is gitignored. The repo includes 5 pre-downloaded books and pre-built indexes, so you can skip steps 1–2 and go straight to searching if you just want to try it out.

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

| Type | Syntax | Example |
|------|--------|---------|
| Keyword | Plain text (AND across all terms) | `whale ocean` |
| Wildcard | Contains `*` | `wom*n` or `*ing` |
| Phrase | Wrapped in double quotes | `"to be or not to be"` |

**Examples:**

```
shakespeare
wom*n
"it was the best of times"
```

---

## Project Structure

```
src/
  download.py      # Gutendex API fetcher
  preprocess.py    # Tokenization, stemming, index building
  search.py        # Query parser and search dispatcher
  main.py          # Interactive CLI entry point
  index/
    inverted.py    # Inverted index (keyword search)
    permuterm.py   # Permuterm trie (wildcard search)
    proximity.py   # Positional index (phrase search)
data/
  books/           # Downloaded .txt and .json files
  indexes/         # Serialized .pkl index files
tests/             # pytest unit tests
```

---

## Running Tests

```bash
pytest tests/ -v
```
