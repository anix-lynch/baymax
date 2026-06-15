# Baymax Brain Diagnosis

## Verdict

The hypothesis is about 70% correct.

Baymax already has a brain, but it behaves like:

> Remember a task-specific protocol and execute it with discipline.

It does not yet behave like:

> Maintain a reusable Brain Library that selects protocols, compares options,
> resolves conflicting evidence, and knows when not to decide.

The current L2 repo is a strong procedural action engine, but not yet a general
reusable reasoning engine.

## Critical Findings

### 1. Conflict resolution only covers safety-floor precedence

Rules beat RAG when a safety floor fires, and prediction cannot downgrade a
NOW case.

Existing code:

- `workflows/classify_esi.py`
- `app/routers/ask.py`

Missing:

- General conflict protocol for patient history versus drug evidence.
- Fresh evidence versus stale operational state.
- Two trusted sources that disagree without a predefined safety-floor winner.

### 2. Baymax selects an action but does not compare actions

Bed Ops uses a deterministic decision tree to select one disposition directly.

Existing code:

- `app/bed_ops_agent.py`

Missing:

```text
candidate actions
→ score benefit / risk / reversibility / evidence quality
→ explain rejected alternatives
→ select an action or ask a human
```

### 3. Uncertainty exists as data but does not consistently control behavior

RAG confidence and prediction confidence are calculated.

Missing reusable rule:

```text
low confidence
+ conflicting evidence
+ high-risk or irreversible action
→ require human review
```

### 4. Most multi-agent protocols are plans, not executed procedural memory

`app/agents.py` creates handoff, retry, stop, and escalation contracts.

Bed Ops executes through a durable loop. Care Follow-up and ER Triage mostly
remain descriptive plans and do not prove the same durable ACK, execution, and
outcome-verification behavior.

### 5. Decision evaluation has honesty drift

Some scenarios still use `MISS-*` names and descriptions claiming that
production logic was intentionally not patched to chase a green score.

The current production rules now pass all 50 scenarios. Therefore,
`decision_correctness=1.0` proves protocol conformance on the current known
scenario set, not independent reasoning generalization.

## Existing Procedural Memory

| Procedural skill | Current proof | Grade |
|---|---|---:|
| Fail closed on invalid evidence | `action_engine/contract.py` | A |
| Safety-floor conflict resolution | `workflows/classify_esi.py` | B+ |
| Prediction cannot downgrade acute safety | `app/routers/ask.py` | B+ |
| Bed and capacity decision tree | `app/bed_ops_agent.py` | A- |
| Handoff planning | `app/agents.py` | B |
| Retry, stop, and escalation | `action_engine/worker.py` | A |
| Durable receiver ACK | `action_engine/store.py` | A- |
| Outcome verification | `action_engine/worker.py` | A |
| False-success detection | `action_engine/worker.py` | A |
| Recommendation generation | `app/prediction.py` | C+ |

## Knowledge Layer vs Thinking Layer

```text
KNOWLEDGE LAYER — What Baymax knows
├── ✅ retrieved patient precedents
├── ✅ citations and provenance
├── ✅ canonical evidence contract
├── ✅ triage and prediction signals
└── 🟡 freshness exists as a field but stale evidence is not actually rejected

THINKING LAYER — How Baymax works
├── ✅ safety rules override weaker signals
├── ✅ deterministic Bed Ops decision tree
├── ✅ bounded retry and escalation
├── ✅ durable action and outcome verification
├── 🟡 conflict resolution only covers known safety conflicts
├── 🟡 handoff protocols exist, but most are descriptive plans
├── ❌ reusable uncertainty-to-human policy
├── ❌ candidate-action comparison and tradeoff scoring
├── ❌ rejected-alternative explanation
├── ❌ learning procedural lessons from failed outcomes
└── ❌ formal reusable Brain Library
```

## Missing Brain Library

Do not build twenty disconnected skill files. Build three reusable protocols.

### 1. Evidence Arbitration

Decide which evidence wins based on:

- source trust
- freshness
- agreement
- uncertainty
- safety impact

### 2. Action Deliberation

Generate two or three reasonable actions, score risk, reversibility, and value,
record rejected alternatives, then choose or escalate.

### 3. Closure Protocol

Generalize the strongest existing Bed Ops behavior:

```text
dispatch
→ receiver ACK
→ action
→ outcome re-read
→ retry or escalate
```

Reuse it for Care Follow-up and clinician review.

## Shortest High-ROI Upgrade

Build one legendary trajectory:

```text
Two trusted evidence sources disagree
→ Baymax detects the conflict
→ generates three possible actions
→ rejects two with reasons
→ asks a human because uncertainty × action risk is too high
→ handoff ACK is verified
→ outcome is checked
```

This single trajectory would prove the missing Thinking Layer better than
another retrieval source or dashboard.

## Audit Proof

- Relevant tests: `33 passed`
- Bed Ops labelled scenario evaluation: `50/50`
- Action-loop floors: all passed

## One-Line Diagnosis

> A/B/C make Baymax good at reading. L2 currently makes Baymax good at
> following a manual. A Brain Library will make Baymax know which manual to
> open, and when to put the manual down and ask a human.
