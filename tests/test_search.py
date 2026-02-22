import pytest
from pathlib import Path
from app.search import SearchEngine, load_products, handle_input

def test_handle_input_lowercase():
    assert handle_input("Cotton SHIRT") == "cotton shirt"
    assert handle_input("sCenTed cAndLE") == "scented candle"
    assert handle_input("SAMEGRELO winter COAt") == "samegrelo winter coat"

def test_handle_input_special_chars():
    assert handle_input("cott@@on") == "cotton"
    assert handle_input("sa@@megr!!elo") == "samegrelo"

def test_handle_input_extra_spaces():
    assert handle_input("SAMEGRELO winter    COAt") == "samegrelo winter coat"
    assert handle_input("cotton   shirt") == "cotton shirt"

def test_handle_input_apostrophe():
    assert handle_input("women's shirt") == "women shirt"

def test_handle_input_numbers_kept():
    assert handle_input("product 123") == "product 123"

@pytest.fixture(scope="module")
def engine():
    products = load_products(Path("data/products.json"))
    return SearchEngine(products)

def test_returns_10_results(engine):
    results = engine.search("cotton shirt")
    assert len(results) == 10

def test_results_are_dicts(engine):
    results = engine.search("cotton shirt")
    assert all(isinstance(r, dict) for r in results)

def test_results_have_required_fields(engine):
    results = engine.search("cotton shirt")
    for r in results:
        assert "id" in r
        assert "name" in r
        assert "description" in r
        assert "price" in r

def test_messy_input_returns_results(engine):
    results = engine.search("  COTTON@@  shirt!!! ")
    assert len(results) == 10

def test_empty_query_does_not_crash(engine):
    results = engine.search("")
    assert isinstance(results, list)

def test_relevant_results_for_cotton(engine):
    results = engine.search("cotton")
    names = [r["name"].lower() for r in results]
    assert any("cotton" in name for name in names)