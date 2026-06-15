# Immune Audit

## Responsibility

The Immune system tells Baymax when not to trust itself, its evidence, its
tools, or its apparent success.

## Current Grade

**B overall**

- Post-action verification: **A**
- Grounding and hallucination controls: **B**
- Uncertainty and conflict handling: **C+**
- Freshness defense: **A- after Decision Safety Envelope**

Baymax is strongest after action: it verifies reality instead of trusting the
tool. Before action, it now rejects caller safety self-certification and
records where each safety fact came from.

## Existing Capabilities

### Fail-closed evidence intake

Malformed or incompatible evidence is blocked before the decision engine.

### Retrieval before grounded generation

Answers use retrieved evidence. Empty retrieval returns a refusal rather than a
guess.

### Citation and output guards

Hallucinated citation IDs are removed. Short or forbidden autonomous-action
outputs can be blocked.

### Evidence conflict detection

Safety-floor/RAG disagreement and prediction/triage conflict are surfaced.

### Decision Safety Envelope

Baymax suppresses stale capacity decisions, asks for missing information,
requires human review for dangerous conflicts, and waits for receiver ACK.

### Durable outcome verification

Baymax re-reads durable state and can detect a tool that reported success
without changing reality.

## Missing Capabilities

- General cross-domain conflict detection.
- Confidence calibration against observed correctness.
- Calibrated confidence derived from observed model/evidence performance.
- Generalized cross-domain conflict rules beyond operational capacity.
- Claim-level citation enforcement for every generated statement.
- Self-critique or alternative-reasoning check before recommendation.
- Runtime memory of prior failure patterns.
- A protocol that names exact additional information required.

## Contradictions

### Self-doubt is honest but incomplete

Baymax records trusted risk, reversibility, ACK, operational conflict, and
evidence sufficiency facts. Operational contradictions can now stop a
high-risk action. The remaining confidence gap is calibration against labelled
correctness, not caller control.

### Unsupported claims can still pass

Explicit fake citation IDs are detected, but an answer containing unsupported
claims without citation IDs may pass the output validator.

### Prompt-injection defense is knowingly incomplete

The regex baseline catches known literal patterns but misses paraphrased
attacks. The repo documents this honestly; it must not be described as complete
prompt-injection defense.

## Evidence Map

| Capability | Evidence |
|---|---|
| Fail-closed intake | `action_engine/contract.py`, `action_engine/loop.py` |
| Empty-retrieval refusal | `generation/generate.py` |
| Output validation | `guardrails/output_validator.py` |
| Safety envelope | `action_engine/safety.py` |
| False-success detection | `action_engine/worker.py::verify_outcome` |
| Adversarial evidence | `evaluation/adversarial_eval.py`, `docs/operational_story.md` |

## Upgrade Path

1. Move all safety facts behind trusted derivation adapters.
2. Require claim-level support before returning generated answers.
3. Add generalized contradiction records with source, severity, and resolution.
4. Add calibrated confidence thresholds and regression tests.
5. Add pre-recommendation self-verification for high-risk decisions.

## Revision History

### June 2026 - Initial canonical audit

Recorded strong post-action skepticism and weak pre-action self-doubt.

### June 2026 - Decision Safety Envelope upgrade

Closed the stale/default-1970 capacity gap and added durable reason-coded
suppression, clarification, human review, and ACK waiting.

### June 2026 - Safety-before-recommendation upgrade

Moved the safety decision ahead of recommendation generation and action
planning. Stale or low-confidence evidence now stops the expensive generator
and planner rather than generating first and suppressing afterward.

### June 2026 - Trusted safety derivation Phase 2A

Removed the public API's ability to self-certify safety. Versioned action
policy now supplies risk and reversibility, durable task state supplies ACK,
and safety receipts persist policy version plus derived-fact provenance.
Regression tests reject attempts to submit the removed safety fields.

### June 2026 - Trusted operational conflict Phase 2B

Versioned capacity-consistency rules now derive conflict from canonical
evidence. A contradictory low-pressure/saturated-capacity case selects
`divert`, then the Immune gate changes the outcome to `HUMAN_REVIEW` before
durable state changes. Missing capacity fields derive low evidence sufficiency
and return `ASK_FOR_INFO`.
