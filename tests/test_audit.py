from baymax.audit import ROOT, nose_route, retrieval_discovery, run_audit_suite, run_case
from baymax.served_nose import evaluate_signal_contract
import importlib.util


def _readiness_module():
    path = ROOT / "deployment-readiness" / "verify.py"
    spec = importlib.util.spec_from_file_location("deployment_readiness_verify", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


def test_nose_stops_low_value_case_before_eyes(tmp_path):
    result = run_case(
        "routine medication refill",
        correlation_id="skip-case",
        db_path=tmp_path / "skip.db",
    )
    assert result["flow"] == ["nose"]
    assert result["nose"]["route_to_eyes"] is False
    assert "left_eye" not in result
    assert "brain_hands" not in result
    assert result["nose"]["decided_by"] == "served_signal"
    assert result["nose"]["signal_version"].startswith("esi-attention-router.v1@")


def test_served_nose_routes_serious_case_before_eyes():
    receipt = nose_route("62yo male chest pain diaphoresis aspirin")
    assert receipt["route_to_eyes"] is True
    assert receipt["decided_by"] == "served_signal"
    assert receipt["priority_tier"] <= 3


def test_served_nose_eval_protects_serious_recall_and_measures_reduction():
    metrics = evaluate_signal_contract()
    assert metrics["labelled_cases"] == 497
    assert metrics["serious_case_recall"] >= 0.95
    assert metrics["expensive_path_reduction_pct"] > 0


def test_retrieval_discovery_finds_unmentioned_heart_failure_precedent():
    result = retrieval_discovery()
    assert result["raw_query_missed_target"] is True
    assert result["top_source_id"] == "L1-000497"
    assert "chronic heart failure history" in result["retrieved_evidence"]
    assert result["source_is_synthetic"] is True
    assert "does not diagnose" in result["safety_boundary"]


def test_retrieval_discovery_carries_real_triage_and_disposition():
    result = retrieval_discovery()
    # Comorbidities the patient never mentioned are extracted from the retrieved record.
    assert len(result["retrieved_evidence"]) >= 3
    assert result["medications_on_record"], "medications should be parsed from the record"
    assert result["prior_care"] and "discharged" in result["prior_care"].lower()
    # Triage tier is derived from the real ESI classifier, not hardcoded.
    rec = result["disposition_recommendation"]
    assert rec["triage_tier"] in {"RED", "YELLOW", "GREEN"}
    assert rec["recommended_care_setting"] == "medical_ward_admit"
    # The bed action is a real durable commit that was re-read.
    assert rec["bed_booking"]["outcome_verified"] is True
    assert rec["bed_booking"]["after_state"] is not None
    # Baymax speaks two ways from the same evidence.
    assert "to_clinician" in result["dual_voice"]
    assert "to_family" in result["dual_voice"]


def test_full_baymax_path_reads_both_eyes_and_verifies_action(tmp_path):
    result = run_case(
        correlation_id="full-case",
        db_path=tmp_path / "full.db",
    )
    assert result["flow"] == [
        "nose", "left_eye", "right_eye", "brain", "brakes", "nerves",
        "hands", "outcome_check"
    ]
    assert result["left_eye"]["rows_scanned"] == 55500
    assert result["right_eye"]["reports_scanned"] == 5000
    assert result["brain_hands"]["receiver_acknowledged"] is True
    assert result["brain_hands"]["before_state"]["committed"] is False
    assert result["brain_hands"]["after_state"]["committed"] is True
    assert result["brain_hands"]["outcome_verified"] is True


def test_cross_domain_eye_changes_action_policy(tmp_path):
    er_state = {"available_beds": 0, "occupancy_pct": 80, "queue_length": 2}
    patient_only = run_case(
        "abdominal pain after ibuprofen",
        correlation_id="patient-only",
        er_state=er_state,
        db_path=tmp_path / "patient.db",
        right_eye_enabled=False,
    )
    cross_domain = run_case(
        "abdominal pain after ibuprofen",
        correlation_id="cross-domain",
        er_state=er_state,
        db_path=tmp_path / "cross.db",
    )
    assert patient_only["brain_hands"]["hands_executed"] is True
    assert patient_only["brain_hands"]["disposition"] == "discharge_plan"
    assert cross_domain["brain_hands"]["cross_domain_decision_change"]["changed"] is True
    assert cross_domain["brain_hands"]["brakes"]["human_review_required"] is True
    assert cross_domain["brain_hands"]["hands_executed"] is False
    assert cross_domain["brain_hands"]["disposition"] == "human_review"
    assert cross_domain["brain_hands"]["receiver_acknowledged"] is True
    assert "does not prove causality" in cross_domain["brain_hands"]["mouth"]


def test_capacity_domain_changes_action(tmp_path):
    query = "62yo male chest pain diaphoresis aspirin"
    bed_available = run_case(
        query,
        correlation_id="capacity-bed",
        er_state={"available_beds": 1, "occupancy_pct": 80, "queue_length": 2},
        db_path=tmp_path / "bed.db",
    )
    gridlock = run_case(
        query,
        correlation_id="capacity-gridlock",
        er_state={"available_beds": 0, "occupancy_pct": 98, "queue_length": 12},
        db_path=tmp_path / "gridlock.db",
    )
    assert bed_available["brain_hands"]["disposition"] == "assign_bed"
    assert gridlock["brain_hands"]["disposition"] == "divert"
    assert bed_available["brain_hands"]["outcome_verified"] is True
    assert gridlock["brain_hands"]["outcome_verified"] is True


def test_immune_suite_pins_counterfactual_behavior():
    suite = run_audit_suite()
    assert suite["immune_proof"]["behavior_changed"] is True
    assert suite["decision_flip_proof"]["action_changed"] is True


def test_honesty_ledger_gates_headline_at_weakest_load_bearing_leaf():
    suite = run_audit_suite()
    ledger = suite["honesty_ledger"]
    # Every core capability lane is accounted for by at least one organ.
    assert {"signal-routing", "data-truth", "evidence-retrieval", "action-engine",
            "clinical-handoff"} <= set(ledger["lanes_proven"])
    # The honesty law: headline ships at the weakest load-bearing organ's verdict.
    rank = {"✅": 2, "🟡": 1, "❌": 0}
    load_bearing = {k: v for k, v in ledger["organs"].items() if v["load_bearing"]}
    weakest = min(rank[v["verdict"]] for v in load_bearing.values())
    assert rank[ledger["headline_verdict"]] == weakest
    assert ledger["weakest_load_bearing_organ"] in load_bearing
    # ❌ leaves are never claimed: any organ that failed its live gate must be RED.
    for organ in ledger["organs"].values():
        if not organ["live_gate_passed"]:
            assert organ["verdict"] == "❌"
    # Each organ cites a real sibling source repo and one capability lane.
    for organ in ledger["organs"].values():
        assert organ["source_repo"]
        assert organ["capability_lane"]


def test_ui_story_is_bound_to_honest_proof():
    html = (ROOT / "ui" / "index.html").read_text(encoding="utf-8")
    script = (ROOT / "ui" / "app.js").read_text(encoding="utf-8")
    hero_gif = ROOT / "demo.gif"
    assert "../outputs/baymax_audit.json" in html
    assert "../outputs/baymax_audit.json" in script
    assert hero_gif.stat().st_size > 50_000
    assert "action_changed === true" in script
    assert "hands_executed === false" in script
    assert "receiver_acknowledged === true" in script
    assert "https://github.com/anix-lynch/baymax" in html
    assert "deployment_readiness_receipt.json" in html
    assert 'nose.decided_by === "served_signal"' in script
    assert "retrieval_discovery" in script
    assert "Warfarin" not in html + script


def test_simulated_readiness_contract_detects_false_success():
    run_audit_suite()
    module = _readiness_module()
    receipt = module.build_receipt()
    assert receipt["label"] == "SIMULATED DEPLOYMENT READINESS"
    assert receipt["acceptance"]["passed"] is True
    assert receipt["incident_drill"]["breach_detected"] is True
    assert receipt["incident_drill"]["decision"] == "rollback_required"
    assert receipt["release_decision"] == "eligible_for_simulated_shadow"


def test_corpus_augmentation_is_disclosed_and_schema_validated():
    result = retrieval_discovery()
    ca = result["corpus_augmentation"]
    assert ca["present_in_upstream_commit"] is False
    assert ca["lineage_class"] == "downstream_augmentation"
    assert ca["reconciles_to_upstream"] is False
    assert ca["schema_validation"]["conforms"] is True
    assert ca["schema_validation"]["unknown_fields_rejected"] == []


def test_contract_rejects_downstream_invented_fields():
    import importlib.util
    import pytest

    path = ROOT / "scripts" / "inject_mother_case.py"
    spec = importlib.util.spec_from_file_location("inj_contract", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    # A field the upstream schema never declared must be rejected, not silently dropped.
    with pytest.raises(ValueError):
        module.validate_against_contract(
            {"Name": "x", "made_up_downstream_field": "y"}, ["Name", "Age"]
        )


def test_state_awareness_detects_worsened_state_and_changes_plan():
    result = retrieval_discovery()
    s = result["state_awareness"]
    # A prior treatment succeeded, but the patient's state has worsened since.
    assert s["prior_success"] is True
    assert s["past_state"] == "CKD stage 2"
    assert s["current_state"] == "CKD stage 3"
    assert s["state_changed"] is True
    # Therefore the previous protocol is no longer the safe default.
    assert s["previous_protocol_still_optimal"] is False
    assert "stage 2 -> stage 3" in s["reasoning"]
