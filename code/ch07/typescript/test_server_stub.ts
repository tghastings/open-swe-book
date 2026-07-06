// §7.5.2 Deploying Test Servers — a stub HTTP server programmed to return 500,
// asserting the clinic client's fallback behavior.
import assert from "node:assert";
import http from "node:http";
import type { AddressInfo } from "node:net";

async function fetchAppointments(baseUrl: string): Promise<Buffer | never[]> {
  const resp = await fetch(baseUrl + "/appointments");
  if (!resp.ok) return [];               // fallback: empty schedule, not a crash
  return Buffer.from(await resp.arrayBuffer());
}

const stub = http.createServer((req, res) => res.writeHead(500).end());
stub.listen(0, "127.0.0.1", async () => {
  const { port } = stub.address() as AddressInfo;
  const base = `http://127.0.0.1:${port}`;
  assert.deepStrictEqual(await fetchAppointments(base), []);
  stub.close();
  console.log("client fell back to an empty schedule on 500");
});
