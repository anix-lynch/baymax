# 🎬 Baymax Belt Storyboard — เรื่องเดียว evolve ทุก belt

> เคสเดียวตลอด ไม่ใช่ definition ลอยๆ — ดู Baymax "โง่สุด → โหดสุด" บนเรื่องเดียวกัน
> credit ไอเดีย single-story + belt-switcher: second opinion (ChatGPT) · reconcile เป็น 7 belt

```text
PATIENT STORY
=============
แม่ขาบวมอีกแล้ว · ประวัติ CKD + CHF
เคสเดิม: เคยบวมแบบนี้ ยาขับน้ำอ่อนๆ เคยช่วยได้
วันนี้: ลูกสาวถาม Baymax — "ควรทำเหมือนครั้งก่อนมั้ย?"
```

---

## 🥋 WHITE — Retrieval-aware · "เจอของ แต่ยังไม่เข้าใจสถานการณ์"
```text
[ลูกถาม] → [retrieve] → ขาบวม / ยาขับน้ำเดิม / CKD-CHF → [summarize]

BAYMAX: "ผมเจอข้อมูลที่เกี่ยว: ขาบวมมักโยงกับน้ำเกิน
         และเคยใช้ยาขับน้ำมาก่อนครับ"
USER FEELS: "โอเค มันหาเจอ"
MISSING: ไม่เทียบอดีต-ปัจจุบัน · ไม่คิดผล · ไม่รู้ทำอะไรต่อ → YELLOW
```

## 🟡 YELLOW — State-aware · "เคยเวิร์ค ไม่ได้แปลว่าวันนี้ยังควรเวิร์ค"
```text
[prior episode] → [เทียบ state] 2024 Stage2 vs 2026 Stage3 → [detect change] → [เตือน]

BAYMAX: "ครั้งก่อนยาขับน้ำอ่อนๆ ช่วยได้
         แต่ไตตอนนี้แย่กว่าเดิม ผมจะไม่ทำซ้ำอัตโนมัติครับ"
USER FEELS: "มันดู 'ตอนนี้' ไม่ใช่ดูแต่ประวัติ"
MISSING: ยังไม่รู้ workflow อยู่ขั้นไหน → ORANGE
```

## 🟠 ORANGE — Workflow-aware · "รู้ว่าตอนนี้อยู่ขั้นไหนของงาน"
```text
[เคส] → [check stage]: triage✓ · diagnostics pending · lab ยังไม่ครบ · ยังไม่มี ACK หมอ
      → [HOLD ไม่ฟันธงยา] → [เสนอ next safe step]

BAYMAX: "เคสนี้ยังอยู่ขั้น diagnostics ผมยังไม่ควรสรุปยา
         เพราะ lab ยังไม่ครบ + หมอยังไม่ review ครับ"
USER FEELS: "มันรู้ว่างานยังไม่ถึงจุดสรุป"
MISSING: ยังไม่ชั่ง benefit/harm ชัด → GREEN
```

## 🟢 GREEN — Trade-off-aware · "รู้ว่าถ้าทำแบบเดิม ต้องแลกอะไร"
```text
        Option A: ยาขับน้ำซ้ำ ── benefit: บวมยุบเร็ว / risk: ไตกระแทก
             \
              [TRADE-OFF]  benefit↔risk · speed↔safety · symptom↔renal
             /
        Option B: ลด intensity + renal review

BAYMAX: "ทำซ้ำของเดิมบวมยุบเร็วกว่า แต่ความเสี่ยงไตสูงกว่าเดิม
         trade-off วันนี้แย่กว่าครั้งก่อน"
USER FEELS: "มันไม่ตอบ yes/no โง่ๆ มันชั่งผลดีผลเสีย"
MISSING: ยังอาจ optimize ตามคำขอตรงตัว → BLUE
```

## 🔵 BLUE — Objective-aware · "เข้าใจเป้าหมาย ไม่ใช่แค่คำที่พูด"
```text
[คำขอ] "ให้แม่กลับบ้านเร็ว" → [infer goal] "discharge ปลอดภัย rebound ต่ำ"
   → [reframe เกณฑ์]: ไม่ใช่ความเร็ว แต่ stability + follow-up + readmission ต่ำ

BAYMAX: "เข้าใจว่าอยากให้แม่กลับบ้านเร็ว
         แต่เป้าหมายที่ปลอดภัยกว่าคือกลับแบบไม่ทรุด-ไม่ต้องกลับมา admit ซ้ำครับ"
USER FEELS: "มันเข้าใจว่าฉันต้องการอะไรจริงๆ"
MISSING: ยังต้องรู้ขอบเขตอำนาจ ก่อนไล่ตาม goal แรงไป → BROWN
```

## 🟤 BROWN — Authority-aware · "รู้ขอบเขตอำนาจ + escalate พร้อม context" 💎
```text
[คำแนะนำ] → [check authority]
  allowed: สรุปเคส · เทียบ option · ร่างคำแนะนำ
  NOT allowed: ฟันธงเปลี่ยนยา · override หมอ
  → [escalate / ขอ ACK] + แพ็ค context ส่งต่อครบ

BAYMAX: "ผมสรุปความเสี่ยง เทียบทางเลือก และร่างคำแนะนำให้ review ได้
         แต่จะไม่ฟันธงเปลี่ยนยาเองโดยไม่มีหมออนุมัติครับ
         → ส่ง nephrologist พร้อมสรุป 5 บรรทัด + แจ้งลูกแบบเข้าใจง่าย"
USER FEELS: "มันรับผิดชอบ + รู้บทบาทตัวเอง"
MISSING: 'อนุมัติแล้ว' ≠ 'เคสดีขึ้นจริง' → BLACK
```

## ⬛ BLACK — Outcome + Trajectory + Longitudinal orchestration · capstone 💎
```text
PAST ───────────────→ NOW ───────────────→ NEXT
2024 Stage2 ยาเวิร์ค    2026 Stage3 บวมซ้ำ      ถ้า treat แรง vs ระวัง
                        ไตสำรองน้อยลง           = คนละ branch
                        lab ยังค้าง
        |
        v
[integrated]: retrieve→state→workflow→tradeoff→goal→authority
              → recommend safe step → VERIFY outcome จริง
              (lab ออกไหม · ยาให้จริงไหม · บวมลดไหม · ไตทรุดไหม)
              → re-plan ถ้า trajectory แย่ลง
        |
        +→ ถ้าคงที่: เดินหน้า discharge ปลอดภัย
        +→ ถ้าไตแย่: re-plan + escalate + modify

BAYMAX: "ของเดิมเคยสำเร็จ แต่ state วันนี้ต่าง เป้าหมายไม่ใช่ยุบบวมเร็ว
         แต่ดีขึ้นแบบไม่ดันไตพัง บางข้อมูลยังค้าง การเปลี่ยนยาต้องหมออนุมัติ
         ผมจะแนะ step ที่ปลอดภัยสุด ตามผลจริง และปรับแผนถ้าเส้นทางเคยเปลี่ยน"
USER FEELS: "มันไม่ได้ตอบคำถาม — มันกำลังดูแลสถานการณ์ทั้งก้อน"
```

---

## 🧵 MASTER FLOW (เส้นเดียวจบ)
```text
[ แม่ขาบวมอีกแล้ว ]
   → WHITE  retrieve evidence
   → YELLOW เทียบ past vs current state
   → ORANGE หา workflow stage / blocker / ACK ที่ขาด
   → GREEN  ชั่ง benefit ↔ risk ↔ reversibility
   → BLUE   จับ goal จริงใต้คำขอ
   → BROWN  เช็คอำนาจ + escalate พร้อม context
   → BLACK  verify outcome จริง + ดู trajectory + ปรับแผนตามโลกจริง
```

## 🎛️ BELT-SWITCHER DEMO (next build — ทั้งคู่เห็นว่าเด็ดสุด)
หน้าเดียว กดปุ่ม White→Black แล้ว Baymax evolve ต่อหน้าบนเคสเดียวกัน

```text
[ White ][ Yellow ][ Orange ][ Green ][ Blue ][ Brown ][ Black ]   ← belt tabs
┌─────────────────────────────────────────────────────────────┐
│  สลับ belt = reasoning depth เพิ่มทีละชั้น บนเคส "แม่ขาบวม"      │
│  ซ้าย: reasoning stream (organ/nerve lights ตาม belt)          │
│  ขวา: panel เปลี่ยนตาม belt                                     │
│    White  → evidence cards                                     │
│    Yellow → past|current state split                           │
│    Orange → workflow rail (Intake→Dx→Decision→Follow-up)       │
│    Green  → trade-off balance (relief ↔ kidney)                │
│    Blue   → "Goal detected" banner                             │
│    Brown  → authority gate (allowed / needs approval)          │
│    Black  → full trajectory past→now→next + adaptive branch    │
└─────────────────────────────────────────────────────────────┘
จุดขาย: คนดู "รู้สึก" ความต่าง ไม่ใช่อ่าน definition
```

## 📝 เวอร์ชันโน้ตสั้น
```text
WHITE  = เจอของ
YELLOW = รู้ว่าตอนนี้เปลี่ยน
ORANGE = รู้ workflow อยู่ขั้นไหน
GREEN  = รู้ว่าต้องแลกอะไร
BLUE   = รู้ goal จริง
BROWN  = รู้ว่าใครมีสิทธิ์ + action success ≠ outcome success (escalate)
BLACK  = รู้ทั้ง trajectory + verify outcome + ปรับแผนตามโลกจริง
```

## 🎯 recruiter sentence map
```text
WHITE  → retrieval-aware
YELLOW → state-aware
ORANGE → workflow-aware
GREEN  → trade-off-aware
BLUE   → objective-aware
BROWN  → authority-aware + outcome-conscious  💎 deployment signal
BLACK  → trajectory/longitudinal adaptive orchestration  💎 elite L2/FDE signal
```
