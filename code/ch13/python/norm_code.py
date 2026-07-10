# Chapter 15, exercise 2 (§15.2) — the inherited, undocumented norm_code the exercise
# asks students to characterize, with the pins a probing session produces.
# Runs standalone: python3 norm_code.py
def norm_code(s, strict=False):
  if s is None:
    return "" if not strict else None
  s = s.strip().upper().replace("-", "")
  if len(s) > 8:
    s = s[:8]
  if strict and not s.isalnum():
    raise ValueError(s)
  return s or ("" if not strict else None)

if __name__ == "__main__":
  # characterization pins: observed behavior, promoted into assertions
  assert norm_code(None) == ""
  assert norm_code(None, strict=True) is None
  assert norm_code(" ab-12 ") == "AB12"
  assert norm_code("abcdefghij") == "ABCDEFGH"   # truncated to 8
  assert norm_code("a!b") == "A!B"               # lenient keeps the junk
  for bad in ("a!b", "", "  ", "--------"):      # empty fails isalnum too
    try:
      norm_code(bad, strict=True)
      raise SystemExit(f"expected ValueError for {bad!r}")
    except ValueError:
      pass
  assert norm_code("  ") == ""
  assert norm_code("--------") == ""
  print("all characterization pins hold")
