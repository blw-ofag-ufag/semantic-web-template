# Contributing

To ensure a smooth collaboration and maintain code quality, please adhere to the following workflow.

## Collaboration via GitHub

### Open an issue

Before writing any code, **open a GitHub Issue** to discuss the proposed change.
Whether it is a bug fix, feature request, or architectural adjustment, establish the scope in an issue first.

### Create a branch

Create a new branch for your specific task. Let GitHub autogenerate the branch name based on an issue; that way it's clear what you're trying to do on said branch.

### Submit a pull request

Once your work is ready:

1. Open a draft PR against the `main` branch.
2. Summarize your changes clearly in the description.
3. Link the PR to the issue it resolves (e.g. `Closes #42`).
4. Ensure there are no merge conflicts and all tests are passed before you change the status to a standard pull request.

### Merging and Deployment

Once your pull request is reviewed and approved, it can be merged into the `main` branch.

> [!IMPORTANT]
> Merging to `main` triggers an automatic deployment workflow. The new version of the RDF graph will be published to LINDAS, replacing the previous version. Ensure your changes are final and have passed all tests before merging.

## Naming conventions

### File naming convention

All files in this project should be named with `snake_case` and lowercase letters.

### RDF namespace naming convention

Namespaces follow a standardized pattern and include the project's eCH identifier, and the major version number[^1]:

[^1]: Embedding only the major version number in the namespace creates a structural contract. If a subsequent release introduces breaking changes, a new major version (and consequently, a new namespace) will be created. This isolates the versions, ensuring that existing data graphs can remain perfectly valid using the old schema while allowing downstream consumers to migrate to the new version at their own pace.

```
https://agriculture.ld.admin.ch/{identifier}/{version}/
```

Note that we use LINDAS namespaces in order to be able to dereference any defined resource.
Following this logic, we would assign a property `eppoCode` specified in a hypothetical version 3.4.1 of a standard eCH-1234 the following URI: 

```
https://agriculture.ld.admin.ch/eCH-1234/3/eppoCode
```

### RDF resource naming convention

Aligning with standard Semantic Web conventions, we enforce the following casing rules for URI local names:

- **Classes and important individuals** (e.g., instances of `owl:Class`): Use **PascalCase** (a.k.a. UpperCamelCase).
- **Properties** (e.g., `owl:ObjectProperty`, `owl:DatatypeProperty`): Use **camelCase** (a.k.a. lowerCamelCase). Don't include starting verbs, i.e. `eppoCode` would be preferred over `hasEppoCode`.

Ensure identifiers are meaningful to facilitate readability and improve [DX](https://en.wikipedia.org/wiki/Developer_experience).

For individuals, use a sub-namespace based on the most important classes. For example, if the project namespace is `https://agriculture.ld.admin.ch/eCH-1234/2/`, use `https://agriculture.ld.admin.ch/eCH-1234/2/person/` for all people:

``` ttl
@prefix eCH-1234: <https://agriculture.ld.admin.ch/eCH-1234/2/> .
@prefix person:   <https://agriculture.ld.admin.ch/eCH-1234/2/person/> .

person:1 a eCH-1234:Person .
person:2 a eCH-1234:Person .
person:3 a eCH-1234:Person .
```

## Diagrams

UML diagrams are written as [PlantUML](https://plantuml.com/) code in the document and drawn when it is rendered. The website, the PDF and the Word file show the drawing; the Markdown version keeps the code, because it is meant to be read as text:

````markdown
```{.plantuml #fig-model fig-cap="The data model."}
class Album
class Track
Album "1" *-- "1..*" Track : contains
```
````

With an identifier that starts with `fig-`, the diagram is a numbered figure that is listed and can be referenced with `@fig-model`. `@startuml` and `@enduml` may be left out. Keep the code of a diagram identical in all language versions and translate only its caption.

The diagrams are drawn by the Quarto extension in `docs/_extensions/ech/` (`plantuml.lua`, `plantuml/render.ts`) without Java. The first render downloads the PlantUML engine (about 9 MB) into `docs/_extensions/ech/plantuml/vendor/` and checks it against a fixed checksum. Sprites and embedded images are not supported.

## Tables from SPARQL queries

A table can be the result of a SPARQL `SELECT` query. The query is run when the document is rendered, on the `endpoint` that the block names: an RDF file such as the built graph, or a SPARQL endpoint on the web.

````markdown
```{.sparql #tbl-genres endpoint="../../build/rdf/03-processed.ttl" tbl-cap="Tracks per genre." header="Genre|Tracks" align="lr"}
PREFIX schema: <http://schema.org/>
SELECT ?name (COUNT(?track) AS ?tracks)
WHERE { ?track schema:genre/schema:name ?name }
GROUP BY ?name ORDER BY DESC(?tracks) LIMIT 10
```
````

A `sparql` block is rendered as a table if its identifier starts with `tbl-` or if it has the class `.table`; every other `sparql` block stays a listing of code. Only `endpoint` is required:

| Attribute | Meaning | Default |
| --- | --- | --- |
| `endpoint` | What to query: an RDF file (`.ttl`, `.nt`; path relative to the document) or the URL of a SPARQL endpoint (`https://...`). | Required |
| `#tbl-...` | Numbered table that is listed and can be referenced with `@tbl-...`. | |
| `tbl-cap` | Caption. | |
| `header` | Column headers, separated by `|`. | The variable names |
| `align` | One letter per column: `l`, `r` or `c`. | Numbers right, others left |
| `widths` | Relative column widths, separated by commas. | Automatic |
| `digits` | Decimal places of decimal numbers. | As in the data |
| `max-rows` | Upper limit of rows; more rows are an error, to catch a missing `LIMIT`. | 200 |
| `echo` | `true` shows the query above the table. | |

The attributes can also be written as lines beginning with `#|` at the top of the block, as in the code cells of Quarto; `label` stands for the identifier. For SPARQL these lines are comments. Where both forms set the same attribute, the `#|` line applies:

````markdown
```{.sparql}
#| label: tbl-genres
#| endpoint: ../../build/rdf/03-processed.ttl
#| tbl-cap: "Tracks per genre."
#| header: "Genre|Tracks"
#| align: lr
PREFIX schema: <http://schema.org/>
SELECT ?name (COUNT(?track) AS ?tracks)
WHERE { ?track schema:genre/schema:name ?name }
GROUP BY ?name ORDER BY DESC(?tracks) LIMIT 10
```
````

Values are shown according to their datatype and the language of the document: integers with a thousands separator, decimals with the decimal mark, dates and booleans in the usual notation, IRIs as links. A query is self-contained: it declares its prefixes itself, and an IRI of the result is abbreviated with them (`genre:1`) if the query declares a matching prefix. Write `{{lang}}` in the query for the language of the document, e.g. `FILTER(lang(?label) = "{{lang}}")`, and keep the query identical in all language versions; translate only the caption and the headers. Always sort the result (`ORDER BY`), so that the table does not change from one build to the next.

A table from an endpoint on the web shows the data of the moment of rendering, and the render fails if the endpoint cannot be reached. Its result is kept for the current hour, so that the formats and languages of one render ask only once.

## Figures

Data analyses and figures of the documentation are written in Python; the project does not use R. Code chunks in `docs/*/index.qmd` run with the packages of `src/python/requirements.txt`, which `make setup` installs into the virtual environment.

All figures share one plot style, `docs/_extensions/ech/ech.mplstyle` (based on ggplot2's `theme_minimal()`): a white background, no axis lines or ticks, a light grey grid behind the data, grey tick labels and the eCH red `#D00D28` as the first colour. Load it at the beginning of every chunk that draws a figure, give the chunk a label and a caption, so that the figure is numbered and listed, and set the size of the figure in inches with `figsize` (the chunk options `fig-width` and `fig-height` have no effect on Python chunks):

````markdown
```{python}
#| label: fig-example
#| fig-cap: "Caption of the figure."
import matplotlib.pyplot as plt

plt.style.use("../_extensions/ech/ech.mplstyle")
fig, ax = plt.subplots(figsize=(6, 2.5))
ax.barh(["A", "B"], [1, 2], height=0.9)
plt.show()
```
````

Write axis labels in the language of the page, and adapt the style file only in the template, so that all projects keep the same look.

## Alignment with eCH processes

To maintain consistency, the releases of this repository must strictly align with the official status of the corresponding document on [ech.ch](https://www.ech.ch/).

- **Official releases:** A GitHub release is *only* created when the document is officially published as an approved standard on the eCH website.
- **Pre-releases (QS/ÖK):** While the project is in intermediate stages such as quality control (QS) or public consultation (ÖK), we use pre-releases.

For a comprehensive overview of the standardization phases, please refer to the [eCH-0003 guidelines](https://www.ech.ch/de/ech/ech-0003).

## Contact

Do you have questions? Please do not hesitate to contact us at [agridata.ch@blw.admin.ch](mailto:agridata.ch@blw.admin.ch), open an [issue in this repository](../../issues), or directly submit a [Request for Change (RFC) via the official eCH feedback form](https://ech.ch/de/ech-standards/standardisierungsprozess/request-change-rfc).
