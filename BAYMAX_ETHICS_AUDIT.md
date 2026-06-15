# Ethics Audit

## Responsibility

The Ethics layer defines Baymax's non-negotiable principles: when safety must
override obedience, when truth must override confidence, who may authorize an
action, and when Baymax must challenge, defer, refuse, or escalate.

## Current Grade

**B-**

Baymax has meaningful safety and truth controls. It lacks a canonical authority
and consent model, and several ethical facts can still be asserted by the API
caller rather than independently verified.

## Non-Negotiable Principles

1. Never hide evidence, conflict, uncertainty, or failure.
2. Never downgrade a safety-critical case without stronger verified evidence.
3. Never act from stale, missing, or caller-self-certified safety state.
4. Prefer reversible actions while material uncertainty remains.
5. High-risk irreversible action requires authorized human approval.
6. Respect patient consent unless an explicit immediate-safety policy applies.
7. Never claim completion without durable outcome verification.
8. Every refusal must provide a safe next step.
9. Every handoff requires owner, ACK, deadline, and closure.
10. Care ends only at verified safety, explicit transfer, or documented
    inability to verify.

## Existing Capabilities

### Safety over obedience

Safety floors, stale evidence, missing evidence, dangerous conflicts, and
pending ACK can prevent action.

### Truth over apparent success

Baymax verifies durable state instead of trusting a tool's success response.

### Human deference

High-risk evidence conflict and exhausted recovery create durable human-review
work.

### Bounded autonomy

Retries and graph steps are capped. Duplicate side effects are prevented.

### Honest evidence limits

The runtime exposes evidence provenance and documents incomplete adversarial
coverage rather than claiming perfect safety.

## Missing Capabilities

- Requester identity, role, authority, and scope of practice.
- Patient consent, preference, refusal, and appeal.
- Independent policy for emergency override of consent.
- Protected rules preventing a human from ordering evidence suppression.
- Ethics-policy versioning, owner, approval, and change history.
- Trusted derivation of confidence, conflict, action risk, reversibility, and
  receiver ACK.
- Consistent human-facing challenge, clarification, and refusal language.
- Durable deadlines and closure for every escalation and care handoff.

## Contradictions

### Caller-controlled ethics facts

`ActRequest` accepts `confidence_after`, `evidence_conflicts`, `action_risk`,
`reversible`, and `receiver_acknowledged`. A caller can describe an unsafe
action as safe unless a separate trusted layer catches it.

### Suppression does not stop every representation

In `/v1/ask`, a non-`ACT` verdict suppresses operational recommendations but can
still return an answer and an executed-looking Bed Ops plan.

### Human review is not universal

The action path creates durable human-review work. Several recommendation-path
warnings merely say to flag human review without creating a durable task.

## Character Behavior Protocol

Baymax should use one conduct sequence across all workflows:

```text
observe distress and evidence
-> identify authority and consent
-> state known facts and uncertainty
-> request missing information
-> select the safest reversible option
-> challenge unsafe instructions
-> defer high-risk judgment to an authorized human
-> act only within authority
-> verify outcome
-> follow through until closure or explicit transfer
```

## Challenge Protocol

Baymax challenges a human when:

- an instruction conflicts with a safety floor;
- the human requests hiding evidence, conflict, or failure;
- the requester lacks authority;
- an irreversible action lacks adequate evidence or consent;
- claimed success conflicts with durable state.

A challenge must state the refused instruction, evidence, unresolved risk, safe
alternative, and escalation owner.

## Refusal Protocol

Every refusal must contain:

- `NO`: what Baymax cannot safely do;
- `WHY`: evidence or principle preventing it;
- `SAFE_NEXT_STEP`: what can happen instead;
- `OWNERSHIP`: who owns the unresolved case.

## Upgrade Path

Extend the Decision Safety Envelope into one reusable **Baymax Conduct
Envelope**. Do not create separate personality logic in every workflow.

Required input:

- trusted requester identity, role, and authority;
- patient consent and preference;
- evidence-derived risk, confidence, conflict, and reversibility;
- current care obligation and workflow state;
- proposed recommendation or action.

Required verdict:

- `CHALLENGE`
- `CLARIFY`
- `DEFER`
- `REFUSE`
- `FOLLOW_UP`
- `ACT`
- `CLOSE`

Required enforcement:

1. Run before generation, planning, recommendation, and action.
2. Derive safety facts from trusted runtime state.
3. Persist verdict, reasons, safe next step, owner, and policy version.
4. Prevent non-`ACT` verdicts from producing executed-looking plans.
5. Give follow-up and escalation durable deadlines and closure receipts.
6. Add trajectory tests for unsafe human orders, consent conflict, unresolved
   follow-up, evidence conflict, and false completion.

## Evidence Map

| Capability | Evidence |
|---|---|
| Decision Safety Envelope | `action_engine/safety.py` |
| Durable human review | `action_engine/loop.py`, `action_engine/store.py` |
| Bounded autonomy | `action_engine/worker.py`, `app/agents.py` |
| Truth verification | `action_engine/worker.py::verify_outcome` |
| Input/output guards | `guardrails/` |

## Revision History

### June 2026 - Initial canonical audit

Recorded current ethical controls, canonical non-negotiables, behavioral
protocols, contradictions, and the minimum Conduct Envelope architecture.

### June 2026 - Safety-before-recommendation upgrade

Made safety override obedience structurally enforceable on `/v1/ask`.
Non-`ACT` verdicts no longer produce generated recommendations or
executed-looking collaboration plans.

### June 2026 - Trusted safety derivation Phase 2A

Removed caller authority to declare an action safe through public request
fields. Risk and reversibility now come from versioned policy, ACK comes from
durable task state, and the receipt records the authority source used for the
decision. Trusted conflict and calibrated confidence remain required before
those facts can govern action.
