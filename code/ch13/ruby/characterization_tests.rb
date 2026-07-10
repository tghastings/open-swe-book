# §15.2 Characterization Tests — probe, promote the observed value, probe an edge.
# The book's step-1 probe asserts the deliberately wrong "XXX" and fails with:
#   Expected: "XXX"
#     Actual: "E10"
# Here the probe is wrapped in assert_raises so the suite stays green.
# Runs standalone: ruby characterization_tests.rb
require "minitest/autorun"

def legacy_fee_code(visit_type)                     # inherited: no docs, no tests
  { "exam" => "E10", "lab" => "L20", "vaccine" => "V30" }.fetch(visit_type, "E10")
end

class TestFeeCode < Minitest::Test
  def test_probe_fails_as_intended                  # the book shows the raw probe failing
    failure = assert_raises(Minitest::Assertion) do
      assert_equal "XXX", legacy_fee_code("phone")  # deliberately wrong
    end
    assert_includes failure.message, 'Expected: "XXX"'
    assert_includes failure.message, 'Actual: "E10"'
  end

  def test_unknown_type_bills_as_exam               # observed value, promoted
    assert_equal "E10", legacy_fee_code("phone")
  end

  def test_empty_type_bills_as_exam                 # edge probe: pinned, bug or not
    assert_equal "E10", legacy_fee_code("")
  end
end
