"""Versioned, evaluated pre-retrieval attention signal for Baymax cases."""
from __future__ import annotations

import csv
import subprocess
import sys
from functools import lru_cache
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
BODY_REPO = ROOT / "sources" / "healthcare-genai-engineer"
LABELLED_CASES = BODY_REPO / "data" / "raw" / "healthcare_dataset.csv"

SIGNAL_NAME = "esi-attention-router.v1"
ROUTE_MAX_ESI = 3
SERIOUS_MAX_ESI = 2


def _commit(path: Path) -> str:
    return subprocess.check_output(
        ["git", "-C", str(path), "rev-parse", "HEAD"], text=True
    ).strip()


@lru_cache(maxsize=1)
def _classifier() -> Callable[[str], tuple[int, list[str]]]:
    body = str(BODY_REPO)
    if body not in sys.path:
        sys.path.insert(0, body)
    from workflows.classify_esi import rule_based_esi

    return rule_based_esi


@lru_cache(maxsize=1)
def evaluate_signal_contract() -> dict[str, Any]:
    """Measure routing reduction and serious-case recall on labelled cases."""
    classify = _classifier()
    labelled = routed = serious = serious_routed = 0
    with LABELLED_CASES.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            truth = (row.get("esi_tier_truth") or "").strip()
            if not truth:
                continue
            query = f"{row.get('chief_complaint', '')} {row.get('hpi', '')}".strip()
            tier, _ = classify(query)
            should_route = tier <= ROUTE_MAX_ESI
            is_serious = int(truth) <= SERIOUS_MAX_ESI
            labelled += 1
            routed += int(should_route)
            serious += int(is_serious)
            serious_routed += int(should_route and is_serious)

    return {
        "labelled_cases": labelled,
        "serious_cases": serious,
        "routed_cases": routed,
        "routed_fraction": round(routed / labelled, 4),
        "expensive_path_reduction_pct": round((1 - routed / labelled) * 100, 2),
        "serious_case_recall": round(serious_routed / serious, 4),
        "route_rule": f"route when deterministic pre-retrieval ESI <= {ROUTE_MAX_ESI}",
        "serious_definition": f"labelled ESI <= {SERIOUS_MAX_ESI}",
        "evaluation_artifact": str(LABELLED_CASES.relative_to(ROOT)),
    }


def route_signal(query: str) -> dict[str, Any]:
    """Return one served attention decision before either expensive eye opens."""
    tier, flags = _classifier()(query)
    metrics = evaluate_signal_contract()
    route_to_eyes = tier <= ROUTE_MAX_ESI
    commit = _commit(BODY_REPO)
    return {
        "route_to_eyes": route_to_eyes,
        "signal_version": f"{SIGNAL_NAME}@{commit[:12]}",
        "route_reason": (
            f"served deterministic ESI attention tier {tier} routes to expensive eyes"
            if route_to_eyes
            else f"served deterministic ESI attention tier {tier} skips expensive eyes"
        ),
        "priority_tier": tier,
        "priority_score": round((6 - tier) / 5, 2),
        "signal_flags": flags,
        "decided_by": "served_signal",
        "evaluation": metrics,
        "served_source_repo": "healthcare-genai-engineer",
        "served_source_commit": commit,
        "served_source_artifact": str(
            (BODY_REPO / "workflows" / "classify_esi.py").relative_to(ROOT)
        ),
    }
