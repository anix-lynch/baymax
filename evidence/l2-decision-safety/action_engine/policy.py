"""Versioned derivation of safety facts from trusted runtime state."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from action_engine.contract import CanonicalEvidence
from action_engine.safety import SafetyContext


POLICY_VERSION = "action-safety.v2"

# Risk is policy, not caller opinion. Changing this table requires a version bump.
ACTION_POLICY: dict[str, tuple[str, bool]] = {
    "assign_bed": ("medium", True),
    "board_ed": ("medium", True),
    "hold_observation": ("medium", True),
    "divert": ("high", False),
    "discharge_plan": ("high", True),
}


@dataclass(frozen=True)
class SafetyDerivation:
    context: SafetyContext
    facts: dict[str, Any]
    policy_version: str = POLICY_VERSION


def _operational_assessment(evidence: CanonicalEvidence) -> tuple[float, list[str], dict[str, Any]]:
    """Derive evidence sufficiency and contradictions from canonical facts.

    This is not model-confidence calibration. It is a deterministic measure of
    whether the operational evidence needed by Bed Ops is present and
    internally consistent.
    """
    state = evidence.er_state
    fields = {
        "available_beds": state.available_beds,
        "occupancy_pct": state.occupancy_pct,
        "queue_length": state.queue_length,
    }
    present = [name for name, value in fields.items() if value is not None]
    completeness = len(present) / len(fields)

    conflicts: list[str] = []
    saturated = (
        (state.available_beds is not None and state.available_beds <= 0)
        or (state.occupancy_pct is not None and state.occupancy_pct >= 95)
        or (state.queue_length is not None and state.queue_length >= 8)
    )
    ample_capacity = (
        state.available_beds is not None
        and state.available_beds >= 5
        and state.occupancy_pct is not None
        and state.occupancy_pct < 70
        and state.queue_length is not None
        and state.queue_length < 3
    )
    if evidence.bed_pressure_risk == "low" and saturated:
        conflicts.append("bed_pressure_low_vs_saturated_capacity")
    if evidence.bed_pressure_risk == "high" and ample_capacity:
        conflicts.append("bed_pressure_high_vs_ample_capacity")

    if completeness == 1.0:
        confidence = 0.9
    elif completeness >= 2 / 3:
        confidence = 0.7
    else:
        confidence = 0.4
    if conflicts:
        confidence = min(confidence, 0.65)

    facts = {
        "evidence_sufficiency_confidence": {
            "value": confidence,
            "source": f"{POLICY_VERSION}.operational_evidence_sufficiency",
            "calibrated_model_confidence": False,
        },
        "capacity_field_completeness": {
            "value": round(completeness, 3),
            "present_fields": present,
            "source": "canonical_evidence.er_state",
        },
        "evidence_conflicts": {
            "value": conflicts,
            "source": f"{POLICY_VERSION}.capacity_consistency_rules",
        },
    }
    return confidence, conflicts, facts


def derive_pre_decision(evidence: CanonicalEvidence) -> SafetyDerivation:
    """Derive the facts available before the Brain chooses an action."""
    confidence, conflicts, assessment_facts = _operational_assessment(evidence)
    facts = {
        "freshness": {
            "value": evidence.ingested_at,
            "source": "canonical_evidence.ingested_at",
        },
        "required_evidence_complete": {
            "value": True,
            "source": f"validated_contract:{evidence.contract_version}",
        },
        **assessment_facts,
        "caller_safety_overrides_used": False,
    }
    return SafetyDerivation(
        context=SafetyContext(
            ingested_at=evidence.ingested_at,
            required_evidence_complete=True,
            confidence_after=confidence,
            evidence_conflicts=conflicts,
            current_stage="pre_decision_safety_review",
        ),
        facts=facts,
    )


def derive_pre_action(evidence: CanonicalEvidence, disposition: str) -> SafetyDerivation:
    """Derive action risk and reversibility from versioned policy."""
    action_risk, reversible = ACTION_POLICY.get(disposition, ("high", False))
    confidence, conflicts, assessment_facts = _operational_assessment(evidence)
    facts = {
        "freshness": {
            "value": evidence.ingested_at,
            "source": "canonical_evidence.ingested_at",
        },
        "action_risk": {
            "value": action_risk,
            "source": f"{POLICY_VERSION}.ACTION_POLICY[{disposition}]",
        },
        "reversible": {
            "value": reversible,
            "source": f"{POLICY_VERSION}.ACTION_POLICY[{disposition}]",
        },
        **assessment_facts,
        "caller_safety_overrides_used": False,
    }
    return SafetyDerivation(
        context=SafetyContext(
            ingested_at=evidence.ingested_at,
            confidence_after=confidence,
            evidence_conflicts=conflicts,
            action_risk=action_risk,
            reversible=reversible,
            current_stage="pre_action_safety_review",
        ),
        facts=facts,
    )


def derive_ack_state(evidence: CanonicalEvidence, task: dict[str, Any] | None) -> SafetyDerivation:
    """Derive receiver ACK from the durable task row, never from the request."""
    acknowledged = bool(task and task["status"] == "acknowledged")
    facts = {
        "freshness": {
            "value": evidence.ingested_at,
            "source": "canonical_evidence.ingested_at",
        },
        "receiver_acknowledged": {
            "value": acknowledged,
            "source": "durable_store.tasks.status",
        },
        "task_id": task["task_id"] if task else None,
        "caller_safety_overrides_used": False,
    }
    return SafetyDerivation(
        context=SafetyContext(
            ingested_at=evidence.ingested_at,
            receiver_acknowledged=acknowledged,
            current_stage="ack_verification",
        ),
        facts=facts,
    )
