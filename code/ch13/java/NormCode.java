// Chapter 15, exercise 2 (§15.2) — the inherited, undocumented norm_code, Java variant.
// null plays Python's None; IllegalArgumentException plays ValueError; the
// allMatch check plays str.isalnum (nonempty, all letters/digits).
// Run: java -ea NormCode.java
public class NormCode {
  static String normCode(String s, boolean strict) {
    if (s == null) return strict ? null : "";
    s = s.strip().toUpperCase().replace("-", "");
    if (s.length() > 8) s = s.substring(0, 8);
    boolean alnum = !s.isEmpty() && s.chars().allMatch(Character::isLetterOrDigit);
    if (strict && !alnum) throw new IllegalArgumentException(s);
    return s.isEmpty() ? (strict ? null : "") : s;
  }

  public static void main(String[] args) {
    // characterization pins, matching the Python original's observed behavior
    assert normCode(null, false).equals("");
    assert normCode(null, true) == null;
    assert normCode(" ab-12 ", false).equals("AB12");
    assert normCode("abcdefghij", false).equals("ABCDEFGH"); // truncated to 8
    assert normCode("a!b", false).equals("A!B");             // lenient keeps the junk
    try {
      normCode("a!b", true);
      throw new AssertionError("expected IllegalArgumentException");
    } catch (IllegalArgumentException e) {
      assert e.getMessage().equals("A!B");
    }
    try {
      normCode("", true);                                    // empty fails isalnum too
      throw new AssertionError("expected IllegalArgumentException");
    } catch (IllegalArgumentException e) {
      assert e.getMessage().equals("");
    }
    assert normCode("  ", false).equals("");
    assert normCode("--------", false).equals("");
    System.out.println("all characterization pins hold");
  }
}
