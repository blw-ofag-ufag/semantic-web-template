# Semantic web project template

[![CI](https://github.com/blw-ofag-ufag/semantic-web-template/actions/workflows/ci.yml/badge.svg)](https://github.com/blw-ofag-ufag/semantic-web-template/actions/workflows/ci.yml)
[![GitHub last commit](https://img.shields.io/github/last-commit/blw-ofag-ufag/semantic-web-template.svg)](https://github.com/blw-ofag-ufag/semantic-web-template/commits)
[![GitHub issues](https://img.shields.io/github/issues/blw-ofag-ufag/semantic-web-template.svg)](https://github.com/blw-ofag-ufag/semantic-web-template/issues)

This template repository publishes an eCH standard together with its linked data. It builds an RDF graph, validates it, uploads it to [LINDAS](https://lindas.admin.ch/) and renders the documentation as a website and a PDF in the eCH layout.

For demonstrative purposes, it includes a full pipeline that creates a graph of around 120 000 triples from the Chinook music database:

1. manual data curation (data files and code lists in `src/rdf/data/`),
2. data integration from a relational database (Python scripts in `src/python/pipeline/`),
3. RDFS inference (using the ontology in `src/rdf/ontology/model.owl.ttl` and the rules in `src/sparql/inference/`),
4. SPARQL-based processing of the graph (updates in `src/sparql/processing/`),
5. SHACL-based validation of the graph (using `src/rdf/shapes/model.shacl.ttl`),
6. a Pytest test suite for everything SHACL cannot check,
7. upload of the final graph to LINDAS,
8. documentation in several languages, built with Quarto.

> [!IMPORTANT]
> After using this template repository for a project, you probably want to delete or overwrite the demo files. [CLEANUP.md](CLEANUP.md) describes how.

## Getting started

The following tools must be installed:

- Python 3.10 or newer
- [Quarto](https://quarto.org/) (for the documentation)
- curl (for the upload to LINDAS)
- the font Nimbus Sans (for the PDF; package `fonts-urw-base35` on Debian and Ubuntu)

Then run:

``` sh
make setup   # create venv/ and install the Python packages
make check   # check the sources, in about a second
make         # build the graph, test it and render the documentation
```

## Configuration

[`project.yml`](project.yml) is the single place that states what the project is:

| Section | Content |
| --- | --- |
| `date`, `ech` | The eCH document: number, version, status, category, languages and the other entries of the title page. |
| `project` | The GitHub repository and the contact. |
| `lindas` | The named graph, the endpoint it is uploaded to, the endpoint the example queries are tested against and the query editor linked from the documentation. |
| `dataset` | The description of the graph as a dataset: titles, descriptions, keywords, publisher, themes and terms of use. |

Everything else is derived from it. `make build` generates the description of the dataset (`build/rdf/metadata.ttl`), and `make docs` generates the metadata for Quarto (`docs/_project.yml`): the eCH title page, the pages to render, the title of the website, its navigation with the language menu, and the banner shown as long as the document is not approved. The tests, the documentation generators and `make publish` read the file as well. `make check` validates it.

Only the credentials for LINDAS are kept elsewhere, see [Publication](#publication).

## Make targets

`make` is the single entry point of the project. `make help` lists all targets.

| Target | What it does | Needs |
| --- | --- | --- |
| `make setup` | Creates the virtual environment `venv/` and installs the Python packages. | Python, network |
| `make check` | Checks the sources: Turtle syntax, prefixes, the project configuration, translations, code lists and glossary. Takes about a second. | |
| `make build` | Builds the graph into `build/rdf/03-processed.ttl`. Takes about ten seconds. | network |
| `make test` | Builds the graph, validates it with SHACL and runs the whole test suite. Takes about a minute. | network |
| `make docs` | Generates the data model, code list and glossary pages and renders the website and the PDF into `build/docs/`. | Quarto |
| `make` | Runs `make test` and `make docs`. | |
| `make publish` | Runs `make test`, then replaces the graph on LINDAS. | `.env` |
| `make delete` | Deletes the graph on LINDAS. | `.env` |
| `make clean` | Removes `build/`, `venv/`, caches and generated pages. | |

The Makefile hides the output of the tools. If a step fails, its log is in `build/log/`.

## Repository layout

| Path | Content |
| --- | --- |
| `project.yml` | The configuration of the project, see [Configuration](#configuration). |
| `src/rdf/ontology/` | The OWL ontology. |
| `src/rdf/shapes/` | The SHACL shapes of the data model (`model.shacl.ttl`), of code lists and of the glossary. |
| `src/rdf/data/` | Manually curated data, code lists and the glossary. |
| `src/rdf/prefixes.ttl` | All prefixes of the project. Every other file must use them consistently. |
| `src/python/pipeline/` | Data integration scripts, run in alphabetical order. |
| `src/python/utils/` | Tools of the template: project configuration, graph build, documentation generators, modification date. |
| `src/sparql/inference/` | Inference rules as SPARQL updates, applied to the merged graph until nothing new is derived. |
| `src/sparql/processing/` | SPARQL updates applied to the graph after inference, in alphabetical order. |
| `src/sparql/queries/` | Example queries, tested against LINDAS. |
| `docs/` | The documentation: one folder per language and the Quarto configuration. |
| `docs/_extensions/ech/` | The eCH layout as a Quarto extension: Lua filters, shortcodes, Typst template, styles, citation style and vocabulary. It provides the formats `ech-html`, `ech-typst`, `ech-gfm` and `ech-docx` that `docs/_quarto.yml` uses. |
| `tests/` | The Pytest suite. |
| `build/` | Everything generated: graphs, logs, test reports and the rendered documentation. Not in Git. |

The pages `entities.md`, `codelists.md`, `namespaces.md` and `glossary.md` in the language folders are generated by `make docs` from the shapes, the graph and the glossary, and `docs/_project.yml` from `project.yml`. They are not in Git and must not be edited.

## How the graph is built

Each step writes one file to `build/rdf/`, so that the result of every step can be inspected:

| File | Step |
| --- | --- |
| `00-integrated.ttl` | The scripts in `src/python/pipeline/` integrate the source data. |
| `metadata.ttl` | The description of the graph as a dataset is generated from `project.yml`. |
| `01-merged.ttl` | Both are merged with the ontology, the shapes and the files in `src/rdf/data/`. |
| `02-inferred.ttl` | The rules in `src/sparql/inference/` derive new statements from the ontology. |
| `03-processed.ttl` | The SPARQL updates in `src/sparql/processing/` are applied and the modification date of the dataset is set. This is the graph that is tested and published. |
| `04-shacl-report.ttl` | pyshacl validates the graph against `model.shacl.ttl`. |

`src/python/utils/build_graph.py` merges, infers and applies the updates in a single run, in memory, with [Oxigraph](https://pyoxigraph.readthedocs.io/). `01-merged.ttl` and `02-inferred.ttl` are written with one statement per line; only `03-processed.ttl` is formatted for readers.

The inference covers RDFS: sub-classes, sub-properties, domains and ranges (`src/sparql/inference/rdfs.rq`). It is not an OWL reasoner: restrictions, inverse or transitive properties are not evaluated, and the ontology is not checked for consistency. A project that needs more adds a rule file to `src/sparql/inference/`.

The modification date is today's date if the graph differs from the one on LINDAS or if LINDAS cannot be reached, otherwise the date found there.

## Tests

The test suite in `tests/` has three kinds of tests:

| Kind | What they check | Run by |
| --- | --- | --- |
| Offline | The sources: Turtle syntax, consistent prefixes, the project configuration, aligned translations, the structure of code lists and glossary. | `make check`, `make test` |
| Graph | The built graph: one test per SHACL shape, and the naming conventions. | `make test` |
| Network | Every link in the Markdown files, the example queries on LINDAS, and the differences to the template repository. | `make test` |

A network test can fail for reasons outside the repository, for example when a linked website is unavailable.

## Publication

The graph is uploaded to [LINDAS](https://lindas.admin.ch/), the linked data service of the Swiss Federal Archives. The upload replaces the content of the named graph in a single request; if it fails, the published graph stays as it was.

The named graph and the endpoint come from the section `lindas` of `project.yml`. Only the credentials are kept outside the repository:

``` dotenv
LINDAS_USER=********
LINDAS_PASSWORD=********
```

**Automatic deployment.** GitHub Actions tests every pull request. On every push or merge to the `main` branch, it also publishes the graph to LINDAS and the documentation to GitHub Pages. For this, add the two variables as repository secrets (`Settings > Secrets and variables > Actions > New repository secret`).

**Manual deployment.** Write the two variables to a file `.env` in the root directory, without quotes. The file is ignored by Git. Then run:

``` sh
make publish   # run the tests and replace the graph on LINDAS
make delete    # only delete the graph on LINDAS
```

## Tools and standards

| Tool | Use |
| --- | --- |
| [Oxigraph](https://pyoxigraph.readthedocs.io/) | Merges the graph and runs the inference rules and the SPARQL updates. It also runs the SPARQL queries that the documentation renders as tables. |
| [RDFLib](https://rdflib.readthedocs.io/) | Parses, serialises and manipulates RDF in Python. |
| [PySHACL](https://github.com/RDFLib/pySHACL) | Validates the graph against the SHACL shapes. |
| [Pytest](https://docs.pytest.org/) | Runs the test suite. |
| [PlantUML](https://plantuml.com/) | Draws the UML diagrams of the documentation from code blocks. The JavaScript build of the engine runs on the Deno runtime that ships with Quarto, so Java is not needed; it is downloaded on first use. |
| [Quarto](https://quarto.org/) | Renders the documentation. It runs the Python code chunks with the virtual environment, so no other language runtime is needed. |
| [Matplotlib](https://matplotlib.org/) | Draws the figures of the documentation. |

The project relies on the W3C standards [RDF](https://www.w3.org/RDF/) (data model), [Turtle](https://www.w3.org/TR/turtle/) (serialisation of all RDF files), [OWL](https://www.w3.org/OWL/) (ontology), [SHACL](https://www.w3.org/TR/shacl/) (validation) and [SPARQL](https://www.w3.org/TR/sparql11-overview/) (queries and updates).

## Further documentation

- [CLEANUP.md](CLEANUP.md): setting up a project from this template.
- [CONTRIBUTING.md](.github/CONTRIBUTING.md): Git workflow, naming conventions and figure style.

## Contact

Do you have questions? Please do not hesitate to contact us at [agridata.ch@blw.admin.ch](mailto:agridata.ch@blw.admin.ch), open an [issue in this repository](../../issues), or directly submit a [Request for Change (RFC) via the official eCH feedback form](https://ech.ch/de/ech-standards/standardisierungsprozess/request-change-rfc).
