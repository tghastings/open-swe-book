-- Convert blockquotes that begin with a KNOWN callout label into tcolorbox
-- callouts. Only these labels — otherwise a bold-lead blockquote (a use-case
-- field, a boxed formula) would wrongly become an empty titled box.
local CALLOUTS = {"Pitfall", "Principle", "Definition", "Tip", "Note", "Case study",
  "Where we are", "Worked example", "Why it matters", "Technique", "Two paths",
  "Anti-pattern", "Heuristic", "Rule of thumb", "Scenario"}
function BlockQuote(el)
  local first = el.content[1]
  if first and first.t == "Para" and first.content[1] and first.content[1].t == "Strong" then
    local raw = pandoc.utils.stringify(first.content[1])
    local ok = false
    for _, c in ipairs(CALLOUTS) do
      if raw:sub(1, #c) == c then ok = true; break end
    end
    if not ok then return nil end
    -- render the bold label to LaTeX so special chars (^ _ & % # ~) are escaped
    local label = pandoc.write(pandoc.Pandoc({pandoc.Plain(first.content[1].content)}),
                               "latex"):gsub("%s+$", "")
    table.remove(first.content, 1)
    while first.content[1] and (first.content[1].t == "Space" or first.content[1].t == "SoftBreak") do
      table.remove(first.content, 1)
    end
    local out = { pandoc.RawBlock("latex", "\\begin{callout}{" .. label .. "}") }
    for _, b in ipairs(el.content) do out[#out+1] = b end
    out[#out+1] = pandoc.RawBlock("latex", "\\end{callout}")
    return out
  end
end
