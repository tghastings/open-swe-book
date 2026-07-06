// §9.2.1 Unit Testing — the three test doubles (stub, mock, fake) standing in
// for the discounts dependency of PriceService (defined in §9.2.2, included
// here so the file runs standalone with `node test_doubles.ts`).
import assert from "node:assert/strict";

// Reduce price by percent (0..100). Throws RangeError on bad input.
function applyDiscount(price: number, percent: number): number {
  if (price < 0) throw new RangeError("price must be non-negative");
  if (percent < 0 || percent > 100) throw new RangeError("percent must be in 0..100");
  return Math.round(price * (1 - percent / 100) * 100) / 100;
}

interface Catalog { priceOf(item: string): number; }
interface Discounts { percentFor(item: string): number; }

class PriceService {
  catalog: Catalog;      // unit A: name -> base price
  discounts: Discounts;  // unit B: name -> percent off
  constructor(catalog: Catalog, discounts: Discounts) {
    this.catalog = catalog;
    this.discounts = discounts;
  }
  quote(item: string): number {
    return applyDiscount(this.catalog.priceOf(item), this.discounts.percentFor(item));
  }
}

// --- stub: canned answers, nothing more ---
class StubCatalog implements Catalog {
  priceOf(item: string): number { return 12.0; }   // every item costs 12.0
}

class StubDiscounts implements Discounts {
  percentFor(item: string): number { return 25; }  // canned answer, whatever the item
}

{
  const svc = new PriceService(new StubCatalog(), new StubDiscounts());
  assert.equal(svc.quote("mug"), 9.0);  // 12.0 * (1 - 0.25)
}

// --- mock: records the interaction so the test can assert on it ---
class MockDiscounts implements Discounts {
  calls: string[] = [];
  percentFor(item: string): number {
    this.calls.push(item);
    return 25;
  }
}

const mock = new MockDiscounts();
new PriceService(new StubCatalog(), mock).quote("mug");
assert.deepEqual(mock.calls, ["mug"]);  // called exactly once, with "mug"

// --- fake: a lightweight working implementation ---
class FakeDiscounts implements Discounts {
  private table: Record<string, number>;
  constructor(table: Record<string, number>) { this.table = { ...table }; }  // stand-in
  percentFor(item: string): number { return this.table[item] ?? 0; }
}

{
  const svc = new PriceService(new StubCatalog(), new FakeDiscounts({ mug: 25 }));
  assert.equal(svc.quote("mug"), 9.0);
  assert.equal(svc.quote("bowl"), 12.0);  // unknown item: no discount
}

console.log("stub, mock, and fake examples all passed");
