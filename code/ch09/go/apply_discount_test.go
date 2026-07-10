// §9.2.1 — the flagship apply_discount unit-test suite, Go testing variant.

package discount

import "testing"

func TestApplyDiscount(t *testing.T) {
	cases := []struct {
		name                 string
		price, percent, want float64
	}{
		{"no discount", 100.0, 0, 100.0},
		{"half off", 143.0, 50, 71.5},
		{"rounds to cents", 9.99, 10, 8.99},
		{"full discount", 40.0, 100, 0.0},
	}
	for _, c := range cases {
		t.Run(c.name, func(t *testing.T) {
			if got, err := ApplyDiscount(c.price, c.percent); err != nil || got != c.want {
				t.Errorf("got %v, %v; want %v", got, err, c.want)
			}
		})
	}
}

func TestRejectsBadPercent(t *testing.T) {
	if _, err := ApplyDiscount(100.0, 150); err == nil {
		t.Error("want error for percent 150, got nil")
	}
}

func TestFreeItemAllowed(t *testing.T) { // kills the `price <= 0` mutant
	if got, err := ApplyDiscount(0.0, 50); err != nil || got != 0.0 {
		t.Errorf("got %v, %v; want 0.0", got, err)
	}
}
