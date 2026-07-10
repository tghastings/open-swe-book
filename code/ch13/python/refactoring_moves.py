# §15.3 Refactoring Under Green Tests — two moves on one function:
# replace magic number with named constant, then introduce guard clauses.
# The same suite runs green before, between, and after the moves.
# Runs standalone: python3 refactoring_moves.py
from collections import namedtuple

Slot = namedtuple("Slot", "open")

# before: magic number, three-deep nesting
def can_book(patient, slot, booked_today):
  if patient is not None:
    if slot.open:
      if booked_today < 8:
        return True
      else:
        return False
    else:
      return False
  else:
    return False

# move 1: replace magic number with named constant
MAX_DAILY_BOOKINGS = 8

def can_book_m1(patient, slot, booked_today):
  if patient is not None:
    if slot.open:
      if booked_today < MAX_DAILY_BOOKINGS:
        return True
      else:
        return False
    else:
      return False
  else:
    return False

# move 2: introduce guard clauses
def can_book_m2(patient, slot, booked_today):
  if patient is None:
    return False
  if not slot.open:
    return False
  return booked_today < MAX_DAILY_BOOKINGS

def run_suite(fn):
  assert fn("p1", Slot(open=True), 0) is True
  assert fn("p1", Slot(open=True), 7) is True
  assert fn("p1", Slot(open=True), 8) is False
  assert fn("p1", Slot(open=False), 0) is False
  assert fn(None, Slot(open=True), 0) is False

if __name__ == "__main__":
  for name, fn in [("before", can_book), ("after move 1", can_book_m1),
          ("after move 2", can_book_m2)]:
    run_suite(fn)
    print(f"{name}: 5 tests green")
  for patient in ("p1", None):
    for slot in (Slot(True), Slot(False)):
      for booked in range(0, 12):
        assert can_book(patient, slot, booked) == can_book_m2(patient, slot, booked)
  print("before/after agree on all 48 input combinations")
