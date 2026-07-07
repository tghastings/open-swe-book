-- Deduplicate footnotes within a chapter: a source cited N times should be ONE
-- numbered footnote referenced N times, not N identical footnotes (pandoc emits
-- an identical \footnote for every citation). First citation carries the note
-- (labelled); later citations become \footnotemark to the same number.
--
-- Footnotes inside callouts (blockquotes) are left alone: tcolorbox makes them
-- box-local (lettered), so \getrefnumber would not yield a usable number.
local seen = {}
local counter = 0

local function dedup_note(el)
  local key = pandoc.utils.stringify(el.content)
  if key == "" then return nil end
  local lbl = seen[key]
  if lbl then
    return pandoc.RawInline("latex", "\\footnotemark[\\getrefnumber{" .. lbl .. "}]")
  end
  counter = counter + 1
  lbl = "dupfn" .. counter
  seen[key] = lbl
  local first = el.content[1]
  if first and (first.t == "Para" or first.t == "Plain") then
    table.insert(first.content, 1, pandoc.RawInline("latex", "\\label{" .. lbl .. "}"))
  else
    table.insert(el.content, 1, pandoc.RawBlock("latex", "\\label{" .. lbl .. "}"))
  end
  return el
end

return {
  {
    traverse = "topdown",
    Header = function(el)
      if el.level == 1 then seen = {} end   -- footnotes reset per chapter
      return nil
    end,
    BlockQuote = function(el)
      return el, false   -- do not descend: leave callout footnotes as-is
    end,
    Note = dedup_note,
  },
}
