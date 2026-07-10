# §15.3 Refactoring Under Green Tests — two moves on one function:
# replace magic number with named constant, then introduce guard clauses.
# The same suite runs green before, between, and after the moves.
# Runs standalone: ruby refactoring_moves.rb
Slot = Struct.new(:open)

# before: magic number, three-deep nesting
def can_book(patient, slot, booked_today)
  if !patient.nil?
    if slot.open
      if booked_today < 8
        true
      else
        false
      end
    else
      false
    end
  else
    false
  end
end

# move 1: replace magic number with named constant
MAX_DAILY_BOOKINGS = 8

def can_book_m1(patient, slot, booked_today)
  if !patient.nil?
    if slot.open
      if booked_today < MAX_DAILY_BOOKINGS
        true
      else
        false
      end
    else
      false
    end
  else
    false
  end
end

# move 2: introduce guard clauses
def can_book_m2(patient, slot, booked_today)
  return false if patient.nil?
  return false unless slot.open
  booked_today < MAX_DAILY_BOOKINGS
end

def run_suite(fn)
  raise unless fn.call("p1", Slot.new(true), 0) == true
  raise unless fn.call("p1", Slot.new(true), 7) == true
  raise unless fn.call("p1", Slot.new(true), 8) == false
  raise unless fn.call("p1", Slot.new(false), 0) == false
  raise unless fn.call(nil, Slot.new(true), 0) == false
end

{ "before" => method(:can_book), "after move 1" => method(:can_book_m1),
  "after move 2" => method(:can_book_m2) }.each do |name, fn|
  run_suite(fn)
  puts "#{name}: 5 tests green"
end
["p1", nil].each do |patient|
  [Slot.new(true), Slot.new(false)].each do |slot|
    (0...12).each do |booked|
      raise unless can_book(patient, slot, booked) == can_book_m2(patient, slot, booked)
    end
  end
end
puts "before/after agree on all 48 input combinations"
