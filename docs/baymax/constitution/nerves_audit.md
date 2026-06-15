# Nerves Audit

## Responsibility

The Nerves tell Baymax what is happening now: current stage, owner, handoff
state, confidence state, capacity state, progress, and the next expected event.

## Current Grade

**B- overall**

- Durable historical state: **A-**
- Live current-state awareness: **C**
- Handoff awareness: **B-**

Baymax records the workflow well, but it still behaves more like an excellent
flight recorder than a fully live nervous system.

## Existing Capabilities

### Durable workflow event history

The action loop records intake, decision, task creation, ACK, action attempts,
retry scheduling, escalation, and outcome verification.

### Durable task and handoff state

Tasks have owner, status, creation time, and acknowledgement time. Receiver ACK
is represented as a separate durable transition.

### Current-state projection

`GET /v1/cases/{correlation_id}/status` exposes:

- current stage
- current owner
- time in stage
- next expected event
- blocking reason
- confidence before and after
- latest safety decision
- latest reason code

### Capacity and confidence visibility

Baymax consumes bed availability, occupancy, queue length, confidence,
disagreement, and decision basis.

## Missing Capabilities

- Streaming or push-based progress through SSE/WebSocket.
- A separately deployed receiver process with independently observed ACK.
- ACK deadlines and handoff timeout enforcement.
- Confidence history explaining why confidence changed at each stage.
- Source health and timestamp visibility for every operational input.
- A generalized progress model shared by recommendation and action workflows.
- Durable status for Care Follow-up execution and closure.

## Contradictions

### ACK is durable but not independently observed

The action loop creates a task and normally acknowledges it in the same runtime.
This proves a second state transition, not a real remote receiver.

### Live-looking UI is primarily post-completion

Trace timing and collaboration state are visible after `/v1/ask` completes.
The UI cannot truthfully display live states such as “waiting for ACK” without
polling the status endpoint.

### Care Follow-up has no current state

The planner describes follow-up ownership and retry policy, but no durable
follow-up worker records whether the patient was contacted, responded, became
safer, or was escalated.

## Evidence Map

| Capability | Evidence |
|---|---|
| Event history | `action_engine/store.py::events`, `action_engine/loop.py` |
| Task and ACK state | `action_engine/store.py::tasks` |
| Current status projection | `action_engine/store.py::case_status`, `app/routers/act.py` |
| Action attempts and escalation | `action_engine/worker.py` |
| Status endpoint test | `tests/test_act.py::test_status_endpoint_reports_waiting_and_blocking_state` |

## Upgrade Path

1. Add a durable separately invoked receiver worker.
2. Add ACK deadline, timeout, and stale-owner transitions.
3. Poll or stream `case_status` into the UI.
4. Record confidence-change reasons, not only values.
5. Give Care Follow-up the same durable lifecycle as Bed Ops.

## Revision History

### June 2026 - Initial canonical audit

Recorded durable state strengths and the gap between reconstructable history and
live workflow awareness.

### June 2026 - Decision Safety Envelope upgrade

Added durable safety decisions, waiting-for-ACK state, blocking reasons,
confidence deltas, and the case status endpoint.
