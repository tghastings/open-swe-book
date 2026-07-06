// §9.4.2 — the buggy boundary guard (`>=` where the spec demands `>`), plus a
// demonstration that the boundary test at 100 fails against it while the
// equivalence-class representatives all pass.
import assert from "node:assert/strict";

let current = 0;
function apply(level: number): void { current = level; }

function setVolume(level: unknown): void {
  if (typeof level !== "number" || !Number.isInteger(level)
      || level < 1 || level >= 100) {          // BUG: >= should be >
    throw new RangeError("level must be 1..100");
  }
  apply(level);
}

const rejected = (level: unknown): boolean => {
  try { setVolume(level); return false; }
  catch (e) { if (e instanceof RangeError) return true; throw e; }
};

assert.ok(!rejected(55));     // C2 representative: accepted — the bug hides
assert.ok(rejected(-3));      // C1 representative: rejected
assert.ok(rejected(250));     // C3 representative: rejected
assert.ok(rejected("loud") && rejected(3.5));  // C4: non-integer rejected
assert.ok(rejected(0));       // just below lower boundary: rejected
assert.ok(!rejected(1) && !rejected(2) && !rejected(99));  // accepted values
assert.ok(rejected(101));     // just above upper boundary: rejected
assert.ok(rejected(100), "boundary test at 100 should expose the >= bug");
console.log("boundary test setVolume(100) fails against the buggy guard");
