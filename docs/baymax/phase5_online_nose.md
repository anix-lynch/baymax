# Phase 5 — Online Nose Wiring (scaffold + Cursor handover)

Status: ACTIVE. Expected maturity gain: +3. This is the highest-leverage move
because the honesty ledger pins NOSE as the weakest load-bearing organ, and the
headline verdict ships at the weakest leaf. Lifting NOSE lifts the headline.

## The exact gap

```
TODAY  nose_route() decides routing by KEYWORD MEMBERSHIP
       high_hits/moderate_hits in HIGH_RISK_TERMS / MODERATE_TERMS
       (batch five-signal proof is LINKED in the receipt, but not the decider)

GOAL   nose_route() decides routing from a SERVED, EVALUATED signal contract
       keyword set demoted to a safety FLOOR only (never the primary decider)
```

Honesty-ledger truth this closes (baymax/audit.py `ORGAN_LANE["nose"]["hedge"]`):
> "per-case routing is a keyword safety gate; the evaluated ranker is
> batch-only, not served online"

## Code anchors (where the work lands)

```
baymax/audit.py
  L25-29   HIGH_RISK_TERMS / MODERATE_TERMS   → demote to safety floor
  L129     nose_route(query)                  → rewire decider
  L139-151 high_hits/moderate_hits/routed     → replace primary logic
  L41-47   ORGAN_LANE["nose"] claim/hedge     → update once served
  L~497    _organ_live_gate() nose gate       → tighten (see below)
  L436-444 run_case() flow=["nose"]           → carry signal_version

sources/healthcare-signal-platform/openfda_signals/...
  router_ablation.operating_point            → the served contract's source
  (already read at L132-158: batch_llm_call_reduction_pct, batch_serious_recall)
```

## Served signal contract (define this)

A single evaluated routing output per case. Keep it a thin local served
module — do NOT open an ML side quest (SPEC "Stop Doing": no separate ML
campaign, no cloud, no model training).

```python
# baymax/served_nose.py  (NEW — thin server over the committed batch artifact)
def route_signal(query: str) -> dict:
    return {
        "route_to_eyes": bool,        # the decision, from the served ranker
        "signal_version": str,        # e.g. "signal-platform@<commit>:router_ablation.v1"
        "route_reason": str,          # human-readable why (top signal + score)
        "score": float,               # ranker score
        "serious_recall_floor": float,# operating-point recall this version guarantees
        "decided_by": "served_signal",# vs "safety_floor" fallback
    }
```

`nose_route()` then becomes: call `route_signal()`; if it abstains/errors, fall
back to the keyword floor and tag `decided_by="safety_floor"`. The receipt must
always carry `signal_version` + `route_reason`.

## Acceptance gates (SPEC Phase 5 — all must pass)

```
[ ] Route decision is produced by the served signal contract
      → assert nose receipt decided_by == "served_signal" on routed cases
[ ] Attention Flip receipt identifies the signal version
      → assert receipt["signal_version"] is non-empty and version-shaped
[ ] Serious-case recall floor remains protected
      → regression test: served version's serious_recall_floor >= 0.954
        (the committed batch operating point) — fail CI if it drops
[ ] Expensive-call reduction is measured, not asserted
      → record routed-vs-skipped counts; compare LLM-call reduction
        against serious recall on the labelled set
```

## Honesty-ledger updates (do these so the headline actually lifts)

```
baymax/audit.py  _organ_live_gate()  nose gate — tighten to:
    gates["nose"] = (
        traj["attention_skip"]["flow"] == ["nose"]
        and traj["attention_skip"]["nose"]["decided_by"] == "served_signal"
        and bool(traj["attention_skip"]["nose"]["signal_version"])
    )

ORGAN_LANE["nose"]:
    claim_allowed → "routes each case from a served, version-pinned evaluated
                     signal before opening expensive eyes"
    hedge         → "signal is served from a committed batch operating point,
                     re-evaluated per release, not retrained online"
```

When the nose gate passes with a served signal AND the dream-state grade for
nose rises to A-/A, `honesty_ledger.headline_verdict` flips 🟡 → ✅ and
`weakest_load_bearing_organ` moves off nose. That is the recruiter payoff.

## CI / scorecard close-out (Phase Completion Protocol)

```
cd ../healthcare-genai-engineer && pytest -q && make action-eval   # if L2 touched
cd ../baymax && make test && make audit                            # always
```
Then bump SPEC.md scorecard row "A/B/C live wiring 6/15 → ~9/15", set Phase 5
status COMPLETE, and update the handover task file's last-verified commit.

## Copy-paste Cursor prompt

```
Read ~/dev/baymax/SPEC.md then ~/dev/baymax/docs/baymax/phase5_online_nose.md.
Execute Phase 5 — Online Nose wiring — only. Do not start other phases.

1. Add baymax/served_nose.py: route_signal(query) -> the served signal
   contract in the scaffold. Source its decision + serious_recall_floor from
   sources/healthcare-signal-platform/openfda_signals router_ablation operating
   point (already read in audit.py L132-158). No training, no cloud, no new repo.
2. Rewire baymax/audit.py nose_route() (L129) to decide from route_signal();
   demote HIGH_RISK_TERMS/MODERATE_TERMS to a safety FLOOR fallback only.
   Always carry signal_version + route_reason + decided_by in the receipt.
3. Tighten _organ_live_gate() nose gate and update ORGAN_LANE["nose"] exactly
   as in the scaffold's "Honesty-ledger updates" section.
4. Add tests in tests/test_audit.py for all four acceptance gates, incl. the
   serious_recall_floor >= 0.954 regression.
5. Run: make test PYTHON=/opt/homebrew/bin/python3 && make audit PYTHON=...
   Confirm honesty_ledger.headline_verdict flips 🟡 -> ✅ (or document why not).
6. Commit on baymax only. Do NOT push (SPEC: no public push until final review).

Honest boundary (SPEC): closed-loop ER simulation, served from a committed
batch operating point re-evaluated per release — never claim online retraining,
hospital adoption, or causality.
```

## Boundary reminders (SPEC "Stop Doing")

- No new repo, no ML resume campaign, no dashboard/cloud/model that doesn't
  change attention/decision/safety/cost/trust/outcome.
- Budget for the later thin deployment-readiness merge is 5% — never the active
  phase while this L2 gap remains.
