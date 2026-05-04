import json
from pathlib import Path
lines = []
for f in sorted(Path('data/books').glob('*.json')):
    d = json.loads(f.read_text(encoding='utf-8'))
    lines.append(f"{d['id']} | {d['title']} | {d['author']}")
Path('books_list.txt').write_text('\n'.join(lines), encoding='utf-8')
print(f"Wrote {len(lines)} books to books_list.txt")
