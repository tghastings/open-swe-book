// §7.3.3 Keep Views Simple — fat view vs. humble view over a view-model
// (clinic scheduler: invoice list with an overdue badge).
// The book's test fence uses *testing.T; here the same check runs as a
// plain function so the whole story runs with `go run humble_view.go`.
package main

import (
	"fmt"
	"time"
)

type Invoice struct {
	PatientName string
	SentOn      time.Time
	Paid        bool
}

// --- Before: fat view ---------------------------------------------------------

type InvoiceWidget struct{}

func (w InvoiceWidget) Render(invoice Invoice, today time.Time) string {
	text := invoice.PatientName
	if !invoice.Paid && today.Sub(invoice.SentOn).Hours() > 30*24 {
		text += " — OVERDUE" // a business rule, trapped on screen
	}
	return text
}

// --- After: humble view -------------------------------------------------------

// the rule, extracted where tests reach it
func isOverdue(invoice Invoice, today time.Time) bool {
	return !invoice.Paid && today.Sub(invoice.SentOn).Hours() > 30*24
}

type InvoiceViewModel struct{ Text string }

func invoiceViewModel(invoice Invoice, today time.Time) InvoiceViewModel {
	badge := ""
	if isOverdue(invoice, today) {
		badge = " — OVERDUE"
	}
	return InvoiceViewModel{Text: invoice.PatientName + badge}
}

// the book shows this widget as InvoiceWidget, rewritten; renamed so both
// versions run in one file
type HumbleInvoiceWidget struct{}

func (w HumbleInvoiceWidget) Render(vm InvoiceViewModel) string { return vm.Text }

// the book's fence writes this as TestUnpaid31DaysIsOverdue(t *testing.T)
func testUnpaid31DaysIsOverdue() {
	adilyn := Invoice{"Adilyn", time.Date(2026, 6, 1, 0, 0, 0, 0, time.UTC), false}
	if !isOverdue(adilyn, time.Date(2026, 7, 2, 0, 0, 0, 0, time.UTC)) {
		panic("unpaid invoice sent 31 days ago should be overdue")
	}
}

func main() {
	adilyn := Invoice{"Adilyn", time.Date(2026, 6, 1, 0, 0, 0, 0, time.UTC), false}
	today := time.Date(2026, 7, 2, 0, 0, 0, 0, time.UTC)
	fat := InvoiceWidget{}.Render(adilyn, today)
	humble := HumbleInvoiceWidget{}.Render(invoiceViewModel(adilyn, today))
	if fat != "Adilyn — OVERDUE" || humble != fat {
		panic("fat and humble views should render identically")
	}
	ben := Invoice{"Ben", time.Date(2026, 6, 15, 0, 0, 0, 0, time.UTC), false}
	cho := Invoice{"Cho", time.Date(2026, 5, 1, 0, 0, 0, 0, time.UTC), true}
	if isOverdue(ben, today) || isOverdue(cho, today) {
		panic("recent or paid invoices are not overdue")
	}
	testUnpaid31DaysIsOverdue()
	fmt.Println("fat view and humble view render identically; rule tested directly")
}
