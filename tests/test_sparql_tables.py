"""
The script behind the tables from SPARQL queries in the documentation
(docs/_extensions/ech/sparql/query.py): it runs a SELECT query on an RDF file
or sends it to a SPARQL endpoint, and returns the result as JSON, which the
Quarto filter sparql.lua formats.
"""
import json
import subprocess
import sys
import threading
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

SCRIPT = Path("docs/_extensions/ech/sparql/query.py")
XSD = "http://www.w3.org/2001/XMLSchema#"

DATA = """
@prefix ex: <http://example.org/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

ex:rock ex:name "Rock"@en, "Rock"@de ; ex:tracks 1297 ; ex:since "2021-01-01"^^xsd:date ; ex:parent ex:music .
ex:jazz ex:name "Jazz"@en ; ex:tracks 130 .
"""

QUERY = """
PREFIX ex: <http://example.org/>
SELECT ?genre ?name ?tracks ?since ?parent
WHERE {
  ?genre ex:name ?name ; ex:tracks ?tracks .
  FILTER(lang(?name) = "en")
  OPTIONAL { ?genre ex:since ?since }
  OPTIONAL { ?genre ex:parent ?parent }
}
ORDER BY DESC(?tracks)
"""


def run(tmp_path, query, graph_name="data.ttl"):
    graph = tmp_path / "data.ttl"
    graph.write_text(DATA, encoding="utf-8")
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--endpoint", str(tmp_path / graph_name)],
        input=query, capture_output=True, text=True)


def run_url(url, query):
    return subprocess.run([sys.executable, str(SCRIPT), "--endpoint", url], input=query, capture_output=True, text=True)


class Endpoint(BaseHTTPRequestHandler):
    """A SPARQL endpoint that answers every query with the same result and keeps the request."""

    answer = {
        "head": {"vars": ["genre", "name", "tracks", "since"]},
        "results": {"bindings": [{
            "genre": {"type": "uri", "value": "http://example.org/rock"},
            "name": {"type": "literal", "value": "Rock", "xml:lang": "en"},
            "tracks": {"type": "literal", "value": "1297", "datatype": XSD + "integer"},
        }]},
    }
    received = {}

    def do_POST(self):
        body = self.rfile.read(int(self.headers["Content-Length"])).decode("utf-8")
        Endpoint.received = {"query": urllib.parse.parse_qs(body)["query"][0], "accept": self.headers["Accept"]}
        if "ASK" in body:
            payload, status = {"head": {}, "boolean": True}, 200
        elif "broken" in body:
            payload, status = {"message": "parse error"}, 400
        else:
            payload, status = self.answer, 200
        data = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/sparql-results+json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *args):
        pass


def test_select_returns_typed_values(tmp_path):
    """Variables keep their order; IRIs get a prefixed name from the query, literals their datatype, unbound values are null."""
    result = run(tmp_path, QUERY)
    assert result.returncode == 0, result.stderr
    table = json.loads(result.stdout)
    assert table["variables"] == ["genre", "name", "tracks", "since", "parent"]
    rock, jazz = table["rows"]
    assert rock[0] == {"type": "iri", "value": "http://example.org/rock", "short": "ex:rock"}
    assert rock[1]["value"] == "Rock" and rock[1]["language"] == "en"
    assert rock[2] == {"type": "literal", "value": "1297", "datatype": XSD + "integer"}
    assert rock[3] == {"type": "literal", "value": "2021-01-01", "datatype": XSD + "date"}
    assert jazz[3] is None and jazz[4] is None


def test_other_query_forms_are_rejected(tmp_path):
    result = run(tmp_path, "ASK { ?s ?p ?o }")
    assert result.returncode != 0
    assert "SELECT" in result.stderr


def test_broken_query_and_missing_graph_fail_with_a_message(tmp_path):
    broken = run(tmp_path, "SELECT WHERE")
    assert broken.returncode != 0 and "query failed" in broken.stderr
    missing = run(tmp_path, QUERY, graph_name="missing.ttl")
    assert missing.returncode != 0 and "does not exist" in missing.stderr


def test_web_endpoint_returns_the_same_structure():
    """A URL is queried over the SPARQL protocol; the answer is brought into the structure of a file query."""
    server = HTTPServer(("127.0.0.1", 0), Endpoint)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    url = f"http://127.0.0.1:{server.server_port}/query"
    try:
        result = run_url(url, QUERY)
        assert result.returncode == 0, result.stderr
        assert Endpoint.received == {"query": QUERY, "accept": "application/sparql-results+json"}
        table = json.loads(result.stdout)
        assert table["variables"] == ["genre", "name", "tracks", "since"]
        assert table["rows"] == [[
            {"type": "iri", "value": "http://example.org/rock", "short": "ex:rock"},
            {"type": "literal", "value": "Rock", "datatype": "http://www.w3.org/1999/02/22-rdf-syntax-ns#langString", "language": "en"},
            {"type": "literal", "value": "1297", "datatype": XSD + "integer"},
            None,
        ]]

        ask = run_url(url, "ASK { ?s ?p ?o }")
        assert ask.returncode != 0 and "SELECT" in ask.stderr
        broken = run_url(url, "SELECT broken")
        assert broken.returncode != 0 and "HTTP 400" in broken.stderr
    finally:
        server.shutdown()
        server.server_close()

    unreachable = run_url(f"http://127.0.0.1:{server.server_port}/query", QUERY)
    assert unreachable.returncode != 0 and "could not be reached" in unreachable.stderr
