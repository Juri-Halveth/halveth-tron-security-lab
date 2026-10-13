const test = require("node:test");
const assert = require("node:assert/strict");
const { computeQuorumModel } = require("./quorum-model.js");

test("classic 3f+1 / 2f+1 model has one guaranteed correct overlap", () => {
  const model = computeQuorumModel({ n: 7, f: 2, q: 5 });
  assert.equal(model.minIntersection, 3);
  assert.equal(model.minCorrectIntersection, 1);
  assert.equal(model.safe, true);
  assert.equal(model.live, true);
  assert.equal(model.safeAndLive, true);
  assert.deepEqual(model.intersection, [3, 4, 5]);
});

test("a quorum below the safety bound may remain available", () => {
  const model = computeQuorumModel({ n: 7, f: 2, q: 4 });
  assert.equal(model.minIntersection, 1);
  assert.equal(model.minCorrectIntersection, 0);
  assert.equal(model.safe, false);
  assert.equal(model.live, true);
});

test("a quorum above the availability bound can be safe but unavailable", () => {
  const model = computeQuorumModel({ n: 7, f: 2, q: 6 });
  assert.equal(model.safe, true);
  assert.equal(model.live, false);
  assert.equal(model.safeAndLive, false);
});

test("the minimum feasible quorum matches the 3f+1 example", () => {
  const model = computeQuorumModel({ n: 4, f: 1, q: 3 });
  assert.equal(model.minSafeQuorum, 3);
  assert.equal(model.maxAvailableQuorum, 3);
  assert.equal(model.feasibleMembership, true);
});

test("infeasible membership parameters remain explicit", () => {
  const model = computeQuorumModel({ n: 5, f: 2, q: 4 });
  assert.equal(model.feasibleMembership, false);
  assert.equal(model.safe, true);
  assert.equal(model.live, false);
});

test("invalid counts are rejected instead of silently normalized", () => {
  assert.throws(() => computeQuorumModel({ n: 7, f: -1, q: 5 }), RangeError);
  assert.throws(() => computeQuorumModel({ n: 7, f: 2, q: 8 }), RangeError);
  assert.throws(() => computeQuorumModel({ n: 7.5, f: 2, q: 5 }), RangeError);
});
