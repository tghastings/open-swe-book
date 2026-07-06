let lastTotal = 0.0;                      // read by Checkout and Receipt

interface Item { qty: number; retail: number; wholesale: number; }
interface Cart { _items: Item[]; }         // internals, not an interface

class PriceEngine {
  compute(cart: Cart, isB2b: boolean): void {
    cart._items.sort((a, b) => a.qty - b.qty);  // reaches into Cart's internals
    let total = 0.0;
    for (const item of cart._items) {
      if (isB2b) {
        total += item.wholesale * item.qty * 0.9;
      } else {
        total += item.retail * item.qty;
      }
    }
    lastTotal = total;
  }
}

class Receipt {
  render(): string { return `Total: $${lastTotal.toFixed(2)}`; }
}

// --- runner (trimmed from the book fence) ---
const cart: Cart = {
  _items: [
    { qty: 2, retail: 10.0, wholesale: 6.0 },
    { qty: 1, retail: 20.0, wholesale: 15.0 },
  ],
};
new PriceEngine().compute(cart, false);
console.log(new Receipt().render());       // Total: $40.00
