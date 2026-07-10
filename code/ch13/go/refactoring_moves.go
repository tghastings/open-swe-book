// §15.3 Refactoring Under Green Tests — two moves on one function:
// replace magic number with named constant, then introduce guard clauses.
// The same suite runs green before, between, and after the moves.
// Run: go test (refactoring_moves_test.go exercises this file)
package delivery

type Patient struct{ ID string }
type Slot struct{ Open bool }

// before: magic number, three-deep nesting
func canBook(patient *Patient, slot Slot, bookedToday int) bool {
	if patient != nil {
		if slot.Open {
			if bookedToday < 8 {
				return true
			} else {
				return false
			}
		} else {
			return false
		}
	} else {
		return false
	}
}

// move 1: replace magic number with named constant
const maxDailyBookings = 8

func canBookM1(patient *Patient, slot Slot, bookedToday int) bool {
	if patient != nil {
		if slot.Open {
			if bookedToday < maxDailyBookings {
				return true
			} else {
				return false
			}
		} else {
			return false
		}
	} else {
		return false
	}
}

// move 2: introduce guard clauses
func canBookM2(patient *Patient, slot Slot, bookedToday int) bool {
	if patient == nil {
		return false
	}
	if !slot.Open {
		return false
	}
	return bookedToday < maxDailyBookings
}
