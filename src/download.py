# src/download.py 
# sketched out
import requests, time, pathlib

def fetch_book_list(count: int) -> list[dict]:
    """Pull book metadata from Gutendex until we have `count` entries."""
    books, page = [], 1
    while len(books) < count:
        r = requests.get(f"https://gutendex.com/books/?page={page}")
        data = r.json()
        books.extend(data["results"])
        page += 1
        time.sleep(0.5)  # be polite
    return books[:count]

def download_text(book_id: int) -> str | None:
    """Try common Gutenberg URL patterns, return text or None."""
    urls = [
        f"https://www.gutenberg.org/files/{book_id}/{book_id}-0.txt",
        f"https://www.gutenberg.org/files/{book_id}/{book_id}.txt",
    ]
    for url in urls:
        r = requests.get(url)
        if r.status_code == 200:
            return r.text
    return None  # log failure, don't crash