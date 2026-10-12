# Warning: Please do not adjust this script in any other place than the upstream repo template

import argparse
import re
import textwrap
from pathlib import Path
from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import DCTERMS, RDF, RDFS, SKOS

SH = Namespace("http://www.w3.org/ns/shacl#")
SCHEMA = Namespace("http://schema.org/")

TRANSLATIONS = {
    "en": {
        "name": "Description",
        "path": "Path",
        "type": "Type",
        "details": "Details",
        "facts_shape": "Shape",
        "facts_class": "Class",
        "facts_target": "Target class",
        "facts_closed": "Closed",
        "facts_closed_yes": "Yes (only the listed properties are allowed)",
        "facts_closed_no": "No (further properties are allowed)",
        "facts_figures": "Key figures",
        "facts_figures_range": "{instances} instances with {min} to {max} triples each ({avg} on average)",
        "facts_figures_fixed": "{instances} instances with {min} triples each",
        "facts_open_data": "Data access",
        "facts_open_yes": "[SPARQL service]({link})",
        "facts_open_no": "None (transactional data, not part of the published graph)",
        "section_overview": "Overview",
        "section_properties": "Properties",
        "section_rules": "Rules (SPARQL)",
        "datatypes": {"string": "Text", "langString": "Language-tagged text", "date": "Date", "dateTime": "Date and time", "time": "Time", "gYear": "Year", "integer": "Integer", "int": "Integer", "long": "Integer", "nonNegativeInteger": "Non-negative integer", "positiveInteger": "Positive integer", "decimal": "Decimal number", "double": "Floating-point number", "float": "Floating-point number", "boolean": "Boolean", "anyURI": "URI", "duration": "Duration"},
        "ns_prefix": "Prefix",
        "ns_caption": "Namespaces used in {{< ech title >}}.",
        "ns_namespace": "Namespace",
        "examples": "Examples",
        "length_unit": "characters",
        "cardinality": "Cardinality",
        "target_class": "Target Class",
        "properties": "properties",
        "or": "or",
        "pattern": "Pattern",
        "range": "Range",
        "length": "Length",
        "languages": "Languages",
        "unique_lang": "one per language",
        "values": "Values",
        "has_value": "Required value",
        "severity": "Severity",
        "Warning": "Warning",
        "code_list": "Code list",
        "type_selection": "with the following selection:",
        "see_code_list": "See code list {list}",
        "type_restrictions": "with the following restrictions:",
        "restrictions": "Restrictions",
        "cl_iri": "IRI",
        "cl_code": "Code",
        "cl_name": "Name",
        "cl_description": "Description",
        "cl_caption": "Values of the code list {name}.",
        "Info": "Info",
    },
    "de": {
        "name": "Beschreibung",
        "path": "Pfad",
        "type": "Typ",
        "details": "Details",
        "facts_shape": "Shape",
        "facts_class": "Klasse",
        "facts_target": "Zielklasse",
        "facts_closed": "Geschlossen",
        "facts_closed_yes": "Ja (nur die aufgeführten Eigenschaften zulässig)",
        "facts_closed_no": "Nein (weitere Eigenschaften zulässig)",
        "facts_figures": "Kennzahlen",
        "facts_figures_range": "{instances} Instanzen mit je {min} bis {max} Tripeln (im Mittel {avg})",
        "facts_figures_fixed": "{instances} Instanzen mit je {min} Tripeln",
        "facts_open_data": "Datenzugriff",
        "facts_open_yes": "[SPARQL-Dienst]({link})",
        "facts_open_no": "Keiner (Transaktionsdaten, nicht Teil des publizierten Graphen)",
        "section_overview": "Übersicht",
        "section_properties": "Eigenschaften",
        "section_rules": "Regeln (SPARQL)",
        "datatypes": {"string": "Zeichenkette", "langString": "Sprachabhängiger Text", "date": "Datum", "dateTime": "Zeitpunkt", "time": "Uhrzeit", "gYear": "Jahr", "integer": "Ganzzahl", "int": "Ganzzahl", "long": "Ganzzahl", "nonNegativeInteger": "Nicht negative Ganzzahl", "positiveInteger": "Positive Ganzzahl", "decimal": "Dezimalzahl", "double": "Gleitkommazahl", "float": "Gleitkommazahl", "boolean": "Wahrheitswert", "anyURI": "URI", "duration": "Zeitdauer"},
        "ns_prefix": "Präfix",
        "ns_caption": "In {{< ech title >}} verwendete Namespaces.",
        "ns_namespace": "Namespace",
        "examples": "Beispiele",
        "length_unit": "Zeichen",
        "cardinality": "Kardinalität",
        "target_class": "Zielklasse",
        "properties": "Eigenschaften",
        "or": "oder",
        "pattern": "Muster",
        "range": "Wertebereich",
        "length": "Länge",
        "languages": "Sprachen",
        "unique_lang": "eine pro Sprache",
        "values": "Werte",
        "has_value": "Pflichtwert",
        "severity": "Schweregrad",
        "Warning": "Warnung",
        "code_list": "Codeliste",
        "type_selection": "mit folgender Auswahl:",
        "see_code_list": "Siehe Codeliste {list}",
        "type_restrictions": "mit folgenden Einschränkungen:",
        "restrictions": "Einschränkungen",
        "cl_iri": "IRI",
        "cl_code": "Code",
        "cl_name": "Name",
        "cl_description": "Beschreibung",
        "cl_caption": "Werte der Codeliste {name}.",
        "Info": "Hinweis",
    },
    "fr": {
        "name": "Description",
        "path": "Chemin",
        "type": "Type",
        "details": "Détails",
        "facts_shape": "Shape",
        "facts_class": "Classe",
        "facts_target": "Classe cible",
        "facts_closed": "Fermée",
        "facts_closed_yes": "Oui (seules les propriétés énumérées sont admises)",
        "facts_closed_no": "Non (d'autres propriétés sont admises)",
        "facts_figures": "Chiffres clés",
        "facts_figures_range": "{instances} instances avec chacune {min} à {max} triplets ({avg} en moyenne)",
        "facts_figures_fixed": "{instances} instances avec chacune {min} triplets",
        "facts_open_data": "Accès aux données",
        "facts_open_yes": "[Service SPARQL]({link})",
        "facts_open_no": "Aucun (données transactionnelles, ne faisant pas partie du graphe publié)",
        "section_overview": "Aperçu",
        "section_properties": "Propriétés",
        "section_rules": "Règles (SPARQL)",
        "datatypes": {"string": "Chaîne de caractères", "langString": "Texte avec indication de langue", "date": "Date", "dateTime": "Date et heure", "time": "Heure", "gYear": "Année", "integer": "Nombre entier", "int": "Nombre entier", "long": "Nombre entier", "nonNegativeInteger": "Nombre entier non négatif", "positiveInteger": "Nombre entier positif", "decimal": "Nombre décimal", "double": "Nombre à virgule flottante", "float": "Nombre à virgule flottante", "boolean": "Booléen", "anyURI": "URI", "duration": "Durée"},
        "ns_prefix": "Préfixe",
        "ns_caption": "Espaces de noms utilisés dans {{< ech title >}}.",
        "ns_namespace": "Espace de noms",
        "examples": "Exemples",
        "length_unit": "caractères",
        "cardinality": "Cardinalité",
        "target_class": "Classe cible",
        "properties": "propriétés",
        "or": "ou",
        "pattern": "Motif",
        "range": "Plage de valeurs",
        "length": "Longueur",
        "languages": "Langues",
        "unique_lang": "une par langue",
        "values": "Valeurs",
        "has_value": "Valeur obligatoire",
        "severity": "Gravité",
        "Warning": "Avertissement",
        "code_list": "Liste de codes",
        "type_selection": "avec la sélection suivante:",
        "see_code_list": "Voir la liste de codes {list}",
        "type_restrictions": "avec les restrictions suivantes:",
        "restrictions": "Restrictions",
        "cl_iri": "IRI",
        "cl_code": "Code",
        "cl_name": "Nom",
        "cl_description": "Description",
        "cl_caption": "Valeurs de la liste de codes {name}.",
        "Info": "Information",
    },
    "it": {
        "name": "Nome",
        "path": "Percorso",
        "type": "Tipo",
        "details": "Dettagli",
        "facts_shape": "Shape",
        "facts_class": "Classe",
        "facts_target": "Classe di destinazione",
        "facts_closed": "Chiusa",
        "facts_closed_yes": "Sì (solo le proprietà elencate sono ammesse)",
        "facts_closed_no": "No (altre proprietà sono ammesse)",
        "facts_figures": "Indicatori",
        "facts_figures_range": "{instances} istanze con {min}–{max} triple ciascuna ({avg} in media)",
        "facts_figures_fixed": "{instances} istanze con {min} triple ciascuna",
        "facts_open_data": "Accesso ai dati",
        "facts_open_yes": "[Servizio SPARQL]({link})",
        "facts_open_no": "Nessuno (dati transazionali, non inclusi nel grafo pubblicato)",
        "section_overview": "Panoramica",
        "section_properties": "Proprietà",
        "section_rules": "Regole (SPARQL)",
        "datatypes": {"string": "Stringa", "langString": "Testo con indicazione della lingua", "date": "Data", "dateTime": "Data e ora", "time": "Ora", "gYear": "Anno", "integer": "Numero intero", "int": "Numero intero", "long": "Numero intero", "nonNegativeInteger": "Numero intero non negativo", "positiveInteger": "Numero intero positivo", "decimal": "Numero decimale", "double": "Numero a virgola mobile", "float": "Numero a virgola mobile", "boolean": "Booleano", "anyURI": "URI", "duration": "Durata"},
        "ns_prefix": "Prefisso",
        "ns_caption": "Spazi dei nomi utilizzati in {{< ech title >}}.",
        "ns_namespace": "Spazio dei nomi",
        "examples": "Esempi",
        "length_unit": "caratteri",
        "cardinality": "Cardinalità",
        "target_class": "Classe di destinazione",
        "properties": "proprietà",
        "or": "o",
        "pattern": "Modello",
        "range": "Intervallo",
        "length": "Lunghezza",
        "languages": "Lingue",
        "unique_lang": "una per lingua",
        "values": "Valori",
        "has_value": "Valore obbligatorio",
        "severity": "Gravità",
        "Warning": "Avvertimento",
        "code_list": "Elenco di codici",
        "type_selection": "con la seguente selezione:",
        "see_code_list": "Vedi l'elenco di codici {list}",
        "type_restrictions": "con le seguenti restrizioni:",
        "restrictions": "Restrizioni",
        "cl_iri": "IRI",
        "cl_code": "Codice",
        "cl_name": "Nome",
        "cl_description": "Descrizione",
        "cl_caption": "Valori dell'elenco di codici {name}.",
        "Info": "Informazione",
    }
}

# Constraint components rendered after the description of a property.
RANGE_PREDICATES = [
    (SH.minInclusive, "≥"), (SH.minExclusive, ">"),
    (SH.maxInclusive, "≤"), (SH.maxExclusive, "<"),
]


def code(text):
    """Inline code for a table cell; pipes must be escaped inside pipe tables."""
    return "`" + str(text).replace("|", "\\|") + "`"


def qname_link(g, uri):
    """A prefixed name linked to its IRI: [prefix:Name](https://…/Name)."""
    return f"[{format_uri(g, uri)}]({uri})"


def format_literal(value):
    """Short textual form of a literal (dates and numbers without datatype noise)."""
    return str(value.toPython()) if hasattr(value, "toPython") else str(value)


def rdf_list(g, head):
    items = []
    while head and head != RDF.nil:
        items.append(g.value(head, RDF.first))
        head = g.value(head, RDF.rest)
    return items


def code_lists_of(g, prop):
    """The code lists (schema:CategoryCodeSet) that a property shape restricts its
    values to, declared as sh:node [ sh:property [ sh:path schema:inCodeSet ;
    sh:hasValue <code list> ] ]."""
    lists = []
    for node in g.objects(prop, SH.node):
        for nested in g.objects(node, SH.property):
            if g.value(nested, SH.path) == SCHEMA.inCodeSet:
                lists.extend(v for v in g.objects(nested, SH.hasValue) if isinstance(v, URIRef))
    return lists


def code_list_slug(code_list):
    """Section slug of a code list, language-independent: codelist-<local name>."""
    return "codelist-" + slugify(str(code_list).split('#')[-1].split('/')[-1])


def code_list_label(g, data, code_list, lang):
    """Name of a code list in the data graph, falling back to its QName."""
    return (get_localized_value(data, code_list, [SCHEMA.name], lang) if data is not None else None) or format_uri(g, code_list)


def code_entry(g, data, iri, lang):
    """(code value, name) of a code of a code list, or None if the IRI is no
    schema:CategoryCode with a code value in the data graph."""
    value = data.value(iri, SCHEMA.codeValue) if data is not None else None
    if value is None:
        return None
    return str(value), get_localized_value(data, iri, [SCHEMA.name], lang) or format_uri(g, iri)


def values_list(g, data, members, lang):
    """The members of a sh:in list. Codes of a code list become a nested list of
    their names with the linked prefixed IRI, "Name ([media:1](…))"; other
    values stay a comma-separated line."""
    entries = [(v, code_entry(g, data, v, lang) if isinstance(v, URIRef) else None) for v in members]
    if not any(entry for _, entry in entries):
        return ", ".join(qname_link(g, v) if isinstance(v, URIRef) else code(format_literal(v)) for v in members)
    items = []
    for v, entry in entries:
        if entry:
            items.append(f"  - {sanitize_cell(entry[1])} ({qname_link(g, v)})")
        elif isinstance(v, URIRef):
            items.append(f"  - {qname_link(g, v)}")
        else:
            items.append(f"  - {code(format_literal(v))}")
    return "\n" + "\n".join(items)


def inline_restrictions(g, prop):
    """The property shapes of the inline node shapes (blank nodes under sh:node)
    of a property shape, except the code list restriction (schema:inCodeSet with
    sh:hasValue), which is rendered separately. Sorted by sh:order, then path."""
    nested = []
    for node in g.objects(prop, SH.node):
        if isinstance(node, URIRef):
            continue
        for shape in g.objects(node, SH.property):
            if g.value(shape, SH.path) == SCHEMA.inCodeSet and g.value(shape, SH.hasValue) is not None:
                continue
            order = g.value(shape, SH.order)
            nested.append((order.toPython() if order is not None else 9999, str(g.value(shape, SH.path) or ""), shape))
    return [shape for _, _, shape in sorted(nested, key=lambda n: n[:2])]


def property_name(g, shape, path, lang):
    """The localized name of the property shape with the given path in a node shape."""
    for prop in g.objects(shape, SH.property):
        if g.value(prop, SH.path) == path:
            return get_localized_value(g, prop, [SH.name, RDFS.label], lang)
    return None


def describe_restriction(g, nested, trans, data, lang, format_type, name):
    """One line for a nested property shape: "name (path): type, constraints, cardinality"."""
    path = g.value(nested, SH.path)
    phrases = []
    primary = next((t for t in [g.value(nested, SH.node), g.value(nested, SH["class"]), g.value(nested, SH.datatype)]
                    if isinstance(t, URIRef)), None)
    if primary is not None:
        phrases.append(f"{trans['type']} {format_type(primary)}")
    phrases.extend(f"{label} {value}" for label, value in describe_constraints(g, nested, trans, data, lang))
    min_c, max_c = g.value(nested, SH.minCount), g.value(nested, SH.maxCount)
    if min_c is not None or max_c is not None:
        phrases.append(f"{trans['cardinality']} {min_c if min_c is not None else 0}..{max_c if max_c is not None else '*'}")
    head = f"{sanitize_cell(name)} ({qname_link(g, path)})" if name else qname_link(g, path)
    return f"  - {head}: {', '.join(phrases)}" if phrases else f"  - {head}"


def describe_constraints(g, prop, trans, data=None, lang=None, skip_values=False):
    """Returns the value constraints of a property shape as (label, value) pairs.
    `skip_values` leaves out the sh:in list (shown with the type instead)."""
    parts = []

    pattern = g.value(prop, SH.pattern)
    if pattern is not None:
        flags = g.value(prop, SH.flags)
        text = code(pattern) + (f" ({code(flags)})" if flags is not None else "")
        parts.append((trans['pattern'], text))

    bounds = [f"{symbol} {format_literal(g.value(prop, pred))}"
              for pred, symbol in RANGE_PREDICATES if g.value(prop, pred) is not None]
    if bounds:
        parts.append((trans['range'], ', '.join(bounds)))

    min_len, max_len = g.value(prop, SH.minLength), g.value(prop, SH.maxLength)
    if min_len is not None or max_len is not None:
        if min_len is not None and max_len is not None:
            text = f"{min_len}–{max_len}"
        elif min_len is not None:
            text = f"≥ {min_len}"
        else:
            text = f"≤ {max_len}"
        parts.append((trans['length'], f"{text} {trans['length_unit']}"))

    languages = g.value(prop, SH.languageIn)
    if languages is not None:
        text = ", ".join(code(lang) for lang in rdf_list(g, languages))
        if g.value(prop, SH.uniqueLang) is not None and bool(g.value(prop, SH.uniqueLang).toPython()):
            text += f" ({trans['unique_lang']})"
        parts.append((trans['languages'], text))
    elif g.value(prop, SH.uniqueLang) is not None and bool(g.value(prop, SH.uniqueLang).toPython()):
        parts.append((trans['languages'], trans['unique_lang']))

    allowed = g.value(prop, SH["in"])
    if allowed is not None and not skip_values:
        parts.append((trans['values'], values_list(g, data, rdf_list(g, allowed), lang)))

    required = g.value(prop, SH.hasValue)
    if required is not None:
        text = qname_link(g, required) if str(required).startswith("http") else code(format_literal(required))
        parts.append((trans['has_value'], text))

    examples = sorted(g.objects(prop, SKOS.example), key=str)
    if examples:
        rendered = [qname_link(g, e) if isinstance(e, URIRef) else format_literal(e) for e in examples]
        parts.append((trans['examples'], ", ".join(rendered)))

    severity = g.value(prop, SH.severity)
    if severity is not None and severity != SH.Violation:
        level = str(severity).split("#")[-1]
        parts.append((trans['severity'], trans.get(level, level)))

    return parts

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

def build_grid_table(headers, rows, min_col_widths, align=None):
    """Builds a Pandoc grid table; cells may contain several lines and lists.
    `align` lists "left" or "right" per column (default left)."""
    align = align or ["left"] * len(headers)
    col_widths = list(min_col_widths)
    for row in [headers] + rows:
        for i, cell in enumerate(row):
            for paragraph in str(cell).split('\n'):
                # continuation lines of a list item are indented (see wrap_cell)
                item = re.match(r'^(\s*)[-*] ', paragraph)
                indent = len(item.group(1)) + 2 if item else 0
                for word in paragraph.split():
                    if len(word) + indent > col_widths[i] - 2:
                        col_widths[i] = len(word) + indent + 2

    def wrap_cell(text, width):
        lines = []
        for paragraph in str(text).split('\n'):
            if paragraph.strip() == '':
                lines.append('')
            else:
                # continuation lines of a list item stay inside the item (nested lists)
                item = re.match(r'^(\s*)[-*] ', paragraph)
                indent = ' ' * (len(item.group(1)) + 2) if item else ''
                lines.extend(textwrap.wrap(paragraph, width, break_long_words=False, break_on_hyphens=False,
                                           subsequent_indent=indent))
        return lines or ['']

    def format_row(row_data, separator_char='-', header=False):
        wrapped = [wrap_cell(cell, w - 2) for cell, w in zip(row_data, col_widths)]
        max_lines = max((len(c) for c in wrapped), default=1)
        lines = []
        for i in range(max_lines):
            parts = []
            for col_idx, c in enumerate(wrapped):
                val = c[i] if i < len(c) else ""
                parts.append(f" {val.ljust(col_widths[col_idx] - 2)} ")
            lines.append("|" + "|".join(parts) + "|")
        sep_parts = []
        for w, a in zip(col_widths, align):
            if header:
                # the colon in the header separator sets the column alignment
                sep_parts.append(("=" * (w - 1) + ":") if a == "right" else (":" + "=" * (w - 1)))
            else:
                sep_parts.append(separator_char * w)
        return lines, "+" + "+".join(sep_parts) + "+"

    output = ["+" + "+".join("-" * w for w in col_widths) + "+"]
    h_lines, h_sep = format_row(headers, header=True)
    output.extend(h_lines)
    output.append(h_sep)
    for row in rows:
        r_lines, r_sep = format_row(row)
        output.extend(r_lines)
        output.append(r_sep)
    return output


def get_localized_value(g, subject, predicates, lang):
    """Finds the best matching localized value for a given subject and list of predicates."""
    for predicate in predicates:
        values = {}
        for obj in g.objects(subject, predicate):
            if hasattr(obj, 'language') and obj.language:
                values[obj.language.lower()] = str(obj)
            else:
                values[''] = str(obj)
        if not values:
            continue            
        if lang in values:
            return values[lang]
        if '' in values:
            return values['']
            
    return None

def class_statistics(data, target_class):
    """Instances of a class in the data graph and the number of triples per
    instance (average, minimum, maximum); None without a data graph."""
    if data is None or target_class is None:
        return None
    query = """
        SELECT ?s (COUNT(*) AS ?n)
        WHERE { ?s a ?cls . ?s ?p ?o . }
        GROUP BY ?s
    """
    counts = [int(row.n) for row in data.query(query, initBindings={'cls': target_class})]
    if not counts:
        return {"instances": 0}
    return {"instances": len(counts), "avg": sum(counts) / len(counts), "min": min(counts), "max": max(counts)}


LINDAS_YASGUI = "https://lindas.admin.ch/sparql/#"


def yasgui_link(g, target_class, properties, graph_iri):
    """Link to LINDAS' Yasgui with a prepared query that lists the instances
    of the class with the properties of the property table. `properties` is a
    list of (path, required) pairs; required properties are matched directly,
    the others optionally."""
    from urllib.parse import quote

    used_prefixes = {}
    def qname(uri):
        try:
            prefix, namespace, local = g.namespace_manager.compute_qname(str(uri), generate=False)
        except Exception:
            return f"<{uri}>"
        used_prefixes[prefix] = str(namespace)
        return f"{prefix}:{local}"

    variables, seen = [], set()
    for path, required in properties:
        local = re.sub(r'[^A-Za-z0-9_]', '_', str(path).rstrip('/').split('#')[-1].split('/')[-1])
        while local in seen:
            local += "_"
        seen.add(local)
        variables.append((local, qname(path), required))

    class_qname = qname(target_class)  # collects its prefix before the PREFIX lines are built
    lines = [f"PREFIX {pfx}: <{ns}>" for pfx, ns in sorted(used_prefixes.items())]
    lines.append("SELECT ?iri " + " ".join(f"?{v}" for v, _, _ in variables))
    if graph_iri:
        lines.append(f"FROM <{graph_iri}>")
    lines.append("WHERE {")
    lines.append(f"  ?iri a {class_qname} .")
    for v, path, required in variables:
        if required:
            lines.append(f"  ?iri {path} ?{v} .")
        else:
            lines.append(f"  OPTIONAL {{ ?iri {path} ?{v} . }}")
    lines.append("}")
    lines.append("LIMIT 1000")
    return LINDAS_YASGUI + "query=" + quote("\n".join(lines), safe="")


def fact_sheet(g, data, shape, target_class, properties, graph_iri, trans):
    """Key-value lines (Pandoc definition list) summarising a node shape."""
    if target_class is not None and target_class == shape:
        # a class that is its own shape ("shape class")
        facts = [(trans['facts_class'], qname_link(g, shape))]
    else:
        facts = [(trans['facts_shape'], qname_link(g, shape))]
        if target_class is not None:
            facts.append((trans['facts_target'], qname_link(g, target_class)))
    closed = g.value(shape, SH.closed)
    facts.append((trans['facts_closed'], trans['facts_closed_yes'] if closed is not None and bool(closed.toPython()) else trans['facts_closed_no']))
    stats = class_statistics(data, target_class)
    if stats is not None:
        if stats['instances']:
            template = trans['facts_figures_fixed'] if stats['min'] == stats['max'] else trans['facts_figures_range']
            facts.append((trans['facts_figures'], template.format(
                instances=stats['instances'], min=stats['min'], max=stats['max'], avg=f"{stats['avg']:.1f}")))
            # comma-separated list of access points (more to come, e.g. i14y)
            access = [trans['facts_open_yes'].format(link=yasgui_link(g, target_class, properties, graph_iri))]
            facts.append((trans['facts_open_data'], ", ".join(access)))
        else:
            facts.append((trans['facts_open_data'], trans['facts_open_no']))
    lines = ["::: {.ech-facts}"]
    for key, value in facts:
        lines.append(f"{key}")
        lines.append(f":   {value}")
        lines.append("")
    lines.append(":::")
    return lines


# Positions in a shape graph whose IRIs belong to the described data, as
# opposed to the SHACL vocabulary that merely structures the shapes.
DATA_POSITIONS = [SH.path, SH.targetClass, SH["class"], SH.datatype, SH.node, SH.hasValue]


def natural_key(text):
    """Sort key that orders embedded numbers numerically ("2" before "10")."""
    return [int(part) if part.isdigit() else part.lower() for part in re.split(r'(\d+)', str(text))]


def alternate_names(data, subject, lang):
    """Language-independent alternate names and those of the page language."""
    names = {str(o) for o in data.objects(subject, SCHEMA.alternateName)
             if not getattr(o, "language", None) or o.language.lower() == lang}
    return sorted(names)


def code_list_pages(g, data, lang, trans):
    """Markdown of the chapter on code lists: one section per
    schema:CategoryCodeSet of the data graph with its description and a table
    of its codes (IRI, code value, name with alternate names, description)."""
    lines = []
    code_lists = sorted(set(data.subjects(RDF.type, SCHEMA.CategoryCodeSet)),
                        key=lambda cl: (code_list_label(g, data, cl, lang).lower(), str(cl)))
    for code_list in code_lists:
        label = sanitize_cell(code_list_label(g, data, code_list, lang))
        slug = code_list_slug(code_list)
        lines.append(f"## {label} {{#sec-{slug}}}")
        lines.append("")
        description = get_localized_value(data, code_list, [SCHEMA.description], lang)
        if description:
            lines.append(sanitize_cell(description))
            lines.append("")
        codes = set(data.objects(code_list, SCHEMA.hasCategoryCode)) | set(data.subjects(SCHEMA.inCodeSet, code_list))
        rows = []
        for item in sorted(codes, key=lambda c: (natural_key(data.value(c, SCHEMA.codeValue) or ""), str(c))):
            value = data.value(item, SCHEMA.codeValue)
            name = get_localized_value(data, item, [SCHEMA.name], lang) or format_uri(g, item)
            alternates = alternate_names(data, item, lang)
            if alternates:
                name += f" ({', '.join(alternates)})"
            rows.append([qname_link(g, item),
                         code(value) if value is not None else "",
                         sanitize_cell(name),
                         sanitize_cell(get_localized_value(data, item, [SCHEMA.description], lang) or "")])
        lines.extend(build_grid_table([trans['cl_iri'], trans['cl_code'], trans['cl_name'], trans['cl_description']],
                                      rows, [20, 10, 30, 50]))
        lines.append("")
        # explicit widths: the IRI links make the ASCII column wider than it should render
        lines.append(f": {trans['cl_caption'].format(name=label)} {{#tbl-{slug} tbl-colwidths=\"[18,10,30,42]\"}}")
        lines.append("")
    return lines


def used_namespaces(g, shapes):
    """Prefixes and namespaces of all IRIs that the data model refers to:
    the node shapes themselves, property paths, target classes, classes,
    datatypes, referenced shapes and the members of sh:in lists."""
    iris = set(shapes)
    for predicate in DATA_POSITIONS:
        iris.update(o for o in g.objects(None, predicate) if isinstance(o, URIRef))
    for head in g.objects(None, SH["in"]):
        iris.update(v for v in rdf_list(g, head) if isinstance(v, URIRef))
    iris.update(e for e in g.objects(None, SKOS.example) if isinstance(e, URIRef))
    namespaces = {}
    for iri in iris:
        try:
            prefix, namespace, _ = g.namespace_manager.compute_qname(str(iri), generate=False)
        except Exception:
            continue
        namespaces[prefix] = str(namespace)
    return sorted(namespaces.items(), key=lambda item: (item[0] != "", item[0]))


def main():
    parser = argparse.ArgumentParser(description="Generate Markdown documentation from a SHACL model.")
    parser.add_argument("-i", "--input", required=True, help="Input SHACL file (.ttl)")
    parser.add_argument("-d", "--docs_dir", required=True, help="Docs directory containing language subdirectories")
    parser.add_argument("-p", "--prefixes", required=False, help="Prefix file (.ttl) to override QNames")
    parser.add_argument("-g", "--graph", required=False, help="Processed data graph (.ttl) for instance statistics")
    parser.add_argument("-c", "--config", required=False, help="eCH metadata (.yml) with the named graph on LINDAS (ech.graph)")
    args = parser.parse_args()

    graph_iri = None
    if args.config and Path(args.config).is_file():
        import yaml
        with open(args.config, encoding="utf-8") as f:
            graph_iri = (yaml.safe_load(f) or {}).get("ech", {}).get("graph")

    data = None
    if args.graph and Path(args.graph).is_file():
        data = Graph(bind_namespaces="none")
        data.parse(args.graph, format="turtle")

    g = Graph(bind_namespaces="none")
    g.parse(args.input, format="turtle")

    if args.prefixes:
        prefix_g = Graph(bind_namespaces="none")
        prefix_g.parse(args.prefixes, format="turtle")
        for prefix, uri in prefix_g.namespaces():
            try:
                g.bind(str(prefix), Namespace(str(uri)), override=True, replace=True)
            except TypeError:
                g.bind(str(prefix), Namespace(str(uri)), override=True)

    docs_dir = Path(args.docs_dir)
    languages_to_process = []
    for lang in TRANSLATIONS.keys():
        if (docs_dir / lang).is_dir():
            languages_to_process.append(lang)

    q_classes = """
        PREFIX sh: <http://www.w3.org/ns/shacl#>
        
        SELECT ?shape ?targetClass
        WHERE {
            ?shape a sh:NodeShape .
            OPTIONAL { ?shape sh:targetClass ?targetClass . }
        }
    """
    
    shapes_list = []
    for row in g.query(q_classes):
        shapes_list.append({
            'uri': row.shape,
            'target_class': row.targetClass
        })

    for lang in languages_to_process:
        md_lines = []
        trans = TRANSLATIONS[lang]
        
        shapes_data = []
        uri_to_slug = {}
        uri_to_label = {}
        class_to_shape = {}
        
        for s_info in shapes_list:
            shape_uri = s_info['uri']
            target_class = s_info['target_class']
            
            # Fetch localized label, fall back to QName / technical name
            label = get_localized_value(g, shape_uri, [RDFS.label, SH.name], lang)
            if not label:
                label = format_uri(g, shape_uri)
                
            comment = get_localized_value(g, shape_uri, [RDFS.comment, SH.description], lang) or ""
            
            # Extract local name from the URI to ensure stable, language-independent slugs
            local_name = str(shape_uri).split('#')[-1].split('/')[-1]
            slug = f"nodeshape-{slugify(local_name)}"
            
            uri_to_slug[shape_uri] = slug
            uri_to_label[shape_uri] = label
            if target_class:
                uri_to_slug[target_class] = slug
                class_to_shape[target_class] = shape_uri
                uri_to_label[target_class] = label
                
            shapes_data.append({
                'uri': shape_uri,
                'label': label,
                'comment': comment,
                'target_class': target_class,
                'slug': slug
            })
            
        shapes_data.sort(key=lambda x: x['label'].lower())

        for s_data in shapes_data:
            shape = s_data['uri']
            label = s_data['label']
            comment = s_data['comment']
            target_class = s_data['target_class']
            slug = s_data['slug']

            md_lines.append(f"## {label} {{#sec-{slug}}}")
            md_lines.append("")
            
            if comment:
                md_lines.append(f"{comment}")
                md_lines.append("")
                
            q_props = """
                PREFIX sh: <http://www.w3.org/ns/shacl#>
                
                SELECT ?prop ?path ?datatype ?class ?node ?minCount ?maxCount ?nodeKind ?order
                WHERE {
                    ?shape sh:property ?prop .
                    OPTIONAL { ?prop sh:path ?path . }
                    OPTIONAL { ?prop sh:datatype ?datatype . }
                    OPTIONAL { ?prop sh:class ?class . }
                    OPTIONAL { ?prop sh:node ?node . }
                    OPTIONAL { ?prop sh:minCount ?minCount . }
                    OPTIONAL { ?prop sh:maxCount ?maxCount . }
                    OPTIONAL { ?prop sh:nodeKind ?nodeKind . }
                    OPTIONAL { ?prop sh:order ?order . }
                } ORDER BY ?order ?path
            """
            
            props = list(g.query(q_props, initBindings={'shape': shape}))
            
            enriched_props = []
            for p in props:
                prop_uri = p["prop"]
                p_name = get_localized_value(g, prop_uri, [SH.name, RDFS.label], lang) or ""
                p_desc = get_localized_value(g, prop_uri, [SH.description, RDFS.comment, SH.message], lang) or ""
                p_path_qname = format_uri(g, p['path']) if p['path'] else ""
                order = p['order'].toPython() if p['order'] else 9999
                
                enriched_props.append({
                    'prop': prop_uri,
                    'name': p_name,
                    'desc': p_desc,
                    'path': p['path'],
                    'path_qname': p_path_qname,
                    'datatype': p['datatype'],
                    'class': p['class'],
                    'node': p['node'],
                    'minCount': p['minCount'],
                    'maxCount': p['maxCount'],
                    'nodeKind': p['nodeKind'],
                    'order': order
                })
                
            enriched_props.sort(key=lambda x: (x['order'], x['name'].lower(), x['path_qname'].lower()))

            properties = [(p['path'], p['minCount'] is not None and int(p['minCount']) > 0) for p in enriched_props if p['path'] is not None]
            md_lines.append(f"### {trans['section_overview']} {{#sec-{slug}-overview .unlisted}}")
            md_lines.append("")
            md_lines.extend(fact_sheet(g, data, shape, target_class, properties, graph_iri, trans))
            md_lines.append("")

            if enriched_props:
                md_lines.append(f"### {trans['section_properties']} {{#sec-{slug}-properties .unlisted}}")
                md_lines.append("")
                headers = [trans['name'], trans['details'], trans['cardinality']]
                rows = []

                for p in enriched_props:
                    sh_name = sanitize_cell(p["name"])
                    sh_desc = sanitize_cell(p["desc"])

                    # "**Name** (`path`): description"
                    p_path_str = qname_link(g, p['path']) if p["path"] else ""
                    heading_parts = []
                    if sh_name:
                        heading_parts.append(f"**{sh_name}**")
                    if p_path_str:
                        heading_parts.append(f"({p_path_str})")
                    display_name = " ".join(heading_parts)
                    if sh_desc:
                        display_name = f"{display_name}: {sh_desc}" if display_name else sh_desc

                    # Expected type, in order of preference: the node shape
                    # (sh:node), the class (sh:class), the datatype. Shapes and
                    # classes described in this document are shown by the shape's
                    # label and linked; common datatypes get a readable name with
                    # the QName in parentheses. sh:nodeKind alone carries no type.
                    def format_type(t_uri):
                        if t_uri in uri_to_slug:
                            return f"[{uri_to_label[t_uri]}](#sec-{uri_to_slug[t_uri]})"
                        qname = format_uri(g, t_uri)
                        local = str(t_uri).split('#')[-1].split('/')[-1]
                        if local in trans['datatypes']:
                            return f"{trans['datatypes'][local]} ({qname_link(g, t_uri)})"
                        return qname_link(g, t_uri)

                    # an inline node shape (blank node, e.g. a code list restriction) is not a type
                    node = p["node"] if isinstance(p["node"], URIRef) else None
                    primary = next((t for t in [node, p["class"], p["datatype"]] if t), None)
                    types = [format_type(primary)] if primary else []

                    if not types and p["prop"]:
                        q_or = """
                            PREFIX sh: <http://www.w3.org/ns/shacl#>
                            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                            SELECT ?alt ?node ?cls ?datatype WHERE {
                                ?prop sh:or/rdf:rest*/rdf:first ?alt .
                                OPTIONAL { ?alt sh:node ?node . }
                                OPTIONAL { ?alt sh:class ?cls . }
                                OPTIONAL { ?alt sh:datatype ?datatype . }
                            }
                        """
                        for alt in g.query(q_or, initBindings={'prop': p['prop']}):
                            t_uri = next((t for t in [alt.node, alt.cls, alt.datatype] if t), None)
                            if t_uri:
                                types.append(format_type(t_uri))

                    # Values from a code list: "Type: schema:CategoryCode, see code list X",
                    # or with an sh:in subset "Type: schema:CategoryCode with the following
                    # selection:" + the values, then "See code list X" on its own line.
                    details = []
                    code_lists = code_lists_of(g, p["prop"])
                    allowed = g.value(p["prop"], SH["in"])
                    see = None
                    if code_lists:
                        links = ", ".join(f"[{code_list_label(g, data, cl, lang)}](#sec-{code_list_slug(cl)})" for cl in code_lists)
                        see = trans['see_code_list'].format(list=links)
                    # Inline node shapes (sh:node [ sh:property [...] ]): "Type: X with the
                    # following restrictions:" + one line per nested property shape, named
                    # after the property of the shape that describes the class, if any.
                    restrictions = inline_restrictions(g, p["prop"])
                    shape_of_class = class_to_shape.get(p["class"]) if p["class"] else None
                    restriction_lines = "\n".join(
                        describe_restriction(g, nested, trans, data, lang, format_type,
                                             get_localized_value(g, nested, [SH.name, RDFS.label], lang)
                                             or (property_name(g, shape_of_class, g.value(nested, SH.path), lang) if shape_of_class else None))
                        for nested in restrictions)
                    if types:
                        type_text = f" {trans['or']} ".join(types)
                        if see and allowed is not None:
                            # the "see code list" line stays in the type item, as a paragraph after the values
                            type_text += f" {trans['type_selection']}" + values_list(g, data, rdf_list(g, allowed), lang)
                            details.append((trans['type'], f"{type_text}\n\n  {see}"))
                        elif see:
                            details.append((trans['type'], f"{type_text}, {see[0].lower()}{see[1:]}"))
                        elif restrictions:
                            details.append((trans['type'], f"{type_text} {trans['type_restrictions']}\n{restriction_lines}"))
                            restrictions = []
                        else:
                            details.append((trans['type'], type_text))
                    elif see:
                        details.append((None, see))
                    if restrictions:
                        details.append((trans['restrictions'], "\n" + restriction_lines))
                    details.extend(describe_constraints(g, p["prop"], trans, data, lang,
                                                        skip_values=bool(see and types and allowed is not None)))
                    details_cell = "\n".join(f"- {label}: {value}" if label else f"- {value}" for label, value in details)
                    if details and "\n  - " in details[0][1]:
                        # A nested list in the first item: pandoc's Typst writer would put that
                        # item on the cell's opening line, which breaks Typst's indentation-based
                        # nesting. A zero-height spacer first makes the list start on its own line.
                        details_cell = "```{=typst}\n#v(0pt)\n```\n\n" + details_cell

                    min_c = str(p["minCount"]) if p["minCount"] else "0"
                    max_c = str(p["maxCount"]) if p["maxCount"] else "*"
                    cardinality = f"{min_c}..{max_c}"

                    rows.append([display_name, details_cell, cardinality])

                # Grid table without caption; the relative column widths of
                # the ASCII grid (42 / 44 / 14) become the rendered widths.
                md_lines.extend(build_grid_table(headers, rows, [42, 44, 14], align=["left", "left", "right"]))
                md_lines.append("")

            # SPARQL rules: one subsection per rule with its description and query
            rules = []
            for constraint in g.objects(shape, SH.sparql):
                r_name = get_localized_value(g, constraint, [SH.name, RDFS.label], lang)
                r_desc = get_localized_value(g, constraint, [DCTERMS.description, SH.description, SH.message], lang)
                r_query = g.value(constraint, SH.select)
                rules.append((r_name or r_desc or "", r_desc if r_name else None, str(r_query).strip("\n") if r_query else None))
            if rules:
                md_lines.append(f"### {trans['section_rules']} {{#sec-{slug}-rules .unlisted}}")
                md_lines.append("")
                for index, (r_name, r_desc, r_query) in enumerate(sorted(rules, key=lambda r: r[0].lower()), start=1):
                    md_lines.append(f"#### {sanitize_cell(r_name)} {{#sec-{slug}-rule-{index} .unlisted}}")
                    md_lines.append("")
                    if r_desc:
                        md_lines.append(sanitize_cell(r_desc))
                        md_lines.append("")
                    if r_query:
                        md_lines.append("```sparql")
                        md_lines.append(textwrap.dedent(r_query).strip())
                        md_lines.append("```")
                        md_lines.append("")

        output_path = docs_dir / lang / "entities.md"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(md_lines))

        # Prefixes and namespaces used by the data model
        ns_rows = [[f"{prefix}:", namespace] for prefix, namespace in used_namespaces(g, [s['uri'] for s in shapes_list])]
        ns_lines = build_grid_table([trans['ns_prefix'], trans['ns_namespace']], ns_rows, [20, 80])
        ns_lines.append(f"\n: {trans['ns_caption']} {{#tbl-namespaces}}")
        with open(docs_dir / lang / "namespaces.md", "w", encoding="utf-8") as f:
            f.write("\n".join(ns_lines) + "\n")

        # Values of the code lists (schema:CategoryCodeSet) of the data graph
        cl_lines = code_list_pages(g, data, lang, trans) if data is not None else []
        with open(docs_dir / lang / "codelists.md", "w", encoding="utf-8") as f:
            f.write("\n".join(cl_lines))

if __name__ == "__main__":
    main()