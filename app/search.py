import json
import re
from pathlib import Path
from rank_bm25 import BM25
from sentence_transformers import SentenceTransformer

def handle_input(txt: str) -> str:
    txt = txt.lower()
    txt = re.sub(r"[^A-Za-z0-9 ]+", " ", txt)
    txt = re.sub(r"\s+", " ", txt)
    return txt

def load_products(path: Path) -> list:
    with open(path, "r") as f:
        return json.load(f)


