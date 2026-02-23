# Product Search Engine

A hybrid search engine for an online store built with FastAPI, BM25, and semantic search using sentence transformers. Users can search 10,000 products by typing natural language queries and get the most relevant results back instantly.

---

## What I Built

A full-stack web application with two main parts: a search backend and a simple browser-based frontend.

The backend exposes a REST API built with FastAPI with a single search endpoint (`GET /search?q=`) that accepts a text query and returns the top 10 most relevant products as JSON. The frontend is a plain HTML page served at the root URL with a search box and results display — no frameworks, no build step.

The core of the project is a hybrid search engine that combines two completely different approaches to ranking: BM25 for keyword matching and sentence transformers for semantic (meaning-based) matching. Both scores are normalized and combined into a single final score, and the top 10 products by that score are returned.

| Feature | Details |
|---|---|
| Backend | FastAPI exposing a `/search` endpoint |
| Search | Hybrid BM25 + semantic search |
| Frontend | Plain HTML/JS served at root URL |
| Performance | Embedding cache for instant startup after first run |

The search engine handles:
- Text queries across product name and description
- Messy input: extra spaces, different casing, special characters
- Intent-based queries like `"gift for kids"` where no exact product words appear

---

## How to Run

**1. Clone the repository**
```bash
git clone https://github.com/EleneJobava/Search-Engine.git
cd Search-Engine
```

**2. Install dependencies**
```bash
pip install fastapi uvicorn rank-bm25 sentence-transformers numpy
```

**3. Run the app**
```bash
uvicorn app.main:app --reload
```

Then open your browser at `http://localhost:8000`, type a query, and hit Search.

> **Note on first startup:** The first time you run the app it will download the sentence transformer model and encode all 10,000 products into embeddings. This takes about 60 seconds. After that, embeddings are saved to `embeddings.npy` and every subsequent startup is instant.

---

## How to Run Tests

```bash
pip install pytest
pytest tests/test_search.py -v
```

The test suite covers input cleaning, result count, result structure, and relevance for known keyword queries. The search engine loads once for the entire test session using a module-scoped pytest fixture so tests run quickly.

---

## Example Queries to Try

| Query | What it tests |
|---|---|
| `eco friendly` | Exact keyword match across descriptions |
| `gift for kids` | No exact product words — semantic search finds relevant results |
| `something sustainable` | Pure intent-based query, works through meaning alone |
| `cott@@on` | Messy input with special characters, cleaned before searching |
| `COTTON T-SHIRT` | Uppercase input, normalized before searching |
| `cotton   shirt` | Extra spaces, collapsed before searching |

---

## How the Search Works

### Input Cleaning

Before any search happens, both the query and product texts go through the same cleaning pipeline: lowercasing, possessive stripping (`"women's"` → `"women"`), special character removal, and whitespace normalization. This happens to both the indexed product text at startup and every incoming query at search time.

### BM25 — Keyword Search

BM25 (Best Match 25) is the industry-standard keyword ranking algorithm used by Elasticsearch and Solr. It scores each product based on how often query words appear in the product text, weighted by how rare those words are across the whole dataset. It is fast, requires no GPU, runs entirely locally, and handles exact keyword queries very well.

Its weakness is that it only understands words, not meaning. A search for `"gift for kids"` scores near zero for every product because none of them use those exact words — that is where semantic search comes in.

### Semantic Search — Sentence Transformers

The semantic layer uses the `all-MiniLM-L6-v2` model which converts any text into a 384-dimensional embedding vector. Texts with similar meaning end up with similar vectors even if they share no words. At startup all 10,000 products are encoded and cached to disk. At search time the query is encoded and compared to every product using a dot product (equivalent to cosine similarity).

### Hybrid Scoring

BM25 scores are raw unbounded numbers while semantic scores are already in -1 to 1 range. BM25 scores are normalized to 0–1 using min-max normalization before combining.

```
final score = 0.6 × BM25_normalized + 0.4 × semantic_score
```

The 0.6 / 0.4 weighting gives BM25 slightly more influence because in product search exact keyword matches are usually the stronger signal of intent. The 0.4 semantic weight supports intent and synonym matching without overriding precise keyword results.

---

## What I Built vs What I Reused

**Built myself:** hybrid search logic, input cleaning pipeline, FastAPI application, embedding cache, HTML frontend, test suite.

**Reused:**
- `rank-bm25` — BM25Okapi implementation. Writing BM25 from scratch is well understood but not the interesting part of this assignment.
- `sentence-transformers` — access to the `all-MiniLM-L6-v2` pre-trained model. Training a semantic model from scratch would require weeks and massive compute.
- `FastAPI` — clean REST API in very few lines of code.
- `numpy` — dot product computation and argsort for ranking.

---

## What Works Well and What Is Still Weak

**Works well:**
- Exact keyword queries are fast and precise
- Intent-based queries return semantically relevant results
- Messy input is handled cleanly
- Startup after first run is instant due to embedding caching

**Still weak or unfinished:**
- Misspellings are not handled — `"cottton"` fails BM25 and relies entirely on semantic search
- No filtering by price, country, brand, or in-stock status
- The embedding cache has no automatic invalidation — delete `embeddings.npy` manually if the dataset changes
- The 0.6 / 0.4 weighting was chosen by manual testing, not systematic evaluation
