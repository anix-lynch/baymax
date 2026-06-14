# Baymax Integration Audit

Human/automation ratio: `5% | 95%`

## Goal

Give a recruiter one repository and one command that proves the Baymax flow:

`nose -> two eyes -> decision change -> brakes -> nerves/hands -> verification`

## Source Repositories

- Left eye: `healthcare-ai-data-engineer` — 55,500 synthetic encounters.
- Right eye: `healthcare-da` + `healthcare-signal-platform` — real openFDA lineage,
  5,000-report evidence corpus, and five evaluated attention signals.
- Body: `healthcare-genai-engineer` — triage, Bed Ops decision, durable action,
  receiver ACK, retry, and outcome verification.

## Done When

- [x] One command syncs public sibling sources.
- [x] NOSE runs before both eyes and can stop a low-value case.
- [x] Left eye scans the full 55,500-row synthetic encounter corpus.
- [x] Right eye scans 5,000 real openFDA reports.
- [x] Every organ records its exact sibling commit and source artifact.
- [x] Brain selects triage and Bed Ops disposition.
- [x] Cross-domain evidence changes action policy on the same case.
- [x] Mouth explains the decision without overstating openFDA causality.
- [x] Brakes stop autonomous action and Nerves hand off to human review.
- [x] Hands produce durable before/after state and receiver ACK.
- [x] Outcome verifier re-reads durable state.
- [x] Immune tests defend skip, decision-change, and full closed-loop paths.
- [x] CI regenerates one recruiter-readable audit receipt.

## Proof Boundary

This proves a closed-loop **simulation**. It does not claim a deployed hospital
workflow, clinician-validated decisions, or a real Bed Ops system integration.
