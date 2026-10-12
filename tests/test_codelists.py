"""
The code lists of src/rdf/data/ (schema:CategoryCodeSet with schema:CategoryCode
values) conform to the template-wide shapes src/rdf/shapes/codelist.shacl.ttl
and are translated into every documentation language.
"""
from pathlib import Path

import pytest
from pyshacl import validate
from rdflib import Graph, URIRef
from rdflib.namespace import RDF

DATA_DIR = Path("src/rdf/data")
SHAPES = Path("src/rdf/shapes/codelist.shacl.ttl")
SCHEMA = "http://schema.org/"
CODE_SET, CODE = URIRef(SCHEMA + "CategoryCodeSet"), URIRef(SCHEMA + "CategoryCode")
NAME, DESCRIPTION = URIRef(SCHEMA + "name"), URIRef(SCHEMA + "description")


def doc_languages():
    return sorted(d.name for d in Path("docs").iterdir() if d.is_dir() and d.name in {"de", "fr", "it", "en"})


@pytest.fixture(scope="module")
def data():
    """All static data files together, since a code list and its codes may be split across files."""
    g = Graph()
    for path in sorted(DATA_DIR.glob("*.ttl")):
        g.parse(path, format="turtle")
    if (None, RDF.type, CODE_SET) not in g:
        pytest.skip(f"no schema:CategoryCodeSet in {DATA_DIR}")
    return g


def test_code_lists_conform(data):
    """Every code list and code has the structure prescribed by the template."""
    if not SHAPES.exists():
        pytest.skip(f"{SHAPES} not found")
    shapes = Graph().parse(SHAPES, format="turtle")
    conforms, _, report = validate(data, shacl_graph=shapes, inference="none", meta_shacl=False, advanced=True)
    if not conforms:
        pytest.fail(f"The code lists do not conform to {SHAPES}:\n\n{report}", pytrace=False)


def test_code_lists_are_translated(data):
    """Every code list and every code has a name and a description in every documentation language."""
    missing = []
    subjects = set(data.subjects(RDF.type, CODE_SET)) | set(data.subjects(RDF.type, CODE))
    for subject in sorted(subjects):
        for predicate in (NAME, DESCRIPTION):
            langs = {o.language for o in data.objects(subject, predicate) if getattr(o, "language", None)}
            for lang in sorted(set(doc_languages()) - langs):
                missing.append(f"{data.namespace_manager.normalizeUri(subject)} {data.namespace_manager.normalizeUri(predicate)} @{lang}")
    assert not missing, "missing translations:\n  " + "\n  ".join(missing)
