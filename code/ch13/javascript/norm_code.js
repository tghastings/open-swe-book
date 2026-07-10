// Chapter 15, exercise 2 (§15.2) — the inherited, undocumented norm_code, JavaScript variant.
// null plays Python's None; RangeError plays ValueError; the Unicode property
// regex plays str.isalnum (nonempty, all letters/digits).
// Run: node norm_code.js
const assert = require("node:assert/strict");

function normCode(s, strict = false) {
  if (s === null) return strict ? null : "";
  s = s.trim().toUpperCase().replaceAll("-", "");
  if (s.length > 8) s = s.slice(0, 8);
  if (strict && !/^[\p{L}\p{N}]+$/u.test(s)) throw new RangeError(s);
  return s || (strict ? null : "");
}

// characterization pins, matching the Python original's observed behavior
assert.equal(normCode(null), "");
assert.equal(normCode(null, true), null);
assert.equal(normCode(" ab-12 "), "AB12");
assert.equal(normCode("abcdefghij"), "ABCDEFGH");   // truncated to 8
assert.equal(normCode("a!b"), "A!B");               // lenient keeps the junk
assert.throws(() => normCode("a!b", true), { name: "RangeError", message: "A!B" });
assert.throws(() => normCode("", true), RangeError); // empty fails isalnum too
assert.equal(normCode("  "), "");
assert.equal(normCode("--------"), "");
console.log("all characterization pins hold");
