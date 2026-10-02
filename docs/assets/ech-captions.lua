-- Quarto filter (runs after Quarto's own filters): sets the caption prefix of
-- figures and tables in bold on the website, "**Tabelle 3:** Beschreibung".
-- The PDF does the same with a Typst show rule in typst-template.typ.

if not quarto.doc.is_format("html") then return {} end

-- Wraps the leading "Tabelle 3:" tokens of a caption in Strong.
local function embolden_prefix(inlines)
  for i = 1, math.min(#inlines, 4) do
    local inline = inlines[i]
    if inline.t == "Str" and inline.text:sub(-1) == ":" then
      local prefix = pandoc.Inlines({})
      for _ = 1, i do prefix:insert(inlines:remove(1)) end
      inlines:insert(1, pandoc.Strong(prefix))
      return true
    end
  end
  return false
end

function Div(div)
  local changed = false
  for i, block in ipairs(div.content) do
    local nextblock = div.content[i + 1]
    if block.t == "RawBlock" and block.text:find("<figcaption", 1, true) and nextblock
      and (nextblock.t == "Plain" or nextblock.t == "Para") then
      if embolden_prefix(nextblock.content) then changed = true end
    end
  end
  if changed then return div end
end
