import pytest
import warnings
from rdflib import Graph, Namespace, URIRef

SH = Namespace("http://www.w3.org/ns/shacl#")

def get_shacl_rules():
    """
    Parses the SHACL definition file during Pytest collection
    to generate one distinct test per Shape or Constraint.
    """
    g = Graph()
    try:
        g.parse("rdf/shapes/model.shacl.ttl", format="turtle")
    except Exception:
        return []
        
    query = """
        PREFIX sh: <http://www.w3.org/ns/shacl#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        
        SELECT DISTINCT ?shape ?type ?name ?message ?path
        WHERE {
            {
                ?shape a sh:NodeShape .
                BIND("NodeShape" AS ?type)
            }
            UNION
            {
                [] sh:property ?shape .
                BIND("Property" AS ?type)
            }
            UNION
            {
                [] sh:sparql ?shape .
                BIND("SPARQL" AS ?type)
            }
            OPTIONAL { ?shape sh:name|rdfs:label|rdfs:comment ?name . }
            OPTIONAL { ?shape sh:message ?message . }
            OPTIONAL { ?shape sh:path ?path . }
        }
    """
    rules = []
    for row in g.query(query):
        # Create a user-friendly test name for the terminal
        if row.message:
            test_name = str(row.message)
        elif row.name:
            test_name = str(row.name)
        elif row.path:
            test_name = f"Property {str(row.path).split('/')[-1].split('#')[-1]}"
        else:
            test_name = f"Unnamed {row.type}"
            
        rules.append({
            "test_name": test_name,
            "type": str(row.type),
            "message": str(row.message) if row.message else None,
            "path": str(row.path) if row.path else None,
            "shape_uri": str(row.shape) if isinstance(row.shape, URIRef) else None
        })
        
    # Deduplicate rules by their test name
    unique_rules = {r["test_name"]: r for r in rules}
    return list(unique_rules.values())

# Extract the rules so Pytest can parameterize them
RULES = get_shacl_rules()

@pytest.fixture(scope="session")
def shacl_report():
    """Loads the pre-generated SHACL validation report exactly once."""
    g = Graph()
    try:
        g.parse("build/rdf/04-shacl-report.ttl", format="turtle")
    except Exception as e:
        pytest.fail(f"Could not load SHACL report. Did PySHACL run? Error: {e}")
    return g

@pytest.mark.parametrize("rule", RULES, ids=lambda r: f"{r['type']} | {r['test_name']}")
def test_shacl_rule(rule, shacl_report):
    """Evaluates an individual SHACL constraint against the validation report."""
    
    # We must match Rules to Report results. Since Blank Nodes do not map 
    # reliably across different RDF graphs, we match by Message, Path, or URI.
    if rule["message"]:
        msg_literal = rule["message"].replace('"', '\\"')
        filter_str = f'?actualMessage = "{msg_literal}"'
    elif rule["path"]:
        filter_str = f'?path = <{rule["path"]}>'
    elif rule["shape_uri"]:
        filter_str = f'?sourceShape = <{rule["shape_uri"]}>'
    else:
        pytest.skip("Rule has no URI, message, or path to map to report results.")
        
    query = f"""
        PREFIX sh: <http://www.w3.org/ns/shacl#>
        SELECT ?focusNode ?severity ?actualMessage
        WHERE {{
            ?report a sh:ValidationReport ;
                    sh:result ?result .
            ?result sh:focusNode ?focusNode ;
                    sh:resultSeverity ?severity .
            OPTIONAL {{ ?result sh:resultMessage ?actualMessage . }}
            OPTIONAL {{ ?result sh:resultPath ?path . }}
            OPTIONAL {{ ?result sh:sourceShape ?sourceShape . }}
            
            # Inject the specific match condition for this rule
            FILTER( {filter_str} )
        }}
    """
    
    warnings_list = []
    errors_list = []
    infos_list = []
    
    for row in shacl_report.query(query):
        node = str(row.focusNode).split("#")[-1].split("/")[-1] if row.focusNode else "Unknown Node"
        if row.severity == SH.Violation:
            errors_list.append(node)
        elif row.severity == SH.Warning:
            warnings_list.append(node)
        elif row.severity == SH.Info:
            infos_list.append(node)
            
    def format_nodes(nodes, limit=5):
        displayed = ", ".join(f"ex:{n}" for n in nodes[:limit])
        if len(nodes) > limit:
            displayed += f", and {len(nodes) - limit} more"
        return displayed

    # Emit native Pytest warnings for non-violating severities
    if infos_list:
        warnings.warn(f"SHACL INFO for '{rule['test_name']}': {format_nodes(infos_list)}", UserWarning)
        
    if warnings_list:
        warnings.warn(f"SHACL WARNING for '{rule['test_name']}': {format_nodes(warnings_list)}", UserWarning)
        
    # Trigger native Pytest failure for Violations
    if errors_list:
        pytest.fail(
            f"SHACL Violation '{rule['test_name']}' failed on {len(errors_list)} node(s):\n" +
            f"Nodes: {format_nodes(errors_list)}",
            pytrace=False
        )