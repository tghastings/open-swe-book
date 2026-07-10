// Chapter 15, exercise 2 (§15.2) — the inherited, undocumented norm_code, Go variant.
// A nil *string plays Python's None; the ValueError becomes an error return.
// Note: len/[:8] count bytes, not characters — identical for the ASCII codes
// this function sees, another behavior a characterization suite would pin.
// Run: go test (norm_code_test.go exercises this file)
package delivery

import (
	"fmt"
	"strings"
	"unicode"
)

func normCode(s *string, strict bool) (*string, error) {
	if s == nil {
		if strict {
			return nil, nil
		}
		return new(string), nil // ""
	}
	t := strings.ReplaceAll(strings.ToUpper(strings.TrimSpace(*s)), "-", "")
	if len(t) > 8 {
		t = t[:8]
	}
	if strict && !isAlnum(t) {
		return nil, fmt.Errorf("invalid code: %q", t)
	}
	return &t, nil
}

func isAlnum(s string) bool { // Python's isalnum: nonempty, all letters/digits
	for _, r := range s {
		if !unicode.IsLetter(r) && !unicode.IsDigit(r) {
			return false
		}
	}
	return s != ""
}
