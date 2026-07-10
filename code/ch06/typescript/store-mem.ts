interface User { id: string; name: string; }
interface Store { find(id: string): User | undefined; save(record: User): void; }

class MemoryUserStore implements Store {  // the new secret: an in-memory table,
  private records: Record<string, User> = {};   // now behind the same Store type
  find(id: string) { return this.records[id]; }
  save(record: User) { this.records[record.id] = record; }
}

const store: Store = new MemoryUserStore();
store.save({ id: "u7", name: "Kati" });
if (store.find("u7")!.name !== "Kati") throw new Error("mismatch");
console.log(store.find("u7")!.name);
