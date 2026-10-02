-- Quarto filter: translates the eCH metadata codes (docs/_ech.yml) into the
-- display values used by the Typst title page (typst-show.typ) and the HTML
-- title block (title-metadata.html).
--
-- Sets `ech-rows` (list of { label, values, bullets }) and `ech-display`
-- (number, version, status, tagline, page-prefix, page-infix, organisation,
-- summary) in the document metadata.

local common = dofile(quarto.utils.resolve_path("ech-common.lua"))

function Meta(meta)
  local display = common.display(meta, { include_name = not quarto.doc.is_format("html") })
  if display == nil then return meta end

  local rows = {}
  for _, row in ipairs(display.rows) do
    table.insert(rows, { label = row.label, values = row.values, bullets = row.bullets })
  end
  meta["ech-rows"] = rows
  meta["ech-display"] = {
    number = display.number,
    version = display.version,
    status = display.status,
    tagline = display.tagline,
    ["page-prefix"] = display["page-prefix"],
    ["page-infix"] = display["page-infix"],
    organisation = display.organisation,
    summary = display.summary,
  }
  return meta
end
