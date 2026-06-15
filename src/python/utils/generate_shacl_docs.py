import argparse
import re
from rdflib import Graph, Namespace

def format_uri(g, uri):
    if not uri:
        return ""
    try:
        return g.namespace_manager.normalizeUri(uri)
    except Exception:
        return str(uri)

def slugify(text):
    """Creates a URL-friendly slug from a string."""
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')

def sanitize_cell(text):
    """Removes newlines and escapes pipe characters to prevent markdown table breaks."""
    return str(text).replace("\n", " ").replace("\r", "").replace("|", "&#124;").strip()

def main():
    parser = argparse.ArgumentParser(description="Generate Markdown documentation from a SHACL model.")
    parser.add_argument("-i", "--input", required=True, help="Input SHACL file (.ttl)")
    parser.add_argument("-o", "--output", required=True, help="Output Markdown file (.md)")
    parser.add_argument("-p", "--prefixes", required=False, help="Prefix file (.ttl) to override QNames")
    args = parser.parse_args()

    # Initialize graph without default namespaces to ensure strict QName mapping
    g = Graph(bind_namespaces="none")
    g.parse(args.input, format="turtle")

    # Load custom prefixes if provided
    if args.prefixes:
        prefix_g = Graph(bind_namespaces="none")
        prefix_g.parse(args.prefixes, format="turtle")
        for prefix, uri in prefix_g.namespaces():
            try:
                g.bind(str(prefix), Namespace(str(uri)), override=True, replace=True)
            except TypeError:
                g.bind(str(prefix), Namespace(str(uri)), override=True)

    md_lines = []

    # 1. Query the class definitions in order
    q_classes = """
        PREFIX sh: <http://www.w3.org/ns/shacl#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        
        SELECT ?shape ?label ?comment ?targetClass
        WHERE {
            ?shape a sh:NodeShape .
            OPTIONAL { ?shape rdfs:label ?label . }
            OPTIONAL { ?shape rdfs:comment ?comment . }
            OPTIONAL { ?shape sh:targetClass ?targetClass . }
        } ORDER BY ?label
    """
    
    shapes_data = []
    uri_to_slug = {}
    
    # Pre-process shapes to build the cross-reference index (for hyperlinking types)
    for row in g.query(q_classes):
        shape_uri = row.shape
        label = str(row.label) if row.label else format_uri(g, shape_uri)
        comment = str(row.comment) if row.comment else ""
        target_class = row.targetClass
        
        slug = slugify(label)
        uri_to_slug[shape_uri] = slug
        
        # If the shape targets a class, map that class URI to this shape's slug as well
        if target_class:
            uri_to_slug[target_class] = slug
            
        shapes_data.append({
            'uri': shape_uri,
            'label': label,
            'comment': comment,
            'target_class': target_class,
            'slug': slug
        })

    # 2. Iterate and build markdown
    for s_data in shapes_data:
        shape = s_data['uri']
        label = s_data['label']
        comment = s_data['comment']
        target_class = s_data['target_class']
        slug = s_data['slug']

        # Add section header with Quarto anchor
        md_lines.append(f"## {label} {{#sec-{slug}}}")
        md_lines.append("")
        
        # Add shape rdfs:comment right below the header
        if comment:
            md_lines.append(f"{comment}")
            md_lines.append("")
            
        if target_class:
            target_qname = format_uri(g, target_class)
            md_lines.append(f"**Target Class:** `{target_qname}`")
            md_lines.append("")

        # 3. Query the properties for each shape
        q_props = """
            PREFIX sh: <http://www.w3.org/ns/shacl#>
            
            SELECT ?prop ?name ?path ?datatype ?class ?minCount ?maxCount ?message ?description ?nodeKind ?order
            WHERE {
                ?shape sh:property ?prop .
                OPTIONAL { ?prop sh:name ?name . }
                OPTIONAL { ?prop sh:path ?path . }
                OPTIONAL { ?prop sh:datatype ?datatype . }
                OPTIONAL { ?prop sh:class ?class . }
                OPTIONAL { ?prop sh:minCount ?minCount . }
                OPTIONAL { ?prop sh:maxCount ?maxCount . }
                OPTIONAL { ?prop sh:message ?message . }
                OPTIONAL { ?prop sh:description ?description . }
                OPTIONAL { ?prop sh:nodeKind ?nodeKind . }
                OPTIONAL { ?prop sh:order ?order . }
            } ORDER BY ?order ?name ?path
        """

        props = list(g.query(q_props, initBindings={'shape': shape}))
        if props:
            md_lines.append("| Name | Path | Type | Cardinality |")
            md_lines.append("|:--|:--|:--|--:|")
            
            for p in props:
                # Format Name and Description cell
                sh_name = sanitize_cell(p["name"]) if p["name"] else ""
                raw_desc = p["description"] if p["description"] else p["message"]
                sh_desc = sanitize_cell(raw_desc) if raw_desc else ""

                if sh_name and sh_desc:
                    display_name = f"**{sh_name}**: {sh_desc}"
                elif sh_desc:
                    display_name = sh_desc
                elif sh_name:
                    display_name = f"**{sh_name}**"
                else:
                    display_name = ""

                p_path = f"`{format_uri(g, p['path'])}`" if p["path"] else ""
                
                # Resolve property types and hyperlink them if applicable
                types = []
                for t_uri in [p["datatype"], p["class"], p["nodeKind"]]:
                    if t_uri:
                        t_qname = format_uri(g, t_uri)
                        if t_uri in uri_to_slug:
                            types.append(f"[{t_qname}](#sec-{uri_to_slug[t_uri]})")
                        else:
                            types.append(f"`{t_qname}`")
                
                # Resolve nested 'sh:or' statements
                if not types and p["prop"]:
                    q_or = """
                        PREFIX sh: <http://www.w3.org/ns/shacl#>
                        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                        SELECT ?cls WHERE {
                            ?prop sh:or/rdf:rest*/rdf:first/sh:class ?cls .
                        }
                    """
                    for oc in g.query(q_or, initBindings={'prop': p['prop']}):
                        t_uri = oc.cls
                        t_qname = format_uri(g, t_uri)
                        if t_uri in uri_to_slug:
                            types.append(f"[{t_qname}](#sec-{uri_to_slug[t_uri]})")
                        else:
                            types.append(f"`{t_qname}`")

                p_type_str = " or ".join(types)

                min_c = str(p["minCount"]) if p["minCount"] else "0"
                max_c = str(p["maxCount"]) if p["maxCount"] else "*"
                cardinality = f"{min_c}..{max_c}"

                md_lines.append(f"| {display_name} | {p_path} | {p_type_str} | {cardinality} |")
            
            # Quarto Table Caption with label and unique ID
            md_lines.append(f": {label} properties {{#tbl-{slug}}}")
            md_lines.append("")

    with open(args.output, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))

if __name__ == "__main__":
    main()