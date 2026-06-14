#!/usr/bin/env python3
"""Play the three recruiter-readable Baymax cases."""
from __future__ import annotations

import json

from baymax.audit import ROOT, run_audit_suite

LINE = "=" * 72


def _scene(title: str, body: list[str]) -> None:
    print(f"\n{LINE}\n{title}\n{LINE}")
    for line in body:
        print(line)


def main() -> None:
    suite = run_audit_suite()
    cases = suite["trajectories"]
    screenplay = json.loads(
        (ROOT / "cases" / "legendary_cases.json").read_text(encoding="utf-8")
    )

    attention = cases["attention_skip"]
    assert attention["query"] == screenplay["attention_flip"]["case"]
    _scene(
        f"CASE 1 · {screenplay['attention_flip']['title'].upper()}",
        [
            f"Incoming case : {attention['query']}",
            f"NOSE          : {attention['nose']['reason']}",
            "Result        : eyes stayed closed; no action attempted",
        ],
    )

    calm = cases["capacity_bed_available"]
    gridlock = cases["capacity_gridlock"]
    assert calm["query"] == screenplay["decision_flip"]["case"]
    _scene(
        f"CASE 2 · {screenplay['decision_flip']['title'].upper()}",
        [
            f"Same patient  : {calm['query']}",
            f"Bed available : {calm['brain_hands']['disposition']}",
            f"ER gridlock   : {gridlock['brain_hands']['disposition']}",
            "Result        : capacity perspective changed the action",
        ],
    )

    patient_only = cases["patient_only_counterfactual"]
    brake = cases["cross_domain_brake"]
    assert brake["query"] == screenplay["brake_save"]["case"]
    signal = brake["right_eye"]["drug_safety_signal"]
    _scene(
        f"CASE 3 · {screenplay['brake_save']['title'].upper()}",
        [
            f"Same patient  : {brake['query']}",
            f"Patient-only  : {patient_only['brain_hands']['disposition']}",
            (
                "Drug eye      : "
                f"{signal['exact_drug_serious_reports']}/{signal['exact_drug_reports']} "
                "exact-drug reports marked serious"
            ),
            f"Brake         : {brake['brain_hands']['disposition']}",
            f"Nerve ACK     : {brake['brain_hands']['receiver_acknowledged']}",
            "Boundary      : population signal; no causality claim",
        ],
    )

    print(f"\n{LINE}")
    print("BAYMAX MOVIE COMPLETE")
    print("attention allocated · decisions changed · unsafe action stopped")
    print(LINE)


if __name__ == "__main__":
    main()
