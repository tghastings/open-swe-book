// UNSAFE: the name is concatenated into the SQL text, so an input like
//   Robert'); DROP TABLE appointments; --  is parsed as SQL, not as a name.
interface Database {
  all(query: string, params?: unknown[]): Promise<unknown[]>;
}

function findUnsafe(db: Database, name: string): Promise<unknown[]> {
  const query =
    "SELECT * FROM appointments WHERE patient_name = '" + name + "'";
  return db.all(query); // A05:2025 Injection
}

// SAFE: the ? placeholder binds the name as a parameter; the database never
// parses it as SQL, so the same malicious input is just an unmatched name.
function findSafe(db: Database, name: string): Promise<unknown[]> {
  const query = "SELECT * FROM appointments WHERE patient_name = ?";
  return db.all(query, [name]);
}

// --- runner: a mock db records the query text and bound params it received ---
interface Call {
  query: string;
  params?: unknown[];
}

class MockDb implements Database {
  public last?: Call;
  all(query: string, params?: unknown[]): Promise<unknown[]> {
    this.last = { query, params };
    return Promise.resolve([]);
  }
}

function assert(cond: boolean, msg: string): void {
  if (!cond) throw new Error(msg);
}

void (async (): Promise<void> => {
  const attack = "Robert'); DROP TABLE appointments; --";

  const unsafeDb = new MockDb();
  await findUnsafe(unsafeDb, attack);
  // the attacker's text is welded into the SQL, with no separate params
  assert(
    unsafeDb.last?.query ===
      "SELECT * FROM appointments WHERE patient_name = " +
        "'Robert'); DROP TABLE appointments; --'",
    "unsafe query mismatch",
  );
  assert(unsafeDb.last?.params === undefined, "unsafe should bind no params");

  const safeDb = new MockDb();
  await findSafe(safeDb, attack);
  // the query text is fixed; the attack rides in as a bound parameter
  assert(
    safeDb.last?.query === "SELECT * FROM appointments WHERE patient_name = ?",
    "safe query mismatch",
  );
  assert(
    JSON.stringify(safeDb.last?.params) === JSON.stringify([attack]),
    "safe should bind name as a parameter",
  );

  console.log("ok");
})();
