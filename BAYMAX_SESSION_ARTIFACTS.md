# Baymax Session Artifacts

This is the root inventory for the Baymax architecture, safety, and positioning work completed in June 2026.

Open this file first when auditing Baymax in Cursor or on the Intel twin.

For active implementation work, start from `SPEC.md`. It is the single
Northstar control plane and names the current phase, wiring, acceptance tests,
and stop-doing rules.

## Source Ownership

- `/Users/anixlynch/dev/healthcare-genai-engineer` is the canonical L2 runtime repository.
- `sources/healthcare-genai-engineer/` is the ignored local sibling clone used by the live demo.
- `evidence/l2-decision-safety/` is the curated, recruiter-visible copy of this session's L2 safety upgrade.
- `docs/baymax/constitution/` contains canonical architecture health records. Future audits append evidence; they do not replace prior findings with summaries.

## Open First

| Artifact | Purpose |
|---|---|
| `BAYMAX_CONSTITUTION_V1.md` | Root-visible copy of the canonical organ registry and audit rules |
| `BAYMAX_BRAIN_AUDIT.md` | Root-visible procedural reasoning diagnosis |
| `BAYMAX_NERVES_AUDIT.md` | Root-visible runtime state-awareness diagnosis |
| `BAYMAX_IMMUNE_AUDIT.md` | Root-visible self-verification and Decision Safety Envelope evidence |
| `BAYMAX_HEART_AUDIT.md` | Root-visible human relationship and care obligations |
| `BAYMAX_ETHICS_AUDIT.md` | Root-visible authority, consent, truth, and refusal controls |
| `BAYMAX_L2_FINAL_POSITIONING.md` | 2026 Applied AI / Agent Engineer positioning |
| `FINISH_SHOWROOM.md` | Showroom completion handover |
| `docs/baymax/constitution/brain_audit.md` | Procedural reasoning diagnosis |
| `docs/baymax/constitution/nerves_audit.md` | Runtime state-awareness diagnosis |
| `docs/baymax/constitution/immune_audit.md` | Self-verification and Decision Safety Envelope evidence |
| `docs/baymax/constitution/heart_audit.md` | Human relationship and care obligations |
| `docs/baymax/constitution/ethics_audit.md` | Authority, consent, truth, and refusal controls |

## Decision Safety Envelope

These files are copied from the canonical L2 repo so a recruiter can audit the complete safety upgrade from this single Baymax repo.

### Runtime

- `evidence/l2-decision-safety/action_engine/safety.py`
- `evidence/l2-decision-safety/action_engine/loop.py`
- `evidence/l2-decision-safety/action_engine/store.py`
- `evidence/l2-decision-safety/app/routers/act.py`
- `evidence/l2-decision-safety/app/routers/ask.py`
- `evidence/l2-decision-safety/app/schemas.py`

### Evaluation And Tests

- `evidence/l2-decision-safety/evaluation/action_eval.py`
- `evidence/l2-decision-safety/tests/test_act.py`
- `evidence/l2-decision-safety/tests/test_action_engine.py`
- `evidence/l2-decision-safety/tests/test_ask.py`
- `evidence/l2-decision-safety/outputs/action_eval_summary.json`

### Audit-Referenced Python Proof

Every Python file cited by the canonical organ audits is included in `evidence/l2-decision-safety/`.

- `evidence/l2-decision-safety/README.md` explains ownership and verification.
- `evidence/l2-decision-safety/SHA256SUMS` records file integrity.

## Positioning Copy

The Notion copy of `BAYMAX_L2_FINAL_POSITIONING.md` is:

https://app.notion.com/p/BAYMAX_L2_FINAL_POSITIONING-380ae09b6cbd81f9b558e8348ed65252

## Legacy Record

The original pre-constitution brain diagnosis remains available for history:

- `docs/baymax/legacy/Baymax_brain_diagnosis_pre_constitution.md`

## Visibility Check

From the Baymax root:

```bash
test -r BAYMAX_SESSION_ARTIFACTS.md
test -r BAYMAX_CONSTITUTION_V1.md
test -r BAYMAX_BRAIN_AUDIT.md
test -r BAYMAX_NERVES_AUDIT.md
test -r BAYMAX_IMMUNE_AUDIT.md
test -r BAYMAX_HEART_AUDIT.md
test -r BAYMAX_ETHICS_AUDIT.md
test -r BAYMAX_L2_FINAL_POSITIONING.md
test -r evidence/l2-decision-safety/action_engine/safety.py
make test
```
