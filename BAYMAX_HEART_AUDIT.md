# Heart Audit

## Responsibility

The Heart defines Baymax's relationship with humans: listening, care,
clarification, compassionate disagreement, respect, follow-through, and the
obligation not to abandon a case.

## Current Grade

**C+**

Baymax has protective instincts and routes cases toward follow-up, but it does
not yet maintain a durable care relationship or verify that a person received
help.

## Existing Capabilities

### Protective challenge

Baymax prevents lower-risk predictions from downgrading acute safety signals.

### Human-readable explanation

Responses expose decision basis, conflicts, override reasons, and operational
recommendations.

### Refusal rather than guessing

When retrieval returns no evidence, Baymax admits the limitation rather than
inventing an answer.

### Follow-up intent

Non-NOW or future-risk cases are routed into a Care Follow-up plan with bounded
retry and escalation descriptions.

## Missing Capabilities

- Patient consent and preference.
- Acknowledgement of distress or the human's stated goal.
- Structured clarification questions.
- Role-aware communication for patient, nurse, physician, and operator.
- Compassionate refusal language with a safe alternative.
- Durable follow-up execution, reminders, response state, reassessment, and
  closure.
- A verified definition of when care is complete.
- A mechanism for patients or clinicians to decline, correct, or appeal.

## Contradictions

### Care Follow-up is a plan, not care delivered

The planner says the follow-up agent keeps patients from disappearing, but no
durable worker proves contact, response, reassessment, escalation, or closure.

### Refusal is mechanically safe but emotionally thin

Baymax returns reason codes, warnings, and HTTP errors. These are useful for
machines but do not consistently explain what the human should do next.

### Protective behavior lacks consent boundaries

Baymax can choose and execute operational dispositions without a formal model
of patient consent, clinician authorization, or contested preference.

## Evidence Map

| Capability | Evidence |
|---|---|
| Safety-preserving challenge | `app/routers/ask.py::orchestration_override_rules` |
| Empty-evidence refusal | `generation/generate.py` |
| Care Follow-up plan | `app/agents.py` |
| Human explanations | `app/schemas.py::AskResponse`, `app/routers/vertex.py` |

## Upgrade Path

1. Add a durable Care Obligation record with owner, due time, status, and
   closure condition.
2. Implement the follow-up lifecycle:
   `followup_due -> outreach_requested -> acknowledged -> reassessed ->
   closed_safe | escalated | unable_to_verify`.
3. Add consent, preference, and role-aware communication fields.
4. Make every refusal provide reason, safe next step, and named owner.
5. Add tests proving Baymax does not claim care completion without closure.

## Revision History

### June 2026 - Initial canonical audit

Recorded protective behavior and the gap between follow-up intention and
verified care completion.
