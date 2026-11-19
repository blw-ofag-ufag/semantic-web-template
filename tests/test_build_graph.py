"""
The build of the graph (src/python/utils/build_graph.py) and the inference
rules of src/sparql/inference/: merge, inference to a fixpoint and SPARQL
updates, checked on a few triples.
"""
import subprocess
import sys
from pathlib import Path

import pytest
from rdflib import Graph, Literal, Namespace
from rdflib.namespace import RDF

SCRIPT = Path("src/python/utils/build_graph.py")
RULES = sorted(Path("src/sparql/inference").glob("*.rq"))
EX = Namespace("http://example.org/")

PREFIXES = """
@prefix : <http://example.org/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
"""

ONTOLOGY = PREFIXES + """
:Dog rdfs:subClassOf :Mammal .
:Mammal rdfs:subClassOf :Animal .
:hasPuppy rdfs:subPropertyOf :hasChild .
:hasChild rdfs:domain :Parent ; rdfs:range :Child .
:name rdfs:range :Name .
"""

DATA = PREFIXES + """
:rex a :Dog ; :hasPuppy :bello ; :name "Rex" .
_:b :name "first file" .
"""

MORE_DATA = PREFIXES + """
_:b :name "second file" .
"""

UPDATE = """
PREFIX : <http://example.org/>
DELETE { ?s :name ?name } INSERT { ?s :label ?name } WHERE { ?s :name ?name }
"""


def build(tmp_path, updates=()):
    """Runs the build on the example files and returns the three graphs."""
    files = {}
    for name, content in {"ontology.ttl": ONTOLOGY, "data.ttl": DATA, "more.ttl": MORE_DATA, "empty.ttl": ""}.items():
        files[name] = tmp_path / name
        files[name].write_text(content, encoding="utf-8")
    update_files = []
    for i, content in enumerate(updates):
        update_files.append(tmp_path / f"{i}.rq")
        update_files[-1].write_text(content, encoding="utf-8")
    outputs = [tmp_path / "merged.ttl", tmp_path / "inferred.ttl", tmp_path / "final.ttl"]
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--input", *map(str, files.values()), "--rules", *map(str, RULES),
         "--update", *map(str, update_files), "--prefixes", str(files["ontology.ttl"]),
         "--merged", str(outputs[0]), "--inferred", str(outputs[1]), "--output", str(outputs[2])],
        capture_output=True, text=True)
    return result, outputs


def parse(path):
    graph = Graph()
    graph.parse(path, format="turtle")
    return graph


@pytest.fixture(scope="module")
def graphs(tmp_path_factory):
    result, outputs = build(tmp_path_factory.mktemp("build"), [UPDATE])
    assert result.returncode == 0, result.stderr
    return [parse(path) for path in outputs]


def test_rule_files_exist():
    assert RULES, "src/sparql/inference/ contains no rule file (*.rq)"


def test_merge_keeps_all_triples_and_blank_nodes_apart(graphs):
    """All files are merged, and equal blank node labels of different files stay different nodes."""
    merged = graphs[0]
    assert len(merged) == 11
    assert len(set(merged.subjects(EX.name, None))) == 3, "blank nodes of different files were merged"
    assert (EX.rex, RDF.type, EX.Mammal) not in merged, "the merged graph must not contain inferred triples"


def test_inference(graphs):
    """Sub-classes (transitively), sub-properties, domains and ranges are applied, also to inferred triples."""
    inferred = graphs[1]
    expected = [
        (EX.rex, RDF.type, EX.Mammal),
        (EX.rex, RDF.type, EX.Animal),
        (EX.rex, EX.hasChild, EX.bello),
        (EX.rex, RDF.type, EX.Parent),
        (EX.bello, RDF.type, EX.Child),
    ]
    missing = [triple for triple in expected if triple not in inferred]
    assert not missing, f"not inferred: {missing}"
    assert not list(inferred.triples((Literal("Rex"), None, None))), "a literal must not get a type from rdfs:range"


def test_updates_run_after_inference(graphs):
    """The SPARQL updates of the project are applied to the inferred graph."""
    final = graphs[2]
    assert (EX.rex, EX.label, Literal("Rex")) in final
    assert not list(final.triples((None, EX.name, None)))
    assert (EX.rex, RDF.type, EX.Animal) in final


def test_broken_update_fails_with_its_file_name(tmp_path):
    result, outputs = build(tmp_path, ["THIS IS NOT SPARQL"])
    assert result.returncode != 0
    assert "0.rq" in result.stderr
    assert not outputs[2].exists(), "no final graph must be written when an update fails"
