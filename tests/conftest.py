from pathlib import Path
import pytest
from rdflib import Graph

# Tests that produce human-readable reports write them to this directory.
TEST_LOG_DIR = Path("build/test")

# Tests that use one of these fixtures need the graph built by `make build`.
GRAPH_FIXTURES = {"final_graph", "shacl_report"}


def pytest_configure(config):
    config.addinivalue_line("markers", "network: the test needs network access (links, LINDAS, GitHub)")
    config.addinivalue_line("markers", "graph: the test needs the built graph in build/rdf (set automatically)")


def pytest_collection_modifyitems(items):
    """Marks every test that depends on the built graph, so that `make check`
    can leave these tests out (-m "not network and not graph")."""
    for item in items:
        if GRAPH_FIXTURES & set(getattr(item, "fixturenames", ())):
            item.add_marker(pytest.mark.graph)


def pytest_addoption(parser):
    parser.addoption(
        "--template-ref",
        action="store",
        default="latest",
        help="Tag (e.g., 'v1.2.3') or 'latest' of the template repository to check against."
    )

@pytest.fixture(scope="session", autouse=True)
def clear_test_logs():
    """Removes the reports of the previous test run, so that every report in
    build/test belongs to the current run (GitHub issue #40)."""
    if TEST_LOG_DIR.is_dir():
        for log in TEST_LOG_DIR.glob("*.log"):
            log.unlink()


@pytest.fixture(scope="session")
def final_graph():
    """Loads the fully reasoned and processed graph for testing."""
    g = Graph()
    g.parse("build/rdf/03-processed.ttl", format="turtle")
    return g