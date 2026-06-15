#!/usr/bin/env python3
"""One-command evidence-to-action audit across Baymax sibling repositories."""
from __future__ import annotations

import csv
import json
import re
import subprocess
import sys
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

# Honesty law: every organ ships at the strength of its weakest load-bearing proof,
# maps to exactly one capability lane, and may only claim the one sentence its proof
# earns. A live gate must pass (else the verdict drops to RED); the maturity grade
# then sets GREEN vs YELLOW. Numbers come from the live run, never from memory.
GREEN, YELLOW, RED = "✅", "🟡", "❌"
_GRADE_TIER = {"A": GREEN, "A-": GREEN, "B+": YELLOW, "B": YELLOW, "C": RED}

# organ -> (capability lane, source repo, load_bearing, claim_allowed, hedge)
ORGAN_LANE = {
    "nose": {
        "lane": "signal-routing",
        "source_repo": "healthcare-genai-engineer",
        "load_bearing": True,
        "claim_allowed": "routes each patient case through a versioned, evaluated pre-retrieval attention signal before opening expensive eyes",
        "hedge": "the served patient router is deterministic and evaluated on synthetic labelled cases; the 30% openFDA router win is a separate batch-domain proof",
    },
    "left_eye": {
        "lane": "data-truth",
        "source_repo": "healthcare-ai-data-engineer",
        "load_bearing": True,
        "claim_allowed": "scans the full 55,500-row encounter corpus with source-commit lineage",
        "hedge": "encounters are synthetic, not real patient records",
    },
    "right_eye": {
        "lane": "evidence-retrieval",
        "source_repo": "healthcare-da",
        "load_bearing": True,
        "claim_allowed": "retrieves real openFDA adverse-event evidence by drug and reaction terms",
        "hedge": "openFDA is a population safety signal only; it does not prove causality or a drug interaction",
    },
    "brain": {
        "lane": "action-engine",
        "source_repo": "healthcare-genai-engineer",
        "load_bearing": True,
        "claim_allowed": "records patient-only and cross-domain decisions separately and changes action policy on the same case",
        "hedge": "decision-change quality is not yet evaluated on a large independent counterfactual set",
    },
    "brakes": {
        "lane": "action-engine",
        "source_repo": "healthcare-genai-engineer",
        "load_bearing": True,
        "claim_allowed": "blocks autonomous action when cross-domain evidence adds uncertainty, without inventing causality",
        "hedge": "the policy matrix for stale, conflicting, missing, and adversarial evidence is not yet covered",
    },
    "nerves": {
        "lane": "clinical-handoff",
        "source_repo": "healthcare-forward-deployed-engineer",
        "load_bearing": True,
        "claim_allowed": "hands work to Bed Ops or clinician review and records a receiver ACK",
        "hedge": "timeout, retry, and dead-letter recovery across separate services is not yet proven",
    },
    "hands": {
        "lane": "action-engine",
        "source_repo": "healthcare-genai-engineer",
        "load_bearing": True,
        "claim_allowed": "commits idempotent bounded actions to durable state and re-reads the outcome",
        "hedge": "a second independently implemented tool target is not yet added",
    },
    "mouth": {
        "lane": "explanation",
        "source_repo": "healthcare-genai-engineer",
        "load_bearing": False,
        "claim_allowed": "explains why it acted or stopped and states the FAERS causality boundary",
        "hedge": "explanations are not yet scored for completeness or unsupported claims",
    },
    "immune": {
        "lane": "regression-guard",
        "source_repo": "healthcare-genai-engineer",
        "load_bearing": False,
        "claim_allowed": "pins the counterfactual decision-change in CI so behavior cannot silently regress",
        "hedge": "the regression suite does not yet span all organs and failure families",
    },
}


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
    """Cheap, pre-retrieval router with served and batch-domain signal receipts."""
    proof_path = (
        _repo("nose")
        / "openfda_signals"
        / "proof"
        / "bullet5_scaled_proof.json"
    )
    proof = _json(proof_path)
    try:
        from baymax.served_nose import route_signal

        served = route_signal(query)
    except Exception as exc:
        # Fail safe if the served contract cannot load: rules may open the eyes,
        # but never claim the evaluated signal made the decision.
        text = query.lower()
        hits = [
            term for term in HIGH_RISK_TERMS + MODERATE_TERMS if term in text
        ]
        served = {
            "route_to_eyes": bool(hits),
            "signal_version": None,
            "route_reason": f"served signal unavailable; safety floor fired: {hits}",
            "priority_tier": None,
            "priority_score": None,
            "signal_flags": hits,
            "decided_by": "safety_floor",
            "evaluation": None,
            "error": type(exc).__name__,
        }
    return {
        "executed_before_eyes": True,
        **served,
        "reason": served["route_reason"],
        "batch_domain_signals_proven": ["anomaly", "cluster", "classify", "rank", "retrieval"],
        "per_case_method": "served deterministic ESI attention signal",
        "batch_domain_source_repo": "healthcare-signal-platform",
        "batch_domain_source_commit": _commit(_repo("nose")),
        "batch_domain_source_artifact": str(proof_path.relative_to(ROOT)),
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


COMORBIDITY_PHRASES = {
    "chronic heart failure history": ("heart failure", "congestive heart failure", "chf"),
    "chronic kidney disease (stage 3)": ("chronic kidney disease", "ckd", "renal disease"),
    "type 2 diabetes": ("diabetes", "diabetic"),
    "prior fluid overload / pulmonary edema": ("fluid overload", "fluid retention", "pulmonary edema"),
    "reduced urine output": ("reduced urine output", "decreased urine", "oliguria"),
    "bilateral lower-extremity edema": ("lower-extremity edema", "leg swelling", "leg edema"),
}
_MED_PHRASES = ("metformin", "lisinopril", "furosemide", "insulin", "warfarin",
                "spironolactone", "aspirin", "carvedilol")


def _extract_present(text: str, mapping: dict[str, tuple[str, ...]]) -> list[str]:
    low = text.lower()
    return [label for label, needles in mapping.items() if any(n in low for n in needles)]


def _extract_meds(text: str) -> list[str]:
    low = text.lower()
    return [m for m in _MED_PHRASES if m in low]


def _triage_tier(esi: int) -> str:
    return "RED" if esi <= 2 else "YELLOW" if esi == 3 else "GREEN"


def _discovery_disposition(triage_level: str, er_state: dict[str, Any], db_path: Path) -> dict[str, Any]:
    """Run the REAL durable bed action so the mother case carries a real disposition."""
    _load_body()
    from action_engine.loop import run_action_loop
    from action_engine.store import ActionStore

    if db_path.exists():
        db_path.unlink()
    record = {
        "correlation_id": "discovery-disposition",
        "evidence": {
            "ingested_at": datetime.now(timezone.utc).isoformat(),
            "triage_level": triage_level,
            "predicted_los_hours": 48 if triage_level == "NOW" else 18,
            "bed_pressure_risk": (
                "high" if er_state["occupancy_pct"] >= 95 or er_state["available_beds"] <= 1 else "medium"
            ),
            "er_state": er_state,
        },
    }
    store = ActionStore(db_path)
    try:
        result = run_action_loop(store=store, record=record)
        action = store.get_action("discovery-disposition")
        outcome = store.get_outcome("discovery-disposition")
    finally:
        store.close()
    return {
        "disposition": result.disposition,
        "task_id": result.task_id,
        "receiver_acknowledged": result.acknowledged,
        "before_state": json.loads(action["before_state_json"]) if action else None,
        "after_state": json.loads(action["after_state_json"]) if action else None,
        "outcome_verified": bool(outcome["verified"]) if outcome else False,
    }


def retrieval_discovery() -> dict[str, Any]:
    """Symptom-language expansion uncovers an unmentioned multi-domain trajectory,
    then carries it through real triage and a real durable bed action."""
    injected_case_id = _ensure_mother_case()
    _load_body()
    from retrieval.retriever import search
    from workflows.classify_esi import rule_based_esi

    patient_words = "my mother's legs are swollen"
    evidence_query = "leg swelling edema fluid retention fatigue"
    raw_hits = search(patient_words, k=3)
    expanded_hits = search(evidence_query, k=3)
    top = expanded_hits[0]
    raw = top["raw"]

    narrative = " ".join([
        raw.get("Medical Condition", ""), raw.get("chief_complaint", ""),
        raw.get("hpi", ""), raw.get("physician_note", ""),
    ])
    retrieved_evidence = _extract_present(narrative, COMORBIDITY_PHRASES)
    medications = _extract_meds(narrative + " " + raw.get("Medication", ""))
    prior_care = next(
        (s.strip() for s in re.split(r"(?<=[.])\s+", raw.get("physician_note", ""))
         if any(w in s.lower() for w in ("prior", "admitted", "discharged"))),
        None,
    )

    esi, red_flags = rule_based_esi(narrative)
    triage_level = _triage_from_esi(esi)
    surface_tier = _triage_tier(esi)

    er_state = {"available_beds": 0, "occupancy_pct": 97, "queue_length": 9}
    booking = _discovery_disposition(triage_level, er_state, OUTPUTS / "discovery_disposition.db")

    # Cross-domain flip: the surface triage under-calls a multi-comorbidity patient.
    # Baymax escalates the recommendation when the retrieved evidence predicts bounce-back.
    bounce_back_risk = len(retrieved_evidence) >= 3
    care_setting = "medical_ward_admit" if bounce_back_risk else "discharge_with_followup"
    recommended_tier = (
        "YELLOW" if bounce_back_risk and surface_tier == "GREEN" else surface_tier
    )
    max_wait_minutes = {"RED": 0, "YELLOW": 120, "GREEN": 240}[recommended_tier]

    disposition_recommendation = {
        "surface_triage_tier": surface_tier,
        "triage_tier": recommended_tier,
        "esi_level": esi,
        "surface_bed_disposition": booking["disposition"],
        "recommended_care_setting": care_setting,
        "escalation_trigger": (
            "Escalate to RED / ICU now if SpO2 falls below 92% or orthopnea worsens — "
            "fluid backing into the lungs strains the heart and cannot wait."
        ),
        "rationale": (
            "Surface triage on leg swelling alone routes toward discharge, repeating the prior "
            "visit. Retrieved comorbidities (heart failure, kidney disease, diabetes) predict "
            "recurrent fluid overload, so Baymax recommends admission and nephrology review "
            "rather than a plain discharge."
        ),
        "max_wait_minutes": max_wait_minutes,
        "bed_booking": {
            "er_state": er_state,
            "er_saturated": er_state["available_beds"] <= 0 or er_state["occupancy_pct"] >= 95,
            "surface_action_taken": booking["disposition"],
            "task_id": booking["task_id"],
            "receiver_acknowledged": booking["receiver_acknowledged"],
            "before_state": booking["before_state"],
            "after_state": booking["after_state"],
            "outcome_verified": booking["outcome_verified"],
            "note": (
                f"Bed engine committed '{booking['disposition']}' to durable state and re-read it. "
                "The ER is full; Baymax flags this as the same path that bounced back last time and "
                "recommends admission instead of leaving the patient in the ER queue."
            ),
        },
    }

    dual_voice = {
        "to_clinician": (
            f"Triage {recommended_tier} (ESI {esi}). Leg swelling is likely recurrent fluid overload from "
            "combined cardiac and renal disease, not an isolated leg problem. The prior visit discharged "
            "after two days without nephrology follow-up. Recommend admission, review diuretic dosing "
            "against stage-3 kidney function, and reassess before any discharge."
        ),
        "to_family": (
            "When your mother's legs get tight and swollen, it usually means her blood sugar and fluid "
            "are not under control. Please help her keep sugar and salt low, write down how often she "
            "passes urine, and tell the doctor about her diabetes and kidney history. If she becomes "
            "short of breath lying flat, that is urgent."
        ),
    }

    return {
        "reporter": "adult child at intake (patient is the mother)",
        "patient_words": patient_words,
        "surface_symptom": "leg swelling",
        "retrieval_method": "BM25 over enriched synthetic encounter narratives",
        "corpus_augmentation": {
            "augmented": True,
            "synthetic_rows_added": 1,
            "injected_case_id": injected_case_id,
            "row_marker": "SYNTHETIC-MOTHER-EDEMA",
            "holdout": True,
            "excluded_from_labelled_eval": True,
            "present_in_upstream_commit": False,
            "downstream_warning": (
                "Local augmentation only. Dense/Vertex index rebuilds from this corpus will "
                "include the marked synthetic row; filter by holdout==1 or the row marker "
                "before any non-demo use. The upstream L1 source-of-truth was not modified."
            ),
        },
        "raw_query_top_source_id": raw_hits[0]["case_id"],
        "raw_query_missed_target": raw_hits[0]["case_id"] != top["case_id"],
        "evidence_query": evidence_query,
        "top_source_id": top["case_id"],
        "top_relevance_score": top["score"],
        "source_commit": _commit(_repo("body")),
        "source_artifact": "sources/healthcare-genai-engineer/data/raw/healthcare_dataset.csv",
        "source_is_synthetic": True,
        "retrieved_evidence": retrieved_evidence,
        "medications_on_record": medications,
        "prior_care": prior_care,
        "evidence_path": [
            "leg swelling (what the family said)",
            "type 2 diabetes",
            "chronic kidney disease",
            "fluid overload",
            "bilateral leg edema",
        ],
        "triage": {
            "esi_level": esi,
            "triage_level": triage_level,
            "triage_tier": surface_tier,
            "recommended_tier": recommended_tier,
            "red_flags": red_flags,
        },
        "disposition_recommendation": disposition_recommendation,
        "dual_voice": dual_voice,
        "next_question": "Has her urine output decreased over the last few days?",
        "safety_boundary": (
            "This retrieves a synthetic precedent, recommends a disposition, and suggests "
            "questions; it does not diagnose the patient or prescribe treatment."
        ),
        "source_receipt": {
            "condition": raw["Medical Condition"],
            "chief_complaint": raw["chief_complaint"],
            "hpi": raw["hpi"],
            "assessment_plan": raw["physician_note"],
        },
    }


def right_eye(query: str, k: int = 5) -> dict[str, Any]:
    """Retrieve real openFDA adverse-event evidence by drug and reaction terms."""
    signal_repo = _repo("nose")
    path = signal_repo / "openfda_signals" / "data" / "openfda_reports_scaled.json"
    reports = _json(path)
    query_tokens = set(TOKEN_RE.findall(query.lower()))
    ranked = []
    exact_drug_reports = []
    for report in reports:
        drug_tokens = set(TOKEN_RE.findall(report.get("primary_drug", "").lower()))
        reaction_tokens = set(TOKEN_RE.findall(report.get("reactions", "").lower()))
        # "Exact drug" means the full reported drug name appears in the query.
        # This avoids treating a generic token such as "pain" as a medication.
        if drug_tokens and drug_tokens.issubset(query_tokens):
            exact_drug_reports.append(report)
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
            "reactions_preview": report["reactions"][:240],
        }
        for score, report in ranked[:k]
    ]
    exact_serious = sum(bool(report["is_serious"]) for report in exact_drug_reports)
    serious_rate = (
        round(exact_serious / len(exact_drug_reports), 3)
        if exact_drug_reports
        else None
    )
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
        "drug_safety_signal": {
            "exact_drug_reports": len(exact_drug_reports),
            "exact_drug_serious_reports": exact_serious,
            "exact_drug_serious_rate": serious_rate,
            "interpretation": (
                "population safety signal only; does not prove causality or a drug interaction"
            ),
        },
        "hits": hits,
    }


def _load_body() -> None:
    body = str(_repo("body"))
    if body not in sys.path:
        sys.path.insert(0, body)


def _ensure_mother_case() -> str:
    """Idempotently re-inject the synthetic mother case into the synced corpus so
    the discovery trajectory is reproducible after any `make sync`. Returns the
    synthetic case_id so the lineage receipt can disclose the augmentation."""
    import importlib.util

    path = ROOT / "scripts" / "inject_mother_case.py"
    spec = importlib.util.spec_from_file_location("inject_mother_case", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module.ensure_mother_case()


def _triage_from_esi(esi: int) -> str:
    return "NOW" if esi <= 2 else "SOON" if esi == 3 else "WAIT"


def _cross_domain_brake(preliminary_triage: str, right: dict[str, Any]) -> dict[str, Any]:
    """Block autonomous action when external safety evidence adds uncertainty."""
    signal = right["drug_safety_signal"]
    enough_reports = signal["exact_drug_reports"] >= 3
    high_serious_rate = (signal["exact_drug_serious_rate"] or 0) >= 0.8
    requires_review = preliminary_triage != "NOW" and enough_reports and high_serious_rate
    return {
        "autonomous_action_allowed": not requires_review,
        "human_review_required": requires_review,
        "reason": (
            "Cross-domain drug-safety signal adds material uncertainty; "
            "block autonomous disposition and request clinician review."
            if requires_review
            else "No cross-domain safety signal strong enough to block the bounded action path."
        ),
        "rule": "non-NOW + >=3 exact-drug reports + >=80% serious -> human review",
    }


def _mouth(
    *,
    preliminary_triage: str,
    final_triage: str,
    right: dict[str, Any],
    brake: dict[str, Any],
    disposition: str | None,
) -> str:
    signal = right["drug_safety_signal"]
    if brake["human_review_required"]:
        return (
            f"Patient evidence alone suggested {preliminary_triage}. "
            f"The drug-safety eye found {signal['exact_drug_serious_reports']}/"
            f"{signal['exact_drug_reports']} exact-drug reports marked serious. "
            "That population signal does not prove causality, so Baymax did not "
            "change clinical triage or act autonomously; it requested human review."
        )
    return (
        f"Patient evidence supports {final_triage}; the cross-domain safety check "
        f"did not block the bounded Bed Ops action {disposition}."
    )


def brain_nerves_hands(
    query: str,
    *,
    correlation_id: str,
    er_state: dict[str, Any],
    left: dict[str, Any],
    right: dict[str, Any],
    db_path: Path,
) -> dict[str, Any]:
    """Combine both eyes, apply brakes, then act or hand off for review."""
    _load_body()
    from action_engine.loop import run_action_loop
    from action_engine.store import ActionStore
    from action_engine.worker import acknowledge
    from workflows.classify_esi import rule_based_esi

    esi, red_flags = rule_based_esi(query)
    preliminary_triage = _triage_from_esi(esi)
    final_triage = preliminary_triage
    brake = _cross_domain_brake(preliminary_triage, right)
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
            "triage_level": final_triage,
            "predicted_los_hours": 48 if final_triage == "NOW" else 12,
            "bed_pressure_risk": bed_pressure,
            "er_state": er_state,
        },
    }
    store = ActionStore(db_path)
    try:
        if brake["human_review_required"]:
            task_id = f"task:{correlation_id}:cross_domain_review"
            store.create_task(
                task_id,
                correlation_id,
                kind="escalation",
                owner="clinician_review_queue",
                idempotency_key=f"{correlation_id}:cross_domain_review",
            )
            store.log_event(correlation_id, "cross_domain_brake_applied", brake)
            acked = acknowledge(store, task_id, correlation_id)
            result = None
            action = None
            outcome = None
        else:
            result = run_action_loop(store=store, record=record)
            task_id = result.task_id
            acked = result.acknowledged
            action = store.get_action(correlation_id)
            outcome = store.get_outcome(correlation_id)
        events = store.events_for(correlation_id)
    finally:
        store.close()
    receipt = json.loads(action["receipt_json"]) if action else {}
    disposition = result.disposition if result else "human_review"
    return {
        "source_commit": _commit(_repo("body")),
        "preliminary_patient_only_decision": {
            "triage_level": preliminary_triage,
            "autonomous_action_candidate": True,
        },
        "cross_domain_decision_change": {
            "changed": brake["human_review_required"],
            "from": "bounded autonomous action",
            "to": "human review before action" if brake["human_review_required"] else "bounded autonomous action",
            "evidence": right["drug_safety_signal"],
        },
        "final_triage_level": final_triage,
        "red_flags": red_flags,
        "brakes": brake,
        "decision_basis": {
            "left_eye_hits": len(left["hits"]),
            "right_eye_hits": len(right["hits"]),
            "right_eye_is_advisory": True,
            "er_state": er_state,
        },
        "disposition": disposition,
        "task_id": task_id,
        "receiver": "clinician_review_queue" if brake["human_review_required"] else "bed_ops_worker",
        "receiver_acknowledged": acked,
        "hands_executed": action is not None,
        "action_status": action["status"] if action else None,
        "before_state": json.loads(action["before_state_json"]) if action else None,
        "after_state": json.loads(action["after_state_json"]) if action else None,
        "tool_receipt": receipt,
        "outcome_verified": bool(outcome["verified"]) if outcome else False,
        "false_success_detected": bool(outcome["false_success_detected"]) if outcome else False,
        "trace_stages": [event["stage"] for event in events],
        "mouth": _mouth(
            preliminary_triage=preliminary_triage,
            final_triage=final_triage,
            right=right,
            brake=brake,
            disposition=disposition,
        ),
    }


def run_case(
    query: str = "62yo male chest pain diaphoresis aspirin",
    *,
    correlation_id: str = "baymax-audit-case",
    er_state: dict[str, Any] | None = None,
    db_path: Path | None = None,
    right_eye_enabled: bool = True,
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
    right = right_eye(query) if right_eye_enabled else {
        "source": "right eye intentionally disabled for counterfactual",
        "hits": [],
        "drug_safety_signal": {
            "exact_drug_reports": 0,
            "exact_drug_serious_reports": 0,
            "exact_drug_serious_rate": None,
            "interpretation": "counterfactual: no cross-domain evidence supplied",
        },
    }
    body = brain_nerves_hands(
        query,
        correlation_id=correlation_id,
        er_state=er_state,
        left=left,
        right=right,
        db_path=db_path,
    )
    result.update(
        {
            "flow": [
                "nose",
                "left_eye",
                "right_eye" if right_eye_enabled else "right_eye_disabled",
                "brain",
                "brakes",
                "nerves",
                "hands" if body["hands_executed"] else "hands_blocked",
                "outcome_check" if body["hands_executed"] else "human_review_ack",
            ],
            "left_eye": left,
            "right_eye": right,
            "brain_hands": body,
            "verdict": (
                "cross-domain brake and human handoff proven"
                if body["brakes"]["human_review_required"]
                and body["receiver_acknowledged"]
                else "closed-loop simulation proven"
                if body["outcome_verified"]
                else "action outcome not verified"
            ),
        }
    )
    return result


def _organ_live_gate(suite: dict[str, Any], organ: str) -> bool:
    """Did this organ's claim actually hold in THIS run? (gates the verdict to RED)."""
    traj = suite["trajectories"]
    cross = traj["cross_domain_brake"]["brain_hands"]
    bed = traj["capacity_bed_available"]["brain_hands"]
    gates = {
        "nose": (
            traj["attention_skip"]["flow"] == ["nose"]
            and traj["attention_skip"]["nose"]["decided_by"] == "served_signal"
            and bool(traj["attention_skip"]["nose"]["signal_version"])
            and traj["attention_skip"]["nose"]["evaluation"]["serious_case_recall"]
            >= 0.95
        ),
        "left_eye": traj["capacity_bed_available"]["left_eye"]["rows_scanned"] == 55500,
        "right_eye": traj["capacity_bed_available"]["right_eye"]["reports_scanned"] == 5000,
        "brain": suite["decision_flip_proof"]["action_changed"]
        and suite["immune_proof"]["behavior_changed"],
        "brakes": cross["brakes"]["human_review_required"] and not cross["hands_executed"],
        "nerves": cross["receiver_acknowledged"],
        "hands": bed["outcome_verified"] and bool(bed["after_state"]["committed"]),
        "mouth": "does not prove causality" in cross["mouth"],
        "immune": suite["immune_proof"]["behavior_changed"]
        and suite["decision_flip_proof"]["action_changed"],
    }
    return bool(gates[organ])


def honesty_ledger(suite: dict[str, Any]) -> dict[str, Any]:
    """Gate every organ's claim at the weakest load-bearing proof: each organ maps to
    one capability lane and may only claim the sentence its live proof earns."""
    grades = suite["dream_state_audit"]["organs"]
    organs: dict[str, Any] = {}
    for organ, meta in ORGAN_LANE.items():
        # Eyes share one maturity grade in the dream-state audit.
        grade = grades["eyes"]["grade"] if organ in ("left_eye", "right_eye") else grades[organ]["grade"]
        gate_pass = _organ_live_gate(suite, organ)
        verdict = _GRADE_TIER.get(grade, RED) if gate_pass else RED
        organs[organ] = {
            "verdict": verdict,
            "capability_lane": meta["lane"],
            "source_repo": meta["source_repo"],
            "maturity_grade": grade,
            "live_gate_passed": gate_pass,
            "load_bearing": meta["load_bearing"],
            "claim_allowed": meta["claim_allowed"],
            "hedge": meta["hedge"],
        }
    rank = {GREEN: 2, YELLOW: 1, RED: 0}
    load_bearing = {k: v for k, v in organs.items() if v["load_bearing"]}
    weakest_key = min(load_bearing, key=lambda k: rank[load_bearing[k]["verdict"]])
    weakest = load_bearing[weakest_key]
    headline_verdict = weakest["verdict"]
    return {
        "law": (
            "Baymax ships at the strength of its weakest load-bearing organ. "
            "Each organ proves one capability lane and may only claim the sentence its "
            "live proof earns; ❌ leaves are never claimed."
        ),
        "headline_verdict": headline_verdict,
        "weakest_load_bearing_organ": weakest_key,
        "headline_claim_allowed": (
            f"Baymax proves the closed evidence-to-action loop end-to-end, "
            f"but ships at {headline_verdict} — gated by {weakest_key.upper()} "
            f"({weakest['capability_lane']}): {weakest['hedge']}."
        ),
        "organs": organs,
        "lanes_proven": sorted({m["lane"] for m in ORGAN_LANE.values()}),
    }


def run_audit_suite() -> dict[str, Any]:
    """Patient discovery plus trajectories proving attention, change, and action."""
    OUTPUTS.mkdir(parents=True, exist_ok=True)
    paths = {
        "patient_only": OUTPUTS / "patient_only.db",
        "cross_domain": OUTPUTS / "cross_domain.db",
        "capacity_bed": OUTPUTS / "capacity_bed.db",
        "capacity_gridlock": OUTPUTS / "capacity_gridlock.db",
    }
    for path in paths.values():
        if path.exists():
            path.unlink()

    skipped = run_case(
        "routine medication refill",
        correlation_id="attention-skip",
        db_path=OUTPUTS / "attention_skip.db",
    )
    patient_only = run_case(
        "abdominal pain after ibuprofen",
        correlation_id="patient-only",
        er_state={"available_beds": 0, "occupancy_pct": 80, "queue_length": 2},
        db_path=paths["patient_only"],
        right_eye_enabled=False,
    )
    cross_domain = run_case(
        "abdominal pain after ibuprofen",
        correlation_id="cross-domain",
        er_state={"available_beds": 0, "occupancy_pct": 80, "queue_length": 2},
        db_path=paths["cross_domain"],
    )
    capacity_bed = run_case(
        "62yo male chest pain diaphoresis aspirin",
        correlation_id="capacity-bed-available",
        er_state={"available_beds": 1, "occupancy_pct": 80, "queue_length": 2},
        db_path=paths["capacity_bed"],
    )
    capacity_gridlock = run_case(
        "62yo male chest pain diaphoresis aspirin",
        correlation_id="capacity-gridlock",
        er_state={"available_beds": 0, "occupancy_pct": 98, "queue_length": 12},
        db_path=paths["capacity_gridlock"],
    )
    discovery = retrieval_discovery()
    suite: dict[str, Any] = {
        "audit_version": "baymax.v2",
        "one_line_truth": (
            "Baymax allocates attention, changes action policy when another domain "
            "adds risk, and verifies bounded actions when brakes allow them."
        ),
        "trajectories": {
            "retrieval_discovery": discovery,
            "attention_skip": skipped,
            "patient_only_counterfactual": patient_only,
            "cross_domain_brake": cross_domain,
            "capacity_bed_available": capacity_bed,
            "capacity_gridlock": capacity_gridlock,
        },
        "immune_proof": {
            "same_case": "abdominal pain after ibuprofen",
            "patient_only_disposition": patient_only["brain_hands"]["disposition"],
            "cross_domain_disposition": cross_domain["brain_hands"]["disposition"],
            "behavior_changed": (
                patient_only["brain_hands"]["hands_executed"]
                and cross_domain["brain_hands"]["brakes"]["human_review_required"]
                and not cross_domain["brain_hands"]["hands_executed"]
            ),
            "protected_in_ci": "tests/test_audit.py::test_cross_domain_eye_changes_action_policy",
        },
        "decision_flip_proof": {
            "same_case": "62yo male chest pain diaphoresis aspirin",
            "bed_available_disposition": capacity_bed["brain_hands"]["disposition"],
            "gridlock_disposition": capacity_gridlock["brain_hands"]["disposition"],
            "action_changed": (
                capacity_bed["brain_hands"]["disposition"]
                != capacity_gridlock["brain_hands"]["disposition"]
            ),
            "protected_in_ci": "tests/test_audit.py::test_capacity_domain_changes_action",
        },
        "organ_report": {
            "nose": "routes cheap cases before expensive evidence work",
            "eyes": "combine patient precedents with real population drug-safety evidence",
            "brain": "records patient-only and cross-domain final decisions separately",
            "mouth": "explains why Baymax acted or stopped without overstating causality",
            "hands": "commits bounded actions to durable state",
            "nerves": "hands work to Bed Ops or clinician review and records receiver ACK",
            "brakes": "blocks autonomous action when cross-domain evidence adds uncertainty",
            "immune": "counterfactual trajectory is pinned in CI so the behavior cannot silently regress",
        },
        "dream_state_audit": {
            "target": "maximum controllable achievement for a solo Applied AI Engineer",
            "organs": {
                "nose": {
                    "grade": "A-",
                    "current": "versioned pre-retrieval patient attention signal with labelled serious-recall and expensive-path reduction, plus a separate five-signal openFDA batch proof",
                    "a_plus": "improve patient-case cost reduction without dropping the serious-case recall floor",
                },
                "eyes": {
                    "grade": "A-",
                    "current": "patient and real drug-safety evidence with source commit lineage",
                    "a_plus": "stronger retrieval evals and explicit contradiction/novelty scoring across domains",
                },
                "brain": {
                    "grade": "A-",
                    "current": "records a patient-only decision and a cross-domain guarded decision",
                    "a_plus": "evaluate decision-change quality across a larger independent counterfactual set",
                },
                "mouth": {
                    "grade": "B+",
                    "current": "explains why Baymax acted or stopped and states the FAERS causality boundary",
                    "a_plus": "citation-linked human explanations scored for completeness and unsupported claims",
                },
                "hands": {
                    "grade": "A",
                    "current": "idempotent durable action with before/after receipt and outcome re-read",
                    "a_plus": "add a second independently implemented tool target while preserving the same contract",
                },
                "nerves": {
                    "grade": "B+",
                    "current": "durable Bed Ops or clinician-review handoff with receiver ACK",
                    "a_plus": "prove timeout, retry, dead-letter, and recovery across separate local services",
                },
                "brakes": {
                    "grade": "A-",
                    "current": "cross-domain uncertainty blocks autonomous action without inventing causality",
                    "a_plus": "policy matrix covering stale, conflicting, missing, and adversarial evidence",
                },
                "immune": {
                    "grade": "A-",
                    "current": "counterfactual decision-change trajectory pinned in CI",
                    "a_plus": "trajectory regression suite spanning all organs and known failure families",
                },
            },
            "smallest_path_to_complete": [
                "add 20-50 independent cross-domain counterfactual scenarios",
                "run Nerves across separate local services with timeout and dead-letter recovery",
                "improve patient-case attention reduction without dropping serious-case recall below 95%",
            ],
        },
        "recruiter_stop_moments": [
            {
                "moment": "Baymax translates ordinary symptom language into evidence language and retrieves an unmentioned heart-failure precedent",
                "proof": "trajectories.retrieval_discovery",
            },
            {
                "moment": "Baymax refuses to open expensive eyes for a routine case",
                "proof": "trajectories.attention_skip",
            },
            {
                "moment": "The same case changes from discharge_plan to human_review when the drug-safety eye opens",
                "proof": "immune_proof",
            },
            {
                "moment": "Baymax states that openFDA is a population signal, not proof of causality",
                "proof": "trajectories.cross_domain_brake.brain_hands.mouth",
            },
            {
                "moment": "The brake stops the hand, but the clinician-review nerve still receives and ACKs work",
                "proof": "trajectories.cross_domain_brake.brain_hands",
            },
            {
                "moment": "When brakes allow action, durable state changes and Baymax re-reads the outcome",
                "proof": "trajectories.capacity_bed_available.brain_hands",
            },
        ],
    }
    suite["honesty_ledger"] = honesty_ledger(suite)
    return suite


def main() -> None:
    result = run_audit_suite()
    out = OUTPUTS / "baymax_audit.json"
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    print(f"\nWROTE {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
