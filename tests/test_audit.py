from baymax.audit import run_case


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
        "nose", "left_eye", "right_eye", "brain", "hands", "outcome_check"
    ]
    assert result["left_eye"]["rows_scanned"] == 55500
    assert result["right_eye"]["reports_scanned"] == 5000
    assert result["brain_hands"]["receiver_acknowledged"] is True
    assert result["brain_hands"]["before_state"]["committed"] is False
    assert result["brain_hands"]["after_state"]["committed"] is True
    assert result["brain_hands"]["outcome_verified"] is True
