function lineTotal(price: number, quantity: number): number {
  return price * quantity;
}

const price = "9.99";       // read from a CSV row, still a string
const total = lineTotal(price, 3);
console.log(total);         // node strips types and prints 29.97
// tsc: Argument of type 'string' is not assignable to parameter of type 'number'.
