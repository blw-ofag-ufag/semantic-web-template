# Setting up a project from this template

This template ships with a working demo pipeline based on the Chinook music database, which integrates data with Python, reasons with ROBOT and HermiT, post-processes the graph with SPARQL, validates it with SHACL and Pytest, builds the documentation with Quarto and publishes the graph on LINDAS.

This guide describes how to remove the demo components and replace them with a custom domain model.

## Setting up the local development environment

The following tools must be installed:

* Python 3 (>= 3.10)
* Java (>= 11, required for ROBOT and HermiT; the CI pipeline uses Java 17)
* Quarto CLI (for the documentation)
* curl (for the deployment to LINDAS)

Then run in the project directory:

```bash
make setup
```

This creates a virtual environment in `venv/`, installs the Python packages and downloads ROBOT.

> [!NOTE]
> On Posit Workbench or in paths containing @, VS Code may report Unable to handle .../.venv.
> In this case, select the interpreter manually: `Ctrl + Shift + P` -> Python: Select Interpreter -> Enter interpreter path... -> `venv/bin/python`.

## Removing demo data and building the domain model

### Prefixes (`src/rdf/prefixes.ttl`)

> [!IMPORTANT]
> All prefixes used in the project must be declared in this file. The build uses only these prefixes, and the test suite checks that they are used consistently across the repository.

The file consists of three blocks:

* **Project-specific:** replace the demo prefixes (album, artist, track, etc.) with the project namespace and its sub-namespaces.
* **LINDAS-specific:** optional, can remain in the file.
* **Globally used:** W3C and other standards, keep them.

### Data integration (`src/python/pipeline/`)

The Makefile runs all Python scripts in this folder in alphabetical order. It calls each script with `--output build/rdf/00-integrated.ttl`, and the script must write its triples as Turtle to exactly this file. The build then merges this file into the graph. If there are several scripts, only the first one may overwrite the file; every further script must add its triples to the existing file, otherwise the triples of the previous scripts are lost. 

**Option A: with data integration** (e.g. from a database, an API or CSV files)

1. Delete the demo script: `rm src/python/pipeline/01_integrate_example_data.py`
2. Add a custom script to this folder, e.g. `01_import_data.py`, that reads the target file from the `--output` argument (e.g. with argparse).

**Option B: static Turtle files only**

Delete all scripts with `rm -f src/python/pipeline/*.py`. The Makefile then creates an empty file instead.

### Static data and glossary (`src/rdf/data/`)

All Turtle files in this folder are merged into the graph. Delete the demo files and add custom master data or vocabularies:

```bash
rm src/rdf/data/genres.ttl src/rdf/data/people.ttl
```

> [!IMPORTANT]
> Do not delete `glossary.skos.ttl`: the documentation requires it. Replace its demo concepts and the demo namespace with the project's own terms and namespace instead.

### Ontology (`src/rdf/ontology/model.owl.ttl`)

Replace the demo classes and properties with the custom OWL model, following the [naming conventions](.github/CONTRIBUTING.md#rdf-resource-naming-convention).

### SHACL shapes (`src/rdf/shapes/model.shacl.ttl`)

Replace the demo shapes with shapes for the custom classes. Provide all labels and messages in every documentation language. Do not change `glossary.shacl.ttl`; it is maintained by the template.

### SPARQL post-processing (`src/sparql/processing/`)

After reasoning, the build applies all SPARQL updates in this folder to the graph. Delete the demo updates:

```bash
rm src/sparql/processing/02_author_linking.rq src/sparql/processing/03_create_companies.rq
```

> [!IMPORTANT]
> Keep `01_hermit_cleanup.rq`. It is not part of the demo but removes auxiliary triples that HermiT adds during reasoning.

Custom updates can be added as further `.rq` files. They must use SPARQL Update (INSERT/DELETE) and declare their prefixes; SELECT queries abort the build.

### Example queries (`src/sparql/queries/`)

The test suite runs every query in this folder against LINDAS. Replace the demo query `test.rq` with queries on the project's published data. Each query must start with a descriptive `#` comment and return at least one result.

## Adapting the documentation (`docs/`)

The pages `entities.md` and `glossary.md` are generated from the SHACL shapes and the glossary on every `make docs`. Everything else is maintained manually.

### Website configuration (`docs/_quarto.yml`)

Adapt `website.title`, `repo-url`, the `announcement` banner and the links in the `navbar` to the project.

If `make docs` fails because the Word template referenced under `reference-doc` cannot be downloaded, delete or comment out this line.

### Landing pages (`docs/{de,en,fr}/index.qmd`)

Replace the template texts with the project description, and replace the Chinook examples in `docs/data/` that the pages include.

The front matter carries the metadata of the eCH title page. `title` is the name of the standard without the eCH number; `date` is the date of issue, formatted as ISO date. The remaining fields of the eCH metadata table live under `ech:` and are written in the language of the respective page, for example in `docs/en/index.qmd`:

```yaml
ech:
  number: eCH-1234                      # eCH number
  category: Standard                    # category
  maturity: Defined                     # quality stage
  version: 2.4.1                        # version
  status: Approved                      # status, printed in bold in the footer
  decision-date: 2026-09-15             # date of decision
  replaces: 2.4.0 – Minor Change        # replaced version
  prerequisites: eCH-0200               # requirements, string or list (optional)
  attachments: [schema.xsd, model.ttl]  # annexes, string or list (optional)
  languages: German (original), French (translation), English (translation)
  group: Technical Unit AgriFood        # technical unit
  publisher: ...                        # editor / distribution, defaults to Verein eCH (optional)
```

Fields that are left out are printed as `---`. The PDF layout itself (header, footer, title page, table of contents) is defined in `docs/assets/typst-template.typ`; the labels of the metadata table are translated there for `de`, `fr` and `en`.

The translations are checked by the test suite: every heading needs a reference ID, and all language versions must have the same headings, the same number of lines, code blocks, images and table rows, and a similar text length.

### Languages

The template is set up for German (`de`), English (`en`) and French (`fr`). Each language requires a folder in `docs/` and matching language tags in the SHACL shapes.

For a single-language project, delete the folders of the other languages. For example, for a German-only project:

```bash
rm -rf docs/en docs/fr
```

Then remove these languages from `render:` in `docs/_quarto.yml`:

```diff
 project:
   output-dir: ../build/docs/
   type: website
   render:
     - de/index.qmd
-    - fr/index.qmd
-    - en/index.qmd
```

## Running the pipeline locally

```bash
make test   # build the graph (integration, reasoning, SPARQL, SHACL) and run the test suite
make docs   # generate the documentation in build/docs/
make        # both of the above
```

If a step fails, `build/log/` contains a log file for each step. `make clean` removes all build artifacts.

## Deployment to LINDAS

The CI pipeline tests every pull request. On `main`, it also publishes the graph to LINDAS and the documentation to GitHub Pages. For this, add `ENDPOINT`, `USER`, `PASSWORD` and `GRAPH` as repository secrets under Settings > Secrets and variables > Actions.

For a manual deployment, create a `.env` file in the root directory (it is ignored by Git). Do not use quotes, as the Makefile reads the values literally:

```dotenv
ENDPOINT=https://test.lindas.admin.ch/sparql
USER=blw-service-account
PASSWORD=my-secure-password
GRAPH=https://agriculture.ld.admin.ch/foag/my-project
```

```bash
make publish   # run the tests, clear the named graph on LINDAS and upload the new graph
make delete    # only clear the named graph on LINDAS
```

After these steps, the repository contains only the project's own model, data and documentation, and the pipeline is ready for development and deployment.