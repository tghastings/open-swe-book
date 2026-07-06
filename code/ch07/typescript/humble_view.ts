// §7.3.3 Keep Views Simple — fat view vs. humble view over a view-model
// (clinic scheduler: invoice list with an overdue badge).
import assert from "node:assert";

interface Invoice {
  patientName: string;
  sentOn: Date;
  paid: boolean;
}

const MS_PER_DAY = 86_400_000;

// --- Before: fat view --------------------------------------------------------
class InvoiceWidget {
  render(invoice: Invoice, today: Date): string {
    let text = invoice.patientName;
    if (!invoice.paid && (+today - +invoice.sentOn) / MS_PER_DAY > 30) {
      text += " — OVERDUE";              // a business rule, trapped on screen
    }
    return text;
  }
}

const ana: Invoice = { patientName: "Ana", sentOn: new Date("2026-06-01"), paid: false };
const today = new Date("2026-07-02");
const fat = new InvoiceWidget().render(ana, today);
assert.strictEqual(fat, "Ana — OVERDUE");

// --- After: humble view ------------------------------------------------------
interface InvoiceViewModel {
  text: string;
}

function isOverdue(invoice: Invoice, today: Date): boolean {  // rule tests can reach
  return !invoice.paid && (+today - +invoice.sentOn) / MS_PER_DAY > 30;
}

function invoiceViewModel(invoice: Invoice, today: Date): InvoiceViewModel {
  const badge = isOverdue(invoice, today) ? " — OVERDUE" : "";
  return { text: invoice.patientName + badge };
}

class HumbleInvoiceWidget {              // the book shows this as InvoiceWidget,
  render(vm: InvoiceViewModel): string { // rewritten; renamed so both versions
    return vm.text;                      // run in one file
  }
}

function testUnpaid31DaysIsOverdue(): void {
  const ana: Invoice =
    { patientName: "Ana", sentOn: new Date("2026-06-01"), paid: false };
  assert(isOverdue(ana, new Date("2026-07-02")));
}

assert.strictEqual(new HumbleInvoiceWidget().render(invoiceViewModel(ana, today)), fat);
const ben: Invoice = { patientName: "Ben", sentOn: new Date("2026-06-15"), paid: false };
const cho: Invoice = { patientName: "Cho", sentOn: new Date("2026-05-01"), paid: true };
assert(!isOverdue(ben, today) && !isOverdue(cho, today));
testUnpaid31DaysIsOverdue();
console.log("fat view and humble view render identically; rule tested directly");
