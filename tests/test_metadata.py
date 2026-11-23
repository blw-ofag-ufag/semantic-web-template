"""
The description of the named graph as a dataset, which `make build` generates
from project.yml (src/python/utils/project_config.py, build/rdf/metadata.ttl).
"""
import pytest
from rdflib import URIRef
from rdflib.namespace import DCTERMS, RDF

import project_config

SCHEMA_NAME = URIRef("http://schema.org/name")
SCHEMA_DESCRIPTION = URIRef("http://schema.org/description")
SCHEMA_DATASET = URIRef("http://schema.org/Dataset")
SCHEMA_STATUS = URIRef("http://schema.org/creativeWorkStatus")
DCAT_LANDING_PAGE = URIRef("http://www.w3.org/ns/dcat#landingPage")


@pytest.fixture(scope="module")
def config():
    if not project_config.CONFIG.exists():
        pytest.skip(f"{project_config.CONFIG} not found")
    return project_config.load()


@pytest.fixture(scope="module")
def metadata(config):
    return project_config.dataset_graph(config)


@pytest.fixture(scope="module")
def dataset(config):
    return URIRef(config["lindas"]["graph"])


def test_metadata_describes_the_configured_graph(metadata, dataset):
    """The dataset is the named graph of project.yml (lindas.graph), and nothing else is described."""
    subjects = {s for s in metadata.subjects(RDF.type, SCHEMA_DATASET)}
    assert subjects == {dataset}, f"the metadata must describe exactly <{dataset}>, found {sorted(map(str, subjects))}"


def test_metadata_is_translated(metadata, dataset, config):
    """Title and description of the dataset exist in every documentation language."""
    for predicate in (SCHEMA_NAME, SCHEMA_DESCRIPTION):
        langs = {o.language for o in metadata.objects(dataset, predicate) if getattr(o, "language", None)}
        missing = set(project_config.languages(config)) - langs
        assert not missing, f"{predicate} of the dataset lacks the languages {sorted(missing)}"


def test_metadata_follows_the_configuration(metadata, dataset, config):
    """Status, languages and landing page are derived from the other sections of project.yml."""
    status = metadata.value(dataset, SCHEMA_STATUS)
    expected = "Draft" if project_config.is_unpublished(config) else "Published"
    assert str(status).endswith(f"/{expected}"), f"status '{config['ech']['status']}' must give {expected}, got <{status}>"
    languages = {str(o) for o in metadata.objects(dataset, DCTERMS.language)}
    assert languages == set(project_config.languages(config))
    assert metadata.value(dataset, DCAT_LANDING_PAGE) == URIRef(project_config.homepage(config))


def test_metadata_has_no_modification_date(metadata, dataset):
    """The modification date is set at the end of `make build`, not generated from the configuration."""
    for predicate in (DCTERMS.modified, URIRef("http://schema.org/dateModified")):
        assert (dataset, predicate, None) not in metadata, f"the generated metadata must not contain {predicate}"
