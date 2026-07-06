#!/usr/bin/env bash
# Run every code example in every language. Exit nonzero if anything that
# should pass fails, or anything that should FAIL (the ch08 type-fault demos)
# unexpectedly compiles. Run from the book/code directory. Used by CI
# (.github/workflows/code-tests.yml) and locally.
set -u
cd "$(dirname "$0")"
PASS=0; FAIL=0
note() { printf '%s\n' "$*"; }
ok()   { PASS=$((PASS+1)); }
bad()  { FAIL=$((FAIL+1)); note "FAIL: $*"; }

# --- Python ---------------------------------------------------------------
for f in */python/*.py; do
  [ -e "$f" ] || continue
  python3 "$f" >/dev/null 2>&1 && ok || bad "python $f"
done

# --- JavaScript (Node >= 18) ----------------------------------------------
for f in */javascript/*.js; do
  [ -e "$f" ] || continue
  node "$f" >/dev/null 2>&1 && ok || bad "node $f"
done

# --- TypeScript: type-check with tsc, run via node (Node >=22.6 strips types).
# The ch08 examples are type-fault demos and MUST fail tsc (like the Go/Java
# compile-fault demos); every other .ts must type-check clean and run.
TSC=""
for c in ./node_modules/.bin/tsc /tmp/node_modules/.bin/tsc "$(command -v tsc 2>/dev/null)"; do
  [ -x "$c" ] && { TSC="$c"; break; }
done
# locate @types/node so tsc can resolve node:test / node:assert imports
TYPEROOTS=""
for r in ./node_modules/@types /tmp/node_modules/@types "$(dirname "$TSC" 2>/dev/null)/../@types"; do
  [ -d "$r/node" ] && { TYPEROOTS="$r"; break; }
done
tscheck() {  # tscheck <file> ; returns 0 if it type-checks clean
  [ -n "$TSC" ] || return 0
  local tr=(); [ -n "$TYPEROOTS" ] && tr=(--typeRoots "$TYPEROOTS")
  "$TSC" --strict --noEmit --target es2022 --module nodenext \
    --moduleResolution nodenext --skipLibCheck "${tr[@]}" "$1" >/dev/null 2>&1
}
for f in */typescript/*.ts; do
  [ -e "$f" ] || continue
  case "$f" in
    ch08/typescript/line_total.ts|ch08/typescript/applyDiscount.ts)
      # type-fault demo: tsc MUST reject it
      if tscheck "$f"; then bad "expected tsc error missing: $f"; else ok; fi ;;
    *)
      tscheck "$f" || { bad "tsc $f"; continue; }
      node --experimental-strip-types "$f" >/dev/null 2>&1 && ok || bad "ts-run $f" ;;
  esac
done

# --- Ruby -------------------------------------------------------------------
for f in */ruby/*.rb; do
  [ -e "$f" ] || continue
  ruby "$f" >/dev/null 2>&1 && ok || bad "ruby $f"
done

# --- Go: test modules run `go test`; plain files run `go run`; the ch08
# type-fault demo MUST fail to compile with the documented message. ----------
for d in */go; do
  [ -d "$d" ] || continue
  if ls "$d"/*_test.go >/dev/null 2>&1; then
    (cd "$d" && go test ./...) >/dev/null 2>&1 && ok || bad "go test $d"
  else
    for g in "$d"/*.go; do
      case "$g" in
        *type_fault*)
          if (cd "$d" && go run "$(basename "$g")") 2>&1 | grep -q 'cannot use price'; then
            ok
          else
            bad "expected compile error missing: $g"
          fi ;;
        *)
          (cd "$d" && go run "$(basename "$g")") >/dev/null 2>&1 && ok || bad "go run $g" ;;
      esac
    done
  fi
done

# --- Java (JDK >= 25 for compact source files) -------------------------------
JUNIT_JAR="${JUNIT_JAR:-/tmp/junit-platform-console-standalone.jar}"
for f in */java/*.java; do
  [ -e "$f" ] || continue
  case "$f" in
    *LineTotal*)  # type-fault demo: must NOT compile
      if java "$f" 2>&1 | grep -q 'String cannot be converted to double'; then
        ok
      else
        bad "expected compile error missing: $f"
      fi ;;
    *Test*)       # JUnit tests need the console-standalone jar
      if [ ! -f "$JUNIT_JAR" ]; then
        curl -sL -o "$JUNIT_JAR" \
          "https://repo1.maven.org/maven2/org/junit/platform/junit-platform-console-standalone/1.11.4/junit-platform-console-standalone-1.11.4.jar" \
          || { bad "junit download for $f"; continue; }
      fi
      dir="$(dirname "$f")"; base="$(basename "$f")"
      (cd "$dir" && javac -cp "$JUNIT_JAR" "$base" \
        && java -jar "$JUNIT_JAR" execute --class-path . \
             --select-class "$(basename "$base" .java)" --fail-if-no-tests) \
        >/dev/null 2>&1 && ok || bad "junit $f"
      rm -f "$dir"/*.class ;;
    *)
      java -ea "$f" >/dev/null 2>&1 && ok || bad "java $f" ;;
  esac
done

note "pass=$PASS fail=$FAIL"
[ "$FAIL" -eq 0 ]
