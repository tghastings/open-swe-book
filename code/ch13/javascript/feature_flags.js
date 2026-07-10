// §14.3.3 Feature Flags — a release flag, then the same check as a percentage rollout,
// JavaScript variant. JS has no built-in string hash, so an FNV-1a helper supplies the
// stable per-user bucket; its buckets differ from the CRC-32 buckets of the Python and
// Ruby variants (any stable hash works, but pick one per system).
// Run: node feature_flags.js
const assert = require("node:assert/strict");

const renderNew = (userId) => `new:${userId}`; // stand-ins for the real pages
const renderOld = (userId) => `old:${userId}`;

function bucket(userId) {                            // FNV-1a: stable, JS has no
  let h = 0x811c9dc5;                                // built-in string hash
  for (const ch of userId) h = Math.imul(h ^ ch.codePointAt(0), 0x01000193);
  return (h >>> 0) % 100;
}

function schedulerPage(userId, flags) {
  if (flags.newScheduler) {                          // release flag: one bit, everyone
    return renderNew(userId);
  }
  return renderOld(userId);
}

function schedulerPageRollout(userId, flags) {       // same conditional, new predicate
  if (bucket(userId) < flags.newSchedulerPct) {      // stable bucket 0..99
    return renderNew(userId);
  }
  return renderOld(userId);
}

const users = Array.from({ length: 10000 }, (_, i) => `user${i}`);
assert.ok(users.every((u) => schedulerPage(u, { newScheduler: true }).startsWith("new")));
assert.ok(users.every((u) => schedulerPage(u, { newScheduler: false }).startsWith("old")));
assert.ok(users.every((u) => schedulerPageRollout(u, { newSchedulerPct: 0 }).startsWith("old")));
assert.ok(users.every((u) => schedulerPageRollout(u, { newSchedulerPct: 100 }).startsWith("new")));
const hits = users.filter((u) => schedulerPageRollout(u, { newSchedulerPct: 3 }).startsWith("new")).length;
console.log(`3% rollout reached ${hits} of ${users.length} users (${(hits / 100).toFixed(1)}%)`);
// the same user always lands in the same bucket, across runs and processes
assert.equal(schedulerPageRollout("user42", { newSchedulerPct: 3 }),
  schedulerPageRollout("user42", { newSchedulerPct: 3 }));
console.log("all assertions passed");
