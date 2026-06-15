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

Current controllable L2 maturity: **70/100** after Phase 1.

The previous audited baseline was **66/100**. Phase 1 added four points by
making the recommendation path fail before generation and planning.

| Surface | Score | Current truth |
|---|---:|---|
| Recruiter movie | 9/10 | Attention Flip, Decision Flip, Brake Save are memorable |
| Brain | 13/15 | Non-ACT now stops before generation/planning; general arbitration remains |
| Hands | 14/15 | Durable action, idempotency, retry, false-success detection |
| Immune | 10/15 | Safety envelope works; several action safety facts remain caller-controlled |
| Nerves | 7/10 | Durable status/ACK exists; receiver is not independently invoked |
| Heart + Ethics | 5/10 | Principles exist; consent, authority, and follow-up closure are not runtime |
| A/B/C live wiring | 6/15 | Eyes are real; online Nose remains a cheap rule gate |
| Runtime/deployment | 6/10 | Live service/showroom exists; operational runtime is not fully unified |

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

Status: **NEXT**

Goal: stop trusting API callers to certify whether an action is safe.

Required changes:

- Derive evidence conflict from trusted evidence records.
- Derive action risk and reversibility from a versioned action policy.
- Derive receiver ACK from durable task state.
- Derive confidence from model/evidence outputs, not arbitrary request values.
- Record derived facts and policy version in every safety receipt.
- Keep request fields only as explicitly labeled test overrides, or remove
  them from the public contract.

Acceptance:

- A caller cannot turn an unsafe case into `ACT` by changing confidence,
  conflict, risk, reversibility, or ACK fields.
- Every safety decision identifies source facts and policy version.
- Existing tests and action eval remain green.

Expected maturity gain: **+4**.

### Phase 3 - Independent Receiver And ACK Deadline

Status: **PENDING**

Goal: turn ACK from a same-runtime second transition into independently
observed ownership.

Required changes:

- Add a separately invoked receiver worker for Bed Ops / human review.
- Add ACK deadline and timeout transition.
- Escalate stale ownership after the deadline.
- Expose owner, deadline, wait time, and escalation through case status.

Acceptance:

- Creating work does not automatically ACK it.
- Receiver invocation creates the ACK.
- Missed deadline creates durable escalation.
- Status endpoint reports waiting and timeout states.

Expected maturity gain: **+3**.

### Phase 4 - Durable Care Follow-Up

Status: **PENDING**

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

- No care-complete claim without a durable closure state.
- Follow-up has owner, deadline, retry budget, and safe escalation.
- Status endpoint exposes the current follow-up state.

Expected maturity gain: **+3**.

### Phase 5 - Online Nose Wiring

Status: **PENDING**

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

Expected maturity gain: **+3**.

## Thin Deployment Readiness

After the L2 phases above, migrate only the useful rehearsal artifacts from
`healthcare-forward-deployed-engineer`:

- integration contract
- acceptance contract
- rollout and rollback
- runbook
- handoff
- simulated incident exercise

Label every artifact `SIMULATED DEPLOYMENT READINESS`. Do not migrate duplicate
agent pipelines, retrieval, guardrails, fake production metrics, or adoption
proof.

Budget: **5% of Baymax effort**, never the active phase while an L2 gap remains.

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
