# 🟡 Yellow Belt · 5th Kyu — "เชื่ออะไร + ควรทำอะไร" (State-aware Trade-off)

**File:** `baymax_yellow_belt_state_aware.html`

## เลื่อนขั้นจากสายขาวยังไง
สายขาวเจอเคสเก่าที่สำเร็จแล้ว "ทำซ้ำ" — สายเหลือง **หยุดแล้วถามต่อ**:

```text
🔁 เจอเคสเก่าที่เคยสำเร็จ ✓
⚡ แต่ "สถานะวันนี้" เปลี่ยนรึเปล่า?
      Past State 2024 : CKD Stage 2
      Current State 2026 : CKD Stage 3   ← ไตแย่ลง!
⚠ ทำซ้ำ protocol เดิมไม่ได้แล้ว
🧠 Re-evaluating recommendation...
```

## 2 organ ใหม่ที่งอกมา
```text
⚡ Nerves (เส้นประสาท) = เราอยู่ตรงไหนตอนนี้  (State)
🧠 Brain  (สมอง)       = แล้วควรทำอะไร        (Trade-off)
```

## Trade-off matrix (จุดขาย)
หลักฐาน 6 อย่างจริงพร้อมกันหมด ไม่มีอันไหนผิด — ปัญหาคือ "ให้น้ำหนักอะไร":

```text
มิติ                    A · textbook       B · เฉพาะแม่
ได้ผลเร็ว                ✓✓                 ✓
ปลอดภัยต่อไต Stage 3     ⚠ เสี่ยง           ✓✓
ตรงกับสถานะวันนี้        ✗ (อิง Stage 2)    ✓ (อิง Stage 3)
                                          👉 แนะนำ B เฉพาะเคสนี้
```

## Level
```text
Lv1 Retrieval → Lv2 Evidence Arbitration → Lv3 Trade-off Reasoning 💥  ← อยู่ตรงนี้
```

## ทำไม recruiter Anthropic ชอบ
```text
Retrieval บอกแค่   : "ผมเจอเคสเก่าแล้วครับ"
Reasoning บอกว่า   : "ผมเจอเคสเก่าแล้ว แต่ผมไม่คิดว่าควรทำเหมือนเดิม"
```
นี่คือ **state-aware reasoning** ไม่ใช่ RAG — ใกล้คำว่า Agent Engineer มากกว่า RAG Engineer เยอะ

→ เลื่อนขั้น **🟠 Orange Belt (Workflow-aware)** เมื่อ Baymax รู้ว่าเคสอยู่ stage ไหน + ยังไม่ commit ก่อนถึงจุด (ดู BELT_PROGRESSION.md v2)
