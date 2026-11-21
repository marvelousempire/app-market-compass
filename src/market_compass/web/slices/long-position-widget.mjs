import { evaluateLongPosition } from "./long-position-plan.mjs";

/* Grand Canvas micro-slice adapter: reads one form and updates its own output only. */
const form = document.querySelector("#position-form");
const output = document.querySelector("#position-output");
const manifestSummary = document.querySelector("#manifest-summary");
const inventory = document.querySelector("#inventory-items");
const count = document.querySelector("#inventory-count");
const money = n => new Intl.NumberFormat("en-US", {style:"currency", currency:"USD", maximumFractionDigits:4}).format(n);
const number = n => new Intl.NumberFormat("en-US", {maximumFractionDigits:4}).format(n);
const item = (label, value) => {
  const row = document.createElement("div");
  row.className = "result-row";
  const title = document.createElement("span");
  title.textContent = label;
  const metric = document.createElement("strong");
  metric.textContent = value;
  row.append(title, metric);
  return row;
};
if (form && output) {
  form.addEventListener("submit", event => {
    event.preventDefault();
    const payload = Object.fromEntries(new FormData(form).entries());
    output.replaceChildren();
    try {
      const r = evaluateLongPosition(payload);
      output.append(
        item("Risk per share", money(r.riskPerShare)),
        item("Reward per share", money(r.rewardPerShare)),
        item("Reward-to-risk", number(r.rewardToRisk) + " : 1"),
        item("Planned loss at stop", money(r.plannedLoss)),
        item("Potential gain at target", money(r.plannedReward)),
        item("Account at planned risk", r.accountRiskPercent == null ? "Not entered" : number(r.accountRiskPercent) + "%")
      );
      const note = document.createElement("p");
      note.className = "warning";
      note.textContent = r.assumptions.join(" ");
      output.append(note);
      output.dataset.state = "calculated";
    } catch (error) {
      const message = document.createElement("p");
      message.className = "warning";
      message.textContent = error.message;
      output.append(message);
      output.dataset.state = "invalid";
    }
  });
}
fetch("/static/slice-manifest.json", {cache:"no-store"})
  .then(response => { if (!response.ok) throw Error("inventory unavailable"); return response.json(); })
  .then(manifest => {
    const entries = manifest.entries || [];
    const accepted = entries.filter(entry => entry.visible === true);
    const pending = entries.filter(entry => entry.visible === false);
    if (count) count.textContent = entries.length.toString();
    if (manifestSummary) manifestSummary.textContent =
      accepted.length + " source-tested slice; " + pending.length +
      " inventoried entries hidden pending independent acceptance. " +
      "Category counts overlap: they do not represent distinct working applications.";
    if (!inventory) return;
    const byCategory = Object.entries(manifest.counts || {});
    const summary = document.createElement("p");
    summary.textContent = byCategory.map(([k,v]) => k.replaceAll("-", " ") + ": " + v).join(" · ");
    inventory.replaceChildren(summary);
    const group = document.createElement("div");
    group.className = "inventory-grid";
    for (const entry of pending) {
      const row = document.createElement("div");
      const name = document.createElement("span");
      name.textContent = entry.id + " · " + entry.title;
      const status = document.createElement("small");
      status.textContent = "NOT ACCEPTED · " + entry.source;
      row.append(name, status);
      group.append(row);
    }
    inventory.append(group);
  })
  .catch(error => {
    if (manifestSummary) manifestSummary.textContent = "Inventory could not be loaded: " + error.message;
  });
