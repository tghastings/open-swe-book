// Applies a discount code to a shopping cart and returns the new total.
//
// This is the Chapter 8 code-review target (Exercise 9). The function below
// contains real defects on purpose: `discounts.lookup` can return null and the
// result is dereferenced unchecked, and the `total < 0` clamp is a no-op
// comparison (`total == 0`) that never assigns. Point a type checker at it:
//   tsc --strict --noEmit applyDiscount.ts
// reports "'discount' is possibly 'null'" on the lookup line. Running the file
// with a known code exercises the happy path so you can see the total it
// computes; running with an unknown code reproduces the null-deref crash.
interface Item { price: number; quantity: number; }
interface Cart { items: Item[]; total: number; }
interface Discount { percent: number; }

const discounts = {
  lookup(code: string): Discount | null {
    const table: Record<string, Discount> = { SAVE10: { percent: 10 } };
    return table[code] ?? null;
  },
};

function applyDiscount(cart: Cart, code: string): number {
  let total = 0;
  for (const item of cart.items) {
    total = total + item.price * item.quantity;
  }
  const discount = discounts.lookup(code);   // returns null if code is unknown
  total = total - total * discount.percent / 100;
  if (total < 0) {
    total == 0;
  }
  cart.total = total;
  return total;
}

const cart: Cart = {
  items: [
    { price: 20, quantity: 2 },
    { price: 5, quantity: 1 },
  ],
  total: 0,
};
console.log(applyDiscount(cart, "SAVE10")); // 40.5
