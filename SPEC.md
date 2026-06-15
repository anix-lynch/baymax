# Baymax Northstar Control Plane

This is the only operational entry point for agents evolving Baymax.

Do not begin from README, audit summaries, old handovers, or sibling repos.
Those are evidence and presentation surfaces. This file decides what work
matters next.

## Northstar

Build the strongest controllable Applied AI / Agent Engineer proof without
claiming hospital adoption, clinical validation, or real customer outcomes.

Baymax must:

```text
notice the right case
-> retrieve trusted cross-domain evidence
-> derive uncertainty and conflict
-> choose a bounded action
-> stop before unsafe recommendation or action
-> hand work to a real owner
-> verify durable outcome
-> follow through until closure
```

## Portfolio Strategy

Baymax is the Northstar showroom. Sibling repositories remain standalone depth
proof for separate Data / Analytics resumes.

```text
Baymax recruiter surface
├── 80% L2 agent movie
├── 15% A/B/C evidence that changes attention, trust, decision, safety, or cost
└── 5% explicitly simulated deployment readiness
```

Admission rule: a sibling feature enters Baymax only when it changes attention,
decision, safety, cost, trust, or verified outcome. Otherwise link it; do not
copy the museum into the movie.

## Honest Boundary

- Closed-loop ER simulation, not a deployed clinical system.
- Synthetic patient encounters, not real patient records.
- openFDA is a population safety signal, not causality or a drug-interaction
  claim.
- Durable Bed Ops state is simulated operational state, not a hospital system.
- Deployment-readiness artifacts may show rehearsal quality, never adoption
  receipts.

## Current Score

Current controllable L2 maturity: **83/100** after Phase 5.

The audited baseline was **66/100**. Phase 1 added four points by making the
recommendation path fail before generation and planning. Phase 2A added three
points by removing public safety self-certification and deriving action policy
and ACK from trusted state. Phase 2B added one point by deriving operational
conflict and evidence sufficiency from canonical evidence.
Phase 3A added two points by requiring an independently invoked receiver ACK
before public action execution.
Phase 3B added one point by enforcing ACK deadlines and durable stale-owner
escalation.
Phase 4 added three points by turning Care Follow-up from a plan into a
durable lifecycle with guarded closure and human escalation.
Phase 5 added three points by replacing the showroom's unversioned keyword
gate with a served, evaluated patient attention contract.

Showroom hardening (no maturity points claimed): the audit emits an
`honesty_ledger` that gates the headline verdict at the weakest load-bearing
organ. Phase 5 lifted NOSE to green; NERVES now honestly caps the headline at
yellow because cross-service recovery is not yet proven.

| Surface | Score | Current truth |
|---|---:|---|
| Recruiter movie | 9/10 | Attention Flip, Decision Flip, Brake Save are memorable |
| Brain | 14/15 | Non-ACT stops early; canonical capacity conflict changes action policy |
| Hands | 14/15 | Durable action, idempotency, retry, false-success detection |
| Immune | 13/15 | Trusted conflict and evidence sufficiency stop actions; calibration remains |
| Nerves | 10/10 | Independent ACK, deadline, timeout, escalation, and visible wait state |
| Heart + Ethics | 8/10 | Follow-up closure is durable; consent and authority remain design gaps |
| A/B/C + signal wiring | 9/15 | Eyes are live; patient Nose is served from L2; C remains a separate batch-domain proof |
| Runtime/deployment | 7/10 | Simulated acceptance, rollback, incident, and handoff contract is runnable |

Target: **80+ without hospital access, sales work, fake adoption, or feature
soup.**

## Agent Reading Order

1. Read this file.
2. Read only the canonical audit for the active phase:
   - Phase 2: `docs/baymax/constitution/brain_audit.md`,
     `docs/baymax/constitution/immune_audit.md`,
     `docs/baymax/constitution/ethics_audit.md`
   - Phase 3: `docs/baymax/constitution/nerves_audit.md`
   - Phase 4: `docs/baymax/constitution/heart_audit.md`
3. Edit canonical runtime in `../healthcare-genai-engineer`.
4. Run the phase acceptance tests there.
5. Mirror only recruiter-auditable evidence into
   `evidence/l2-decision-safety/`.
6. Update this scorecard and append audit revision evidence.
7. Regenerate `outputs/baymax_audit.json` and run Baymax tests.

Do not replace canonical audits with summaries. Do not add another planning
markdown file.

## Runtime Wiring Map

```text
Canonical L2 runtime: ../healthcare-genai-engineer

/v1/ask
├── input guard + PII redaction
├── retrieval + ESI evidence fusion
├── prediction signal
├── Decision Safety Envelope
│   ├── non-ACT -> deterministic refusal, no generator, no planner
│   └── ACT -> grounded generation + collaboration plan
└── visible evidence, decision, safety, and routing receipt

/v1/act
├── canonical evidence intake
├── Decision Safety Envelope
├── durable task + ACK
├── bounded tool execution
└── durable outcome verification

Baymax showroom
├── baymax/audit.py -> sibling integration movie
├── cases/legendary_cases.json -> memorable cases
├── outputs/baymax_audit.json -> recruiter receipt
└── ui/ -> receipt-bound story surface
```

## Execution Phases

### Phase 1 - Safety Before Recommendation

Status: **COMPLETE**

Goal: a non-`ACT` verdict cannot spend generation cost or produce an
executed-looking plan.

Implemented in canonical L2:

- Safety fusion and verdict run before grounded generation.
- `ASK_FOR_INFO`, `HUMAN_REVIEW`, `WAIT_FOR_ACK`, and `SUPPRESS` return a
  deterministic withheld response.
- Non-`ACT` responses return no operational recommendations and no agent
  collaboration plan.
- Regression tests prove generator and planner were not called.

Acceptance:

- `pytest -q` -> 78 passed.
- `make action-eval` -> all action-loop floors pass.

### Phase 2 - Trusted Safety Derivation

Status: **COMPLETE FOR OPERATIONAL SAFETY; MODEL CALIBRATION DEFERRED**

Goal: stop trusting API callers to certify whether an action is safe.

Required changes:

- [x] Derive action risk and reversibility from a versioned action policy.
- [x] Derive receiver ACK from durable task state.
- [x] Record derived facts and policy version in every safety receipt.
- [x] Remove confidence, conflict, risk, reversibility, and ACK overrides from
  the public action contract.
- [x] Derive operational conflict from canonical capacity evidence.
- [x] Derive evidence-sufficiency confidence from canonical field completeness.
- [ ] Calibrate model confidence against labelled correctness before calling it
  calibrated confidence.

Acceptance:

- [x] A caller cannot turn an unsafe case into `ACT` by changing confidence,
  conflict, risk, reversibility, or ACK fields.
- [x] Every safety decision identifies source facts and policy version.
- [x] Existing tests and action eval remain green.
- [x] Trusted conflict and evidence-sufficiency facts change or suppress a real
  action.

Earned maturity gain: **+4**. Model calibration remains a separate evidence
quality upgrade, not a blocker for trusted operational safety derivation.

### Phase 3 - Independent Receiver And ACK Deadline

Status: **COMPLETE**

Goal: turn ACK from a same-runtime second transition into independently
observed ownership.

Required changes:

- [x] Add a separately invoked receiver transition for Bed Ops.
- [x] Add ACK deadline and timeout transition.
- [x] Escalate stale ownership after the deadline.
- [x] Expose owner, deadline, wait time, and escalation through case status.

Acceptance:

- [x] Creating work does not automatically ACK it.
- [x] Receiver invocation creates the ACK.
- [x] Missed deadline creates durable escalation.
- [x] Status endpoint reports waiting and timeout states.

Earned maturity gain: **+3**.

### Phase 4 - Durable Care Follow-Up

Status: **COMPLETE**

Goal: prove Baymax does not abandon non-NOW cases after making a plan.

Required lifecycle:

```text
followup_due
-> outreach_requested
-> acknowledged
-> reassessed
-> closed_safe | escalated | unable_to_verify
```

Acceptance:

- [x] No care-complete claim without a durable closure state.
- [x] Follow-up has owner, deadline, retry budget, and safe escalation.
- [x] Status endpoint exposes the current follow-up state.

Earned maturity gain: **+3**.

### Phase 5 - Online Nose Wiring

Status: **COMPLETE.**

Goal: replace the per-case keyword gate with a served, evaluated signal
contract without opening an ML-career side quest.

Required changes:

- Serve one evaluated ranking/routing output per case.
- Baymax consumes the output before expensive retrieval/generation.
- Record model/signal version and route reason.
- Compare expensive-call reduction against serious-case recall.

Acceptance:

- Route decision is produced by the served signal contract.
- Attention Flip receipt identifies the signal version.
- Serious-case recall floor remains protected.

Measured proof:

- 497 labelled synthetic patient cases.
- 95.39% serious-case recall.
- 4.83% expensive-path reduction.
- Separate openFDA batch proof remains 30% call reduction at 95.4% recall on
  5,000 real FAERS reports; that metric is not claimed for patient routing.

Earned maturity gain: **+3**.

## Thin Deployment Readiness

Status: **COMPLETE — deliberately thin.**

Implemented:

- Machine-readable acceptance contract over the live Baymax receipt.
- Bounded offline replay, simulated shadow, and supervised sandbox stages.
- False-success incident drill that must produce `rollback_required`.
- Explicit release, safety, and sandbox ownership handoff.

Every artifact is labelled `SIMULATED DEPLOYMENT READINESS`. No duplicate FDE
runtime, fake customer metrics, hospital workflow, or adoption proof was
migrated.

## Stop Doing

- No new flagship repo.
- No separate ML resume campaign.
- No full FDE resume or fake customer receipt.
- No new organ because the metaphor sounds good.
- No dashboard, cloud, model, or markdown that does not change attention,
  decision, safety, cost, trust, or verified outcome.
- No public push until showroom filters and final review pass.

## Phase Completion Protocol

When completing a phase:

1. Commit canonical L2 runtime separately.
2. Mirror the exact proof files into Baymax evidence.
3. Append evidence to canonical organ audits.
4. Update the score and phase status in this file.
5. Run:

```bash
cd ../healthcare-genai-engineer && pytest -q && make action-eval
cd ../baymax && make test && make audit
```

6. Update `agent_common/slack_twins/tasks/baymax_finish_showroom.md` with the
   active phase and last verified commit.
