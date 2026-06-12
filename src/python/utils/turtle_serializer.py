import argparse
import glob
from pathlib import Path
from rdflib import Graph, Namespace

def main():
    parser = argparse.ArgumentParser(description="Silently merge and normalize RDF turtle files.")
    
    # Input argument accepts multiple strings to allow shell globbing or quoted wildcard patterns
    parser.add_argument(
        "input", 
        nargs="+", 
        help="Path(s) or glob pattern(s) to read (e.g., 'data/*.ttl')."
    )
    
    parser.add_argument(
        "output", 
        type=Path, 
        help="Destination path for the serialized graph."
    )

    args = parser.parse_args()

    # 1. Initialize empty graph
    g = Graph()

    # 2. Resolve input paths and load data
    # Iterating through arguments and applying glob.glob ensures cross-platform 
    # wildcard expansion, even if the user wraps the argument in quotes.
    for pattern in args.input:
        for file_path in glob.glob(pattern, recursive=True):
            g.parse(file_path, format="turtle")

    # 3. Enforce http://schema.org/ namespace binding
    # override=True and replace=True ensure any existing 'schema' prefixes 
    # (like the https variant) are completely overwritten in the graph's namespace manager.
    try:
        g.bind("schema", Namespace("http://schema.org/"), override=True, replace=True)
    except TypeError:
        # Fallback for older rdflib versions that do not support the 'replace' kwarg
        g.bind("schema", Namespace("http://schema.org/"), override=True)

    # 4. Ensure output directory hierarchy exists
    args.output.parent.mkdir(parents=True, exist_ok=True)

    # 5. Serialize standard output
    g.serialize(destination=args.output, format="turtle")

if __name__ == "__main__":
    main()