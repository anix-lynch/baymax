# Brain Audit

## Responsibility

The Brain determines how Baymax works: how it combines evidence, resolves
signals, selects decisions, applies safety policy, and converts knowledge into
recommendations or actions.

## Current Grade

**B+**

Baymax has strong task-specific procedural reasoning. It does not yet have a
formal reusable library for generalized evidence arbitration, tradeoff
reasoning, or alternative-action comparison.

## Existing Capabilities

### Safety-floor triage fusion

Deterministic safety rules override retrieval-driven predictions for
safety-critical cases. Rule/RAG disagreement is exposed rather than hidden.

### Prediction-aware operational reasoning

Acute triage cannot be downgraded by lower future-risk predictions. High
future-risk signals can increase monitoring within SOON and WAIT pathways.

### Deterministic Bed Ops decision tree

Baymax selects `assign_bed`, `board_ed`, `hold_observation`, `divert`, or
`discharge_plan` from triage, predicted length of stay, bed pressure, and
capacity state.

### Decision Safety Envelope

Before recommendation or action, the reusable gate selects:

- `ACT`
- `ASK_FOR_INFO`
- `HUMAN_REVIEW`
- `WAIT_FOR_ACK`
- `SUPPRESS`

### Bounded recovery and outcome reasoning

Action execution has bounded retries, stop conditions, escalation, idempotency,
and durable outcome verification.

## Missing Capabilities

- General arbitration between two trusted but conflicting evidence sources.
- Comparison of multiple reasonable actions with explicit tradeoffs.
- General policy for choosing reversible alternatives under uncertainty.
- A reusable protocol for identifying the exact missing information required
  before proceeding.
- Trusted derivation of evidence conflict and calibrated confidence.
- Counterfactual or second-pass verification of recommendations before they are
  presented.

## Contradictions

### Recommendation safety is evaluated after generation

`/v1/ask` retrieves and generates an answer before the Decision Safety Envelope
evaluates whether a direct recommendation is safe. Operational recommendations
are suppressed, but the answer already exists.

### Suppressed recommendation can still produce an executed-looking plan

After a non-`ACT` safety verdict, `/v1/ask` still builds the collaboration
graph. Bed Ops can appear with `executed=True` and a disposition even when the
safety decision is `ASK_FOR_INFO` or `SUPPRESS`.

### Trusted conflict and confidence are unavailable

The public action API can no longer assert confidence, conflict, risk,
reversibility, or ACK. Action risk and reversibility come from versioned
policy, and ACK comes from durable task state. However, the action loop does
not yet receive trusted cross-domain conflict or calibrated confidence facts.

## Evidence Map

| Capability | Evidence |
|---|---|
| Safety-floor fusion | `workflows/classify_esi.py` |
| Prediction overrides | `app/routers/ask.py::orchestration_override_rules` |
| Bed Ops decisions | `app/bed_ops_agent.py` |
| Decision Safety Envelope | `action_engine/safety.py` |
| Action loop | `action_engine/loop.py` |
| Decision correctness eval | `evaluation/agent_eval.py` |
| Safety-envelope acceptance | `tests/test_action_engine.py`, `tests/test_act.py`, `tests/test_ask.py` |

## Upgrade Path

1. Run the conduct/safety verdict before generation, planning, and action.
2. Derive risk, conflict, confidence, reversibility, and ACK from trusted
   runtime state.
3. Add an action-comparison protocol that records alternatives, tradeoffs, and
   why the selected action is safest.
4. Replace generic `ASK_FOR_INFO` with structured missing questions.
5. Add tests proving a non-`ACT` verdict cannot create an executed-looking plan.

## Revision History

### June 2026 - Initial canonical audit

Recorded task-specific procedural strengths, Decision Safety Envelope behavior,
and the absence of a generalized Brain Library.

### June 2026 - Safety-before-recommendation upgrade

Closed the recommendation-ordering contradiction. The `/v1/ask` safety verdict
now runs before grounded generation and collaboration planning. A non-`ACT`
verdict returns a deterministic withheld response, no operational
recommendations, and no executed-looking collaboration plan. Regression tests
prove the generator and planner are not called.

### June 2026 - Trusted safety derivation Phase 2A

Removed public action-request fields that allowed callers to self-certify
confidence, conflict, risk, reversibility, and ACK. The Brain now derives
action risk and reversibility from `action-safety.v1`, verifies ACK from
durable task state, and persists policy version plus source facts in every
safety receipt. Trusted conflict and calibrated confidence wiring remain open.
