// full precision: the hand math rounded 20^0.05 to 1.16, so its 55.7 prints as 55.8
const effort = (kloc: number, a = 2.4, b = 1.05): number => a * kloc ** b; // organic
const schedule = (e: number): number => 2.5 * e ** 0.38;   // calendar months

const row = (kloc: number, e: number): string =>
  `${kloc} KLOC: ${e.toFixed(1).padStart(5)} person-months, ` +
  `${schedule(e).toFixed(1)} months`;

const [e20, e40]: [number, number] = [effort(20), effort(40)];
console.log(row(20, e20));
console.log(row(40, e40));
console.log(`doubling factor: ${(e40 / e20).toFixed(2)}`);
