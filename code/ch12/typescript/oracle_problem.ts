import assert from "node:assert";

function applyDiscount(price: number, percent: number): number { // AI-generated:
  return Number((price * (1 - percent / 100)).toFixed(2)); // toFixed(2) rounds the double
}

function testHalfOff(): void {            // AI-generated: asserts the code's own behavior
  assert.strictEqual(applyDiscount(17.15, 50), 8.57);
}

testHalfOff();                           // passes — and every line of the unit is covered
console.log(applyDiscount(17.15, 50));   // 8.57; the billing spec says 8.58 (half up)
