// §9.2.1 — the flagship apply_discount unit-test suite, JUnit 5 variant.
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

class ApplyDiscountTest {
  /** Reduce price by percent (0..100). Throws IllegalArgumentException on bad input. */
  static double applyDiscount(double price, double percent) {
    if (price < 0) throw new IllegalArgumentException("price must be non-negative");
    if (percent < 0 || percent > 100)
      throw new IllegalArgumentException("percent must be in 0..100");
    return Math.round(price * (1 - percent / 100) * 100) / 100.0;
  }

  @Test void noDiscount()    { assertEquals(100.0, applyDiscount(100.0, 0)); }
  @Test void halfOff()       { assertEquals(71.5, applyDiscount(143.0, 50)); }
  @Test void roundsToCents() { assertEquals(8.99, applyDiscount(9.99, 10)); }
  @Test void fullDiscount()  { assertEquals(0.0, applyDiscount(40.0, 100)); }
  @Test void freeItemAllowed() {
    assertEquals(0.0, applyDiscount(0.0, 50));  // kills the `price <= 0` mutant
  }
  @Test void rejectsBadPercent() {
    assertThrows(IllegalArgumentException.class, () -> applyDiscount(100.0, 150));
  }
}
