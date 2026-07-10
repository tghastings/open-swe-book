// Chapter 15, exercise 2 (§15.2) — characterization pins for norm_code, matching the
// Python original's observed behavior on every probed input class.
package delivery

import "testing"

func str(s string) *string { return &s }

func TestNormCodeCharacterization(t *testing.T) {
	cases := []struct {
		name   string
		in     *string
		strict bool
		want   *string
		erring bool
	}{
		{"nil lenient", nil, false, str(""), false},
		{"nil strict", nil, true, nil, false},
		{"hyphens and spaces", str(" ab-12 "), false, str("AB12"), false},
		{"over-length truncates", str("abcdefghij"), false, str("ABCDEFGH"), false},
		{"non-alnum lenient", str("a!b"), false, str("A!B"), false},
		{"non-alnum strict", str("a!b"), true, nil, true},
		{"empty strict raises", str(""), true, nil, true},
		{"whitespace lenient", str("  "), false, str(""), false},
		{"all hyphens lenient", str("--------"), false, str(""), false},
	}
	for _, c := range cases {
		got, err := normCode(c.in, c.strict)
		if c.erring != (err != nil) {
			t.Errorf("%s: err = %v, want erring=%v", c.name, err, c.erring)
			continue
		}
		if (got == nil) != (c.want == nil) || (got != nil && *got != *c.want) {
			t.Errorf("%s: got %v, want %v", c.name, got, c.want)
		}
	}
}
