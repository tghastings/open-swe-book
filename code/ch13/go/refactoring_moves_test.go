// §15.3 — the green net: the same suite passes before, between, and after the moves,
// and before/after agree on all 48 input combinations.
package delivery

import "testing"

func runSuite(t *testing.T, name string, fn func(*Patient, Slot, int) bool) {
	t.Helper()
	p := &Patient{ID: "p1"}
	cases := []struct {
		patient *Patient
		slot    Slot
		booked  int
		want    bool
	}{
		{p, Slot{Open: true}, 0, true},
		{p, Slot{Open: true}, 7, true},
		{p, Slot{Open: true}, 8, false},
		{p, Slot{Open: false}, 0, false},
		{nil, Slot{Open: true}, 0, false},
	}
	for _, c := range cases {
		if got := fn(c.patient, c.slot, c.booked); got != c.want {
			t.Errorf("%s: fn(%v, %v, %d) = %v, want %v",
				name, c.patient, c.slot, c.booked, got, c.want)
		}
	}
}

func TestSuiteGreenAcrossMoves(t *testing.T) {
	runSuite(t, "before", canBook)
	runSuite(t, "after move 1", canBookM1)
	runSuite(t, "after move 2", canBookM2)
}

func TestBeforeAfterAgreeOnAllCombinations(t *testing.T) {
	for _, patient := range []*Patient{{ID: "p1"}, nil} {
		for _, slot := range []Slot{{Open: true}, {Open: false}} {
			for booked := 0; booked < 12; booked++ {
				if canBook(patient, slot, booked) != canBookM2(patient, slot, booked) {
					t.Errorf("disagree at (%v, %v, %d)", patient, slot, booked)
				}
			}
		}
	}
}
