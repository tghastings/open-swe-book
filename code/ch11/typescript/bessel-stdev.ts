const cfds: number[] = [2, 4, 5, 5, 7, 8, 9, 10, 12, 14, 23];

const mean: number = cfds.reduce((sum, x) => sum + x, 0) / cfds.length;
const ss: number = cfds.reduce((sum, x) => sum + (x - mean) ** 2, 0);

const s: number = Math.sqrt(ss / (cfds.length - 1)); // divides by n - 1 (Bessel)
const sigma: number = Math.sqrt(ss / cfds.length);   // divides by n

console.log(`s     = ${s.toFixed(2)}`);     // 5.85 — matches the hand computation
console.log(`sigma = ${sigma.toFixed(2)}`); // 5.58
