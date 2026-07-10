// §7.3.3 Keep Views Simple — fat view vs. humble view over a view-model
// (clinic scheduler: invoice list with an overdue badge).
const assert = require("node:assert");

const MS_PER_DAY = 86_400_000;

// --- Before: fat view --------------------------------------------------------
class InvoiceWidget {
  render(invoice, today) {
    let text = invoice.patientName;
    if (!invoice.paid && (today - invoice.sentOn) / MS_PER_DAY > 30) {
      text += " — OVERDUE";              // a business rule, trapped on screen
    }
    return text;
  }
}

const adilyn = { patientName: "Adilyn", sentOn: new Date("2026-06-01"), paid: false };
const today = new Date("2026-07-02");
const fat = new InvoiceWidget().render(adilyn, today);
assert.strictEqual(fat, "Adilyn — OVERDUE");

// --- After: humble view ------------------------------------------------------
function isOverdue(invoice, today) {     // the rule, extracted where tests reach it
  return !invoice.paid && (today - invoice.sentOn) / MS_PER_DAY > 30;
}

function invoiceViewModel(invoice, today) {
  const badge = isOverdue(invoice, today) ? " — OVERDUE" : "";
  return { text: invoice.patientName + badge };
}

class HumbleInvoiceWidget {              // the book shows this as InvoiceWidget,
  render(vm) {                           // rewritten; renamed so both versions
    return vm.text;                      // run in one file
  }
}

function testUnpaid31DaysIsOverdue() {
  const adilyn = { patientName: "Adilyn", sentOn: new Date("2026-06-01"), paid: false };
  assert(isOverdue(adilyn, new Date("2026-07-02")));
}

assert.strictEqual(new HumbleInvoiceWidget().render(invoiceViewModel(adilyn, today)), fat);
const ben = { patientName: "Ben", sentOn: new Date("2026-06-15"), paid: false };
const cho = { patientName: "Cho", sentOn: new Date("2026-05-01"), paid: true };
assert(!isOverdue(ben, today) && !isOverdue(cho, today));
testUnpaid31DaysIsOverdue();
console.log("fat view and humble view render identically; rule tested directly");
