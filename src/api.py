# src/api.py
import pickle
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.search import search

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["GET"],
)

def _load_indexes():
    with open("data/indexes/inverted.pkl", "rb") as f:
        inv = pickle.load(f)
    with open("data/indexes/permuterm.pkl", "rb") as f:
        perm = pickle.load(f)
    with open("data/indexes/positional.pkl", "rb") as f:
        pos = pickle.load(f)
    return inv, perm, pos

try:
    inverted, permuterm, positional = _load_indexes()
except FileNotFoundError:
    inverted = permuterm = positional = None

@app.get("/api/search")
def api_search(q: str):
    results = search(q, inverted, permuterm, positional)
    return {"query": q, "results": results}
