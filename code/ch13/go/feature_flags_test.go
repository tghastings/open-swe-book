// §14.3.3 — checks for the feature-flag and percentage-rollout examples.
package delivery

import (
	"fmt"
	"strings"
	"testing"
)

func TestReleaseFlag(t *testing.T) {
	for i := 0; i < 10000; i++ {
		u := fmt.Sprintf("user%d", i)
		if !strings.HasPrefix(schedulerPage(u, Flags{NewScheduler: true}), "new") {
			t.Fatalf("flag on: %s did not get the new page", u)
		}
		if !strings.HasPrefix(schedulerPage(u, Flags{NewScheduler: false}), "old") {
			t.Fatalf("flag off: %s did not get the old page", u)
		}
	}
}

func TestPercentageRollout(t *testing.T) {
	hits := 0
	for i := 0; i < 10000; i++ {
		u := fmt.Sprintf("user%d", i)
		if !strings.HasPrefix(schedulerPageRollout(u, Flags{NewSchedulerPct: 0}), "old") {
			t.Fatalf("0%%: %s got the new page", u)
		}
		if !strings.HasPrefix(schedulerPageRollout(u, Flags{NewSchedulerPct: 100}), "new") {
			t.Fatalf("100%%: %s got the old page", u)
		}
		if strings.HasPrefix(schedulerPageRollout(u, Flags{NewSchedulerPct: 3}), "new") {
			hits++
		}
	}
	t.Logf("3%% rollout reached %d of 10000 users (%.1f%%)", hits, float64(hits)/100)
	if hits < 200 || hits > 400 {
		t.Errorf("3%% rollout reached %d of 10000 — bucketing looks broken", hits)
	}
	// the same user always lands in the same bucket, across runs and processes
	a := schedulerPageRollout("user42", Flags{NewSchedulerPct: 3})
	if b := schedulerPageRollout("user42", Flags{NewSchedulerPct: 3}); a != b {
		t.Errorf("user42 changed buckets: %s vs %s", a, b)
	}
}
