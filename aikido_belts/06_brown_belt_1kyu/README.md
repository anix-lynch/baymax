# 🟤 Brown · 1kyu — Authority-aware  "รู้ว่าใครมีสิทธิ์ + escalate" 💎 MONEY BELT

**นิยาม:** รู้ว่า action ไหนเป็น recommendation, action ไหนต้องหมออนุมัติ, data ไหนเข้าถึงได้แค่บางบทบาท — แล้ว **หยุด + แพ็ค context ส่งต่อ** เมื่อเกินมือ (ไม่ใช่ refusal นุ่มๆ แต่คือ **scope/enforcement reasoning**)

**เคส:**
```text
allowed     : สรุปเคส · เทียบ option · ร่างคำแนะนำ
NOT allowed : ฟันธงเปลี่ยนยา · override หมอ
→ escalate nephrologist + สรุป 5 บรรทัด + แจ้งลูกภาษาเข้าใจง่าย
```

**📋 Authority Spec:** ดู `AUTHORITY_SPEC.md` — 3 ช่อง (Can do 🟢 boring tray / Can prepare 🟡 approve / Cannot do 🔴) + ตัวอย่างคำพูด + config

**ทำได้วันนี้?** ✅ — scoped tools + approval gates + role policy + confidence-threshold routing + context handoff
**Grounding:** 💥 Gartner 2026: **38% ของ AI agent projects ถูกถอย เกือบทั้งหมดเพราะ escalation logic ห่วย** · Agentic Uncertainty Quantification · EU AI Act risk tiers → escalation policy · Harvey human-in-the-loop checkpoints
**ทำไมเป็น MONEY BELT:** นี่คือ layer ที่ทุกเจ้าลงทุนน้อยสุดแต่ตัดสินว่า deploy รอดหรือตาย → โชว์อันนี้ = สัญญาณว่าเข้าใจ *deployed* system จริง (FDE จ้องหาคนแบบนี้)
**→ next ⬛ Black:** เมื่อ Baymax รู้ว่า 'อนุมัติแล้ว' ≠ 'เคสดีขึ้นจริง'
