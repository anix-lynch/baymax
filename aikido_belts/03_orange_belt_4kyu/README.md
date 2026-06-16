# 🟠 Orange · 4kyu — Workflow-aware  "รู้ว่าเคสอยู่ขั้นไหน + verify จริง"

> belt นี้มาจาก second opinion (ChatGPT) ที่ deep research ผมตกไป + insight ของ Bchan เรื่อง booking-hands & ACK
> **Workflow-aware ↔ ACK/action layer ↔ boring-tray/god-mode (tool zones) ↔ harness wiring = เรื่องเดียวกันคนละมุม**

**นิยาม:** รู้ว่าเคสอยู่ stage ไหน, อะไร pending, รอ ACK ใคร, precondition ครบยัง — **ไม่ commit ก่อนถึงจุดที่ถูกต้อง** และ **ไม่เชื่อคำว่า "ส่งแล้ว" จนกว่าจะ verify**

## 🤚 มือ 2 ข้างของ Baymax (insight Bchan)
```text
🤚 ซ้าย = ER triage      : ประเมินด่วน/ไม่ด่วน → route track ที่ถูก
🤚 ขวา = care-ops booking : non-urgent → ขอ room ให้แม่
```

## ⚡ ACK verify (หัวใจของ belt นี้)
```text
nurse บอก "ส่งไป care ops แล้ว"
   → Baymax ไม่เชื่อคำพูด → query ระบบ: room ลงทะเบียนชื่อแม่จริงไหม?
   → ยัง = ยังไม่ ACK → ตามต่อ ไม่ mark done
"lab ออกอีก 2 วันค่อย consult ได้"
   → precondition + temporal gate → HOLD + เตือนล่วงหน้า ไม่ฟันธงก่อน lab ครบ
```

## 🚦 workflow rail
```text
Intake ✓ → Triage ✓ → Room ⏳(ยังไม่ confirm) → Diagnostics ⏳(lab 2 วัน) → Decision 🔒 → Follow-up
                              ^ ACK verify              ^ temporal gate        ^ HOLD ไม่ commit
```

## 🔌 ผูกกับ action layer / tool zones (preview ของ Brown)
```text
booking/consult/notify = "มือ" ที่ register เป็น tools → มี 3 โซน:
  🟢 boring tray (auto)  · 🟡 ต้อง approve · 🔴 ห้าม
belt นี้โชว์ "มือทำงาน + verify" — Brown belt จะ formalize เป็น Authority Spec (ดู AUTHORITY_SPEC.md)
```

**ทำได้วันนี้?** ✅ — state machine + precondition gates + ACK polling (OpenAI Agent Builder, agent frameworks)
**Grounding:** OpenAI agent workflows (approvals/triggers/state), production agent guides 2026
**Hiring signal:** สูง (L2 + FDE) — "งานจริงมีลำดับ + verify ผลจริง ไม่ใช่ตอบทันที"
**HTML demo:** `baymax_orange_belt_workflow.html`
**→ next 🟢 Green:** เมื่อ Baymax เริ่มชั่ง benefit/risk ของแต่ละทางเลือกชัดๆ
