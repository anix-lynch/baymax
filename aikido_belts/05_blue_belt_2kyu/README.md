# 🔵 Blue · 2kyu — Objective-aware  "รู้ goal จริง ไม่ใช่แค่คำขอ"

**นิยาม:** แยก **request** ออกจาก **goal** แล้ว optimize ไปที่เป้าหมายจริง ไม่ใช่ตามคำพูดตรงตัว (+preference-aware เป็น flavor รอง — ต้องรองจาก safety/authority ใน healthcare)

**เคส:** ลูกขอ "ให้แม่กลับบ้านเร็ว" → goal จริง = "discharge ปลอดภัย rebound ต่ำ ไม่กลับมา admit ซ้ำ" ไม่ใช่เร็วสุด

```text
request: fastest discharge
   ↓ infer
goal: stable + follow-up ready + low readmission
```

**ทำได้วันนี้?** ✅ — goal schema แยกจาก user utterance + memory (Mem0/Zep) สำหรับ preference
**Grounding:** goal-based agents = reasoning layer ใต้ agentic AI (production 2026), outcome-oriented eval (IBM/Galileo), Glean work-goal framing
**Hiring signal:** สูง (product/FDE) — "understands my goals not my request"
**→ next 🟤 Brown:** เมื่อ Baymax รู้ขอบเขตอำนาจก่อนไล่ตาม goal แรงเกิน
