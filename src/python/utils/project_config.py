# Warning: Please do not adjust this script in any other place than the upstream repo template
"""
Reads the project configuration (project.yml) and derives from it what other
tools need, so that nothing has to be stated twice.

    python project_config.py get lindas.graph          # print one value
    python project_config.py quarto -o docs/_project.yml
    python project_config.py metadata -o build/rdf/metadata.ttl -p src/rdf/prefixes.ttl

`quarto` writes the metadata file that docs/_quarto.yml includes: the pages
to render (one folder per language), the eCH metadata of the title page, the
website title, the navigation bar and the announcement banner. `metadata` writes the description of the named graph as
a dataset. The tests and the documentation generators import this module.
"""

import argparse
import sys
from pathlib import Path

import yaml
from rdflib import BNode, Graph, Literal, Namespace, URIRef
from rdflib.namespace import DCAT, DCTERMS, RDF, VOID, XSD, NamespaceManager

ROOT = Path(__file__).resolve().parents[3]
CONFIG = ROOT / "project.yml"
VOCABULARY = ROOT / "docs" / "assets" / "ech_vocabulary.yml"

# Documents whose status precedes "approved" are not published yet.
UNPUBLISHED_STATUSES = {"in-progress", "draft", "proposal"}

# Names of the languages in the language menu of the website.
LANGUAGE_NAMES = {"de": "Deutsch", "fr": "Français", "it": "Italiano", "en": "English"}

SCHEMA = Namespace("http://schema.org/")
VCARD = Namespace("http://www.w3.org/2006/vcard/ns#")
ORG = Namespace("https://register.ld.admin.ch/opendataswiss/org/")
THEME = Namespace("https://register.ld.admin.ch/opendataswiss/category/")
STATUS = Namespace("https://ld.admin.ch/vocabulary/CreativeWorkStatus/")
TERMS_OF_USE = Namespace("https://ld.admin.ch/vocabulary/TermsOfUse/")
FREQUENCY = Namespace("https://publications.europa.eu/resource/authority/frequency/")


def load(path=CONFIG):
    """The project configuration as a dictionary."""
    with open(path, encoding="utf-8") as f:
        config = yaml.safe_load(f)
    if not isinstance(config, dict):
        sys.exit(f"{path} must be a YAML mapping")
    return config


def lookup(config, key):
    """The value at a dotted key such as 'lindas.graph'; a missing key is an error."""
    value = config
    for part in key.split("."):
        if not isinstance(value, dict) or part not in value:
            sys.exit(f"project.yml has no entry '{key}'")
        value = value[part]
    return value


def languages(config):
    """The languages of the documentation, the original first."""
    entry = config["ech"]["languages"]
    return [entry["original"], *(entry.get("translations") or [])]


def is_unpublished(config):
    return config["ech"]["status"] in UNPUBLISHED_STATUSES


def repository_url(config):
    return f"https://github.com/{config['project']['repository']}"


def homepage(config):
    """The landing page of the project: project.homepage, or its GitHub Pages site."""
    project = config["project"]
    if project.get("homepage"):
        return project["homepage"]
    owner, name = project["repository"].split("/")
    return f"https://{owner}.github.io/{name}/"


# ------------------------------------------------------------------------------
# Quarto metadata
# ------------------------------------------------------------------------------

def quarto_metadata(config, vocabulary):
    """The metadata that docs/_quarto.yml includes with `metadata-files`."""
    ech = config["ech"]
    voc = vocabulary[ech["languages"]["original"]]
    repository = repository_url(config)

    navigation = [
        {"icon": "github", "href": repository, "aria-label": "GitHub"},
        {"icon": "bug", "href": f"{repository}/issues/new", "aria-label": "Issue"},
        {"icon": "envelope", "href": f"mailto:{config['project']['contact']['email']}", "aria-label": "Contact"},
    ]
    if len(languages(config)) > 1:
        navigation.append({
            "icon": "translate",
            "menu": [{"text": LANGUAGE_NAMES.get(lang, lang), "href": f"/{lang}/index.html"} for lang in languages(config)],
        })

    website = {
        "title": f"{ech['number']} Version {ech['version']} ({voc['status'][ech['status']]})",
        "repo-url": repository,
        "navbar": {"right": navigation},
    }
    if is_unpublished(config):
        website["announcement"] = {
            "icon": "info-circle",
            "dismissable": True,
            "content": voc["announcement"],
            "type": "warning",
        }

    return {
        "project": {"render": [f"{lang}/**/*.qmd" for lang in languages(config)]},
        "date": config["date"],
        "date-format": "iso",
        "ech": ech,
        "website": website,
    }


# ------------------------------------------------------------------------------
# Dataset description of the named graph
# ------------------------------------------------------------------------------

def dataset_graph(config):
    """The description of the named graph as void:, dcat: and schema:Dataset."""
    dataset_config = config["dataset"]
    contact = config["project"]["contact"]
    g = Graph(bind_namespaces="none")
    dataset = URIRef(config["lindas"]["graph"])

    for kind in (VOID.Dataset, DCAT.Dataset, SCHEMA.Dataset):
        g.add((dataset, RDF.type, kind))
    for lang, text in dataset_config["title"].items():
        g.add((dataset, SCHEMA.name, Literal(text, lang=lang)))
    for lang, text in dataset_config["description"].items():
        g.add((dataset, SCHEMA.description, Literal(text, lang=lang)))
    for lang, keywords in (dataset_config.get("keywords") or {}).items():
        for keyword in keywords:
            g.add((dataset, DCAT.keyword, Literal(keyword, lang=lang)))

    issued = Literal(config["date"].isoformat(), datatype=XSD.date)
    created = Literal(dataset_config.get("created", config["date"]).isoformat(), datatype=XSD.date)
    g.add((dataset, SCHEMA.dateCreated, created))
    g.add((dataset, DCTERMS.issued, issued))
    g.add((dataset, SCHEMA.datePublished, issued))
    g.add((dataset, SCHEMA.creativeWorkStatus, STATUS.Draft if is_unpublished(config) else STATUS.Published))

    publisher = ORG[dataset_config["publisher"]]
    g.add((dataset, SCHEMA.creator, publisher))
    g.add((dataset, SCHEMA.publisher, publisher))
    contact_point = BNode()
    g.add((dataset, DCAT.contactPoint, contact_point))
    g.add((contact_point, RDF.type, VCARD.Organization))
    g.add((contact_point, VCARD.fn, Literal(contact["name"])))
    g.add((contact_point, VCARD.hasEmail, URIRef(f"mailto:{contact['email']}")))

    terms = TERMS_OF_USE[dataset_config["terms-of-use"]]
    g.add((dataset, DCTERMS.rights, terms))
    g.add((dataset, DCTERMS.license, terms))
    g.add((dataset, DCAT.landingPage, URIRef(homepage(config))))
    for theme in dataset_config.get("themes") or []:
        g.add((dataset, DCAT.theme, THEME[theme]))
    for lang in languages(config):
        g.add((dataset, DCTERMS.language, Literal(lang)))
    g.add((dataset, DCTERMS.accrualPeriodicity, FREQUENCY[dataset_config["frequency"]]))
    return g


def bind_prefixes(graph, prefix_file):
    """Gives the graph exactly the prefixes of a Turtle file, dropping all others."""
    graph.namespace_manager = NamespaceManager(Graph(bind_namespaces="none"), bind_namespaces="none")
    prefixes = Graph(bind_namespaces="none")
    prefixes.parse(prefix_file, format="turtle")
    for prefix, namespace in prefixes.namespaces():
        graph.bind(str(prefix), Namespace(str(namespace)), override=True, replace=True)


# ------------------------------------------------------------------------------
# Command line
# ------------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--config", type=Path, default=CONFIG, help="Project configuration (default: project.yml)")
    commands = parser.add_subparsers(dest="command", required=True)

    get = commands.add_parser("get", help="Print one value, e.g. lindas.graph")
    get.add_argument("key")

    quarto = commands.add_parser("quarto", help="Write the metadata file for Quarto")
    quarto.add_argument("-o", "--output", type=Path, required=True)
    quarto.add_argument("--vocabulary", type=Path, default=VOCABULARY)

    metadata = commands.add_parser("metadata", help="Write the dataset description of the named graph")
    metadata.add_argument("-o", "--output", type=Path, required=True)
    metadata.add_argument("-p", "--prefixes", type=Path, help="Prefix file (.ttl) for the serialisation")

    args = parser.parse_args()
    config = load(args.config)

    if args.command == "get":
        print(lookup(config, args.key))
        return

    args.output.parent.mkdir(parents=True, exist_ok=True)
    if args.command == "quarto":
        with open(args.vocabulary, encoding="utf-8") as f:
            vocabulary = yaml.safe_load(f)
        header = "# Generated from project.yml by src/python/utils/project_config.py. Do not edit.\n"
        body = yaml.safe_dump(quarto_metadata(config, vocabulary), allow_unicode=True, sort_keys=False)
        args.output.write_text(header + body, encoding="utf-8")
    elif args.command == "metadata":
        graph = dataset_graph(config)
        if args.prefixes:
            bind_prefixes(graph, args.prefixes)
        graph.serialize(destination=args.output, format="turtle")


if __name__ == "__main__":
    main()
