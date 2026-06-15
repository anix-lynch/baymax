#!/usr/bin/env python3
"""Verify Baymax's simulated rollout contract and run one failure drill."""
from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "deployment-readiness" / "contract.json"
AUDIT_PATH = ROOT / "outputs" / "baymax_audit.json"
RECEIPT_PATH = ROOT / "outputs" / "deployment_readiness_receipt.json"


def _read(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _value_at(document: dict[str, Any], path: str) -> Any:
    value: Any = document
    for part in path.split("."):
        value = value[part]
    return value


def evaluate(document: dict[str, Any], contract: dict[str, Any]) -> list[dict[str, Any]]:
    results = []
    for gate in contract["acceptance_gates"]:
        actual = _value_at(document, gate["path"])
        expected = gate["expected"]
        passed = (
            actual == expected
            if gate["operator"] == "equals"
            else actual >= expected
        )
        results.append(
            {
                "id": gate["id"],
                "description": gate["description"],
                "passed": passed,
                "actual": actual,
                "expected": expected,
                "operator": gate["operator"],
            }
        )
    return results


def build_receipt() -> dict[str, Any]:
    contract = _read(CONTRACT_PATH)
    audit = _read(AUDIT_PATH)
    acceptance = evaluate(audit, contract)

    # Failure drill: a release receipt falsely claims success without a verified
    # durable outcome. The contract must detect it and require rollback.
    corrupted = copy.deepcopy(audit)
    corrupted["trajectories"]["capacity_bed_available"]["brain_hands"][
        "outcome_verified"
    ] = False
    drill_results = evaluate(corrupted, contract)
    detected = any(
        result["id"] == "OUTCOME-001" and not result["passed"]
        for result in drill_results
    )

    all_passed = all(result["passed"] for result in acceptance)
    return {
        "label": contract["label"],
        "contract_version": contract["contract_version"],
        "boundary": contract["boundary"],
        "acceptance": {
            "passed": all_passed,
            "passed_count": sum(result["passed"] for result in acceptance),
            "total_count": len(acceptance),
            "results": acceptance,
        },
        "incident_drill": {
            "scenario": "false success: action receipt loses durable outcome verification",
            "breach_detected": detected,
            "failed_gate": "OUTCOME-001" if detected else None,
            "decision": "rollback_required" if detected else "unsafe_release",
        },
        "release_decision": (
            "eligible_for_simulated_shadow"
            if all_passed and detected
            else "blocked"
        ),
        "rollout": contract["rollout"],
        "handoff": contract["handoff"],
    }


def main() -> int:
    receipt = build_receipt()
    RECEIPT_PATH.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(
        f"{receipt['label']}: {receipt['acceptance']['passed_count']}/"
        f"{receipt['acceptance']['total_count']} gates pass; "
        f"incident={receipt['incident_drill']['decision']}; "
        f"release={receipt['release_decision']}"
    )
    return 0 if receipt["release_decision"] == "eligible_for_simulated_shadow" else 1


if __name__ == "__main__":
    raise SystemExit(main())
