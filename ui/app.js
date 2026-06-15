const organs = [
  ["nose", "👃", "Nose · what matters first"],
  ["left", "👁", "Eyes · her history"],
  ["right", "💊", "Eyes · her medicines"],
  ["brain", "🧠", "Brain · piece it together"],
  ["mouth", "🗣", "Voice · say it simply"],
  ["nerves", "⚡", "Reflex · pass it on"],
  ["hands", "🤝", "Hands · get it done"],
  ["brakes", "🛑", "Brakes · stop if unsure"],
  ["immune", "🛡", "Memory · past slip-ups"],
];

const scenes = {
  discovery: {
    patient: "Daughter at intake: “My mother’s legs are swollen.” · Patient: the mother, 71F",
    boundary: "This retrieves a synthetic precedent and suggests a question. It does not diagnose the patient.",
    money: "Nobody mentioned her heart failure — I found it anyway.",
    moneyClass: "",
    receipt: "The discovery is bound to source L1-000497 and its synthetic encounter receipt.",
    steps: [
      ["nose", "👃", "The family used ordinary words. I translate “swollen legs” into evidence language before searching."],
      ["left", "👁", "Literal words miss it. Expanded symptom language retrieves her record — and the history nobody mentioned."],
      ["left", "👁", "On her record: heart failure, kidney disease stage 3, type-2 diabetes, prior fluid overload."],
      ["right", "👁", "Her home medications: metformin, lisinopril, furosemide. Salt and repeat diuretics interact with stage-3 kidneys."],
      ["immune", "🛡", "What the last clinician did: admitted two days for leg edema, diuresed, discharged without nephrology follow-up."],
      ["brain", "🧠", "I connect it: diabetes → kidney disease → fluid overload → swollen legs. The loop that bounced back."],
      ["brakes", "🛑", "Surface triage reads low and routes to discharge — the same path as last time. I will not repeat it without review."],
      ["hands", "🤝", "The ER is full. I record the capacity action and flag admission instead of an ER-queue wait."],
      ["mouth", "🗣", "I explain it two ways: clinically to the doctor, and plainly to the family."],
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
const resultCard = document.querySelector("#result-card");
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
  if (resultCard) { resultCard.hidden = true; resultCard.innerHTML = ""; }
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

function addThought(icon, copy, extra) {
  const item = document.createElement("li");
  item.className = "thought";
  item.innerHTML = `<span class="thought-icon">${icon}</span><div class="thought-copy">${copy}${extra ? `<div class="thought-extra">${extra}</div>` : ""}</div>`;
  transcript.appendChild(item);
}

const EV_PLAIN = {
  "chronic heart failure history": "heart failure",
  "chronic kidney disease (stage 3)": "kidney disease (stage 3)",
  "type 2 diabetes": "diabetes",
  "prior fluid overload / pulmonary edema": "fluid in the lungs before",
  "reduced urine output": "peeing less lately",
  "bilateral lower-extremity edema": "both legs swollen",
};

function chipRow(items) {
  return `<div class="thought-chips">${items.map((x) => `<span>${x}</span>`).join("")}</div>`;
}

function buildDiscoverySteps(d) {
  const r = d.disposition_recommendation;
  const er = r.bed_booking.er_state;
  const ev = (d.retrieved_evidence || []).map((e) => EV_PLAIN[e] || e);
  const meds = (d.medications_on_record || []).slice();
  const s = d.state_awareness || {};
  return [
    ["nose", "👃", "The family used everyday words. Let me turn “swollen legs” into medical clues before I look."],
    ["left", "👁", "Wait a second… let me open her old records first."],
    ["left", "👁", "Nobody mentioned these — but they were on file:", chipRow(ev)],
    ["right", "💊", "Her current medicines — and why they matter with weak kidneys:", chipRow(meds.concat(["too much salt → more swelling"]))],
    ["immune", "🛡", `Last time this worked: a mild water pill eight months ago — back when her kidneys were at ${s.past_state || "an earlier stage"}.`],
    ["brain", "🧠", `But her kidneys are worse now: <strong>${s.past_state || "stage 2"} → ${s.current_state || "stage 3"}</strong>. The old fix isn’t safe to repeat — let me re-think it.`],
    ["brain", "🧠", "Here’s the real story: <strong>diabetes → kidney trouble → fluid builds up → swollen legs</strong>. The same loop that came back."],
    ["brakes", "🛑", "The quick read says “send her home” — same as last time. I won’t repeat that without a proper check."],
    ["hands", "🤝", `The ER is full (${er.occupancy_pct}% full, ${er.available_beds} beds free). I won’t leave her waiting in line — I’m flagging her for a ward bed.`],
    ["mouth", "🗣", "Let me say it two ways — one for the doctor, one for the family."],
  ];
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
    <div class="lanes">
      <div class="lane"><span class="lane-label">💊 Medications on record</span><span>${(discovery.medications_on_record || []).join(", ") || "—"}</span></div>
      <div class="lane"><span class="lane-label">🛡 What the last clinician did</span><span>${discovery.prior_care || "—"}</span></div>
    </div>
    <div class="source-receipt">
      <span>Source receipt · ${discovery.top_source_id} · synthetic encounter</span>
      <p>${discovery.source_receipt.chief_complaint}</p>
    </div>`;
  discoveryCard.hidden = false;
}

function renderResult() {
  if (!audit || !audit.trajectories.retrieval_discovery.disposition_recommendation) return;
  const d = audit.trajectories.retrieval_discovery;
  const r = d.disposition_recommendation;
  const dv = d.dual_voice || {};
  const bb = r.bed_booking;
  const sa = d.state_awareness || {};
  const stateShift = sa.state_changed
    ? `<div class="state-shift"><span class="rc-label">🔁 Why not just repeat last time</span><p>It worked before at <strong>${sa.past_state}</strong>, but she’s now at <strong>${sa.current_state}</strong> — so I’d change the plan, not copy it.</p></div>`
    : "";
  const tiers = ["GREEN", "YELLOW", "RED"];
  const pills = tiers
    .map((t) => `<span class="tier ${t.toLowerCase()}${t === r.triage_tier ? " on" : ""}">${t}</span>`)
    .join("");
  const tidy = (s) => (s || "").replace(/_/g, " ");
  resultCard.innerHTML = `
    <div class="result-head">What I’d recommend <span class="sim">simulation</span></div>
    <div class="triage-flip">
      <span class="flip-from">Quick read: ${r.surface_triage_tier} (ESI ${r.esi_level})</span>
      <b>→</b>
      <span class="flip-to">I’d raise it to ${r.triage_tier}</span>
      <span class="tier-pills">${pills}</span>
    </div>
    <div class="result-grid">
      <div class="result-cell"><span class="rc-label">Where she should go</span><strong>${tidy(r.recommended_care_setting)}</strong></div>
      <div class="result-cell"><span class="rc-label">Quick-read bed call</span><strong>${tidy(r.surface_bed_disposition)}</strong></div>
      <div class="result-cell"><span class="rc-label">Safe to wait</span><strong>${r.max_wait_minutes} min</strong></div>
    </div>
    <div class="escalation">⚠️ ${r.escalation_trigger}</div>
    ${stateShift}
    <div class="booking">
      <span class="rc-label">🛏 Bed booking · real durable action</span>
      <p>ER ${bb.er_state.occupancy_pct}% full · ${bb.er_state.available_beds} free · queue ${bb.er_state.queue_length}. Committed “${tidy(bb.surface_action_taken)}”, re-read &amp; verified: ${bb.outcome_verified ? "yes" : "no"}. ${bb.note}</p>
    </div>
    <div class="dual">
      <div class="voice clinician"><span class="rc-label">🩺 To the clinician</span><p>${dv.to_clinician || ""}</p></div>
      <div class="voice family"><span class="rc-label">👧 To the family</span><p>${dv.to_family || ""}</p></div>
    </div>
    ${d.corpus_augmentation ? `<div class="provenance">🔗 Lineage: ${d.corpus_augmentation.synthetic_rows_added} synthetic row (${d.corpus_augmentation.injected_case_id}, marked + holdout) added locally and disclosed — not in the upstream commit. Downstream index/Vertex rebuilds must filter it before non-demo use.</div>` : ""}`;
  resultCard.hidden = false;
}

function play(caseId) {
  activeCase = caseId;
  reset();
  const scene = scenes[caseId];
  patientCard.textContent = scene.patient;
  thinkingTitle.textContent = caseId === "discovery"
    ? "What Baymax discovered before answering"
    : "I am reviewing this case";
  boundary.textContent = scene.boundary;
  receiptText.textContent = "I am verifying the outcome.";
  workingLabel.textContent = "I am reviewing the case...";
  workingDot.classList.add("busy");

  scene.steps.forEach((step, index) => {
    const [organ, icon, copy, extra] = step;
    timerIds.push(setTimeout(() => {
      document.querySelectorAll(".organ.active").forEach((item) => {
        item.classList.remove("active");
        item.classList.add("done");
        item.querySelector(".organ-state").textContent = "Complete";
      });
      setOrgan(organ, organ === "brakes" ? "blocked" : "active", organ === "brakes" ? "Guarding" : "Working");
      addThought(icon, copy, extra);
    }, 750 * index));
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
    if (caseId === "discovery") renderResult();
    const truthful = validateTruth(caseId);
    receiptText.textContent = truthful ? scene.receipt : "I cannot verify this claim from the audit receipt.";
    receiptState.textContent = truthful ? "Verified" : "Unverified";
    receiptState.classList.toggle("done", truthful);
    workingLabel.textContent = truthful ? "Case review complete." : "I will not guess.";
    workingDot.classList.remove("busy");
  }, 750 * scene.steps.length + 250));
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
    if (audit.trajectories && audit.trajectories.retrieval_discovery) {
      scenes.discovery.steps = buildDiscoverySteps(audit.trajectories.retrieval_discovery);
    }
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
