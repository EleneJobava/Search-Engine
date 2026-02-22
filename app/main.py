from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pathlib import Path
from app.search import SearchEngine, load_products

app = FastAPI()

products = load_products(Path("data/products.json"))
engine = SearchEngine(products)

@app.get("/search")
def search(q: str):
    results = engine.search(q)
    return {"query": q, "results": results}

@app.get("/", response_class=HTMLResponse)
def home():
    return open("templates/index.html").read()