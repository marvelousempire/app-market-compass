/** Pure, offline, independently testable CCK-style long position plan. No market feeds, execution, or score mutation. */
export function evaluateLongPosition(input) {
  const positive = (key, optional = false) => {
    const raw = input[key];
    if (raw === undefined || raw === null || String(raw).trim() === "") {
      if (optional) return null;
      throw new Error(key + " is required.");
    }
    const value = Number(raw);
    if (!Number.isFinite(value) || value <= 0) throw new Error(key + " must be a positive number.");
    return value;
  };
  const round = value => Math.round((value + Number.EPSILON) * 10000) / 10000;
  const entry = positive("entry");
  const stop = positive("stop");
  const target = positive("target");
  const quantity = positive("quantity");
  const accountSize = positive("accountSize", true);
  if (stop >= entry) throw new Error("For a long-position plan, stop must be below entry.");
  if (target <= entry) throw new Error("For a long-position plan, target must be above entry.");
  const riskPerShare = entry - stop;
  const rewardPerShare = target - entry;
  return {
    scenario: "hypothetical-long-only",
    riskPerShare: round(riskPerShare),
    rewardPerShare: round(rewardPerShare),
    rewardToRisk: round(rewardPerShare / riskPerShare),
    plannedLoss: round(riskPerShare * quantity),
    plannedReward: round(rewardPerShare * quantity),
    accountRiskPercent: accountSize === null ? null : round(riskPerShare * quantity / accountSize * 100),
    assumptions: ["Inputs are manually entered, not market quotes.", "Stop orders may fill worse than planned; gaps, fees, slippage and taxes are excluded.", "This is arithmetic, not a probability estimate or an investment recommendation."]
  };
}
