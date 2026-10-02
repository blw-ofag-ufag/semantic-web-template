-- Quarto shortcodes for the eCH metadata (docs/_ech.yml).
--
--   {{< ech status >}}   the status of the document with its eCH definition,
--                        e.g. "Genehmigt: Das Dokument wurde ..."

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
    error("{{< ech >}}: unknown argument '" .. what .. "' (expected: status)")
  end,
}
