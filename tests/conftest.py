import pytest
from rdflib import Graph

@pytest.fixture(scope="session")
def final_graph():
    """Loads the fully reasoned and processed graph for testing."""
    g = Graph()
    # Ensure this path matches the final output of your Makefile
    g.parse("build/03_processed.ttl", format="turtle")
    return g