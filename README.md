# Baymax ER Nurse Assistant

One recruiter-auditable integration spine over four public healthcare AI repos.

```text
cheap NOSE
  -> left eye: 55,500 synthetic ER encounters
  -> right eye: 5,000 real openFDA adverse-event reports
  -> brain: NOW / SOON / WAIT + Bed Ops disposition
  -> hands: durable state change + receiver ACK
  -> outcome check: re-read state; never trust "action succeeded"
```

## Audit In One Command

```bash
make sync
pip install -r requirements.txt
make test
make audit
```

The final receipt is `outputs/baymax_audit.json`. It records:

- exact source commit and artifact for every organ
- whether NOSE ran before the expensive eyes
- patient and openFDA corpus counts
- evidence hits from both eyes
- triage and Bed Ops decision
- receiver ACK
- durable before/after state
- independently re-read outcome

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
├── outputs/baymax_audit.json   🟡 machine-readable end-to-end receipt
├── .github/workflows/audit.yml ✅ regenerates proof on every change
├── Makefile                    ✅ one-command audit entry points
├── SPEC.md                     📖 scope and proof boundary
└── README.md                   📖 recruiter audit map
```
