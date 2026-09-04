# eCH-1234 Template Quarto Document

September 4, 2026

- [Note](#sec-note)
- [<span class="toc-section-number">1</span>
  Introduction](#sec-introduction)
  - [<span class="toc-section-number">1.1</span> Status](#sec-status)
  - [<span class="toc-section-number">1.2</span> Scope of
    application](#sec-scope-of-application)
  - [<span class="toc-section-number">1.3</span> We can have
    sub-headings](#sec-example-subheading)
- [<span class="toc-section-number">2</span> Technical
  notes](#sec-technical-notes)
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
  - [<span class="toc-section-number">3.7</span> Quantitative
    Value](#sec-nodeshape-quantitativevalueshape)
- [<span class="toc-section-number">4</span> Data
  Retrieval](#sec-data-retrieval)
- [<span class="toc-section-number">5</span> Safety
  considerations](#sec-safety-consideration)
- [<span class="toc-section-number">6</span>
  Disclaimer](#sec-disclaimer)
- [<span class="toc-section-number">7</span>
  Copyrights](#sec-copyrights)
- [<span class="toc-section-number">8</span> Annex A -
  References](#sec-appendix-a)
- [<span class="toc-section-number">9</span> Annex B - Cooperation and
  Verification](#sec-appendix-b)
- [<span class="toc-section-number">10</span> Annex C - Abbreviations
  and Glossary](#sec-appendix-c)
- [<span class="toc-section-number">11</span> Annex D - Changes in
  comparison to previous version](#sec-appendix-d)
- [<span class="toc-section-number">12</span> Annex E - Table of
  figures](#sec-appendix-e)
- [<span class="toc-section-number">13</span> Annex F - Table of
  tables](#sec-appendix-f)

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

Approved: This document was approved by the Experts’ Committee. It has
normative power for the defined field of application in the determined
scope of application.

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

Figure 1: Always add some text to describe what the image shows.

</div>

When displaying diagrams, try to write them in Mermaid JS straight away;
this makes changes in the future or translations straightforward.

# Technical notes

We use the ROBOT CLI in our project (Jackson et al. 2019), especially
for it’s ability to run the HermiT reasoner (Glimm et al. 2014).

# Data Model

## Genre

A musical category in the Chinook dataset.

**Target Class:** `:Genre`

<div id="tbl-nodeshape-genreshape">

Table 1: properties Genre

| Description | Path | Type | Cardinality |
|:---|:---|:---|---:|
| **Name** | `schema:name` |  | 1..1 |
| **Part of** | `schema:partOf` | [`:Genre`](#sec-nodeshape-genreshape) or `sh:IRI` | 0..\* |

</div>

## Invoice

A purchase receipt in the Chinook dataset.

**Target Class:** `schema:Invoice`

<div id="tbl-nodeshape-invoiceshape">

Table 2: properties Invoice

| Description | Path | Type | Cardinality |
|:---|:---|:---|---:|
| **Customer**: An invoice must be linked to exactly one customer. | `schema:customer` | [`schema:Person`](#sec-nodeshape-personshape) | 1..1 |
| **Total payment due**: An invoice must define a total payment due as a schema:QuantitativeValue. | `schema:totalPaymentDue` | [`schema:QuantitativeValue`](#sec-nodeshape-quantitativevalueshape) | 1..1 |
| **Has part**: An invoice must have at least one line item (OrderItem). | `schema:hasPart` | `schema:OrderItem` | 1..\* |
| **Date created** | `schema:dateCreated` | `xsd:date` | 0..\* |

</div>

## Music album

A collection of tracks in the Chinook dataset.

**Target Class:** `schema:MusicAlbum`

<div id="tbl-nodeshape-musicalbumshape">

Table 3: properties Music album

| Description | Path | Type | Cardinality |
|:---|:---|:---|---:|
| **Name**: Every album must have a name. | `schema:name` | `xsd:string` | 1..1 |
| **Artist**: Person or music group who created the album. | `schema:byArtist` | [`schema:Person`](#sec-nodeshape-personshape) or `schema:MusicGroup` | 0..\* |

</div>

## Music Recording

A single music track in the Chinook dataset.

**Target Class:** `schema:MusicRecording`

<div id="tbl-nodeshape-trackshape">

Table 4: properties Music Recording

| Description | Path | Type | Cardinality |
|:---|:---|:---|---:|
| **Name**: Every track must have a name. | `schema:name` | `xsd:string` | 1..1 |
| **In Album**: A track can only belong to a valid schema:MusicAlbum. | `schema:inAlbum` | [`schema:MusicAlbum`](#sec-nodeshape-musicalbumshape) | 0..\* |
| **Author**: The person or group who wrote the track. | `schema:author` |  | 0..\* |
| **Genre** | `schema:genre` | [`:Genre`](#sec-nodeshape-genreshape) | 1..1 |
| **Duration**: Track duration must be expressed as a schema:QuantitativeValue. | `schema:duration` | [`schema:QuantitativeValue`](#sec-nodeshape-quantitativevalueshape) | 0..\* |
| **Content Size** | `schema:contentSize` | [`schema:QuantitativeValue`](#sec-nodeshape-quantitativevalueshape) | 0..\* |

</div>

## Organisation

A company or organization in the Chinook dataset.

**Target Class:** `schema:Organisation`

<div id="tbl-nodeshape-organisationshape">

Table 5: properties Organisation

| Description | Path | Type | Cardinality |
|:---|:---|:---|---:|
| **Name**: Every organisation must have a name. | `schema:name` | `xsd:string` | 1..1 |

</div>

## Person

Any person (employee, customer, or custom person) present in the
dataset.

**Target Class:** `schema:Person`

<div id="tbl-nodeshape-personshape">

Table 6: properties Person

| Description | Path | Type | Cardinality |
|:---|:---|:---|---:|
| **Given Name**: Every person must have a given name. | `schema:givenName` | `xsd:string` | 1..1 |
| **Family Name**: Every person must have a family name. | `schema:familyName` | `xsd:string` | 1..1 |
| **Email Address**: If an email is provided, it must follow a standard email format. | `schema:email` | `xsd:string` | 0..\* |
| **Birth date**: A person should have a valid birth date. | `schema:birthDate` | `xsd:date` | 0..\* |
| **Address** | `schema:address` | `schema:PostalAddress` | 0..\* |
| **Works for**: An employee can report to another person. | `schema:worksFor` | [`schema:Person`](#sec-nodeshape-personshape) or `schema:Organization` | 0..\* |
| **Job title** | `schema:jobTitle` |  | 0..1 |
| **knows** | `schema:knows` | [`schema:Person`](#sec-nodeshape-personshape) | 0..\* |

</div>

## Quantitative Value

A numerical value with an associated unit.

**Target Class:** `schema:QuantitativeValue`

<div id="tbl-nodeshape-quantitativevalueshape">

Table 7: properties Quantitative Value

| Description | Path | Type | Cardinality |
|:---|:---|:---|---:|
| **Value**: A quantitative value must have exactly one numeric value. | `schema:value` |  | 1..1 |
| **Unit Code**: A quantitative value must specify its unit via a unitCode URI. | `schema:unitCode` | `sh:IRI` | 1..1 |

</div>

# Data Retrieval

The master and reference data underlying this document are available as
*Linked Data*.

The technological basis for this is the Resource Description Framework
(RDF, Cyganiak et al. 2014), a central standard of the World Wide Web
Consortium (W3C) for modeling data structures on the web. In RDF,
information is not represented in classic tables, but as interconnected
graphs. Each statement consists of a so-called triple (subject,
predicate, object). This structure enables a machine-readable,
interoperable, and cross-system unambiguous description of resources and
their relations to one another.

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

# Annex A - References

<div id="refs" class="references csl-bib-body hanging-indent">

<div id="ref-cyganiak2014rdf11" class="csl-entry">

Cyganiak, Richard, David Wood, and Markus Lanthaler. 2014. *RDF 1.1
Concepts and Abstract Syntax*. W3C Recommendation. World Wide Web
Consortium (W3C). <https://www.w3.org/TR/rdf11-concepts/>.

</div>

<div id="ref-glimm2014hermit" class="csl-entry">

Glimm, Birte, Ian Horrocks, Boris Motik, Giorgos Stoilos, and Zhe Wang.
2014. “HermiT: An OWL 2 Reasoner.” *Journal of Automated Reasoning* 53
(3): 245–69.

</div>

<div id="ref-jackson2019robot" class="csl-entry">

Jackson, Rebecca C, James P Balhoff, Eric Douglass, Nomi L Harris,
Christopher J Mungall, and James A Overton. 2019. “ROBOT: A Tool for
Automating Ontology Workflows.” *BMC Bioinformatics* 20 (1): 407.
<https://doi.org/10.1186/s12859-019-3002-3>.

</div>

</div>

# Annex B - Cooperation and Verification

# Annex C - Abbreviations and Glossary

<div id="tbl-glossary">

Table 8: Glossary of the eCH-1234 standard

| IRI | Term | Description | Relations |
|:---|:---|:---|:---|
| [`term:lindas`](https://agriculture.ld.admin.ch/eCH-1234/2/term/lindas) | **Linked Data Service** (LINDAS) | The official Linked Data service of the Swiss Federal Administration, acting as a triple store. |  |
| [`term:rdf`](https://agriculture.ld.admin.ch/eCH-1234/2/term/rdf) | **Resource Description Framework** (RDF) | A central standard of the World Wide Web Consortium (W3C) for modeling data structures on the Web. Information is represented as networked graphs rather than in traditional tables. |  |
| [`term:triple`](https://agriculture.ld.admin.ch/eCH-1234/2/term/triple) | **Triple** | The basic structure of a statement in RDF, consisting of a subject, predicate, and object. | *broader*: [`term:rdf`](https://agriculture.ld.admin.ch/eCH-1234/2/term/rdf) |

</div>

# Annex D - Changes in comparison to previous version

# Annex E - Table of figures

# Annex F - Table of tables
