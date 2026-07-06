// Chapter 2, §2.3.2 "Testing: Make It Central to Development" — one red–green
// TDD micro-cycle for the clinic-scheduling app's appointment-slot overlap check.
// Red: with the slotsOverlap function below removed, both tests fail with
// ReferenceError: slotsOverlap is not defined.
// Green: with it in place, both tests pass.
// Run: node --experimental-strip-types tdd_slots_overlap.test.ts
import test from "node:test";
import assert from "node:assert/strict";

type Slot = [string, string];

test("overlapping slots conflict", () => {
  assert.ok(slotsOverlap(["09:00", "09:30"], ["09:15", "09:45"]));
});

test("back-to-back slots do not conflict", () => {
  assert.ok(!slotsOverlap(["09:00", "09:30"], ["09:30", "10:00"]));
});

function slotsOverlap(a: Slot, b: Slot): boolean {
  return a[0] < b[1] && b[0] < a[1];
}
