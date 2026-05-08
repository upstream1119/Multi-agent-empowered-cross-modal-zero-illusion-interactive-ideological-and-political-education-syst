import json
import os
from pathlib import Path

from src.retriever.hybrid_retriever import retrieve


REQUIRED_HYBRID_FIELDS = {
    "id",
    "source",
    "citation",
    "vector_score",
    "graph_score",
    "hybrid_score",
}


def _load_demo_queries() -> list[dict]:
    path = Path(__file__).with_name("demo_queries.json")
    return json.loads(path.read_text(encoding="utf-8"))


def test_demo_queries_return_expected_evidence(monkeypatch):
    monkeypatch.setenv("DACHUANG_RETRIEVE_MODE", "mock")
    monkeypatch.setenv("DACHUANG_LOCAL_MOCK_ACK", "1")

    for case in _load_demo_queries():
        result = retrieve(case["query"])

        for entity in case["expected_entities"]:
            assert entity in result["query_entities"], case["id"]

        hybrid_hits = result["hybrid_hits"]
        assert len(hybrid_hits) >= case["min_hybrid_hits"], case["id"]

        for hit in hybrid_hits:
            assert REQUIRED_HYBRID_FIELDS.issubset(hit), case["id"]
            assert isinstance(hit["citation"], dict), case["id"]
            assert hit["citation"].get("doc"), case["id"]
            assert hit["citation"].get("section"), case["id"]


def test_team_mode_keeps_fixed_empty_contract(monkeypatch):
    monkeypatch.delenv("DACHUANG_RETRIEVE_MODE", raising=False)
    monkeypatch.delenv("DACHUANG_LOCAL_MOCK_ACK", raising=False)

    result = retrieve("遵义会议是在什么背景下召开的？")

    assert result["query_entities"] == []
    assert result["vector_hits"] == []
    assert result["graph_hits"] == []
    assert result["hybrid_hits"] == []
