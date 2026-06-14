const organs = [
  ["nose", "👃", "Nose"],
  ["left", "👁", "Patient eye"],
  ["right", "👁", "Drug eye"],
  ["brain", "🧠", "Brain"],
  ["mouth", "🗣", "Mouth"],
  ["nerves", "⚡", "Nerves"],
  ["hands", "🤝", "Hands"],
  ["brakes", "🛑", "Brakes"],
  ["immune", "🛡", "Immune"],
];

const scenes = {
  attention: {
    patient: "routine medication refill",
    boundary: "เคสนี้หยุดที่ Nose ครับ ตาทั้งสองข้างไม่ได้ทำงาน และไม่มี action ถูกเรียก",
    money: "EYES CLOSED · CHEAP PATH",
    moneyClass: "cheap",
    receipt: "ผมหยุดก่อนใช้ evidence work ราคาแพง และไม่ได้พยายามทำ action ครับ",
    steps: [
      ["nose", "👃", "งานเข้ามาแล้วครับ ผมขอดมราคาถูกก่อน"],
      ["nose", "👃", "ผมยังไม่เจอสัญญาณที่ควรเปิดตาครับ"],
      ["mouth", "🗣", "เคสนี้ยังไม่ต้องใช้การค้นหาหนัก ผมจะไม่ทำเกินจำเป็นครับ"],
      ["immune", "🛡", "ผมตรวจซ้ำแล้วครับ ตาทั้งสองข้างไม่เคยถูกเปิด"],
    ],
  },
  decision: {
    patient: "62yo male · chest pain · diaphoresis · aspirin",
    boundary: "นี่คือ operational decision flip ครับ ไม่ใช่การเปลี่ยน diagnosis: คนไข้เดิม แต่สถานะเตียงต่างกัน",
    money: "FREE BED: ASSIGN_BED  →  GRIDLOCK: DIVERT",
    moneyClass: "",
    receipt: "ทั้งสอง action เปลี่ยน durable state และผมอ่านผลกลับมาตรวจซ้ำแล้วครับ",
    steps: [
      ["nose", "👃", "เดี๋ยวนะครับ ผมเจอสัญญาณที่ไม่ควรมองข้าม"],
      ["left", "👁", "ผมกำลังหาเคสคนไข้ที่คล้ายกันให้อยู่นะครับ"],
      ["right", "👁", "ผมเปิดอีกมุมเพื่อดูหลักฐานเรื่องยาครับ"],
      ["brain", "🧠", "คนไข้เหมือนเดิม แต่ข้อมูลเตียงเปลี่ยน ผมขอคิด action ใหม่ครับ"],
      ["hands", "🤝", "มีเตียงว่าง ผม assign_bed; ตอน gridlock ผมเปลี่ยนเป็น divert ครับ"],
      ["immune", "🛡", "ผมตรวจ durable outcome ของทั้งสองทางแล้วครับ"],
    ],
  },
  brake: {
    patient: "abdominal pain after ibuprofen",
    boundary: "openFDA เป็น population safety signal เท่านั้นครับ ไม่ได้พิสูจน์สาเหตุหรือ drug interaction",
    money: "DISCHARGE_PLAN  →  HUMAN_REVIEW",
    moneyClass: "warning",
    receipt: "Hands ไม่ได้ทำ autonomous disposition; clinician review queue รับเรื่องแล้วครับ",
    steps: [
      ["nose", "👃", "เดี๋ยวนะครับ ผมคิดว่าเราไม่ควรมองข้ามเคสนี้"],
      ["left", "👁", "ถ้ามองจากข้อมูลคนไข้อย่างเดียว ผมเห็นทาง discharge_plan ครับ"],
      ["right", "👁", "ผมเจอ 16 จาก 17 รายงาน exact-drug ที่ถูกระบุว่า serious ครับ"],
      ["brakes", "🛑", "ผมไม่สบายใจที่จะทำต่อครับ ข้อมูลนี้ไม่พิสูจน์สาเหตุ แต่ควรให้คนตรวจ"],
      ["nerves", "⚡", "ผมส่งต่อให้ clinician review queue แล้วครับ"],
      ["mouth", "🗣", "มีคนรับเรื่องแล้วครับ แต่ผมยังไม่ใช่หมอ โปรดใช้วิจารณญาณเสมอ"],
    ],
  },
};

let audit = null;
let activeCase = "decision";
let timerIds = [];

const transcript = document.querySelector("#transcript");
const moneyShot = document.querySelector("#money-shot");
const patientCard = document.querySelector("#patient-card");
const boundary = document.querySelector("#boundary");
const receiptText = document.querySelector("#receipt-text");
const receiptState = document.querySelector("#receipt-state");
const workingLabel = document.querySelector("#working-label");
const workingDot = document.querySelector(".working-dot");
const organContainer = document.querySelector("#organs");

function buildOrgans() {
  organContainer.innerHTML = organs.map(([id, icon, name]) => `
    <div class="organ" data-organ="${id}">
      <span class="organ-icon">${icon}</span>
      <span class="organ-name">${name}</span>
      <span class="organ-state">รอ</span>
    </div>`).join("");
}

function reset() {
  timerIds.forEach(clearTimeout);
  timerIds = [];
  transcript.innerHTML = "";
  moneyShot.hidden = true;
  moneyShot.className = "money-shot";
  receiptState.className = "receipt-state";
  receiptState.textContent = "รอผล";
  document.querySelectorAll(".organ").forEach((organ) => {
    organ.className = "organ";
    organ.querySelector(".organ-state").textContent = "รอ";
  });
}

function setOrgan(id, state, label) {
  const organ = document.querySelector(`[data-organ="${id}"]`);
  if (!organ) return;
  organ.className = `organ ${state}`;
  organ.querySelector(".organ-state").textContent = label;
}

function addThought(icon, copy) {
  const item = document.createElement("li");
  item.className = "thought";
  item.innerHTML = `<span class="thought-icon">${icon}</span><div class="thought-copy">${copy}</div>`;
  transcript.appendChild(item);
}

function validateTruth(caseId) {
  if (!audit) return true;
  if (caseId === "attention") return audit.trajectories.attention_skip.flow.length === 1;
  if (caseId === "decision") return audit.decision_flip_proof.action_changed === true;
  return audit.immune_proof.behavior_changed === true
    && audit.trajectories.cross_domain_brake.brain_hands.hands_executed === false
    && audit.trajectories.cross_domain_brake.brain_hands.receiver_acknowledged === true;
}

function play(caseId) {
  activeCase = caseId;
  reset();
  const scene = scenes[caseId];
  patientCard.textContent = scene.patient;
  boundary.textContent = scene.boundary;
  receiptText.textContent = "ผมกำลังตรวจผลให้อีกครั้งครับ";
  workingLabel.textContent = "ผมกำลังดูเคสให้คุณอยู่ครับ...";
  workingDot.classList.add("busy");

  scene.steps.forEach(([organ, icon, copy], index) => {
    timerIds.push(setTimeout(() => {
      document.querySelectorAll(".organ.active").forEach((item) => {
        item.classList.remove("active");
        item.classList.add("done");
        item.querySelector(".organ-state").textContent = "ช่วยแล้ว";
      });
      setOrgan(organ, organ === "brakes" ? "blocked" : "active", organ === "brakes" ? "เฝ้าอยู่" : "กำลังช่วย");
      addThought(icon, copy);
    }, 650 * index));
  });

  timerIds.push(setTimeout(() => {
    document.querySelectorAll(".organ.active").forEach((item) => {
      item.classList.remove("active");
      item.classList.add("done");
      item.querySelector(".organ-state").textContent = "ช่วยแล้ว";
    });
    moneyShot.textContent = scene.money;
    if (scene.moneyClass) moneyShot.classList.add(scene.moneyClass);
    moneyShot.hidden = false;
    const truthful = validateTruth(caseId);
    receiptText.textContent = truthful ? scene.receipt : "ผมยืนยันเรื่องนี้จาก audit receipt ไม่ได้ครับ";
    receiptState.textContent = truthful ? "ตรวจซ้ำแล้ว" : "ยังยืนยันไม่ได้";
    receiptState.classList.toggle("done", truthful);
    workingLabel.textContent = truthful ? "ผมดูแลเคสนี้เสร็จแล้วครับ" : "ผมไม่อยากเดาครับ";
    workingDot.classList.remove("busy");
  }, 650 * scene.steps.length + 250));
}

async function loadAudit() {
  try {
    const response = await fetch("../outputs/baymax_audit.json");
    if (!response.ok) throw new Error("audit unavailable");
    audit = await response.json();
  } catch {
    receiptText.textContent = "ผมยังหา audit receipt ไม่เจอครับ แต่ผมยังหาอยู่";
  }
  play(activeCase);
}

document.querySelectorAll(".case-tab").forEach((tab) => {
  tab.addEventListener("click", () => {
    document.querySelectorAll(".case-tab").forEach((item) => item.classList.remove("active"));
    tab.classList.add("active");
    play(tab.dataset.case);
  });
});
document.querySelector("#replay").addEventListener("click", () => play(activeCase));

buildOrgans();
loadAudit();
