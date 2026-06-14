from baymax.audit import run_audit_suite, run_case


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
