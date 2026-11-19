# Warning: Please do not adjust this script in any other place than the upstream repo template
"""
Builds the graph from its sources in three steps:

1. merge:  all input files are loaded into one graph,
2. infer:  the rules (SPARQL updates) are applied until nothing new is derived,
3. update: the SPARQL updates of the project are applied once, in the given order.

    python build_graph.py --input src/rdf/ontology/model.owl.ttl build/rdf/00-integrated.ttl \\
        --rules src/sparql/inference/*.rq --update src/sparql/processing/*.rq \\
        --prefixes src/rdf/prefixes.ttl \\
        --merged build/rdf/01-merged.ttl --inferred build/rdf/02-inferred.ttl \\
        --output build/rdf/03-processed.ttl

The result of each step is written to its own file, so that it can be
inspected. The files are plain Turtle, one statement per line; the final graph
is formatted for readers by graph_metadata.py.
"""

import argparse
import sys
from pathlib import Path

import pyoxigraph as ox

# The rules are applied in rounds until the graph stops growing. A rule set
# that still derives triples after this many rounds creates new resources in
# every round and would never end.
MAX_ROUNDS = 50


def fail(message):
    sys.exit(f"ERROR: {message}")


def read_prefixes(path):
    """The prefixes declared in a Turtle file as {prefix: namespace}."""
    reader = ox.parse(path=str(path), format=ox.RdfFormat.TURTLE)
    for _ in reader:
        pass
    return dict(reader.prefixes)


def load(store, paths):
    """Loads the files into the store. Blank nodes are renamed, so that equal
    labels in different files do not denote the same node."""
    for path in paths:
        if path.stat().st_size == 0:
            continue
        try:
            store.extend(ox.parse(path=str(path), rename_blank_nodes=True))
        except (SyntaxError, ValueError) as e:
            fail(f"could not read {path}: {e}")


def update(store, path):
    try:
        store.update(path.read_text(encoding="utf-8"))
    except (SyntaxError, ValueError, OSError) as e:
        fail(f"SPARQL update {path} failed: {e}")


def infer(store, rules):
    """Applies the rule files round by round until no new triple is derived."""
    for _ in range(MAX_ROUNDS):
        before = len(store)
        for path in rules:
            update(store, path)
        if len(store) == before:
            return
    fail(f"the rules still derive new triples after {MAX_ROUNDS} rounds: {', '.join(map(str, rules))}")


def write(store, path, prefixes):
    if path is None:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    store.dump(str(path), format=ox.RdfFormat.TURTLE, from_graph=ox.DefaultGraph(), prefixes=prefixes)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-i", "--input", type=Path, nargs="+", required=True, help="RDF files to merge")
    parser.add_argument("--rules", type=Path, nargs="*", default=[], help="SPARQL updates applied until nothing new is derived")
    parser.add_argument("--update", type=Path, nargs="*", default=[], help="SPARQL updates applied once, in this order")
    parser.add_argument("-p", "--prefixes", type=Path, help="Prefix file (.ttl) for the written files")
    parser.add_argument("--merged", type=Path, help="Where to write the merged graph")
    parser.add_argument("--inferred", type=Path, help="Where to write the graph after inference")
    parser.add_argument("-o", "--output", type=Path, required=True, help="Where to write the final graph")
    args = parser.parse_args()

    prefixes = read_prefixes(args.prefixes) if args.prefixes else {}
    store = ox.Store()

    load(store, args.input)
    merged = len(store)
    write(store, args.merged, prefixes)

    infer(store, args.rules)
    inferred = len(store)
    write(store, args.inferred, prefixes)

    for path in args.update:
        update(store, path)
    write(store, args.output, prefixes)

    print(f"Merged {merged} triples, inferred {inferred - merged}, {len(store)} after the SPARQL updates.")


if __name__ == "__main__":
    main()
