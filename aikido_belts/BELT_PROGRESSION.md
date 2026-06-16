# 🥋 Baymax Dojo — สายขาว → สายดำ (reconciled v2)

> v2 = รวม deep research ของผม + second opinion (ChatGPT) แล้ว reconcile
> หลัก: **1 capability / 1 belt** · เรื่อง demo เดียวตลอด = "แม่ขาบวม" · ดู `STORYBOARD.md`

```text
🥋 01 WHITE  Retrieval-aware    "หาเจอ"                    ✅ done   baseline
🟡 02 YELLOW State-aware        "รู้ว่าตอนนี้ต่างจากเดิม"   ✅ done   (demo preview trade-off ด้วย)
🟠 03 ORANGE Workflow-aware     "รู้ว่าเคสอยู่ขั้นไหน"      ⬜       ← เพิ่มจาก second opinion
🟢 04 GREEN  Trade-off-aware    "รู้ว่าต้องแลกอะไร"         ⬜       (+counterfactual-lite)
🔵 05 BLUE   Objective-aware    "รู้ goal จริง ไม่ใช่คำขอ"  ⬜       (+preference รองจาก safety)
🟤 06 BROWN  Authority-aware    "รู้ว่าใครมีสิทธิ์ + escalate" ⬜    💎 MONEY BELT (FDE)
⬛ 07 BLACK  Trajectory+Outcome+Longitudinal adaptive orchestration ⬜  💎 capstone
```

## ทำไมเรียงแบบนี้ (จุดที่ reconcile)
```text
• Workflow (Orange) = ของที่ second opinion จับได้ ผมตกไป → ใส่กลับ
• Authority (Brown) เลื่อนขึ้นเกือบบนสุด — ไม่ใช่กลางๆ
  เหตุผล: Gartner 2026 บอก 38% ของ AI agent projects ถูกถอย
  เกือบทั้งหมดเพราะ "escalation logic ห่วย" → นี่คือ deployment make-or-break
• Black = capstone ที่รวม outcome-verification + trajectory + longitudinal
  (ของผม Black=outcome, ของเขา Black=trajectory → รวมเป็นอันเดียว ถูกทั้งคู่)
• care/preference ไม่ได้กิน belt เดี่ยว — เป็น flavor ที่รองจาก safety/authority
```

## ความรู้สึก user (3 ระดับ) แมปกับ belt
```text
"เข้าใจสถานการณ์ ไม่ใช่แค่ query"   → White→Yellow→Black (state+trajectory+longitudinal)
"เข้าใจผลที่ตามมา ไม่ใช่แค่คำสั่ง"  → Green+Brown+Black (tradeoff+authority+outcome)
"เข้าใจเป้าหมายฉัน ไม่ใช่แค่ที่ขอ"  → Blue (objective, +preference)
```

## Build order ที่แนะ (ROI สัมภาษณ์ สูง→ต่ำ)
```text
1. 🟤 Brown authority/escalation  ← ทำก่อน คนทำน้อย ต่างทันที (FDE money shot)
2. 🟠 Orange workflow stage/ACK    ← ต่อ state เดิมง่าย
3. 🟢 Green trade-off (มีอยู่ใน yellow แล้ว แยกให้ชัด)
4. 🔵 Blue objective reframing
5. ⬛ Black capstone: outcome loop + trajectory + belt-switcher demo
```

## โครงสร้างโฟลเดอร์
```text
aikido_belts/
├── BELT_PROGRESSION.md        ← ไฟล์นี้ (master map v2)
├── CAPABILITY_LADDER.md       ← deep research + reconciliation note
├── STORYBOARD.md              ← เรื่องเดียว evolve ทุก belt + belt-switcher spec
├── 01_white_belt_6kyu/   ✅ Retrieval  (html + README)
├── 02_yellow_belt_5kyu/  ✅ State      (html + README)
├── 03_orange_belt_4kyu/  ⬜ Workflow   (README)
├── 04_green_belt_3kyu/   ⬜ Trade-off  (README)
├── 05_blue_belt_2kyu/    ⬜ Objective  (README)
├── 06_brown_belt_1kyu/   ⬜ Authority  (README) 💎
└── 07_black_belt_1dan/   ⬜ Capstone   (README) 💎
```
ถึงสายดำ = Baymax deploy ขึ้น Vercel แบบหมอใช้จริงได้ 🤍

---

## 🌀 ANTICIPATION-AWARE (cross-cutting trait — ไม่ใช่ belt rung)
> "Perplexity instinct" — รู้คำถามถัดไปที่ useful ก่อน user ถาม + เสนอทำให้เลย

```text
เปิดเมื่อมี : Blue (objective) + Black (trajectory) → Baymax เดา adjacent needs ออก
demo 2 ชั้น :
  READ layer : likely next questions · "people in similar situations also needed" · related actions
  HAND layer : "I can check consult status / calendar / insurance now" (boring tray)
= ANTICIPATE ขั้นแรกของ core loop (anticipate→prepare→act→verify)
⚠ ถ้าหยุดที่ anticipate เฉยๆ = "perfect city" ฉลาดพูดแต่ไม่ยกของ → ต้องมี HAND layer ด้วย
```

## 🦴 HARNESS + AUTHORITY (โครงเหล็ก ไม่ใช่แค่สายรัดพุง)
```text
Agent = Model + Harness · ~98.4% ของ agent จริง = harness infra (ดู HARNESS_SPEC.md)
harness บังคับ belt ชั้นสูงให้เป็นจริง (lock ที่ระบบ ไม่ใช่ขอจาก model):
  🟠 Orange Workflow → precondition/temporal gate + ACK verify
  🟤 Brown Authority → 3 tool zones (🟢 boring tray / 🟡 approve / 🔴 ห้าม) + PreToolUse hook
  ⬛ Black Outcome   → PostToolUse verify + eval harness

ACK = action layer = boring-tray/god-mode = harness wiring → เรื่องเดียวกันคนละมุม
Authority Spec (Can do / Can prepare / Cannot do) → AUTHORITY_SPEC.md
```

## 🗂️ FILE INDEX (อัปเดต)
```text
BELT_PROGRESSION.md   master map (v3)
CAPABILITY_LADDER.md  deep research + reconciliation
STORYBOARD.md         เคสเดียว evolve ทุก belt + belt-switcher spec
HARNESS_SPEC.md       4-field harness (data/tools/sandbox/policy) + lock points + SDK decision
AUTHORITY_SPEC.md     boring-tray/god-mode/forbidden + ตัวอย่างคำพูด
01_white  ✅ html+README   Retrieval
02_yellow ✅ html+README   State (+trade-off preview)
03_orange ✅ html+README   Workflow (มือ+ACK+gate+anticipate)  ← เพิ่งทำ
04_green  ⬜ README         Trade-off
05_blue   ⬜ README         Objective
06_brown  ⬜ README         Authority 💎 (ดู AUTHORITY_SPEC.md)
07_black  ⬜ README         Capstone 💎
```
