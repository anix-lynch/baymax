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

## Three Cases, One Movie

```text
CASE 1 · ATTENTION FLIP
routine medication refill
→ NOSE finds no cheap safety trigger
→ expensive eyes stay closed
→ no action attempted

CASE 2 · DECISION FLIP
same critical chest-pain patient
→ bed available: assign_bed
→ ER gridlock: divert
→ capacity perspective changes the action

CASE 3 · BRAKE SAVE
abdominal pain after Ibuprofen
→ patient-only: discharge_plan
→ drug eye: 16/17 exact-Ibuprofen reports marked serious
→ population signal only; no causality claim
→ brake blocks autonomous discharge
→ clinician-review nerve receives and ACKs the case
```

```bash
make sync
make demo
```

That is the recruiter path. Three cases show that Baymax allocates attention,
changes decisions when another perspective matters, and stops itself before an
unsafe autonomous action.

## Technical Audit

```bash
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
├── baymax/demo.py              ✅ plays the three memorable cases
├── baymax/audit.py             ✅ generates deep evidence receipts
├── cases/legendary_cases.json  ✅ the public three-case screenplay
├── tests/test_audit.py         ✅ pins every movie outcome in CI
├── scripts/sync_sources.sh     ✅ fetches the four public sibling sources
├── outputs/baymax_audit.json   🟡 three trajectories + dream-state audit
├── .github/workflows/audit.yml ✅ regenerates proof on every change
├── Makefile                    ✅ one-command audit entry points
├── SPEC.md                     📖 scope and proof boundary
└── README.md                   📖 recruiter audit map
```
