#!/usr/bin/env python3
"""One-command evidence-to-action audit across Baymax sibling repositories."""
from __future__ import annotations

import csv
import json
import re
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "sources"
OUTPUTS = ROOT / "outputs"

REPOS = {
    "left_eye": "healthcare-ai-data-engineer",
    "right_eye": "healthcare-da",
    "nose": "healthcare-signal-platform",
    "body": "healthcare-genai-engineer",
}

HIGH_RISK_TERMS = (
    "cardiac arrest", "stroke", "stemi", "chest pain", "diaphoresis",
    "sepsis", "septic", "respiratory failure", "anaphylax", "suicid",
)
MODERATE_TERMS = ("shortness of breath", "fever", "vomiting", "abdominal pain")
TOKEN_RE = re.compile(r"[a-z0-9]+")


def _repo(name: str) -> Path:
    path = SOURCES / REPOS[name]
    if not path.exists():
        raise FileNotFoundError(f"missing sibling source: {path}; run `make sync`")
    return path


def _commit(path: Path) -> str:
    return subprocess.check_output(
        ["git", "-C", str(path), "rev-parse", "HEAD"], text=True
    ).strip()


def _json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _line_count(path: Path) -> int:
    with path.open(encoding="utf-8") as handle:
        return sum(1 for _ in handle)


def nose_route(query: str) -> dict[str, Any]:
    """Cheap, pre-retrieval safety router with a committed signal receipt."""
    proof_path = (
        _repo("nose")
        / "openfda_signals"
        / "proof"
        / "bullet5_scaled_proof.json"
    )
    proof = _json(proof_path)
    text = query.lower()
    high_hits = [term for term in HIGH_RISK_TERMS if term in text]
    moderate_hits = [term for term in MODERATE_TERMS if term in text]
    routed = bool(high_hits or moderate_hits)
    return {
        "executed_before_eyes": True,
        "route_to_eyes": routed,
        "reason": (
            f"safety terms fired: {high_hits + moderate_hits}"
            if routed
            else "no cheap safety term fired; expensive eyes skipped"
        ),
        "batch_signals_proven": ["anomaly", "cluster", "classify", "rank", "retrieval"],
        "per_case_method": "cheap safety-term gate",
        "source_commit": _commit(_repo("nose")),
        "source_artifact": str(proof_path.relative_to(ROOT)),
        "batch_n": proof["n_reports"],
        "batch_llm_call_reduction_pct": proof["router_ablation"][
            "llm_calls_reduced_pct_at_95_recall"
        ],
        "batch_serious_recall": proof["router_ablation"]["operating_point"][
            "serious_recall"
        ],
    }


def left_eye(query: str, k: int = 5) -> dict[str, Any]:
    """Search the full 55,500-row synthetic encounter corpus."""
    repo = _repo("left_eye")
    path = repo / "data" / "raw" / "healthcare_dataset.csv"
    query_tokens = set(TOKEN_RE.findall(query.lower()))
    ranked: list[tuple[int, int, dict[str, str]]] = []
    with path.open(newline="", encoding="utf-8") as handle:
        for row_number, row in enumerate(csv.DictReader(handle), start=1):
            text = " ".join(
                row.get(key, "")
                for key in (
                    "Age", "Gender", "Medical Condition", "Admission Type",
                    "Medication", "Test Results",
                )
            ).lower()
            score = len(query_tokens & set(TOKEN_RE.findall(text)))
            if score:
                ranked.append((score, row_number, row))
    ranked.sort(key=lambda item: (-item[0], item[1]))
    hits = [
        {
            "source_id": f"encounter:{row_number}",
            "score": score,
            "condition": row["Medical Condition"],
            "medication": row["Medication"],
            "admission_type": row["Admission Type"],
        }
        for score, row_number, row in ranked[:k]
    ]
    reconciliation = _json(repo / "quality" / "proof_reconciliation.json")
    return {
        "source": "synthetic patient encounters",
        "source_commit": _commit(repo),
        "source_artifact": str(path.relative_to(ROOT)),
        "rows_scanned": _line_count(path) - 1,
        "reconciliation": reconciliation["grain_chain"],
        "hits": hits,
    }


def right_eye(query: str, k: int = 5) -> dict[str, Any]:
    """Retrieve real openFDA adverse-event evidence by drug and reaction terms."""
    signal_repo = _repo("nose")
    path = signal_repo / "openfda_signals" / "data" / "openfda_reports_scaled.json"
    reports = _json(path)
    query_tokens = set(TOKEN_RE.findall(query.lower()))
    ranked = []
    for report in reports:
        drug_tokens = set(TOKEN_RE.findall(report.get("primary_drug", "").lower()))
        reaction_tokens = set(TOKEN_RE.findall(report.get("reactions", "").lower()))
        # Exact drug evidence is more valuable than a generic symptom overlap.
        score = 3 * len(query_tokens & drug_tokens) + len(query_tokens & reaction_tokens)
        if score:
            ranked.append((score, report))
    ranked.sort(key=lambda item: (-item[0], item[1]["safetyreportid"]))
    hits = [
        {
            "source_id": f"openfda:{report['safetyreportid']}",
            "score": score,
            "primary_drug": report["primary_drug"],
            "is_serious": report["is_serious"],
            "reactions": report["reactions"],
        }
        for score, report in ranked[:k]
    ]
    semantic_proof = _json(_repo("right_eye") / "proof" / "reconcile_gcp_fabric.json")
    return {
        "source": "real openFDA FAERS adverse-event reports",
        "source_commit": _commit(signal_repo),
        "source_artifact": str(path.relative_to(ROOT)),
        "reports_scanned": len(reports),
        "semantic_layer_commit": _commit(_repo("right_eye")),
        "semantic_layer_artifact": str(
            (_repo("right_eye") / "proof" / "reconcile_gcp_fabric.json").relative_to(ROOT)
        ),
        "semantic_layer_n": semantic_proof["n_reports"],
        "hits": hits,
    }


def _load_body() -> None:
    body = str(_repo("body"))
    if body not in sys.path:
        sys.path.insert(0, body)


def brain_and_hands(
    query: str,
    *,
    correlation_id: str,
    er_state: dict[str, Any],
    left: dict[str, Any],
    right: dict[str, Any],
    db_path: Path,
) -> dict[str, Any]:
    """Use the L2 brain and durable action loop, then re-read the outcome."""
    _load_body()
    from action_engine.loop import run_action_loop
    from action_engine.store import ActionStore
    from workflows.classify_esi import rule_based_esi

    esi, red_flags = rule_based_esi(query)
    triage = "NOW" if esi <= 2 else "SOON" if esi == 3 else "WAIT"
    bed_pressure = (
        "high"
        if er_state["occupancy_pct"] >= 95 or er_state["available_beds"] <= 1
        else "medium"
        if er_state["occupancy_pct"] >= 85
        else "low"
    )
    record = {
        "correlation_id": correlation_id,
        "evidence": {
            "ingested_at": datetime.now(timezone.utc).isoformat(),
            "triage_level": triage,
            "predicted_los_hours": 48 if triage == "NOW" else 12,
            "bed_pressure_risk": bed_pressure,
            "er_state": er_state,
        },
    }
    store = ActionStore(db_path)
    try:
        result = run_action_loop(store=store, record=record)
        action = store.get_action(correlation_id)
        outcome = store.get_outcome(correlation_id)
        events = store.events_for(correlation_id)
    finally:
        store.close()
    receipt = json.loads(action["receipt_json"]) if action else {}
    return {
        "source_commit": _commit(_repo("body")),
        "triage_level": triage,
        "red_flags": red_flags,
        "decision_basis": {
            "left_eye_hits": len(left["hits"]),
            "right_eye_hits": len(right["hits"]),
            "right_eye_is_advisory": True,
            "er_state": er_state,
        },
        "disposition": result.disposition,
        "task_id": result.task_id,
        "receiver_acknowledged": result.acknowledged,
        "action_status": action["status"] if action else None,
        "before_state": json.loads(action["before_state_json"]) if action else None,
        "after_state": json.loads(action["after_state_json"]) if action else None,
        "tool_receipt": receipt,
        "outcome_verified": bool(outcome["verified"]) if outcome else False,
        "false_success_detected": bool(outcome["false_success_detected"]) if outcome else False,
        "trace_stages": [event["stage"] for event in events],
    }


def run_case(
    query: str = "62yo male chest pain diaphoresis aspirin",
    *,
    correlation_id: str = "baymax-audit-case",
    er_state: dict[str, Any] | None = None,
    db_path: Path | None = None,
) -> dict[str, Any]:
    er_state = er_state or {
        "available_beds": 1,
        "occupancy_pct": 96,
        "queue_length": 8,
    }
    db_path = db_path or OUTPUTS / "baymax_action.db"
    nose = nose_route(query)
    result: dict[str, Any] = {
        "audit_version": "baymax.v1",
        "query": query,
        "correlation_id": correlation_id,
        "flow": ["nose"],
        "nose": nose,
    }
    if not nose["route_to_eyes"]:
        result["verdict"] = "cheap path stopped before eyes; no action attempted"
        return result

    left = left_eye(query)
    right = right_eye(query)
    body = brain_and_hands(
        query,
        correlation_id=correlation_id,
        er_state=er_state,
        left=left,
        right=right,
        db_path=db_path,
    )
    result.update(
        {
            "flow": ["nose", "left_eye", "right_eye", "brain", "hands", "outcome_check"],
            "left_eye": left,
            "right_eye": right,
            "brain_hands": body,
            "verdict": (
                "closed-loop simulation proven"
                if body["outcome_verified"]
                else "action outcome not verified"
            ),
        }
    )
    return result


def main() -> None:
    OUTPUTS.mkdir(parents=True, exist_ok=True)
    db_path = OUTPUTS / "baymax_action.db"
    if db_path.exists():
        db_path.unlink()
    result = run_case(db_path=db_path)
    out = OUTPUTS / "baymax_audit.json"
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    print(f"\nWROTE {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
