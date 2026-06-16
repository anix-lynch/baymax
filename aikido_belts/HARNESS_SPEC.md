# Baymax Harness Spec v2

> **Agent = Model + Harness.**
> The harness is every part of Baymax that is **not** the model itself: loops, tools, sandbox, memory, constraints, logging, and evals.

Baymax's harness is responsible for:

- limiting **what Baymax can see**,
- limiting **what Baymax can do**,
- controlling **where Baymax can execute**,
- and enforcing **how Baymax should behave across time**.

The goal is to make Baymax deployable in regulated environments, even before it is integrated with a real hospital.

> 💡 Why this matters: a May 2026 study of Claude Code's source found ~98.4% of a production agent is harness infrastructure (permissions, context, sandbox, tool routing, recovery) and only ~1.6% is AI decision logic. The harness is the product, not the wrapper.

Companion specs: `AUTHORITY_SPEC.md` (policy: what is allowed) · `CAPABILITY_LADDER.md` (reasoning levels) · `BELT_PROGRESSION.md` (narrative).

---

## 1. Data Harness — What Baymax Can See

Baymax never talks directly to a raw production EMR or entire hospital database. The data harness defines a **scoped, curated view** of the world for each patient and task.

### Data scope

For a given patient and session, Baymax can see:

- Curated patient summary for **this patient only**.
- Relevant visits and admissions for the current problem space.
- Labs and imaging strictly required for the task (e.g., renal function, prior CHF episodes).
- Consult state: whether cardiology, nephrology, or other specialists are involved.
- Workflow markers: scheduled visits, pending referrals, resolved vs unresolved tasks.

Baymax must **not** see:

- Raw hospital-wide databases.
- Charts of other patients.
- Fields not relevant to the current task or consented scope.

### Representation

The harness controls representation, not just access:

- Clinical state that must be precise is exposed as **structured JSON** (e.g., CKD stage, eGFR trend, admission counts).
- Narrative context, notes, and explanations are exposed as **summaries or excerpts**, not unbounded free-text dumps.

This supports both good reasoning (clean structure) and safety (less junk, fewer injection surfaces).

---

## 2. Tool Harness — What Baymax Can Do

The harness defines which tools Baymax is allowed to call. Tools are grouped into three authority levels, consistent with `AUTHORITY_SPEC.md`:

1. Auto-safe tools (boring tray)
2. Approval-gated tools
3. Forbidden tools (not registered, or blocked at the harness level)

### Auto-safe tools (boring tray)

```text
summarize_case()            list_specialists_involved()
detect_recurrent_patterns() suggest_next_questions()
translate_jargon()          draft_referral_note()        (draft only)
draft_discharge_checklist() prepare_followup_options()
monitor_status()            (e.g., no nephro follow-up in 14 days)
```

Baymax may call these without user approval. They do not modify external systems or change clinical state.

### Approval-gated tools

```text
send_referral()             book_followup_slot()
send_reminder_to_family()   (if opt-in)
share_summary_with_clinician()
submit_prefilled_lab_order() (routine labs allowed by policy)
```

The harness enforces that these tools are **never called without an approval token**, and the UI/system must explicitly collect confirmation before passing that token to the harness.

### Forbidden tools

Actions such as changing medications/dosages, deciding admit/discharge, cancelling critical labs or scans, or committing billing/insurance guarantees are **not implemented as callable tools**, or are hard-blocked behind non-bypassable policy checks. The model cannot "talk its way into" them because there is no callable interface from the harness.

---

## 3. Sandbox Harness — Where Baymax Runs

To execute tools and potential code safely, Baymax runs inside a sandboxed environment.

### Filesystem
- Read/write is limited to a dedicated workspace for the current agent session.
- Baymax cannot access host system files, credentials, or other patients' workspaces.
- Any persistent storage must be explicitly designed and audited.

### Network
- Outbound network access is restricted to an allowlist: hospital APIs (mock or real), insurer APIs (mock or real), MCP tool servers or equivalent.
- No arbitrary internet access by default.

### Compute
- Code execution (if any) runs inside isolated containers or VMs.
- If generated code fails or misbehaves, the container is torn down; the host remains unaffected.

The sandbox harness protects both the hospital from Baymax, and Baymax from hostile or malformed environments.

---

## 4. Policy Harness — How Baymax Behaves Over Time

Beyond data, tools, and sandbox, the harness defines Baymax's **behavioral loop**:

> **ANTICIPATE → PREPARE → ACT → VERIFY**

### Anticipate (read-only, planning)
- Infer what is likely to matter next for this patient and family.
- Surface situation-specific next questions.
- Identify emerging risks and likely next steps.

### Prepare (auto-safe tools only)
- Gather information and documents.
- Draft notes, referrals, and summaries.
- Prepare follow-up options; set up internal reminders and status checks where safe.

### Act (routed through the authority gate)
- Execute auto-safe actions immediately (summaries, drafts, internal tracking).
- Propose approval-gated actions and wait for explicit confirmation.
- Never touch forbidden actions.

The harness enforces this by routing every tool call through an authority gate that checks whether the tool is green (auto), yellow (needs approval), or red (blocked), and rejects or rewrites any call that violates policy.

### Verify (outcome-aware)
Baymax must not assume that "tool success" equals "real-world success." The harness tracks the difference between:

```text
draft prepared → request submitted → request accepted →
appointment scheduled → patient informed → plan updated
```

It checks whether a referral was actually accepted, whether an appointment is truly scheduled, and which tasks remain unresolved. This is where outcome-aware behavior is enforced.

---

## 5. Lock Points

```text
Input / Data (Eyes)   validate+normalize inputs · redact identifiers · defend prompt-injection
Tools (Hands)         3-zone policy · hard allowlist · deny-by-default for critical actions
Output (Voice)        no suggestion-as-decision · disclaimers + uncertainty · dual-voice
State / ACK (Nerves)  require real confirmations before marking a flow "done"
Memory (Longitudinal) define what is stored long-term · who can read which parts
Eval (Brain audit)    hooks for escalation correctness · over/under-escalation · hallucination · outcome verify
```

---

## 6. SDK and Implementation

Baymax should use an Agent SDK (e.g., Claude Agent SDK, OpenAI Agents SDK, or equivalent) for the generic pieces: agent loop, tool execution, context management, sandbox integration.

Baymax's uniqueness lives in:

- its domain-specific tools and schemas,
- the authority and harness rules above,
- the anticipate → prepare → act → verify loop tuned for healthcare,
- the evaluation harness that tests safety and behavior.

Concretely, the harness bolts onto SDK lifecycle hooks: `PreToolUse` = authority gate (green/yellow/red), `PostToolUse` = ACK / outcome verify, subagents = separate planner/reviewer/checker scopes.

> Using an SDK is not the flex. **Designing this harness on top of the SDK is the flex.**

---

## 7. Relationship to Authority and Capability Specs

- `AUTHORITY_SPEC.md` defines **what** Baymax is allowed to do at a policy level.
- `HARNESS_SPEC.md` (this file) defines **how** those policies are enforced in software.
- `CAPABILITY_LADDER.md` defines the reasoning/behavior levels (state-aware → anticipate → prepare → act → verify → outcome-aware).

The harness is where high-level belt concepts are turned into concrete enforcement.

---

## One-line Summary

Baymax's harness limits what it sees, what it can do, where it can execute, and how it behaves across time — so that a powerful model becomes a safe, deployable healthcare workflow agent instead of an unconstrained clinical actor.
