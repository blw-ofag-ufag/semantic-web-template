# Template Quarto Document

2026-10-01

- [<span class="toc-section-number">1</span>
  Introduction](#sec-introduction)
  - [<span class="toc-section-number">1.1</span> Status](#sec-status)
  - [<span class="toc-section-number">1.2</span> Scope of
    application](#sec-scope-of-application)
  - [<span class="toc-section-number">1.3</span> We can have
    sub-headings](#sec-example-subheading)
  - [<span class="toc-section-number">1.4</span>
    Formatting](#sec-formatting)
- [<span class="toc-section-number">2</span> Usage
  notes](#sec-usage-notes)
  - [<span class="toc-section-number">2.1</span>
    Namespaces](#sec-namespaces)
- [<span class="toc-section-number">3</span> Data
  Model](#sec-data-model)
  - [<span class="toc-section-number">3.1</span>
    Genre](#sec-nodeshape-genreshape)
  - [<span class="toc-section-number">3.2</span>
    Invoice](#sec-nodeshape-invoiceshape)
  - [<span class="toc-section-number">3.3</span> Music
    album](#sec-nodeshape-musicalbumshape)
  - [<span class="toc-section-number">3.4</span> Music
    Recording](#sec-nodeshape-trackshape)
  - [<span class="toc-section-number">3.5</span>
    Organisation](#sec-nodeshape-organisationshape)
  - [<span class="toc-section-number">3.6</span>
    Person](#sec-nodeshape-personshape)
  - [<span class="toc-section-number">3.7</span> Postal
    address](#sec-nodeshape-postaladdressshape)
  - [<span class="toc-section-number">3.8</span> Quantitative
    Value](#sec-nodeshape-quantitativevalueshape)
- [<span class="toc-section-number">4</span> Data
  Retrieval](#sec-data-retrieval)
- [<span class="toc-section-number">5</span> Safety
  considerations](#sec-safety-consideration)
- [<span class="toc-section-number">6</span>
  Disclaimer](#sec-disclaimer)
- [<span class="toc-section-number">7</span>
  Copyrights](#sec-copyrights)
- [Annex A – References](#sec-appendix-a)
- [Annex B – Cooperation and Verification](#sec-appendix-b)
- [Annex C – Abbreviations and Glossary](#sec-appendix-c)
- [Annex D – Changes in comparison to previous version](#sec-appendix-d)
- [Annex E – Table of figures](#sec-appendix-e)
- [Annex F – Table of tables](#sec-appendix-f)

# Note

This document uses a gender-neutral formulation when referring to
persons. This is based on the guidelines (German) of the Federal
Chancellery. Depending on the situation, paired forms (citizens),
gender-abstract forms (insured person), gender-neutral forms (insured
person) or paraphrases with-out personal reference are used. The generic
masculine (citizen) is not permitted. Full forms are used in continuous
texts, i.e. in texts consisting of formulated sentences. Short forms can
be used in ab-breviated text passages, namely in tables. The short form
is used with a slash but without an ellipsis (referent). Gender
asterisks and similar spellings are not used.

# Introduction

## Status

In progress: Use is only permitted within the Technical Unit or the
Expert Committee.

## Scope of application

The information in this chapter should provide the reader with a brief
overview of what this standard is intended for. Information about the
following matters may be helpful here.

## We can have sub-headings

And write some text.

### Also sub-sub-headings

And write some more text. Maybe even with a pretty image.

<div id="fig-example">

![](https://fastly.picsum.photos/id/653/536/354.jpg?hmac=3InR8I5KmwbdkPHehlM8BMPd_BDHG_RWZkxt_IkeQGY)

Figure 1: Always add some text to describe what the image shows. If a
figure has a caption, it appears in the list of figures. Only the first
sentence of the caption is shown there.

</div>

When displaying diagrams, try to write them in Mermaid JS straight away;
this makes changes in the future or translations straightforward.

## Formatting

This chapter is a stress test: it contains the common Markdown and
Quarto elements so that their rendering in the PDF and on the website
can be checked.

### Text styling

Text can be **bold**, *italic*, <u>underlined</u>,
<span class="mark">highlighted</span>, <span class="smallcaps">in small
caps</span> or ~~struck through~~. Keyboard shortcuts such as `Ctrl-C` +
`Ctrl-V` and inline code such as `schema:name` are set off visually.[^1]

#### A fourth-level heading

Headings down to the fourth level are possible; they are numbered but do
not appear in the table of contents.[^2]

### Lists and callouts

Unordered list:

- First item
- Second item
  - Sub-item
- Third item

Ordered list:

1.  First step
2.  Second step
3.  Third step

> [!NOTE]
>
> A note draws attention to connections that are easily overlooked.

> [!WARNING]
>
> A warning points out sources of error, for example unchecked input
> data.

### Code, tables and formulas

The following code block shows a SPARQL query:

``` sparql
SELECT ?s ?p ?o
WHERE {
  ?s ?p ?o .
}
LIMIT 10
```

<div id="tbl-example">

Table 1: Example table with three columns. If a table has a caption, it
appears in the list of tables. Only the first sentence of the caption is
shown there.

| Column   | Type           | Remark          |
|:---------|:---------------|:----------------|
| Name     | String         | Mandatory field |
| Quantity | Decimal number | with unit       |

</div>

A formula can appear in the text, for example $E = m c^2$, or as a
standalone equation such as
<a href="#eq-example" class="quarto-xref">Equation 1</a>:

<span id="eq-example">$$
\sum_{i=1}^{n} x_i = n \bar{x}
 \qquad(1)$$</span>

# Usage notes

The following paragraph is deliberately nonsense and only tests the
citation style: according to the approval guideline \[eCH-0003 11.1.0\],
all postal addresses \[eCH-0010 8.1.0\] must be serialised in Turtle
\[Turtle\], validated as a DCAT catalogue \[DCAT; eCH-0200 3.0.1\] with
SHACL \[SHACL\] and published via SPARQL \[SPARQL\] as Linked Open Data
\[eCH-0205 1.0\] on agricultural crops \[eCH-0265 1.0.0\] in JSON-LD
\[JSON-LD\] and OWL \[OWL 2\], as the Semantic Web \[Berners-Lee 2023\]
intends.

## Namespaces

<a href="#tbl-namespaces" class="quarto-xref">Table 2</a> lists the
prefixes and namespaces used in this document. A prefix stands for a
namespace IRI, the common beginning of the IRIs of a vocabulary. The
Turtle specification describes how such [*prefixed
names*](https://www.w3.org/TR/turtle/#prefixed-name) are resolved
\[Turtle\].

<div id="tbl-namespaces">

Table 2: Namespaces used in eCH-1234 – Template Quarto Document.

| Prefix     | Namespace                                     |
|:-----------|:----------------------------------------------|
| `:`        | <https://agriculture.ld.admin.ch/eCH-1234/2/> |
| `country:` | <https://ld.admin.ch/country/>                |
| `rdf:`     | <http://www.w3.org/1999/02/22-rdf-syntax-ns#> |
| `schema:`  | <http://schema.org/>                          |
| `unit:`    | <http://qudt.org/vocab/unit/>                 |
| `xsd:`     | <http://www.w3.org/2001/XMLSchema#>           |

</div>

# Data Model

## Genre

A musical category in the Chinook dataset.

### Overview

<div class="ech-facts">

IRI  
<https://agriculture.ld.admin.ch/eCH-1234/2/GenreShape>

Target class  
`:Genre`

Closed  
Yes (only the listed properties are allowed)

Key figures  
25 instances with 5 to 7 triples each (5.4 on average)

Open data  
Yes ([published on
LINDAS](https://lindas.admin.ch/sparql/#query=PREFIX%20%3A%20%3Chttps%3A%2F%2Fagriculture.ld.admin.ch%2FeCH-1234%2F2%2F%3E%0APREFIX%20schema%3A%20%3Chttp%3A%2F%2Fschema.org%2F%3E%0ASELECT%20%3Firi%20%3Fname%20%3FpartOf%20%3FalternateName%0AFROM%20%3Chttps%3A%2F%2Flindas.admin.ch%2Ffoag%2Fogd%3E%0AWHERE%20%7B%0A%20%20%3Firi%20a%20%3AGenre%20.%0A%20%20%3Firi%20schema%3Aname%20%3Fname%20.%0A%20%20OPTIONAL%20%7B%20%3Firi%20schema%3ApartOf%20%3FpartOf%20.%20%7D%0A%20%20OPTIONAL%20%7B%20%3Firi%20schema%3AalternateName%20%3FalternateName%20.%20%7D%0A%7D%0ALIMIT%201000))

</div>

### Properties

<table style="width:99%;">
<colgroup>
<col style="width: 41%" />
<col style="width: 43%" />
<col style="width: 14%" />
</colgroup>
<thead>
<tr>
<th style="text-align: left;">Description</th>
<th style="text-align: left;">Details</th>
<th style="text-align: right;">Cardinality</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: left;"><strong>Name</strong>
(<code>schema:name</code>)</td>
<td style="text-align: left;"><ul>
<li>Type: Text (<code>xsd:string</code>)</li>
<li>Pattern: <code>^[A-Z]</code></li>
<li>Length: 2–50 characters</li>
</ul></td>
<td style="text-align: right;">1..1</td>
</tr>
<tr>
<td style="text-align: left;"><strong>Part of</strong>
(<code>schema:partOf</code>)</td>
<td style="text-align: left;"><ul>
<li>Type: <a href="#sec-nodeshape-genreshape">Genre</a></li>
</ul></td>
<td style="text-align: right;">0..*</td>
</tr>
<tr>
<td style="text-align: left;"><strong>Alternate name</strong>
(<code>schema:alternateName</code>): Translated or colloquial name of
the genre, at most one per language.</td>
<td style="text-align: left;"><ul>
<li>Type: Language-tagged text (<code>rdf:langString</code>)</li>
<li>Length: ≤ 50 characters</li>
<li>Languages: <code>de</code>, <code>fr</code>, <code>it</code>,
<code>en</code> (one per language)</li>
</ul></td>
<td style="text-align: right;">0..*</td>
</tr>
</tbody>
</table>

### Rules (SPARQL)

#### No cyclic hierarchy

A genre cannot be a part of itself, either directly or transitively.

``` sparql
SELECT $this
WHERE {
    $this schema:partOf+ $this .
}
```

## Invoice

A purchase receipt in the Chinook dataset. An invoice groups the items
of one purchase. The invoice total is not only recorded as a value but
also checked against the sum of its items; differences of more than five
cents count as errors. Invoices dated before the year 2000 stem from a
legacy system and are not permitted in this dataset.

### Overview

<div class="ech-facts">

IRI  
<https://agriculture.ld.admin.ch/eCH-1234/2/InvoiceShape>

Target class  
`schema:Invoice`

Closed  
No (further properties are allowed)

Key figures  
412 instances with 8 to 21 triples each (12.4 on average)

Open data  
Yes ([published on
LINDAS](https://lindas.admin.ch/sparql/#query=PREFIX%20schema%3A%20%3Chttp%3A%2F%2Fschema.org%2F%3E%0ASELECT%20%3Firi%20%3Fcustomer%20%3FtotalPaymentDue%20%3FhasPart%20%3FdateCreated%0AFROM%20%3Chttps%3A%2F%2Flindas.admin.ch%2Ffoag%2Fogd%3E%0AWHERE%20%7B%0A%20%20%3Firi%20a%20schema%3AInvoice%20.%0A%20%20%3Firi%20schema%3Acustomer%20%3Fcustomer%20.%0A%20%20%3Firi%20schema%3AtotalPaymentDue%20%3FtotalPaymentDue%20.%0A%20%20%3Firi%20schema%3AhasPart%20%3FhasPart%20.%0A%20%20OPTIONAL%20%7B%20%3Firi%20schema%3AdateCreated%20%3FdateCreated%20.%20%7D%0A%7D%0ALIMIT%201000))

</div>

### Properties

<table style="width:99%;">
<colgroup>
<col style="width: 40%" />
<col style="width: 44%" />
<col style="width: 14%" />
</colgroup>
<thead>
<tr>
<th style="text-align: left;">Description</th>
<th style="text-align: left;">Details</th>
<th style="text-align: right;">Cardinality</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: left;"><strong>Customer</strong>
(<code>schema:customer</code>): An invoice must be linked to exactly one
customer.</td>
<td style="text-align: left;"><ul>
<li>Type: <a href="#sec-nodeshape-personshape">Person</a></li>
</ul></td>
<td style="text-align: right;">1..1</td>
</tr>
<tr>
<td style="text-align: left;"><strong>Total payment due</strong>
(<code>schema:totalPaymentDue</code>): An invoice must define a total
payment due as a schema:QuantitativeValue.</td>
<td style="text-align: left;"><ul>
<li>Type: <a href="#sec-nodeshape-quantitativevalueshape">Quantitative
Value</a></li>
</ul></td>
<td style="text-align: right;">1..1</td>
</tr>
<tr>
<td style="text-align: left;"><strong>Has part</strong>
(<code>schema:hasPart</code>): An invoice must have at least one line
item (OrderItem).</td>
<td style="text-align: left;"><ul>
<li>Type: <code>schema:OrderItem</code></li>
</ul></td>
<td style="text-align: right;">1..*</td>
</tr>
<tr>
<td style="text-align: left;"><strong>Date created</strong>
(<code>schema:dateCreated</code>)</td>
<td style="text-align: left;"><ul>
<li>Type: Date (<code>xsd:date</code>)</li>
<li>Range: ≥ 2000-01-01</li>
<li>Examples: 2001-01-01, 2024-05-21</li>
</ul></td>
<td style="text-align: right;">0..*</td>
</tr>
</tbody>
</table>

### Rules (SPARQL)

#### Invoice date

An invoice cannot be dated before the year 2000.

``` sparql
SELECT $this
WHERE {
    $this schema:dateCreated ?date .
    FILTER(?date < "2000-01-01"^^xsd:date)
}
```

#### Invoice total

Invoice total payment due must exactly match the sum of its lines
(within 0.05 tolerance).

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

## Music album

A collection of tracks in the Chinook dataset.

### Overview

<div class="ech-facts">

IRI  
<https://agriculture.ld.admin.ch/eCH-1234/2/MusicAlbumShape>

Target class  
`schema:MusicAlbum`

Closed  
No (further properties are allowed)

Key figures  
347 instances with 5 triples each

Open data  
Yes ([published on
LINDAS](https://lindas.admin.ch/sparql/#query=PREFIX%20schema%3A%20%3Chttp%3A%2F%2Fschema.org%2F%3E%0ASELECT%20%3Firi%20%3Fname%20%3FbyArtist%0AFROM%20%3Chttps%3A%2F%2Flindas.admin.ch%2Ffoag%2Fogd%3E%0AWHERE%20%7B%0A%20%20%3Firi%20a%20schema%3AMusicAlbum%20.%0A%20%20%3Firi%20schema%3Aname%20%3Fname%20.%0A%20%20OPTIONAL%20%7B%20%3Firi%20schema%3AbyArtist%20%3FbyArtist%20.%20%7D%0A%7D%0ALIMIT%201000))

</div>

### Properties

<table style="width:99%;">
<colgroup>
<col style="width: 41%" />
<col style="width: 43%" />
<col style="width: 14%" />
</colgroup>
<thead>
<tr>
<th style="text-align: left;">Description</th>
<th style="text-align: left;">Details</th>
<th style="text-align: right;">Cardinality</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: left;"><strong>Name</strong>
(<code>schema:name</code>): Every album must have a name.</td>
<td style="text-align: left;"><ul>
<li>Type: Text (<code>xsd:string</code>)</li>
<li>Length: ≤ 200 characters</li>
</ul></td>
<td style="text-align: right;">1..1</td>
</tr>
<tr>
<td style="text-align: left;"><strong>Artist</strong>
(<code>schema:byArtist</code>): Person or music group who created the
album.</td>
<td style="text-align: left;"><ul>
<li>Type: <a href="#sec-nodeshape-personshape">Person</a> or
<code>schema:MusicGroup</code></li>
</ul></td>
<td style="text-align: right;">0..*</td>
</tr>
</tbody>
</table>

## Music Recording

A single music track in the Chinook dataset.

### Overview

<div class="ech-facts">

IRI  
<https://agriculture.ld.admin.ch/eCH-1234/2/TrackShape>

Target class  
`schema:MusicRecording`

Closed  
No (further properties are allowed)

Key figures  
3503 instances with 10 to 15 triples each (11.1 on average)

Open data  
Yes ([published on
LINDAS](https://lindas.admin.ch/sparql/#query=PREFIX%20schema%3A%20%3Chttp%3A%2F%2Fschema.org%2F%3E%0ASELECT%20%3Firi%20%3Fname%20%3FinAlbum%20%3Fauthor%20%3Fgenre%20%3Fduration%20%3FcontentSize%0AFROM%20%3Chttps%3A%2F%2Flindas.admin.ch%2Ffoag%2Fogd%3E%0AWHERE%20%7B%0A%20%20%3Firi%20a%20schema%3AMusicRecording%20.%0A%20%20%3Firi%20schema%3Aname%20%3Fname%20.%0A%20%20OPTIONAL%20%7B%20%3Firi%20schema%3AinAlbum%20%3FinAlbum%20.%20%7D%0A%20%20OPTIONAL%20%7B%20%3Firi%20schema%3Aauthor%20%3Fauthor%20.%20%7D%0A%20%20%3Firi%20schema%3Agenre%20%3Fgenre%20.%0A%20%20OPTIONAL%20%7B%20%3Firi%20schema%3Aduration%20%3Fduration%20.%20%7D%0A%20%20OPTIONAL%20%7B%20%3Firi%20schema%3AcontentSize%20%3FcontentSize%20.%20%7D%0A%7D%0ALIMIT%201000))

</div>

### Properties

<table style="width:99%;">
<colgroup>
<col style="width: 40%" />
<col style="width: 44%" />
<col style="width: 14%" />
</colgroup>
<thead>
<tr>
<th style="text-align: left;">Description</th>
<th style="text-align: left;">Details</th>
<th style="text-align: right;">Cardinality</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: left;"><strong>Name</strong>
(<code>schema:name</code>): Every track must have a name.</td>
<td style="text-align: left;"><ul>
<li>Type: Text (<code>xsd:string</code>)</li>
<li>Length: 1–200 characters</li>
</ul></td>
<td style="text-align: right;">1..1</td>
</tr>
<tr>
<td style="text-align: left;"><strong>In Album</strong>
(<code>schema:inAlbum</code>): A track can only belong to a valid
schema:MusicAlbum.</td>
<td style="text-align: left;"><ul>
<li>Type: <a href="#sec-nodeshape-musicalbumshape">Music album</a></li>
</ul></td>
<td style="text-align: right;">0..*</td>
</tr>
<tr>
<td style="text-align: left;"><strong>Author</strong>
(<code>schema:author</code>): The person or group who wrote the
track.</td>
<td style="text-align: left;"></td>
<td style="text-align: right;">0..*</td>
</tr>
<tr>
<td style="text-align: left;"><strong>Genre</strong>
(<code>schema:genre</code>)</td>
<td style="text-align: left;"><ul>
<li>Type: <a href="#sec-nodeshape-genreshape">Genre</a></li>
</ul></td>
<td style="text-align: right;">1..1</td>
</tr>
<tr>
<td style="text-align: left;"><strong>Duration</strong>
(<code>schema:duration</code>): Track duration must be expressed as a
schema:QuantitativeValue.</td>
<td style="text-align: left;"><ul>
<li>Type: <a href="#sec-nodeshape-quantitativevalueshape">Quantitative
Value</a></li>
</ul></td>
<td style="text-align: right;">0..*</td>
</tr>
<tr>
<td style="text-align: left;"><strong>Content Size</strong>
(<code>schema:contentSize</code>)</td>
<td style="text-align: left;"><ul>
<li>Type: <a href="#sec-nodeshape-quantitativevalueshape">Quantitative
Value</a></li>
</ul></td>
<td style="text-align: right;">0..*</td>
</tr>
</tbody>
</table>

## Organisation

A company or organization in the Chinook dataset.

### Overview

<div class="ech-facts">

IRI  
<https://agriculture.ld.admin.ch/eCH-1234/2/OrganisationShape>

Target class  
`schema:Organisation`

Closed  
No (further properties are allowed)

Open data  
No (transactional data, not part of the published graph)

</div>

### Properties

<table style="width:99%;">
<colgroup>
<col style="width: 41%" />
<col style="width: 43%" />
<col style="width: 14%" />
</colgroup>
<thead>
<tr>
<th style="text-align: left;">Description</th>
<th style="text-align: left;">Details</th>
<th style="text-align: right;">Cardinality</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: left;"><strong>Name</strong>
(<code>schema:name</code>): Every organisation must have a name.</td>
<td style="text-align: left;"><ul>
<li>Type: Text (<code>xsd:string</code>)</li>
<li>Length: 2–100 characters</li>
</ul></td>
<td style="text-align: right;">1..1</td>
</tr>
</tbody>
</table>

## Person

Any person (employee, customer, or custom person) present in the
dataset.

Persons are described uniformly regardless of their role: employees of
the music store, customers and manually recorded persons share the same
properties. The role follows from the relationships, for example
`schema:worksFor` for employees or `schema:customer` on an invoice for
customers.

Names are recorded as the person uses them; academic titles do not
belong in the given name. Email addresses and birth dates are optional
and rule violations are reported as warnings only.

### Overview

<div class="ech-facts">

IRI  
<https://agriculture.ld.admin.ch/eCH-1234/2/PersonShape>

Target class  
`schema:Person`

Closed  
Yes (only the listed properties are allowed)

Key figures  
383 instances with 5 to 10 triples each (5.6 on average)

Open data  
Yes ([published on
LINDAS](https://lindas.admin.ch/sparql/#query=PREFIX%20schema%3A%20%3Chttp%3A%2F%2Fschema.org%2F%3E%0ASELECT%20%3Firi%20%3FgivenName%20%3FfamilyName%20%3Femail%20%3FbirthDate%20%3Faddress%20%3FworksFor%20%3FjobTitle%20%3Fknows%0AFROM%20%3Chttps%3A%2F%2Flindas.admin.ch%2Ffoag%2Fogd%3E%0AWHERE%20%7B%0A%20%20%3Firi%20a%20schema%3APerson%20.%0A%20%20%3Firi%20schema%3AgivenName%20%3FgivenName%20.%0A%20%20%3Firi%20schema%3AfamilyName%20%3FfamilyName%20.%0A%20%20OPTIONAL%20%7B%20%3Firi%20schema%3Aemail%20%3Femail%20.%20%7D%0A%20%20OPTIONAL%20%7B%20%3Firi%20schema%3AbirthDate%20%3FbirthDate%20.%20%7D%0A%20%20OPTIONAL%20%7B%20%3Firi%20schema%3Aaddress%20%3Faddress%20.%20%7D%0A%20%20OPTIONAL%20%7B%20%3Firi%20schema%3AworksFor%20%3FworksFor%20.%20%7D%0A%20%20OPTIONAL%20%7B%20%3Firi%20schema%3AjobTitle%20%3FjobTitle%20.%20%7D%0A%20%20OPTIONAL%20%7B%20%3Firi%20schema%3Aknows%20%3Fknows%20.%20%7D%0A%7D%0ALIMIT%201000))

</div>

### Properties

<table style="width:99%;">
<colgroup>
<col style="width: 40%" />
<col style="width: 43%" />
<col style="width: 14%" />
</colgroup>
<thead>
<tr>
<th style="text-align: left;">Description</th>
<th style="text-align: left;">Details</th>
<th style="text-align: right;">Cardinality</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: left;"><strong>Given Name</strong>
(<code>schema:givenName</code>): Every person must have a given
name.</td>
<td style="text-align: left;"><ul>
<li>Type: Text (<code>xsd:string</code>)</li>
</ul></td>
<td style="text-align: right;">1..1</td>
</tr>
<tr>
<td style="text-align: left;"><strong>Family Name</strong>
(<code>schema:familyName</code>): Every person must have a family
name.</td>
<td style="text-align: left;"><ul>
<li>Type: Text (<code>xsd:string</code>)</li>
</ul></td>
<td style="text-align: right;">1..1</td>
</tr>
<tr>
<td style="text-align: left;"><strong>Email Address</strong>
(<code>schema:email</code>): If an email is provided, it must follow a
standard email format.</td>
<td style="text-align: left;"><ul>
<li>Type: Text (<code>xsd:string</code>)</li>
<li>Pattern: <code>^.+@.+\..+$</code> (<code>i</code>)</li>
<li>Length: ≤ 254 characters</li>
<li>Severity: Warning</li>
</ul></td>
<td style="text-align: right;">0..*</td>
</tr>
<tr>
<td style="text-align: left;"><strong>Birth date</strong>
(<code>schema:birthDate</code>): A person should have a valid birth
date.</td>
<td style="text-align: left;"><ul>
<li>Type: Date (<code>xsd:date</code>)</li>
<li>Range: ≥ 1900-01-01, ≤ 2025-12-31</li>
<li>Severity: Warning</li>
</ul></td>
<td style="text-align: right;">0..*</td>
</tr>
<tr>
<td style="text-align: left;"><strong>Address</strong>
(<code>schema:address</code>)</td>
<td style="text-align: left;"><ul>
<li>Type: <a href="#sec-nodeshape-postaladdressshape">Postal
address</a></li>
</ul></td>
<td style="text-align: right;">0..*</td>
</tr>
<tr>
<td style="text-align: left;"><strong>Works for</strong>
(<code>schema:worksFor</code>): An employee can report to another
person.</td>
<td style="text-align: left;"><ul>
<li>Type: <a href="#sec-nodeshape-personshape">Person</a> or
<code>schema:Organization</code></li>
</ul></td>
<td style="text-align: right;">0..*</td>
</tr>
<tr>
<td style="text-align: left;"><strong>Job title</strong>
(<code>schema:jobTitle</code>)</td>
<td style="text-align: left;"><ul>
<li>Type: Text (<code>xsd:string</code>)</li>
<li>Length: 2–100 characters</li>
</ul></td>
<td style="text-align: right;">0..1</td>
</tr>
<tr>
<td style="text-align: left;"><strong>knows</strong>
(<code>schema:knows</code>)</td>
<td style="text-align: left;"><ul>
<li>Type: <a href="#sec-nodeshape-personshape">Person</a></li>
</ul></td>
<td style="text-align: right;">0..*</td>
</tr>
</tbody>
</table>

### Rules (SPARQL)

#### No self-reporting

An employee cannot report to themselves.

``` sparql
SELECT $this
WHERE {
    $this schema:worksFor $this .
}
```

## Postal address

The postal address of a person.

Addresses follow the structure of schema.org rather than the Swiss
address standard eCH-0010, since the dataset contains mostly foreign
addresses. Postal codes are therefore only checked for a plausible
format, not against a directory.

### Overview

<div class="ech-facts">

IRI  
<https://agriculture.ld.admin.ch/eCH-1234/2/PostalAddressShape>

Target class  
`schema:PostalAddress`

Closed  
Yes (only the listed properties are allowed)

Key figures  
67 instances with 6 to 8 triples each (7.5 on average)

Open data  
Yes ([published on
LINDAS](https://lindas.admin.ch/sparql/#query=PREFIX%20schema%3A%20%3Chttp%3A%2F%2Fschema.org%2F%3E%0ASELECT%20%3Firi%20%3FstreetAddress%20%3FpostalCode%20%3FaddressLocality%20%3FaddressRegion%20%3FaddressCountry%0AFROM%20%3Chttps%3A%2F%2Flindas.admin.ch%2Ffoag%2Fogd%3E%0AWHERE%20%7B%0A%20%20%3Firi%20a%20schema%3APostalAddress%20.%0A%20%20%3Firi%20schema%3AstreetAddress%20%3FstreetAddress%20.%0A%20%20OPTIONAL%20%7B%20%3Firi%20schema%3ApostalCode%20%3FpostalCode%20.%20%7D%0A%20%20%3Firi%20schema%3AaddressLocality%20%3FaddressLocality%20.%0A%20%20OPTIONAL%20%7B%20%3Firi%20schema%3AaddressRegion%20%3FaddressRegion%20.%20%7D%0A%20%20%3Firi%20schema%3AaddressCountry%20%3FaddressCountry%20.%0A%7D%0ALIMIT%201000))

</div>

### Properties

<table style="width:99%;">
<colgroup>
<col style="width: 41%" />
<col style="width: 43%" />
<col style="width: 14%" />
</colgroup>
<thead>
<tr>
<th style="text-align: left;">Description</th>
<th style="text-align: left;">Details</th>
<th style="text-align: right;">Cardinality</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: left;"><strong>Street address</strong>
(<code>schema:streetAddress</code>)</td>
<td style="text-align: left;"><ul>
<li>Type: Text (<code>xsd:string</code>)</li>
<li>Length: 3–100 characters</li>
<li>Examples: Schwarzenburgstrasse 165</li>
</ul></td>
<td style="text-align: right;">1..1</td>
</tr>
<tr>
<td style="text-align: left;"><strong>Postal code</strong>
(<code>schema:postalCode</code>): Letters, digits, spaces and hyphens,
two to ten characters.</td>
<td style="text-align: left;"><ul>
<li>Type: Text (<code>xsd:string</code>)</li>
<li>Pattern: <code>^[A-Za-z0-9][A-Za-z0-9 -]{1,9}$</code></li>
<li>Severity: Warning</li>
</ul></td>
<td style="text-align: right;">0..1</td>
</tr>
<tr>
<td style="text-align: left;"><strong>Locality</strong>
(<code>schema:addressLocality</code>): Every address needs exactly one
locality.</td>
<td style="text-align: left;"><ul>
<li>Type: Text (<code>xsd:string</code>)</li>
<li>Length: ≤ 100 characters</li>
</ul></td>
<td style="text-align: right;">1..1</td>
</tr>
<tr>
<td style="text-align: left;"><strong>Region</strong>
(<code>schema:addressRegion</code>): Canton, state or province where
customary in the country.</td>
<td style="text-align: left;"><ul>
<li>Type: Text (<code>xsd:string</code>)</li>
<li>Length: ≤ 100 characters</li>
</ul></td>
<td style="text-align: right;">0..1</td>
</tr>
<tr>
<td style="text-align: left;"><strong>Country</strong>
(<code>schema:addressCountry</code>): Country as an IRI from the country
list of the Swiss Federal Archives on LINDAS (ISO 3166-1 alpha-3).</td>
<td style="text-align: left;"><ul>
<li>Pattern: <code>^https://ld\.admin\.ch/country/[A-Z]{3}$</code></li>
<li>Examples: <code>country:CHE</code>, <code>country:FRA</code>,
<code>country:ITA</code></li>
</ul></td>
<td style="text-align: right;">1..1</td>
</tr>
</tbody>
</table>

## Quantitative Value

A numerical value with an associated unit.

Quantitative values are never recorded as a bare number but always
together with a unit from the QUDT vocabulary. This keeps it unambiguous
whether a duration is meant in milliseconds or a file size in bytes.
Negative values are not foreseen in this dataset.

### Overview

<div class="ech-facts">

IRI  
<https://agriculture.ld.admin.ch/eCH-1234/2/QuantitativeValueShape>

Target class  
`schema:QuantitativeValue`

Closed  
Yes (only the listed properties are allowed)

Key figures  
15401 instances with 3 triples each

Open data  
Yes ([published on
LINDAS](https://lindas.admin.ch/sparql/#query=PREFIX%20schema%3A%20%3Chttp%3A%2F%2Fschema.org%2F%3E%0ASELECT%20%3Firi%20%3Fvalue%20%3FunitCode%0AFROM%20%3Chttps%3A%2F%2Flindas.admin.ch%2Ffoag%2Fogd%3E%0AWHERE%20%7B%0A%20%20%3Firi%20a%20schema%3AQuantitativeValue%20.%0A%20%20%3Firi%20schema%3Avalue%20%3Fvalue%20.%0A%20%20%3Firi%20schema%3AunitCode%20%3FunitCode%20.%0A%7D%0ALIMIT%201000))

</div>

### Properties

<table style="width:99%;">
<colgroup>
<col style="width: 41%" />
<col style="width: 43%" />
<col style="width: 14%" />
</colgroup>
<thead>
<tr>
<th style="text-align: left;">Description</th>
<th style="text-align: left;">Details</th>
<th style="text-align: right;">Cardinality</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: left;"><strong>Value</strong>
(<code>schema:value</code>): A quantitative value must have exactly one
numeric value.</td>
<td style="text-align: left;"><ul>
<li>Type: Decimal number (<code>xsd:decimal</code>) or Integer
(<code>xsd:integer</code>)</li>
<li>Range: ≥ 0</li>
</ul></td>
<td style="text-align: right;">1..1</td>
</tr>
<tr>
<td style="text-align: left;"><strong>Unit Code</strong>
(<code>schema:unitCode</code>): A quantitative value must specify its
unit via a unitCode URI.</td>
<td style="text-align: left;"><ul>
<li>Values: <code>unit:USD</code>, <code>unit:EA</code>,
<code>unit:BYTE</code>, <code>unit:MilliSEC</code></li>
</ul></td>
<td style="text-align: right;">1..1</td>
</tr>
</tbody>
</table>

# Data Retrieval

The master and reference data underlying this document are available as
*Linked Data*.

The technological basis for this is the Resource Description Framework
\[RDF, RDF\], a central standard of the World Wide Web Consortium (W3C)
for modeling data structures on the web. In RDF, information is not
represented in classic tables, but as interconnected graphs. Each
statement consists of a so-called triple (subject, predicate, object).
This structure enables a machine-readable, interoperable, and
cross-system unambiguous description of resources and their relations to
one another.

For the storage and publication of this RDF data,
[LINDAS](https://lindas.admin.ch/) (Linked Data Service) is used, the
official Linked Data service of the Swiss Federal Administration. LINDAS
functions as a so-called *triple store*, a specialized graph database
optimized for the efficient storage and querying of RDF triples, which
makes the data publicly available via a standardized interface.

The following chapter provides minimal instructions on how the data can
be queried and retrieved from LINDAS.

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

The underlying data itself is maintained on GitHub as Turtle files.

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

# Safety considerations

Information about the explicitly relevant legal bases or a note that
during the implementation the rele-vant legal bases must be observed.

# Disclaimer

eCH-standards which the registered association eCH provides the user
free of charge or which make reference to eCH shall only have the status
of recommendations. The registered association eCH will not be liable in
any event for any decisions made or measures taken by the user based on
these documents. The user will be responsible for verifying the
documents himself prior to their use and to seek advice if required.
eCH-standards can and shall not replace the technical, organizational or
legal advice in the individual case.

Documents, procedures, methods, products and standards that are made
reference to in eCH-standards are possibly protected by trademarks,
copyrights or patents. It is the exclusive responsibil-ity of the user
to obtain the necessary licences from the entitled persons and/or
organizations.

Although the registered association eCH has taken adequate care to
prepare the eCH-standards with due diligence, it cannot grant any
warranty or guarantee that the information and documents provided are
up-to-date, complete, true or without any errors. eCH reserves the right
to change the contents of the eCH-standards at any time and without
prior announcement.

Any liability for damage caused by the use of the eCH-standards by the
user shall be excluded to the extent legally admissible.

# Copyrights

Persons preparing eCH-standards shall remain the owners of their
intellectual property rights. These persons, however, obligate
themselves to provide their intellectual property rights or other rights
in third party intellectual property rights, to the extent possible, to
the relevant technical units and the registered association eCH for free
and for unlimited use and further development as part of the purpose of
the association.

The standards prepared by the technical units can be used, distributed
and developed further for free and to an unlimited extent by stating the
name of the respective author of eCH.

eCH-standards are fully documented and free of any restrictions of
licence and/or patent law. The associated documentation can be requested
for free. These provisions shall apply to the standards prepared by eCH
only, however, not to any standards or products of third parties which
include reference to eCH-standards. The standards include the relevant
references to third party rights.

# Annex A – References

<div id="refs" class="references csl-bib-body">

<div id="ref-berners2023semantic" class="csl-entry">

<span class="csl-left-margin">\[Berners-Lee 2023\]
</span><span class="csl-right-inline">Berners-Lee, Tim ; Hendler,
James ; Lassila, Ora: [The Semantic Web: A new form of Web content that
is meaningful to computers will unleash a revolution of new
possibilities](https://doi.org/10.1145/3591366.3591376). In: *Linking
the World’s Information: Essays on Tim Berners-Lee’s Invention of the
World Wide Web* : Association for Computing Machinery, 2023,
pp. 91–103</span>

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

# Annex B – Cooperation and Verification

| Name              | Organisation                   |
|:------------------|:-------------------------------|
| Damian Oswald     | Federal Office for Agriculture |
| Michael Schüpbach | Federal Office for Agriculture |
| Lea Stauber       | Federal Office for Agriculture |

# Annex C – Abbreviations and Glossary

This glossary is also available in machine-readable form as a SKOS
glossary \[SKOS\], on [LINDAS](https://lindas.admin.ch/) and in the
[GitHub
repository](https://github.com/blw-ofag-ufag/semantic-web-template/blob/main/src/rdf/data/glossary.skos.ttl).

<div id="tbl-glossary">

Table 3: Glossary of the eCH-1234 standard

<table>
<colgroup>
<col style="width: 35%" />
<col style="width: 65%" />
</colgroup>
<thead>
<tr>
<th style="text-align: left;">Term</th>
<th style="text-align: left;">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: left;"><strong>Graph</strong> (Named graph)</td>
<td style="text-align: left;"><p>A set of triples. A named graph is
itself identified by an IRI and allows data in a triple store to be
grouped.</p>
<p><em>Broader</em>: Resource Description Framework</p></td>
</tr>
<tr>
<td style="text-align: left;"><strong>Internationalized Resource
Identifier</strong> (IRI)</td>
<td style="text-align: left;"><p>Globally unique identifier of a
resource. In RDF, subjects, predicates and most objects are identified
by IRIs.</p>
<p><em>Broader</em>: Resource Description Framework</p></td>
</tr>
<tr>
<td style="text-align: left;"><strong>JSON for Linking Data</strong>
(JSON-LD)</td>
<td style="text-align: left;"><p>A serialization of RDF based on JSON,
particularly suited to web interfaces.</p>
<p><em>Broader</em>: Serialization</p></td>
</tr>
<tr>
<td style="text-align: left;"><strong>Linked Data</strong> (Linked Open
Data)</td>
<td style="text-align: left;"><p>Data published according to the
principles of the Semantic Web: identified by IRIs, described in RDF and
linked to one another.</p>
<p><em>Related</em>: Linked Data Service, Resource Description
Framework</p></td>
</tr>
<tr>
<td style="text-align: left;"><strong>Linked Data Service</strong>
(LINDAS)</td>
<td style="text-align: left;">The official Linked Data service of the
Swiss Federal Administration, acting as a triple store.</td>
</tr>
<tr>
<td style="text-align: left;"><strong>Literal</strong></td>
<td style="text-align: left;"><p>A concrete value in RDF, such as a
string, a number or a date, optionally with a datatype or a language
tag.</p>
<p><em>Broader</em>: Resource Description Framework</p></td>
</tr>
<tr>
<td style="text-align: left;"><strong>Namespace</strong> (Prefix)</td>
<td style="text-align: left;"><p>Common beginning of a group of IRIs. In
Turtle and SPARQL, a namespace is abbreviated by a prefix, for example
<code>schema:</code> for <code>http://schema.org/</code>.</p>
<p><em>Related</em>: Internationalized Resource Identifier</p></td>
</tr>
<tr>
<td style="text-align: left;"><strong>Ontology</strong></td>
<td style="text-align: left;"><p>A formal model of a domain that
describes classes, properties and their logical relationships in a way
that allows machines to draw conclusions.</p>
<p><em>Broader</em>: Vocabulary</p>
<p><em>Related</em>: Web Ontology Language</p></td>
</tr>
<tr>
<td style="text-align: left;"><strong>Reasoning</strong>
(Inference)</td>
<td style="text-align: left;">The automatic derivation of new statements
from the existing data and the axioms of an ontology, for example by the
HermiT reasoner.</td>
</tr>
<tr>
<td style="text-align: left;"><strong>Resource Description
Framework</strong> (RDF)</td>
<td style="text-align: left;">A central standard of the World Wide Web
Consortium (W3C) for modeling data structures on the Web. Information is
represented as networked graphs rather than in traditional tables.</td>
</tr>
<tr>
<td style="text-align: left;"><strong>Serialization</strong></td>
<td style="text-align: left;"><p>Textual representation of an RDF graph
in a defined format, used to store or exchange it.</p>
<p><em>Narrower</em>: JSON for Linking Data, Terse RDF Triple
Language</p></td>
</tr>
<tr>
<td style="text-align: left;"><strong>Shape</strong></td>
<td style="text-align: left;"><p>A set of conditions that a class of
resources or a property must fulfil, such as mandatory fields, datatypes
and cardinalities.</p>
<p><em>Broader</em>: Shapes Constraint Language</p></td>
</tr>
<tr>
<td style="text-align: left;"><strong>Shapes Constraint
Language</strong> (SHACL)</td>
<td style="text-align: left;"><p>The W3C language for describing and
validating the structure of RDF data. The data model of this standard is
formulated in SHACL.</p>
<p><em>Narrower</em>: Shape</p></td>
</tr>
<tr>
<td style="text-align: left;"><strong>Simple Knowledge Organization
System</strong> (SKOS)</td>
<td style="text-align: left;"><p>A W3C vocabulary for thesauri,
classifications and glossaries. This glossary is itself recorded in
SKOS.</p>
<p><em>Related</em>: Vocabulary</p></td>
</tr>
<tr>
<td style="text-align: left;"><strong>SPARQL endpoint</strong></td>
<td style="text-align: left;"><p>A web interface through which SPARQL
queries can be sent to a triple store.</p>
<p><em>Broader</em>: SPARQL Protocol and RDF Query Language</p></td>
</tr>
<tr>
<td style="text-align: left;"><strong>SPARQL Protocol and RDF Query
Language</strong> (SPARQL)</td>
<td style="text-align: left;"><p>The W3C query language for RDF data.
SPARQL is used to read data from graphs, modify them and exchange them
between systems.</p>
<p><em>Related</em>: Resource Description Framework</p></td>
</tr>
<tr>
<td style="text-align: left;"><strong>Terse RDF Triple Language</strong>
(Turtle)</td>
<td style="text-align: left;"><p>A compact, human-readable serialization
for RDF. All RDF files of this standard are written in Turtle.</p>
<p><em>Broader</em>: Serialization</p></td>
</tr>
<tr>
<td style="text-align: left;"><strong>Triple</strong></td>
<td style="text-align: left;"><p>The basic structure of a statement in
RDF, consisting of a subject, predicate, and object.</p>
<p><em>Broader</em>: Resource Description Framework</p></td>
</tr>
<tr>
<td style="text-align: left;"><strong>Triple store</strong> (Graph
database)</td>
<td style="text-align: left;"><p>A database specialised in storing and
querying RDF triples.</p>
<p><em>Related</em>: Linked Data Service</p></td>
</tr>
<tr>
<td style="text-align: left;"><strong>Vocabulary</strong></td>
<td style="text-align: left;"><p>A collection of classes and properties
with defined meaning that is reused to describe data, for example
schema.org.</p>
<p><em>Narrower</em>: Ontology</p></td>
</tr>
<tr>
<td style="text-align: left;"><strong>Web Ontology Language</strong>
(OWL)</td>
<td style="text-align: left;"><p>The W3C language for formulating
ontologies. It allows classes and properties to be defined with logical
axioms.</p>
<p><em>Related</em>: Reasoning</p></td>
</tr>
</tbody>
</table>

</div>

# Annex D – Changes in comparison to previous version

The most important changes of version 2.0.0 compared to the previous
version 1.4.6:

- **Document template:** the PDF output now follows the eCH document
  template (title page with metadata table, header and footer, table of
  contents, annexes); the website adopts the same style in a light and a
  dark variant.
- **Metadata:** number, category, quality stage, version, status and
  further details of the standard are recorded once and inserted
  automatically into all language versions, the title page, the footer
  and <a href="#sec-status" class="quarto-xref">Section 1.1</a>.
- **Lists:** the table of figures and the table of tables (Annexes E
  and F) are generated automatically and linked to the figures and
  tables.
- **Presentation:** uniform styling of tables, captions and code in the
  PDF and on the website.

A complete list of all changes per version can be found in the [releases
on
GitHub](https://github.com/blw-ofag-ufag/semantic-web-template/releases).

# Annex E – Table of figures

# Annex F – Table of tables

[^1]: On the website, footnotes appear in the right margin; in the PDF,
    at the bottom of the page.

[^2]: A second footnote with a link to [ech.ch](https://www.ech.ch/).
