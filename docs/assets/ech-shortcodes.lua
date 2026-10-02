-- Quarto shortcodes for the eCH metadata (docs/_ech.yml).
--
--   {{< ech status >}}   the status of the document with its eCH definition,
--                        e.g. "Genehmigt: Das Dokument wurde ..."
--   {{< ech figures >}}  list of all figures with their captions, linked
--   {{< ech tables >}}   list of all tables with their captions, linked
--
-- The lists are produced for the PDF (Typst outline) and the website (filled
-- in by ech-captions.lua after Quarto has numbered the floats).

local common = dofile(quarto.utils.resolve_path("ech-common.lua"))

return {
  ["ech"] = function(args, kwargs, meta)
    local what = args[1] and pandoc.utils.stringify(args[1]) or ""
    local display = common.display(meta)
    if display == nil then
      error("{{< ech >}}: the document has no `ech` metadata (see docs/_ech.yml)")
    end
    if what == "status" then
      return display["status-text"] or pandoc.Inlines(pandoc.Str("---"))
    end
    local lists = { figures = { kind = "fig", class = "ech-list-of-figures" },
                    tables = { kind = "tbl", class = "ech-list-of-tables" } }
    if lists[what] then
      if quarto.doc.is_format("typst") then
        return pandoc.RawBlock("typst", string.format(
          '#outline(title: none, target: figure.where(kind: "quarto-float-%s"))', lists[what].kind))
      elseif quarto.doc.is_format("html") then
        return pandoc.Div({}, pandoc.Attr("", { lists[what].class }))
      end
      return pandoc.Blocks({})
    end
    error("{{< ech >}}: unknown argument '" .. what .. "' (expected: status, figures, tables)")
  end,
}
