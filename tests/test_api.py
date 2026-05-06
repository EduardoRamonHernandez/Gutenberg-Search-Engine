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
        assert "score" in r


def test_keyword_results_have_numeric_scores(client):
    res = client.get("/api/search", params={"q": "ahab"})
    results = res.json()["results"]
    for r in results:
        assert isinstance(r["score"], float)


def test_keyword_results_sorted_by_score_descending(client):
    res = client.get("/api/search", params={"q": "ahab"})
    results = res.json()["results"]
    scores = [r["score"] for r in results]
    assert scores == sorted(scores, reverse=True)


def test_keyword_top_result_is_most_relevant(client):
    # "gatsby" only appears in book 3 — must be rank 1
    res = client.get("/api/search", params={"q": "gatsby"})
    results = res.json()["results"]
    assert results[0]["id"] == 3  # book 3 = Gatsby


def test_phrase_results_have_null_score(client):
    res = client.get("/api/search", params={"q": '"white whale"'})
    results = res.json()["results"]
    for r in results:
        assert r["score"] is None


def test_wildcard_results_have_null_score(client):
    res = client.get("/api/search", params={"q": "dracul*"})
    results = res.json()["results"]
    for r in results:
        assert r["score"] is None
