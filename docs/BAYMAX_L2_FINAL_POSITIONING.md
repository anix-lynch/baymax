# BAYMAX L2 FINAL POSITIONING

## Purpose

This document replaces the old L2 bullet framework with a June 2026 positioning
for frontier Applied AI / Agent Engineer roles.

It is optimized for the capabilities repeatedly requested by Anthropic,
OpenAI, Perplexity, Databricks, Scale AI, Glean, Sierra, Decagon, Cognition,
and similar agent companies:

- turn ambiguous evidence into defensible decisions;
- build end-to-end agent workflows, not isolated model calls;
- connect decisions to tools and verify outcomes;
- create evaluation and feedback loops that improve reliability;
- know when to act, ask, refuse, or defer;
- deploy reusable systems across changing models, tools, and customer
  environments.

This is a positioning and proof-target document. It does not override the
canonical diagnoses in `docs/baymax/constitution/`.

## Frontier Hiring Signal

### What companies repeatedly hire for

The recurring 2026 signal is not "prompt engineering" or "RAG chatbot."
Hiring managers repeatedly ask for:

1. **End-to-end ownership** from ambiguous problem to production workflow.
2. **Agent orchestration and tool use** with explicit control logic.
3. **Evals, observability, and feedback loops** that expose failures and drive
   improvement.
4. **Reliability and safety** under uncertainty, stale inputs, conflict, and
   tool failure.
5. **Human-in-the-loop collaboration** for high-stakes or ambiguous decisions.
6. **Customer and workflow integration** rather than model demos.
7. **Reusable platform learning** that generalizes beyond one implementation.
8. **Clear technical communication** with users, customers, and cross-functional
   teams.

### Frequency of recurring capabilities

This table combines the repeated language found across the target-company
research. Frequency is directional rather than a statistical census.

| Capability | Frequency | Role Weight |
|---|---|---|
| Design and build LLM/agent workflows | Very high | Applied AI / Agent / Both |
| Strong software engineering and APIs | Very high | Both |
| Production deployment of AI systems | Very high | Both |
| Customer-facing technical ownership | Very high in FDE | FDE / Solutions |
| End-to-end workflow integration | High | Both, heavier in FDE |
| Monitoring, observability, and reliability | High | Both |
| Prompting, RAG, retrieval, and model selection | High | Applied AI / Agent |
| Customer discovery and solution architecture | High in FDE | FDE / Solutions |
| POCs, pilots, and evaluation suites | High | FDE / Solutions / Applied AI |
| Adoption and go-live ownership | High in FDE | FDE / Solutions |
| Cross-functional collaboration | High | Both |
| Safety, guardrails, and evals | Medium-high and rising | Applied AI / Agent |
| Multi-agent and long-horizon reasoning | Medium | Applied AI / Agent |

### Keyword clusters

**Technology:** LLM workflows, autonomous agents, agent orchestration, tool use,
function calling, RAG, semantic retrieval, vector databases, APIs, distributed
systems, Docker, cloud infrastructure, Python, TypeScript, model selection.

**Behavior and reliability:** robustness, production reliability, guardrails,
ethical AI, failure detection, monitoring, troubleshooting, ambiguity,
ownership.

**Deployment:** production environments, real-time inference, CI/CD,
containerization, maintenance, performance benchmarking.

**Adoption and customer:** discovery, solution architecture, POC, pilot,
onboarding, go-live, adoption, technical advisor, workflow integration,
business outcomes.

**Evaluation:** rigorous evaluations, agent performance, safety testing,
failure analysis, evaluation suites, realistic environments.

### Applied AI versus FDE

| Applied AI / Agent Engineer | Forward Deployed Engineer |
|---|---|
| Builds reusable agent behavior, evals, control loops, and platform primitives | Adapts those primitives to a customer's workflow, systems, constraints, and success criteria |
| Primary proof: agent correctness, reliability, tool use, feedback loops, reusable architecture | Primary proof: integration, adoption, customer ownership, rollout, measurable workflow outcome |
| Baymax L2 currently owns this layer | Baymax Hospital/L3 remains the future FDE proof layer |

### The actual L2/L3 boundary

Baymax is already deployed as a live Cloud Run service. The missing L3 proof is
not deployment itself.

The missing proof is:

> Has Baymax passed through another organization's data, auth, security,
> workflow, politics, user training, and adoption process, then produced a
> measured operational outcome?

That is the boundary between a deployed Applied AI system and a
forward-deployed, adopted workflow.

### Organ-to-hiring-signal map

| Organ | Primary Hiring Signal | L2 / L3 Boundary |
|---|---|---|
| Nose | Applied AI | Attention, routing, model/tool cost control |
| Eyes | Both | Trusted evidence in L2; customer data/security reality in L3 |
| Tongue | Applied AI | Grounding and semantic meaning |
| Brain | Applied AI | Reasoning, arbitration, decision policy |
| Hands | Both | Tool execution in L2; real customer systems in L3 |
| Nerves | Both | Runtime state in L2; live operational workflow in L3 |
| Immune | Applied AI, then FDE when live | Safety/evals in L2; customer-environment enforcement in L3 |
| Heart | FDE-heavy | Trust, follow-up, adoption, user behavior |
| Ethics | Both | Policy design in L2; enforcement under customer constraints in L3 |
| Hospital | FDE | Discovery, rollout, adoption, workflow change, outcomes |

## Benchmark Tiers

| Tier | Meaning |
|---|---|
| Foundation | Feature exists or works on a narrow happy path |
| Strong | End-to-end behavior is tested, measurable, and honestly bounded |
| Frontier | Behavior generalizes across workflows, uses trusted runtime state, and improves through evaluation/feedback loops |
| Field-Proven | Real users or customers repeatedly use it; adoption, operational ownership, and outcomes are measured |

---

# Bullet 1 - Evidence Arbitration

## Positioning

Turns conflicting, incomplete, or stale evidence into defensible decisions.

## 1. Resume Bullet

**Current earned wording**

> Built a reusable decision-safety gate that detects stale or incomplete
> evidence, tracks confidence degradation and conflicts, suppresses unsafe
> recommendations, and routes high-risk decisions to durable human review.

**Frontier target wording**

> Built an evidence-arbitration layer that ranks source trust, detects
> cross-domain contradictions and freshness decay, selects the safest
> reversible decision, and escalates unresolved high-risk conflicts with a
> complete audit trail.

## 2. ATS Keywords

Evidence arbitration, grounding, provenance, source trust, uncertainty
estimation, confidence scoring, conflict detection, data freshness, decision
support, human-in-the-loop, escalation, guardrails, policy engine, risk
assessment, explainability, audit trail, retrieval, context engineering.

## 3. Human Explanation

**ข้อมูลตีกัน Baymax รู้ว่าเมื่อไรควรหยุด เมื่อไรควรถามเพิ่ม และเมื่อไรต้องเรียกคน**

Today Baymax can detect stale capacity data, low confidence, supplied conflict,
and missing evidence. It cannot yet independently decide which of two trusted
cross-domain sources deserves more weight.

## 4. Benchmark Tier

**Current: Strong-minus**

Why:

- stale/default-1970 evidence is suppressed before action;
- low-confidence recommendations are withheld;
- dangerous conflict creates durable human review;
- reason codes and confidence before/after are queryable.

Why not Frontier:

- source-trust ranking does not yet exist;
- conflict signals and several safety facts can be supplied by the caller;
- no generalized arbitration across patient, drug, operational, and policy
  evidence.

## 5. Proof Targets

### To earn Strong completely

- 100% stale-capacity suppression across a dated adversarial suite.
- 100% high-risk conflict escalation with zero durable action commits.
- Every non-`ACT` decision records reason code, missing evidence, owner, and
  next expected event.
- No caller-controlled field can bypass a safety decision.

### To earn Frontier

- Trusted source registry with explicit lineage, freshness policy, and trust
  score.
- Cross-domain conflict benchmark containing patient history, drug risk,
  capacity state, and policy evidence.
- Independent labels for the correct arbitration outcome.
- Measured calibration: confidence bands correspond to observed correctness.
- Decision-change receipts showing exactly which new evidence changed the
  action.

## 6. Repo Mapping

### Baymax organs

Eyes + Brain + Immune + Ethics.

### Actual files

- `action_engine/safety.py`
- `action_engine/contract.py`
- `action_engine/loop.py`
- `action_engine/store.py`
- `workflows/classify_esi.py`
- `app/routers/ask.py`
- `app/routers/act.py`
- `docs/baymax/constitution/brain_audit.md`
- `docs/baymax/constitution/immune_audit.md`
- `docs/baymax/constitution/ethics_audit.md`

## 7. Evidence Artifacts

- `tests/test_action_engine.py::test_stale_1970_capacity_is_suppressed_before_action`
- `tests/test_action_engine.py::test_high_risk_irreversible_conflict_requires_human_review`
- `tests/test_ask.py::test_low_confidence_recommendation_is_suppressed`
- `tests/test_act.py::test_legendary_safety_envelope_case`
- `GET /v1/cases/{correlation_id}/status`
- Future required artifact: `outputs/evidence_arbitration_eval.json`

## Remaining Gaps

- Trusted source ranking.
- General cross-domain contradiction detection.
- Independent derivation of confidence, conflict, risk, and reversibility.
- Explicit alternative-action comparison.

---

# Bullet 2 - Decision to Action to Outcome

## Positioning

Turns decisions into verified real-world actions.

## 1. Resume Bullet

**Current earned wording**

> Built a durable evidence-to-action agent loop that converts ER capacity
> decisions into idempotent tool execution, records receiver ACK and
> before/after state, retries within bounded budgets, escalates exhausted
> failures, and independently verifies outcomes to catch false success.

**Frontier target wording**

> Built a reusable closed-loop agent runtime that plans, delegates, executes,
> verifies, recovers, and learns across multiple workflows and tools while
> preserving idempotency, ownership, and complete trajectory receipts.

## 2. ATS Keywords

Agent orchestration, tool calling, workflow automation, durable execution,
state machines, idempotency, event-driven architecture, handoff protocol,
receiver acknowledgement, retries, recovery, escalation, outcome verification,
closed-loop agents, distributed systems, auditability, observability.

## 3. Human Explanation

**AI ไม่ได้ตอบเก่งอย่างเดียว มันส่งงาน ลงมือ เช็กว่าเกิดจริง และไม่โกหกว่าสำเร็จ**

## 4. Benchmark Tier

**Current: Strong**

This is Baymax's strongest hiring signal.

Why:

- real durable state change rather than recommendation-only JSON;
- separate task creation and ACK transition;
- before/after receipts;
- idempotent replay;
- bounded retries and escalation;
- durable-state re-read catches false success;
- all action-loop proof floors currently pass.

Why not Frontier:

- one principal action workflow and one state-changing tool;
- ACK is durable but normally performed by the same runtime;
- no generalized workflow/tool registry or learning loop;
- no real external receiver or customer system.

## 5. Proof Targets

### To preserve Strong

- 100% valid intake acceptance and invalid intake blocking.
- 100% durable task creation and receiver ACK coverage.
- 100% verified action-state transition on applicable cases.
- 0% duplicate side effects.
- 100% false-success detection.
- 100% bounded-retry and exhausted-escalation compliance.

### To earn Frontier

- At least three materially different action workflows using the same runtime.
- At least two independently running receiver workers.
- Real ACK timeout, takeover, and recovery behavior.
- Outcome verifier contracts for multiple tools.
- Trajectory-level evals measuring task completion, recovery, and verified
  outcome across workflows.
- Learning artifact showing repeated failures changed reusable agent policy.

## 6. Repo Mapping

### Baymax organs

Brain + Hands + Nerves + Brakes + Immune.

### Actual files

- `action_engine/loop.py`
- `action_engine/store.py`
- `action_engine/tools.py`
- `action_engine/worker.py`
- `app/bed_ops_agent.py`
- `app/routers/act.py`
- `evaluation/action_eval.py`
- `evaluation/agent_eval.py`

## 7. Evidence Artifacts

- `outputs/action_eval_summary.json`
- `outputs/action_loop.db`
- `outputs/agent_eval_summary.json`
- `tests/test_action_engine.py`
- `tests/test_act.py`
- Current action-eval proof:
  - successful transition rate: `1.0`
  - duplicate side-effect rate: `0.0`
  - outcome verification coverage: `1.0`
  - false-success rate: `0.0`
  - exhausted escalation rate: `1.0`

## Remaining Gaps

- Independent receiver runtime.
- Multi-tool and multi-workflow generalization.
- External-system integration.
- Policy learning from trajectory failures.

---

# Bullet 3 - Agent Reliability and Safety

## Positioning

Prevents unsafe, hallucinated, stale, degraded, or falsely successful behavior.

## 1. Resume Bullet

**Current earned wording**

> Engineered an evaluated agent reliability layer with fail-closed evidence
> intake, grounded-answer refusal, safety-floor overrides, stale-state
> suppression, bounded recovery, durable escalation, regression gates, and
> outcome verification that detects false tool success.

**Frontier target wording**

> Built a continuous agent-improvement system that converts production
> trajectories and adversarial failures into calibrated evals, policy updates,
> release gates, and measurable reliability gains across models and workflows.

## 2. ATS Keywords

Agent evaluation, LLM evaluation, eval-driven development, observability,
guardrails, adversarial testing, red teaming, hallucination prevention,
grounding, regression testing, release gates, safety engineering, reliability,
monitoring, failure analysis, uncertainty, policy enforcement, feedback loops.

## 3. Human Explanation

**AI ฉลาดอย่างเดียวไม่พอ ต้องรู้ว่าเมื่อไรตัวเองอาจผิด และหยุดก่อนทำเรื่องพัง**

## 4. Benchmark Tier

**Current: Strong-minus**

Why:

- safety envelope changes behavior rather than only emitting warnings;
- malformed and stale evidence fail closed;
- empty retrieval refuses to guess;
- action outcome is independently verified;
- adversarial, agent, action, retrieval, and regression evals exist;
- known weaknesses are reported honestly.

Why not Frontier:

- adversarial prompt-injection recall is `0.545`;
- unsupported claims without explicit fake citation IDs may still pass;
- eval failures do not yet automatically become reusable policy improvements;
- no production trajectory feedback loop or model-comparison gate.

## 5. Proof Targets

### To earn Strong completely

- 100% safety-critical and stale-state floors.
- 100% non-`ACT` suppression across recommendation, planning, and action paths.
- Claim-level citation enforcement.
- Adversarial recall above an explicit release floor without unacceptable
  benign false positives.
- Every safety failure mapped to owner, remediation, and regression test.

### To earn Frontier

- Continuous trajectory ingestion from the runtime.
- Automated clustering and taxonomy of agent failures.
- Evaluation-driven release policy across multiple models.
- Calibrated uncertainty and measured abstention quality.
- Published reliability improvement across successive policy/model versions.
- Cost, latency, safety, and task-success tradeoff curves.

## 6. Repo Mapping

### Baymax organs

Immune + Brakes + Brain + Nerves.

### Actual files

- `action_engine/safety.py`
- `action_engine/contract.py`
- `action_engine/worker.py`
- `generation/generate.py`
- `guardrails/input_validator.py`
- `guardrails/output_validator.py`
- `evaluation/adversarial_eval.py`
- `evaluation/action_eval.py`
- `evaluation/regression_gate.py`
- `.github/workflows/eval.yml`

## 7. Evidence Artifacts

- `outputs/adversarial_summary.json`
- `outputs/action_eval_summary.json`
- `outputs/eval_summary.json`
- `outputs/agent_eval_summary.json`
- `docs/operational_story.md`
- `docs/baymax/constitution/immune_audit.md`

## Remaining Gaps

- Claim-level grounding enforcement.
- Strong paraphrased prompt-injection defense.
- Calibrated uncertainty.
- Continuous runtime-to-eval feedback loop.
- Cross-model reliability comparison.

---

# Bullet 4 - Human Collaboration and Conduct

## Positioning

Knows when to act, when to ask, when to challenge, and when to defer.

## 1. Resume Bullet

**Current earned wording**

> Designed reason-coded human-in-the-loop controls that withhold
> low-confidence recommendations, pause high-risk conflicting actions, create
> durable review ownership, expose current blocking state, and preserve
> safety-critical decisions against unsafe downgrade.

**Frontier target wording**

> Built a conduct-aware agent that reasons over requester authority, patient
> consent, uncertainty, action reversibility, and care obligations to
> consistently challenge unsafe instructions, ask targeted clarifying
> questions, defer high-risk decisions, and follow through to verified closure.

## 2. ATS Keywords

Human-in-the-loop, human-AI collaboration, escalation, clarification,
abstention, refusal, consent, authorization, policy enforcement, decision
support, explainability, workflow ownership, case management, follow-up,
customer experience, responsible AI, trust and safety.

## 3. Human Explanation

**Baymax ไม่ได้มาแทนคน มันรู้ว่าเมื่อไรควรช่วย เมื่อไรควรถาม และเมื่อไรต้องยอมให้คนตัดสิน**

## 4. Benchmark Tier

**Current: Foundation-plus**

This is Baymax's most differentiated future theme and its least complete current
bullet.

What exists:

- low confidence triggers `ASK_FOR_INFO`;
- dangerous conflict triggers durable `HUMAN_REVIEW`;
- pending ownership triggers `WAIT_FOR_ACK`;
- safety rules challenge lower-risk predictions;
- status endpoint exposes owner and blocking reason.

Why not Strong:

- no requester authority or scope-of-practice model;
- no patient consent, preference, refusal, or appeal;
- clarification is a decision code, not a targeted question;
- Care Follow-up is a plan, not a durable closure loop;
- refusal language is mechanically safe but not consistently helpful;
- recommendation-path human review is not always durable.

## 5. Proof Targets

### To earn Strong

- Conduct Envelope enforced before generation, planning, recommendation, and
  action.
- Trusted requester identity, role, authority, and consent state.
- Structured clarification questions tied to missing evidence.
- Every refusal includes reason, safe next step, and owner.
- Durable Care Follow-up lifecycle with deadline, ACK, reassessment, escalation,
  and closure.
- Character trajectory tests for challenge, clarification, refusal, defer, and
  follow-through.

### To earn Frontier

- User studies measuring whether humans understand and appropriately respond to
  Baymax challenges and uncertainty.
- Measured human override quality and unsafe-compliance reduction.
- Policy generalization across workflows and requester roles.
- Learning loop from human corrections, overrides, and follow-up outcomes.
- Field evidence that humans trust Baymax without over-trusting it.

## 6. Repo Mapping

### Baymax organs

Heart + Ethics + Brain + Nerves.

### Actual files

- `action_engine/safety.py`
- `action_engine/loop.py`
- `action_engine/store.py`
- `app/agents.py`
- `app/routers/ask.py`
- `app/routers/act.py`
- `docs/baymax/constitution/heart_audit.md`
- `docs/baymax/constitution/ethics_audit.md`

## 7. Evidence Artifacts

- `GET /v1/cases/{correlation_id}/status`
- `tests/test_action_engine.py::test_high_risk_irreversible_conflict_requires_human_review`
- `tests/test_act.py::test_status_endpoint_reports_waiting_and_blocking_state`
- `tests/test_ask.py::test_low_confidence_recommendation_is_suppressed`
- Future required artifact: `outputs/conduct_trajectory_eval.json`
- Future required artifact: `outputs/care_followup_closure_eval.json`

## Remaining Gaps

- Conduct Envelope.
- Consent and authority.
- Targeted clarification.
- Durable follow-up closure.
- Human-centered behavior evaluation.

---

# Bullet 5 - Deployable Agent Platform

## Positioning

Separates agent behavior from model, retriever, cloud, and tool choices.

## 1. Resume Bullet

**Current earned wording**

> Built a provider-swappable agent service with Anthropic/OpenAI generation,
> BM25/dense/hybrid retrieval, versioned evidence contracts, deterministic
> safety and action logic, Cloud Run deployment, and cross-cloud upstream data
> parity proofs across GCP, Microsoft Fabric, and AWS.

**Frontier target wording**

> Built a portable agent platform that runs the same governed workflows,
> safety policies, tools, evals, and outcome contracts across model providers,
> clouds, and customer environments without changing behavioral guarantees.

## 2. ATS Keywords

AI platform, agent platform, model-agnostic, vendor-agnostic, multi-model,
multi-cloud, cloud-native, API integration, platform engineering, reusable
workflows, SDK, tool adapters, model routing, deployment, CI/CD, FastAPI,
Docker, GCP, AWS, Azure, Microsoft Fabric, Anthropic, OpenAI, Gemini.

## 3. Human Explanation

**เปลี่ยนสมองหรือย้ายครัวได้ โดยไม่ต้องสอน Baymax ใหม่ว่าควรคิดและทำงานอย่างไร**

## 4. Benchmark Tier

**Current: Strong-minus platform story; Foundation L2 runtime portability**

What exists:

- Anthropic/OpenAI provider switch with deterministic fallback;
- BM25/dense/hybrid retrieval methods;
- versioned canonical evidence contract;
- deterministic decision and action path independent of LLM calls;
- Docker/FastAPI/Cloud Run deployment;
- upstream GCP/Fabric/AWS data parity proof.

Honest boundary:

- L2 runtime is deployed on GCP Cloud Run, not independently deployed and
  behavior-verified across three clouds;
- Gemini is not wired as an L2 generation provider;
- tool adapters and workflows are not yet a public reusable SDK;
- no cross-model behavioral parity eval.

## 5. Proof Targets

### To earn Strong runtime portability

- Same L2 contract and acceptance suite passes on at least two cloud runtimes.
- Anthropic and OpenAI paths both execute the same golden and safety evals.
- Model/provider failure produces bounded fallback without behavioral drift.
- Tool adapters implement one common contract with parity tests.
- Deployment artifacts and costs are reproducible.

### To earn Frontier

- Three model providers and three deployment environments.
- Behavioral parity gates across provider/cloud combinations.
- Policy and outcome contracts remain invariant across environments.
- Automated model routing by task success, safety, latency, and cost.
- Reusable workflow/tool SDK consumed by more than one application.
- Customer/environment adapter pattern proven without forking core behavior.

## 6. Repo Mapping

### Baymax organs

Whole body, especially Brain + Hands + Nerves + Immune, consuming Eyes/Tongue/Nose
infrastructure.

### Actual files and sibling proof

- `generation/generate.py`
- `retrieval/query_pipeline.py`
- `action_engine/contract.py`
- `action_engine/loop.py`
- `Dockerfile`
- `deploy/cloudrun.sh`
- `.github/workflows/eval.yml`
- `outputs/portability_proof.json`
- sibling GCP, Fabric, and AWS healthcare repositories referenced in the
  portability artifact.

## 7. Evidence Artifacts

- `outputs/portability_proof.json`
- `outputs/action_eval_summary.json`
- `outputs/eval_summary.json`
- `Dockerfile`
- Cloud Run live service
- Future required artifact: `outputs/model_behavior_parity.json`
- Future required artifact: `outputs/l2_multicloud_acceptance.json`

## Remaining Gaps

- L2 multi-cloud runtime execution.
- Gemini provider adapter.
- Cross-provider behavioral parity.
- Reusable workflow/tool SDK.
- Automated model routing.

---

# Final L2 Positioning

## Strongest Evidence-Supported Identity Today

**Applied AI / Agent Engineer building reliable evidence-to-action systems.**

Baymax's strongest proof is not that it answers healthcare questions. It is
that it:

```text
reads evidence
-> detects when evidence is unsafe
-> makes a bounded decision
-> creates durable work
-> waits for ownership
-> executes idempotently
-> verifies reality
-> escalates when it cannot finish safely
```

## Current Hiring Signal by Bullet

| Bullet | Current Tier | Hiring Value | Primary Gap |
|---|---|---|---|
| Evidence Arbitration | Strong-minus | High differentiation | Trusted cross-domain arbitration |
| Decision to Action to Outcome | Strong | Strongest current proof | Multi-workflow / independent receivers |
| Agent Reliability and Safety | Strong-minus | Core frontier signal | Continuous eval-feedback loop |
| Human Collaboration and Conduct | Foundation-plus | Highest future differentiation | Consent, authority, durable follow-up |
| Deployable Agent Platform | Strong-minus story / Foundation runtime portability | Broad platform signal | L2 parity across models/clouds |

## Minimum Work With Maximum Hiring Return

1. Prevent every non-`ACT` verdict from producing an executed-looking plan.
2. Build trusted evidence arbitration for one legendary cross-domain decision
   flip.
3. Add a Conduct Envelope with targeted clarification and durable human review.
4. Turn Care Follow-up from a plan into a verified closure loop.
5. Run the same safety/eval suite across Anthropic and OpenAI and publish the
   behavioral parity receipt.

These upgrades directly match recurring frontier hiring signals: reliable
agents, eval-driven improvement, human collaboration, end-to-end ownership, and
reusable systems.

## Artifacts That Signal L2 Applied AI / Agent Engineer

1. A serious agent-system repository with orchestration, tools, retrieval,
   safety, state, and evaluation mechanisms.
2. A live deployment with operational traces, latency, failure receipts, and
   bounded recovery.
3. A system card or constitutional health record documenting safety behavior,
   known limits, and evaluation evidence.
4. A technical narrative explaining architecture tradeoffs and why specific
   controls exist.
5. Reproducible evaluation and release gates proving the agent remains reliable
   as behavior changes.

Baymax currently has meaningful proof for all five, though the public showroom
must make the path easier for a busy reviewer.

## Additional Artifacts Required for L3 / FDE

1. A real external-team workflow with discovery notes and an agreed baseline.
2. Customer-specific integration with data, auth, tools, and security
   constraints.
3. A pilot or POC carried through go-live.
4. User onboarding, training, support, and operational handover artifacts.
5. Adoption and workflow outcome metrics.
6. Evidence that the customer or receiving team can operate the system without
   the builder acting as the hidden runtime.

The same Baymax architecture can support an FDE resume later, but L3 claims
must not inherit L2 engineering proof as a substitute for adoption.

# Research Sources

Research accessed June 2026. Job pages change; retain the recurring capability
signals rather than treating any single posting as permanent.

- Anthropic, Forward Deployed Engineer / Applied AI:
  `https://www.anthropic.com/careers/jobs/4957321008`
- Anthropic, Research Engineer / Production Model Post-Training:
  `https://www.anthropic.com/careers/jobs/5107129008`
- OpenAI, Forward Deployed Engineer:
  `https://openai.com/careers/forward-deployed-engineer-san-francisco/`
- OpenAI, Enterprise AI Platform Engineer:
  `https://openai.com/careers/enterprise-ai-platform-engineer-san-francisco/`
- Perplexity, Forward Deployed AI Engineer:
  `https://www.perplexity.ai/hub/job/forward-deployed-ai-engineer-london`
- Databricks, Agent Bricks / production AI agents:
  `https://www.databricks.com/blog/productionizing-ai-agents`
- Databricks, Applied AI / Agent Evaluation:
  `https://www.databricks.com/blog/announcing-applied-ai-agent-evaluation`
- Scale AI, Forward Deployed Engineer:
  `https://scale.com/careers/4660694005`
- Glean, Forward Deployed Engineer:
  `https://jobs.ashbyhq.com/glean/42d4452d-54ca-47ba-872b-6c017d86a971`
- Sierra, Forward Deployed Engineer:
  `https://sierra.ai/careers/3d62ba98-9f6f-43d6-9429-8818447bf068`
- Decagon, AI Agent Product Engineer:
  `https://jobs.ashbyhq.com/decagon/182c1da1-5d05-4c00-843a-cf362bdc5d07`
- Cognition, Forward Deployed Engineer:
  `https://jobs.ashbyhq.com/cognition/022f17a3-e2e1-4f08-8393-a3077087248e`
- Palantir, Forward Deployed AI Engineer:
  `https://jobs.lever.co/palantir/636fc05c-d348-4a06-be51-597cb9e07488`
- GE Vernova, AI Agent Engineer:
  `https://careers.gevernova.com/ai-agent-engineer/job/R5042488`
- Decagon, Introducing the Agent Engineer:
  `https://decagon.ai/blog/introducing-agent-engineer`
- OpenAI, Software Engineer - Agent Infrastructure:
  `https://openai.com/careers/software-engineer-agent-infrastructure-san-francisco/`
