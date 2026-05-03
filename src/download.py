# src/download.py
import requests
import time
import pathlib
import json
import argparse

DATA_DIR = pathlib.Path("data/books")

def fetch_book_list(count):
    """Pull book metadata from Gutendex until we have `count` entries."""
    books, page = [], 1
    while len(books) < count:
        r = requests.get(f"https://gutendex.com/books/?page={page}")
        data = r.json()
        books.extend(data["results"])
        page += 1
        time.sleep(0.5)
    return books[:count]

def download_text(book_id):
    """Try common Gutenberg URL patterns, return text or None."""
    urls = [
        f"https://www.gutenberg.org/files/{book_id}/{book_id}-0.txt",
        f"https://www.gutenberg.org/files/{book_id}/{book_id}.txt",
    ]
    for url in urls:
        r = requests.get(url)
        if r.status_code == 200:
            return r.text
    print(f"  [WARN] Could not download book {book_id}")
    return None

def save_book(book_id, text, meta):
    """Save raw text and metadata to data/books/."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    # Save text
    (DATA_DIR / f"{book_id}.txt").write_text(text, encoding="utf-8")
    # Save metadata (title, author) as JSON alongside it
    (DATA_DIR / f"{book_id}.json").write_text(json.dumps(meta), encoding="utf-8")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=10)
    args = parser.parse_args()

    print(f"Fetching metadata for {args.count} books...")
    books = fetch_book_list(args.count)

    downloaded = 0
    for book in books:
        book_id = book["id"]
        title = book.get("title", "Unknown")
        authors = book.get("authors", [])
        author = authors[0]["name"] if authors else "Unknown"

        text = download_text(book_id)
        if text:
            meta = {"id": book_id, "title": title, "author": author}
            save_book(book_id, text, meta)
            downloaded += 1

    print(f"\nDone. Downloaded {downloaded}/{args.count} books to data/books/")