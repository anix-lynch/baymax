# Baymax Constitution v1

## Purpose

This directory is the canonical architectural health record for Baymax as of
June 2026.

It is not a summary. It is not onboarding material. It is not marketing
content. It records what Baymax demonstrably does, what remains missing, where
the implementation contradicts its intended behavior, and what evidence is
required before findings may change.

Future agents, contributors, and AI systems must consult the relevant organ
record before changing Baymax behavior.

## Authority

These records have higher authority than stale README files, planning notes,
chat summaries, generated roadmaps, or presentation copy.

Runtime code and executable evidence remain the final source of truth. When
code contradicts a record, preserve the record's historical finding and append
a revision supported by proof. Never silently rewrite history to match the
latest implementation.

## Record Rules

1. Do not replace these records with summaries.
2. Do not remove or overwrite findings without executable evidence.
3. New audits append dated revisions rather than rewriting historical findings.
4. Every organ record maintains:
   - Current Grade
   - Existing Capabilities
   - Missing Capabilities
   - Contradictions
   - Evidence Map
   - Upgrade Path
   - Revision History
5. When context is limited, retrieve the relevant organ section. Never retrieve
   only an executive summary.
6. Operating instructions belong in `AGENTS.md`. Architectural diagnoses belong
   here. Do not merge the two.
7. Public claims may cite these records, but these records must not be weakened
   or rewritten to support marketing language.

## Organ Registry

| Organ | Layer | Responsibility | Canonical Record |
|---|---|---|---|
| Tongue | A | Meaning infrastructure | Pending |
| Eyes | B | Truth infrastructure | Pending |
| Nose | C | Signal and attention infrastructure | Pending |
| Brain | L2 | Procedural reasoning and decisions | `brain_audit.md` |
| Hands | L2 | Durable execution | Pending |
| Nerves | L2 | Runtime state awareness | `nerves_audit.md` |
| Immune | L2 | Self-verification and self-doubt | `immune_audit.md` |
| Heart | L2 | Care obligation and human relationship | `heart_audit.md` |
| Ethics | L2 | Authority, consent, safety, and truth | `ethics_audit.md` |
| Hospital | L3 | Human adoption and operations | Pending |

## Audit Status

| Audit | Status | Latest Record |
|---|---|---|
| Brain | COMPLETE | June 2026 |
| Nerves | COMPLETE | June 2026 |
| Immune | COMPLETE | June 2026 |
| Heart | COMPLETE | June 2026 |
| Ethics | COMPLETE | June 2026 |
| Eyes Deep Audit | PENDING | - |
| Nose Deep Audit | PENDING | - |
| Tongue Deep Audit | PENDING | - |
| Hands Deep Audit | PENDING | - |
| Hospital Adoption Audit | PENDING | - |

## Cross-Organ Truth

Baymax currently has strong task-specific procedural reasoning, durable action
receipts, bounded recovery, and unusually strong post-action verification.

Baymax is weaker at generalized reasoning, live state awareness, independent
derivation of safety facts, consent, compassionate disagreement, and verified
care follow-through.

The current highest-level contradiction is:

> Baymax can stop an unsafe action, but does not yet consistently stop every
> downstream plan, representation, or care claim produced from the same unsafe
> state.

## Revision Protocol

Append revisions using this shape:

```text
## Revision YYYY-MM-DD

Finding changed:
Previous state:
New evidence:
New state:
Remaining boundary:
```

Do not delete the previous finding.
