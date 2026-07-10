// §9.2.1 — the flagship apply_discount unit-test suite, node:test variant.
const test = require("node:test");
const assert = require("node:assert/strict");

// Reduce price by percent (0..100). Throws RangeError on bad input.
function applyDiscount(price, percent) {
  if (price < 0) throw new RangeError("price must be non-negative");
  if (percent < 0 || percent > 100) throw new RangeError("percent must be in 0..100");
  return Math.round(price * (1 - percent / 100) * 100) / 100;
}

test("no discount", () => assert.equal(applyDiscount(100.0, 0), 100.0));
test("half off", () => assert.equal(applyDiscount(143.0, 50), 71.5));
test("rounds to cents", () => assert.equal(applyDiscount(9.99, 10), 8.99));
test("full discount", () => assert.equal(applyDiscount(40.0, 100), 0.0));
test("rejects bad percent", () => {
  assert.throws(() => applyDiscount(100.0, 150), RangeError);
});
test("free item allowed", () => {
  assert.equal(applyDiscount(0.0, 50), 0.0);  // kills the `price <= 0` mutant
});
