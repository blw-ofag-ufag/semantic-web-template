# Warning: Please do not adjust this script in any other place than the upstream repo template
"""
Runs a SPARQL SELECT query and prints the result as JSON. The endpoint is an
RDF file or the URL of a SPARQL endpoint on the web:

    python query.py --endpoint build/rdf/03-processed.ttl < query.rq
    python query.py --endpoint https://example.org/query < query.rq

    {"variables": ["genre", "n"],
     "rows": [[{"type": "iri", "value": "https://...", "short": "genre:1"},
               {"type": "literal", "value": "1297", "datatype": "http://www.w3.org/2001/XMLSchema#integer"}]]}

An unbound variable is null. IRIs get a prefixed name ("short") from the
PREFIX declarations of the query. The Quarto filter sparql.lua calls this
script and renders the result as a table.
"""

import argparse
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

FORMATS = {".ttl": "TURTLE", ".nt": "N_TRIPLES", ".nq": "N_QUADS", ".trig": "TRIG", ".rdf": "RDF_XML", ".jsonld": "JSON_LD"}
XSD_STRING = "http://www.w3.org/2001/XMLSchema#string"
LANG_STRING = "http://www.w3.org/1999/02/22-rdf-syntax-ns#langString"
TIMEOUT = 60  # seconds


def fail(message):
    sys.exit(f"SPARQL table: {message}")


def query_prefixes(query):
    """The PREFIX declarations of a query as (namespace, prefix) pairs, the longest namespace first."""
    found = re.findall(r"\bPREFIX\s+([^\s:<>]*):\s*<([^<>\s]*)>", query, flags=re.IGNORECASE)
    return sorted(((namespace, prefix) for prefix, namespace in found), key=lambda item: -len(item[0]))


def iri(value, prefixes):
    result = {"type": "iri", "value": value}
    for namespace, prefix in prefixes:
        local = value[len(namespace):]
        if value.startswith(namespace) and local and "/" not in local and "#" not in local:
            result["short"] = f"{prefix}:{local}"
            break
    return result


def literal(value, datatype, language):
    result = {"type": "literal", "value": value, "datatype": datatype or (LANG_STRING if language else XSD_STRING)}
    if language:
        result["language"] = language
    return result


def query_file(path, query, prefixes):
    import pyoxigraph as ox

    if not path.exists():
        fail(f"the file {path} does not exist (run `make build` first)")
    if path.suffix not in FORMATS:
        fail(f"unknown file type '{path.suffix}' of {path} (known: {', '.join(FORMATS)})")
    store = ox.Store()
    try:
        store.load(path=str(path), format=getattr(ox.RdfFormat, FORMATS[path.suffix]))
    except (SyntaxError, ValueError) as e:
        fail(f"could not read {path}: {e}")

    # Named graphs of the file are queried together with the default graph.
    try:
        solutions = store.query(query, use_default_graph_as_union=True)
    except (SyntaxError, ValueError) as e:
        fail(f"the query failed: {e}")
    if not isinstance(solutions, ox.QuerySolutions):
        fail("only SELECT queries can be rendered as a table")

    def term(value):
        if value is None:
            return None
        if isinstance(value, ox.NamedNode):
            return iri(value.value, prefixes)
        if isinstance(value, ox.BlankNode):
            return {"type": "bnode", "value": value.value}
        if isinstance(value, ox.Literal):
            return literal(value.value, value.datatype.value, value.language)
        return literal(str(value), None, None)

    variables = [variable.value for variable in solutions.variables]
    return variables, [[term(solution[name]) for name in variables] for solution in solutions]


def query_url(url, query, prefixes):
    """Sends the query to a SPARQL endpoint (SPARQL 1.1 Protocol, result as JSON)."""
    request = urllib.request.Request(
        url,
        data=urllib.parse.urlencode({"query": query}).encode("utf-8"),
        headers={
            "Accept": "application/sparql-results+json",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "quarto-sparql-table",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
            body = response.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace").strip()[:500]
        fail(f"the endpoint {url} answered with HTTP {e.code}: {detail or e.reason}")
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        fail(f"the endpoint {url} could not be reached: {getattr(e, 'reason', e)}")
    try:
        result = json.loads(body)
        variables = result["head"]["vars"]
        bindings = result["results"]["bindings"]
    except (ValueError, KeyError, TypeError):
        if isinstance(locals().get("result"), dict) and "boolean" in result:
            fail("only SELECT queries can be rendered as a table")
        fail(f"the endpoint {url} did not return a SELECT result: {body.strip()[:200]}")

    def term(binding):
        if binding is None:
            return None
        kind = binding.get("type")
        if kind == "uri":
            return iri(binding["value"], prefixes)
        if kind == "bnode":
            return {"type": "bnode", "value": binding["value"]}
        return literal(binding["value"], binding.get("datatype"), binding.get("xml:lang"))

    return variables, [[term(binding.get(name)) for name in variables] for binding in bindings]


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-e", "--endpoint", required=True, help="RDF file (.ttl, .nt, ...) or URL of a SPARQL endpoint")
    args = parser.parse_args()

    query = sys.stdin.read()
    prefixes = query_prefixes(query)
    if re.match(r"https?://", args.endpoint):
        variables, rows = query_url(args.endpoint, query, prefixes)
    else:
        variables, rows = query_file(Path(args.endpoint), query, prefixes)
    json.dump({"variables": variables, "rows": rows}, sys.stdout, ensure_ascii=False)


if __name__ == "__main__":
    main()
