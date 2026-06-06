import pytest
import warnings
from collections import defaultdict
from rdflib import Graph, Namespace

SH = Namespace("http://www.w3.org/ns/shacl#")

@pytest.fixture(scope="session")
def shacl_report():
    """Pytest fixture to load the pre-generated SHACL report exactly once."""
    g = Graph()
    try:
        g.parse("build/04-shacl-report.ttl", format="turtle")
    except Exception as e:
        pytest.fail(f"Could not load SHACL report. Did PySHACL run? Error: {e}")
    return g

def test_shacl_conformance(shacl_report):
    """Evaluates SHACL report natively using pytest warnings and assertions."""
    query = """
        PREFIX sh: <http://www.w3.org/ns/shacl#>
        SELECT ?focusNode ?severity ?message ?sourceShape
        WHERE {
            ?report a sh:ValidationReport ;
                    sh:result ?result .
            ?result sh:focusNode ?focusNode ;
                    sh:resultSeverity ?severity .
            OPTIONAL { ?result sh:resultMessage ?message . }
            OPTIONAL { ?result sh:sourceShape ?sourceShape . }
        }
    """
    
    infos = defaultdict(list)
    warnings_dict = defaultdict(list)
    errors = defaultdict(list)

    for row in shacl_report.query(query):
        node = row.focusNode.split("#")[-1] if row.focusNode else "Unknown Node"
        shape = row.sourceShape.split("#")[-1] if row.sourceShape else "Unknown Shape"
        message = row.message or "No message provided."
        
        category = f"[{shape}] {message}"
        
        if row.severity == SH.Violation:
            errors[category].append(node)
        elif row.severity == SH.Warning:
            warnings_dict[category].append(node)
        elif row.severity == SH.Info:
            infos[category].append(node)

    def format_summary(category, nodes, limit=3):
        """Helper to truncate the list of nodes for Pytest output."""
        displayed = ", ".join(f"ex:{n}" for n in nodes[:limit])
        if len(nodes) > limit:
            displayed += f", and {len(nodes) - limit} more"
        return f"{category} -> Nodes: {displayed}"

    # 1. Feed sh:Info and sh:Warning into Pytest's native warnings summary
    for cat, nodes in infos.items():
        warnings.warn(f"SHACL INFO: {format_summary(cat, nodes)}", UserWarning)
        
    for cat, nodes in warnings_dict.items():
        warnings.warn(f"SHACL WARNING: {format_summary(cat, nodes)}", UserWarning)

    # 2. Trigger a native Pytest failure for sh:Violations
    if errors:
        error_details = [format_summary(cat, nodes) for cat, nodes in errors.items()]
        total_errors = sum(len(v) for v in errors.values())
        pytest.fail(
            f"SHACL Validation failed with {total_errors} violation(s):\n" + 
            "\n".join(f"  - {err}" for err in error_details),
            pytrace=False
        )