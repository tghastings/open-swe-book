// §15.2 Characterization Tests — probe, promote the observed value, probe an edge.
// The book's step-1 probe asserts the deliberately wrong "XXX" and fails with
// `legacyFeeCode("phone") = "E10", want "XXX"`. Here the probe asserts the
// observed failure instead, so `go test` stays green.
package delivery

import (
	"cmp"
	"testing"
)

func legacyFeeCode(visitType string) string { // inherited: no docs, no tests
	codes := map[string]string{"exam": "E10", "lab": "L20", "vaccine": "V30"}
	return cmp.Or(codes[visitType], "E10")
}

func TestProbeFailsAsIntended(t *testing.T) { // the book shows got != "XXX" failing
	if got := legacyFeeCode("phone"); got == "XXX" {
		t.Error(`probe unexpectedly passed: got "XXX"`)
	}
}

func TestUnknownTypeBillsAsExam(t *testing.T) { // observed value, promoted
	if got := legacyFeeCode("phone"); got != "E10" {
		t.Errorf("got %q", got)
	}
}

func TestEmptyTypeBillsAsExam(t *testing.T) { // edge probe: pinned, bug or not
	if got := legacyFeeCode(""); got != "E10" {
		t.Errorf("got %q", got)
	}
}
