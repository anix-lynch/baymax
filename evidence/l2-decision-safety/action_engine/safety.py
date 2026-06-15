"""Reusable pre-recommendation and pre-action safety gate."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Literal


SafetyDecision = Literal["ACT", "ASK_FOR_INFO", "HUMAN_REVIEW", "WAIT_FOR_ACK", "SUPPRESS"]

CAPACITY_TTL_SECONDS = 15 * 60
MIN_RECOMMEND_CONFIDENCE = 0.55


@dataclass(frozen=True)
class SafetyContext:
    ingested_at: str | None
    required_evidence_complete: bool = True
    confidence_before: float | None = None
    confidence_after: float | None = None
    evidence_conflicts: list[str] = field(default_factory=list)
    action_risk: Literal["low", "medium", "high"] = "low"
    reversible: bool = True
    receiver_acknowledged: bool | None = None
    current_stage: str = "safety_review"


@dataclass(frozen=True)
class SafetyVerdict:
    decision: SafetyDecision
    reason_code: str
    blocking_reason: str | None
    next_expected_event: str
    confidence_before: float | None
    confidence_after: float | None
    current_stage: str


def _age_seconds(value: str | None, now: datetime) -> float | None:
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return (now - parsed.astimezone(timezone.utc)).total_seconds()


def evaluate_safety(
    context: SafetyContext,
    *,
    now: datetime | None = None,
    capacity_ttl_seconds: int = CAPACITY_TTL_SECONDS,
    min_confidence: float = MIN_RECOMMEND_CONFIDENCE,
) -> SafetyVerdict:
    """Return the strongest required stop condition, otherwise permit ACT."""
    now = now or datetime.now(timezone.utc)
    age = _age_seconds(context.ingested_at, now)

    if age is None:
        return SafetyVerdict(
            "ASK_FOR_INFO", "MISSING_OR_INVALID_EVIDENCE_TIMESTAMP",
            "Capacity evidence needs a valid freshness timestamp.",
            "fresh_capacity_received", context.confidence_before, context.confidence_after,
            context.current_stage,
        )
    if age < -60 or age > capacity_ttl_seconds:
        return SafetyVerdict(
            "SUPPRESS", "STALE_CAPACITY_STATE",
            f"Capacity evidence is stale ({max(0, int(age))} seconds old).",
            "fresh_capacity_received", context.confidence_before, context.confidence_after,
            context.current_stage,
        )
    if not context.required_evidence_complete:
        return SafetyVerdict(
            "ASK_FOR_INFO", "REQUIRED_EVIDENCE_MISSING",
            "Required evidence is incomplete.",
            "required_evidence_received", context.confidence_before, context.confidence_after,
            context.current_stage,
        )
    if context.evidence_conflicts and (context.action_risk == "high" or not context.reversible):
        return SafetyVerdict(
            "HUMAN_REVIEW", "HIGH_RISK_EVIDENCE_CONFLICT",
            "Conflicting evidence makes this action unsafe without human review.",
            "human_review_resolved", context.confidence_before, context.confidence_after,
            context.current_stage,
        )
    if context.confidence_after is not None and context.confidence_after < min_confidence:
        decision: SafetyDecision = "HUMAN_REVIEW" if context.evidence_conflicts else "ASK_FOR_INFO"
        code = "LOW_CONFIDENCE_CONFLICT" if context.evidence_conflicts else "LOW_CONFIDENCE"
        return SafetyVerdict(
            decision, code, "Confidence is below the direct-recommendation threshold.",
            "additional_evidence_received", context.confidence_before, context.confidence_after,
            context.current_stage,
        )
    if context.receiver_acknowledged is False:
        return SafetyVerdict(
            "WAIT_FOR_ACK", "RECEIVER_ACK_PENDING",
            "The receiver has not acknowledged ownership.",
            "task_acknowledged", context.confidence_before, context.confidence_after,
            context.current_stage,
        )
    return SafetyVerdict(
        "ACT", "SAFETY_CHECKS_PASSED", None, "action_succeeded",
        context.confidence_before, context.confidence_after, context.current_stage,
    )
