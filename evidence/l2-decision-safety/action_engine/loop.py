"""The durable Bed Ops action loop — the Phase-1 vertical spine.

Stages (each one a durable write the audit can replay):

    intake (validate contract, fail closed)
      -> decision (REUSES app.bed_ops_agent.decide_bed_disposition)
      -> create durable action task
      -> worker acknowledges ownership (separate transition)
      -> idempotent state-changing tool + before/after receipt
      -> outcome verifier re-reads durable state
      -> exhausted recovery -> durable human escalation task

The decision is intentionally the existing, already-tested Bed Ops function:
that call IS the "evidence caused the decision" link, and it keeps existing
behavior intact. The action engine adds the durable execution spine around it.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Optional

from app.bed_ops_agent import decide_bed_disposition
from app.schemas import ERState

from action_engine.adapters import SourceAdapter, SyntheticFixtureAdapter
from action_engine.contract import CanonicalEvidence, validate_evidence
from action_engine.policy import (
    SafetyDerivation,
    derive_ack_state,
    derive_pre_action,
    derive_pre_decision,
)
from action_engine.safety import SafetyContext, evaluate_safety
from action_engine.store import ActionStore
from action_engine.tools import Injection
from action_engine.worker import ActionResult, ActionRetryPolicy, acknowledge, execute_action, verify_outcome


@dataclass
class LoopResult:
    correlation_id: str
    accepted: bool
    blocked_reason: Optional[list[str]]
    disposition: Optional[str]
    task_id: Optional[str]
    acknowledged: bool
    action: Optional[ActionResult]
    outcome: Optional[dict[str, Any]]
    escalation_id: Optional[str]
    safety_decision: str
    safety_reason_code: str


def _idempotency_key(correlation_id: str, disposition: str) -> str:
    """Stable key shared by task, action, world-state, and outcome for a case."""
    return f"{correlation_id}:{disposition}"


def _decide(evidence: CanonicalEvidence) -> dict[str, Any]:
    """Run the EXISTING Bed Ops decision over canonical evidence."""
    er = ERState(
        available_beds=evidence.er_state.available_beds,
        occupancy_pct=evidence.er_state.occupancy_pct,
        queue_length=evidence.er_state.queue_length,
    )
    return decide_bed_disposition(
        er_state=er,
        triage_level=evidence.triage_level,
        predicted_los_hours=evidence.predicted_los_hours,
        bed_pressure_risk=evidence.bed_pressure_risk,
    )


def run_action_loop(
    *,
    store: ActionStore,
    record: dict[str, Any],
    adapter: SourceAdapter | None = None,
    injection: Injection | None = None,
    policy: ActionRetryPolicy | None = None,
    sleep: Callable[[float], None] | None = None,
    safety_context: SafetyContext | None = None,
    require_external_ack: bool = False,
) -> LoopResult:
    """Process one source record through the full durable action loop.

    `record` is a source-specific row; `adapter` maps it to the canonical
    contract. `injection` is an optional failure-injection directive (defaults
    to none / production behavior). `safety_context` is an internal test-only
    failure injection. Public API callers cannot set it.
    """
    adapter = adapter or SyntheticFixtureAdapter()
    injection = injection or Injection.from_raw(record.get("inject"))

    raw = adapter.to_contract(record)
    result = validate_evidence(raw)
    correlation_id = (raw.get("correlation_id") or record.get("correlation_id") or "unknown")

    # ── Eyes: fail closed before the decision engine ────────────────────────
    if not result.ok:
        store.record_case(
            correlation_id=correlation_id,
            contract_version=str(raw.get("contract_version")),
            source=str(raw.get("source", adapter.name)),
            source_id=str(raw.get("source_id", "")),
            evidence_json=raw, status="blocked",
        )
        store.log_event(correlation_id, "intake_blocked", {"errors": result.errors})
        return LoopResult(
            correlation_id=correlation_id, accepted=False, blocked_reason=result.errors,
            disposition=None, task_id=None, acknowledged=False, action=None,
            outcome=None, escalation_id=None,
            safety_decision="SUPPRESS", safety_reason_code="INVALID_EVIDENCE_CONTRACT",
        )

    evidence = result.evidence
    assert evidence is not None
    store.record_case(
        correlation_id=correlation_id, contract_version=evidence.contract_version,
        source=evidence.source, source_id=evidence.source_id,
        evidence_json=raw, status="accepted",
    )
    store.log_event(correlation_id, "intake_accepted", {"lineage": evidence.lineage()})

    if safety_context is None:
        pre_derivation = derive_pre_decision(evidence)
    else:
        pre_derivation = SafetyDerivation(
            context=SafetyContext(
                ingested_at=safety_context.ingested_at,
                required_evidence_complete=safety_context.required_evidence_complete,
                confidence_before=safety_context.confidence_before,
                confidence_after=safety_context.confidence_after,
                evidence_conflicts=safety_context.evidence_conflicts,
                action_risk=safety_context.action_risk,
                reversible=safety_context.reversible,
                receiver_acknowledged=None,
                current_stage="pre_decision_safety_review",
            ),
            facts={"internal_test_override": True},
            policy_version="internal-test-override.v1",
        )
    pre_verdict = evaluate_safety(pre_derivation.context)
    store.record_safety_decision(
        correlation_id, pre_verdict,
        policy_version=pre_derivation.policy_version,
        derived_facts=pre_derivation.facts,
    )
    if pre_verdict.decision != "ACT":
        stage = "human_review_required" if pre_verdict.decision == "HUMAN_REVIEW" else "safety_blocked"
        if pre_verdict.decision == "HUMAN_REVIEW":
            store.create_escalation(
                escalation_id=f"esc:safety:{correlation_id}",
                correlation_id=correlation_id,
                reason=pre_verdict.blocking_reason or pre_verdict.reason_code,
                owner="charge_nurse_review_queue",
                attempts_used=0,
            )
        store.log_event(correlation_id, stage, {
            "decision": pre_verdict.decision,
            "reason_code": pre_verdict.reason_code,
            "next_expected_event": pre_verdict.next_expected_event,
        })
        return LoopResult(
            correlation_id=correlation_id, accepted=False,
            blocked_reason=[pre_verdict.reason_code], disposition=None, task_id=None,
            acknowledged=False, action=None, outcome=None,
            escalation_id=f"esc:safety:{correlation_id}" if pre_verdict.decision == "HUMAN_REVIEW" else None,
            safety_decision=pre_verdict.decision, safety_reason_code=pre_verdict.reason_code,
        )

    # ── Brain: existing Bed Ops decision over canonical evidence ────────────
    decision = _decide(evidence)
    disposition = decision["disposition"]
    store.record_decision(correlation_id, disposition, decision["reason"])
    store.log_event(correlation_id, "decided", {
        "disposition": disposition, "inputs_used": decision["inputs_used"],
    })

    if safety_context is None:
        action_derivation = derive_pre_action(evidence, disposition)
        action_verdict = evaluate_safety(action_derivation.context)
        store.record_safety_decision(
            correlation_id, action_verdict,
            policy_version=action_derivation.policy_version,
            derived_facts=action_derivation.facts,
        )
        if action_verdict.decision != "ACT":
            store.log_event(correlation_id, "safety_blocked", {
                "decision": action_verdict.decision,
                "reason_code": action_verdict.reason_code,
                "policy_version": action_derivation.policy_version,
            })
            return LoopResult(
                correlation_id=correlation_id, accepted=False,
                blocked_reason=[action_verdict.reason_code], disposition=disposition, task_id=None,
                acknowledged=False, action=None, outcome=None, escalation_id=None,
                safety_decision=action_verdict.decision, safety_reason_code=action_verdict.reason_code,
            )

    idem = _idempotency_key(correlation_id, disposition)
    task_id = f"task:{idem}"

    # ── Coordination: durable task + separate receiver ACK ──────────────────
    store.create_task(task_id, correlation_id, kind="action", owner="bed_ops_worker", idempotency_key=idem)
    store.log_event(correlation_id, "task_created", {"task_id": task_id, "idempotency_key": idem})
    if require_external_ack:
        ack_derivation = derive_ack_state(evidence, store.get_task(task_id))
        ack_verdict = evaluate_safety(ack_derivation.context)
        store.record_safety_decision(
            correlation_id, ack_verdict,
            policy_version=ack_derivation.policy_version,
            derived_facts=ack_derivation.facts,
        )
        if ack_verdict.decision != "ACT":
            store.log_event(correlation_id, "waiting_for_ack", {
                "task_id": task_id, "reason_code": ack_verdict.reason_code,
            })
            return LoopResult(
                correlation_id=correlation_id, accepted=True, blocked_reason=[ack_verdict.reason_code],
                disposition=disposition, task_id=task_id, acknowledged=False, action=None,
                outcome=None, escalation_id=None, safety_decision=ack_verdict.decision,
                safety_reason_code=ack_verdict.reason_code,
            )
    if safety_context is not None and safety_context.receiver_acknowledged is False:
        ack_verdict = evaluate_safety(SafetyContext(
            ingested_at=evidence.ingested_at,
            receiver_acknowledged=False,
            current_stage="waiting_for_ack",
        ))
        store.record_safety_decision(
            correlation_id, ack_verdict,
            policy_version="internal-test-override.v1",
            derived_facts={"internal_test_override": True},
        )
        store.log_event(correlation_id, "waiting_for_ack", {
            "task_id": task_id, "reason_code": ack_verdict.reason_code,
        })
        return LoopResult(
            correlation_id=correlation_id, accepted=True, blocked_reason=[ack_verdict.reason_code],
            disposition=disposition, task_id=task_id, acknowledged=False, action=None,
            outcome=None, escalation_id=None, safety_decision=ack_verdict.decision,
            safety_reason_code=ack_verdict.reason_code,
        )
    acked = False if require_external_ack else acknowledge(store, task_id, correlation_id)
    # Replay: task already acknowledged on the first pass; durable state is the
    # source of truth, so treat an already-acknowledged task as owned.
    if not acked:
        task = store.get_task(task_id)
        acked = bool(task and task["status"] == "acknowledged")
    if safety_context is None:
        ack_derivation = derive_ack_state(evidence, store.get_task(task_id))
    else:
        task = store.get_task(task_id)
        ack_derivation = SafetyDerivation(
            context=SafetyContext(
                ingested_at=safety_context.ingested_at,
                receiver_acknowledged=bool(task and task["status"] == "acknowledged"),
                current_stage="ack_verification",
            ),
            facts={
                "internal_test_override": True,
                "receiver_acknowledged": {
                    "value": bool(task and task["status"] == "acknowledged"),
                    "source": "durable_store.tasks.status",
                },
            },
            policy_version="internal-test-override.v1",
        )
    ack_verdict = evaluate_safety(ack_derivation.context)
    store.record_safety_decision(
        correlation_id, ack_verdict,
        policy_version=ack_derivation.policy_version,
        derived_facts=ack_derivation.facts,
    )
    if ack_verdict.decision != "ACT":
        store.log_event(correlation_id, "waiting_for_ack", {
            "task_id": task_id, "reason_code": ack_verdict.reason_code,
        })
        return LoopResult(
            correlation_id=correlation_id, accepted=True, blocked_reason=[ack_verdict.reason_code],
            disposition=disposition, task_id=task_id, acknowledged=False, action=None,
            outcome=None, escalation_id=None, safety_decision=ack_verdict.decision,
            safety_reason_code=ack_verdict.reason_code,
        )

    # ── Hands + Brakes: idempotent execution with bounded retry/escalation ──
    action = execute_action(
        store=store, correlation_id=correlation_id, idempotency_key=idem,
        disposition=disposition, injection=injection, policy=policy, sleep=sleep,
    )

    # ── Nerves: verify outcome by re-reading durable state ──────────────────
    outcome = verify_outcome(
        store=store, correlation_id=correlation_id, idempotency_key=idem,
        intended_disposition=disposition, action=action,
    )

    return LoopResult(
        correlation_id=correlation_id, accepted=True, blocked_reason=None,
        disposition=disposition, task_id=task_id, acknowledged=acked,
        action=action, outcome=outcome, escalation_id=action.escalation_id,
        safety_decision="ACT", safety_reason_code="SAFETY_CHECKS_PASSED",
    )
