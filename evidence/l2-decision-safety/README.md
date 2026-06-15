# L2 Decision Safety Evidence Pack

This tracked evidence pack makes every Python file cited by the Baymax Brain, Nerves, Immune, Heart, and Ethics audits reviewable from the Baymax showroom repository.

## Ownership

- Canonical implementation: [healthcare-genai-engineer](https://github.com/anix-lynch/healthcare-genai-engineer)
- Recruiter-visible evidence copy: this directory
- Integrity manifest: `SHA256SUMS`

The evidence copy is not a second runtime source of truth. Changes must be made in the canonical L2 repository and then mirrored here.

## Included Proof

- Procedural reasoning and evidence arbitration
- Decision Safety Envelope
- Versioned action-risk and reversibility policy
- Durable ACK-derived safety facts with provenance receipts
- Public API regression proof preventing caller safety self-certification
- Durable action, ACK, retry, and outcome verification
- Bed and capacity routing
- Recommendation and guardrail behavior
- API schemas and action/status routes
- Relevant tests and evaluation output

## Verify

From the Baymax repository root:

```bash
(cd evidence/l2-decision-safety && shasum -a 256 -c SHA256SUMS)
python -m compileall -q evidence/l2-decision-safety
```
