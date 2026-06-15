#!/usr/bin/env python3
"""Inject the synthetic 'mother' encounter into the genai L1 corpus.

Why this exists: the sibling source corpora under sources/ are git-ignored and
rebuilt by `make sync`. This committed, idempotent step re-adds the mother case
after every sync so the retriever genuinely surfaces her record — the discovery
demo is reproducible from a clean checkout, not patched only in the frontend.

Idempotent: removes any prior injected row before appending exactly one.
"""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "sources" / "healthcare-genai-engineer" / "data" / "raw" / "healthcare_dataset.csv"
MARK = "SYNTHETIC-MOTHER-EDEMA"

MOTHER = {
    "Name": f"{MARK} (synthetic)",
    "Age": "71",
    "Gender": "Female",
    "Blood Type": "O+",
    "Medical Condition": "Heart Failure",
    "Date of Admission": "2026-06-10",
    "Doctor": "ER Night Shift",
    "Hospital": "Synthetic General",
    "Insurance Provider": "Synthetic",
    "Billing Amount": "0",
    "Room Number": "0",
    "Admission Type": "Emergency",
    "Discharge Date": "",
    "Medication": "Furosemide",
    "Test Results": "Abnormal",
    "chief_complaint": "Bilateral leg swelling and fluid retention for one week",
    "hpi": ("71-year-old female with type-2 diabetes and chronic kidney disease stage 3 "
            "presents with progressive bilateral lower-extremity edema, leg swelling and "
            "fluid retention over one week, with fatigue and mild dyspnea on exertion and "
            "orthopnea when lying flat. Home medications: metformin, lisinopril, furosemide. "
            "Reduced urine output over the past three days."),
    "physician_note": ("History of congestive heart failure. Prior ED visit eight months ago: "
                       "admitted two days for bilateral leg edema, diuresed, symptoms resolved, "
                       "discharged without nephrology follow-up. Pattern consistent with recurrent "
                       "fluid overload from combined cardiac and renal disease."),
    "bp_systolic": "158", "bp_diastolic": "92", "heart_rate": "92",
    "respiratory_rate": "20", "temperature_f": "98.4", "spo2_pct": "94",
    "lab_panel_json": "{}",
    "lab_flags": "elevated creatinine; elevated BNP",
    "esi_tier_truth": "",
    "acuity_red_flags": "fluid overload; reduced urine output; orthopnea",
    "holdout": "1",
}


def ensure_mother_case() -> str:
    """Append the mother case if absent. Returns its synthetic case_id."""
    if not CORPUS.exists():
        raise FileNotFoundError(f"corpus not found at {CORPUS}; run `make sync` first")
    rows = list(csv.DictReader(CORPUS.open(newline="")))
    fieldnames = list(rows[0].keys())
    rows = [r for r in rows if MARK not in (r.get("Name") or "")]
    row = {k: "" for k in fieldnames}
    row.update({k: v for k, v in MOTHER.items() if k in fieldnames})
    rows.append(row)
    with CORPUS.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return f"L1-{len(rows) - 1:06d}"


if __name__ == "__main__":
    print("injected mother case:", ensure_mother_case())
