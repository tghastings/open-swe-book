import { open } from "node:fs/promises";

interface Discounts {
  percentFor(item: string): number;
}

async function exportPrices(
  catalog: Record<string, number>,
  discounts: Discounts,
  path: string,
): Promise<string | null> {
  const out = await open(path, "w");
  await out.write("item,price\n");
  for (const item of Object.keys(catalog).sort()) {
    const pct = discounts.percentFor(item);
    if (pct < 0 || pct > 100) {
      return null;                // error path: `out` is never closed
    }
    const final = Math.round(catalog[item] * (1 - pct / 100) * 100) / 100;
    await out.write(`${item},${final}\n`);
  }
  await out.close();
  return path;
}
// node, when the abandoned handle is finally garbage-collected:
//   Warning: Closing file descriptor 20 on garbage collection

// --- runner (trimmed from the book fence) ---
const disc: Discounts = { percentFor: (item) => (item === "pen" ? 10 : 0) };
void (async () => {
  const result = await exportPrices({ pen: 1.5, mug: 8 }, disc, "/tmp/out.csv");
  console.log(result);
})();
