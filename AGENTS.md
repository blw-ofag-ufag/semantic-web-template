# AGENTS.md

Template for eCH standards: an RDF data model and data, validated with SHACL,
published on LINDAS and documented as a multilingual eCH document with Quarto.
The template ships with demo content (the Chinook music database); a project
created from it replaces the demo with its own model and data. 
This file serves the template repository and every project created from it; 
`git remote -v` shows which one you are in.

## Build and test

Run all commands from the repository root.

```sh
make setup   # once: creates venv/, installs the Python packages and ROBOT
make test    # steps 1–6 below
make docs    # step 7 (builds the graph first if needed)
make clean   # removes build/ and venv/; run make setup again afterwards
```

Every step writes into `build/`:

1. `src/python/pipeline/*.py` integrate external data → `build/rdf/00-integrated.ttl`
2. ROBOT merges it with `src/rdf/` (ontology, shapes, data, metadata) → `01-merged.ttl`
3. HermiT infers new triples → `02-inferred.ttl`
4. The SPARQL updates in `src/sparql/processing/` run → `03-processed.ttl` (the final graph)
5. pyshacl validates the graph against `src/rdf/shapes/model.shacl.ttl` → `04-shacl-report.ttl`
6. pytest runs the tests in `tests/`
7. Pages are generated from the shapes, the graph and the glossary, and Quarto renders `docs/` → `build/docs/`

On `main`, the CI publishes the graph on LINDAS and the documentation on GitHub Pages.

- Check every change with `make test`, not with `pytest` alone: pytest reads the
  graph in `build/` and does not rebuild it. After `make test`, a single test
  file can be repeated with `venv/bin/pytest tests/<file>.py -v`.
- `make` reruns only the steps whose inputs changed, so a repeated `make test` is fast.
- The Makefile hides the output of the tools. If a step fails, read its log in `build/log/`.


## Common tasks

The documentation languages are the folders in `docs/` (de, fr, en); every RDF
text needs a language tag for each of them (`@de`, `@fr`, `@en`).

- **Add or change a property of a class:** add a property shape to
  `src/rdf/shapes/model.shacl.ttl` with `sh:name` (and `sh:message` if needed) in
  every documentation language and `sh:order` for its position in the
  documentation. Declare new classes and properties of the project namespace in
  `src/rdf/ontology/model.owl.ttl`. Shapes with `sh:closed true` reject data that
  has no property shape.
- **Add or change data:** static data, code lists and the glossary live in
  `src/rdf/data/`; every `.ttl` file there is merged into the graph.
- **Integrate external data:** a script in `src/python/pipeline/` that writes
  Turtle to the file given by `--output`. The first script overwrites the file,
  every further script appends to it.
- **Add a code list:** a new file in `src/rdf/data/` modelled on `mediatypes.ttl`.
  Every list and code needs a name and a description in every documentation
  language. Restrict a property to the list with
  `sh:node [ sh:property [ sh:path schema:inCodeSet ; sh:hasValue <list> ] ]`.
- **Add a glossary term:** `src/rdf/data/glossary.skos.ttl`, with name and
  description in every documentation language.
- **Change the documentation:** edit `docs/de`, `docs/fr` and `docs/en` together,
  on the same lines. New headings need an ID (`{#sec-...}`); cite with `[@key]`
  from `docs/references.yaml`. Write German in Swiss spelling (ss, never ß), here
  and in the `@de` labels of the RDF files.
- **Add a figure:** a Python chunk with a label `fig-...` and a caption that
  loads `../assets/ech.mplstyle` and sets its size with `figsize`. Take colours
  from the style; never hard-code them.
- **Transform the graph:** a SPARQL Update (INSERT/DELETE) in
  `src/sparql/processing/`; the number in the file name sets the order.
- **Set up a new project from this template:** follow `CLEANUP.md`.

## Boundaries

Never:

- Run `make publish` or `make delete`: they replace or delete the published graph on LINDAS.
- Read, print or commit `.env`: it holds the LINDAS credentials.
- Push to `main` or force-push: `main` is published automatically. Work on a branch.
- Edit generated files (`build/`, `docs/*/{entities,namespaces,codelists,glossary}.md`);
  change their source instead.
- Delete or weaken a link, a query or a test to make a failing test pass.

Ask first:

- Renaming or removing classes, properties, individuals or namespaces, or changing
  `number` or `version` in `docs/_ech.yml`: published data depends on these IRIs.
  Replacing the demo content while following `CLEANUP.md` is the exception.
- In a project created from this template: changing files that the template
  maintains (`PATTERNS` in `tests/test_template_sync.py`). Propose the change for
  the template repository instead.
- Adding a Python package or a tool.

## Gotchas

- A failing SHACL test names only the shape and the nodes. The reason is in
  `build/rdf/04-shacl-report.ttl`.
- The files in `build/rdf/` are large. Query them with `grep` or rdflib; never
  read them whole.
- Some checks need the network: `test_links.py` (every URL in the Markdown files),
  `test_queries.py` (runs the example queries against the production LINDAS
  endpoint), `test_template_sync.py` (GitHub) and `make docs` (downloads images
  and the Word template). If one fails on something the change did not touch,
  report it.
- Warnings from `test_naming.py` (as long as the demo data is present) and
  `test_template_sync.py` (files that differ from the template) are expected.
- The eCH colours are defined three times: `docs/assets/ech.mplstyle` (figures),
  `ech.scss` (website) and `typst-template.typ` (PDF). Change them in all three.
- The CI runs Python 3.10: do not use language features of later versions.

## Done

A change is done when:

- `make test` passes, with no warnings other than the expected ones above.
- `make docs` passes, if the change touches the shapes, the glossary or `docs/`.
- All language versions are updated.
- If only network checks fail, for reasons unrelated to the change, the change
  is done; report the failure.

## More documentation

- `README.md`: the tools and standards used, and how to publish.
- `CLEANUP.md`: setting up a new project from this template, step by step.
- `.github/CONTRIBUTING.md`: Git workflow (issue, branch, draft pull request),
  naming conventions, figure style and eCH releases.

If you learn something that the next agent would need, propose a line for this file.