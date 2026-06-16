# Baymax Wiring Map — mockup UI ↔ Codex FastAPI backend

> Connects the belt-switcher mockup (organs/belts) to the real endpoints in
> `sources/healthcare-ai-data-engineer/api/app/main.py`.
> Status: ✅ wired today · 🟡 partial · 🚧 gap (Codex must build).

API base (local): `http://localhost:8000` · served UI mount: `/ui`

---

## Organ → data source → endpoint

```text
ORGAN            SOURCE/DOMAIN        ENDPOINT                         STATUS
👁 ตาซ้าย         อาการ/vitals         (classify input vitals)          🟡 input only
👁 ตาขวา         ยา (pharmacy)        GET /api/medications             ✅
👂 หู             ประวัติ+เคสเก่า (EHR) GET /api/retrieve?q= , /search   ✅
👅 ลิ้น            ค่า lab              GET /api/encounters (Test Results) 🟡 no live lab ETA
👃 จมูก           5 ML signals (FAERS)  GET /api/signals                 ✅ WIRED
🖐️ มือ            จองเตียง/ops         —                                🚧 GAP
🧠 สมอง           reasoning            GET /api/ask?q= (grounded+cite)  ✅
⚡ เส้นประสาท      state วันนี้          GET /api/classify (acuity only)  🟡 no state-diff
❤️ หัวใจ           authority/ethics     POST /api/classify (human_review)✅
🔭 ตาไกล          trajectory           —                                🚧 GAP
```

---

## Belt → endpoint(s) → status

### 🥋 White · Retrieval ✅ WIRED
- `GET /api/retrieve?q={complaint}&k=5` → `{results:[{rank,score,age,gender,medical_condition,chief_complaint,esi_tier_truth,snippet}]}`
- `GET /api/medications`, `GET /api/conditions`, `GET /api/search?q=` → chips
- Baymax says: "ผมหาเจอ — ขาบวม + เคสคล้าย {n} ราย"

### 🟡 Yellow · State 🟡 PARTIAL (nose wired, state-diff left)
- 👃 nose: ✅ **WIRED** — `GET /api/signals` serves 5 evaluated openFDA signals
  (anomaly·cluster·classify·rank·retrieval) + cost/quality router from
  `healthcare-signal-platform` proof. classify F1=0.877, router cuts 30% LLM
  calls at ≥0.95 serious-recall (real FAERS, n=5000).
- ⚡ state-diff: 🚧 **GAP** — no longitudinal compare (Stage 2→3) yet.
- have: `POST /api/classify` gives current acuity (esi_tier) = a slice of "now".

### 🟠 Orange · Workflow 🚧 mostly GAP
- 👅 lab ETA / 🖐️ bed-ACK: **GAP** — no ops/scheduling endpoint, no ACK check.

### 🟢 Green · Trade-off 🚧 GAP
- No options/trade-off endpoint. (Reasoning could be derived in `/api/ask` prompt later.)

### 🔵 Blue · Objective 🚧 GAP
- No goal/preference memory endpoint.

### 🟤 Brown · Authority ✅ WIRED (the strong one)
- `POST /api/classify` → `{esi_tier, rules_fired:[{id,rule,action}], confidence, human_review_required}`
- `human_review_required=true` + `rules_fired` = real authority-aware escalation signal.
- `GET /api/trust-room` → governance/trust payload.

### ⬛ Black · Capstone 🚧 GAP
- No outcome-verify / trajectory endpoint.

---

## Gap contracts (what Codex should build next, in priority order)

```text
1. 👃 GET /api/signals  ✅ DONE — serves 5 evaluated FAERS signals + router
   (api/app/signals.py reads the signal-platform proof). Yellow nose UNLOCKED.

2. ⚡ GET /api/state-diff?patient_id=   → {past:{date,ckd_stage,...}, now:{...}, changed:[...]}
   longitudinal compare. Unlocks Yellow state-diff (the iconic "Stage 2→3" moment).

3. 🖐️ GET /api/ops/bed?patient_id=     → {requested, registered, nurse_said_sent}
   + verify. Unlocks Orange ACK ("ส่งแล้ว ≠ ลงทะเบียนจริง").

4. ⚖️ POST /api/tradeoff               → {options:[{id,benefit,risk,reversible}], recommend}
   Unlocks Green.

5. 🔍 GET /api/outcome?action_id=       → {stage:'sent|accepted|scheduled|verified', open}
   Unlocks Black verify.
```

---

## Frontend wiring
- Live front: `sources/healthcare-ai-data-engineer/web/baymax/` (served at `/ui/baymax/`).
- `baymax_live.js` calls real endpoints for ✅ belts, shows 🚧 "backend gap" badges on the rest.
- `API_BASE` configurable; graceful fallback to mock when API is offline.
- Same single input "ขาแม่บวมค่ะ" → mapped to a clinical complaint string for the API.
