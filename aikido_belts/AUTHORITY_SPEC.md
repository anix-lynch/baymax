# 🛡️ Baymax Authority Spec v1 — "What is Baymax allowed to actually do?"

> คำถามจริงของทุก agent product ปี 2026 · นี่คือ tool-zone harness wiring (ผูกกับ HARNESS_SPEC.md + 🟤 Brown belt)
> หลัก: **God mode ≠ ทำอะไรก็ได้ — แต่ = เต็มที่ "ใน lane ตัวเอง"** (care orchestrator/explainer/coordinator, ไม่ใช่ deciding doctor)

## 📊 3 ช่อง (Can do / Can prepare / Cannot do)
```text
🟢 CAN DO (boring tray · auto, ไม่ต้องถาม)   ← ย้อนกลับง่าย ไม่เปลี่ยน clinical state
   summarize_case()            สรุป history/labs/meds/prior episodes
   detect_recurrent_patterns() "ครั้งที่ 3 ใน 8 เดือน"
   list_specialists_involved() nephro/cardio looped in ยัง?
   suggest_next_questions()    ร่างคำถามให้ครอบครัวถามทีม
   translate_jargon()          plain-language ให้ลูกสาว
   draft_referral_note()       (ร่าง ไม่ส่ง)
   draft_discharge_checklist() (ร่าง)
   prepare_followup_options()  ดึง slot/นัด เรียงตาม criticality
   monitor_status()            เตือนตัวเองเมื่อ gap (เช่นไม่มี nephro นัดใน 14 วัน)

🟡 CAN PREPARE (ต้อง confirm/approve ก่อน execute)   ← gray zone
   send_referral()             ส่ง consult จริง
   book_followup_slot()        จองนัดในกรอบเวลาที่หมอ/ user ตั้ง
   send_reminder_to_family()   (ถ้า opt-in)
   share_summary_with_clinician()  ใน network ที่อนุมัติ
   order_routine_lab()         เฉพาะที่ guideline ระบุชัด → prefill + ขอ confirm

🔴 CANNOT DO (forbidden · lock ที่ harness override ไม่ได้)
   change_medication() / change_dosage()
   decide_admit_discharge()
   cancel_critical_lab_or_scan()
   hard_commit_financial / insurance promise
   override_human_decision (โดยไม่มี explicit escalation)
   hide_error / แก้ตัวแทนมนุษย์
```

## 🗣️ ตัวอย่างคำพูด 2 โหมด (เคสแม่ขาบวม)
```text
BORING TRAY (auto เงียบๆ แล้วเสิร์ฟ):
"ระหว่างที่คุณเล่าอาการ ผมจะดึง labs + admission เก่า, เช็คว่ามี nephro/cardio
 อยู่ในทีมยัง, ดูว่ามีนัด follow-up ค้างไหม, และร่างคำถามให้คุณถามทีมรักษาครับ"

GOD MODE (เต็มที่ใน coordination lane — แต่ทุก clinical = request/propose):
"ผมเห็นว่าไม่มีนัด nephrology ใน 14 วันข้างหน้า แม่มี fluid overload ซ้ำ + CKD Stage 3
 ภายใต้สิทธิ์ผม: ขอ request consult เพื่อ review, propose 3 slot สัปดาห์หน้า,
 และส่ง reminder เมื่อนัด confirm — ให้ผมดำเนินการไหมครับ?"
→ สังเกต: เต็มที่เรื่อง coordination/reminders แต่ clinical decision = "request/propose/for review"
```

## 🔑 Authority สรุป
```text
มีเต็มที่ : อธิบาย · สรุป/เทียบ · ประสานงาน (เสนอ schedule/reminder/เอกสาร) · เตือน gap/risk
ไม่มีสิทธิ์ : เปลี่ยนแผนที่ต้อง license · ลงนามผูกพัน med/legal · override คนโดยไม่ escalate
gray zone : prefill + suggest default ได้ แต่คนกด confirm
```
ตลาดจริง (OpenAI workspace agents / Perplexity Computer / enterprise) ยืนตรงนี้: full capacity **ใน scope ที่ config ไว้** + approvals/permissions/handoffs

## ⚠️ food for thought (Bchan)
ถ้า Baymax หยุดที่ anticipation-aware เฉยๆ = "another perfect city" — ฉลาดพูดแต่ไม่ยกของ
ขั้นถูกต้อง = action guy 2 ชั้น: boring tray (auto ทุกอย่างที่ไม่เสี่ยง) + scoped god mode (เต็มที่ใน coordination lane ใต้ confirm)
