import assert from "node:assert";

class LostLinkBank {                        // the fake — the link drops at step 8
  debits: number[] = [];
  authorize(amount: number): void { throw new Error("link lost"); }
}

class Atm {
  dispensed = 0;
  dispense(amount: number): void { this.dispensed += amount; }
}

function withdraw(atm: Atm, bank: LostLinkBank, amount: number): void {
  try { bank.authorize(amount); }          // steps 8–11 of the basic flow
  catch { return; }                        // B1 — cancel, return the card
  atm.dispense(amount);
  bank.debits.push(amount);
}

const atm = new Atm(), bank = new LostLinkBank();
withdraw(atm, bank, 200);
// the failure postcondition, verbatim
assert(atm.dispensed === 0 && bank.debits.length === 0);
