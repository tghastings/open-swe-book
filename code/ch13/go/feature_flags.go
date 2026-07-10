// §14.3.3 Feature Flags — a release flag, then the same check as a percentage rollout,
// Go variant. FNV-1a gives a stable per-user bucket; note the buckets differ from the
// CRC-32 buckets of the Python and Ruby variants (any stable hash works, but pick one
// per system, or a user's bucket changes when a service is rewritten).
// Run: go test (feature_flags_test.go exercises this file)
package delivery

import "hash/fnv"

func renderNew(userID string) string { return "new:" + userID } // stand-ins for the
func renderOld(userID string) string { return "old:" + userID } // real pages

type Flags struct {
	NewScheduler    bool
	NewSchedulerPct uint32
}

func schedulerPage(userID string, flags Flags) string {
	if flags.NewScheduler { // release flag: one bit, everyone
		return renderNew(userID)
	}
	return renderOld(userID)
}

// same conditional, new predicate: FNV-1a gives a stable bucket 0..99
func schedulerPageRollout(userID string, flags Flags) string {
	h := fnv.New32a()
	h.Write([]byte(userID))
	if h.Sum32()%100 < flags.NewSchedulerPct {
		return renderNew(userID)
	}
	return renderOld(userID)
}
