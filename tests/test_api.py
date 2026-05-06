def test_keyword_search_returns_results(client):
    res = client.get("/api/search", params={"q": "ahab"})
    assert res.status_code == 200
    data = res.json()
    assert data["query"] == "ahab"
    assert any(r["id"] == 1 for r in data["results"])  # book 1 = Moby Dick


def test_phrase_search_returns_results(client):
    res = client.get("/api/search", params={"q": '"white whale"'})
    assert res.status_code == 200
    data = res.json()
    assert any(r["id"] == 1 for r in data["results"])


def test_wildcard_search_returns_results(client):
    res = client.get("/api/search", params={"q": "dracul*"})
    assert res.status_code == 200
    data = res.json()
    assert any(r["id"] == 2 for r in data["results"])  # book 2 = Dracula


def test_missing_query_param_returns_422(client):
    res = client.get("/api/search")
    assert res.status_code == 422


def test_result_shape(client):
    res = client.get("/api/search", params={"q": "gatsby"})
    assert res.status_code == 200
    results = res.json()["results"]
    assert len(results) > 0
    for r in results:
        assert "id" in r
        assert "title" in r
        assert "author" in r
