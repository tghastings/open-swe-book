// §13.6.3 Refactoring Under Green Tests — two moves on one function:
// replace magic number with named constant, then introduce guard clauses.
// TypeScript variant. The same suite runs green before, between, and after the moves.
// Run: node --experimental-strip-types refactoring_moves.ts
import assert from "node:assert/strict";

interface Slot {
  open: boolean;
}

// before: magic number, three-deep nesting
function canBook(patient: string | null, slot: Slot, bookedToday: number): boolean {
  if (patient !== null) {
    if (slot.open) {
      if (bookedToday < 8) {
        return true;
      } else {
        return false;
      }
    } else {
      return false;
    }
  } else {
    return false;
  }
}

// move 1: replace magic number with named constant
const MAX_DAILY_BOOKINGS = 8;

function canBookM1(patient: string | null, slot: Slot, bookedToday: number): boolean {
  if (patient !== null) {
    if (slot.open) {
      if (bookedToday < MAX_DAILY_BOOKINGS) {
        return true;
      } else {
        return false;
      }
    } else {
      return false;
    }
  } else {
    return false;
  }
}

// move 2: introduce guard clauses
function canBookM2(patient: string | null, slot: Slot, bookedToday: number): boolean {
  if (patient === null) return false;
  if (!slot.open) return false;
  return bookedToday < MAX_DAILY_BOOKINGS;
}

type BookFn = (patient: string | null, slot: Slot, bookedToday: number) => boolean;

function runSuite(fn: BookFn): void {
  assert.equal(fn("p1", { open: true }, 0), true);
  assert.equal(fn("p1", { open: true }, 7), true);
  assert.equal(fn("p1", { open: true }, 8), false);
  assert.equal(fn("p1", { open: false }, 0), false);
  assert.equal(fn(null, { open: true }, 0), false);
}

const variants: [string, BookFn][] = [
  ["before", canBook], ["after move 1", canBookM1], ["after move 2", canBookM2],
];
for (const [name, fn] of variants) {
  runSuite(fn);
  console.log(`${name}: 5 tests green`);
}
for (const patient of ["p1", null]) {
  for (const slot of [{ open: true }, { open: false }]) {
    for (let booked = 0; booked < 12; booked++) {
      assert.equal(canBook(patient, slot, booked), canBookM2(patient, slot, booked));
    }
  }
}
console.log("before/after agree on all 48 input combinations");
