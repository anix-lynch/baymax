# Baymax Capability Ladder

> This is the single master capability file for Baymax.
> It defines how Baymax evolves from a retrieval assistant into a deployable healthcare workflow agent.

Baymax is not being designed as a generic chatbot. Baymax is being designed as a **stateful, safety-bounded, healthcare workflow agent**.

The ladder below answers one question:

**What can Baymax understand, prepare, do, and verify at each stage of maturity?**

Enforcement detail lives in companion files (referenced, not restated): `HARNESS_SPEC.md` (how policies are enforced in software) and `AUTHORITY_SPEC.md` (the 3-zone action policy). This file is the master mental model.

---

## Core progression

Baymax grows through this sequence:

**Know → Understand → Weigh → Anticipate → Prepare → Act → Verify**

This sequence is more important than belt color. Belt color is just a storytelling layer on top.

---

## Level 1 — Retrieval-aware

Baymax can find relevant information.

**What this means**
- Retrieve relevant history, labs, medications, prior episodes, and prior notes.
- Retrieve guidelines, reference protocols, and related evidence.
- Ground answers in evidence instead of guessing.

**What Baymax can do here**
- Answer: "What is in the chart?"
- Pull the prior successful case.
- Surface relevant diagnoses like CKD, CHF, diabetes, and prior fluid overload.

**Limitation:** Baymax can find things, but it does not yet understand whether old evidence still applies today.

---

## Level 2 — State-aware

Baymax can understand the current situation, not just the retrieved facts.

**What this means**
- Compare current state with prior state.
- Recognize that the same patient may now be in a different condition.
- Integrate multiple simultaneously true signals into a single situation model.

**What Baymax can do here**
- Detect that the patient was CKD Stage 2 before and is now CKD Stage 3.
- Notice that previous success may no longer transfer safely.
- Say: "I found the old successful treatment, but today's state is different."

**Limitation:** Baymax can detect differences, but it does not yet fully reason through downstream consequences.

---

## Level 3 — Trade-off-aware

Baymax can weigh competing truths and reason across consequences.

**What this means**
- Multiple evidences may all be true at once.
- Baymax must decide what matters more for this decision.
- Baymax can reason in terms of benefits, costs, risks, and reversibility.

**What Baymax can do here**
- Compare stronger diuresis for faster symptom relief versus a more conservative approach to reduce renal risk.
- Explain why one option is safer even if another is more immediately effective.
- Handle heart–kidney tension instead of reasoning about only one organ.

**Limitation:** Baymax can evaluate options, but it still reacts mostly to the present question.

---

## Level 4 — Anticipation-aware

Baymax can infer what will matter next before the user asks.

**What this means**
- Infer the next useful questions.
- Anticipate which specialist, workflow, family burden, or follow-up issue will likely become important.
- Shift from "answering the complaint" to "understanding the next needs."

**What Baymax can do here**
Instead of stopping at "possible causes include CHF, CKD, and diabetes," Baymax continues with: "Is this worse than the last admission? Is nephrology already involved? Who will help manage medications at home? Should follow-up be arranged before discharge?"

**Limitation:** Baymax can see ahead, but it has not reduced the user's workload unless it prepares something concrete.

---

## Level 5 — Preparation-aware

Baymax can prepare the next safe moves before being told exactly what to do.

**What this means**
- Turn anticipation into drafts, options, summaries, and coordination artifacts.
- Reduce cognitive load and logistical friction.
- Do the boring-but-useful work automatically when risk is low.

**What Baymax can do here**
- Draft a nephrology referral summary.
- Check whether specialist follow-up is already scheduled.
- Find candidate follow-up slots.
- Draft plain-language explanations for the family.
- Surface missing workflow items (unresolved referrals, no follow-up).

**Boring tray:** this is Baymax's boring-tray layer — summarize, organize, draft, prepare, monitor, tee up the next step. Safe because it does not change treatment or create irreversible commitments.

**Limitation:** Baymax can prepare, but it must respect authority boundaries before execution.

---

## Level 6 — Action-aware

Baymax can execute bounded workflow actions inside its lane.

**What this means**
- No longer just a reasoning layer — it can act using tools and workflow integrations, within clear authority boundaries.

**What Baymax can do here**
- Auto-perform low-risk actions: summarize, monitor, update internal task state, prepare reminders.
- Propose then execute approval-gated actions: send a referral, book a follow-up slot, notify the family, share a summary with a clinician.

**Authority model (3 zones):** Auto-safe (do directly) · Approval-gated (prepare, execute on confirmation) · Forbidden (never). Baymax is a care coordinator and workflow agent, not an autonomous clinician.

**Limitation:** a submitted request is not the same as a completed care loop.

---

## Level 7 — Outcome-aware

Baymax can verify whether actions actually resulted in real-world progress.

**What this means**
- Tool success is not enough. Task completion is not enough. Baymax must check whether the intended real-world outcome happened.

**What Baymax can do here**
- Distinguish drafted → submitted → accepted → scheduled → completed → verified.
- Notice that "referral sent" does not mean "appointment happened."
- Detect unresolved care gaps and continue follow-through.

**Example:** bad agent says "Referral sent, done." Outcome-aware Baymax says "Referral submitted, but not yet accepted; appointment created, but patient not yet informed; care loop still open."

---

## Level 8 — Longitudinal / Trajectory-aware

Baymax can reason across time, not just across one episode.

**What this means**
- Sees the patient as a trajectory, not a snapshot.
- Reasons over recurrence, decline, adherence, follow-up reliability, cumulative burden.
- Says not just "what is happening" but "how this pattern is evolving."

**What Baymax can do here**
- Detect that this is the third edema-related episode in eight months.
- Recognize care is failing from continuity breakdown, not only physiology.
- Surface trajectory risks: worsening kidney reserve, repeated admissions, rising home-management burden, likely follow-up failure.

**Why this matters:** this is where Baymax stops feeling like a search agent and starts feeling like a trusted care companion.

---

## Belt mapping (storytelling layer)

Belt color is a presentation layer, not the core spec. The clean canonical mapping:

- White — Retrieval-aware
- Yellow — State-aware
- Green — Trade-off-aware
- Blue — Anticipation-aware
- Brown — Preparation + bounded Action-aware
- Black — Outcome-aware + Longitudinal-aware

> Demo-set note: the current HTML theaters use a finer 7-belt skin (White · Yellow · Orange · Green · Blue · Brown · Black) where **Orange** dramatizes Workflow/Preparation (booking hands + ACK) and **Blue** dramatizes Objective + Anticipation (real goal + next needs). Belts are storytelling only — the 8 levels above are the truth.

---

## Swollen legs example across the ladder

- **Retrieval:** "I found prior CHF, CKD, diabetes, and a previous successful treatment."
- **State:** "That success happened when kidney function was better than today."
- **Trade-off:** "A stronger diuretic may reduce swelling faster but may worsen kidney function."
- **Anticipation:** "The next useful questions are whether nephrology is involved, whether this is worse than last time, and who manages meds after discharge."
- **Preparation:** "I drafted the nephrology summary, checked for follow-up gaps, and found three appointment windows."
- **Action:** "With approval, I can submit the referral and book the follow-up."
- **Outcome:** "The referral was sent, but the appointment has not yet been confirmed."
- **Longitudinal:** "This is part of a repeated pattern of fluid overload and deteriorating kidney reserve, not a one-off event."

---

## Build order for a solo engineer

1. Retrieval → 2. State → 3. Trade-off → 4. Anticipation → 5. Preparation → 6. Action → 7. Outcome → 8. Longitudinal.

Realistic for a solo builder in 2026 — moves from reasoning quality to operational usefulness without new model training.

## What matters most for hiring

The strongest signals are not raw retrieval. They are: Baymax knows when prior success no longer applies; reasons about trade-offs instead of pretending there's one obvious answer; anticipates what matters next; prepares real workflow artifacts; acts within authority; and verifies outcomes instead of trusting tool calls blindly. That is what makes Baymax look like an applied agent system rather than a medical RAG demo.

## One-line summary

Baymax evolves from **finding evidence** to **understanding the current state**, to **reasoning about consequences**, to **anticipating future needs**, to **preparing and executing bounded actions**, and finally to **verifying real-world outcomes across time**.
