import * as fs from "node:fs";
import * as assert from "node:assert";

interface User { id: string; name: string; }
interface Store { find(id: string): User | undefined; save(record: User): void; }
class UserStore implements Store {        // the secret: a JSON file
  private path: string;
  constructor(path: string) { this.path = path; }
  find(id: string) { return this.load()[id]; }
  save(record: User) {
    fs.writeFileSync(this.path, JSON.stringify({ ...this.load(), [record.id]: record }));
  }
  private load(): Record<string, User> {
    return fs.existsSync(this.path) ? JSON.parse(fs.readFileSync(this.path, "utf8")) : {};
  }
}
class MemoryUserStore implements Store {  // the new secret: an in-memory table
  private records: Record<string, User> = {};
  find(id: string) { return this.records[id]; }
  save(record: User) { this.records[record.id] = record; }
}

for (const store of [new UserStore("users.json"), new MemoryUserStore()]) {
  store.save({ id: "u7", name: "Dana" });        // the identical caller, untouched
  assert.strictEqual(store.find("u7")!.name, "Dana");
}
