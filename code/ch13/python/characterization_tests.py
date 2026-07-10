# §15.2 Characterization Tests — probe, promote the observed value, probe an edge.
# Runs standalone: python3 characterization_tests.py
# Under pytest, the step-1 probe fails by design with the line the book shows:
#   AssertionError: assert 'E10' == 'XXX'

def legacy_fee_code(visit_type):                    # inherited: no docs, no tests
  return {"exam": "E10", "lab": "L20", "vaccine": "V30"}.get(visit_type, "E10")

def test_probe_unknown_type():
  assert legacy_fee_code("phone") == "XXX"        # deliberately wrong

def test_unknown_type_bills_as_exam():              # observed value, promoted
  assert legacy_fee_code("phone") == "E10"

def test_empty_type_bills_as_exam():                # edge probe: pinned, bug or not
  assert legacy_fee_code("") == "E10"

if __name__ == "__main__":
  try:
    test_probe_unknown_type()
  except AssertionError:
    print("probe failed as intended; observed value:", legacy_fee_code("phone"))
  test_unknown_type_bills_as_exam()
  test_empty_type_bills_as_exam()
  print("2 promoted characterization tests pass")
