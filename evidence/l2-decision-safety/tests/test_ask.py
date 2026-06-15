"""Smoke test the one workflow — /v1/ask end-to-end through the FastAPI app."""
from __future__ import annotations
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ok"
    assert data["service"] == "healthcare-genai-engineer"


def test_ask_returns_grounded_answer(client):
    r = client.post(
        "/v1/ask",
        json={"query": "62yo male chest pain hypertension", "k": 5, "method": "bm25"},
    )
    assert r.status_code == 200, r.text
    data = r.json()
    assert data["query"] == "62yo male chest pain hypertension"
    assert isinstance(data["answer"], str) and len(data["answer"]) > 10
    assert data["retrieved_count"] >= 0
    assert isinstance(data["citations"], list)
    assert data["method_used"] == "bm25"
    assert data["latency_ms"] >= 0
    assert data["triage_level"] in {"NOW", "SOON", "WAIT"}
    assert "prediction_signal" in data
    assert "decision_basis" in data
    assert "operational_recommendations" in data
    assert "explanation_for_human" in data
    assert data["agent_collaboration"]["primary_agent"] == "er_triage"
    assert len(data["agent_collaboration"]["handoffs"]) >= 2


def test_ask_empty_query_rejected(client):
    r = client.post("/v1/ask", json={"query": "", "k": 5, "method": "bm25"})
    assert r.status_code == 422  # pydantic validation


def test_ask_reports_bm25_when_dense_falls_back(client):
    with patch("retrieval.query_pipeline._dense.search", side_effect=RuntimeError("encoder missing")):
        r = client.post(
            "/v1/ask",
            json={"query": "62yo male chest pain hypertension", "k": 5, "method": "dense"},
        )
    assert r.status_code == 200, r.text
    data = r.json()
    assert data["method_used"] == "bm25"


def test_low_confidence_recommendation_is_suppressed(client):
    with (
        patch("app.routers.ask.classify_rag", return_value=(None, 0.0, {})),
        patch("app.routers.ask.generate_grounded_answer") as generate,
        patch("app.routers.ask.plan_agent_collaboration") as plan,
    ):
        r = client.post(
            "/v1/ask",
            json={"query": "routine question with no matching evidence", "k": 5, "method": "bm25"},
        )
    assert r.status_code == 200, r.text
    data = r.json()
    assert data["safety_decision"] == "ASK_FOR_INFO"
    assert data["safety_reason_code"] == "LOW_CONFIDENCE"
    assert data["operational_recommendations"] == []
    assert data["agent_collaboration"] is None
    assert data["generate_ms"] == 0
    assert "withheld a direct recommendation" in data["answer"]
    generate.assert_not_called()
    plan.assert_not_called()


def test_stale_capacity_stops_before_generation_and_planning(client):
    with (
        patch("app.routers.ask.generate_grounded_answer") as generate,
        patch("app.routers.ask.plan_agent_collaboration") as plan,
    ):
        r = client.post(
            "/v1/ask",
            json={
                "query": "62yo male chest pain hypertension",
                "k": 5,
                "method": "bm25",
                "er_state": {
                    "available_beds": 2,
                    "occupancy_pct": 70,
                    "queue_length": 2,
                    "observed_at": "1970-01-01T00:00:00Z",
                },
            },
        )
    assert r.status_code == 200, r.text
    data = r.json()
    assert data["safety_decision"] == "SUPPRESS"
    assert data["safety_reason_code"] == "STALE_CAPACITY_STATE"
    assert data["operational_recommendations"] == []
    assert data["agent_collaboration"] is None
    generate.assert_not_called()
    plan.assert_not_called()
