# §9.2.1 — the flagship apply_discount unit-test suite, Minitest variant.
require "minitest/autorun"

# Reduce price by percent (0..100). Raises ArgumentError on bad input.
def apply_discount(price, percent)
  raise ArgumentError, "price must be non-negative" if price < 0
  raise ArgumentError, "percent must be in 0..100" unless (0..100).cover?(percent)
  (price * (1 - percent / 100.0)).round(2)
end

class TestApplyDiscount < Minitest::Test
  def test_no_discount     = assert_equal(100.0, apply_discount(100.0, 0))
  def test_half_off        = assert_equal(71.5, apply_discount(143.0, 50))
  def test_rounds_to_cents = assert_equal(8.99, apply_discount(9.99, 10))
  def test_full_discount   = assert_equal(0.0, apply_discount(40.0, 100))

  def test_rejects_bad_percent
    assert_raises(ArgumentError) { apply_discount(100.0, 150) }
  end

  def test_free_item_allowed
    assert_equal(0.0, apply_discount(0.0, 50))  # kills the `price <= 0` mutant
  end
end
