(function (root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) {
    module.exports = api;
  } else {
    root.HalvethQuorumModel = api;
  }
})(typeof globalThis === "object" ? globalThis : this, function () {
  "use strict";

  function integerInRange(name, value, minimum, maximum) {
    if (!Number.isInteger(value) || value < minimum || value > maximum) {
      throw new RangeError(`${name} must be an integer from ${minimum} to ${maximum}`);
    }
  }

  function computeQuorumModel({ n, f, q }) {
    integerInRange("n", n, 1, 1000);
    integerInRange("f", f, 0, n - 1);
    integerInRange("q", q, 1, n);

    const minIntersection = Math.max(0, 2 * q - n);
    const minCorrectIntersection = Math.max(0, minIntersection - f);
    const minSafeQuorum = Math.floor((n + f) / 2) + 1;
    const maxAvailableQuorum = n - f;

    const quorumA = Array.from({ length: q }, (_, index) => index + 1);
    const quorumB = Array.from({ length: q }, (_, index) => n - q + index + 1);
    const quorumASet = new Set(quorumA);
    const quorumBSet = new Set(quorumB);
    const intersection = quorumA.filter((member) => quorumBSet.has(member));

    // Place as many Byzantine members as possible in the overlap to show the
    // worst case for this constructed pair, then fill the remaining fault set.
    const faulty = new Set(intersection.slice(0, f));
    for (let member = 1; member <= n && faulty.size < f; member += 1) {
      faulty.add(member);
    }

    const correctIntersection = intersection.filter((member) => !faulty.has(member));
    const safe = minIntersection > f;
    const live = q <= maxAvailableQuorum;

    return {
      n,
      f,
      q,
      quorumA,
      quorumB,
      intersection,
      faulty: [...faulty].sort((left, right) => left - right),
      correctIntersection,
      minIntersection,
      minCorrectIntersection,
      minSafeQuorum,
      maxAvailableQuorum,
      safe,
      live,
      safeAndLive: safe && live,
      feasibleMembership: n >= 3 * f + 1
    };
  }

  return Object.freeze({ computeQuorumModel });
});
