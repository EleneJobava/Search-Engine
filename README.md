**Product Search Engine**
A hybrid search engine for an online store built with FastAPI, BM25, and semantic search using sentence transformers. Users can search 10,000 products by typing natural language queries and get the most relevant results back instantly.

This is a full-stack web application with two main parts: a search backend and a simple browser-based frontend.
The backend exposes a REST API built with FastAPI. It has a single search endpoint (GET /search?q=) that accepts a text query and returns the top 10 most relevant products as JSON. The frontend is a plain HTML page served at the root URL with a search box and a results display no frameworks, no build step. 
The core of the project is a hybrid search engine that combines two completely different approaches to ranking: BM25 for keyword matching and sentence transformers for semantic (meaning-based) matching. Both scores are normalized and combined into a single final score, and the top 10 products by that score are returned.

**A full-stack web application with:**
  • A FastAPI backend exposing a /search endpoint
  • A hybrid search engine combining BM25 (keyword matching) and semantic search (meaning-based matching)
  • A clean HTML/JS frontend served at the root URL
  • Embedding cache so the app starts instantly after the first run

**The search engine handles:** 
Text queries across product name and description as well as messy input: extra spaces, different casing, special characters.
Intent-based queries like "gift for kids" where no exact product words appear and returns top 10 most relevant results ranked by combined score.

**How to Run:**
1. Clone the repository
  git clone https://github.com/EleneJobava/Search-Engine.git
  cd Search-Engine
2. Install dependencies
  pip install fastapi uvicorn rank-bm25 sentence-transformers numpy
3.  Run the app
  uvicorn app.main:app --reload

Then open your browser at http://localhost:8000. You will see a search box. Type a query and hit Search.
Note on first startup: The first time you run the app, it will download the sentence transformer model and encode all 10,000 products into embeddings. This takes about 60 seconds. After that, the embeddings are saved to embeddings.npy and every subsequent startup is instant.

**How to Run Tests:**
pip install pytest
pytest tests/test_search.py -v

The test suite covers input cleaning, result count, result structure, and relevance for a known keyword query. The search engine loads once for the entire test session using a module-scoped pytest fixture so tests run quickly.

**Example Queries to Try:**
• cotton shirt — exact keyword match, BM25 dominates, very precise results
• eco friendly — keyword match across descriptions
• gift for kids — no exact product words, semantic search kicks in and finds toys and children's products
• something sustainable — intent-based query, works purely through meaning
• cott@@on — messy input with special characters, cleaned to cott on, still returns reasonable results
• COTTON T-SHIRT — uppercase input, normalized before searching
• cotton   shirt  — extra spaces, collapsed before searching











