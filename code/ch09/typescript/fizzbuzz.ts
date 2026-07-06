// Ch. 9 exercises — fizzbuzz, the subject of the draw-a-CFG exercise.
import assert from "node:assert/strict";

function fizzbuzz(n: number): string {
  if (n % 15 === 0) {
    return "FizzBuzz";
  } else if (n % 3 === 0) {
    return "Fizz";
  } else if (n % 5 === 0) {
    return "Buzz";
  } else {
    return String(n);
  }
}

assert.equal(fizzbuzz(15), "FizzBuzz");
assert.equal(fizzbuzz(9), "Fizz");
assert.equal(fizzbuzz(10), "Buzz");
assert.equal(fizzbuzz(7), "7");
console.log("fizzbuzz exercise example ok");
