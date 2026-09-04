# Modèle de document Quarto eCH-1234

4 septembre 2026

- [Remarque](#sec-note)
- [<span class="toc-section-number">1</span>
  Introduction](#sec-introduction)
  - [<span class="toc-section-number">1.1</span> Statut](#sec-status)
  - [<span class="toc-section-number">1.2</span> Champ
    d’application](#sec-scope-of-application)
  - [<span class="toc-section-number">1.3</span> Nous pouvons avoir des
    sous-titres](#sec-example-subheading)
- [<span class="toc-section-number">2</span> Notes
  techniques](#sec-technical-notes)
- [<span class="toc-section-number">3</span> Modèle de
  données](#sec-data-model)
  - [<span class="toc-section-number">3.1</span> Album de
    musique](#sec-nodeshape-musicalbumshape)
  - [<span class="toc-section-number">3.2</span> Enregistrement
    musical](#sec-nodeshape-trackshape)
  - [<span class="toc-section-number">3.3</span>
    Facture](#sec-nodeshape-invoiceshape)
  - [<span class="toc-section-number">3.4</span>
    Genre](#sec-nodeshape-genreshape)
  - [<span class="toc-section-number">3.5</span>
    Organisation](#sec-nodeshape-organisationshape)
  - [<span class="toc-section-number">3.6</span>
    Personne](#sec-nodeshape-personshape)
  - [<span class="toc-section-number">3.7</span> Valeur
    quantitative](#sec-nodeshape-quantitativevalueshape)
- [<span class="toc-section-number">4</span> Accès aux
  données](#sec-data-retrieval)
- [<span class="toc-section-number">5</span> Considérations de
  sécurité](#sec-safety-consideration)
- [<span class="toc-section-number">6</span> Clause de
  non-responsabilité](#sec-disclaimer)
- [<span class="toc-section-number">7</span> Droits
  d’auteur](#sec-copyrights)
- [<span class="toc-section-number">8</span> Annexe A -
  Références](#sec-appendix-a)
- [<span class="toc-section-number">9</span> Annexe B - Collaboration et
  Vérification](#sec-appendix-b)
- [<span class="toc-section-number">10</span> Annexe C - Abréviations et
  glossaire](#sec-appendix-c)
- [<span class="toc-section-number">11</span> Annexe D - Modifications
  par rapport à la version précédente](#sec-appendix-d)
- [<span class="toc-section-number">12</span> Annexe E - Table des
  illustrations](#sec-appendix-e)
- [<span class="toc-section-number">13</span> Annexe F - Liste des
  tableaux](#sec-appendix-f)

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

## Album de musique

Une collection de pistes dans le jeu de données Chinook.

**Classe cible:** `schema:MusicAlbum`

<div id="tbl-nodeshape-musicalbumshape">

Table 1: propriétés Album de musique

| Description | Chemin | Type | Cardinalité |
|:---|:---|:---|---:|
| **Nom**: Chaque album doit avoir un nom. | `schema:name` | `xsd:string` | 1..1 |
| **Artiste**: Personne ou groupe de musique ayant créé l’album. | `schema:byArtist` | [`schema:Person`](#sec-nodeshape-personshape) ou `schema:MusicGroup` | 0..\* |

</div>

## Enregistrement musical

Une piste musicale unique dans le jeu de données Chinook.

**Classe cible:** `schema:MusicRecording`

<div id="tbl-nodeshape-trackshape">

Table 2: propriétés Enregistrement musical

| Description | Chemin | Type | Cardinalité |
|:---|:---|:---|---:|
| **Nom**: Chaque piste doit avoir un nom. | `schema:name` | `xsd:string` | 1..1 |
| **Dans l’album**: Une piste ne peut appartenir qu’à un schema:MusicAlbum valide. | `schema:inAlbum` | [`schema:MusicAlbum`](#sec-nodeshape-musicalbumshape) | 0..\* |
| **Auteur**: La personne ou le groupe qui a écrit la piste. | `schema:author` |  | 0..\* |
| **Genre** | `schema:genre` | [`:Genre`](#sec-nodeshape-genreshape) | 1..1 |
| **Durée**: La durée doit être exprimée en tant que schema:QuantitativeValue. | `schema:duration` | [`schema:QuantitativeValue`](#sec-nodeshape-quantitativevalueshape) | 0..\* |
| **Taille du contenu** | `schema:contentSize` | [`schema:QuantitativeValue`](#sec-nodeshape-quantitativevalueshape) | 0..\* |

</div>

## Facture

Un reçu d’achat dans le jeu de données Chinook.

**Classe cible:** `schema:Invoice`

<div id="tbl-nodeshape-invoiceshape">

Table 3: propriétés Facture

| Description | Chemin | Type | Cardinalité |
|:---|:---|:---|---:|
| **Client**: Une facture doit être liée à exactement un client. | `schema:customer` | [`schema:Person`](#sec-nodeshape-personshape) | 1..1 |
| **Paiement total dû**: Une facture doit définir un paiement total dû en tant que schema:QuantitativeValue. | `schema:totalPaymentDue` | [`schema:QuantitativeValue`](#sec-nodeshape-quantitativevalueshape) | 1..1 |
| **Contient**: Une facture doit avoir au moins un article (OrderItem). | `schema:hasPart` | `schema:OrderItem` | 1..\* |
| **Date de création** | `schema:dateCreated` | `xsd:date` | 0..\* |

</div>

## Genre

Une catégorie musicale dans le jeu de données Chinook.

**Classe cible:** `:Genre`

<div id="tbl-nodeshape-genreshape">

Table 4: propriétés Genre

| Description | Chemin | Type | Cardinalité |
|:---|:---|:---|---:|
| **Nom** | `schema:name` |  | 1..1 |
| **Partie de** | `schema:partOf` | [`:Genre`](#sec-nodeshape-genreshape) ou `sh:IRI` | 0..\* |

</div>

## Organisation

Une entreprise ou organisation dans le jeu de données Chinook.

**Classe cible:** `schema:Organisation`

<div id="tbl-nodeshape-organisationshape">

Table 5: propriétés Organisation

| Description | Chemin | Type | Cardinalité |
|:---|:---|:---|---:|
| **Nom**: Chaque organisation doit avoir un nom. | `schema:name` | `xsd:string` | 1..1 |

</div>

## Personne

Toute personne (employé, client ou personne personnalisée) présente dans
le jeu de données.

**Classe cible:** `schema:Person`

<div id="tbl-nodeshape-personshape">

Table 6: propriétés Personne

| Description | Chemin | Type | Cardinalité |
|:---|:---|:---|---:|
| **Prénom**: Chaque personne doit avoir un prénom. | `schema:givenName` | `xsd:string` | 1..1 |
| **Nom de famille**: Chaque personne doit avoir un nom de famille. | `schema:familyName` | `xsd:string` | 1..1 |
| **Adresse e-mail**: Si une adresse e-mail est fournie, elle doit respecter un format standard. | `schema:email` | `xsd:string` | 0..\* |
| **Date de naissance**: Une personne doit avoir une date de naissance valide. | `schema:birthDate` | `xsd:date` | 0..\* |
| **Adresse** | `schema:address` | `schema:PostalAddress` | 0..\* |
| **Travaille pour**: Un employé peut relever d’une autre personne. | `schema:worksFor` | [`schema:Person`](#sec-nodeshape-personshape) ou `schema:Organization` | 0..\* |
| **Titre du poste** | `schema:jobTitle` |  | 0..1 |
| **Connaît** | `schema:knows` | [`schema:Person`](#sec-nodeshape-personshape) | 0..\* |

</div>

## Valeur quantitative

Une valeur numérique avec une unité associée.

**Classe cible:** `schema:QuantitativeValue`

<div id="tbl-nodeshape-quantitativevalueshape">

Table 7: propriétés Valeur quantitative

| Description | Chemin | Type | Cardinalité |
|:---|:---|:---|---:|
| **Valeur**: Une valeur quantitative doit avoir exactement une valeur numérique. | `schema:value` |  | 1..1 |
| **Code d’unité**: Une valeur quantitative doit spécifier son unité via une URI unitCode. | `schema:unitCode` | `sh:IRI` | 1..1 |

</div>

# Accès aux données

Les données de base et de référence qui sous-tendent ce document sont
disponibles sous forme de *Linked Data*.

La base technologique de cette approche est le Resource Description
Framework (RDF, Cyganiak et al. 2014), un standard central du World Wide
Web Consortium (W3C) pour la modélisation des structures de données sur
le Web. En RDF, les informations ne sont pas représentées dans des
tableaux classiques, mais sous forme de graphes interconnectés. Chaque
déclaration est constituée de ce que l’on appelle un triplet (sujet,
prédicat, objet). Cette structure permet une description des ressources
et de leurs relations mutuelles qui soit lisible par machine,
interopérable et univoque à travers différents systèmes.

Pour le stockage et la publication de ces données RDF, on utilise
[LINDAS](https://lindas.admin.ch/) (Linked Data Service), le service
officiel de Linked Data de l’administration fédérale suisse. LINDAS fait
office de *Triple Store*, une base de données orientée graphe
spécialisée et optimisée pour le stockage et l’interrogation efficaces
de triplets RDF, qui met les données publiquement à disposition via une
interface standardisée.

Le chapitre suivant fournit des instructions minimales sur la façon dont
les données peuvent être interrogées et extraites de LINDAS.

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

Les données sous-jacentes elles-mêmes sont gérées sur GitHub sous forme
de fichiers Turtle.

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

<div id="ref-cyganiak2014rdf11" class="csl-entry">

Cyganiak, Richard, David Wood, et Markus Lanthaler. 2014. *RDF 1.1
Concepts and Abstract Syntax*. W3C Recommendation. World Wide Web
Consortium (W3C). <https://www.w3.org/TR/rdf11-concepts/>.

</div>

<div id="ref-glimm2014hermit" class="csl-entry">

Glimm, Birte, Ian Horrocks, Boris Motik, Giorgos Stoilos, et Zhe Wang.
2014. « HermiT: an OWL 2 reasoner ». *Journal of automated reasoning* 53
(3): 245‑69.

</div>

<div id="ref-jackson2019robot" class="csl-entry">

Jackson, Rebecca C, James P Balhoff, Eric Douglass, Nomi L Harris,
Christopher J Mungall, et James A Overton. 2019. « ROBOT: a tool for
automating ontology workflows ». *BMC bioinformatics* 20 (1): 407.
<https://doi.org/10.1186/s12859-019-3002-3>.

</div>

</div>

# Annexe B - Collaboration et Vérification

# Annexe C - Abréviations et glossaire

<div id="tbl-glossary">

Table 8: Glossaire de la norme eCH-1234

| IRI | Terme | Description | Relations |
|:---|:---|:---|:---|
| [`term:lindas`](http://example.org/term/lindas) | **Linked Data Service** (LINDAS) | Le service officiel de données liées de l’administration fédérale suisse, fonctionnant comme un triple store (magasin de triplets). |  |
| [`term:rdf`](http://example.org/term/rdf) | **Resource Description Framework** (RDF) | Une norme centrale du World Wide Web Consortium (W3C) pour la modélisation des structures de données sur le Web. Les informations ne sont pas représentées dans des tableaux classiques, mais sous forme de graphes interconnectés. |  |
| [`term:triple`](http://example.org/term/triple) | **Triplet** | La structure de base d’une déclaration en RDF, composée d’un sujet, d’un prédicat et d’un objet. | *plus générique*: [`term:rdf`](http://example.org/term/rdf) |

</div>

# Annexe D - Modifications par rapport à la version précédente

# Annexe E - Table des illustrations

# Annexe F - Liste des tableaux
