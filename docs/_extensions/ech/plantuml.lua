-- Renders PlantUML code blocks as figures. In Markdown output (gfm) the code
-- of the diagram is kept instead, as it is meant to be read as text:
--
--     ```{.plantuml #fig-model fig-cap="The data model."}
--     class Album
--     class Track
--     Album "1" *-- "many" Track
--     ```
--
-- The identifier and the caption are optional; with both, the diagram is a
-- numbered figure that can be referenced with @fig-model. `@startuml` and
-- `@enduml` may be left out.
--
-- The diagram is drawn by plantuml/render.ts, which runs the PlantUML engine
-- on the Deno runtime of Quarto (no Java). Rendered diagrams are kept in
-- plantuml/cache/, so that a diagram is drawn once for all formats and
-- languages.

local script = quarto.utils.resolve_path("plantuml/render.ts")
local cache_dir = quarto.utils.resolve_path("plantuml/cache")

-- The Quarto that renders this document, also when it is not on the PATH.
local function quarto_command()
  local bin = os.getenv("QUARTO_BIN_PATH")
  if bin and bin ~= "" then
    return pandoc.path.join({ bin, "quarto" })
  end
  return "quarto"
end

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

local function render(source)
  local path = pandoc.path.join({ cache_dir, pandoc.utils.sha1(source) .. ".svg" })
  local svg = read_file(path)
  if svg == nil then
    local ok, result = pcall(pandoc.pipe, quarto_command(), { "run", script }, source)
    if not ok then
      local message = type(result) == "table" and result.output or tostring(result)
      error("PlantUML diagram could not be rendered:\n" .. tostring(message) .. "\n\n" .. source)
    end
    svg = result
    write_file(path, svg)
  end
  return svg
end

-- A caption given as an attribute is Markdown.
local function caption_inlines(text)
  if text == nil or text == "" then return pandoc.Inlines({}) end
  return pandoc.utils.blocks_to_inlines(pandoc.read(text, "markdown").blocks)
end

-- Draws the diagram and returns it as an image. The file is written beside
-- the document, into the folder of its other generated files, and registered
-- so that Quarto moves it to the output.
local function image(block)
  local svg = render(block.text)
  local input = quarto.doc.input_file
  local stem = pandoc.path.split_extension(pandoc.path.filename(input))
  -- One folder per output format: Quarto clears the generated files of a
  -- format when it has rendered it.
  local folder = stem .. "_files/plantuml-" .. FORMAT:gsub("[^%w]", "")
  local name = folder .. "/" .. pandoc.utils.sha1(block.text) .. ".svg"
  local path = pandoc.path.join({ pandoc.path.directory(input), name })
  write_file(path, svg)
  quarto.doc.add_supporting(path)

  local attributes = {}
  for key, value in pairs(block.attributes) do
    if key ~= "fig-cap" then attributes[key] = value end
  end
  return pandoc.Image(pandoc.Inlines({}), name, "", pandoc.Attr("", {}, attributes))
end

function CodeBlock(block)
  if not block.classes:includes("plantuml") then return nil end

  local caption = caption_inlines(block.attributes["fig-cap"])
  local content
  if quarto.doc.is_format("markdown") then
    -- Markdown output is read as text (by people and language models): keep
    -- the code of the diagram instead of linking an image.
    content = pandoc.CodeBlock(block.text, pandoc.Attr("", { "plantuml" }))
  else
    content = pandoc.Plain({ image(block) })
  end

  -- With an identifier (#fig-...): a numbered figure that can be referenced.
  if block.identifier ~= "" then
    return quarto.FloatRefTarget({
      identifier = block.identifier,
      type = "Figure",
      content = pandoc.Blocks({ content }),
      caption_long = pandoc.Blocks({ pandoc.Plain(caption) }),
    })
  end
  -- With a caption only: a figure without a number. Otherwise a plain image.
  if #caption > 0 then
    return pandoc.Figure(pandoc.Blocks({ content }), { long = pandoc.Blocks({ pandoc.Plain(caption) }) })
  end
  return content
end
