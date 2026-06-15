"""Smoke test /v1/act — the live action endpoint that changes durable state.

The point this test defends: unlike /v1/ask (which returns advice JSON),
/v1/act produces a receipt where `before_committed != after_committed` — proof
the service actually acted — and replaying the same correlation_id is
idempotent (no duplicate side effect).
"""
from __future__ import annotations
from datetime import datetime, timezone
import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client(tmp_path, monkeypatch):
    # Isolate durable action state per test run.
    monkeypatch.setenv("ACTION_DB_PATH", str(tmp_path / "act.db"))
    return TestClient(app)


def _payload(correlation_id="case-act-smoke"):
    return {
        "correlation_id": correlation_id,
        "triage_level": "NOW",
        "predicted_los_hours": 6,
        "bed_pressure_risk": "low",
        "er_state": {"available_beds": 3, "occupancy_pct": 70, "queue_length": 2},
        "ingested_at": datetime.now(timezone.utc).isoformat(),
    }


def test_act_changes_durable_state(client):
    r = client.post("/v1/act", json=_payload())
    assert r.status_code == 200
    data = r.json()
    assert data["accepted"] is True
    assert data["disposition"] is not None
    assert data["acknowledged"] is True
    # the action actually happened: durable world-state went false -> true
    assert data["before_committed"] is False
    assert data["after_committed"] is True
    assert data["outcome_verified"] is True
    assert data["false_success_detected"] is False


def test_act_is_idempotent_on_replay(client):
    first = client.post("/v1/act", json=_payload("case-replay")).json()
    second = client.post("/v1/act", json=_payload("case-replay")).json()
    # Replay applies nothing new; state is already committed, no duplicate.
    assert first["after_committed"] is True
    assert second["after_committed"] is True
    assert second["accepted"] is True


def test_act_fails_closed_on_bad_evidence(client):
    bad = _payload("case-bad")
    bad["er_state"] = {"occupancy_pct": 999}  # out of range → schema rejects
    r = client.post("/v1/act", json=bad)
    assert r.status_code == 422


def test_act_missing_or_1970_timestamp_never_commits(client):
    missing = _payload("case-missing-time")
    missing.pop("ingested_at")
    missing_result = client.post("/v1/act", json=missing).json()
    assert missing_result["safety_decision"] == "ASK_FOR_INFO"
    assert missing_result["after_committed"] is None

    stale = _payload("case-stale-time")
    stale["ingested_at"] = "1970-01-01T00:00:00Z"
    stale_result = client.post("/v1/act", json=stale).json()
    assert stale_result["safety_decision"] == "SUPPRESS"
    assert stale_result["safety_reason_code"] == "STALE_CAPACITY_STATE"
    assert stale_result["after_committed"] is None


def test_status_endpoint_reports_waiting_and_blocking_state(client):
    payload = _payload("case-waiting")
    payload["receiver_acknowledged"] = False
    result = client.post("/v1/act", json=payload).json()
    assert result["safety_decision"] == "WAIT_FOR_ACK"

    status = client.get("/v1/cases/case-waiting/status")
    assert status.status_code == 200
    data = status.json()
    assert data["current_stage"] == "waiting_for_ack"
    assert data["next_expected_event"] == "task_acknowledged"
    assert data["latest_reason_code"] == "RECEIVER_ACK_PENDING"
    assert data["blocking_reason"]


def test_legendary_safety_envelope_case(client):
    cid = "legendary-safety-envelope"
    stale_conflict = _payload(cid)
    stale_conflict.update({
        "ingested_at": "1970-01-01T00:00:00Z",
        "confidence_before": 0.91,
        "confidence_after": 0.42,
        "evidence_conflicts": ["patient_history_vs_drug_risk"],
        "action_risk": "high",
        "reversible": False,
    })
    first = client.post("/v1/act", json=stale_conflict).json()
    assert first["safety_decision"] == "SUPPRESS"
    assert first["safety_reason_code"] == "STALE_CAPACITY_STATE"
    stale_status = client.get(f"/v1/cases/{cid}/status").json()
    assert stale_status["confidence_before"] == 0.91
    assert stale_status["confidence_after"] == 0.42
    assert stale_status["blocking_reason"]

    fresh_waiting = _payload(cid)
    fresh_waiting["receiver_acknowledged"] = False
    second = client.post("/v1/act", json=fresh_waiting).json()
    assert second["safety_decision"] == "WAIT_FOR_ACK"

    fresh_acked = _payload(cid)
    third = client.post("/v1/act", json=fresh_acked).json()
    assert third["safety_decision"] == "ACT"
    assert third["after_committed"] is True
    assert third["outcome_verified"] is True
