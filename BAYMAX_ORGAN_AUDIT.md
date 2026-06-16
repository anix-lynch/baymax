# Baymax Organ Audit — REAL vs Hardcode Theater (lineage review)

> Analyst rule: **an organ may never store the answer. It must compute the answer
> from a source.** A per-patient dict baked into the endpoint = the Excel hardcode
> your old boss hated. It works for `mom-001` and dies for everyone else.

## Verdict (one line)
The **infrastructure is real** (55,500-encounter API, BM25 retrieval, openFDA FAERS
ML, rule-based ESI). But **8 of 12 organs return a hardcoded `mom-001` dict**, so the
emotional story (kidney 2→3, ACK missing, outcome unverified) is a **single-patient
theater**: type any other patient and Baymax goes blank. That is why it "only shines
on mom."

## Score
```
🟢 REAL (computes from a source, works for any input):   3
🟡 SEMI (real mechanism, seeded default):                1
🔴 HARDCODE THEATER (per-patient dict in code):          8
```

## Organ-by-organ ledger

| Organ | Endpoint | Resume claim | What it REALLY is | Verdict |
|---|---|---|---|---|
| 👁 Eyes · retrieval | `/api/retrieve` | "retrieves similar cases" | REAL BM25 over 397-doc corpus, any query | 🟢 real |
| 👃 Nose · signals | `/api/signals` | "cross-domain ML early-warning" | REAL openFDA FAERS 5,000 reports, anomaly/cluster | 🟢 real |
| 🛑 Brakes · authority | `/api/classify` | "safe triage + escalation gate" | REAL rule ESI, fires on any vitals input | 🟢 real |
| 🎯 Memory · goal | `/api/goal` | "remembers the real objective" | REAL sqlite store, BUT seeded default for mom | 🟡 semi |
| ⚡ Nerves · state-diff | `/api/state-diff` | "state-aware longitudinal reasoning" | `_DEMO={"mom-001":{CKD 2→3}}` literal dict | 🔴 hardcode |
| 🖐 Hands · workflow ACK | `/api/ops/bed` | "knows said ≠ done" | `BED_OPS={"mom-001":{ack:false}}` frozen | 🔴 hardcode |
| 👅 Tongue · lab gate | `/api/lab-status` | "waits for fresh labs" | `LAB_STATUS={"mom-001":{...}}` frozen | 🔴 hardcode |
| 🧠 Brain · tradeoff | `/api/tradeoff` | "weighs trade-offs" | static A/B text, ignores patient | 🔴 hardcode |
| 🔭 Far-sight · trajectory | `/api/trajectory` | "multi-timepoint path + branches" | `TRAJECTORIES={"mom-001":{...}}` frozen | 🔴 hardcode |
| 🔍 Verify · outcome | `/api/outcome` | "tool success ≠ real success" | `OUTCOMES={"ref-1","bed-1"}` frozen | 🔴 hardcode |
| ⚡ Nerves · case status | `/v1/cases/{id}/status` | "live execution state" | frozen WAIT_FOR_ACK response | 🔴 hardcode |
| 🗣 Voice · dual | (frontend) | "explains in 2 voices" | hardcoded strings in UI, not from API | 🔴 hardcode |

## Why the resume bullet is WRONG (the analyst objection)
```
Bullet: "state-aware longitudinal reasoning; verifies outcomes; weighs trade-offs"
Reality: each of those reads a per-patient dict. Swap mom-001 → dad-002 and the
         organ returns available:false or nothing. The formula has the answer
         typed into it. That is not reasoning — it is a screenshot with a pulse.
```
The 3 REAL organs survive an interviewer typing a new input. The 8 hardcoded ones
do not. A resume claim is only true if it survives an input it has never seen.

## What "stub" actually means (so no one fools you with the word)
```
stub = a placeholder that returns the RIGHT SHAPE (schema) with FROZEN VALUES (snapshot).
       It is BOTH at once:
         • snapshot → one fixed answer, never computed
         • schema   → keys/shape identical to the real thing
The schema is the costume; the snapshot is the dummy inside. The matching schema
is EXACTLY what lets it pass the eye test on the frontend.

Honest stub  = labels itself + lineage says "no real source" (state-diff does this).
Dishonest    = correct shape, NO label, presented as computed → that is the fooling.
The only thing separating the two is whether it confesses its lineage.
```

## How to design the backend (frontend-first was RIGHT)
Building the frontend first was not a detour — it **defined the contract**: we now know
the exact useful shape each organ must emit. Backend's only remaining job is to
**produce that shape from a real source**, generically.

```
THE RULE (every organ obeys this):
  1. take an id (patient_id / action_id / correlation_id)
  2. read a real store or upstream — never an in-code per-patient dict
  3. COMPUTE the field (diff, group-by, state transition, weighting)
  4. return value + lineage{ source, derived_how, as_of }
  5. if the source has nothing for that id → available:false (do NOT invent)
```

Per family:
```
Longitudinal (state-diff, trajectory):
  generic differ over /api/encounters grouped by patient_id + date.
  upstream lacks CKD staging → inject mom as a DISCLOSED multi-encounter record
  (lineage-marked, like the genai corpus injection). Logic stays generic; the
  value lives in DATA, not in code. Add dad-002 and it just works.

Workflow (bed, lab, outcome, case-status):
  ONE real sqlite event store. Values come from recorded transitions
  (requested→acked→registered→verified). The goal endpoint already proves this
  pattern. "ack=false" must be a real un-acked row, not a frozen literal.

Trade-off (brain):
  derive options from the REAL state-diff + signals, not static A/B text.
```

## Effort — not a monster (~1–2 focused days + 1 redeploy)
```
🟢 retrieve / signals / classify   0   already real → just tag LIVE in UI
🟡 goal                            S   drop the seeded default; keep sqlite
🔴 state-diff + trajectory         M   generic differ + disclosed mom record
🔴 bed + lab + outcome + status    M   one shared sqlite event store + generic read
🔴 tradeoff                        S   compute from state-diff + signals
   Cloud Run redeploy              S   Dockerfile exists → gcloud run deploy
```

## Acceptance test (analyst-grade — the anti-theater proof)
```
Run Baymax on a SECOND patient (dad-002, COPD, different timeline).
  ✅ organs return real computed values OR honest available:false
  ❌ organs return mom's data, or crash, or go blank
"Swap the cell reference and the formula still works" = not theater.
```
