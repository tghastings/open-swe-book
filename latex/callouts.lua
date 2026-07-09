-- Convert blockquotes that begin with a KNOWN callout label into a tcolorbox
-- callout, tagged with a STYLE KEY so the preamble can render each type with a
-- distinct (grayscale) treatment. Only these labels — otherwise a bold-lead
-- blockquote (a use-case field, a boxed formula) would wrongly become a box.
-- Order matters: longer/more-specific labels are matched by prefix first.
local MAP = {
  {"Pitfall",        "pitfall"},
  {"Anti-pattern",   "pitfall"},
  {"Principle",      "principle"},
  {"Definition",     "definition"},
  {"Case study",     "example"},
  {"Worked example", "example"},
  {"Scenario",       "example"},
  {"Tip",            "tip"},
  {"Technique",      "tip"},
  {"Heuristic",      "tip"},
  {"Rule of thumb",  "tip"},
  {"Note",           "note"},
  {"Where we are",   "note"},
  {"Why it matters", "note"},
  {"Two paths",      "note"},
}
function BlockQuote(el)
  local first = el.content[1]
  if first and first.t == "Para" and first.content[1] and first.content[1].t == "Strong" then
    local raw = pandoc.utils.stringify(first.content[1])
    local key = nil
    for _, m in ipairs(MAP) do
      if raw:sub(1, #m[1]) == m[1] then key = m[2]; break end
    end
    if not key then return nil end
    -- render the bold label to LaTeX so special chars (^ _ & % # ~) are escaped
    local label = pandoc.write(pandoc.Pandoc({pandoc.Plain(first.content[1].content)}),
                               "latex"):gsub("%s+$", "")
    table.remove(first.content, 1)
    while first.content[1] and (first.content[1].t == "Space" or first.content[1].t == "SoftBreak") do
      table.remove(first.content, 1)
    end
    local out = { pandoc.RawBlock("latex", "\\begin{callout}{" .. key .. "}{" .. label .. "}") }
    for _, b in ipairs(el.content) do out[#out+1] = b end
    out[#out+1] = pandoc.RawBlock("latex", "\\end{callout}")
    return out
  end
end
