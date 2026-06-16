"""
Baymax NERVES ⚡ — longitudinal state-diff (Yellow belt completer).

CONTRACT STUB. The real implementation should pull two timepoints for the same
patient from the longitudinal EHR (e.g. /api/encounters history grouped by
patient) and diff the clinically meaningful fields (CKD stage, eGFR, ejection
fraction, weight trend). Here we serve the canonical swollen-legs demo case so
the front can render the iconic "Stage 2 → Stage 3" moment end-to-end.

CODEX TODO: replace the mock timeline with a real longitudinal query +
field-level diff. Keep the response shape below stable (the front depends on it).
"""
from typing import Any, Dict

# Canonical demo timeline (mother, swollen legs). Replace with real EHR pull.
_DEMO = {
    "mom-001": {
        "past": {"date": "2024", "ckd_stage": 2, "context": "ขาบวม/fluid overload — ยาขับน้ำอ่อนๆ ได้ผล"},
        "now":  {"date": "2026", "ckd_stage": 3, "context": "ขาบวมซ้ำ — ไตสำรองน้อยลง"},
    }
}


def build_state_diff(patient_id: str = "mom-001") -> Dict[str, Any]:
    tl = _DEMO.get(patient_id)
    if not tl:
        return {"available": False, "patient_id": patient_id, "reason": "no longitudinal timeline (stub knows mom-001 only)"}

    changed = []
    for field in ("ckd_stage",):
        a, b = tl["past"].get(field), tl["now"].get(field)
        if a != b:
            changed.append({
                "field": field, "from": a, "to": b,
                "direction": "worse" if isinstance(a, (int, float)) and isinstance(b, (int, float)) and b > a else "changed",
            })

    return {
        "available": True,
        "patient_id": patient_id,
        "past": tl["past"],
        "now": tl["now"],
        "changed": changed,
        "verdict": "state changed — previous protocol may not transfer safely"
                   if changed else "state stable — prior approach may still apply",
        "source": "STUB (demo timeline) — CODEX: wire to longitudinal EHR diff",
    }
