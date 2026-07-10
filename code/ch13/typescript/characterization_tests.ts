// §15.2 Characterization Tests — probe, promote the observed value, probe an edge.
// TypeScript variant. The book's step-1 probe asserts the deliberately wrong "XXX"
// and fails with:
//   AssertionError [ERR_ASSERTION]: Expected values to be strictly equal:
//   'E10' !== 'XXX'
// Here the probe is wrapped in assert.throws so the suite stays green.
// Run: node --experimental-strip-types characterization_tests.ts
import test from "node:test";
import assert from "node:assert/strict";

function legacyFeeCode(visitType: string): string {  // inherited: no docs, no tests
  const codes: Record<string, string> =
    { exam: "E10", lab: "L20", vaccine: "V30" };
  return codes[visitType] ?? "E10";
}

test("probe fails as intended", () => {              // the book shows the raw probe fail
  assert.throws(
    () => assert.equal(legacyFeeCode("phone"), "XXX"), // deliberately wrong
    { name: "AssertionError", actual: "E10", expected: "XXX" }
  );
});

test("unknown type bills as exam", () => {           // observed value, promoted
  assert.equal(legacyFeeCode("phone"), "E10");
});

test("empty type bills as exam", () => {             // edge probe: pinned, bug or not
  assert.equal(legacyFeeCode(""), "E10");
});
