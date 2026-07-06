// §9.3.1 — the control-flow-graph worked example: classify a number and,
// for non-negative numbers, sum 1..n. Node comments match the CFG figure.
import assert from "node:assert/strict";

function classifyAndSum(n: number): string {  // node 1  (entry)
  if (n < 0) {                // node 2  (decision)
    return "negative";        // node 3
  }
  let total = 0;              // node 4
  let i = 1;                  // node 4
  while (i <= n) {            // node 5  (decision)
    total += i;               // node 6
    i += 1;                   // node 6
  }
  return `sum=${total}`;      // node 7  (exit)
}

assert.equal(classifyAndSum(-5), "negative"); // T1: node 2 true edge
assert.equal(classifyAndSum(3), "sum=6");     // T2: loop runs three times
assert.equal(classifyAndSum(0), "sum=0");     // loop body never executes
console.log("classifyAndSum: statement/branch example ok");
