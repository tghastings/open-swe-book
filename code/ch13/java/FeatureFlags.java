// §14.3.3 Feature Flags — a release flag, then the same check as a percentage rollout,
// Java variant. String.hashCode() is fixed by the Java spec, so buckets are stable
// across JVMs — but they differ from the CRC-32 buckets of the Python and Ruby
// variants (any stable hash works, but pick one per system).
// Run: java -ea FeatureFlags.java
public class FeatureFlags {
  record Flags(boolean newScheduler, int newSchedulerPct) {}

  static String renderNew(String userId) { return "new:" + userId; } // stand-ins for
  static String renderOld(String userId) { return "old:" + userId; } // the real pages

  static String schedulerPage(String userId, Flags flags) {
    if (flags.newScheduler()) {                     // release flag: one bit, everyone
      return renderNew(userId);
    }
    return renderOld(userId);
  }

  static String schedulerPageRollout(String userId, Flags flags) { // same conditional
    // String.hashCode() is spec-fixed, so buckets are stable across JVMs — but they
    // differ from the CRC-32 buckets the Python and Ruby variants compute
    if (Math.floorMod(userId.hashCode(), 100) < flags.newSchedulerPct()) { // 0..99
      return renderNew(userId);
    }
    return renderOld(userId);
  }

  public static void main(String[] args) {
    int hits = 0;
    for (int i = 0; i < 10_000; i++) {
      String u = "user" + i;
      assert schedulerPage(u, new Flags(true, 0)).startsWith("new");
      assert schedulerPage(u, new Flags(false, 0)).startsWith("old");
      assert schedulerPageRollout(u, new Flags(false, 0)).startsWith("old");
      assert schedulerPageRollout(u, new Flags(false, 100)).startsWith("new");
      if (schedulerPageRollout(u, new Flags(false, 3)).startsWith("new")) hits++;
    }
    System.out.printf("3%% rollout reached %d of 10000 users (%.1f%%)%n",
        hits, hits / 100.0);
    // the same user always lands in the same bucket, across runs and processes
    assert schedulerPageRollout("user42", new Flags(false, 3))
        .equals(schedulerPageRollout("user42", new Flags(false, 3)));
    System.out.println("all assertions passed");
  }
}
