# Baymax — finish the recruiter showroom

Owner: Intel Claude or Codex
Source machine: `Anixs-Mac-mini.local`
Repo: `~/dev/baymax`
Branch: `codex/baymax-integration`
Checkpoint commit: `ce8d25c feat: add Baymax live story surface`

## Mission

Finish Baymax as one recruiter-auditable public showroom repo.

Do not build more organs. The brain already works. Finish the movie, inspect the
real surface, remove anything that weakens the story, and prepare the repo for a
public GitHub push.

## What already works

```text
Incoming case
→ Nose allocates attention
→ Patient + drug/capacity perspectives add evidence
→ Brain changes action when perspective changes
→ Brakes stop uncertain autonomous action
→ Nerves hand off and record ACK
→ Hands change durable state when allowed
→ Immune tests pin the outcomes
```

Recruiter movie:

1. Attention Flip: routine refill stops before expensive eyes.
2. Decision Flip: same critical patient, free bed `assign_bed` → gridlock `divert`.
3. Brake Save: patient-only `discharge_plan` → drug-safety evidence → `human_review`.

Live UI:

```bash
cd ~/dev/baymax
make sync
make audit
make ui
```

Open `http://localhost:8000/ui/`.

Current proof:

- `6 passed`
- clean-room source sync passed
- desktop and 390px mobile visually verified
- all three UI scenes end with `ตรวจซ้ำแล้ว`
- hero GIF generated from the truthful Decision Flip UI
- secret scan passed
- no Warfarin interaction fantasy or clinical diagnosis claim

## Finish line

```text
Baymax showroom
├── ✅ one repo, sibling sources synced at audit time
├── ✅ three memorable golden cases
├── ✅ live personality UI bound to audit receipt
├── ✅ README hero GIF
├── ⏳ independent Intel visual/simplicity review
├── ⏳ final public diff review
└── 🎯 publish only after Bchan clearly intends public push
```

## Execute

1. Confirm commit `ce8d25c` exists locally and worktree is clean.
2. Run `make sync && make test && make audit`.
3. Run `make ui`; inspect all three tabs on desktop and mobile.
4. Treat any visible red, console error, false receipt, overflow, or awkward
   recruiter story as unfinished. Fix it.
5. Run simplicity review, secret scrub, and showroom/bragable gate.
6. Keep scope lean. Prefer deleting confusion over adding features.
7. Prepare final public review:
   - files/commits to publish
   - strongest honest claim
   - claims still unsafe
   - exact GitHub repo/title/description
8. Do not invent hospital integration, clinician validation, diagnosis,
   causality, or drug-interaction proof.
9. Do not push publicly unless Bchan's current instruction clearly means publish.

## Truth boundary

Baymax is a closed-loop ER simulation. Durable actions use simulated Bed Ops
state. openFDA is a population safety signal, not proof of causality or a drug
interaction. The Decision Flip changes an operational action, not diagnosis.

## One-line test

> Recruiter should remember Baymax changed its mind, stopped itself, and checked
> that work really happened — not remember how many files it has.
