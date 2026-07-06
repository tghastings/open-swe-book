// §9.2.2 — PriceService wires two collaborators behind the Catalog and
// Discounts interfaces; a small runner exercises it standalone.
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
    const base = this.catalog.priceOf(item);
    const pct = this.discounts.percentFor(item);
    return applyDiscount(base, pct);
  }
}

const svc = new PriceService(
  { priceOf: () => 12.0 },
  { percentFor: () => 25 },
);
assert.equal(svc.quote("mug"), 9.0);
console.log("PriceService quote ok");
