# eCH-1234 Quarto-Dokument als Vorlage

12. August 2026

- [Hinweis](#hinweis)
- [<span class="toc-section-number">1</span> Einleitung](#einleitung)
  - [<span class="toc-section-number">1.1</span> Status](#status)
  - [<span class="toc-section-number">1.2</span>
    Geltungsbereich](#geltungsbereich)
  - [<span class="toc-section-number">1.3</span> Wir können Untertitel
    haben](#wir-können-untertitel-haben)
    - [<span class="toc-section-number">1.3.1</span> Auch
      Unter-Unterüberschriften](#auch-unter-unterüberschriften)
- [<span class="toc-section-number">2</span> Technische
  Hinweise](#technische-hinweise)
- [<span class="toc-section-number">3</span> Datenmodell](#datenmodell)
  - [<span class="toc-section-number">3.1</span>
    :GenreShape](#sec-genreshape)
  - [<span class="toc-section-number">3.2</span>
    :InvoiceShape](#sec-invoiceshape)
  - [<span class="toc-section-number">3.3</span>
    :MusicAlbumShape](#sec-musicalbumshape)
  - [<span class="toc-section-number">3.4</span>
    :OrganisationShape](#sec-organisationshape)
  - [<span class="toc-section-number">3.5</span>
    :PersonShape](#sec-personshape)
  - [<span class="toc-section-number">3.6</span>
    :QuantitativeValueShape](#sec-quantitativevalueshape)
  - [<span class="toc-section-number">3.7</span>
    :TrackShape](#sec-trackshape)
- [<span class="toc-section-number">4</span>
  Sicherheitsaspekte](#sicherheitsaspekte)
- [<span class="toc-section-number">5</span>
  Haftungsausschluss](#haftungsausschluss)
- [<span class="toc-section-number">6</span>
  Urheberrechte](#urheberrechte)
- [<span class="toc-section-number">7</span> Anhang A -
  Referenzen](#anhang-a---referenzen)
- [<span class="toc-section-number">8</span> Anhang B - Mitwirkung &
  Prüfung](#anhang-b---mitwirkung--prüfung)
- [<span class="toc-section-number">9</span> Anhang C - Abkürzungen und
  Glossar](#anhang-c---abkürzungen-und-glossar)
- [<span class="toc-section-number">10</span> Anhang D - Änderungen
  gegenüber der
  Vorversion](#anhang-d---änderungen-gegenüber-der-vorversion)
- [<span class="toc-section-number">11</span> Anhang E -
  Abbildungsverzeichnis](#anhang-e---abbildungsverzeichnis)
- [<span class="toc-section-number">12</span> Anhang F -
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

## :GenreShape

**Zielklasse:** `:Genre`

<div id="tbl-genreshape">

Tabelle 1: :GenreShape Eigenschaften

| Beschreibung | Pfad | Typ | Kardinalität |
|:---|:---|:---|---:|
|  | `schema:name` |  | 1..1 |
|  | `schema:partOf` | [:Genre](#sec-genreshape) oder `sh:IRI` | 0..\* |

</div>

## :InvoiceShape

**Zielklasse:** `schema:Invoice`

<div id="tbl-invoiceshape">

Tabelle 2: :InvoiceShape Eigenschaften

| Beschreibung | Pfad | Typ | Kardinalität |
|:---|:---|:---|---:|
| An invoice must be linked to exactly one customer. | `schema:customer` | [schema:Person](#sec-personshape) | 1..1 |
| An invoice must define a total payment due as a schema:QuantitativeValue. | `schema:totalPaymentDue` | [schema:QuantitativeValue](#sec-quantitativevalueshape) | 1..1 |
| An invoice must have at least one line item (OrderItem). | `schema:hasPart` | `schema:OrderItem` | 1..\* |
|  | `schema:dateCreated` | `xsd:date` | 0..\* |

</div>

## :MusicAlbumShape

**Zielklasse:** `schema:MusicAlbum`

<div id="tbl-musicalbumshape">

Tabelle 3: :MusicAlbumShape Eigenschaften

| Beschreibung | Pfad | Typ | Kardinalität |
|:---|:---|:---|---:|
| Every album must have a name. | `schema:name` | `xsd:string` | 1..1 |
|  | `schema:byArtist` | [schema:Person](#sec-personshape) oder `schema:MusicGroup` | 0..\* |

</div>

## :OrganisationShape

**Zielklasse:** `schema:Organisation`

<div id="tbl-organisationshape">

Tabelle 4: :OrganisationShape Eigenschaften

| Beschreibung | Pfad | Typ | Kardinalität |
|:---|:---|:---|---:|
| Every organisation must have a name. | `schema:name` | `xsd:string` | 1..1 |

</div>

## :PersonShape

**Zielklasse:** `schema:Person`

<div id="tbl-personshape">

Tabelle 5: :PersonShape Eigenschaften

| Beschreibung | Pfad | Typ | Kardinalität |
|:---|:---|:---|---:|
| Every person must have a given name. | `schema:givenName` | `xsd:string` | 1..1 |
| Every person must have a family name. | `schema:familyName` | `xsd:string` | 1..1 |
| If an email is provided, it must follow a standard email format. | `schema:email` | `xsd:string` | 0..\* |
| A person should have a valid birth date. | `schema:birthDate` | `xsd:date` | 0..\* |
|  | `schema:address` | `schema:PostalAddress` | 0..\* |
| An employee can report to another person. | `schema:worksFor` | [schema:Person](#sec-personshape) oder `schema:Organization` | 0..\* |
|  | `schema:jobTitle` |  | 0..1 |
|  | `schema:knows` | [schema:Person](#sec-personshape) | 0..\* |

</div>

## :QuantitativeValueShape

**Zielklasse:** `schema:QuantitativeValue`

<div id="tbl-quantitativevalueshape">

Tabelle 6: :QuantitativeValueShape Eigenschaften

| Beschreibung | Pfad | Typ | Kardinalität |
|:---|:---|:---|---:|
| A quantitative value must have exactly one numeric value. | `schema:value` |  | 1..1 |
| A quantitative value must specify its unit via a unitCode URI. | `schema:unitCode` | `sh:IRI` | 1..1 |

</div>

## :TrackShape

**Zielklasse:** `schema:MusicRecording`

<div id="tbl-trackshape">

Tabelle 7: :TrackShape Eigenschaften

| Beschreibung | Pfad | Typ | Kardinalität |
|:---|:---|:---|---:|
| Every track must have a name. | `schema:name` | `xsd:string` | 1..1 |
| A track can only belong to a valid schema:MusicAlbum. | `schema:inAlbum` | [schema:MusicAlbum](#sec-musicalbumshape) | 0..\* |
|  | `schema:author` |  | 0..\* |
|  | `schema:genre` | [:Genre](#sec-genreshape) | 1..1 |
| Track duration must be expressed as a schema:QuantitativeValue. | `schema:duration` | [schema:QuantitativeValue](#sec-quantitativevalueshape) | 0..\* |
|  | `schema:contentSize` | [schema:QuantitativeValue](#sec-quantitativevalueshape) | 0..\* |

</div>

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
