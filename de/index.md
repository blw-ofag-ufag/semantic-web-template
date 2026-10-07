# Quarto-Dokument als Vorlage

2026-10-01

- [<span class="toc-section-number">1</span>
  Einleitung](#sec-introduction)
  - [<span class="toc-section-number">1.1</span> Status](#sec-status)
  - [<span class="toc-section-number">1.2</span>
    Geltungsbereich](#sec-scope-of-application)
  - [<span class="toc-section-number">1.3</span> Wir können Untertitel
    haben](#sec-example-subheading)
  - [<span class="toc-section-number">1.4</span>
    Formatierungen](#sec-formatting)
- [<span class="toc-section-number">2</span> Hinweise zur
  Verwendung](#sec-usage-notes)
  - [<span class="toc-section-number">2.1</span>
    Namespaces](#sec-namespaces)
- [<span class="toc-section-number">3</span>
  Datenmodell](#sec-data-model)
  - [<span class="toc-section-number">3.1</span>
    Genre](#sec-nodeshape-genreshape)
  - [<span class="toc-section-number">3.2</span>
    Musikalbum](#sec-nodeshape-musicalbumshape)
  - [<span class="toc-section-number">3.3</span>
    Musikaufnahme](#sec-nodeshape-trackshape)
  - [<span class="toc-section-number">3.4</span>
    Organisation](#sec-nodeshape-organisationshape)
  - [<span class="toc-section-number">3.5</span>
    Person](#sec-nodeshape-personshape)
  - [<span class="toc-section-number">3.6</span>
    Postadresse](#sec-nodeshape-postaladdressshape)
  - [<span class="toc-section-number">3.7</span> Quantitativer
    Wert](#sec-nodeshape-quantitativevalueshape)
  - [<span class="toc-section-number">3.8</span>
    Rechnung](#sec-nodeshape-invoiceshape)
- [<span class="toc-section-number">4</span>
  Datenbezug](#sec-data-retrieval)
- [<span class="toc-section-number">5</span>
  Sicherheitsaspekte](#sec-safety-consideration)
- [<span class="toc-section-number">6</span>
  Haftungsausschluss](#sec-disclaimer)
- [<span class="toc-section-number">7</span>
  Urheberrechte](#sec-copyrights)
- [Anhang A – Referenzen](#sec-appendix-a)
- [Anhang B – Mitwirkung und Prüfung](#sec-appendix-b)
- [Anhang C – Abkürzungen und Glossar](#sec-appendix-c)
- [Anhang D – Änderungen gegenüber der Vorversion](#sec-appendix-d)
- [Anhang E – Abbildungsverzeichnis](#sec-appendix-e)
- [Anhang F – Tabellenverzeichnis](#sec-appendix-f)

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

In Arbeit: Der Gebrauch ist nur innerhalb der Fachgruppe,
beziehungsweise im Expertenausschuss zugelassen.

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
das Bild zeigt. Hat eine Abbildung eine Beschriftung, erscheint sie im
Abbildungsverzeichnis. Dort wird nur der erste Satz der Beschriftung
angezeigt.

</div>

Bei der Darstellung von Diagrammen sollte versucht werden, diese direkt
in Mermaid JS zu erstellen; dies macht zukünftige Änderungen oder
Übersetzungen sehr einfach.

## Formatierungen

Dieses Kapitel ist ein Stresstest: Es enthält die gängigen Markdown- und
Quarto-Elemente, damit ihre Darstellung in PDF und Website geprüft
werden kann.

### Textauszeichnungen

Text kann **fett**, *kursiv*, <u>unterstrichen</u>,
<span class="mark">markiert</span>, <span class="smallcaps">in
Kapitälchen</span> oder ~~durchgestrichen~~ gesetzt werden. Tastenkürzel
wie `Ctrl-C` + `Ctrl-V` und Inline-Code wie `schema:name` werden
speziell hervorgehoben.[^1]

#### Eine Überschrift vierter Stufe

Überschriften bis zur vierten Stufe sind möglich; sie werden nummeriert,
erscheinen aber nicht im Inhaltsverzeichnis.[^2]

### Listen und Hinweise

Ungeordnete Liste:

- Erster Punkt
- Zweiter Punkt
  - Unterpunkt
- Dritter Punkt

Geordnete Liste:

1.  Erster Schritt
2.  Zweiter Schritt
3.  Dritter Schritt

> [!NOTE]
>
> Ein Hinweis macht auf Zusammenhänge aufmerksam, die leicht übersehen
> werden.

> [!WARNING]
>
> Eine Warnung weist auf Fehlerquellen hin, zum Beispiel auf ungeprüfte
> Eingabedaten.

### Code, Tabellen und Formeln

Der folgende Codeblock zeigt eine SPARQL-Abfrage:

``` sparql
SELECT ?s ?p ?o
WHERE {
  ?s ?p ?o .
}
LIMIT 10
```

<div id="tbl-example">

Tabelle 1: Beispieltabelle mit drei Spalten. Hat eine Tabelle eine
Beschriftung, erscheint sie im Tabellenverzeichnis. Dort wird nur der
erste Satz der Beschriftung angezeigt.

| Spalte | Typ          | Bemerkung   |
|:-------|:-------------|:------------|
| Name   | Zeichenkette | Pflichtfeld |
| Menge  | Dezimalzahl  | mit Einheit |

</div>

Eine Formel kann im Text stehen, etwa $E = m c^2$, oder als eigene
Gleichung wie <a href="#eq-example" class="quarto-xref">Gleichung 1</a>:

<span id="eq-example">$$
\sum_{i=1}^{n} x_i = n \bar{x}
 \qquad(1)$$</span>

# Hinweise zur Verwendung

Der folgende Absatz ist bewusst Unsinn und dient nur dem Test der
Zitierweise: Gemäss dem Genehmigungsleitfaden \[eCH-0003 11.1.0\] müssen
alle Postadressen \[eCH-0010 8.1.0\] in Turtle \[Turtle\] serialisiert,
als DCAT-Katalog \[DCAT; eCH-0200 3.0.1\] mit SHACL \[SHACL\] geprüft
und per SPARQL \[SPARQL\] als Linked Open Data \[eCH-0205 1.0\] über
landwirtschaftliche Kulturen \[eCH-0265 1.0.0\] in JSON-LD \[JSON-LD\]
und OWL \[OWL 2\] veröffentlicht werden, wie es das Semantic Web
\[Berners-Lee 2023\] vorsieht.

## Namespaces

<a href="#tbl-namespaces" class="quarto-xref">Tabelle 2</a> listet die
Präfixe und Namespaces, die in diesem Dokument verwendet werden. Ein
Präfix steht stellvertretend für eine Namespace-IRI, den gemeinsamen
Anfang der IRIs eines Vokabulars. Die Turtle-Spezifikation beschreibt,
wie solche [*Prefixed
Names*](https://www.w3.org/TR/turtle/#prefixed-name) aufgelöst werden
\[Turtle\].

<div id="tbl-namespaces">

Tabelle 2: In eCH-1234 – Quarto-Dokument als Vorlage verwendete
Namespaces.

| Präfix   | Namespace                                   |
|:---------|:--------------------------------------------|
| :        | https://agriculture.ld.admin.ch/eCH-1234/2/ |
| country: | https://ld.admin.ch/country/                |
| rdf:     | http://www.w3.org/1999/02/22-rdf-syntax-ns# |
| schema:  | http://schema.org/                          |
| unit:    | http://qudt.org/vocab/unit/                 |
| xsd:     | http://www.w3.org/2001/XMLSchema#           |

</div>

# Datenmodell

## Genre

Eine musikalische Kategorie im Chinook-Datensatz.

### Übersicht

<div class="ech-facts">

Shape  
[:GenreShape](https://agriculture.ld.admin.ch/eCH-1234/2/GenreShape)

Zielklasse  
[:Genre](https://agriculture.ld.admin.ch/eCH-1234/2/Genre)

Geschlossen  
Ja (nur die aufgeführten Eigenschaften zulässig)

Kennzahlen  
25 Instanzen mit je 5 bis 7 Tripeln (im Mittel 5.4)

Datenzugriff  
[SPARQL-Dienst](https://lindas.admin.ch/sparql/#query=PREFIX%20%3A%20%3Chttps%3A%2F%2Fagriculture.ld.admin.ch%2FeCH-1234%2F2%2F%3E%0APREFIX%20schema%3A%20%3Chttp%3A%2F%2Fschema.org%2F%3E%0ASELECT%20%3Firi%20%3Fname%20%3FpartOf%20%3FalternateName%0AFROM%20%3Chttps%3A%2F%2Flindas.admin.ch%2Ffoag%2Fogd%3E%0AWHERE%20%7B%0A%20%20%3Firi%20a%20%3AGenre%20.%0A%20%20%3Firi%20schema%3Aname%20%3Fname%20.%0A%20%20OPTIONAL%20%7B%20%3Firi%20schema%3ApartOf%20%3FpartOf%20.%20%7D%0A%20%20OPTIONAL%20%7B%20%3Firi%20schema%3AalternateName%20%3FalternateName%20.%20%7D%0A%7D%0ALIMIT%201000)

</div>

### Eigenschaften

<table style="width:99%;">
<colgroup>
<col style="width: 39%" />
<col style="width: 49%" />
<col style="width: 9%" />
</colgroup>
<thead>
<tr>
<th style="text-align: left;">Beschreibung</th>
<th style="text-align: left;">Details</th>
<th style="text-align: right;">Kardinalität</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: left;"><strong>Name</strong> (<a
href="http://schema.org/name">schema:name</a>)</td>
<td style="text-align: left;"><ul>
<li>Typ: Zeichenkette (<a
href="http://www.w3.org/2001/XMLSchema#string">xsd:string</a>)</li>
<li>Muster: <code>^[A-Z]</code></li>
<li>Länge: 2–50 Zeichen</li>
</ul></td>
<td style="text-align: right;">1..1</td>
</tr>
<tr>
<td style="text-align: left;"><strong>Teil von</strong> (<a
href="http://schema.org/partOf">schema:partOf</a>)</td>
<td style="text-align: left;"><ul>
<li>Typ: <a href="#sec-nodeshape-genreshape">Genre</a></li>
</ul></td>
<td style="text-align: right;">0..*</td>
</tr>
<tr>
<td style="text-align: left;"><strong>Alternative Bezeichnung</strong>
(<a href="http://schema.org/alternateName">schema:alternateName</a>):
Übersetzte oder umgangssprachliche Bezeichnung des Genres, höchstens
eine pro Sprache.</td>
<td style="text-align: left;"><ul>
<li>Typ: Sprachabhängiger Text (<a
href="http://www.w3.org/1999/02/22-rdf-syntax-ns#langString">rdf:langString</a>)</li>
<li>Länge: ≤ 50 Zeichen</li>
<li>Sprachen: <code>de</code>, <code>fr</code>, <code>it</code>,
<code>en</code> (eine pro Sprache)</li>
</ul></td>
<td style="text-align: right;">0..*</td>
</tr>
</tbody>
</table>

### Regeln (SPARQL)

#### Keine zyklische Hierarchie

Ein Genre darf weder direkt noch transitiv ein Teil von sich selbst
sein.

``` sparql
SELECT $this
WHERE {
    $this schema:partOf+ $this .
}
```

## Musikalbum

Eine Sammlung von Titeln im Chinook-Datensatz.

### Übersicht

<div class="ech-facts">

Shape  
[:MusicAlbumShape](https://agriculture.ld.admin.ch/eCH-1234/2/MusicAlbumShape)

Zielklasse  
[schema:MusicAlbum](http://schema.org/MusicAlbum)

Geschlossen  
Nein (weitere Eigenschaften zulässig)

Kennzahlen  
347 Instanzen mit je 5 Tripeln

Datenzugriff  
[SPARQL-Dienst](https://lindas.admin.ch/sparql/#query=PREFIX%20schema%3A%20%3Chttp%3A%2F%2Fschema.org%2F%3E%0ASELECT%20%3Firi%20%3Fname%20%3FbyArtist%0AFROM%20%3Chttps%3A%2F%2Flindas.admin.ch%2Ffoag%2Fogd%3E%0AWHERE%20%7B%0A%20%20%3Firi%20a%20schema%3AMusicAlbum%20.%0A%20%20%3Firi%20schema%3Aname%20%3Fname%20.%0A%20%20OPTIONAL%20%7B%20%3Firi%20schema%3AbyArtist%20%3FbyArtist%20.%20%7D%0A%7D%0ALIMIT%201000)

</div>

### Eigenschaften

<table style="width:99%;">
<colgroup>
<col style="width: 40%" />
<col style="width: 46%" />
<col style="width: 12%" />
</colgroup>
<thead>
<tr>
<th style="text-align: left;">Beschreibung</th>
<th style="text-align: left;">Details</th>
<th style="text-align: right;">Kardinalität</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: left;"><strong>Name</strong> (<a
href="http://schema.org/name">schema:name</a>): Jedes Album muss einen
Namen haben.</td>
<td style="text-align: left;"><ul>
<li>Typ: Zeichenkette (<a
href="http://www.w3.org/2001/XMLSchema#string">xsd:string</a>)</li>
<li>Länge: ≤ 200 Zeichen</li>
</ul></td>
<td style="text-align: right;">1..1</td>
</tr>
<tr>
<td style="text-align: left;"><strong>Künstler</strong> (<a
href="http://schema.org/byArtist">schema:byArtist</a>): Person oder
Musikgruppe, die das Album erstellt hat.</td>
<td style="text-align: left;"><ul>
<li>Typ: <a href="#sec-nodeshape-personshape">Person</a> oder <a
href="http://schema.org/MusicGroup">schema:MusicGroup</a></li>
</ul></td>
<td style="text-align: right;">0..*</td>
</tr>
</tbody>
</table>

## Musikaufnahme

Ein einzelner Musiktitel im Chinook-Datensatz.

### Übersicht

<div class="ech-facts">

Shape  
[:TrackShape](https://agriculture.ld.admin.ch/eCH-1234/2/TrackShape)

Zielklasse  
[schema:MusicRecording](http://schema.org/MusicRecording)

Geschlossen  
Nein (weitere Eigenschaften zulässig)

Kennzahlen  
3503 Instanzen mit je 10 bis 15 Tripeln (im Mittel 11.1)

Datenzugriff  
[SPARQL-Dienst](https://lindas.admin.ch/sparql/#query=PREFIX%20schema%3A%20%3Chttp%3A%2F%2Fschema.org%2F%3E%0ASELECT%20%3Firi%20%3Fname%20%3FinAlbum%20%3Fauthor%20%3Fgenre%20%3Fduration%20%3FcontentSize%0AFROM%20%3Chttps%3A%2F%2Flindas.admin.ch%2Ffoag%2Fogd%3E%0AWHERE%20%7B%0A%20%20%3Firi%20a%20schema%3AMusicRecording%20.%0A%20%20%3Firi%20schema%3Aname%20%3Fname%20.%0A%20%20OPTIONAL%20%7B%20%3Firi%20schema%3AinAlbum%20%3FinAlbum%20.%20%7D%0A%20%20OPTIONAL%20%7B%20%3Firi%20schema%3Aauthor%20%3Fauthor%20.%20%7D%0A%20%20%3Firi%20schema%3Agenre%20%3Fgenre%20.%0A%20%20OPTIONAL%20%7B%20%3Firi%20schema%3Aduration%20%3Fduration%20.%20%7D%0A%20%20OPTIONAL%20%7B%20%3Firi%20schema%3AcontentSize%20%3FcontentSize%20.%20%7D%0A%7D%0ALIMIT%201000)

</div>

### Eigenschaften

<table style="width:99%;">
<colgroup>
<col style="width: 43%" />
<col style="width: 44%" />
<col style="width: 11%" />
</colgroup>
<thead>
<tr>
<th style="text-align: left;">Beschreibung</th>
<th style="text-align: left;">Details</th>
<th style="text-align: right;">Kardinalität</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: left;"><strong>Name</strong> (<a
href="http://schema.org/name">schema:name</a>): Jeder Titel muss einen
Namen haben.</td>
<td style="text-align: left;"><ul>
<li>Typ: Zeichenkette (<a
href="http://www.w3.org/2001/XMLSchema#string">xsd:string</a>)</li>
<li>Länge: 1–200 Zeichen</li>
</ul></td>
<td style="text-align: right;">1..1</td>
</tr>
<tr>
<td style="text-align: left;"><strong>In Album</strong> (<a
href="http://schema.org/inAlbum">schema:inAlbum</a>): Ein Titel kann nur
zu einem gültigen schema:MusicAlbum gehören.</td>
<td style="text-align: left;"><ul>
<li>Typ: <a href="#sec-nodeshape-musicalbumshape">Musikalbum</a></li>
</ul></td>
<td style="text-align: right;">0..*</td>
</tr>
<tr>
<td style="text-align: left;"><strong>Autor</strong> (<a
href="http://schema.org/author">schema:author</a>): Die Person oder
Gruppe, die den Titel geschrieben hat.</td>
<td style="text-align: left;"></td>
<td style="text-align: right;">0..*</td>
</tr>
<tr>
<td style="text-align: left;"><strong>Genre</strong> (<a
href="http://schema.org/genre">schema:genre</a>)</td>
<td style="text-align: left;"><ul>
<li>Typ: <a href="#sec-nodeshape-genreshape">Genre</a></li>
</ul></td>
<td style="text-align: right;">1..1</td>
</tr>
<tr>
<td style="text-align: left;"><strong>Dauer</strong> (<a
href="http://schema.org/duration">schema:duration</a>): Die Dauer muss
als schema:QuantitativeValue ausgedrückt werden.</td>
<td style="text-align: left;"><ul>
<li>Typ: <a href="#sec-nodeshape-quantitativevalueshape">Quantitativer
Wert</a></li>
</ul></td>
<td style="text-align: right;">0..*</td>
</tr>
<tr>
<td style="text-align: left;"><strong>Dateigrösse</strong> (<a
href="http://schema.org/contentSize">schema:contentSize</a>)</td>
<td style="text-align: left;"><ul>
<li>Typ: <a href="#sec-nodeshape-quantitativevalueshape">Quantitativer
Wert</a></li>
</ul></td>
<td style="text-align: right;">0..*</td>
</tr>
</tbody>
</table>

## Organisation

Ein Unternehmen oder eine Organisation im Chinook-Datensatz.

### Übersicht

<div class="ech-facts">

Shape  
[:OrganisationShape](https://agriculture.ld.admin.ch/eCH-1234/2/OrganisationShape)

Zielklasse  
[schema:Organisation](http://schema.org/Organisation)

Geschlossen  
Nein (weitere Eigenschaften zulässig)

Datenzugriff  
Keiner (Transaktionsdaten, nicht Teil des publizierten Graphen)

</div>

### Eigenschaften

<table style="width:99%;">
<colgroup>
<col style="width: 36%" />
<col style="width: 49%" />
<col style="width: 12%" />
</colgroup>
<thead>
<tr>
<th style="text-align: left;">Beschreibung</th>
<th style="text-align: left;">Details</th>
<th style="text-align: right;">Kardinalität</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: left;"><strong>Name</strong> (<a
href="http://schema.org/name">schema:name</a>): Jede Organisation muss
einen Namen haben.</td>
<td style="text-align: left;"><ul>
<li>Typ: Zeichenkette (<a
href="http://www.w3.org/2001/XMLSchema#string">xsd:string</a>)</li>
<li>Länge: 2–100 Zeichen</li>
</ul></td>
<td style="text-align: right;">1..1</td>
</tr>
</tbody>
</table>

## Person

Jede Person (Mitarbeiter, Kunde oder benutzerdefinierte Person) im
Datensatz.

Personen werden unabhängig von ihrer Rolle einheitlich beschrieben:
Angestellte des Musikhandels, Kundinnen und Kunden sowie manuell
erfasste Personen teilen dieselben Eigenschaften. Die Rolle ergibt sich
aus den Beziehungen, etwa `schema:worksFor` für Angestellte oder
`schema:customer` auf einer Rechnung für Kundschaft.

Namen werden so erfasst, wie sie die Person selbst verwendet;
akademische Titel gehören nicht in den Vornamen. E-Mail-Adressen und
Geburtsdaten sind freiwillige Angaben und werden bei Verstössen gegen
die Regeln lediglich als Warnung gemeldet.

### Übersicht

<div class="ech-facts">

Shape  
[:PersonShape](https://agriculture.ld.admin.ch/eCH-1234/2/PersonShape)

Zielklasse  
[schema:Person](http://schema.org/Person)

Geschlossen  
Ja (nur die aufgeführten Eigenschaften zulässig)

Kennzahlen  
383 Instanzen mit je 5 bis 10 Tripeln (im Mittel 5.6)

Datenzugriff  
[SPARQL-Dienst](https://lindas.admin.ch/sparql/#query=PREFIX%20schema%3A%20%3Chttp%3A%2F%2Fschema.org%2F%3E%0ASELECT%20%3Firi%20%3FgivenName%20%3FfamilyName%20%3Femail%20%3FbirthDate%20%3Faddress%20%3FworksFor%20%3FjobTitle%20%3Fknows%0AFROM%20%3Chttps%3A%2F%2Flindas.admin.ch%2Ffoag%2Fogd%3E%0AWHERE%20%7B%0A%20%20%3Firi%20a%20schema%3APerson%20.%0A%20%20%3Firi%20schema%3AgivenName%20%3FgivenName%20.%0A%20%20%3Firi%20schema%3AfamilyName%20%3FfamilyName%20.%0A%20%20OPTIONAL%20%7B%20%3Firi%20schema%3Aemail%20%3Femail%20.%20%7D%0A%20%20OPTIONAL%20%7B%20%3Firi%20schema%3AbirthDate%20%3FbirthDate%20.%20%7D%0A%20%20OPTIONAL%20%7B%20%3Firi%20schema%3Aaddress%20%3Faddress%20.%20%7D%0A%20%20OPTIONAL%20%7B%20%3Firi%20schema%3AworksFor%20%3FworksFor%20.%20%7D%0A%20%20OPTIONAL%20%7B%20%3Firi%20schema%3AjobTitle%20%3FjobTitle%20.%20%7D%0A%20%20OPTIONAL%20%7B%20%3Firi%20schema%3Aknows%20%3Fknows%20.%20%7D%0A%7D%0ALIMIT%201000)

</div>

### Eigenschaften

<table style="width:99%;">
<colgroup>
<col style="width: 42%" />
<col style="width: 44%" />
<col style="width: 11%" />
</colgroup>
<thead>
<tr>
<th style="text-align: left;">Beschreibung</th>
<th style="text-align: left;">Details</th>
<th style="text-align: right;">Kardinalität</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: left;"><strong>Vorname</strong> (<a
href="http://schema.org/givenName">schema:givenName</a>): Jede Person
muss einen Vornamen haben.</td>
<td style="text-align: left;"><ul>
<li>Typ: Zeichenkette (<a
href="http://www.w3.org/2001/XMLSchema#string">xsd:string</a>)</li>
</ul></td>
<td style="text-align: right;">1..1</td>
</tr>
<tr>
<td style="text-align: left;"><strong>Nachname</strong> (<a
href="http://schema.org/familyName">schema:familyName</a>): Jede Person
muss einen Nachnamen haben.</td>
<td style="text-align: left;"><ul>
<li>Typ: Zeichenkette (<a
href="http://www.w3.org/2001/XMLSchema#string">xsd:string</a>)</li>
</ul></td>
<td style="text-align: right;">1..1</td>
</tr>
<tr>
<td style="text-align: left;"><strong>E-Mail-Adresse</strong> (<a
href="http://schema.org/email">schema:email</a>): Falls angegeben, muss
die E-Mail-Adresse einem Standardformat entsprechen.</td>
<td style="text-align: left;"><ul>
<li>Typ: Zeichenkette (<a
href="http://www.w3.org/2001/XMLSchema#string">xsd:string</a>)</li>
<li>Muster: <code>^.+@.+\..+$</code> (<code>i</code>)</li>
<li>Länge: ≤ 254 Zeichen</li>
<li>Schweregrad: Warnung</li>
</ul></td>
<td style="text-align: right;">0..*</td>
</tr>
<tr>
<td style="text-align: left;"><strong>Geburtsdatum</strong> (<a
href="http://schema.org/birthDate">schema:birthDate</a>): Eine Person
sollte ein gültiges Geburtsdatum haben.</td>
<td style="text-align: left;"><ul>
<li>Typ: Datum (<a
href="http://www.w3.org/2001/XMLSchema#date">xsd:date</a>)</li>
<li>Wertebereich: ≥ 1900-01-01, ≤ 2025-12-31</li>
<li>Schweregrad: Warnung</li>
</ul></td>
<td style="text-align: right;">0..*</td>
</tr>
<tr>
<td style="text-align: left;"><strong>Adresse</strong> (<a
href="http://schema.org/address">schema:address</a>)</td>
<td style="text-align: left;"><ul>
<li>Typ: <a
href="#sec-nodeshape-postaladdressshape">Postadresse</a></li>
</ul></td>
<td style="text-align: right;">0..*</td>
</tr>
<tr>
<td style="text-align: left;"><strong>Arbeitet für</strong> (<a
href="http://schema.org/worksFor">schema:worksFor</a>): Ein Mitarbeiter
kann einer anderen Person unterstellt sein.</td>
<td style="text-align: left;"><ul>
<li>Typ: <a href="#sec-nodeshape-personshape">Person</a> oder <a
href="http://schema.org/Organization">schema:Organization</a></li>
</ul></td>
<td style="text-align: right;">0..*</td>
</tr>
<tr>
<td style="text-align: left;"><strong>Berufsbezeichnung</strong> (<a
href="http://schema.org/jobTitle">schema:jobTitle</a>)</td>
<td style="text-align: left;"><ul>
<li>Typ: Zeichenkette (<a
href="http://www.w3.org/2001/XMLSchema#string">xsd:string</a>)</li>
<li>Länge: 2–100 Zeichen</li>
</ul></td>
<td style="text-align: right;">0..1</td>
</tr>
<tr>
<td style="text-align: left;"><strong>Kennt</strong> (<a
href="http://schema.org/knows">schema:knows</a>)</td>
<td style="text-align: left;"><ul>
<li>Typ: <a href="#sec-nodeshape-personshape">Person</a></li>
</ul></td>
<td style="text-align: right;">0..*</td>
</tr>
</tbody>
</table>

### Regeln (SPARQL)

#### Keine Selbstunterstellung

Ein Mitarbeiter kann nicht sich selbst unterstellt sein.

``` sparql
SELECT $this
WHERE {
    $this schema:worksFor $this .
}
```

## Postadresse

Die Postadresse einer Person.

Adressen folgen dem Aufbau von schema.org und nicht dem Schweizer
Adressstandard eCH-0010, da der Datensatz überwiegend ausländische
Adressen enthält. Postleitzahlen werden deshalb nur auf ein plausibles
Format geprüft, nicht gegen ein Verzeichnis.

### Übersicht

<div class="ech-facts">

Shape  
[:PostalAddressShape](https://agriculture.ld.admin.ch/eCH-1234/2/PostalAddressShape)

Zielklasse  
[schema:PostalAddress](http://schema.org/PostalAddress)

Geschlossen  
Ja (nur die aufgeführten Eigenschaften zulässig)

Kennzahlen  
67 Instanzen mit je 6 bis 8 Tripeln (im Mittel 7.5)

Datenzugriff  
[SPARQL-Dienst](https://lindas.admin.ch/sparql/#query=PREFIX%20schema%3A%20%3Chttp%3A%2F%2Fschema.org%2F%3E%0ASELECT%20%3Firi%20%3FstreetAddress%20%3FpostalCode%20%3FaddressLocality%20%3FaddressRegion%20%3FaddressCountry%0AFROM%20%3Chttps%3A%2F%2Flindas.admin.ch%2Ffoag%2Fogd%3E%0AWHERE%20%7B%0A%20%20%3Firi%20a%20schema%3APostalAddress%20.%0A%20%20%3Firi%20schema%3AstreetAddress%20%3FstreetAddress%20.%0A%20%20OPTIONAL%20%7B%20%3Firi%20schema%3ApostalCode%20%3FpostalCode%20.%20%7D%0A%20%20%3Firi%20schema%3AaddressLocality%20%3FaddressLocality%20.%0A%20%20OPTIONAL%20%7B%20%3Firi%20schema%3AaddressRegion%20%3FaddressRegion%20.%20%7D%0A%20%20%3Firi%20schema%3AaddressCountry%20%3FaddressCountry%20.%0A%7D%0ALIMIT%201000)

</div>

### Eigenschaften

<table style="width:99%;">
<colgroup>
<col style="width: 46%" />
<col style="width: 41%" />
<col style="width: 10%" />
</colgroup>
<thead>
<tr>
<th style="text-align: left;">Beschreibung</th>
<th style="text-align: left;">Details</th>
<th style="text-align: right;">Kardinalität</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: left;"><strong>Strasse und Hausnummer</strong>
(<a
href="http://schema.org/streetAddress">schema:streetAddress</a>)</td>
<td style="text-align: left;"><ul>
<li>Typ: Zeichenkette (<a
href="http://www.w3.org/2001/XMLSchema#string">xsd:string</a>)</li>
<li>Länge: 3–100 Zeichen</li>
<li>Beispiele: Schwarzenburgstrasse 165</li>
</ul></td>
<td style="text-align: right;">1..1</td>
</tr>
<tr>
<td style="text-align: left;"><strong>Postleitzahl</strong> (<a
href="http://schema.org/postalCode">schema:postalCode</a>): Buchstaben,
Ziffern, Leerzeichen und Bindestriche, zwei bis zehn Zeichen.</td>
<td style="text-align: left;"><ul>
<li>Typ: Zeichenkette (<a
href="http://www.w3.org/2001/XMLSchema#string">xsd:string</a>)</li>
<li>Muster: <code>^[A-Za-z0-9][A-Za-z0-9 -]{1,9}$</code></li>
<li>Schweregrad: Warnung</li>
</ul></td>
<td style="text-align: right;">0..1</td>
</tr>
<tr>
<td style="text-align: left;"><strong>Ort</strong> (<a
href="http://schema.org/addressLocality">schema:addressLocality</a>):
Jede Adresse braucht genau einen Ort.</td>
<td style="text-align: left;"><ul>
<li>Typ: Zeichenkette (<a
href="http://www.w3.org/2001/XMLSchema#string">xsd:string</a>)</li>
<li>Länge: ≤ 100 Zeichen</li>
</ul></td>
<td style="text-align: right;">1..1</td>
</tr>
<tr>
<td style="text-align: left;"><strong>Region</strong> (<a
href="http://schema.org/addressRegion">schema:addressRegion</a>):
Kanton, Bundesstaat oder Provinz, sofern im Land üblich.</td>
<td style="text-align: left;"><ul>
<li>Typ: Zeichenkette (<a
href="http://www.w3.org/2001/XMLSchema#string">xsd:string</a>)</li>
<li>Länge: ≤ 100 Zeichen</li>
</ul></td>
<td style="text-align: right;">0..1</td>
</tr>
<tr>
<td style="text-align: left;"><strong>Land</strong> (<a
href="http://schema.org/addressCountry">schema:addressCountry</a>): Land
als IRI aus dem Länderverzeichnis des Bundesarchivs auf LINDAS (ISO
3166-1 alpha-3).</td>
<td style="text-align: left;"><ul>
<li>Muster: <code>^https://ld\.admin\.ch/country/[A-Z]{3}$</code></li>
<li>Beispiele: <a
href="https://ld.admin.ch/country/CHE">country:CHE</a>, <a
href="https://ld.admin.ch/country/FRA">country:FRA</a>, <a
href="https://ld.admin.ch/country/ITA">country:ITA</a></li>
</ul></td>
<td style="text-align: right;">1..1</td>
</tr>
</tbody>
</table>

## Quantitativer Wert

Ein numerischer Wert mit einer dazugehörigen Einheit.

Quantitative Werte werden nie als blosse Zahl erfasst, sondern immer
zusammen mit einer Einheit aus dem QUDT-Vokabular. So bleibt eindeutig,
ob eine Dauer in Millisekunden oder eine Dateigrösse in Bytes gemeint
ist. Negative Werte sind in diesem Datensatz nicht vorgesehen.

### Übersicht

<div class="ech-facts">

Shape  
[:QuantitativeValueShape](https://agriculture.ld.admin.ch/eCH-1234/2/QuantitativeValueShape)

Zielklasse  
[schema:QuantitativeValue](http://schema.org/QuantitativeValue)

Geschlossen  
Ja (nur die aufgeführten Eigenschaften zulässig)

Kennzahlen  
15401 Instanzen mit je 3 Tripeln

Datenzugriff  
[SPARQL-Dienst](https://lindas.admin.ch/sparql/#query=PREFIX%20schema%3A%20%3Chttp%3A%2F%2Fschema.org%2F%3E%0ASELECT%20%3Firi%20%3Fvalue%20%3FunitCode%0AFROM%20%3Chttps%3A%2F%2Flindas.admin.ch%2Ffoag%2Fogd%3E%0AWHERE%20%7B%0A%20%20%3Firi%20a%20schema%3AQuantitativeValue%20.%0A%20%20%3Firi%20schema%3Avalue%20%3Fvalue%20.%0A%20%20%3Firi%20schema%3AunitCode%20%3FunitCode%20.%0A%7D%0ALIMIT%201000)

</div>

### Eigenschaften

<table style="width:99%;">
<colgroup>
<col style="width: 40%" />
<col style="width: 47%" />
<col style="width: 11%" />
</colgroup>
<thead>
<tr>
<th style="text-align: left;">Beschreibung</th>
<th style="text-align: left;">Details</th>
<th style="text-align: right;">Kardinalität</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: left;"><strong>Wert</strong> (<a
href="http://schema.org/value">schema:value</a>): Ein quantitativer Wert
muss genau einen numerischen Wert haben.</td>
<td style="text-align: left;"><ul>
<li>Typ: Dezimalzahl (<a
href="http://www.w3.org/2001/XMLSchema#decimal">xsd:decimal</a>) oder
Ganzzahl (<a
href="http://www.w3.org/2001/XMLSchema#integer">xsd:integer</a>)</li>
<li>Wertebereich: ≥ 0</li>
</ul></td>
<td style="text-align: right;">1..1</td>
</tr>
<tr>
<td style="text-align: left;"><strong>Einheitencode</strong> (<a
href="http://schema.org/unitCode">schema:unitCode</a>): Ein
quantitativer Wert muss seine Einheit über eine unitCode-URI
angeben.</td>
<td style="text-align: left;"><ul>
<li>Werte: <a href="http://qudt.org/vocab/unit/USD">unit:USD</a>, <a
href="http://qudt.org/vocab/unit/EA">unit:EA</a>, <a
href="http://qudt.org/vocab/unit/BYTE">unit:BYTE</a>, <a
href="http://qudt.org/vocab/unit/MilliSEC">unit:MilliSEC</a></li>
</ul></td>
<td style="text-align: right;">1..1</td>
</tr>
</tbody>
</table>

## Rechnung

Ein Kaufbeleg im Chinook-Datensatz. Eine Rechnung fasst die Positionen
eines Kaufs zusammen. Der Rechnungsbetrag wird nicht nur als Wert
erfasst, sondern auch gegen die Summe der Positionen geprüft;
Abweichungen von mehr als fünf Rappen gelten als Fehler. Rechnungen vor
dem Jahr 2000 stammen aus einem Altsystem und sind in diesem Datensatz
nicht zulässig.

### Übersicht

<div class="ech-facts">

Shape  
[:InvoiceShape](https://agriculture.ld.admin.ch/eCH-1234/2/InvoiceShape)

Zielklasse  
[schema:Invoice](http://schema.org/Invoice)

Geschlossen  
Nein (weitere Eigenschaften zulässig)

Kennzahlen  
412 Instanzen mit je 8 bis 21 Tripeln (im Mittel 12.4)

Datenzugriff  
[SPARQL-Dienst](https://lindas.admin.ch/sparql/#query=PREFIX%20schema%3A%20%3Chttp%3A%2F%2Fschema.org%2F%3E%0ASELECT%20%3Firi%20%3Fcustomer%20%3FtotalPaymentDue%20%3FhasPart%20%3FdateCreated%0AFROM%20%3Chttps%3A%2F%2Flindas.admin.ch%2Ffoag%2Fogd%3E%0AWHERE%20%7B%0A%20%20%3Firi%20a%20schema%3AInvoice%20.%0A%20%20%3Firi%20schema%3Acustomer%20%3Fcustomer%20.%0A%20%20%3Firi%20schema%3AtotalPaymentDue%20%3FtotalPaymentDue%20.%0A%20%20%3Firi%20schema%3AhasPart%20%3FhasPart%20.%0A%20%20OPTIONAL%20%7B%20%3Firi%20schema%3AdateCreated%20%3FdateCreated%20.%20%7D%0A%7D%0ALIMIT%201000)

</div>

### Eigenschaften

<table style="width:99%;">
<colgroup>
<col style="width: 48%" />
<col style="width: 40%" />
<col style="width: 11%" />
</colgroup>
<thead>
<tr>
<th style="text-align: left;">Beschreibung</th>
<th style="text-align: left;">Details</th>
<th style="text-align: right;">Kardinalität</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: left;"><strong>Kunde</strong> (<a
href="http://schema.org/customer">schema:customer</a>): Eine Rechnung
muss genau einem Kunden zugeordnet sein.</td>
<td style="text-align: left;"><ul>
<li>Typ: <a href="#sec-nodeshape-personshape">Person</a></li>
</ul></td>
<td style="text-align: right;">1..1</td>
</tr>
<tr>
<td style="text-align: left;"><strong>Fälliger Gesamtbetrag</strong> (<a
href="http://schema.org/totalPaymentDue">schema:totalPaymentDue</a>):
Eine Rechnung muss einen fälligen Gesamtbetrag als
schema:QuantitativeValue definieren.</td>
<td style="text-align: left;"><ul>
<li>Typ: <a href="#sec-nodeshape-quantitativevalueshape">Quantitativer
Wert</a></li>
</ul></td>
<td style="text-align: right;">1..1</td>
</tr>
<tr>
<td style="text-align: left;"><strong>Enthält</strong> (<a
href="http://schema.org/hasPart">schema:hasPart</a>): Eine Rechnung muss
mindestens eine Position (OrderItem) enthalten.</td>
<td style="text-align: left;"><ul>
<li>Typ: <a href="http://schema.org/OrderItem">schema:OrderItem</a></li>
</ul></td>
<td style="text-align: right;">1..*</td>
</tr>
<tr>
<td style="text-align: left;"><strong>Erstellungsdatum</strong> (<a
href="http://schema.org/dateCreated">schema:dateCreated</a>)</td>
<td style="text-align: left;"><ul>
<li>Typ: Datum (<a
href="http://www.w3.org/2001/XMLSchema#date">xsd:date</a>)</li>
<li>Wertebereich: ≥ 2000-01-01</li>
<li>Beispiele: 2001-01-01, 2024-05-21</li>
</ul></td>
<td style="text-align: right;">0..*</td>
</tr>
</tbody>
</table>

### Regeln (SPARQL)

#### Rechnungsdatum

Eine Rechnung darf nicht vor dem Jahr 2000 datiert sein.

``` sparql
SELECT $this
WHERE {
    $this schema:dateCreated ?date .
    FILTER(?date < "2000-01-01"^^xsd:date)
}
```

#### Rechnungssumme

Die Rechnungssumme muss exakt mit der Summe ihrer Positionen
übereinstimmen (Toleranz 0.05).

``` sparql
SELECT $this
WHERE {
    $this schema:totalPaymentDue/schema:value ?invoiceTotal .
    {
        SELECT $this (SUM(?price * ?qty) AS ?calculatedTotal)
        WHERE {
            $this schema:hasPart ?line .
            ?line schema:price/schema:value ?price .
            ?line schema:orderQuantity/schema:value ?qty .
        }
        GROUP BY $this
    }
    FILTER(ABS(?invoiceTotal - ?calculatedTotal) > 0.05)
}
```

# Datenbezug

Die diesem Dokument zugrundeliegenden Master- und Referenzdaten sind als
*Linked Data* verfügbar.

Die technologische Basis dafür bildet das Resource Description Framework
\[RDF, RDF\], ein zentraler Standard des World Wide Web Consortiums
(W3C) zur Modellierung von Datenstrukturen im Web. In RDF werden
Informationen nicht in klassischen Tabellen, sondern als vernetzte
Graphen abgebildet. Jede Aussage besteht dabei aus einem sogenannten
Triple (Subjekt, Prädikat, Objekt). Diese Struktur ermöglicht eine
maschinenlesbare, interoperable und systemübergreifend eindeutige
Beschreibung von Ressourcen und deren Relationen zueinander.

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
BASE <https://agriculture.ld.admin.ch/eCH-1234/2/>
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
@base <https://agriculture.ld.admin.ch/eCH-1234/2/> .
@prefix genre: <https://agriculture.ld.admin.ch/eCH-1234/2/genre/> .
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

# Anhang A – Referenzen

<div id="refs" class="references csl-bib-body">

<div id="ref-berners2023semantic" class="csl-entry">

<span class="csl-left-margin">\[Berners-Lee 2023\]
</span><span class="csl-right-inline">Berners-Lee, Tim ; Hendler,
James ; Lassila, Ora: [The Semantic Web: A new form of Web content that
is meaningful to computers will unleash a revolution of new
possibilities](https://doi.org/10.1145/3591366.3591376). In: *Linking
the World’s Information: Essays on Tim Berners-Lee’s Invention of the
World Wide Web* : Association for Computing Machinery, 2023,
S. 91–103</span>

</div>

<div id="ref-DCAT" class="csl-entry">

<span class="csl-left-margin">\[DCAT\]
</span><span class="csl-right-inline">Albertoni, Riccardo ; Browning,
David ; Cox, Simon ; Gonzalez Beltran, Alejandra ; Perego, Andrea ;
Winstanley, Peter: *[Data Catalog Vocabulary (DCAT) – Version
3](https://www.w3.org/TR/vocab-dcat-3/)* (W3C Recommendation) : World
Wide Web Consortium (W3C), 2024</span>

</div>

<div id="ref-eCH-0003:11.1.0" class="csl-entry">

<span class="csl-left-margin">\[eCH-0003 11.1.0\]
</span><span class="csl-right-inline">Verein eCH: *[eCH-0003 Leitfaden
zur Genehmigung von
Anträgen](https://www.ech.ch/de/ech/ech-0003/11.1.0)* (eCH-Standard) :
Verein eCH, 2022</span>

</div>

<div id="ref-eCH-0010:8.1.0" class="csl-entry">

<span class="csl-left-margin">\[eCH-0010 8.1.0\]
</span><span class="csl-right-inline">Verein eCH: *[eCH-0010
Datenstandard Postadresse für natürliche Personen, Firmen,
Organisationen und Behörden](https://www.ech.ch/de/ech/ech-0010/8.1.0)*
(eCH-Standard) : Verein eCH, 2021</span>

</div>

<div id="ref-eCH-0200:3.0.1" class="csl-entry">

<span class="csl-left-margin">\[eCH-0200 3.0.1\]
</span><span class="csl-right-inline"><span class="nocase">eCH-Fachgruppe
Open Government Data</span>: *[eCH-0200 DCAT-Anwendungsprofil für
Datenportale in der Schweiz (DCAT-AP
CH)](https://www.ech.ch/de/ech/ech-0200/3.0.1)* (eCH-Standard) : Verein
eCH, 2025</span>

</div>

<div id="ref-eCH-0205:1.0" class="csl-entry">

<span class="csl-left-margin">\[eCH-0205 1.0\]
</span><span class="csl-right-inline"><span class="nocase">eCH-Fachgruppe
Open Government Data</span>: *[eCH-0205 Linked Open
Data](https://www.ech.ch/de/ech/ech-0205/1.0)* (eCH-Hilfsmittel) :
Verein eCH, 2018</span>

</div>

<div id="ref-eCH-0265:1.0.0" class="csl-entry">

<span class="csl-left-margin">\[eCH-0265 1.0.0\]
</span><span class="csl-right-inline"><span class="nocase">eCH-Fachgruppe
AgriFood</span>: *[eCH-0265 Datenstandard Agrardaten – Flächen und
Kulturen](https://www.ech.ch/de/ech/ech-0265/1.0.0)* (eCH-Standard) :
Verein eCH, 2024</span>

</div>

<div id="ref-JSON-LD" class="csl-entry">

<span class="csl-left-margin">\[JSON-LD\]
</span><span class="csl-right-inline">Sporny, Manu ; Longley, Dave ;
Kellogg, Gregg ; Lanthaler, Markus ; Champin, Pierre-Antoine ;
Lindström, Niklas: *[JSON-LD 1.1 – A JSON-based Serialization for Linked
Data](https://www.w3.org/TR/json-ld11/)* (W3C Recommendation) : World
Wide Web Consortium (W3C), 2020</span>

</div>

<div id="ref-OWL2" class="csl-entry">

<span class="csl-left-margin">\[OWL 2\]
</span><span class="csl-right-inline">W3C OWL Working Group: *[OWL 2 Web
Ontology Language Document Overview (Second
Edition)](https://www.w3.org/TR/owl2-overview/)* (W3C Recommendation) :
World Wide Web Consortium (W3C), 2012</span>

</div>

<div id="ref-cyganiak2014rdf11" class="csl-entry">

<span class="csl-left-margin">\[RDF\]
</span><span class="csl-right-inline">Cyganiak, Richard ; Wood, David ;
Lanthaler, Markus: *[RDF 1.1 Concepts and Abstract
Syntax](https://www.w3.org/TR/rdf11-concepts/)* (W3C Recommendation) :
World Wide Web Consortium (W3C), 2014</span>

</div>

<div id="ref-SHACL" class="csl-entry">

<span class="csl-left-margin">\[SHACL\]
</span><span class="csl-right-inline">Knublauch, Holger ; Kontokostas,
Dimitris: *[Shapes Constraint Language
(SHACL)](https://www.w3.org/TR/shacl/)* (W3C Recommendation) : World
Wide Web Consortium (W3C), 2017</span>

</div>

<div id="ref-SKOS" class="csl-entry">

<span class="csl-left-margin">\[SKOS\]
</span><span class="csl-right-inline">Miles, Alistair ; Bechhofer, Sean:
*[SKOS Simple Knowledge Organization System
Reference](https://www.w3.org/TR/skos-reference/)* (W3C
Recommendation) : World Wide Web Consortium (W3C), 2009</span>

</div>

<div id="ref-SPARQL" class="csl-entry">

<span class="csl-left-margin">\[SPARQL\]
</span><span class="csl-right-inline">Harris, Steve ; Seaborne, Andy:
*[SPARQL 1.1 Query Language](https://www.w3.org/TR/sparql11-query/)*
(W3C Recommendation) : World Wide Web Consortium (W3C), 2013</span>

</div>

<div id="ref-Turtle" class="csl-entry">

<span class="csl-left-margin">\[Turtle\]
</span><span class="csl-right-inline">Beckett, David ; Berners-Lee,
Tim ; Prud’hommeaux, Eric ; Carothers, Gavin: *[RDF 1.1 Turtle – Terse
RDF Triple Language](https://www.w3.org/TR/turtle/)* (W3C
Recommendation) : World Wide Web Consortium (W3C), 2014</span>

</div>

</div>

# Anhang B – Mitwirkung und Prüfung

| Name              | Organisation                 |
|:------------------|:-----------------------------|
| Damian Oswald     | Bundesamt für Landwirtschaft |
| Michael Schüpbach | Bundesamt für Landwirtschaft |
| Lea Stauber       | Bundesamt für Landwirtschaft |

# Anhang C – Abkürzungen und Glossar

Dieses Glossar ist als SKOS-Glossar \[SKOS\] auch maschinenlesbar
verfügbar, auf [LINDAS](https://lindas.admin.ch/) und im
[GitHub-Repository](https://github.com/blw-ofag-ufag/semantic-web-template/blob/main/src/rdf/data/glossary.skos.ttl).

<div id="tbl-glossary">

Tabelle 3: Glossar des Standards eCH-1234

<table>
<colgroup>
<col style="width: 35%" />
<col style="width: 65%" />
</colgroup>
<thead>
<tr>
<th style="text-align: left;">Begriff</th>
<th style="text-align: left;">Beschreibung</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: left;"><strong>Graph</strong> (Named Graph)</td>
<td style="text-align: left;"><p>Eine Menge von Tripeln. Ein benannter
Graph wird selbst durch eine IRI identifiziert und erlaubt es, Daten in
einem Triple Store zu gruppieren.</p>
<p><em>Oberbegriff</em>: Resource Description Framework</p></td>
</tr>
<tr>
<td style="text-align: left;"><strong>Inferenz</strong> (Reasoning)</td>
<td style="text-align: left;">Das automatische Ableiten neuer Aussagen
aus den vorhandenen Daten und den Axiomen einer Ontologie, zum Beispiel
durch den Reasoner HermiT.</td>
</tr>
<tr>
<td style="text-align: left;"><strong>Internationalized Resource
Identifier</strong> (IRI)</td>
<td style="text-align: left;"><p>Weltweit eindeutiger Bezeichner einer
Ressource. In RDF werden Subjekte, Prädikate und die meisten Objekte
durch IRIs identifiziert.</p>
<p><em>Oberbegriff</em>: Resource Description Framework</p></td>
</tr>
<tr>
<td style="text-align: left;"><strong>JSON for Linking Data</strong>
(JSON-LD)</td>
<td style="text-align: left;"><p>Eine Serialisierung von RDF auf der
Basis von JSON, die sich besonders für Web-Schnittstellen eignet.</p>
<p><em>Oberbegriff</em>: Serialisierung</p></td>
</tr>
<tr>
<td style="text-align: left;"><strong>Linked Data</strong> (Verknüpfte
Daten)</td>
<td style="text-align: left;"><p>Daten, die nach den Prinzipien des
Semantic Web mit IRIs identifiziert, in RDF beschrieben und
untereinander verknüpft publiziert werden.</p>
<p><em>Verwandt</em>: Linked Data Service, Resource Description
Framework</p></td>
</tr>
<tr>
<td style="text-align: left;"><strong>Linked Data Service</strong>
(LINDAS)</td>
<td style="text-align: left;">Der offizielle Linked-Data-Dienst der
Schweizer Bundesverwaltung, der als Triple Store fungiert.</td>
</tr>
<tr>
<td style="text-align: left;"><strong>Literal</strong></td>
<td style="text-align: left;"><p>Ein konkreter Wert in RDF, etwa eine
Zeichenkette, eine Zahl oder ein Datum, optional mit Datentyp oder
Sprachangabe.</p>
<p><em>Oberbegriff</em>: Resource Description Framework</p></td>
</tr>
<tr>
<td style="text-align: left;"><strong>Namensraum</strong> (Präfix)</td>
<td style="text-align: left;"><p>Gemeinsamer Anfang einer Gruppe von
IRIs. In Turtle und SPARQL wird ein Namensraum durch ein Präfix
abgekürzt, zum Beispiel <code>schema:</code> für
<code>http://schema.org/</code>.</p>
<p><em>Verwandt</em>: Internationalized Resource Identifier</p></td>
</tr>
<tr>
<td style="text-align: left;"><strong>Ontologie</strong></td>
<td style="text-align: left;"><p>Ein formales Modell eines Fachgebiets,
das Klassen, Eigenschaften und deren logische Beziehungen so beschreibt,
dass Maschinen daraus Schlüsse ziehen können.</p>
<p><em>Oberbegriff</em>: Vokabular</p>
<p><em>Verwandt</em>: Web Ontology Language</p></td>
</tr>
<tr>
<td style="text-align: left;"><strong>Resource Description
Framework</strong> (RDF)</td>
<td style="text-align: left;">Ein zentraler Standard des World Wide Web
Consortiums (W3C) zur Modellierung von Datenstrukturen im Web.
Informationen werden nicht in klassischen Tabellen, sondern als
vernetzte Graphen abgebildet.</td>
</tr>
<tr>
<td style="text-align: left;"><strong>Serialisierung</strong></td>
<td style="text-align: left;"><p>Textuelle Darstellung eines RDF-Graphen
in einem definierten Format, um ihn zu speichern oder auszutauschen.</p>
<p><em>Unterbegriff</em>: JSON for Linking Data, Terse RDF Triple
Language</p></td>
</tr>
<tr>
<td style="text-align: left;"><strong>Shape</strong></td>
<td style="text-align: left;"><p>Eine Menge von Bedingungen, die eine
Klasse von Ressourcen oder eine Eigenschaft erfüllen muss, etwa
Pflichtfelder, Datentypen und Kardinalitäten.</p>
<p><em>Oberbegriff</em>: Shapes Constraint Language</p></td>
</tr>
<tr>
<td style="text-align: left;"><strong>Shapes Constraint
Language</strong> (SHACL)</td>
<td style="text-align: left;"><p>Die Sprache des W3C zur Beschreibung
und Prüfung der Struktur von RDF-Daten. Das Datenmodell dieses Standards
ist in SHACL formuliert.</p>
<p><em>Unterbegriff</em>: Shape</p></td>
</tr>
<tr>
<td style="text-align: left;"><strong>Simple Knowledge Organization
System</strong> (SKOS)</td>
<td style="text-align: left;"><p>Ein Vokabular des W3C für Thesauri,
Klassifikationen und Glossare. Dieses Glossar ist selbst in SKOS
erfasst.</p>
<p><em>Verwandt</em>: Vokabular</p></td>
</tr>
<tr>
<td style="text-align: left;"><strong>SPARQL Protocol and RDF Query
Language</strong> (SPARQL)</td>
<td style="text-align: left;"><p>Die Abfragesprache des W3C für
RDF-Daten. Mit SPARQL werden Daten aus Graphen gelesen, verändert und
zwischen Systemen ausgetauscht.</p>
<p><em>Verwandt</em>: Resource Description Framework</p></td>
</tr>
<tr>
<td style="text-align: left;"><strong>SPARQL-Endpunkt</strong></td>
<td style="text-align: left;"><p>Eine Web-Schnittstelle, über die
SPARQL-Abfragen an einen Triple Store gesendet werden können.</p>
<p><em>Oberbegriff</em>: SPARQL Protocol and RDF Query Language</p></td>
</tr>
<tr>
<td style="text-align: left;"><strong>Terse RDF Triple Language</strong>
(Turtle)</td>
<td style="text-align: left;"><p>Eine kompakte, gut lesbare
Serialisierung für RDF. Alle RDF-Dateien dieses Standards sind in Turtle
verfasst.</p>
<p><em>Oberbegriff</em>: Serialisierung</p></td>
</tr>
<tr>
<td style="text-align: left;"><strong>Tripel</strong></td>
<td style="text-align: left;"><p>Die Grundstruktur einer Aussage in RDF,
bestehend aus Subjekt, Prädikat und Objekt.</p>
<p><em>Oberbegriff</em>: Resource Description Framework</p></td>
</tr>
<tr>
<td style="text-align: left;"><strong>Triple Store</strong>
(Graphdatenbank)</td>
<td style="text-align: left;"><p>Eine Datenbank, die auf das Speichern
und Abfragen von RDF-Tripeln spezialisiert ist.</p>
<p><em>Verwandt</em>: Linked Data Service</p></td>
</tr>
<tr>
<td style="text-align: left;"><strong>Vokabular</strong></td>
<td style="text-align: left;"><p>Eine Sammlung von Klassen und
Eigenschaften mit festgelegter Bedeutung, die zur Beschreibung von Daten
wiederverwendet wird, zum Beispiel schema.org.</p>
<p><em>Unterbegriff</em>: Ontologie</p></td>
</tr>
<tr>
<td style="text-align: left;"><strong>Web Ontology Language</strong>
(OWL)</td>
<td style="text-align: left;"><p>Die Sprache des W3C zur Formulierung
von Ontologien. Sie erlaubt es, Klassen und Eigenschaften mit logischen
Axiomen zu definieren.</p>
<p><em>Verwandt</em>: Inferenz</p></td>
</tr>
</tbody>
</table>

</div>

# Anhang D – Änderungen gegenüber der Vorversion

Die wichtigsten Änderungen der Version 2.0.0 gegenüber der Vorversion
1.4.6:

- **Dokumentvorlage:** Die PDF-Ausgabe folgt neu der eCH-Dokumentvorlage
  (Titelseite mit Metadatentabelle, Kopf- und Fusszeile,
  Inhaltsverzeichnis, Anhänge); die Website übernimmt denselben Stil in
  einer hellen und einer dunklen Variante.
- **Metadaten:** Nummer, Kategorie, Reifegrad, Version, Status und
  weitere Angaben des Standards werden einmal zentral erfasst und
  automatisch in alle Sprachversionen, in die Titelseite, in die
  Fusszeile und in
  <a href="#sec-status" class="quarto-xref">Kapitel 1.1</a> übernommen.
- **Verzeichnisse:** Abbildungs- und Tabellenverzeichnis (Anhang E
  und F) werden automatisch erzeugt und sind mit den Abbildungen und
  Tabellen verlinkt.
- **Darstellung:** Einheitliche Gestaltung von Tabellen, Beschriftungen
  und Code in PDF und Website.

Eine vollständige Liste aller Änderungen je Version findet sich in den
[Releases auf
GitHub](https://github.com/blw-ofag-ufag/semantic-web-template/releases).

# Anhang E – Abbildungsverzeichnis

# Anhang F – Tabellenverzeichnis

[^1]: Fussnoten erscheinen auf der Website am rechten Rand, im PDF am
    Seitenende.

[^2]: Eine zweite Fussnote mit einem Link auf
    [ech.ch](https://www.ech.ch/).
