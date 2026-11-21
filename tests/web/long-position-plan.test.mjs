import test from "node:test";
import assert from "node:assert/strict";
import { evaluateLongPosition } from "../../src/market_compass/web/slices/long-position-plan.mjs";

test("long plan uses actual input arithmetic, not a canned risk label", () => {
  const result = evaluateLongPosition({entry:100,stop:95,target:110,quantity:10,accountSize:10000});
  assert.equal(result.riskPerShare,5);
  assert.equal(result.rewardPerShare,10);
  assert.equal(result.rewardToRisk,2);
  assert.equal(result.plannedLoss,50);
  assert.equal(result.plannedReward,100);
  assert.equal(result.accountRiskPercent,0.5);
  assert.equal(result.scenario,"hypothetical-long-only");
});
test("optional account and fractional quantities work", () => {
  const noAccount = evaluateLongPosition({entry:100,stop:98,target:104,quantity:2});
  assert.equal(noAccount.accountRiskPercent,null);
  assert.equal(noAccount.plannedLoss,4);
  const partial = evaluateLongPosition({entry:20.5,stop:19.5,target:22.5,quantity:2.5,accountSize:500});
  assert.equal(partial.plannedLoss,2.5);
  assert.equal(partial.accountRiskPercent,0.5);
});
test("wrong stop and target sides fail instead of giving a fake score", () => {
  assert.throws(() => evaluateLongPosition({entry:100,stop:105,target:110,quantity:5}), /stop must be below/);
  assert.throws(() => evaluateLongPosition({entry:100,stop:90,target:99,quantity:5}), /target must be above/);
});
test("missing, empty, zero, negative and non-finite inputs fail", () => {
  const base={entry:100,stop:90,target:110,quantity:5};
  assert.throws(() => evaluateLongPosition({...base,quantity:""}), /quantity is required/);
  assert.throws(() => evaluateLongPosition({...base,quantity:-2}), /positive number/);
  assert.throws(() => evaluateLongPosition({...base,accountSize:0}), /positive number/);
  assert.throws(() => evaluateLongPosition({...base,entry:Infinity}), /positive number/);
});
