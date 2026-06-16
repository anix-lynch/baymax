# Baymax Backend TODO — Yellow → Black (handover for Codex / Claude Code)

> Paste this to Codex. It builds the remaining organ endpoints in the existing
> FastAPI (`sources/healthcare-ai-data-engineer/api/app/`). Pattern to follow:
> one module per organ + a thin `@app.get/post` in `main.py` (same try/except
> import style already used for signals.py / state_diff.py). Keep response
> shapes stable — the front (`ui/baymax/baymax_live.js`) depends on them.

## Status now
```text
✅ White  retrieval     GET /api/retrieve, /api/medications, /api/conditions
✅ Yellow nose          GET /api/signals      (real FAERS proof; HARDEN: live run optional)
✅ Yellow state-diff    GET /api/state-diff   (STUB demo timeline; HARDEN: real longitudinal diff)
✅ Brown  authority     POST /api/classify    (real rules)
🟡 Brain  ask           GET /api/ask          (needs Vertex creds)
🚧 Orange / Green / Blue / Black  → build below
```

---

## 1. 🟠 Orange · Workflow — ACK + lab gate
`GET /api/ops/bed?patient_id=` → bed registration truth (the "ส่งแล้ว ≠ ลงทะเบียนจริง" moment)
```json
{ "requested": true, "registered": false, "nurse_said_sent": true,
  "ack": false, "note": "nurse marked sent; bed not yet registered in ops system" }
```
`GET /api/lab-status?patient_id=` → lab readiness gate
```json
{ "ready": false, "eta_days": 2, "pending": ["creatinine","eGFR"] }
```
- Source: hospital ops/scheduling system (mock a small stateful store first).
- Acceptance: `ack=false` when registered≠true even if nurse_said_sent; front shows "ผมยังไม่ปิดงาน".
- Baymax voice: "พยาบาลบอกส่งแล้ว แต่ผมเช็คระบบ — เตียงยังไม่ลงทะเบียนจริง".

## 2. 🟢 Green · Trade-off
`POST /api/tradeoff` body `{ "patient_id":"mom-001", "context":{...} }` →
```json
{ "options":[
    {"id":"A","label":"ยาขับน้ำซ้ำ","benefit":"บวมยุบเร็ว","risk":"ไตเสี่ยง","reversible":"medium","fits_today":false},
    {"id":"B","label":"ลด intensity + renal review","benefit":"ถนอมไต","risk":"ช้ากว่า","reversible":"high","fits_today":true}],
  "dimensions":["ได้ผลเร็ว","ปลอดภัยต่อไต","ตรงกับ state วันนี้"],
  "recommend":"B","why":"ไต Stage 3 ทำให้ kidney risk แพงกว่าความเร็ว" }
```
- Source: can be rules + `/api/ask` (LLM) over retrieved evidence + state-diff.
- Acceptance: recommend explained by why (not a bare yes/no); counterfactual present.

## 3. 🔵 Blue · Objective + memory
`GET /api/goal?patient_id=` → recalled goal (preference memory)
```json
{ "stated_request":"discharge fast", "inferred_goal":"safe discharge, low rebound",
  "preferences":["plain-language nightly update"], "source":"memory" }
```
`POST /api/goal` to upsert. Use a small persistent store (Mem0/Zep/sqlite/KV).
- Acceptance: goal recalled from memory, NOT from current turn input (no cheating).

## 4. ⬛ Black · Outcome + trajectory
`GET /api/outcome?action_id=` → real-world verify stages
```json
{ "stage":"submitted", "stages":["drafted","submitted","accepted","scheduled","verified"],
  "open": true, "note":"referral sent but appointment not yet booked" }
```
`GET /api/trajectory?patient_id=` → multi-timepoint path (extends state-diff to N points)
```json
{ "points":[{"date":"2024","ckd_stage":2},{"date":"2026","ckd_stage":3}],
  "slope":"worsening", "branches":[{"if":"treat_aggressive","then":"kidney_decline"},{"if":"cautious","then":"stable"}] }
```
- Acceptance: outcome distinguishes "sent" vs "happened" (tool success ≠ real success);
  trajectory shows direction + branches.

---

## Harness (cross-cutting, see HARNESS_SPEC.md / AUTHORITY_SPEC.md)
- 3-zone tool policy (🟢 auto / 🟡 approval / 🔴 forbidden) enforced server-side,
  not just UI. classify's `human_review_required` already models the escalation gate.
- Verify hooks: every action endpoint should expose its outcome stage (see #4).

## Front contract
Each new endpoint flips one belt in `ui/baymax/baymax_live.js` from 🚧 GAP → ✅ LIVE.
Follow the existing nose/state-diff belt blocks as the wiring template.
