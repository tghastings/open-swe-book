// §9.2.2 — PriceService plus the integration test that wires the real
// (object-backed) Catalog and Discounts components together.
import test from "node:test";
import assert from "node:assert/strict";

// Reduce price by percent (0..100). Throws RangeError on bad input.
function applyDiscount(price: number, percent: number): number {
  if (price < 0) throw new RangeError("price must be non-negative");
  if (percent < 0 || percent > 100) throw new RangeError("percent must be in 0..100");
  return Math.round(price * (1 - percent / 100) * 100) / 100;
}

class Catalog {
  prices: Record<string, number>;                      // name -> base price
  constructor(prices: Record<string, number>) { this.prices = prices; }
  priceOf(item: string): number { return this.prices[item]; }
}

class Discounts {
  percents: Record<string, number>;                    // name -> percent off
  constructor(percents: Record<string, number>) { this.percents = percents; }
  percentFor(item: string): number { return this.percents[item] ?? 0; }
}

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

test("quote integrates catalog and discounts", () => {
  const catalog = new Catalog({ mug: 12.0 });
  const discounts = new Discounts({ mug: 25 });
  const svc = new PriceService(catalog, discounts);
  assert.equal(svc.quote("mug"), 9.0);  // 12.0 * (1 - 0.25)
});
