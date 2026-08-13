# eCH-1234 Quarto-Dokument als Vorlage

13. August 2026

- [Hinweis](#hinweis)
- [<span class="toc-section-number">1</span> Einleitung](#einleitung)
  - [<span class="toc-section-number">1.1</span> Status](#status)
  - [<span class="toc-section-number">1.2</span>
    Geltungsbereich](#geltungsbereich)
  - [<span class="toc-section-number">1.3</span> Wir können Untertitel
    haben](#wir-können-untertitel-haben)
- [<span class="toc-section-number">2</span> Technische
  Hinweise](#technische-hinweise)
- [<span class="toc-section-number">3</span> Datenmodell](#datenmodell)
  - [<span class="toc-section-number">3.1</span> Genre](#sec-genre)
  - [<span class="toc-section-number">3.2</span>
    Musikalbum](#sec-musikalbum)
  - [<span class="toc-section-number">3.3</span>
    Musikaufnahme](#sec-musikaufnahme)
  - [<span class="toc-section-number">3.4</span>
    Organisation](#sec-organisation)
  - [<span class="toc-section-number">3.5</span> Person](#sec-person)
  - [<span class="toc-section-number">3.6</span> Quantitativer
    Wert](#sec-quantitativer-wert)
  - [<span class="toc-section-number">3.7</span>
    Rechnung](#sec-rechnung)
- [<span class="toc-section-number">4</span> Datenbezug](#datenbezug)
- [<span class="toc-section-number">5</span>
  Sicherheitsaspekte](#sicherheitsaspekte)
- [<span class="toc-section-number">6</span>
  Haftungsausschluss](#haftungsausschluss)
- [<span class="toc-section-number">7</span>
  Urheberrechte](#urheberrechte)
- [<span class="toc-section-number">8</span> Anhang A -
  Referenzen](#anhang-a---referenzen)
- [<span class="toc-section-number">9</span> Anhang B - Mitwirkung &
  Prüfung](#anhang-b---mitwirkung--prüfung)
- [<span class="toc-section-number">10</span> Anhang C - Abkürzungen und
  Glossar](#anhang-c---abkürzungen-und-glossar)
- [<span class="toc-section-number">11</span> Anhang D - Änderungen
  gegenüber der
  Vorversion](#anhang-d---änderungen-gegenüber-der-vorversion)
- [<span class="toc-section-number">12</span> Anhang E -
  Abbildungsverzeichnis](#anhang-e---abbildungsverzeichnis)
- [<span class="toc-section-number">13</span> Anhang F -
  Tabellenverzeichnis](#anhang-f---tabellenverzeichnis)

# Hinweis

Im vorliegenden Dokument wird bei der Bezeichnung von Personen eine
geschlechtsneutrale Formulierung verwendet. Basis bildet der Leitfaden
der Bundeskanzlei. Je nach Situation kommen Paarformen (Bürgerinnen und
Bürger), geschlechtsabstrakte Formen (versicherte Person),
geschlechtsneutrale Formen (Versicherte) oder Umschreibungen ohne
Personenbezug zum Einsatz. Das generische Maskulin (Bürger) ist nicht
zulässig. Vollformen werden in fortlaufenden Texten verwendet, also in
Texten, die aus ausformulierten Sätzen bestehen. In verknappten
Textpassagen, namentlich in Tabellen, können Kurzformen verwendet
werden. Dabei wird die Kurzform mit Schrägstrich, aber ohne
Auslassungsstrich verwendet (Referent/in). Genderstern und ähnliche
Schreibweisen werden nicht verwendet.

# Einleitung

## Status

Genehmigt: Dieses Dokument wurde vom Fach-Ausschuss verabschiedet. Es
entfaltet normative Kraft für den definierten Anwendungsbereich im
festgelegten Geltungsbereich.

## Geltungsbereich

Die Angaben in diesem Kapitel sollen dem Leser einen raschen Überblick
geben, wofür dieser Standard gedacht ist. Hinweise zu folgenden
Sachverhalten können dabei hilfreich sein.

## Wir können Untertitel haben

Und etwas Text schreiben.

### Auch Unter-Unterüberschriften

Und noch mehr Text schreiben. Vielleicht sogar mit einem schönen Bild.

<div id="fig-example">

![](https://fastly.picsum.photos/id/653/536/354.jpg?hmac=3InR8I5KmwbdkPHehlM8BMPd_BDHG_RWZkxt_IkeQGY)

Abbildung 1: Fügen Sie immer etwas Text hinzu, um zu beschreiben, was
das Bild zeigt.

</div>

Bei der Darstellung von Diagrammen sollte versucht werden, diese direkt
in Mermaid JS zu erstellen; dies macht zukünftige Änderungen oder
Übersetzungen sehr einfach.

# Technische Hinweise

Wir verwenden die ROBOT CLI in unserem Projekt (Jackson u. a. 2019),
insbesondere wegen ihrer Fähigkeit, den HermiT Reasoner auszuführen
(Glimm u. a. 2014).

# Datenmodell

## Genre

Eine musikalische Kategorie im Chinook-Datensatz.

**Zielklasse:** `:Genre`

<div id="tbl-genre">

Tabelle 1: Eigenschaften Genre

| Beschreibung | Pfad | Typ | Kardinalität |
|:---|:---|:---|---:|
| **Name** | `schema:name` |  | 1..1 |
| **Teil von** | `schema:partOf` | [`:Genre`](#sec-genre) oder `sh:IRI` | 0..\* |

</div>

## Musikalbum

Eine Sammlung von Titeln im Chinook-Datensatz.

**Zielklasse:** `schema:MusicAlbum`

<div id="tbl-musikalbum">

Tabelle 2: Eigenschaften Musikalbum

| Beschreibung | Pfad | Typ | Kardinalität |
|:---|:---|:---|---:|
| **Name**: Jedes Album muss einen Namen haben. | `schema:name` | `xsd:string` | 1..1 |
| **Künstler**: Person oder Musikgruppe, die das Album erstellt hat. | `schema:byArtist` | [`schema:Person`](#sec-person) oder `schema:MusicGroup` | 0..\* |

</div>

## Musikaufnahme

Ein einzelner Musiktitel im Chinook-Datensatz.

**Zielklasse:** `schema:MusicRecording`

<div id="tbl-musikaufnahme">

Tabelle 3: Eigenschaften Musikaufnahme

| Beschreibung | Pfad | Typ | Kardinalität |
|:---|:---|:---|---:|
| **Name**: Jeder Titel muss einen Namen haben. | `schema:name` | `xsd:string` | 1..1 |
| **In Album**: Ein Titel kann nur zu einem gültigen schema:MusicAlbum gehören. | `schema:inAlbum` | [`schema:MusicAlbum`](#sec-musikalbum) | 0..\* |
| **Autor**: Die Person oder Gruppe, die den Titel geschrieben hat. | `schema:author` |  | 0..\* |
| **Genre** | `schema:genre` | [`:Genre`](#sec-genre) | 1..1 |
| **Dauer**: Die Dauer muss als schema:QuantitativeValue ausgedrückt werden. | `schema:duration` | [`schema:QuantitativeValue`](#sec-quantitativer-wert) | 0..\* |
| **Dateigröße** | `schema:contentSize` | [`schema:QuantitativeValue`](#sec-quantitativer-wert) | 0..\* |

</div>

## Organisation

Ein Unternehmen oder eine Organisation im Chinook-Datensatz.

**Zielklasse:** `schema:Organisation`

<div id="tbl-organisation">

Tabelle 4: Eigenschaften Organisation

| Beschreibung | Pfad | Typ | Kardinalität |
|:---|:---|:---|---:|
| **Name**: Jede Organisation muss einen Namen haben. | `schema:name` | `xsd:string` | 1..1 |

</div>

## Person

Jede Person (Mitarbeiter, Kunde oder benutzerdefinierte Person) im
Datensatz.

**Zielklasse:** `schema:Person`

<div id="tbl-person">

Tabelle 5: Eigenschaften Person

| Beschreibung | Pfad | Typ | Kardinalität |
|:---|:---|:---|---:|
| **Vorname**: Jede Person muss einen Vornamen haben. | `schema:givenName` | `xsd:string` | 1..1 |
| **Nachname**: Jede Person muss einen Nachnamen haben. | `schema:familyName` | `xsd:string` | 1..1 |
| **E-Mail-Adresse**: Falls angegeben, muss die E-Mail-Adresse einem Standardformat entsprechen. | `schema:email` | `xsd:string` | 0..\* |
| **Geburtsdatum**: Eine Person sollte ein gültiges Geburtsdatum haben. | `schema:birthDate` | `xsd:date` | 0..\* |
| **Adresse** | `schema:address` | `schema:PostalAddress` | 0..\* |
| **Arbeitet für**: Ein Mitarbeiter kann einer anderen Person unterstellt sein. | `schema:worksFor` | [`schema:Person`](#sec-person) oder `schema:Organization` | 0..\* |
| **Berufsbezeichnung** | `schema:jobTitle` |  | 0..1 |
| **Kennt** | `schema:knows` | [`schema:Person`](#sec-person) | 0..\* |

</div>

## Quantitativer Wert

Ein numerischer Wert mit einer dazugehörigen Einheit.

**Zielklasse:** `schema:QuantitativeValue`

<div id="tbl-quantitativer-wert">

Tabelle 6: Eigenschaften Quantitativer Wert

| Beschreibung | Pfad | Typ | Kardinalität |
|:---|:---|:---|---:|
| **Wert**: Ein quantitativer Wert muss genau einen numerischen Wert haben. | `schema:value` |  | 1..1 |
| **Einheitencode**: Ein quantitativer Wert muss seine Einheit über eine unitCode-URI angeben. | `schema:unitCode` | `sh:IRI` | 1..1 |

</div>

## Rechnung

Ein Kaufbeleg im Chinook-Datensatz.

**Zielklasse:** `schema:Invoice`

<div id="tbl-rechnung">

Tabelle 7: Eigenschaften Rechnung

| Beschreibung | Pfad | Typ | Kardinalität |
|:---|:---|:---|---:|
| **Kunde**: Eine Rechnung muss genau einem Kunden zugeordnet sein. | `schema:customer` | [`schema:Person`](#sec-person) | 1..1 |
| **Fälliger Gesamtbetrag**: Eine Rechnung muss einen fälligen Gesamtbetrag als schema:QuantitativeValue definieren. | `schema:totalPaymentDue` | [`schema:QuantitativeValue`](#sec-quantitativer-wert) | 1..1 |
| **Enthält**: Eine Rechnung muss mindestens eine Position (OrderItem) enthalten. | `schema:hasPart` | `schema:OrderItem` | 1..\* |
| **Erstellungsdatum** | `schema:dateCreated` | `xsd:date` | 0..\* |

</div>

# Datenbezug

Die diesem Dokument zugrundeliegenden Master- und Referenzdaten sind als
*Linked Data* verfügbar.

Die technologische Basis dafür bildet das [Resource Description
Framework (RDF)](https://www.w3.org/TR/rdf11-concepts/), ein zentraler
Standard des World Wide Web Consortiums (W3C) zur Modellierung von
Datenstrukturen im Web. In RDF werden Informationen nicht in klassischen
Tabellen, sondern als vernetzte Graphen abgebildet. Jede Aussage besteht
dabei aus einem sogenannten Triple (Subjekt, Prädikat, Objekt). Diese
Struktur ermöglicht eine maschinenlesbare, interoperable und
systemübergreifend eindeutige Beschreibung von Ressourcen und deren
Relationen zueinander.

Für die Speicherung und Publikation dieser RDF-Daten wird
[LINDAS](https://lindas.admin.ch/) (Linked Data Service) genutzt, der
offizielle Linked-Data-Dienst der Schweizer Bundesverwaltung. LINDAS
fungiert als sogenannter *Triple Store*, einer spezialisierte
Graphdatenbank, die für das effiziente Speichern und Abfragen von
RDF-Triples optimiert ist und die Daten öffentlich über eine genormte
Schnittstelle bereitstellt.

Das folgende Kapitel gibt eine minimale Anleitung, wie die Daten von
LINDAS abgefragt und bezogen werden können.

``` rq
BASE <https://example.org/>
PREFIX schema: <http://schema.org/>
SELECT *
WHERE {
    ?genre a <Genre> ;
        schema:name ?name .
}
LIMIT 10
```

Die zugrundeliegenden Daten selbst werden auf GitHub als Turtle-Files
gepflegt.

``` ttl
@base <http://example.org/> .
@prefix genre: <http://example.org/genre/> .
@prefix schema: <http://schema.org/> .

genre:1 a <Genre> ;
    schema:name "Rock" .

genre:2 a <Genre> ;
    schema:name "Jazz" .

genre:3 a <Genre> ;
    schema:name "Metal" ;
    schema:partOf genre:1 .
```

# Sicherheitsaspekte

Informationen zu den ausdrücklich massgeblichen rechtlichen Grundlagen
oder ein Hinweis darauf, dass bei der Umsetzung die entsprechenden
rechtlichen Grundlagen zu beachten sind.

# Haftungsausschluss

eCH-Standards, die der Verein eCH dem Anwender kostenlos zur Verfügung
stellt oder die auf eCH verweisen, haben nur den Status von
Empfehlungen. Der Verein eCH haftet in keinem Fall für Entscheidungen
oder Massnahmen, die der Anwender auf der Grundlage dieser Dokumente
trifft bzw. ergreift. Der Anwender ist dafür verantwortlich, die
Dokumente vor ihrer Verwendung selbst zu überprüfen und gegebenenfalls
fachlichen Rat einzuholen. eCH-Standards können und sollen die
technische, organisatorische oder rechtliche Beratung im Einzelfall
nicht ersetzen.

Dokumente, Verfahren, Methoden, Produkte und Standards, auf die in
eCH-Standards verwiesen wird, sind möglicherweise durch Marken-,
Urheber- oder Patentrechte geschützt. Es liegt in der ausschliesslichen
Verantwortung des Anwenders, die erforderlichen Lizenzen von den
berechtigten Personen und/oder Organisationen einzuholen.

Obwohl der Verein eCH bei der Erstellung der eCH-Standards mit
angemessener Sorgfalt vorgegangen ist, kann er keine Gewährleistung oder
Garantie dafür übernehmen, dass die bereitgestellten Informationen und
Dokumente aktuell, vollständig, richtig oder fehlerfrei sind. eCH behält
sich das Recht vor, die Inhalte der eCH-Standards jederzeit und ohne
vorherige Ankündigung zu ändern.

Jede Haftung für Schäden, die durch die Nutzung der eCH-Standards durch
den Anwender entstehen, wird im gesetzlich zulässigen Rahmen
ausgeschlossen.

# Urheberrechte

Personen, die eCH-Standards erarbeiten, bleiben Inhaber ihrer geistigen
Eigentumsrechte. Diese Personen verpflichten sich jedoch, ihre geistigen
Eigentumsrechte oder andere Rechte an geistigen Eigentumsrechten
Dritter, soweit möglich, den jeweiligen Fachgruppen und dem Verein eCH
kostenlos und zur uneingeschränkten Nutzung und Weiterentwicklung im
Rahmen des Vereinszwecks zur Verfügung zu stellen.

Die von den Fachgruppen erarbeiteten Standards dürfen unter Nennung des
jeweiligen Autors von eCH kostenlos und in uneingeschränktem Umfang
genutzt, verbreitet und weiterentwickelt werden.

eCH-Standards sind vollständig dokumentiert und frei von lizenz-
und/oder patentrechtlichen Einschränkungen. Die dazugehörige
Dokumentation kann kostenlos angefordert werden. Diese Bestimmungen
gelten jedoch nur für die von eCH erarbeiteten Standards, nicht aber für
Standards oder Produkte Dritter, die auf eCH-Standards verweisen. Die
Standards enthalten die entsprechenden Hinweise auf Rechte Dritter.

# Anhang A - Referenzen

<div id="refs" class="references csl-bib-body hanging-indent">

<div id="ref-glimm2014hermit" class="csl-entry">

Glimm, Birte, Ian Horrocks, Boris Motik, Giorgos Stoilos, und Zhe Wang.
2014. „HermiT: an OWL 2 reasoner“. *Journal of automated reasoning* 53
(3): 245–69.

</div>

<div id="ref-jackson2019robot" class="csl-entry">

Jackson, Rebecca C, James P Balhoff, Eric Douglass, Nomi L Harris,
Christopher J Mungall, und James A Overton. 2019. „ROBOT: a tool for
automating ontology workflows“. *BMC bioinformatics* 20 (1): 407.

</div>

</div>

# Anhang B - Mitwirkung & Prüfung

# Anhang C - Abkürzungen und Glossar

# Anhang D - Änderungen gegenüber der Vorversion

# Anhang E - Abbildungsverzeichnis

# Anhang F - Tabellenverzeichnis
