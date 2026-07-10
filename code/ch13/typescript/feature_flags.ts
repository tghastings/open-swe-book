// §14.3.3 Feature Flags — a release flag, then the same check as a percentage rollout,
// TypeScript variant. JS has no built-in string hash, so an FNV-1a helper supplies the
// stable per-user bucket; its buckets differ from the CRC-32 buckets of the Python and
// Ruby variants (any stable hash works, but pick one per system).
// Run: node --experimental-strip-types feature_flags.ts
import assert from "node:assert/strict";

interface Flags {
  newScheduler: boolean;
  newSchedulerPct: number;
}

const renderNew = (userId: string): string => `new:${userId}`; // stand-ins
const renderOld = (userId: string): string => `old:${userId}`;

function bucket(userId: string): number {           // FNV-1a: stable, JS has no
  let h = 0x811c9dc5;                               // built-in string hash
  for (const ch of userId) h = Math.imul(h ^ ch.codePointAt(0)!, 0x01000193);
  return (h >>> 0) % 100;
}

function schedulerPage(userId: string, flags: Flags): string {
  if (flags.newScheduler) {                         // release flag: one bit, everyone
    return renderNew(userId);
  }
  return renderOld(userId);
}

function schedulerPageRollout(userId: string, flags: Flags): string {
  if (bucket(userId) < flags.newSchedulerPct) {     // stable bucket 0..99
    return renderNew(userId);
  }
  return renderOld(userId);
}

const users = Array.from({ length: 10000 }, (_, i) => `user${i}`);
const on: Flags = { newScheduler: true, newSchedulerPct: 0 };
const off: Flags = { newScheduler: false, newSchedulerPct: 0 };
assert.ok(users.every((u) => schedulerPage(u, on).startsWith("new")));
assert.ok(users.every((u) => schedulerPage(u, off).startsWith("old")));
assert.ok(users.every((u) =>
  schedulerPageRollout(u, { newScheduler: false, newSchedulerPct: 0 }).startsWith("old")));
assert.ok(users.every((u) =>
  schedulerPageRollout(u, { newScheduler: false, newSchedulerPct: 100 }).startsWith("new")));
const three: Flags = { newScheduler: false, newSchedulerPct: 3 };
const hits = users.filter((u) => schedulerPageRollout(u, three).startsWith("new")).length;
console.log(`3% rollout reached ${hits} of ${users.length} users (${(hits / 100).toFixed(1)}%)`);
assert.equal(schedulerPageRollout("user42", three), schedulerPageRollout("user42", three));
console.log("all assertions passed");
