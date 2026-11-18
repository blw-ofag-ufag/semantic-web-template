"""
Validity of project.yml, the configuration of the project: the eCH metadata
(against the codes of docs/assets/ech_vocabulary.yml), the repository, the
LINDAS endpoints and the description of the dataset.
"""
import datetime
import re
from pathlib import Path

import pytest
import yaml

import project_config

VOCABULARY = Path("docs/assets/ech_vocabulary.yml")
DOCS_DIR = Path("docs")

SECTIONS = {"date", "ech", "project", "lindas", "dataset"}
REQUIRED_KEYS = {"number", "category", "maturity", "version", "status", "languages", "group"}
OPTIONAL_KEYS = {"decision-date", "replaces", "prerequisites", "attachments", "publisher"}
CODE_GROUPS = {"category": "category", "maturity": "maturity", "status": "status"}
STATUSES_WITH_DECISION = {"approved", "replaced"}
LINDAS_KEYS = {"graph", "graph-store", "sparql", "yasgui"}
DATASET_REQUIRED = {"title", "description", "publisher", "terms-of-use", "frequency"}
DATASET_OPTIONAL = {"keywords", "created", "themes"}

ECH_NUMBER = re.compile(r"eCH-\d{4}")
SEMVER = re.compile(r"\d+\.\d+\.\d+")
URL = re.compile(r"https://\S+")
REPOSITORY = re.compile(r"[\w.-]+/[\w.-]+")
EMAIL = re.compile(r"[^@\s]+@[^@\s]+\.[^@\s]+")


@pytest.fixture(scope="module")
def config():
    if not project_config.CONFIG.exists():
        pytest.skip(f"{project_config.CONFIG} not found")
    return project_config.load()


@pytest.fixture(scope="module")
def ech(config):
    assert isinstance(config.get("ech"), dict), "project.yml needs an 'ech' mapping"
    return config["ech"]


@pytest.fixture(scope="module")
def vocabulary():
    if not VOCABULARY.exists():
        pytest.skip(f"{VOCABULARY} not found")
    return yaml.safe_load(VOCABULARY.read_text(encoding="utf-8"))


def codes(vocabulary, group):
    """The codes of a vocabulary group, taken from the first language."""
    first = next(iter(vocabulary.values()))
    return set(first[group])


def language_folders(vocabulary):
    """The folders in docs/ that are named like a language code."""
    return {d.name for d in DOCS_DIR.iterdir() if d.is_dir() and d.name in codes(vocabulary, "language")}


def test_vocabulary_is_consistent_across_languages(vocabulary):
    """Every language of the vocabulary defines the same keys and codes."""
    languages = list(vocabulary)
    reference = vocabulary[languages[0]]
    for lang in languages[1:]:
        assert set(vocabulary[lang]) == set(reference), f"vocabulary keys of '{lang}' differ from '{languages[0]}'"
        for group in ("labels", "category", "maturity", "status", "status-description", "change", "language"):
            assert set(vocabulary[lang][group]) == set(reference[group]), (
                f"'{group}' codes of '{lang}' differ from '{languages[0]}'"
            )


def test_sections(config):
    """All sections exist and no unknown one is present (typos would be ignored silently)."""
    missing = SECTIONS - set(config)
    unknown = set(config) - SECTIONS
    assert not missing, f"missing sections in project.yml: {sorted(missing)}"
    assert not unknown, f"unknown sections in project.yml: {sorted(unknown)} (allowed: {sorted(SECTIONS)})"


# ------------------------------------------------------------------------------
# eCH metadata
# ------------------------------------------------------------------------------

def test_keys(ech):
    """All required keys exist and no unknown key is present (typos would be ignored silently)."""
    missing = REQUIRED_KEYS - set(ech)
    unknown = set(ech) - REQUIRED_KEYS - OPTIONAL_KEYS
    assert not missing, f"missing keys under 'ech': {sorted(missing)}"
    assert not unknown, f"unknown keys under 'ech': {sorted(unknown)} (allowed: {sorted(REQUIRED_KEYS | OPTIONAL_KEYS)})"


def test_dates(config, ech):
    """The date of issue is a date; the decision date is a date or null, and set for approved documents."""
    assert isinstance(config.get("date"), datetime.date), "'date' (date of issue) must be an ISO date, e.g. 2026-10-01"
    decision = ech.get("decision-date")
    assert decision is None or isinstance(decision, datetime.date), "'decision-date' must be an ISO date or null"
    if ech.get("status") in STATUSES_WITH_DECISION:
        assert decision is not None, f"status '{ech['status']}' requires a 'decision-date'"
    if decision is not None:
        assert decision <= config["date"], "'decision-date' must not be after the date of issue"


def test_number_and_version(ech):
    assert ECH_NUMBER.fullmatch(str(ech["number"])), f"'number' must look like eCH-0000, got {ech['number']!r}"
    assert SEMVER.fullmatch(str(ech["version"])), f"'version' must be a semantic version (e.g. 2.4.1), got {ech['version']!r}"


@pytest.mark.parametrize("field", sorted(CODE_GROUPS))
def test_codes(ech, vocabulary, field):
    """category, maturity and status are codes of the vocabulary."""
    allowed = codes(vocabulary, CODE_GROUPS[field])
    assert ech[field] in allowed, f"'{field}' is {ech[field]!r}, allowed: {sorted(allowed)}"


def test_replaces(ech, vocabulary):
    """'replaces' is null (first version) or gives the replaced version and the kind of change."""
    replaces = ech.get("replaces")
    if replaces is None:
        return
    assert isinstance(replaces, dict), "'replaces' must be a mapping with 'version' and 'change', or null"
    assert not set(replaces) - {"version", "change"}, f"unknown keys under 'replaces': {sorted(set(replaces) - {'version', 'change'})}"
    allowed = codes(vocabulary, "change")
    assert replaces.get("change") in allowed, f"'replaces.change' is {replaces.get('change')!r}, allowed: {sorted(allowed)}"
    if replaces["change"] != "new":
        assert SEMVER.fullmatch(str(replaces.get("version", ""))), "'replaces.version' must be a semantic version"
        assert str(replaces["version"]) != str(ech["version"]), "'replaces.version' must differ from 'version'"


def test_lists(ech):
    """prerequisites and attachments are lists of strings; prerequisites are eCH numbers."""
    for key in ("prerequisites", "attachments"):
        value = ech.get(key, [])
        assert isinstance(value, list) and all(isinstance(v, str) for v in value), f"'{key}' must be a list of strings"
    bad = [p for p in ech.get("prerequisites", []) if not ECH_NUMBER.match(p)]
    assert not bad, f"'prerequisites' must name eCH standards (eCH-0000 ...), got {bad}"


def test_languages(ech, vocabulary):
    """The original language and its translations are known codes, and each has its folder in docs/."""
    languages = ech["languages"]
    assert isinstance(languages, dict) and "original" in languages, "'languages' needs 'original' (and optionally 'translations')"
    original = languages["original"]
    translations = languages.get("translations") or []
    allowed = codes(vocabulary, "language")
    assert original in allowed, f"'languages.original' is {original!r}, allowed: {sorted(allowed)}"
    assert isinstance(translations, list) and set(translations) <= allowed, f"'languages.translations' must be a list of {sorted(allowed)}"
    assert original not in translations, "the original language is not a translation"
    assert len(translations) == len(set(translations)), "'languages.translations' has duplicates"
    configured = {original, *translations}
    assert configured == language_folders(vocabulary), (
        f"languages {sorted(configured)} differ from the language folders in docs/ {sorted(language_folders(vocabulary))}"
    )


def test_group(ech):
    assert isinstance(ech["group"], str) and ech["group"].strip(), "'group' (Fachgruppe) must be a non-empty string"


# ------------------------------------------------------------------------------
# Repository, LINDAS and dataset
# ------------------------------------------------------------------------------

def test_project(config):
    """The repository is given as owner/name, and the contact has a name and an e-mail address."""
    project = config["project"]
    assert REPOSITORY.fullmatch(str(project.get("repository", ""))), (
        f"'project.repository' must be owner/name on GitHub, got {project.get('repository')!r}"
    )
    if project.get("homepage") is not None:
        assert URL.fullmatch(str(project["homepage"])), "'project.homepage' must be an https URL"
    contact = project.get("contact") or {}
    assert isinstance(contact.get("name"), str) and contact["name"].strip(), "'project.contact.name' must be a non-empty string"
    assert EMAIL.fullmatch(str(contact.get("email", ""))), f"'project.contact.email' must be an e-mail address, got {contact.get('email')!r}"


def test_lindas(config):
    """The named graph and the three endpoints are https URLs."""
    lindas = config["lindas"]
    assert set(lindas) == LINDAS_KEYS, f"'lindas' must have exactly the keys {sorted(LINDAS_KEYS)}, got {sorted(lindas)}"
    for key in sorted(LINDAS_KEYS):
        assert URL.fullmatch(str(lindas[key])), f"'lindas.{key}' must be an https URL, got {lindas[key]!r}"


def test_dataset(config):
    """The dataset has the required entries, and its title and description exist in every documentation language."""
    dataset = config["dataset"]
    missing = DATASET_REQUIRED - set(dataset)
    unknown = set(dataset) - DATASET_REQUIRED - DATASET_OPTIONAL
    assert not missing, f"missing keys under 'dataset': {sorted(missing)}"
    assert not unknown, f"unknown keys under 'dataset': {sorted(unknown)} (allowed: {sorted(DATASET_REQUIRED | DATASET_OPTIONAL)})"
    for key in ("title", "description"):
        lacking = set(project_config.languages(config)) - set(dataset[key])
        assert not lacking, f"'dataset.{key}' lacks the languages {sorted(lacking)}"
    created = dataset.get("created")
    assert created is None or isinstance(created, datetime.date), "'dataset.created' must be an ISO date"
    for key in ("keywords",):
        value = dataset.get(key) or {}
        assert isinstance(value, dict) and all(isinstance(v, list) for v in value.values()), (
            f"'dataset.{key}' must map language codes to lists"
        )
    assert isinstance(dataset.get("themes") or [], list), "'dataset.themes' must be a list"
