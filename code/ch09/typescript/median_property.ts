// §9.1.4 Test Oracles — property oracle for median(xs), as a property-based
// test. Uses fast-check when installed (npm install fast-check); otherwise
// falls back to a hand-rolled random-input loop over the same two properties.

function median(xs: number[]): number {
  const ys = xs.slice().sort((a, b) => a - b);
  return ys[Math.floor(xs.length / 2)];   // middle element (upper median)
}

function propertiesHold(xs: number[]): void {
  const m = median(xs);
  if (m !== median(xs.slice().reverse())) throw new Error(`order dependence on ${xs}`);
  if (!xs.includes(m)) throw new Error(`median ${m} not in ${xs}`);
}

let fc: any = null;
try { fc = require("fast-check"); } catch { /* not installed: use the fallback */ }

if (fc) {
  fc.assert(
    fc.property(fc.array(fc.integer(), { minLength: 1 }), (xs: number[]) => {
      propertiesHold(xs);
      return true;
    }),
  );
  console.log("fast-check: both properties held on generated lists");
} else {
  for (let i = 0; i < 10000; i++) {
    const n = 1 + Math.floor(Math.random() * 50);
    const xs = Array.from({ length: n }, () => Math.floor(Math.random() * 2001) - 1000);
    propertiesHold(xs);
  }
  console.log("10000 random lists: both properties held");
}
