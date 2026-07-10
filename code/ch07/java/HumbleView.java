// §7.3.3 Keep Views Simple — fat view vs. humble view over a view-model
// (clinic scheduler: invoice list with an overdue badge).
// Compact source file (JDK 25+): run with `java -ea HumbleView.java`.
record Invoice(String patientName, LocalDate sentOn, boolean paid) {}

// --- Before: fat view --------------------------------------------------------
class InvoiceWidget {
  String render(Invoice invoice, LocalDate today) {
    String text = invoice.patientName();
    if (!invoice.paid() && ChronoUnit.DAYS.between(invoice.sentOn(), today) > 30) {
      text += " — OVERDUE";              // a business rule, trapped on screen
    }
    return text;
  }
}

// --- After: humble view ------------------------------------------------------
// the rule, extracted where tests reach it
boolean isOverdue(Invoice invoice, LocalDate today) {
  return !invoice.paid() && ChronoUnit.DAYS.between(invoice.sentOn(), today) > 30;
}

record InvoiceViewModel(String text) {}

InvoiceViewModel invoiceViewModel(Invoice invoice, LocalDate today) {
  String badge = isOverdue(invoice, today) ? " — OVERDUE" : "";
  return new InvoiceViewModel(invoice.patientName() + badge);
}

class HumbleInvoiceWidget {              // the book shows this as InvoiceWidget,
  String render(InvoiceViewModel vm) {   // rewritten; renamed so both versions
    return vm.text();                    // run in one file
  }
}

void testUnpaid31DaysIsOverdue() {
  assert isOverdue(new Invoice("Adilyn", LocalDate.of(2026, 6, 1), false),
      LocalDate.of(2026, 7, 2));
}

void main() {
  var adilyn = new Invoice("Adilyn", LocalDate.of(2026, 6, 1), false);
  var today = LocalDate.of(2026, 7, 2);
  var fat = new InvoiceWidget().render(adilyn, today);
  assert fat.equals("Adilyn — OVERDUE");

  var vm = invoiceViewModel(adilyn, today);
  assert new HumbleInvoiceWidget().render(vm).equals(fat);
  assert !isOverdue(new Invoice("Ben", LocalDate.of(2026, 6, 15), false), today);
  assert !isOverdue(new Invoice("Cho", LocalDate.of(2026, 5, 1), true), today);
  testUnpaid31DaysIsOverdue();
  IO.println("fat view and humble view render identically; rule tested directly");
}
