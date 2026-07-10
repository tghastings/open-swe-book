// §15.2 Characterization Tests — probe, promote the observed value, probe an edge.
// The book's step-1 probe asserts the deliberately wrong "XXX" and fails with:
//   org.opentest4j.AssertionFailedError: expected: <XXX> but was: <E10>
// Here the probe is wrapped in assertThrows so the suite stays green.
// Run via JUnit console (see code/run-all.sh).
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;
import java.util.Map;

class CharacterizationTests {
  static String legacyFeeCode(String visitType) {   // inherited: no docs, no tests
    return Map.of("exam", "E10", "lab", "L20", "vaccine", "V30")
        .getOrDefault(visitType, "E10");
  }

  @Test void probeFailsAsIntended() {               // the book shows the raw probe failing
    var failure = assertThrows(AssertionError.class,
        () -> assertEquals("XXX", legacyFeeCode("phone")));   // deliberately wrong
    assertTrue(failure.getMessage().contains("expected: <XXX> but was: <E10>"));
  }

  @Test void unknownTypeBillsAsExam() {             // observed value, promoted
    assertEquals("E10", legacyFeeCode("phone"));
  }

  @Test void emptyTypeBillsAsExam() {               // edge probe: pinned, bug or not
    assertEquals("E10", legacyFeeCode(""));
  }
}
