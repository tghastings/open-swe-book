import * as assert from "node:assert";

interface User { id: string; name: string; }
interface Store { find(id: string): User | undefined; save(record: User): void; }

class MemoryUserStore implements Store {
  private records: Record<string, User> = {};
  find(id: string) { return this.records[id]; }
  save(record: User) { this.records[record.id] = record; }
}

const store: Store = new MemoryUserStore();
store.save({ id: "u7", name: "Kati" });
assert.strictEqual(store.find("u7")!.name, "Kati");
console.log("ok");
