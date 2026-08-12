# Modèle de document Quarto eCH-1234

12 août 2026

- [Remarque](#remarque)
- [<span class="toc-section-number">1</span>
  Introduction](#introduction)
  - [<span class="toc-section-number">1.1</span> Statut](#statut)
  - [<span class="toc-section-number">1.2</span> Champ
    d’application](#champ-dapplication)
  - [<span class="toc-section-number">1.3</span> Nous pouvons avoir des
    sous-titres](#nous-pouvons-avoir-des-sous-titres)
    - [<span class="toc-section-number">1.3.1</span> Et aussi des
      sous-sous-titres](#et-aussi-des-sous-sous-titres)
- [<span class="toc-section-number">2</span> Notes
  techniques](#notes-techniques)
- [<span class="toc-section-number">3</span> Modèle de
  données](#modèle-de-données)
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
- [<span class="toc-section-number">4</span> Considérations de
  sécurité](#considérations-de-sécurité)
- [<span class="toc-section-number">5</span> Clause de
  non-responsabilité](#clause-de-non-responsabilité)
- [<span class="toc-section-number">6</span> Droits
  d’auteur](#droits-dauteur)
- [<span class="toc-section-number">7</span> Annexe A -
  Références](#annexe-a---références)
- [<span class="toc-section-number">8</span> Annexe B - Collaboration &
  Vérification](#annexe-b---collaboration--vérification)
- [<span class="toc-section-number">9</span> Annexe C - Abréviations et
  glossaire](#annexe-c---abréviations-et-glossaire)
- [<span class="toc-section-number">10</span> Annexe D - Modifications
  par rapport à la version
  précédente](#annexe-d---modifications-par-rapport-à-la-version-précédente)
- [<span class="toc-section-number">11</span> Annexe E - Table des
  illustrations](#annexe-e---table-des-illustrations)
- [<span class="toc-section-number">12</span> Annexe F - Liste des
  tableaux](#annexe-f---liste-des-tableaux)

# Remarque

Dans le présent document, les désignations de personnes sont formulées
de manière épicène (neutre du point de vue du genre). Le guide de la
Chancellerie fédérale sert de base. Selon la situation, on utilise des
formulations paires (citoyennes et citoyens), des formes abstraites
(personne assurée), des formes neutres ou des périphrases sans référence
à la personne. L’usage du masculin générique n’est pas autorisé. Les
formes complètes sont employées dans le texte continu, c’est-à-dire dans
les textes composés de phrases rédigées. Dans les passages de texte
raccourcis, notamment dans les tableaux, des formes abrégées peuvent
être utilisées. La forme abrégée s’utilise alors avec une barre oblique,
mais sans trait d’omission (rapporteur/euse). L’astérisque de genre et
les typographies similaires ne sont pas utilisés.

# Introduction

## Statut

Approuvé : Ce document a été approuvé par le comité d’experts. Il a
force normative pour le domaine d’application défini et dans le champ
d’application déterminé.

## Champ d’application

Les informations de ce chapitre doivent donner au lecteur un aperçu
rapide de ce à quoi ce standard est destiné. Des indications sur les
éléments suivants peuvent s’avérer utiles.

## Nous pouvons avoir des sous-titres

Et écrire un peu de texte.

### Et aussi des sous-sous-titres

Et écrire encore plus de texte. Peut-être même avec une belle image.

<div id="fig-example">

![](https://fastly.picsum.photos/id/653/536/354.jpg?hmac=3InR8I5KmwbdkPHehlM8BMPd_BDHG_RWZkxt_IkeQGY)

Figure 1: Ajoutez toujours du texte pour décrire ce que montre l’image.

</div>

Lors de la présentation de diagrammes, essayez de les créer directement
dans Mermaid JS ; cela facilite grandement les modifications futures ou
les traductions.

# Notes techniques

Nous utilisons l’interface en ligne de commande (CLI) ROBOT dans notre
projet (Jackson et al. 2019), en particulier pour sa capacité à exécuter
le raisonneur HermiT (Glimm et al. 2014).

# Modèle de données

## :GenreShape

**Classe cible:** `:Genre`

<div id="tbl-genreshape">

Table 1: :GenreShape propriétés

| Description | Chemin | Type | Cardinalité |
|:---|:---|:---|---:|
|  | `schema:name` |  | 1..1 |
|  | `schema:partOf` | [:Genre](#sec-genreshape) ou `sh:IRI` | 0..\* |

</div>

## :InvoiceShape

**Classe cible:** `schema:Invoice`

<div id="tbl-invoiceshape">

Table 2: :InvoiceShape propriétés

| Description | Chemin | Type | Cardinalité |
|:---|:---|:---|---:|
| An invoice must be linked to exactly one customer. | `schema:customer` | [schema:Person](#sec-personshape) | 1..1 |
| An invoice must define a total payment due as a schema:QuantitativeValue. | `schema:totalPaymentDue` | [schema:QuantitativeValue](#sec-quantitativevalueshape) | 1..1 |
| An invoice must have at least one line item (OrderItem). | `schema:hasPart` | `schema:OrderItem` | 1..\* |
|  | `schema:dateCreated` | `xsd:date` | 0..\* |

</div>

## :MusicAlbumShape

**Classe cible:** `schema:MusicAlbum`

<div id="tbl-musicalbumshape">

Table 3: :MusicAlbumShape propriétés

| Description | Chemin | Type | Cardinalité |
|:---|:---|:---|---:|
| Every album must have a name. | `schema:name` | `xsd:string` | 1..1 |
|  | `schema:byArtist` | [schema:Person](#sec-personshape) ou `schema:MusicGroup` | 0..\* |

</div>

## :OrganisationShape

**Classe cible:** `schema:Organisation`

<div id="tbl-organisationshape">

Table 4: :OrganisationShape propriétés

| Description                          | Chemin        | Type         | Cardinalité |
|:-------------------------------------|:--------------|:-------------|------------:|
| Every organisation must have a name. | `schema:name` | `xsd:string` |        1..1 |

</div>

## :PersonShape

**Classe cible:** `schema:Person`

<div id="tbl-personshape">

Table 5: :PersonShape propriétés

| Description | Chemin | Type | Cardinalité |
|:---|:---|:---|---:|
| Every person must have a given name. | `schema:givenName` | `xsd:string` | 1..1 |
| Every person must have a family name. | `schema:familyName` | `xsd:string` | 1..1 |
| If an email is provided, it must follow a standard email format. | `schema:email` | `xsd:string` | 0..\* |
| A person should have a valid birth date. | `schema:birthDate` | `xsd:date` | 0..\* |
|  | `schema:address` | `schema:PostalAddress` | 0..\* |
| An employee can report to another person. | `schema:worksFor` | [schema:Person](#sec-personshape) ou `schema:Organization` | 0..\* |
|  | `schema:jobTitle` |  | 0..1 |
|  | `schema:knows` | [schema:Person](#sec-personshape) | 0..\* |

</div>

## :QuantitativeValueShape

**Classe cible:** `schema:QuantitativeValue`

<div id="tbl-quantitativevalueshape">

Table 6: :QuantitativeValueShape propriétés

| Description | Chemin | Type | Cardinalité |
|:---|:---|:---|---:|
| A quantitative value must have exactly one numeric value. | `schema:value` |  | 1..1 |
| A quantitative value must specify its unit via a unitCode URI. | `schema:unitCode` | `sh:IRI` | 1..1 |

</div>

## :TrackShape

**Classe cible:** `schema:MusicRecording`

<div id="tbl-trackshape">

Table 7: :TrackShape propriétés

| Description | Chemin | Type | Cardinalité |
|:---|:---|:---|---:|
| Every track must have a name. | `schema:name` | `xsd:string` | 1..1 |
| A track can only belong to a valid schema:MusicAlbum. | `schema:inAlbum` | [schema:MusicAlbum](#sec-musicalbumshape) | 0..\* |
|  | `schema:author` |  | 0..\* |
|  | `schema:genre` | [:Genre](#sec-genreshape) | 1..1 |
| Track duration must be expressed as a schema:QuantitativeValue. | `schema:duration` | [schema:QuantitativeValue](#sec-quantitativevalueshape) | 0..\* |
|  | `schema:contentSize` | [schema:QuantitativeValue](#sec-quantitativevalueshape) | 0..\* |

</div>

# Considérations de sécurité

Informations sur les bases légales expressément déterminantes ou
remarque indiquant que les bases légales pertinentes doivent être
respectées lors de la mise en œuvre.

# Clause de non-responsabilité

Les standards eCH que l’association eCH met gratuitement à la
disposition de l’utilisateur ou qui font référence à eCH n’ont que le
statut de recommandations. L’association eCH décline toute
responsabilité pour les décisions ou mesures prises par l’utilisateur
sur la base de ces documents. Il incombe à l’utilisateur de vérifier
lui-même les documents avant de les utiliser et, si nécessaire, de
demander des conseils professionnels. Les standards eCH ne peuvent et ne
doivent pas remplacer les conseils techniques, organisationnels ou
juridiques dans un cas individuel.

Les documents, procédures, méthodes, produits et standards auxquels il
est fait référence dans les standards eCH sont potentiellement protégés
par des droits de marque, d’auteur ou de brevet. Il est de la
responsabilité exclusive de l’utilisateur d’obtenir les licences
nécessaires auprès des ayants droit et/ou des organisations.

Bien que l’association eCH ait apporté le soin nécessaire à
l’élaboration des standards eCH, elle ne peut garantir ni assurer que
les informations et documents fournis sont actuels, complets, exacts ou
exempts d’erreurs. eCH se réserve le droit de modifier le contenu de ses
standards à tout moment et sans préavis.

Toute responsabilité pour les dommages causés par l’utilisation des
standards eCH par l’utilisateur est exclue dans les limites autorisées
par la loi.

# Droits d’auteur

Les personnes qui élaborent les standards eCH restent propriétaires de
leurs droits de propriété intellectuelle. Ces personnes s’engagent
toutefois à mettre leurs droits de propriété intellectuelle ou d’autres
droits sur des droits de propriété intellectuelle de tiers, dans la
mesure du possible, à la disposition des groupes d’experts concernés et
de l’association eCH, et ce gratuitement et pour une utilisation ainsi
qu’un développement ultérieur illimités dans le cadre du but de
l’association.

Les standards élaborés par les groupes d’experts peuvent être utilisés,
diffusés et développés gratuitement et de manière illimitée en
mentionnant le nom de l’auteur respectif d’eCH.

Les standards eCH sont entièrement documentés et libres de toute
restriction de droit de licence et/ou de brevet. La documentation
correspondante peut être demandée gratuitement. Ces dispositions ne
s’appliquent toutefois qu’aux standards élaborés par eCH, et non aux
standards ou produits de tiers qui font référence aux standards eCH. Les
standards contiennent les références correspondantes aux droits de
tiers.

# Annexe A - Références

<div id="refs" class="references csl-bib-body hanging-indent">

<div id="ref-glimm2014hermit" class="csl-entry">

Glimm, Birte, Ian Horrocks, Boris Motik, Giorgos Stoilos, et Zhe Wang.
2014. « HermiT: an OWL 2 reasoner ». *Journal of automated reasoning* 53
(3): 245‑69.

</div>

<div id="ref-jackson2019robot" class="csl-entry">

Jackson, Rebecca C, James P Balhoff, Eric Douglass, Nomi L Harris,
Christopher J Mungall, et James A Overton. 2019. « ROBOT: a tool for
automating ontology workflows ». *BMC bioinformatics* 20 (1): 407.

</div>

</div>

# Annexe B - Collaboration & Vérification

# Annexe C - Abréviations et glossaire

# Annexe D - Modifications par rapport à la version précédente

# Annexe E - Table des illustrations

# Annexe F - Liste des tableaux
