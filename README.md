# Baymax: Cross-Domain Evidence-to-Action Agent

Baymax is not impressive because it has more data. It is impressive when
another perspective changes what it decides to do.

```text
cheap NOSE
  -> patient eye: what does this case look like?
  -> drug-safety eye: what risk is invisible from the patient view?
  -> brain: compare the patient-only decision with the cross-domain decision
  -> brakes: act, or stop and require human review
  -> nerves + hands: hand off or change durable state
  -> immune: pin the decision-changing trajectory in CI
```

## The Stop-And-Read Proof

```text
Same case: abdominal pain after Ibuprofen

Patient eye only
  -> SOON
  -> discharge_plan

Add the drug-safety eye
  -> 16/17 exact-Ibuprofen openFDA reports marked serious
  -> population signal only; Baymax does NOT claim causality
  -> brake blocks autonomous discharge
  -> clinician-review nerve receives and ACKs the case
```

This is the point of the two eyes: cross-domain evidence can change action
policy without pretending the model knows more than the evidence supports.

## Audit In One Command

```bash
make sync
pip install -r requirements.txt
make test
make audit
```

The final receipt is `outputs/baymax_audit.json`. It contains three trajectories:

- attention skip: NOSE stops a routine case before expensive evidence work
- cross-domain brake: another perspective changes action into human review
- bounded action: durable state changes and the outcome is independently re-read

It also records exact source commits, organ grades, the solo-engineer A+ ceiling,
and the remaining shortest path.

## Organ Sources

| Organ | Public source | What this repo audits |
|---|---|---|
| NOSE | [healthcare-signal-platform](https://github.com/anix-lynch/healthcare-signal-platform) | Five-signal batch proof; 30% fewer LLM calls at 95.4% serious recall |
| Left eye | [healthcare-ai-data-engineer](https://github.com/anix-lynch/healthcare-ai-data-engineer) | Full 55,500-row synthetic encounter corpus and reconciliation |
| Right eye | [healthcare-da](https://github.com/anix-lynch/healthcare-da) + [healthcare-signal-platform](https://github.com/anix-lynch/healthcare-signal-platform) | Real openFDA evidence plus governed semantic-layer lineage |
| Brain + hands | [healthcare-genai-engineer](https://github.com/anix-lynch/healthcare-genai-engineer) | Triage, Bed Ops decision, durable action, ACK, and outcome verification |

## Honest Boundary

Baymax is a closed-loop ER **simulation**, not a deployed clinical system.
The action engine changes durable SQLite state representing a Bed Ops
disposition; it does not write to a hospital EHR or bed-management platform.

The per-case NOSE is deliberately cheap: a safety-term gate decides whether to
open both eyes. The five statistical/ML/retrieval signals are independently
batch-evaluated in the signal sibling and linked in the audit receipt; this repo
does not pretend all five models execute online for every patient query.

## Repo Map

```text
baymax/
├── baymax/audit.py             ✅ runs nose -> eyes -> brain -> hands -> verify
├── tests/test_audit.py         ✅ proves skip-path and full closed-loop path
├── scripts/sync_sources.sh     ✅ fetches the four public sibling sources
├── outputs/baymax_audit.json   🟡 three trajectories + dream-state audit
├── .github/workflows/audit.yml ✅ regenerates proof on every change
├── Makefile                    ✅ one-command audit entry points
├── SPEC.md                     📖 scope and proof boundary
└── README.md                   📖 recruiter audit map
```
