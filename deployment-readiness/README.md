# Simulated Deployment Readiness

This thin package proves that Baymax has an acceptance contract, bounded rollout
stages, rollback rules, and an ownership handoff. It does **not** claim a
hospital deployment, clinical validation, live users, or adoption.

```bash
make readiness
```

The verifier reads the live Baymax audit receipt, checks five release gates,
then corrupts a copy of the receipt to simulate false success. A release is
eligible for simulated shadow only when the normal receipt passes and the
corrupted receipt triggers `rollback_required`.

```text
offline replay
-> simulated shadow
-> supervised sandbox
-> never production or hospital adoption
```

Source contract: `deployment-readiness/contract.json`  
Machine-readable result: `outputs/deployment_readiness_receipt.json`
