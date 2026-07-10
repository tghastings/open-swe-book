# §7.3.3 Keep Views Simple — fat view vs. humble view over a view-model
# (clinic scheduler: invoice list with an overdue badge).
require "date"

Invoice = Struct.new(:patient_name, :sent_on, :paid)

# --- Before: fat view ---------------------------------------------------------
class InvoiceWidget
  def render(invoice, today)
    text = invoice.patient_name
    if !invoice.paid && (today - invoice.sent_on) > 30
      text += " — OVERDUE"             # a business rule, trapped on screen
    end
    text
  end
end

adilyn = Invoice.new("Adilyn", Date.new(2026, 6, 1), false)
today = Date.new(2026, 7, 2)
fat = InvoiceWidget.new.render(adilyn, today)
raise unless fat == "Adilyn — OVERDUE"

# --- After: humble view -------------------------------------------------------
def overdue?(invoice, today)             # the rule, extracted where tests reach it
  !invoice.paid && (today - invoice.sent_on) > 30
end

def invoice_view_model(invoice, today)
  badge = overdue?(invoice, today) ? " — OVERDUE" : ""
  { text: invoice.patient_name + badge }
end

class HumbleInvoiceWidget                # the book shows this as InvoiceWidget,
  def render(vm)                         # rewritten; renamed so both versions
    vm[:text]                            # run in one file
  end
end

def test_unpaid_31_days_is_overdue
  adilyn = Invoice.new("Adilyn", Date.new(2026, 6, 1), false)
  raise unless overdue?(adilyn, Date.new(2026, 7, 2))
end

raise unless HumbleInvoiceWidget.new.render(invoice_view_model(adilyn, today)) == fat
raise if overdue?(Invoice.new("Ben", Date.new(2026, 6, 15), false), today)
raise if overdue?(Invoice.new("Cho", Date.new(2026, 5, 1), true), today)
test_unpaid_31_days_is_overdue
puts "fat view and humble view render identically; rule tested directly"
