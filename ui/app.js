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
  discovery: {
    patient: "Patient said: “My mother’s legs are swollen.”",
    boundary: "This retrieves a synthetic precedent and suggests a question. It does not diagnose the patient.",
    money: "NOBODY MENTIONED HEART FAILURE. BAYMAX RETRIEVED IT ANYWAY.",
    moneyClass: "",
    receipt: "The discovery is bound to source L1-000162 and its synthetic encounter receipt.",
    steps: [
      ["nose", "👃", "The patient used ordinary language. I translate it into evidence language before searching."],
      ["left", "👁", "Raw words miss the target. Expanded symptom language retrieves a heart-failure precedent."],
      ["brain", "🧠", "I connect the retrieved clues into a possible fluid-overload pattern without claiming a diagnosis."],
      ["mouth", "🗣", "The next useful question is: Is she short of breath at rest or when lying flat?"],
    ],
  },
  attention: {
    patient: "routine medication refill",
    boundary: "This case stops at the Nose. Neither eye runs and no action is called.",
    money: "EYES CLOSED · CHEAP PATH",
    moneyClass: "cheap",
    receipt: "I stopped before expensive evidence work and did not attempt an action.",
    steps: [
      ["nose", "👃", "A case arrived. I check the served ESI attention signal first."],
      ["nose", "👃", "This case is priority tier 4, so I keep the expensive eyes closed."],
      ["mouth", "🗣", "Heavy retrieval is not justified yet. I will not do more than necessary."],
      ["immune", "🛡", "Verified: serious-case recall remains above 95%, and neither eye was opened."],
    ],
  },
  decision: {
    patient: "62yo male · chest pain · diaphoresis · aspirin",
    boundary: "This is an operational decision flip, not a diagnosis change: same patient, different bed capacity.",
    money: "FREE BED: ASSIGN_BED  →  GRIDLOCK: DIVERT",
    moneyClass: "",
    receipt: "Both actions changed durable state, and I read the outcomes back to verify them.",
    steps: [
      ["nose", "👃", "One moment. I found a signal that should not be ignored."],
      ["left", "👁", "I am retrieving similar patient evidence."],
      ["right", "👁", "I am opening another perspective for drug-safety evidence."],
      ["brain", "🧠", "The patient is unchanged, but bed capacity changed. I must reconsider the action."],
      ["hands", "🤝", "With a free bed, I assign_bed. During gridlock, I change course to divert."],
      ["immune", "🛡", "I verified the durable outcome of both paths."],
    ],
  },
  brake: {
    patient: "abdominal pain after ibuprofen",
    boundary: "openFDA is a population safety signal only. It does not prove causality or a drug interaction.",
    money: "DISCHARGE_PLAN  →  HUMAN_REVIEW",
    moneyClass: "warning",
    receipt: "Hands did not perform an autonomous disposition; the clinician review queue acknowledged the case.",
    steps: [
      ["nose", "👃", "One moment. I do not think this case should be overlooked."],
      ["left", "👁", "Patient evidence alone supports a discharge_plan path."],
      ["right", "👁", "I found 16 of 17 exact-drug reports marked serious."],
      ["brakes", "🛑", "I should not continue autonomously. This does not prove causality, but it requires human review."],
      ["nerves", "⚡", "I handed the case to the clinician review queue."],
      ["mouth", "🗣", "The receiver acknowledged the case. I am not a clinician; human judgment remains required."],
    ],
  },
};

let audit = null;
let activeCase = "discovery";
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
const discoveryCard = document.querySelector("#discovery-card");
const thinkingTitle = document.querySelector("#thinking-title");

function buildOrgans() {
  organContainer.innerHTML = organs.map(([id, icon, name]) => `
    <div class="organ" data-organ="${id}">
      <span class="organ-icon">${icon}</span>
      <span class="organ-name">${name}</span>
      <span class="organ-state">Waiting</span>
    </div>`).join("");
}

function reset() {
  timerIds.forEach(clearTimeout);
  timerIds = [];
  transcript.innerHTML = "";
  discoveryCard.hidden = true;
  discoveryCard.innerHTML = "";
  moneyShot.hidden = true;
  moneyShot.className = "money-shot";
  receiptState.className = "receipt-state";
  receiptState.textContent = "Awaiting result";
  document.querySelectorAll(".organ").forEach((organ) => {
    organ.className = "organ";
    organ.querySelector(".organ-state").textContent = "Waiting";
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
  if (caseId === "discovery") {
    const discovery = audit.trajectories.retrieval_discovery;
    return discovery.raw_query_missed_target === true
      && discovery.top_source_id === "L1-000162"
      && discovery.source_is_synthetic === true;
  }
  if (caseId === "attention") {
    const nose = audit.trajectories.attention_skip.nose;
    return audit.trajectories.attention_skip.flow.length === 1
      && nose.decided_by === "served_signal"
      && nose.evaluation.serious_case_recall >= 0.95;
  }
  if (caseId === "decision") return audit.decision_flip_proof.action_changed === true;
  return audit.immune_proof.behavior_changed === true
    && audit.trajectories.cross_domain_brake.brain_hands.hands_executed === false
    && audit.trajectories.cross_domain_brake.brain_hands.receiver_acknowledged === true;
}

function renderDiscovery() {
  if (!audit) return;
  const discovery = audit.trajectories.retrieval_discovery;
  discoveryCard.innerHTML = `
    <div class="retrieval-contrast">
      <div class="retrieval-step missed">
        <span class="retrieval-label">RAW WORDS · MISSED</span>
        <strong>${discovery.patient_words}</strong>
        <span>Top result: ${discovery.raw_query_top_source_id}</span>
      </div>
      <div class="retrieval-arrow">→</div>
      <div class="retrieval-step found">
        <span class="retrieval-label">EVIDENCE LANGUAGE · FOUND</span>
        <strong>${discovery.evidence_query}</strong>
        <span>Top result: ${discovery.top_source_id} · relevance ${discovery.top_relevance_score}</span>
      </div>
    </div>
    <div class="found-banner">What Baymax found that nobody mentioned</div>
    <div class="finding-grid">
      ${discovery.retrieved_evidence.map((finding) => `<span>✓ ${finding}</span>`).join("")}
    </div>
    <div class="evidence-path">${discovery.evidence_path.join("<b>→</b>")}</div>
    <div class="source-receipt">
      <span>Source receipt · ${discovery.top_source_id} · synthetic encounter</span>
      <p>${discovery.source_receipt.chief_complaint}</p>
    </div>`;
  discoveryCard.hidden = false;
}

function play(caseId) {
  activeCase = caseId;
  reset();
  const scene = scenes[caseId];
  patientCard.textContent = scene.patient;
  thinkingTitle.textContent = caseId === "discovery"
    ? "What Baymax discovered before answering"
    : "I am reviewing this case";
  if (caseId === "discovery") renderDiscovery();
  boundary.textContent = scene.boundary;
  receiptText.textContent = "I am verifying the outcome.";
  workingLabel.textContent = "I am reviewing the case...";
  workingDot.classList.add("busy");

  scene.steps.forEach(([organ, icon, copy], index) => {
    timerIds.push(setTimeout(() => {
      document.querySelectorAll(".organ.active").forEach((item) => {
        item.classList.remove("active");
        item.classList.add("done");
        item.querySelector(".organ-state").textContent = "Complete";
      });
      setOrgan(organ, organ === "brakes" ? "blocked" : "active", organ === "brakes" ? "Guarding" : "Working");
      addThought(icon, copy);
    }, 650 * index));
  });

  timerIds.push(setTimeout(() => {
    document.querySelectorAll(".organ.active").forEach((item) => {
      item.classList.remove("active");
      item.classList.add("done");
      item.querySelector(".organ-state").textContent = "Complete";
    });
    moneyShot.textContent = scene.money;
    if (scene.moneyClass) moneyShot.classList.add(scene.moneyClass);
    moneyShot.hidden = false;
    const truthful = validateTruth(caseId);
    receiptText.textContent = truthful ? scene.receipt : "I cannot verify this claim from the audit receipt.";
    receiptState.textContent = truthful ? "Verified" : "Unverified";
    receiptState.classList.toggle("done", truthful);
    workingLabel.textContent = truthful ? "Case review complete." : "I will not guess.";
    workingDot.classList.remove("busy");
  }, 650 * scene.steps.length + 250));
}

const ledgerLabels = {
  nose: "👃 Nose", left_eye: "👁 Patient eye", right_eye: "👁 Drug eye",
  brain: "🧠 Brain", brakes: "🛑 Brakes", nerves: "⚡ Nerves",
  hands: "🤝 Hands", mouth: "🗣 Mouth", immune: "🛡 Immune",
};

function renderHonesty() {
  const grid = document.querySelector("#honesty-ledger");
  const headline = document.querySelector("#honesty-headline");
  const claim = document.querySelector("#honesty-claim");
  if (!grid || !audit || !audit.honesty_ledger) return;
  const ledger = audit.honesty_ledger;
  headline.textContent = `${ledger.headline_verdict} ships at weakest leaf`;
  headline.classList.toggle("warning", ledger.headline_verdict !== "✅");
  claim.textContent = ledger.headline_claim_allowed;
  grid.innerHTML = Object.entries(ledger.organs).map(([id, organ]) => {
    const weakest = id === ledger.weakest_load_bearing_organ ? " weakest" : "";
    const note = organ.verdict === "✅" ? organ.claim_allowed : organ.hedge;
    return `
      <div class="ledger-cell${weakest}">
        <div class="ledger-top">
          <span class="ledger-verdict">${organ.verdict}</span>
          <span class="ledger-organ">${ledgerLabels[id] || id}</span>
          <span class="ledger-variant">${organ.capability_lane}</span>
        </div>
        <p class="ledger-claim">${note}</p>
      </div>`;
  }).join("");
}

async function loadAudit() {
  try {
    const response = await fetch("../outputs/baymax_audit.json");
    if (!response.ok) throw new Error("audit unavailable");
    audit = await response.json();
    renderHonesty();
  } catch {
    receiptText.textContent = "I cannot find the audit receipt yet. I am still checking.";
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
