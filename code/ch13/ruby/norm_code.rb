# Chapter 15, exercise 2 (§15.2) — the inherited, undocumented norm_code, Ruby variant.
# nil plays Python's None; ArgumentError plays ValueError; the [[:alnum:]] regex
# plays str.isalnum (nonempty, all letters/digits). Ruby's "" is truthy, so the
# final `s or ...` needs an explicit empty? check.
# Runs standalone: ruby norm_code.rb
def norm_code(s, strict: false)
  return strict ? nil : "" if s.nil?
  s = s.strip.upcase.delete("-")
  s = s[0, 8] if s.length > 8
  raise ArgumentError, s if strict && s !~ /\A[[:alnum:]]+\z/
  s.empty? ? (strict ? nil : "") : s
end

# characterization pins, matching the Python original's observed behavior
raise unless norm_code(nil) == ""
raise unless norm_code(nil, strict: true).nil?
raise unless norm_code(" ab-12 ") == "AB12"
raise unless norm_code("abcdefghij") == "ABCDEFGH" # truncated to 8
raise unless norm_code("a!b") == "A!B"             # lenient keeps the junk
begin
  norm_code("a!b", strict: true)
  raise "expected ArgumentError"
rescue ArgumentError => e
  raise unless e.message == "A!B"
end
begin
  norm_code("", strict: true)                      # empty fails isalnum too
  raise "expected ArgumentError"
rescue ArgumentError
  nil
end
raise unless norm_code("  ") == ""
raise unless norm_code("--------") == ""
puts "all characterization pins hold"
