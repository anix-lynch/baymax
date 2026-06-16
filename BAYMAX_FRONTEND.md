# Baymax Frontend Map — READ THIS before touching the UI (for Codex)

> The backend docs (BAYMAX_WIRING / BACKEND_TODO / AUDIT) explain the organs.
> This explains the FRONT: which file is real, the one concept, and the data flow.

## The ONE concept (do not lose this)
The daughter says **one sentence** — "my mother's legs are swollen." That input
NEVER changes. What changes is **how deeply Baymax thinks**. Baymax has organs;
each organ is a **different data source** (cross-domain). As capability grows,
more organs fire and the reasoning stream gets longer.

```
ONE sentence ─▶ organs light up (each = a data SOURCE) ─▶ reasoning stream ─▶ answer
"ขาแม่บวม"      👁 vitals · 👂 ยา · 👃 ML signals ·        (grows longer        (2 voices:
                👅 lab · 🖐️ ops · 🧠 reason · ⚡ state      as belt rises)        doctor / family)
```
Belts (white→black) = capability LEVELS, NOT 7 different screens. Same input,
deeper reasoning. (The mockups dramatize this; the live front renders it from API.)

## File map — canonical vs reference vs dead
```
✅ CANONICAL — wire / improve THIS (the live product):
   ui/baymax/index.html       live reasoning theater  (you already polished it 👍)
   ui/baymax/baymax_live.js   the wiring: fetch /api/* → render organs + belts
   → deployed on Vercel at / and /baymax ; API base via ?api= / Cloud Run default

🔁 GITHUB BACKEND MIRROR — keep byte-identical to ui/baymax:
   backend/healthcare-ai-data-engineer/web/baymax/{index.html,baymax_live.js}
   → auditable backend slice committed inside Baymax

🔁 LOCAL SOURCE MIRROR — keep byte-identical while developing/deploying Cloud Run:
   sources/healthcare-ai-data-engineer/web/baymax/{index.html,baymax_live.js}
   → local sibling mirror; ignored by Baymax git because it is a nested repo

🎨 DESIGN REFERENCE ONLY — hardcoded mockups, NOT wired. Copy the STORY/visual rhythm, not the code:
   aikido_belts/baymax_belt_switcher.html      the 7-belt evolution on one input
   aikido_belts/0*/baymax_*belt*.html          per-belt theaters (white→black)

🗑️ DEAD — ignore (and safe to delete):
   baymax-engine/                               abandoned TS scaffold (backend is Python)
   ~/Downloads/baymax_switcher_*.html           a render snapshot outside the repo
```

## Data flow (how the live front actually works)
```
index.html ──loads──▶ baymax_live.js
  1. apiBase()         ?api= ▸ window.BAYMAX_API ▸ Cloud Run default
  2. loadEvidence()    parallel GET/POST {API}/api/*
  3. buildSteps()      converts endpoint payloads into one reasoning movie
  4. organ panel       lights up which data sources fired
  5. API down          renders explicit backend error, never silent blank
```
Contract: **each backend endpoint powers one step/organ in the same one-patient movie.**

## Belt → endpoint → status (front renders this; full contracts in BAYMAX_WIRING.md)
```
🥋 White  retrieval     GET /api/retrieve, /api/medications      ✅ live
🟡 Yellow nose          GET /api/signals  (5 FAERS ML signals)   ✅ live
🟡 Yellow state-diff    GET /api/state-diff (Stage 2→3)          ✅ live (stub data)
🟤 Brown  authority     POST /api/classify (human_review)        ✅ live
🧠 ask    grounded      GET /api/ask (needs Vertex)              🟡 partial
🟠 Orange workflow      GET /api/ops/bed, /api/lab-status        ✅ live
🟢 Green  tradeoff      POST /api/tradeoff                       ✅ live
🔵 Blue   objective     GET/POST /api/goal                       ✅ live
⬛ Black  outcome/traj  GET /api/outcome, /api/trajectory        ✅ live
⚡ Nerves status        GET /v1/cases/{correlation_id}/status    ✅ live
```

## What "done" looks like for the front (sample)
```
open  https://baymax-bice.vercel.app/
→ CoWork-style reasoning theater renders
→ organ rail lights up
→ stream shows retrieval, signals, state change, ACK/lab block, tradeoff,
  memory, authority, outcome, and case status from REAL API data
→ footer keeps the honest boundary: simulation, not clinician
```

## DON'T
- Don't invent a new front. `ui/baymax/` is canonical — improve it, don't fork it.
- Don't copy `aikido_belts/` code (hardcoded mockup) — copy its STORY/visual only.
- Don't wire anything to `baymax-engine/` (dead TS scaffold).
- Don't change a belt's response shape without updating baymax_live.js (front is coupled).
