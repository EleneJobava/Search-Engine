import json
import re
from pathlib import Path
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer
import numpy as np

DEFAULT_RESULTS = 10

def handle_input(txt: str) -> str:
    txt = txt.lower()
    txt = re.sub(r"'s\b", "", txt)
    txt = re.sub(r"[^a-z0-9 ]+", "", txt)
    txt = re.sub(r"\s+", " ", txt).strip()
    return txt

def load_products(path: Path) -> list:
    with open(path, "r") as f:
        return json.load(f)

def normalize(scores):
    min_s, max_s = scores.min(), scores.max()
    if max_s - min_s == 0:
        return scores
    return (scores - min_s) / (max_s - min_s)

class SearchEngine:
    def __init__(self, products: list[dict]) -> None:
        self.products = products

        corpus = [handle_input(p["name"] + " " + p["description"]) for p in products]

        self.tokenized_corpus = [
            doc.split()
            for doc in corpus
        ]

        self.bm25 = BM25Okapi(self.tokenized_corpus)
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        cache_path = Path("embeddings.npy")
        if cache_path.exists():
            self.embeddings = np.load(cache_path)
        else:
            self.embeddings = self.model.encode(corpus, show_progress_bar=True)
            np.save(cache_path, self.embeddings)

    def search(self, query: str) -> list[dict]:
        processed_query = handle_input(query)
        tokens = processed_query.split()

        bm25_scores = self.bm25.get_scores(tokens)
        query_embedding = self.model.encode([processed_query])
        semantic_scores = np.dot(self.embeddings, query_embedding.T).flatten()

        bm25_norm = normalize(bm25_scores)
        semantic_norm = normalize(semantic_scores)
        combined_scores = 0.6 * bm25_norm + 0.4 * semantic_norm
        top_indices = np.argsort(combined_scores)[::-1][:DEFAULT_RESULTS]

        return [self.products[i] for i in top_indices]