"""Smoke test /v1/act — the live action endpoint that changes durable state.

The point this test defends: unlike /v1/ask (which returns advice JSON),
/v1/act produces a receipt where `before_committed != after_committed` — proof
the service actually acted — and replaying the same correlation_id is
idempotent (no duplicate side effect).
"""
from __future__ import annotations
from datetime import datetime, timedelta, timezone
import os
import pytest
from fastapi.testclient import TestClient

from action_engine.store import ActionStore
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


def _act_to_completion(client, payload):
    first = client.post("/v1/act", json=payload).json()
    assert first["safety_decision"] == "WAIT_FOR_ACK"
    ack = client.post(f"/v1/cases/{payload['correlation_id']}/ack")
    assert ack.status_code == 200 and ack.json()["acknowledged"] is True
    return client.post("/v1/act", json=payload).json()


def test_act_changes_durable_state(client):
    data = _act_to_completion(client, _payload())
    assert data["accepted"] is True
    assert data["disposition"] is not None
    assert data["acknowledged"] is True
    # the action actually happened: durable world-state went false -> true
    assert data["before_committed"] is False
    assert data["after_committed"] is True
    assert data["outcome_verified"] is True
    assert data["false_success_detected"] is False


def test_act_is_idempotent_on_replay(client):
    first = _act_to_completion(client, _payload("case-replay"))
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
    assert missing_result["safety_decision"] == "SUPPRESS"
    assert missing_result["after_committed"] is None

    stale = _payload("case-stale-time")
    stale["ingested_at"] = "1970-01-01T00:00:00Z"
    stale_result = client.post("/v1/act", json=stale).json()
    assert stale_result["safety_decision"] == "SUPPRESS"
    assert stale_result["safety_reason_code"] == "STALE_CAPACITY_STATE"
    assert stale_result["after_committed"] is None


def test_status_endpoint_reports_waiting_and_blocking_state(client):
    result = client.post("/v1/act", json=_payload("case-waiting")).json()
    assert result["safety_decision"] == "WAIT_FOR_ACK"

    status = client.get("/v1/cases/case-waiting/status")
    assert status.status_code == 200
    data = status.json()
    assert data["current_stage"] == "waiting_for_ack"
    assert data["next_expected_event"] == "task_acknowledged"
    assert data["latest_reason_code"] == "RECEIVER_ACK_PENDING"
    assert data["blocking_reason"]
    assert data["ack_deadline_at"]
    assert data["ack_wait_seconds"] >= 0


@pytest.mark.parametrize("field,value", [
    ("confidence_after", 1.0),
    ("evidence_conflicts", []),
    ("action_risk", "low"),
    ("reversible", True),
    ("receiver_acknowledged", True),
])
def test_public_caller_cannot_self_certify_safety(client, field, value):
    payload = _payload(f"case-self-certify-{field}")
    payload[field] = value
    response = client.post("/v1/act", json=payload)
    assert response.status_code == 422


def test_status_exposes_versioned_trusted_safety_receipt(client):
    cid = "case-policy-receipt"
    result = _act_to_completion(client, _payload(cid))
    assert result["safety_decision"] == "ACT"

    status = client.get(f"/v1/cases/{cid}/status").json()
    assert status["latest_policy_version"] == "action-safety.v2"
    assert status["latest_derived_facts"]["caller_safety_overrides_used"] is False
    assert status["latest_derived_facts"]["receiver_acknowledged"]["source"] == "durable_store.tasks.status"

    store = ActionStore(os.environ["ACTION_DB_PATH"])
    try:
        pre_action = store.conn.execute(
            "SELECT policy_version, derived_facts_json FROM safety_decisions "
            "WHERE correlation_id=? AND current_stage='pre_action_safety_review'",
            (cid,),
        ).fetchone()
    finally:
        store.close()
    assert pre_action["policy_version"] == "action-safety.v2"
    assert "action-safety.v2.ACTION_POLICY" in pre_action["derived_facts_json"]


def test_missing_capacity_fields_derive_low_confidence_and_stop_action(client):
    payload = _payload("case-derived-low-confidence")
    payload["er_state"] = {"available_beds": 3}

    result = client.post("/v1/act", json=payload).json()
    assert result["safety_decision"] == "ASK_FOR_INFO"
    assert result["safety_reason_code"] == "LOW_CONFIDENCE"
    assert result["after_committed"] is None

    status = client.get("/v1/cases/case-derived-low-confidence/status").json()
    assert status["confidence_after"] == 0.4
    assert status["latest_derived_facts"]["capacity_field_completeness"]["value"] == 0.333
    assert status["latest_derived_facts"]["evidence_sufficiency_confidence"]["calibrated_model_confidence"] is False


def test_derived_capacity_conflict_blocks_high_risk_action(client):
    payload = _payload("case-derived-conflict")
    payload["bed_pressure_risk"] = "low"
    payload["er_state"] = {"available_beds": 0, "occupancy_pct": 99, "queue_length": 12}

    result = client.post("/v1/act", json=payload).json()
    assert result["disposition"] == "divert"
    assert result["safety_decision"] == "HUMAN_REVIEW"
    assert result["safety_reason_code"] == "HIGH_RISK_EVIDENCE_CONFLICT"
    assert result["after_committed"] is None

    status = client.get("/v1/cases/case-derived-conflict/status").json()
    conflict = status["latest_derived_facts"]["evidence_conflicts"]
    assert conflict["value"] == ["bed_pressure_low_vs_saturated_capacity"]
    assert conflict["source"] == "action-safety.v2.capacity_consistency_rules"


def test_receiver_ack_is_separate_and_required_before_action(client):
    cid = "case-independent-ack"
    payload = _payload(cid)

    waiting = client.post("/v1/act", json=payload).json()
    assert waiting["safety_decision"] == "WAIT_FOR_ACK"
    assert waiting["after_committed"] is None

    ack = client.post(f"/v1/cases/{cid}/ack").json()
    assert ack["acknowledged"] is True
    assert ack["task_status"] == "acknowledged"

    completed = client.post("/v1/act", json=payload).json()
    assert completed["safety_decision"] == "ACT"
    assert completed["after_committed"] is True


def test_ack_deadline_timeout_escalates_and_late_ack_is_rejected(client):
    cid = "case-ack-timeout"
    payload = _payload(cid)
    waiting = client.post("/v1/act", json=payload).json()
    assert waiting["safety_decision"] == "WAIT_FOR_ACK"

    store = ActionStore(os.environ["ACTION_DB_PATH"])
    try:
        expired = (datetime.now(timezone.utc) - timedelta(seconds=1)).isoformat()
        store.conn.execute(
            "UPDATE tasks SET ack_deadline_at=? WHERE correlation_id=?",
            (expired, cid),
        )
        store.conn.commit()
    finally:
        store.close()

    status = client.get(f"/v1/cases/{cid}/status").json()
    assert status["current_stage"] == "ack_timeout_escalated"
    assert status["current_owner"] == "charge_nurse_review_queue"
    assert status["latest_safety_decision"] == "HUMAN_REVIEW"
    assert status["latest_reason_code"] == "RECEIVER_ACK_TIMEOUT"
    assert status["blocking_reason"] == "Receiver acknowledgement deadline expired."

    late_ack = client.post(f"/v1/cases/{cid}/ack")
    assert late_ack.status_code == 409

    replay = client.post("/v1/act", json=payload).json()
    assert replay["safety_decision"] == "HUMAN_REVIEW"
    assert replay["safety_reason_code"] == "RECEIVER_ACK_TIMEOUT"
    assert replay["after_committed"] is None
