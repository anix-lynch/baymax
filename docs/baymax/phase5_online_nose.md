# Phase 5 — Online Nose Wiring

Status: COMPLETE. Earned maturity gain: +3. This was the highest-leverage move
because the honesty ledger pins NOSE as the weakest load-bearing organ, and the
headline verdict ships at the weakest leaf. Lifting NOSE lifts the headline.

## The exact gap

```
BEFORE nose_route() decided routing by local keyword membership while the
       five-signal openFDA proof was only linked in the receipt.

NOW    nose_route() consumes a versioned served ESI attention contract before
       either eye opens. It is evaluated on 497 labelled synthetic patient
       cases and fails safe to the local safety floor if loading fails.
```

## Implementation

```
baymax/served_nose.py
  route_signal(query)              served per-case decision + version receipt
  evaluate_signal_contract()       labelled patient routing evaluation

baymax/audit.py
  nose_route(query)                consumes served signal before both eyes
  _organ_live_gate()               requires version + >=95% serious recall
  safety-floor fallback            fails safe without claiming served proof
```

## Served signal contract

A single evaluated routing output per case. The patient router and openFDA
five-signal router are deliberately reported as separate domain proofs.

```python
# baymax/served_nose.py
def route_signal(query: str) -> dict:
    return {
        "route_to_eyes": bool,        # deterministic ESI attention decision
        "signal_version": str,        # version + source commit
        "route_reason": str,          # human-readable why (top signal + score)
        "priority_score": float,      # deterministic urgency score, not probability
        "evaluation": dict,           # labelled patient routing metrics
        "decided_by": "served_signal",# vs "safety_floor" fallback
    }
```

Measured patient-case operating point:

```text
497 labelled synthetic patient cases
route ESI <= 3 before expensive eyes
serious-case recall: 95.39%
expensive-path reduction: 4.83%
```

The sibling C/openFDA signal platform separately proves 30% call reduction at
95.4% serious-report recall on 5,000 real FAERS reports. That number is not
claimed for patient-case routing, and C is not presented as the served patient
router.

## Acceptance gates (SPEC Phase 5 — all must pass)

```
[x] Route decision is produced by the served signal contract
      → assert nose receipt decided_by == "served_signal" on routed cases
[x] Attention Flip receipt identifies the signal version
      → assert receipt["signal_version"] is non-empty and version-shaped
[x] Serious-case recall floor remains protected
      → regression test: patient-case serious recall >= 0.95
[x] Expensive-call reduction is measured, not asserted
      → record routed-vs-skipped counts; compare LLM-call reduction
        against serious recall on the labelled set
```

The Nose now earns A- and no longer caps the headline. Its hedge explicitly
states that it is deterministic, evaluated on synthetic patient cases, and
separate from the openFDA batch router.

## Verification

```
Baymax: 9 tests passed; audit live gate passed
L2: 89 tests passed; action eval and 50-scenario agent eval passed
```

## Boundary reminders (SPEC "Stop Doing")

- No new repo, no ML resume campaign, no dashboard/cloud/model that doesn't
  change attention/decision/safety/cost/trust/outcome.
- Budget for the later thin deployment-readiness merge is 5% — never the active
  phase while this L2 gap remains.
