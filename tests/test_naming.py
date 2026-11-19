"""
Naming conventions of .github/CONTRIBUTING.md: file names, the project
namespace and the local names of classes and properties.

Violations are reported as warnings (one per convention), not as failures:
the conventions are recommendations, and renaming published resources is a
breaking change that has to be planned.
"""
import re
import subprocess
import warnings
from pathlib import Path

import pytest
from rdflib import Graph, URIRef
from rdflib.namespace import OWL, RDF, RDFS

import project_config

PREFIXES = Path("src/rdf/prefixes.ttl")
NAMESPACE_ROOT = "https://agriculture.ld.admin.ch/"

# Fixed by convention (GitHub, make) or by the tools that read them (Quarto
# recognises its template partials by name).
CONVENTIONAL_FILES = {"README.md", "LICENSE.md", "CLEANUP.md", "CONTRIBUTING.md", "AGENTS.md", "CLAUDE.md", "Makefile",
                      "typst-template.typ", "typst-show.typ", "title-metadata.html"}

SNAKE_CASE = re.compile(r"_?[a-z0-9]+(_[a-z0-9]+)*")  # Quarto config files start with "_"
PASCAL_CASE = re.compile(r"[A-Z][a-z0-9]*([A-Z][a-z0-9]*)*")
CAMEL_CASE = re.compile(r"[a-z][a-z0-9]*([A-Z][a-z0-9]*)*")
VERB_PREFIX = re.compile(r"(has|is)[A-Z]")
SUBNAMESPACE = re.compile(r"[a-z][a-z0-9_]*/")

MAX_EXAMPLES = 10


def report(title, items):
    """Emits one aggregated warning for a convention, with a few examples."""
    if not items:
        return
    items = sorted(items)
    shown = items[:MAX_EXAMPLES]
    more = f"\n  ... and {len(items) - MAX_EXAMPLES} more" if len(items) > MAX_EXAMPLES else ""
    warnings.warn(f"{title} ({len(items)}):\n  " + "\n  ".join(shown) + more, UserWarning)


def tracked_files():
    result = subprocess.run(["git", "ls-files", "-z"], capture_output=True, text=True, check=True)
    return [Path(f) for f in result.stdout.split("\0") if f]


def project_namespace():
    """The IRI of the empty prefix in src/rdf/prefixes.ttl (the project namespace)."""
    match = re.search(r"^@prefix\s+:\s*<([^>]+)>", PREFIXES.read_text(encoding="utf-8"), re.M)
    return match.group(1) if match else None


def declared_namespaces():
    """All prefix declarations of src/rdf/prefixes.ttl as {prefix: iri}."""
    return dict(re.findall(r"^@prefix\s+([^\s:]*):\s*<([^>]+)>", PREFIXES.read_text(encoding="utf-8"), re.M))


def qname_function():
    """Abbreviates IRIs with the prefixes of src/rdf/prefixes.ttl (longest namespace wins)."""
    namespaces = sorted(declared_namespaces().items(), key=lambda item: -len(item[1]))

    def qname(iri):
        for prefix, namespace in namespaces:
            if str(iri).startswith(namespace):
                return f"{prefix}:{str(iri)[len(namespace):]}"
        return f"<{iri}>"
    return qname


def test_file_names_are_snake_case():
    """All files are named in lowercase snake_case (CONTRIBUTING.md, "File naming convention")."""
    violations = []
    for path in tracked_files():
        if path.name in CONVENTIONAL_FILES or path.name.startswith("."):
            continue
        stem, *extensions = path.name.split(".")
        bad_extensions = [e for e in extensions if not (e.islower() and e.isalnum())]
        if not SNAKE_CASE.fullmatch(stem) or bad_extensions:
            violations.append(str(path))
    report("Files not named in lowercase snake_case", violations)


def test_project_namespace_follows_convention():
    """
    The project namespace is https://agriculture.ld.admin.ch/{eCH number}/{major version}/
    and its sub-namespaces add one lowercase segment (CONTRIBUTING.md, "RDF namespace naming convention").
    """
    if not PREFIXES.exists():
        pytest.skip(f"{PREFIXES} not found")
    base = project_namespace()
    ech = project_config.load().get("ech", {})
    number, version = ech.get("number"), str(ech.get("version", ""))
    violations = []
    if not base:
        violations.append("src/rdf/prefixes.ttl declares no empty prefix ':' for the project namespace")
    elif number and version:
        expected = f"{NAMESPACE_ROOT}{number}/{version.split('.')[0]}/"
        if base != expected:
            violations.append(f"project namespace is <{base}>, expected <{expected}> from project.yml")
    if base:
        for prefix, iri in declared_namespaces().items():
            if iri.startswith(base) and iri != base and not SUBNAMESPACE.fullmatch(iri[len(base):]):
                violations.append(f"sub-namespace {prefix}: <{iri}> should be <{base}segment/> with a lowercase segment")
    report("Namespaces not following the convention", violations)


CLASS_TYPES = {OWL.Class, RDFS.Class}
PROPERTY_TYPES = {RDF.Property, OWL.ObjectProperty, OWL.DatatypeProperty, OWL.AnnotationProperty}


def test_class_and_property_names_follow_convention(final_graph):
    """
    Local names of the classes and properties in the project namespace
    (CONTRIBUTING.md, "RDF resource naming convention"): classes in PascalCase,
    properties in camelCase without a leading verb. All other resources
    (individuals, code list entries, shapes, the ontology) are named freely.
    """
    base = project_namespace()
    if not base:
        pytest.skip("src/rdf/prefixes.ttl declares no project namespace")

    def own(nodes):
        return {n for n in nodes if isinstance(n, URIRef) and str(n).startswith(base) and str(n) != base}

    def name(node):
        return str(node)[len(base):].rpartition("/")[2]

    qname = qname_function()
    classes = own(s for kind in CLASS_TYPES for s in final_graph.subjects(RDF.type, kind))
    properties = own(final_graph.predicates()) | own(s for kind in PROPERTY_TYPES for s in final_graph.subjects(RDF.type, kind))
    properties -= classes

    report("Classes not in PascalCase", {qname(n) for n in classes if not PASCAL_CASE.fullmatch(name(n))})
    report("Properties not in camelCase", {qname(n) for n in properties if not CAMEL_CASE.fullmatch(name(n))})
    report("Properties starting with a verb (prefer eppoCode over hasEppoCode)",
           {qname(n) for n in properties if CAMEL_CASE.fullmatch(name(n)) and VERB_PREFIX.match(name(n))})
