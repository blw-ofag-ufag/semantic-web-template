# AGENTS.md

Template for eCH standards: an RDF data model and data, validated with SHACL,
published on LINDAS and documented as a multilingual eCH document with Quarto.

## Commands

Run all commands from the repository root.

```sh
make setup   # once: venv/, Python packages, ROBOT
make test    # build the graph, validate with SHACL, run all tests
make docs    # render the documentation into build/docs/
```

Always check with `make test`, not with `pytest` alone: pytest reads the
graph in `build/` and does not rebuild it.

## Never

- Run `make publish` or `make delete`: they replace or delete the published graph on LINDAS.
- Push to `main`: a merge publishes the graph and the website. Work on a branch.
- Read, print or commit `.env`: it holds the LINDAS credentials.
- Edit generated files (`build/`, `docs/*/{entities,namespaces,codelists,glossary}.md`).
  Change their source instead: the shapes, the graph or the glossary.
- Remove a link, a query or a test to make a failing test pass.

## Ask first

- Renaming or removing classes, properties, individuals or namespaces:
  published data and other systems depend on these IRIs.
- In a project created from this template: changing a file maintained by the
  template (see `PATTERNS` in `tests/test_template_sync.py`). Such changes
  belong in the template repository.
- Adding a Python package or a tool.

## Gotchas

- A failing SHACL test names only the shape and the nodes. The reason is in
  `build/rdf/04-shacl-report.ttl`.
- The shapes are closed (`sh:closed true`): a new property in the data needs a
  property shape in `src/rdf/shapes/model.shacl.ttl`, with names and messages
  in every documentation language.
- The files in `build/rdf/` have about 100 000 lines. Query them with `grep` or
  rdflib; never read them whole.
- `test_links.py`, `test_queries.py` and `test_template_sync.py` need the
  network, `test_queries.py` runs against the production endpoint of LINDAS.
  If they fail on something the change did not touch, report it.
- Warnings from `test_naming.py` and `test_template_sync.py` are reports, not failures.
- Pipeline scripts in `src/python/pipeline/` share one `--output` file: only the
  first may overwrite it, every further script appends.
- `src/sparql/processing/` takes only SPARQL Update (INSERT/DELETE); a SELECT aborts the build.

## Conventions

- Change `docs/de`, `docs/fr` and `docs/en` together, on the same lines: the
  tests compare line counts, headings, code blocks, images and table rows.
- German text in Swiss orthography (no ß).
- Python only, no R. Keep code compatible with Python 3.10, which the CI uses.

## Done

`make test` passes. If shapes, glossary or `docs/` changed, `make docs` passes too.
