#!/usr/bin/env python3
"""Render a findings JSON into a self-contained interactive HTML scorecard.

    python3 render-scorecard.py findings.json -o report.html
    python3 render-scorecard.py findings.json --markdown -o report.md

No network, no dependencies, no external assets — the output is one file that
opens from disk. Recomputes the weighted total from the per-area grades and warns
on stderr if it disagrees with `overall.score`, so arithmetic slips are caught
before the owner sees them.

Colors follow the validated reference palette from the `dataviz` skill: status
roles for grade bands and severities (always paired with a glyph and a label, so
meaning never rides on hue alone), and its documented light/dark surface and ink
steps.
"""

from __future__ import annotations

import argparse
import html
import json
import pathlib
import re
import sys
from string import Template

# Fixed letter -> points, mirroring rubric.md. Kept here so the renderer can
# verify the weighted total independently of whoever filled in the JSON.
POINTS = {"A": 95, "A-": 91, "A−": 91, "B+": 88, "B": 85, "B-": 81, "B−": 81,
          "C+": 78, "C": 75, "C-": 71, "C−": 71, "D": 65, "F": 50}

# Grade band -> status role. The letter is always rendered beside the color, so
# hue carries "how worried should I be", never the grade itself.
def band(grade: str) -> str:
    g = (grade or "").strip().upper().replace("−", "-")
    if g in ("N/A", "NA", ""):
        return "na"
    if g.startswith("A") or g.startswith("B"):
        return "good"
    if g.startswith("C"):
        return "warning"
    if g.startswith("D"):
        return "serious"
    return "critical"


SEVERITY = {
    "critical": ("critical", "▲", 0),
    "major":    ("serious",  "●", 1),
    "minor":    ("warning",  "◆", 2),
    "nit":      ("muted",    "○", 3),
}


def sev_key(s: str) -> str:
    return (s or "minor").strip().lower()


def esc(s) -> str:
    return html.escape(str(s if s is not None else ""))


def md_inline(s) -> str:
    """Minimal inline markdown: escape first, then code/bold/italic/links."""
    out = esc(s)
    out = re.sub(r"`([^`]+)`", r"<code>\1</code>", out)
    out = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", out)
    out = re.sub(r"(?<![*\w])\*([^*\n]+)\*(?!\w)", r"<em>\1</em>", out)
    return out


def md_block(s) -> str:
    """Paragraphs plus '- ' bullet runs. Enough for evidence blocks."""
    lines = str(s or "").split("\n")
    parts, bullets, para = [], [], []

    def flush_para():
        if para:
            parts.append("<p>" + md_inline(" ".join(para).strip()) + "</p>")
            para.clear()

    def flush_bullets():
        if bullets:
            items = "".join(f"<li>{md_inline(b)}</li>" for b in bullets)
            parts.append(f"<ul>{items}</ul>")
            bullets.clear()

    for raw in lines:
        line = raw.rstrip()
        stripped = line.strip()
        if stripped.startswith(("- ", "* ")):
            flush_para()
            bullets.append(stripped[2:])
        elif not stripped:
            flush_para()
            flush_bullets()
        else:
            flush_bullets()
            para.append(stripped)
    flush_para()
    flush_bullets()
    return "".join(parts)


def verify_total(data: dict) -> tuple[float | None, list[str]]:
    """Recompute weighted score, excluding N/A areas (weight redistributes)."""
    warnings: list[str] = []
    num = den = 0.0
    for a in data.get("areas", []):
        grade = str(a.get("grade", "")).strip()
        if band(grade) == "na":
            continue
        pts = a.get("points")
        canonical = POINTS.get(grade.upper().replace("−", "-"))
        if canonical is None:
            warnings.append(f"area {a.get('n')}: unknown grade {grade!r}")
            continue
        if pts is None:
            pts = canonical
        elif abs(float(pts) - canonical) > 0.01:
            warnings.append(
                f"area {a.get('n')} ({a.get('name')}): grade {grade} should be "
                f"{canonical} points, JSON says {pts} — using {canonical}")
            pts = canonical
        w = float(a.get("weight", 0))
        num += w * pts
        den += w
    if den == 0:
        return None, warnings
    computed = num / den
    stated = data.get("overall", {}).get("score")
    if stated is not None and abs(computed - float(stated)) > 0.5:
        warnings.append(
            f"overall.score is {stated} but weights recompute to {computed:.1f} "
            f"— check the area grades")
    if abs(den - 100.0) > 0.01:
        warnings.append(f"weights sum to {den:g}, not 100 (N/A areas redistribute)")
    return computed, warnings


# --------------------------------------------------------------------------- #
# HTML
# --------------------------------------------------------------------------- #

TEMPLATE = Template(r"""<!doctype html>
<html lang="en" data-theme="auto">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>$title</title>
<style>
:root{
  color-scheme: light;
  --surface-1:#fcfcfb; --plane:#f9f9f7;
  --text-primary:#0b0b0b; --text-secondary:#52514e; --muted:#898781;
  --grid:#e1e0d9; --baseline:#c3c2b7; --border:rgba(11,11,11,.10);
  --good:#0ca30c; --warning:#fab219; --serious:#ec835a; --critical:#d03b3b;
  --na:#898781;
  --radius:10px;
  --sans:ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  --mono:ui-monospace,SFMono-Regular,Menlo,Consolas,"Liberation Mono",monospace;
}
@media (prefers-color-scheme: dark){
  :root:where(:not([data-theme="light"])){
    color-scheme: dark;
    --surface-1:#1a1a19; --plane:#0d0d0d;
    --text-primary:#fff; --text-secondary:#c3c2b7; --muted:#898781;
    --grid:#2c2c2a; --baseline:#383835; --border:rgba(255,255,255,.10);
  }
}
:root[data-theme="dark"]{
  color-scheme: dark;
  --surface-1:#1a1a19; --plane:#0d0d0d;
  --text-primary:#fff; --text-secondary:#c3c2b7; --muted:#898781;
  --grid:#2c2c2a; --baseline:#383835; --border:rgba(255,255,255,.10);
}
*{box-sizing:border-box}
body{margin:0;background:var(--plane);color:var(--text-primary);font-family:var(--sans);
  font-size:15px;line-height:1.55;-webkit-font-smoothing:antialiased}
.wrap{max-width:1080px;margin:0 auto;padding:28px 20px 80px}
a{color:inherit}
code{font-family:var(--mono);font-size:.88em;background:var(--grid);
  padding:.12em .38em;border-radius:4px;word-break:break-word}
h1,h2,h3{line-height:1.25;margin:0}
.card{background:var(--surface-1);border:1px solid var(--border);
  border-radius:var(--radius);padding:20px}

/* header + hero */
header.top{display:flex;flex-wrap:wrap;gap:20px;align-items:flex-start;
  justify-content:space-between;margin-bottom:8px}
.repo h1{font-size:26px;letter-spacing:-.01em}
.meta{color:var(--text-secondary);font-size:13px;margin-top:6px}
.meta span{white-space:nowrap}
.meta .sep{color:var(--muted);margin:0 7px}
.hero{display:flex;align-items:baseline;gap:14px}
.hero .figure{font-size:56px;font-weight:650;letter-spacing:-.03em;line-height:1}
.hero .of{font-size:15px;color:var(--muted)}
.gradepill{display:inline-flex;align-items:center;gap:7px;font-weight:650;
  font-size:15px;padding:5px 12px;border-radius:999px;border:1px solid currentColor}
.toolbarbtn{font:inherit;font-size:13px;color:var(--text-secondary);cursor:pointer;
  background:var(--surface-1);border:1px solid var(--border);border-radius:7px;padding:5px 10px}
.toolbarbtn:hover{border-color:var(--baseline)}

.callout{margin:16px 0 22px;border-left:3px solid var(--critical);
  background:color-mix(in oklab,var(--critical) 8%,var(--surface-1));
  border-radius:0 var(--radius) var(--radius) 0;padding:14px 18px}
.callout h2{font-size:15px;margin-bottom:4px}
.callout p{margin:0;color:var(--text-secondary);font-size:14px}
.counter{margin:14px 0 24px;color:var(--text-secondary);font-size:14px;
  background:var(--surface-1);border:1px solid var(--border);
  border-radius:var(--radius);padding:12px 16px}
.counter strong{color:var(--text-primary)}

h2.section{font-size:13px;text-transform:uppercase;letter-spacing:.08em;
  color:var(--muted);margin:32px 0 12px;font-weight:600}

/* areas table — doubles as the accessible table view */
table.areas{width:100%;border-collapse:collapse;font-size:14px}
table.areas caption{text-align:left;color:var(--muted);font-size:12px;
  padding-bottom:8px}
table.areas th{text-align:left;font-weight:600;font-size:12px;color:var(--muted);
  text-transform:uppercase;letter-spacing:.05em;padding:0 10px 8px 0;
  border-bottom:1px solid var(--grid)}
table.areas td{padding:11px 10px 11px 0;border-bottom:1px solid var(--grid);
  vertical-align:middle}
table.areas tr:last-child td{border-bottom:none}
.areaname{font-weight:550}
.areach{display:block;color:var(--muted);font-size:12px;margin-top:2px}
.just{color:var(--text-secondary);font-size:13.5px}
.num{font-variant-numeric:tabular-nums;text-align:right;color:var(--text-secondary)}
/* meter: fill carries the band, track is the same hue lightened */
.meter{width:120px;height:9px;border-radius:999px;overflow:hidden;
  background:color-mix(in oklab,var(--bandcolor) 18%,transparent)}
.meter>i{display:block;height:100%;border-radius:999px;background:var(--bandcolor)}
.gradecell{display:flex;align-items:center;gap:10px}
.gletter{font-weight:650;min-width:26px;font-variant-numeric:tabular-nums}
[data-band="good"]{--bandcolor:var(--good)}
[data-band="warning"]{--bandcolor:var(--warning)}
[data-band="serious"]{--bandcolor:var(--serious)}
[data-band="critical"]{--bandcolor:var(--critical)}
[data-band="na"]{--bandcolor:var(--na)}

ul.plain{margin:0;padding-left:18px;color:var(--text-secondary)}
ul.plain li{margin:7px 0}
ul.plain strong{color:var(--text-primary)}

/* controls */
.controls{display:flex;flex-wrap:wrap;gap:10px;align-items:center;
  margin:0 0 14px;padding:12px 14px;background:var(--surface-1);
  border:1px solid var(--border);border-radius:var(--radius);
  position:sticky;top:0;z-index:5}
.chip{font:inherit;font-size:13px;cursor:pointer;border-radius:999px;
  padding:5px 12px;border:1px solid var(--border);background:transparent;
  color:var(--text-secondary);display:inline-flex;align-items:center;gap:6px}
.chip:hover{border-color:var(--baseline)}
.chip[aria-pressed="true"]{background:var(--text-primary);color:var(--surface-1);
  border-color:var(--text-primary)}
.chip .glyph{font-size:11px;color:var(--chipcolor,inherit)}
.chip[aria-pressed="true"] .glyph{color:var(--surface-1)}
.chip .count{font-variant-numeric:tabular-nums;opacity:.7}
.controls input[type=search],.controls select{font:inherit;font-size:13px;
  padding:6px 10px;border-radius:7px;border:1px solid var(--border);
  background:var(--plane);color:var(--text-primary)}
.controls input[type=search]{flex:1;min-width:150px}
.spacer{flex:1}
.progress{font-size:13px;color:var(--text-secondary);white-space:nowrap;
  font-variant-numeric:tabular-nums}

/* findings */
.finding{background:var(--surface-1);border:1px solid var(--border);
  border-left:3px solid var(--bandcolor);border-radius:var(--radius);
  margin-bottom:10px;overflow:hidden}
.finding[hidden]{display:none}
.fhead{display:flex;gap:12px;align-items:flex-start;width:100%;
  padding:13px 16px;background:none;border:0;font:inherit;color:inherit;
  cursor:pointer;text-align:left}
.fhead:hover{background:color-mix(in oklab,var(--bandcolor) 5%,transparent)}
.fid{font-family:var(--mono);font-size:12px;color:var(--muted);padding-top:3px;
  min-width:24px}
.ftitles{flex:1;min-width:0}
.ftitle{font-weight:550;font-size:15px}
.fmeta{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-top:5px;
  font-size:12px;color:var(--muted)}
.badge{display:inline-flex;align-items:center;gap:5px;font-weight:600;
  font-size:11.5px;letter-spacing:.02em;text-transform:uppercase;
  color:var(--bandcolor);border:1px solid currentColor;border-radius:999px;
  padding:1px 8px}
.tag{border:1px solid var(--grid);border-radius:999px;padding:1px 8px}
.caret{color:var(--muted);transition:transform .15s;padding-top:2px}
.finding.open .caret{transform:rotate(90deg)}
.fbody{padding:0 16px 16px 52px;display:none;font-size:14px}
.finding.open .fbody{display:block}
.fbody h4{margin:14px 0 4px;font-size:11.5px;text-transform:uppercase;
  letter-spacing:.07em;color:var(--muted);font-weight:600}
.fbody h4:first-child{margin-top:0}
.fbody p{margin:0 0 6px;color:var(--text-secondary)}
.fbody ul{margin:4px 0 6px;padding-left:18px;color:var(--text-secondary)}
.fbody li{margin:4px 0}
.fbody strong{color:var(--text-primary)}
.book{color:var(--muted);font-size:12.5px;border-top:1px solid var(--grid);
  margin-top:14px;padding-top:10px}
.done{display:inline-flex;align-items:center;gap:6px;font-size:12.5px;
  color:var(--text-secondary);cursor:pointer;user-select:none}
.finding.resolved{opacity:.55}
.finding.resolved .ftitle{text-decoration:line-through}
.empty{color:var(--muted);font-size:14px;padding:22px;text-align:center;
  border:1px dashed var(--grid);border-radius:var(--radius)}

.dropped li{margin:6px 0}
.verify{color:var(--text-secondary);font-size:13.5px}
footer{margin-top:36px;padding-top:16px;border-top:1px solid var(--grid);
  color:var(--muted);font-size:12.5px}

@media print{
  .controls,.toolbarbtn,.caret,.done{display:none!important}
  .fbody{display:block!important}
  body{background:#fff}
  .finding,.card,.counter{break-inside:avoid;border-color:#ccc}
  .wrap{max-width:none}
}
@media (max-width:680px){
  .hero .figure{font-size:44px}
  .meter{width:70px}
  .fbody{padding-left:16px}
  .hidesm{display:none}
}
</style>
</head>
<body>
<div class="wrap">

<header class="top">
  <div class="repo">
    <h1>$repo</h1>
    <div class="meta">
      <span>$profile profile</span><span class="sep">·</span>
      <span>$reviewed</span>$commit_html
    </div>
  </div>
  <div style="text-align:right">
    <div class="hero">
      <span class="figure">$score</span>
      <span class="of">/100</span>
      <span class="gradepill" data-band="$overall_band" style="color:var(--bandcolor)">$grade</span>
    </div>
    $theme_btn
  </div>
</header>

$lead_html
$counter_html

<h2 class="section">Areas</h2>
<div class="card">
<table class="areas">
  <caption>Grades by SDLC area. Bar length is the area score; color is the band; the
  letter is authoritative.</caption>
  <thead><tr>
    <th style="width:30%">Area</th><th class="hidesm" style="width:8%">Weight</th>
    <th style="width:22%">Grade</th><th>Justification</th>
  </tr></thead>
  <tbody>$area_rows</tbody>
</table>
</div>

$actions_html
$strengths_html

<h2 class="section">Findings</h2>
<div class="controls">
  <div role="group" aria-label="Filter by severity" style="display:flex;gap:6px;flex-wrap:wrap">
    $sev_chips
  </div>
  <select id="areaSel" aria-label="Filter by area">$area_opts</select>
  <input type="search" id="q" placeholder="Search findings…" aria-label="Search findings">
  <button class="toolbarbtn" id="expandBtn" type="button">Expand all</button>
  <span class="spacer"></span>
  <span class="progress" id="progress"></span>
</div>
<div id="findings">$findings_html</div>
<div class="empty" id="noresults" hidden>No findings match these filters.</div>

$dropped_html
$verify_html

<footer>
  Generated by <strong>repo-scorecard</strong> — graded against
  <em>Software Engineering: Standing on the Shoulders of Giants</em>.
  Findings are triple-verified; every grade traces to evidence. Checkbox state is
  stored locally in this browser.
</footer>
</div>

<script>
(function(){
  "use strict";
  var KEY = "scorecard:" + $store_key;
  var root = document.documentElement;
  var findings = Array.prototype.slice.call(document.querySelectorAll(".finding"));

  /* theme — only when we own the document. Embedded (artifact/fragment)
     the host stamps data-theme itself, and a second writer would fight it. */
  var tb = document.getElementById("themeBtn");
  if (tb) {
    var modes = ["auto","light","dark"], mi = 0;
    try { var sm = localStorage.getItem(KEY+":theme"); if (sm) mi = Math.max(0, modes.indexOf(sm)); } catch(e){}
    var applyTheme = function(){
      root.setAttribute("data-theme", modes[mi]);
      tb.textContent = "Theme: " + modes[mi];
      try { localStorage.setItem(KEY+":theme", modes[mi]); } catch(e){}
    };
    tb.addEventListener("click", function(){ mi = (mi+1) % modes.length; applyTheme(); });
    applyTheme();
  }

  /* resolved state ----------------------------------------------------- */
  var resolved = {};
  try { resolved = JSON.parse(localStorage.getItem(KEY) || "{}") || {}; } catch(e){ resolved = {}; }
  function persist(){ try { localStorage.setItem(KEY, JSON.stringify(resolved)); } catch(e){} }

  function updateProgress(){
    var total = findings.length, n = 0;
    findings.forEach(function(f){ if (resolved[f.dataset.id]) n++; });
    var el = document.getElementById("progress");
    el.textContent = n ? (n + " of " + total + " resolved") : (total + " findings");
  }

  findings.forEach(function(f){
    var id = f.dataset.id;
    var cb = f.querySelector("input[type=checkbox]");
    if (resolved[id]) { f.classList.add("resolved"); if (cb) cb.checked = true; }
    if (cb) cb.addEventListener("change", function(){
      if (cb.checked) { resolved[id] = true; f.classList.add("resolved"); }
      else { delete resolved[id]; f.classList.remove("resolved"); }
      persist(); updateProgress();
    });
    var head = f.querySelector(".fhead");
    head.addEventListener("click", function(){
      var open = f.classList.toggle("open");
      head.setAttribute("aria-expanded", open ? "true" : "false");
    });
  });

  /* filters ------------------------------------------------------------ */
  var sev = "all";
  var chips = Array.prototype.slice.call(document.querySelectorAll(".chip"));
  chips.forEach(function(c){
    c.addEventListener("click", function(){
      sev = c.dataset.sev;
      chips.forEach(function(o){ o.setAttribute("aria-pressed", o === c ? "true" : "false"); });
      apply();
    });
  });
  var areaSel = document.getElementById("areaSel");
  var q = document.getElementById("q");
  areaSel.addEventListener("change", apply);
  q.addEventListener("input", apply);

  function apply(){
    var term = q.value.toLowerCase().trim();
    var area = areaSel.value;
    var shown = 0;
    findings.forEach(function(f){
      var ok = (sev === "all" || f.dataset.sev === sev)
            && (area === "all" || f.dataset.area === area)
            && (!term || f.dataset.search.indexOf(term) !== -1);
      f.hidden = !ok;
      if (ok) shown++;
    });
    document.getElementById("noresults").hidden = shown !== 0;
  }

  /* expand all --------------------------------------------------------- */
  var eb = document.getElementById("expandBtn"), expanded = false;
  eb.addEventListener("click", function(){
    expanded = !expanded;
    findings.forEach(function(f){
      if (f.hidden) return;
      f.classList.toggle("open", expanded);
      f.querySelector(".fhead").setAttribute("aria-expanded", expanded ? "true":"false");
    });
    eb.textContent = expanded ? "Collapse all" : "Expand all";
  });

  window.addEventListener("beforeprint", function(){
    findings.forEach(function(f){ f.classList.add("open"); });
  });

  updateProgress();
})();
</script>
</body>
</html>
""")


def render_fragment(d: dict) -> str:
    """Body-only: `<style>` + page content, no doctype/html/head/body.

    For embedding — notably Claude Artifacts, which supply their own document
    skeleton and their own theme toggle (hence no theme button here; the CSS
    already answers both `prefers-color-scheme` and `[data-theme]`)."""
    full = render_html(d, embedded=True)
    style = re.search(r"<style>.*?</style>", full, re.S)
    body = re.search(r"<body>(.*?)</body>", full, re.S)
    if not style or not body:  # template changed shape
        raise RuntimeError("could not split template into style + body")
    return style.group(0) + "\n" + body.group(1).strip() + "\n"


def render_html(d: dict, embedded: bool = False) -> str:
    overall = d.get("overall", {}) or {}
    score = overall.get("score", "—")
    grade = overall.get("grade", "—")

    commit_html = ""
    if d.get("commit"):
        commit_html = ('<span class="sep">·</span><span><code>'
                       + esc(d["commit"]) + "</code>")
        if d.get("branch"):
            commit_html += " on <code>" + esc(d["branch"]) + "</code>"
        commit_html += "</span>"

    # area rows
    rows = []
    for a in d.get("areas", []):
        g = str(a.get("grade", "—"))
        b = band(g)
        pts = POINTS.get(g.upper().replace("−", "-"), 0)
        pct = 0 if b == "na" else max(4, min(100, pts))
        rows.append(
            f'<tr data-band="{b}">'
            f'<td><span class="areaname">{esc(a.get("name",""))}</span>'
            f'<span class="areach">Ch. {esc(a.get("chapters","—"))}</span></td>'
            f'<td class="num hidesm">{esc(a.get("weight",""))}</td>'
            f'<td><div class="gradecell"><span class="gletter" '
            f'style="color:var(--bandcolor)">{esc(g)}</span>'
            f'<span class="meter" role="img" aria-label="score {pts} of 100">'
            f'<i style="width:{pct}%"></i></span></div></td>'
            f'<td class="just">{md_inline(a.get("justification",""))}</td></tr>')

    # lead callout = the single most severe finding
    findings = list(d.get("findings", []))
    order = {k: v[2] for k, v in SEVERITY.items()}
    findings.sort(key=lambda f: (order.get(sev_key(f.get("severity")), 9),
                                 str(f.get("id", ""))))
    lead_html = ""
    if findings and sev_key(findings[0].get("severity")) == "critical":
        f0 = findings[0]
        lead_html = (
            '<div class="callout"><h2>▲ Critical — '
            + esc(f0.get("id", "")) + ": " + esc(f0.get("title", "")) + "</h2><p>"
            + md_inline(str(f0.get("do", "")).split(".")[0]) + ".</p></div>")

    counter_html = ""
    cf = d.get("counterfactual")
    if cf:
        counter_html = (
            '<div class="counter">With <strong>'
            + esc(cf.get("note", "the top finding fixed")) + "</strong>, the same rubric "
            "scores this repo <strong>" + esc(cf.get("grade", "")) + " ("
            + esc(cf.get("score", "")) + ")</strong> — no other change required.</div>")

    # top actions
    actions_html = ""
    acts = d.get("actions") or []
    if not acts:
        acts = [{"id": f.get("id"), "text": f.get("title"), "effort": f.get("effort")}
                for f in findings[:3]]
    if acts:
        items = "".join(
            f'<li><strong>{esc(a.get("id",""))}</strong> — {md_inline(a.get("text",""))}'
            + (f' <span style="color:var(--muted)">(~{esc(a.get("effort"))})</span>'
               if a.get("effort") else "") + "</li>"
            for a in acts)
        actions_html = ('<h2 class="section">Top next actions</h2>'
                        f'<div class="card"><ul class="plain">{items}</ul></div>')

    strengths_html = ""
    if d.get("strengths"):
        items = "".join(f"<li>{md_inline(s)}</li>" for s in d["strengths"])
        strengths_html = ('<h2 class="section">What&rsquo;s working</h2>'
                          f'<div class="card"><ul class="plain">{items}</ul></div>')

    # severity chips
    counts = {}
    for f in findings:
        counts[sev_key(f.get("severity"))] = counts.get(sev_key(f.get("severity")), 0) + 1
    chips = ['<button class="chip" data-sev="all" aria-pressed="true" type="button">'
             f'All <span class="count">{len(findings)}</span></button>']
    for name in ("critical", "major", "minor", "nit"):
        if not counts.get(name):
            continue
        role, glyph, _ = SEVERITY[name]
        chips.append(
            f'<button class="chip" data-sev="{name}" aria-pressed="false" type="button" '
            f'style="--chipcolor:var(--{role})">'
            f'<span class="glyph">{glyph}</span>{name.capitalize()} '
            f'<span class="count">{counts[name]}</span></button>')

    areas_present = []
    for f in findings:
        if f.get("area") and f["area"] not in areas_present:
            areas_present.append(f["area"])
    area_opts = '<option value="all">All areas</option>' + "".join(
        f'<option value="{esc(a)}">{esc(a)}</option>' for a in areas_present)

    # finding cards
    cards = []
    for f in findings:
        sk = sev_key(f.get("severity"))
        role, glyph, _ = SEVERITY.get(sk, SEVERITY["minor"])
        fid = esc(f.get("id", ""))
        blob = " ".join(str(f.get(k, "")) for k in
                        ("id", "title", "area", "evidence", "why", "do", "book")).lower()
        body = []
        if f.get("evidence"):
            body.append("<h4>Evidence</h4>" + md_block(f["evidence"]))
        if f.get("why"):
            body.append("<h4>Why it matters</h4>" + md_block(f["why"]))
        if f.get("do"):
            body.append("<h4>Do this</h4>" + md_block(f["do"]))
        extra = []
        if f.get("book"):
            extra.append("<strong>Book:</strong> " + md_inline(f["book"]))
        if f.get("effort"):
            extra.append("<strong>Effort:</strong> " + esc(f["effort"]))
        if extra:
            body.append('<div class="book">' + " &nbsp;·&nbsp; ".join(extra) + "</div>")
        body.append(
            f'<label class="done"><input type="checkbox"> Mark {fid} resolved</label>')

        cards.append(
            f'<article class="finding" data-band="{role}" data-id="{fid}" '
            f'data-sev="{sk}" data-area="{esc(f.get("area",""))}" '
            f'data-search="{esc(blob)}">'
            f'<button class="fhead" type="button" aria-expanded="false">'
            f'<span class="caret">&#9656;</span>'
            f'<span class="fid">{fid}</span>'
            f'<span class="ftitles"><span class="ftitle">'
            f'{esc(f.get("title",""))}</span>'
            f'<span class="fmeta">'
            f'<span class="badge"><span aria-hidden="true">{glyph}</span>'
            f'{esc(f.get("severity",""))}</span>'
            f'<span class="tag">{esc(f.get("area",""))}</span>'
            + (f'<span class="tag">Effort {esc(f.get("effort"))}</span>'
               if f.get("effort") else "")
            + f'</span></span></button>'
            f'<div class="fbody">{"".join(body)}</div></article>')

    dropped_html = ""
    if d.get("dropped"):
        items = "".join(
            f'<li><em>{md_inline(x.get("claim",""))}</em> — {md_inline(x.get("reason",""))}</li>'
            for x in d["dropped"])
        dropped_html = (
            '<h2 class="section">Considered and dropped</h2><div class="card">'
            '<p style="margin:0 0 8px;color:var(--muted);font-size:13px">'
            'Plausible findings the evidence killed — listed so they are not '
            're-reported next run.</p>'
            f'<ul class="plain dropped">{items}</ul></div>')

    verify_html = ""
    v = d.get("verification")
    if v:
        lines = []
        for label, key in (("Pass 1 · Locate", "pass1"), ("Pass 2 · Refute", "pass2"),
                           ("Pass 3 · Actionability", "pass3")):
            if v.get(key):
                lines.append(f"<li><strong>{label}:</strong> {md_inline(v[key])}</li>")
        if v.get("shipped") is not None:
            lines.append(f"<li><strong>{esc(v['shipped'])} findings ship.</strong> "
                         "Grades derive from surviving findings only.</li>")
        verify_html = ('<h2 class="section">Verification</h2>'
                       f'<div class="card verify"><ul class="plain">{"".join(lines)}</ul></div>')

    return TEMPLATE.substitute(
        title=esc(f"Scorecard — {d.get('repo','repo')}"),
        repo=esc(d.get("repo", "repository")),
        profile=esc(str(d.get("profile", "")).capitalize()),
        reviewed=esc(d.get("reviewed", "")),
        commit_html=commit_html,
        score=esc(score), grade=esc(grade), overall_band=band(str(grade)),
        lead_html=lead_html, counter_html=counter_html,
        area_rows="".join(rows), actions_html=actions_html,
        strengths_html=strengths_html, sev_chips="".join(chips),
        area_opts=area_opts, findings_html="".join(cards),
        dropped_html=dropped_html, verify_html=verify_html,
        store_key=json.dumps(str(d.get("path") or d.get("repo") or "repo")),
        theme_btn=("" if embedded else
                   '<button class="toolbarbtn" id="themeBtn" style="margin-top:10px" '
                   'type="button">Theme: auto</button>'),
    )


def render_markdown(d: dict) -> str:
    o = d.get("overall", {}) or {}
    L = [f"# Scorecard — {d.get('repo','repo')}", "",
         f"Profile: **{d.get('profile','')}** · Reviewed: {d.get('reviewed','')}"
         + (f" · Commit: `{d['commit']}`" if d.get("commit") else ""), "",
         f"**Overall: {o.get('grade','—')} ({o.get('score','—')}/100)**", ""]
    cf = d.get("counterfactual")
    if cf:
        L += [f"> With {cf.get('note','the top finding fixed')}, the same rubric scores "
              f"**{cf.get('grade')} ({cf.get('score')})**.", ""]
    L += ["| # | Area | Weight | Grade | Justification |", "|---|---|---:|:---:|---|"]
    for a in d.get("areas", []):
        L.append(f"| {a.get('n','')} | {a.get('name','')} | {a.get('weight','')} "
                 f"| {a.get('grade','')} | {a.get('justification','')} |")
    if d.get("strengths"):
        L += ["", "## What's working", ""] + [f"- {s}" for s in d["strengths"]]
    order = {k: v[2] for k, v in SEVERITY.items()}
    fs = sorted(d.get("findings", []),
                key=lambda f: (order.get(sev_key(f.get("severity")), 9), str(f.get("id"))))
    if fs:
        L += ["", "## Findings"]
        for f in fs:
            L += ["", f"### {f.get('id','')} · [{f.get('severity','')}] "
                      f"{f.get('area','')} — {f.get('title','')}", ""]
            for label, key in (("Evidence", "evidence"), ("Why it matters", "why"),
                               ("Do this", "do"), ("Book", "book"), ("Effort", "effort")):
                if not f.get(key):
                    continue
                val = str(f[key])
                # A multi-line block needs its own line, or the bullets fold
                # into the bold label and Markdown renders one run-on paragraph.
                if "\n" in val:
                    L += [f"**{label}:**", "", val, ""]
                else:
                    L += [f"**{label}:** {val}", ""]
    if d.get("dropped"):
        L += ["## Considered and dropped", ""] + [
            f"- *{x.get('claim','')}* — {x.get('reason','')}" for x in d["dropped"]]
    v = d.get("verification") or {}
    if v:
        L += ["", "## Verification", ""]
        for label, key in (("Pass 1", "pass1"), ("Pass 2", "pass2"), ("Pass 3", "pass3")):
            if v.get(key):
                L.append(f"- **{label}:** {v[key]}")
        if v.get("shipped") is not None:
            L.append(f"- **{v['shipped']} findings ship.**")
    return "\n".join(L) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("findings", help="path to the findings JSON")
    ap.add_argument("-o", "--out", help="output path (default: stdout)")
    ap.add_argument("--markdown", action="store_true", help="emit Markdown, not HTML")
    ap.add_argument("--fragment", action="store_true",
                    help="body-only HTML for embedding (e.g. a Claude Artifact)")
    args = ap.parse_args()

    try:
        data = json.loads(pathlib.Path(args.findings).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        print(f"cannot read findings JSON: {e}", file=sys.stderr)
        return 1

    computed, warnings = verify_total(data)
    for w in warnings:
        print(f"warning: {w}", file=sys.stderr)
    if computed is not None:
        print(f"weighted total recomputed: {computed:.1f}", file=sys.stderr)

    if args.markdown:
        out = render_markdown(data)
    elif args.fragment:
        out = render_fragment(data)
    else:
        out = render_html(data)
    if args.out:
        pathlib.Path(args.out).write_text(out, encoding="utf-8")
        print(f"wrote {args.out}", file=sys.stderr)
    else:
        sys.stdout.write(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
