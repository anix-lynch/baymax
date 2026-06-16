# ⬛ Black · 1dan — Trajectory + Outcome + Longitudinal adaptive orchestration 💎 CAPSTONE

**นิยาม (capstone):** รวมทุก belt ล่าง แล้วทำ **adaptive plan revision** ระหว่างทาง:
- **Outcome-aware** — tool success ≠ real-world success; verify ผลจริง (lab ออก, ยาให้จริง, บวมลด, ไตไม่ทรุด) → ไม่เกิดต้อง re-plan
- **Trajectory-aware** — มองเคสเป็นเส้นทาง past→now→next branch ไม่ใช่ snapshot turn เดียว
- **Longitudinal** — reason ข้ามเวลา: trend, adherence เสื่อม, escalation ซ้ำ, data drift ข้ามเดือน

**เคส:**
```text
PAST 2024 Stage2 ยาเวิร์ค → NOW 2026 Stage3 บวมซ้ำ ไตน้อยลง lab ค้าง → NEXT
   treat แรง = branch ไตทรุด   |   ระวัง = branch คงที่
→ verify outcome จริง → ถ้า trajectory แย่: re-plan + escalate + modify
```

**ทำได้วันนี้?** 🟡 frontier-but-demoable — reflection loop + eval harness + trace logging + state transitions ใน orchestration layer (demo ใช้ simulated longitudinal data)
**Grounding:** Anthropic extended thinking + self-verification + Effort Control (Opus 4.x); Cognition Devin plan→execute→learn→fix; Nature longitudinal health-AI framework; EHR2Path trajectory forecasting; outcome-oriented eval
**Hiring signal:** สูงสุด — frontier *product* behavior, โชว์ว่าเข้าใจ eval + reliability + safety เป็นระบบ ไม่ใช่ prompt สวย
**Demo ปลายทาง:** belt-switcher หน้าเดียว (ดู `STORYBOARD.md`) + deploy Vercel
