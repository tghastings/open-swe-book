// §15.3 Refactoring Under Green Tests — two moves on one function:
// replace magic number with named constant, then introduce guard clauses.
// The same suite runs green before, between, and after the moves.
// Run: java -ea RefactoringMoves.java
public class RefactoringMoves {
  record Patient(String id) {}
  record Slot(boolean open) {}

  interface Booker { boolean canBook(Patient patient, Slot slot, int bookedToday); }

  // before: magic number, three-deep nesting
  static boolean canBook(Patient patient, Slot slot, int bookedToday) {
    if (patient != null) {
      if (slot.open()) {
        if (bookedToday < 8) {
          return true;
        } else {
          return false;
        }
      } else {
        return false;
      }
    } else {
      return false;
    }
  }

  // move 1: replace magic number with named constant
  static final int MAX_DAILY_BOOKINGS = 8;

  static boolean canBookM1(Patient patient, Slot slot, int bookedToday) {
    if (patient != null) {
      if (slot.open()) {
        if (bookedToday < MAX_DAILY_BOOKINGS) {
          return true;
        } else {
          return false;
        }
      } else {
        return false;
      }
    } else {
      return false;
    }
  }

  // move 2: introduce guard clauses
  static boolean canBookM2(Patient patient, Slot slot, int bookedToday) {
    if (patient == null) return false;
    if (!slot.open()) return false;
    return bookedToday < MAX_DAILY_BOOKINGS;
  }

  static void runSuite(Booker fn) {
    Patient p = new Patient("p1");
    assert fn.canBook(p, new Slot(true), 0);
    assert fn.canBook(p, new Slot(true), 7);
    assert !fn.canBook(p, new Slot(true), 8);
    assert !fn.canBook(p, new Slot(false), 0);
    assert !fn.canBook(null, new Slot(true), 0);
  }

  public static void main(String[] args) {
    String[] names = {"before", "after move 1", "after move 2"};
    Booker[] fns = {RefactoringMoves::canBook, RefactoringMoves::canBookM1,
        RefactoringMoves::canBookM2};
    for (int i = 0; i < fns.length; i++) {
      runSuite(fns[i]);
      System.out.println(names[i] + ": 5 tests green");
    }
    for (Patient patient : new Patient[]{new Patient("p1"), null}) {
      for (Slot slot : new Slot[]{new Slot(true), new Slot(false)}) {
        for (int booked = 0; booked < 12; booked++) {
          assert canBook(patient, slot, booked) == canBookM2(patient, slot, booked);
        }
      }
    }
    System.out.println("before/after agree on all 48 input combinations");
  }
}
