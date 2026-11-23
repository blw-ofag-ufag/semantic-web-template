-- Renders the result of a SPARQL SELECT query as a table, in every output format:
--
--     ```{.sparql #tbl-genres endpoint="../../build/rdf/03-processed.ttl"
--         tbl-cap="Tracks per genre." header="Genre|Tracks" align="lr"}
--     PREFIX schema: <http://schema.org/>
--     SELECT ?name (COUNT(?track) AS ?tracks)
--     WHERE { ?track schema:genre/schema:name ?name }
--     GROUP BY ?name ORDER BY DESC(?tracks)
--     ```
--
-- A block is rendered as a table if it has an identifier #tbl-... or the
-- class .table (```{.sparql .table}); any other ```sparql block stays a
-- listing of code. Only `endpoint` is required:
--
--   endpoint   what to query: an RDF file (.ttl, .nt; path relative to the
--              document) or the URL of a SPARQL endpoint (https://...)
--   #tbl-...   numbered table that can be referenced with @tbl-...
--   tbl-cap    caption (Markdown)
--   header     column headers, separated by "|" (default: the variable names)
--   align      one letter per column: l, r or c (default: numbers right, others left)
--   widths     relative column widths, separated by commas
--   digits     decimal places of decimal numbers
--   max-rows   upper limit of rows, to catch a forgotten LIMIT (default: 200)
--   echo       "true" shows the query above the table
--
-- The attributes can also be written as lines beginning with `#|` at the top
-- of the block, as in the code cells of Quarto (`label` is the identifier).
-- For SPARQL these lines are comments. They take precedence over the
-- attributes in the header of the block:
--
--     ```{.sparql}
--     #| label: tbl-genres
--     #| endpoint: ../../build/rdf/03-processed.ttl
--     #| tbl-cap: "Tracks per genre."
--     #| header: "Genre|Tracks"
--     #| align: lr
--     SELECT ...
--     ```
--
-- `{{lang}}` in the query is replaced by the language of the document, so
-- that one query serves all language versions:
-- FILTER(lang(?label) = "{{lang}}").
--
-- Values are shown according to their datatype and the language of the
-- document: integers with a thousands separator, decimals with the decimal
-- mark, dates in the usual notation, booleans as yes or no, IRIs as linked
-- prefixed names (with the prefixes that the query declares).
--
-- The query is run by sparql/query.py with the Python of the project
-- (QUARTO_PYTHON; the package pyoxigraph for files). Results are kept in
-- sparql/cache/: of a file as long as the query and the file do not change,
-- of an endpoint on the web for the current hour.

local script = quarto.utils.resolve_path("sparql/query.py")
local cache_dir = quarto.utils.resolve_path("sparql/cache")

local XSD = "http://www.w3.org/2001/XMLSchema#"
local INTEGER_TYPES = {
  integer = true, int = true, long = true, short = true, byte = true,
  nonNegativeInteger = true, positiveInteger = true, nonPositiveInteger = true, negativeInteger = true,
  unsignedInt = true, unsignedLong = true, unsignedShort = true, unsignedByte = true,
}
local DECIMAL_TYPES = { decimal = true, double = true, float = true }

-- Notation of numbers, dates and booleans per language (Swiss conventions
-- for German, French and Italian). `date` is a pattern of %d, %m and %Y.
local THIN_SPACE = "\u{202F}"
local LOCALES = {
  de = { thousands = "’", decimal = ".", date = "%d.%m.%Y", yes = "ja", no = "nein" },
  fr = { thousands = THIN_SPACE, decimal = ",", date = "%d.%m.%Y", yes = "oui", no = "non" },
  it = { thousands = "’", decimal = ".", date = "%d.%m.%Y", yes = "sì", no = "no" },
  en = { thousands = ",", decimal = ".", date = "%Y-%m-%d", yes = "yes", no = "no" },
}

local lang = "en"
local locale = LOCALES.en
local document_dir = "."

-- ---------------------------------------------------------------------------
-- Files
-- ---------------------------------------------------------------------------

local function read_file(path)
  local file = io.open(path, "rb")
  if file == nil then return nil end
  local content = file:read("a")
  file:close()
  return content
end

local function write_file(path, content)
  pandoc.system.make_directory(pandoc.path.directory(path), true)
  local file = assert(io.open(path, "wb"))
  file:write(content)
  file:close()
end

-- A path of the document: absolute, or relative to the document.
local function resolve(path)
  if pandoc.path.is_absolute(path) then return path end
  return pandoc.path.join({ document_dir, path })
end

-- ---------------------------------------------------------------------------
-- Running the query
-- ---------------------------------------------------------------------------

local function exists(path)
  local file = io.open(path, "rb")
  if file == nil then return false end
  file:close()
  return true
end

-- The Python of the project. QUARTO_PYTHON may be relative to the folder
-- Quarto was started in, which is the document's folder or one above it.
local function python_command()
  local python = os.getenv("QUARTO_PYTHON")
  if python == nil or python == "" then return "python3" end
  if pandoc.path.is_absolute(python) or not python:find("/") then return python end
  local folder = pandoc.path.normalize(pandoc.path.join({ pandoc.system.get_working_directory(), document_dir }))
  if pandoc.path.is_absolute(document_dir) then folder = document_dir end
  for _ = 1, 8 do
    local candidate = pandoc.path.join({ folder, python })
    if exists(candidate) then return candidate end
    local parent = pandoc.path.directory(folder)
    if parent == folder then break end
    folder = parent
  end
  return python
end

local function is_url(endpoint)
  return endpoint:match("^https?://") ~= nil
end

local function run(query, endpoint)
  -- What the result depends on: the content of a file; for an endpoint on
  -- the web the hour, so that one render asks once and the next hour again.
  local state = is_url(endpoint) and os.date("!%Y-%m-%dT%H") or pandoc.utils.sha1(read_file(endpoint))
  local key = pandoc.utils.sha1(table.concat({ query, endpoint, state }, "\n"))
  local path = pandoc.path.join({ cache_dir, key .. ".json" })
  local json = read_file(path)
  if json == nil or json == "" then
    local ok, result = pcall(pandoc.pipe, python_command(), { script, "--endpoint", endpoint }, query)
    if not ok then
      local message = type(result) == "table" and result.output or tostring(result)
      assert(false, "SPARQL table could not be rendered:\n" .. tostring(message) .. "\n\n" .. query)
    end
    json = result
    write_file(path, json)
  end
  return quarto.json.decode(json)
end

-- ---------------------------------------------------------------------------
-- Formatting the values
-- ---------------------------------------------------------------------------

-- Text as inlines that can wrap at spaces.
local function text_inlines(text)
  local inlines = pandoc.Inlines({})
  for word, space in tostring(text):gmatch("(%S*)(%s*)") do
    if word ~= "" then inlines:insert(pandoc.Str(word)) end
    if space ~= "" then inlines:insert(pandoc.Space()) end
  end
  return inlines
end

local function group_thousands(digits)
  local grouped = digits:reverse():gsub("(%d%d%d)", "%1\0"):reverse()
  grouped = grouped:gsub("^%z", "")
  return (grouped:gsub("%z", locale.thousands))
end

-- "-1234.50" in the notation of the language; `digits` rounds to decimal places.
local function format_number(lexical, digits)
  local number = tonumber(lexical)
  if number == nil or number ~= number or number == math.huge or number == -math.huge then
    return lexical
  end
  local text = lexical
  if digits then
    text = string.format("%." .. digits .. "f", number)
  elseif lexical:find("[eE]") then
    text = string.format("%.2f", number)
  end
  local sign, whole, fraction = text:match("^([+-]?)(%d*)%.?(%d*)$")
  if whole == nil then return lexical end
  if whole == "" then whole = "0" end
  if sign == "+" then sign = "" end
  if sign == "-" then sign = "−" end
  local result = sign .. group_thousands(whole)
  if fraction ~= "" then result = result .. locale.decimal .. fraction end
  return result
end

local function format_date(lexical)
  local year, month, day = lexical:match("^(-?%d%d%d%d+)-(%d%d)-(%d%d)")
  if year == nil then return nil end
  return (locale.date:gsub("%%Y", year):gsub("%%m", month):gsub("%%d", day))
end

local function is_numeric(cell)
  if cell.type ~= "literal" or cell.datatype:sub(1, #XSD) ~= XSD then return false end
  local name = cell.datatype:sub(#XSD + 1)
  return INTEGER_TYPES[name] or DECIMAL_TYPES[name] or false
end

-- The inlines of a table cell for one value of the result (nil if unbound).
local function format_cell(cell, digits)
  if cell == nil or cell == quarto.json.null or type(cell) ~= "table" then
    return pandoc.Inlines({})
  end
  if cell.type == "iri" then
    return pandoc.Inlines({ pandoc.Link(text_inlines(cell.short or cell.value), cell.value) })
  end
  if cell.type == "bnode" then
    return pandoc.Inlines({})
  end
  local value = cell.value
  local datatype = cell.datatype or ""
  local name = datatype:sub(1, #XSD) == XSD and datatype:sub(#XSD + 1) or nil
  if name == nil then
    return text_inlines(value)
  elseif INTEGER_TYPES[name] then
    return pandoc.Inlines({ pandoc.Str(format_number(value, nil)) })
  elseif DECIMAL_TYPES[name] then
    return pandoc.Inlines({ pandoc.Str(format_number(value, digits)) })
  elseif name == "date" then
    return pandoc.Inlines({ pandoc.Str(format_date(value) or value) })
  elseif name == "dateTime" or name == "dateTimeStamp" then
    local date = format_date(value)
    local time = value:match("T(%d%d:%d%d)")
    if date and time then return pandoc.Inlines({ pandoc.Str(date), pandoc.Space(), pandoc.Str(time) }) end
    return text_inlines(value)
  elseif name == "boolean" then
    local yes = value == "true" or value == "1"
    return pandoc.Inlines({ pandoc.Str(yes and locale.yes or locale.no) })
  end
  return text_inlines(value)
end

-- ---------------------------------------------------------------------------
-- The table
-- ---------------------------------------------------------------------------

local ALIGNMENTS = { l = pandoc.AlignLeft, r = pandoc.AlignRight, c = pandoc.AlignCenter }

local function markdown_inlines(text)
  if text == nil or text == "" then return pandoc.Inlines({}) end
  return pandoc.utils.blocks_to_inlines(pandoc.read(text, "markdown").blocks)
end

local function split(text, separator)
  local parts = {}
  for part in (text .. separator):gmatch("(.-)" .. separator:gsub("%p", "%%%0")) do
    table.insert(parts, (part:gsub("^%s+", ""):gsub("%s+$", "")))
  end
  return parts
end

local function fail(block, message)
  assert(false, "SPARQL table" .. (block.identifier ~= "" and " #" .. block.identifier or "") .. ": " .. message)
end

local function build_table(block, result, caption)
  local columns = #result.variables
  local attributes = block.attributes

  local headers = {}
  if attributes["header"] then
    local names = split(attributes["header"], "|")
    if #names ~= columns then
      fail(block, string.format("'header' names %d columns, the query returns %d (%s)",
        #names, columns, table.concat(result.variables, ", ")))
    end
    for _, name in ipairs(names) do table.insert(headers, { pandoc.Plain(markdown_inlines(name)) }) end
  else
    for _, name in ipairs(result.variables) do table.insert(headers, { pandoc.Plain(text_inlines(name)) }) end
  end

  local aligns = {}
  if attributes["align"] then
    local letters = attributes["align"]:gsub("[%s,|]", ""):lower()
    if #letters ~= columns or letters:find("[^lrc]") then
      fail(block, string.format("'align' needs one of l, r, c for each of the %d columns, got '%s'", columns, attributes["align"]))
    end
    for letter in letters:gmatch(".") do table.insert(aligns, ALIGNMENTS[letter]) end
  else
    -- Numbers are aligned to the right, everything else to the left.
    for column = 1, columns do
      local numeric, bound = true, false
      for _, row in ipairs(result.rows) do
        local cell = row[column]
        if type(cell) == "table" then
          bound = true
          if not is_numeric(cell) then numeric = false end
        end
      end
      table.insert(aligns, (numeric and bound) and pandoc.AlignRight or pandoc.AlignLeft)
    end
  end

  local widths = {}
  if attributes["widths"] then
    local values, total = split(attributes["widths"], ","), 0
    if #values ~= columns then
      fail(block, string.format("'widths' needs %d values, got '%s'", columns, attributes["widths"]))
    end
    for _, value in ipairs(values) do
      local number = tonumber(value)
      if number == nil or number <= 0 then fail(block, "'widths' must be positive numbers, got '" .. attributes["widths"] .. "'") end
      total = total + number
    end
    for _, value in ipairs(values) do table.insert(widths, tonumber(value) / total) end
  else
    for _ = 1, columns do table.insert(widths, 0) end
  end

  local digits = nil
  if attributes["digits"] then
    digits = math.tointeger(tonumber(attributes["digits"]))
    if digits == nil or digits < 0 then fail(block, "'digits' must be a whole number, got '" .. attributes["digits"] .. "'") end
  end

  local rows = {}
  for _, row in ipairs(result.rows) do
    local cells = {}
    for column = 1, columns do
      table.insert(cells, { pandoc.Plain(format_cell(row[column], digits)) })
    end
    table.insert(rows, cells)
  end

  return pandoc.utils.from_simple_table(pandoc.SimpleTable(caption, aligns, widths, headers, rows))
end

-- ---------------------------------------------------------------------------
-- The filter
-- ---------------------------------------------------------------------------

-- Splits the option lines (`#| key: value` or `#| key="value"`) from the top
-- of the block. Returns the options and the remaining text, the query.
local function cell_options(block)
  local options, lines, in_options = {}, {}, true
  for line in (block.text .. "\n"):gmatch("(.-)\r?\n") do
    local option = in_options and line:match("^%s*#|%s*(.-)%s*$")
    if option then
      local key, value = option:match("^([%w_-]+)%s*[:=]%s*(.-)$")
      if key == nil then
        fail(block, "cannot read the option line '" .. line .. "', expected '#| key: value'")
      end
      local quote = value:sub(1, 1)
      if #value >= 2 and (quote == '"' or quote == "'") and value:sub(-1) == quote then
        value = value:sub(2, -2)
      end
      options[key] = value
    else
      in_options = false
      table.insert(lines, line)
    end
  end
  return options, table.concat(lines, "\n")
end

local function sparql_block(block)
  -- An ordinary ```sparql block stays a listing of code. It becomes a table
  -- with an identifier #tbl-... or with the class .table.
  if not block.classes:includes("sparql") then return nil end
  local options, text = cell_options(block)
  for key, value in pairs(options) do
    if key == "label" then
      block.identifier = value
    else
      block.attributes[key] = value
    end
  end
  if block.identifier:sub(1, 4) ~= "tbl-" and not block.classes:includes("table") then return nil end

  local endpoint = block.attributes["endpoint"]
  if endpoint == nil or endpoint == "" then
    fail(block, "no 'endpoint': name the RDF file (path relative to the document) or the URL of the SPARQL endpoint to query")
  end
  if not is_url(endpoint) then
    endpoint = resolve(endpoint)
    if not exists(endpoint) then
      fail(block, "the file '" .. block.attributes["endpoint"] .. "' does not exist (the path is relative to the document; run `make build` first)")
    end
  end

  local query = text:gsub("{{%s*lang%s*}}", lang)
  local result = run(query, endpoint)

  local limit = tonumber(block.attributes["max-rows"] or "200")
  if #result.rows > limit then
    fail(block, string.format("the query returns %d rows, more than max-rows=%d. Add a LIMIT or raise max-rows.", #result.rows, limit))
  end

  local caption = markdown_inlines(block.attributes["tbl-cap"])
  local blocks = pandoc.Blocks({})
  if block.attributes["echo"] == "true" then
    blocks:insert(pandoc.CodeBlock(query, pandoc.Attr("", { "sparql" })))
  end

  if block.identifier ~= "" then
    local float = quarto.FloatRefTarget({
      identifier = block.identifier,
      type = "Table",
      content = pandoc.Blocks({ build_table(block, result, pandoc.Inlines({})) }),
      caption_long = pandoc.Blocks({ pandoc.Plain(caption) }),
    })
    blocks:insert(float)
  else
    blocks:insert(build_table(block, result, caption))
  end
  return blocks
end

-- The language comes from the metadata, so the document is
-- read first and its blocks afterwards.
function Pandoc(doc)
  local meta = doc.meta
  if meta.lang then
    lang = pandoc.utils.stringify(meta.lang):match("^(%a+)") or lang
  end
  locale = LOCALES[lang] or LOCALES.en
  if quarto.doc.input_file then
    document_dir = pandoc.path.directory(quarto.doc.input_file)
  end
  return doc:walk({ CodeBlock = sparql_block })
end
