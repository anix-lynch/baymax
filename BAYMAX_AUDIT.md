# Baymax Belt Audit — QA protocol (Claude audits Codex, belt by belt)

> Codex builds per `BAYMAX_BACKEND_TODO.md`. After each belt lands, run this
> audit and emit a verdict. Goal: catch drift, mock-passed-as-real, and
> buzzword-without-behavior before it reaches the demo.

## How I audit one belt
1. Read the new module + the `main.py` endpoint diff.
2. Run it: `python3 -c "import <mod>; print(<mod>.build_...())"` or curl the live endpoint.
3. Score the 6 dimensions below.
4. Emit verdict: ✅ PASS / 🟡 PARTIAL / ❌ FAIL per dimension + a fix-list.

## The 6 audit dimensions (every belt)
```text
1. CONTRACT     response shape == BAYMAX_BACKEND_TODO.md? (front won't break)
2. REAL vs STUB real data/logic, or still mock? — state it honestly, no hiding
3. ACCEPTANCE   belt-specific criteria met (see per-belt below)
4. SAFETY       authority zones server-side · no forbidden action · PII scoped · escalation correct
5. HONESTY      actually demonstrates the reasoning level (not buzzword)
                — the "apples-to-apples intelligent" test from the mockup
6. FRONT        belt flips 🚧→✅ in ui/baymax · renders · graceful offline fallback
```

## Verdict template (copy per belt)
```text
BELT: <name>   DATE: <>   COMMIT: <>
1 CONTRACT  [ ]   2 REAL/STUB [ ]   3 ACCEPTANCE [ ]
4 SAFETY    [ ]   5 HONESTY   [ ]   6 FRONT      [ ]
VERDICT: PASS / PARTIAL / FAIL
FIX-LIST:
 -
```

---

## Per-belt audit criteria + test command

### 🟡 Yellow · nose  (GET /api/signals)  — currently: real proof, served
- ACCEPTANCE: 5 named signals each with an honest metric; router floor + cost cut present.
- HONESTY: metrics are real & modest (not invented targets). Flag if numbers look too clean.
- TEST: `curl -s $API/api/signals | jq '.signals[].name, .router'`

### 🟡 Yellow · state-diff  (GET /api/state-diff)  — currently: STUB demo timeline
- ACCEPTANCE: past vs now + `changed[]` with direction. HARDEN target: pulls 2 real timepoints.
- REAL/STUB: today = STUB (mom-001 only). PASS only when wired to real longitudinal query.
- TEST: `curl -s "$API/api/state-diff?patient_id=mom-001" | jq '.changed,.source'`

### 🟠 Orange · ops/bed + lab  (GET /api/ops/bed, /api/lab-status)
- ACCEPTANCE: `ack=false` when registered≠true even if nurse_said_sent (the ACK truth).
  lab gate returns eta_days when not ready.
- SAFETY: read-only; booking itself stays approval-gated, not auto.
- HONESTY: must distinguish "said sent" vs "registered" — that IS the belt.
- TEST: `curl -s "$API/api/ops/bed?patient_id=mom-001" | jq '.registered,.ack'`

### 🟢 Green · tradeoff  (POST /api/tradeoff)
- ACCEPTANCE: ≥2 options with benefit/risk/reversible/fits_today; `recommend` + `why`.
- HONESTY: recommendation explained (not bare yes/no); counterfactual present; not always "A".
- TEST: `curl -s -X POST $API/api/tradeoff -H 'content-type: application/json' -d '{"patient_id":"mom-001"}' | jq '.recommend,.why,.options'`

### 🔵 Blue · goal/memory  (GET/POST /api/goal)
- ACCEPTANCE: `inferred_goal` ≠ `stated_request`; recalled from store, not echoed from input.
- HONESTY (key): goal must come from MEMORY, not from the current turn — re-test by
  changing the current input and confirming the goal is still recalled (no cheating).
- TEST: `curl -s "$API/api/goal?patient_id=mom-001" | jq '.stated_request,.inferred_goal,.source'`

### ⬛ Black · outcome + trajectory  (GET /api/outcome, /api/trajectory)
- ACCEPTANCE: outcome has stages drafted→…→verified + `open` flag; trajectory has slope + branches.
- HONESTY (the strongest test): outcome must distinguish "submitted" vs "accepted/verified"
  — tool success ≠ real-world success. FAIL if "sent" is reported as "done".
- TEST: `curl -s "$API/api/outcome?action_id=ref-1" | jq '.stage,.open'`

---

## Cross-cutting (audit once, re-check each belt)
```text
HARNESS    3-zone tool policy enforced in code (not just UI label)?  see HARNESS_SPEC.md
AUTHORITY  forbidden actions (change_med, admit/discharge) have NO callable path?  AUTHORITY_SPEC.md
CITATIONS  any clinical claim grounded (ask/citations) or flagged uncertain?
CORS/PII   responses scoped to one patient; no raw PII leak.
```

## Audit log (append verdicts here)
<!-- Claude appends one verdict block per belt as Codex delivers -->
