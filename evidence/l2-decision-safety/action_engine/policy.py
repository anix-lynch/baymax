"""Versioned derivation of safety facts from trusted runtime state."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from action_engine.contract import CanonicalEvidence
from action_engine.safety import SafetyContext


POLICY_VERSION = "action-safety.v1"

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


def derive_pre_decision(evidence: CanonicalEvidence) -> SafetyDerivation:
    """Derive the facts available before the Brain chooses an action."""
    facts = {
        "freshness": {
            "value": evidence.ingested_at,
            "source": "canonical_evidence.ingested_at",
        },
        "required_evidence_complete": {
            "value": True,
            "source": f"validated_contract:{evidence.contract_version}",
        },
        "confidence": {
            "value": None,
            "source": "not_available_from_trusted_runtime",
        },
        "evidence_conflicts": {
            "value": [],
            "source": "not_available_from_trusted_runtime",
        },
        "caller_safety_overrides_used": False,
    }
    return SafetyDerivation(
        context=SafetyContext(
            ingested_at=evidence.ingested_at,
            required_evidence_complete=True,
            current_stage="pre_decision_safety_review",
        ),
        facts=facts,
    )


def derive_pre_action(evidence: CanonicalEvidence, disposition: str) -> SafetyDerivation:
    """Derive action risk and reversibility from versioned policy."""
    action_risk, reversible = ACTION_POLICY.get(disposition, ("high", False))
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
        "evidence_conflicts": {
            "value": [],
            "source": "not_available_from_trusted_runtime",
        },
        "caller_safety_overrides_used": False,
    }
    return SafetyDerivation(
        context=SafetyContext(
            ingested_at=evidence.ingested_at,
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
