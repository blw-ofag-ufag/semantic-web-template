import pytest
import warnings
from pyshacl import validate
from rdflib import Graph, Namespace

SH = Namespace("http://www.w3.org/ns/shacl#")

def test_shacl_validation(final_graph):
    """
    Validates the data graph against SHACL shapes and translates 
    sh:severity into native pytest warnings and failures.
    """
    # Load the SHACL shapes
    shapes_graph = Graph().parse("rdf/shapes/model.shacl.ttl", format="turtle")

    # Run PySHACL programmatically
    # advanced=True is required for SHACL-SPARQL constraints
    conforms, results_graph, results_text = validate(
        data_graph=final_graph,
        shacl_graph=shapes_graph,
        meta_shacl=True,
        inference="rdfs",
        advanced=True, 
        debug=False
    )

    # If it fully conforms, the test passes immediately
    if conforms:
        assert True
        return

    # If it does not conform, parse the results graph by severity
    violations = []
    shacl_warnings = []

    # Query the generated report graph
    query = """
        PREFIX sh: <http://www.w3.org/ns/shacl#>
        SELECT ?focusNode ?severity ?message
        WHERE {
            ?report a sh:ValidationReport ;
                    sh:result ?result .
            ?result sh:focusNode ?focusNode ;
                    sh:resultSeverity ?severity .
            OPTIONAL { ?result sh:resultMessage ?message . }
        }
    """
    
    for row in results_graph.query(query):
        # Clean up the node URI for readability
        node = row.focusNode.split("#")[-1] if row.focusNode else "Unknown Node"
        severity = row.severity
        message = row.message or "No sh:message provided in shape."
        
        error_string = f"Node: ex:{node} | Message: {message}"
        
        if severity == SH.Violation:
            violations.append(error_string)
        elif severity == SH.Warning or severity == SH.Info:
            shacl_warnings.append(error_string)

    # 1. Translate sh:Warning to Pytest Warnings
    for w in shacl_warnings:
        warnings.warn(f"SHACL Warning: {w}", UserWarning)

    # 2. Translate sh:Violation to Pytest Failures
    if violations:
        formatted_violations = "\n".join(f"  - {v}" for v in violations)
        pytest.fail(
            f"SHACL Validation failed with {len(violations)} Violation(s):\n{formatted_violations}"
        )