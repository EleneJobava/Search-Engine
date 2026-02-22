import json
import re
from pathlib import Path
from rank_bm25 import BM25
from sentence_transformers import SentenceTransformer

DEFAULT_RESULTS = 10

def handle_input(txt: str) -> str:
    txt = txt.lower()
    txt = re.sub(r"'s\b", "", txt)
    txt = re.sub(r"[^a-z0-9 ]+", " ", txt)
    txt = re.sub(r"\s+", " ", txt).strip()
    return txt

def load_products(path: Path) -> list:
    with open(path, "r") as f:
        return json.load(f)

class SearchEngine:
    def __init__(self, products: list[dict]) -> None:
        self.products = products

        corpus = [handle_input(p["name"] + " " + p["description"]) for p in products]

        self.tokenized_corpus = [
            doc.split()
            for doc in corpus
        ]

        self.bm25 = BM25(self.tokenized_corpus)
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.embeddings = self.model.encode(corpus, show_progress_bar=True)



