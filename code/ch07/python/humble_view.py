# §7.3.3 Keep Views Simple — fat view vs. humble view over a view-model
# (clinic scheduler: invoice list with an overdue badge).
from dataclasses import dataclass
from datetime import date

@dataclass
class Invoice:
  patient_name: str
  sent_on: date
  paid: bool

# --- Before: fat view -------------------------------------------------------
class InvoiceWidget:
  def render(self, invoice, today):
    text = invoice.patient_name
    if not invoice.paid and (today - invoice.sent_on).days > 30:
      text += " — OVERDUE"         # a business rule, trapped on screen
    return text

fat = InvoiceWidget().render(Invoice("Adilyn", date(2026, 6, 1), False), date(2026, 7, 2))
assert fat == "Adilyn — OVERDUE"

# --- After: humble view -----------------------------------------------------
def is_overdue(invoice, today):          # the rule, extracted where tests reach it
  return not invoice.paid and (today - invoice.sent_on).days > 30

def invoice_view_model(invoice, today):
  badge = " — OVERDUE" if is_overdue(invoice, today) else ""
  return {"text": invoice.patient_name + badge}

class HumbleInvoiceWidget:               # the book shows this as InvoiceWidget,
  def render(self, vm):                # rewritten; renamed so both versions
    return vm["text"]                # run in one file

def test_unpaid_31_days_is_overdue():
  assert is_overdue(Invoice("Adilyn", sent_on=date(2026, 6, 1), paid=False), date(2026, 7, 2))

vm = invoice_view_model(Invoice("Adilyn", date(2026, 6, 1), False), date(2026, 7, 2))
assert HumbleInvoiceWidget().render(vm) == "Adilyn — OVERDUE"
assert not is_overdue(Invoice("Ben", date(2026, 6, 15), False), date(2026, 7, 2))
assert not is_overdue(Invoice("Cho", date(2026, 5, 1), True), date(2026, 7, 2))
test_unpaid_31_days_is_overdue()
print("fat view and humble view render identically; rule tested directly")
