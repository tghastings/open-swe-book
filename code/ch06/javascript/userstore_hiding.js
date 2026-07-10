// Chapter 6, §6.2.1 (The Modularity Principle) — information hiding.
// The same UserStore surface with two different secrets; the caller never changes.
// Run: node userstore_hiding.js
const fs = require("node:fs"), assert = require("node:assert");

class UserStore {                       // the secret: a JSON file
  constructor(path) { this.path = path; }
  find(id) { return this.load()[id]; }
  save(record) {
    const users = { ...this.load(), [record.id]: record };
    fs.writeFileSync(this.path, JSON.stringify(users));
  }
  load() {
    if (!fs.existsSync(this.path)) return {};
    return JSON.parse(fs.readFileSync(this.path, "utf8"));
  }
}

class MemoryUserStore {                 // the new secret: an in-memory table.
  constructor() { this.records = {}; }  // No interface to declare — any object
  find(id) { return this.records[id]; } // shaped like find/save will do.
  save(record) { this.records[record.id] = record; }
}

for (const store of [new UserStore("users.json"), new MemoryUserStore()]) {
  store.save({ id: "u7", name: "Kati" });        // the identical caller, untouched
  assert.strictEqual(store.find("u7").name, "Kati");
}

fs.rmSync("users.json", { force: true });        // cleanup
console.log("both versions satisfy the same caller: OK");
