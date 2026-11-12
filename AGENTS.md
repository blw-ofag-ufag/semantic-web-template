# Guide for coding agents

This repository is a template for publishing an eCH standard together with its linked data. It builds an RDF graph, validates it, publishes it on LINDAS and renders the documentation (website, PDF) in the eCH layout. The demo content is the Chinook music database.

Related documents:

- [README.md](README.md): overview of the pipeline and the tools.
- [.github/CONTRIBUTING.md](.github/CONTRIBUTING.md): Git workflow, naming conventions and figure style.
- [CLEANUP.md](CLEANUP.md): how to turn the template into a project. It exists only in the template and in projects that have not finished their setup.

## Rules

- **Never run `make publish` or `make delete`.** They act on the production graph on LINDAS with the credentials in `.env`.
- **Never read, print or change `.env`.** It holds the LINDAS credentials.
- **Never push to `main` or merge into it.** A merge deploys the graph and the website. Work on a branch and leave commits to the user unless they ask for them.
- **Do not edit generated files.** Change their source instead (see the table below).
- **Do not edit template-managed files in a project.** Propose the change for the template repository. In the template repository itself they are edited normally.

## Commands

The tools required are Python 3.10 or newer, Java 11 or newer, Quarto and curl.

| Command | What it does | Time |
| --- | --- | --- |
| `make setup` | Creates `venv/`, installs the Python packages and downloads ROBOT. | 1 min |
| `make build` | Builds the graph into `build/rdf/03-processed.ttl`. | 1 min |
| `make test` | Builds, validates with SHACL and runs all tests. | 3 min |
| `make docs` | Generates the data model pages and renders the documentation into `build/docs/`. | several min |
| `make help` | Lists all targets. | |

`make build` downloads the Chinook database. If `.env` exists, it also reads the published graph from LINDAS to set the modification date.

For a quick check that needs neither Java, the network nor a built graph, run the offline tests directly (about one second):

``` sh
venv/bin/pytest -p no:cacheprovider -q tests/test_syntax.py tests/test_prefixes.py \
    tests/test_ech_config.py tests/test_metadata.py tests/test_translations.py \
    tests/test_codelists.py tests/test_glossary.py
```

The Makefile hides the output of the tools. When a step fails, read its log in `build/log/`.

## Who owns which file

| Owner | Files | Rule |
| --- | --- | --- |
| Project | `src/rdf/ontology/`, `src/rdf/data/`, `src/rdf/shapes/model.shacl.ttl`, `src/rdf/metadata.ttl`, `src/rdf/prefixes.ttl`, `src/python/pipeline/`, `src/sparql/`, `docs/_ech.yml`, `docs/_quarto.yml`, `docs/references.yaml`, `docs/{de,fr,en}/index.qmd`, `docs/data/`, `Makefile`, `README.md` | Edit freely. |
| Template | `tests/`, `src/python/utils/`, `docs/assets/`, `src/rdf/shapes/glossary.shacl.ttl`, `src/rdf/shapes/codelist.shacl.ttl`, `.github/` | Edit only in the template repository. `tests/test_template_sync.py` warns about differences. |
| Generated | `build/`, `docs/*/entities.md`, `docs/*/codelists.md`, `docs/*/namespaces.md`, `docs/*/glossary.md` | Never edit. They are ignored by Git and rewritten by `make build` and `make docs`. |

The generated pages come from `src/python/utils/generate_shacl_docs.py` (shapes and graph) and `src/python/utils/generate_glossary_docs.py` (`src/rdf/data/glossary.skos.ttl`). To change their content, change the shapes or the glossary; to change their form, change the generator.

## How the graph is built

1. The scripts in `src/python/pipeline/` run in alphabetical order and write `build/rdf/00-integrated.ttl`. Each script receives `--output`. The first script creates the file; every further script must add to it.
2. ROBOT merges that file with the ontology, `model.shacl.ttl`, `metadata.ttl`, the files in `src/rdf/data/` and the prefixes.
3. HermiT infers class and property assertions.
4. The SPARQL updates in `src/sparql/processing/` run in alphabetical order. They must be updates (`INSERT`, `DELETE`); a `SELECT` aborts the build. Keep `01_hermit_cleanup.rq`, which removes artefacts of the reasoner.
5. pyshacl validates the result against `model.shacl.ttl`. Its exit code is ignored on purpose: `tests/test_shacl.py` turns each shape into a test and reports the violations.

## Invariants that the tests enforce

- **Translations stay aligned.** The files `docs/{de,fr,en}/index.qmd` must have the same number of lines, the same headings with the same reference IDs (`{#sec-...}`), and the same number of code blocks, images and table rows. Their text lengths must be within 25 % of each other. Any change to one language needs the same change, on the same lines, in the others.
- **Shapes are translated.** Every label, description and message in `model.shacl.ttl` exists in every documentation language.
- **Prefixes are declared once.** `src/rdf/prefixes.ttl` is the reference. A prefix used in any `.ttl`, `.rq`, `.py`, `.md` or `.qmd` file must map to the same namespace as there. Add new prefixes to that file.
- **The namespace follows the eCH number.** It is `https://agriculture.ld.admin.ch/{number}/{major version}/`, with the number and version from `docs/_ech.yml`.
- **Names follow the conventions.** Classes and individuals use PascalCase, properties camelCase without a leading verb, and files lowercase snake_case. Violations are warnings, not failures.
- **The eCH metadata uses codes.** The values in `docs/_ech.yml` must be codes listed in `docs/assets/ech_vocabulary.yml`. The languages listed there must match the folders rendered by `docs/_quarto.yml`.
- **The dataset describes the graph.** The subject of `src/rdf/metadata.ttl` is `ech.graph` from `docs/_ech.yml`, and the file must not contain a modification date, which the build sets.
- **Code lists and the glossary have a fixed structure**, given by `codelist.shacl.ttl` and `glossary.shacl.ttl`.
- **Example queries are documented.** Every file in `src/sparql/queries/` starts with a `#` comment and returns at least one result from LINDAS.

## Verifying a change

| Change | Check |
| --- | --- |
| Turtle, SPARQL, prefixes | The offline tests above, then `make test`. |
| Shapes or ontology | `make test`. Read the failures of `tests/test_shacl.py`; each names the shape and the nodes that violate it. |
| Documentation text | `tests/test_translations.py` and `tests/test_links.py`, then `make docs` if the layout is affected. |
| Lua filters, Typst template, styles | `make docs`, then look at the PDF and the website in `build/docs/`. |
| Makefile or `src/python/utils/` | `make test` and `make docs`. |

Three test files need the network: `test_links.py` (every URL in the Markdown files), `test_queries.py` (LINDAS) and `test_template_sync.py` (GitHub). If one of them fails on something the change did not touch, report it; do not remove the link or the query to make the test pass. `test_naming.py` and `test_template_sync.py` report warnings by design.

## Pitfalls

- **Quarto rewrites metadata values that look like paths.** A language code `de` in `docs/_ech.yml` arrives in the Lua filter as `../de`, because the folder `docs/de/` exists. The filter keeps only the last path component. Avoid metadata values that match a file or folder name.
- **An empty Lua table becomes `true` in Pandoc metadata.** Use `pandoc.MetaList({})` for lists that can be empty.
- **Python chunks ignore `fig-width` and `fig-height`.** Set the size with `figsize` and load `docs/assets/ech.mplstyle`. The documentation uses Python only, not R.
- **The PDF needs the font Nimbus Sans** (package `fonts-urw-base35` on Debian and Ubuntu).
- **`make clean` also deletes `venv/`.** Run `make setup` afterwards.
