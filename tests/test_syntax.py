import pytest
from pathlib import Path
from rdflib import Graph

# Dynamically find all .ttl files in the rdf/ directory and its subdirectories
rdf_dir = Path("rdf")
ttl_files = list(rdf_dir.rglob("*.ttl"))

@pytest.mark.parametrize("file_path", ttl_files, ids=lambda p: str(p))
def test_turtle_syntax(file_path):
    """
    Tests if a given .ttl file contains valid Turtle syntax.
    """
    g = Graph()
    try:
        # Attempt to parse the file; rdflib will throw an exception on invalid syntax
        g.parse(source=file_path, format="turtle")
    except Exception as e:
        pytest.fail(f"Syntax error in '{file_path}':\n{e}")