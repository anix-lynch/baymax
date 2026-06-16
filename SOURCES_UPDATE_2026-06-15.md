# Sources Update — ลิ้น A + จมูก signal อัปเป็น senior (2026-06-15)
> For Codex (Baymax owner). The L1/L1.5 source organs Baymax reads got upgraded to S-tier.
> NO Baymax code was touched. Contracts unchanged — no breaking change to the L2 plug.

## healthcare-da — the "ลิ้น/tongue" (analytics source) · PUSHED to GitHub (HEAD 8204314)
`baymax/sources/healthcare-da` is now synced to this HEAD.
- **Live contract gate** (`pipeline/run_contract_gate.py`): validate → quarantine → anomaly → log,
  code-generated proof, exits non-zero on FAIL. Bad data can't reach silver/gold/the model.
- **Vertex serve-preflight** (`pipeline/vertex_preflight.py`): reuses the SAME contract on the serve
  side — a Vertex/LLM consumer refuses to serve contract-failing data.
- **AI-ready semantic layer**: 9 governed measures + descriptions + synonyms (NL/LLM Q&A);
  measured **3.8× fewer query tokens** vs raw SQL.
- **Governance as code**: RBAC roles + RLS in `model.bim` + retention/classification.
- CI: gate → preflight → bench → governance → tests + daily cron. 10 tests pass.
→ **Baymax's SignalSource/agent now reads cleaner, governed, contract-gated data.**

## healthcare-signal-platform — the "จมูก/nose" (signal source) · LOCAL commit 64bf852 (push pending its own simplicity-review)
- **NEW** `openfda_signals/feedback.py`: human-in-the-loop loop — uncertain signals route to a human
  review queue → verdicts → agreement + threshold feedback. Closes the loop the model can't.
- `signal_source.py` / `signal_contract_v1` UNCHANGED — the L2 prefilter plug is stable.

## Action for Codex
- `sources/healthcare-da` already reset to GitHub HEAD 8204314 — nothing to do.
- signal-platform `feedback.py` is local-only until its own simplicity-review + push.
- No contract change → Baymax integration needs no edit; the organs are just better now.
