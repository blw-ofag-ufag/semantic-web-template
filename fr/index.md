# Modèle de document Quarto

2026-10-01

- [<span class="toc-section-number">1</span>
  Introduction](#sec-introduction)
  - [<span class="toc-section-number">1.1</span> Statut](#sec-status)
  - [<span class="toc-section-number">1.2</span> Champ
    d’application](#sec-scope-of-application)
  - [<span class="toc-section-number">1.3</span> Nous pouvons avoir des
    sous-titres](#sec-example-subheading)
  - [<span class="toc-section-number">1.4</span> Mises en
    forme](#sec-formatting)
- [<span class="toc-section-number">2</span> Indications
  d’utilisation](#sec-usage-notes)
  - [<span class="toc-section-number">2.1</span> Espaces de
    noms](#sec-namespaces)
- [<span class="toc-section-number">3</span> Modèle de
  données](#sec-data-model)
  - [<span class="toc-section-number">3.1</span> Adresse
    postale](#sec-nodeshape-postaladdressshape)
  - [<span class="toc-section-number">3.2</span> Album de
    musique](#sec-nodeshape-musicalbumshape)
  - [<span class="toc-section-number">3.3</span> Enregistrement
    musical](#sec-nodeshape-trackshape)
  - [<span class="toc-section-number">3.4</span>
    Facture](#sec-nodeshape-invoiceshape)
  - [<span class="toc-section-number">3.5</span>
    Genre](#sec-nodeshape-genreshape)
  - [<span class="toc-section-number">3.6</span>
    Organisation](#sec-nodeshape-organisationshape)
  - [<span class="toc-section-number">3.7</span>
    Personne](#sec-nodeshape-personshape)
  - [<span class="toc-section-number">3.8</span> Valeur
    quantitative](#sec-nodeshape-quantitativevalueshape)
- [<span class="toc-section-number">4</span> Accès aux
  données](#sec-data-retrieval)
- [<span class="toc-section-number">5</span> Considérations de
  sécurité](#sec-safety-consideration)
- [<span class="toc-section-number">6</span> Clause de
  non-responsabilité](#sec-disclaimer)
- [<span class="toc-section-number">7</span> Droits
  d’auteur](#sec-copyrights)
- [Annexe A – Références](#sec-appendix-a)
- [Annexe B – Collaboration et Vérification](#sec-appendix-b)
- [Annexe C – Abréviations et glossaire](#sec-appendix-c)
- [Annexe D – Modifications par rapport à la version
  précédente](#sec-appendix-d)
- [Annexe E – Table des illustrations](#sec-appendix-e)
- [Annexe F – Liste des tableaux](#sec-appendix-f)

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

En cours: L’utilisation est autorisée uniquement au sein du groupe
spécialisé et/ou du Comité des experts.

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
Si une illustration a une légende, elle figure dans la table des
illustrations. Seule la première phrase de la légende y est affichée.

</div>

Lors de la présentation de diagrammes, essayez de les créer directement
dans Mermaid JS ; cela facilite grandement les modifications futures ou
les traductions.

## Mises en forme

Ce chapitre est un test de charge: il contient les éléments Markdown et
Quarto courants, afin de vérifier leur rendu dans le PDF et sur le site
web.

### Mise en évidence du texte

Le texte peut être en **gras**, en *italique*, <u>souligné</u>,
<span class="mark">surligné</span>, <span class="smallcaps">en petites
capitales</span> ou ~~barré~~. Les raccourcis clavier comme `Ctrl-C` +
`Ctrl-V` et le code en ligne comme `schema:name` sont mis en
évidence.[^1]

#### Un titre de quatrième niveau

Les titres jusqu’au quatrième niveau sont possibles; ils sont numérotés,
mais n’apparaissent pas dans la table des matières.[^2]

### Listes et encadrés

Liste non ordonnée:

- Premier point
- Deuxième point
  - Sous-point
- Troisième point

Liste ordonnée:

1.  Première étape
2.  Deuxième étape
3.  Troisième étape

> [!NOTE]
>
> Une remarque attire l’attention sur des liens faciles à négliger.

> [!WARNING]
>
> Un avertissement signale des sources d’erreur, par exemple des données
> d’entrée non vérifiées.

### Code, tableaux et formules

Le bloc de code suivant montre une requête SPARQL:

``` sparql
SELECT ?s ?p ?o
WHERE {
  ?s ?p ?o .
}
LIMIT 10
```

<div id="tbl-example">

Table 1: Tableau d’exemple à trois colonnes. Si un tableau a une
légende, il figure dans la liste des tableaux. Seule la première phrase
de la légende y est affichée.

| Colonne  | Type           | Remarque          |
|:---------|:---------------|:------------------|
| Nom      | Chaîne         | Champ obligatoire |
| Quantité | Nombre décimal | avec unité        |

</div>

Une formule peut figurer dans le texte, par exemple $E = m c^2$, ou
comme équation à part entière telle que
<a href="#eq-example" class="quarto-xref">Équation 1</a>:

<span id="eq-example">$$
\sum_{i=1}^{n} x_i = n \bar{x}
 \qquad(1)$$</span>

# Indications d’utilisation

Le paragraphe suivant est volontairement absurde et ne sert qu’à tester
le style de citation: selon le guide d’approbation \[eCH-0003 11.1.0\],
toutes les adresses postales \[eCH-0010 8.1.0\] doivent être sérialisées
en Turtle \[Turtle\], vérifiées comme catalogue DCAT \[DCAT; eCH-0200
3.0.1\] avec SHACL \[SHACL\] et publiées via SPARQL \[SPARQL\] comme
Linked Open Data \[eCH-0205 1.0\] sur les cultures agricoles \[eCH-0265
1.0.0\] en JSON-LD \[JSON-LD\] et OWL \[OWL 2\], comme le prévoit le Web
sémantique \[Berners-Lee 2023\].

## Espaces de noms

Le <a href="#tbl-namespaces" class="quarto-xref">Table 2</a> énumère les
préfixes et les espaces de noms utilisés dans ce document. Un préfixe
tient lieu d’une IRI d’espace de noms, le début commun des IRI d’un
vocabulaire. La spécification Turtle décrit comment ces [*prefixed
names*](https://www.w3.org/TR/turtle/#prefixed-name) sont résolus
\[Turtle\].

<div id="tbl-namespaces">

Table 2: Espaces de noms utilisés dans eCH-1234 – Modèle de document
Quarto.

| Préfixe  | Espace de noms                              |
|:---------|:--------------------------------------------|
| :        | https://agriculture.ld.admin.ch/eCH-1234/2/ |
| country: | https://ld.admin.ch/country/                |
| rdf:     | http://www.w3.org/1999/02/22-rdf-syntax-ns# |
| schema:  | http://schema.org/                          |
| unit:    | http://qudt.org/vocab/unit/                 |
| xsd:     | http://www.w3.org/2001/XMLSchema#           |

</div>

# Modèle de données

## Adresse postale

L’adresse postale d’une personne.

Les adresses suivent la structure de schema.org et non la norme suisse
d’adresse eCH-0010, car le jeu de données contient surtout des adresses
étrangères. Les codes postaux ne sont donc vérifiés que quant à leur
format plausible, et non par rapport à un répertoire.

### Aperçu

<div class="ech-facts">

Shape  
[:PostalAddressShape](https://agriculture.ld.admin.ch/eCH-1234/2/PostalAddressShape)

Classe cible  
[schema:PostalAddress](http://schema.org/PostalAddress)

Fermée  
Oui (seules les propriétés énumérées sont admises)

Chiffres clés  
67 instances avec chacune 6 à 8 triplets (7.5 en moyenne)

Accès aux données  
[Service
SPARQL](https://lindas.admin.ch/sparql/#query=PREFIX%20schema%3A%20%3Chttp%3A%2F%2Fschema.org%2F%3E%0ASELECT%20%3Firi%20%3FstreetAddress%20%3FpostalCode%20%3FaddressLocality%20%3FaddressRegion%20%3FaddressCountry%0AFROM%20%3Chttps%3A%2F%2Flindas.admin.ch%2Ffoag%2Fogd%3E%0AWHERE%20%7B%0A%20%20%3Firi%20a%20schema%3APostalAddress%20.%0A%20%20%3Firi%20schema%3AstreetAddress%20%3FstreetAddress%20.%0A%20%20OPTIONAL%20%7B%20%3Firi%20schema%3ApostalCode%20%3FpostalCode%20.%20%7D%0A%20%20%3Firi%20schema%3AaddressLocality%20%3FaddressLocality%20.%0A%20%20OPTIONAL%20%7B%20%3Firi%20schema%3AaddressRegion%20%3FaddressRegion%20.%20%7D%0A%20%20%3Firi%20schema%3AaddressCountry%20%3FaddressCountry%20.%0A%7D%0ALIMIT%201000)

</div>

### Propriétés

<table style="width:99%;">
<colgroup>
<col style="width: 46%" />
<col style="width: 41%" />
<col style="width: 10%" />
</colgroup>
<thead>
<tr>
<th style="text-align: left;">Description</th>
<th style="text-align: left;">Détails</th>
<th style="text-align: right;">Cardinalité</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: left;"><strong>Rue et numéro</strong> (<a
href="http://schema.org/streetAddress">schema:streetAddress</a>)</td>
<td style="text-align: left;"><ul>
<li>Type: Chaîne de caractères (<a
href="http://www.w3.org/2001/XMLSchema#string">xsd:string</a>)</li>
<li>Longueur: 3–100 caractères</li>
<li>Exemples: Schwarzenburgstrasse 165</li>
</ul></td>
<td style="text-align: right;">1..1</td>
</tr>
<tr>
<td style="text-align: left;"><strong>Code postal</strong> (<a
href="http://schema.org/postalCode">schema:postalCode</a>): Lettres,
chiffres, espaces et traits d’union, de deux à dix caractères.</td>
<td style="text-align: left;"><ul>
<li>Type: Chaîne de caractères (<a
href="http://www.w3.org/2001/XMLSchema#string">xsd:string</a>)</li>
<li>Motif: <code>^[A-Za-z0-9][A-Za-z0-9 -]{1,9}$</code></li>
<li>Gravité: Avertissement</li>
</ul></td>
<td style="text-align: right;">0..1</td>
</tr>
<tr>
<td style="text-align: left;"><strong>Localité</strong> (<a
href="http://schema.org/addressLocality">schema:addressLocality</a>):
Chaque adresse requiert exactement une localité.</td>
<td style="text-align: left;"><ul>
<li>Type: Chaîne de caractères (<a
href="http://www.w3.org/2001/XMLSchema#string">xsd:string</a>)</li>
<li>Longueur: ≤ 100 caractères</li>
</ul></td>
<td style="text-align: right;">1..1</td>
</tr>
<tr>
<td style="text-align: left;"><strong>Région</strong> (<a
href="http://schema.org/addressRegion">schema:addressRegion</a>):
Canton, État ou province, lorsque c’est l’usage dans le pays.</td>
<td style="text-align: left;"><ul>
<li>Type: Chaîne de caractères (<a
href="http://www.w3.org/2001/XMLSchema#string">xsd:string</a>)</li>
<li>Longueur: ≤ 100 caractères</li>
</ul></td>
<td style="text-align: right;">0..1</td>
</tr>
<tr>
<td style="text-align: left;"><strong>Pays</strong> (<a
href="http://schema.org/addressCountry">schema:addressCountry</a>): Pays
sous forme d’IRI tirée de la liste des pays des Archives fédérales sur
LINDAS (ISO 3166-1 alpha-3).</td>
<td style="text-align: left;"><ul>
<li>Motif: <code>^https://ld\.admin\.ch/country/[A-Z]{3}$</code></li>
<li>Exemples: <a href="https://ld.admin.ch/country/CHE">country:CHE</a>,
<a href="https://ld.admin.ch/country/FRA">country:FRA</a>, <a
href="https://ld.admin.ch/country/ITA">country:ITA</a></li>
</ul></td>
<td style="text-align: right;">1..1</td>
</tr>
</tbody>
</table>

## Album de musique

Une collection de pistes dans le jeu de données Chinook.

### Aperçu

<div class="ech-facts">

Shape  
[:MusicAlbumShape](https://agriculture.ld.admin.ch/eCH-1234/2/MusicAlbumShape)

Classe cible  
[schema:MusicAlbum](http://schema.org/MusicAlbum)

Fermée  
Non (d’autres propriétés sont admises)

Chiffres clés  
347 instances avec chacune 5 triplets

Accès aux données  
[Service
SPARQL](https://lindas.admin.ch/sparql/#query=PREFIX%20schema%3A%20%3Chttp%3A%2F%2Fschema.org%2F%3E%0ASELECT%20%3Firi%20%3Fname%20%3FbyArtist%0AFROM%20%3Chttps%3A%2F%2Flindas.admin.ch%2Ffoag%2Fogd%3E%0AWHERE%20%7B%0A%20%20%3Firi%20a%20schema%3AMusicAlbum%20.%0A%20%20%3Firi%20schema%3Aname%20%3Fname%20.%0A%20%20OPTIONAL%20%7B%20%3Firi%20schema%3AbyArtist%20%3FbyArtist%20.%20%7D%0A%7D%0ALIMIT%201000)

</div>

### Propriétés

<table style="width:99%;">
<colgroup>
<col style="width: 40%" />
<col style="width: 46%" />
<col style="width: 12%" />
</colgroup>
<thead>
<tr>
<th style="text-align: left;">Description</th>
<th style="text-align: left;">Détails</th>
<th style="text-align: right;">Cardinalité</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: left;"><strong>Nom</strong> (<a
href="http://schema.org/name">schema:name</a>): Chaque album doit avoir
un nom.</td>
<td style="text-align: left;"><ul>
<li>Type: Chaîne de caractères (<a
href="http://www.w3.org/2001/XMLSchema#string">xsd:string</a>)</li>
<li>Longueur: ≤ 200 caractères</li>
</ul></td>
<td style="text-align: right;">1..1</td>
</tr>
<tr>
<td style="text-align: left;"><strong>Artiste</strong> (<a
href="http://schema.org/byArtist">schema:byArtist</a>): Personne ou
groupe de musique ayant créé l’album.</td>
<td style="text-align: left;"><ul>
<li>Type: <a href="#sec-nodeshape-personshape">Personne</a> ou <a
href="http://schema.org/MusicGroup">schema:MusicGroup</a></li>
</ul></td>
<td style="text-align: right;">0..*</td>
</tr>
</tbody>
</table>

## Enregistrement musical

Une piste musicale unique dans le jeu de données Chinook.

### Aperçu

<div class="ech-facts">

Shape  
[:TrackShape](https://agriculture.ld.admin.ch/eCH-1234/2/TrackShape)

Classe cible  
[schema:MusicRecording](http://schema.org/MusicRecording)

Fermée  
Non (d’autres propriétés sont admises)

Chiffres clés  
3503 instances avec chacune 10 à 15 triplets (11.1 en moyenne)

Accès aux données  
[Service
SPARQL](https://lindas.admin.ch/sparql/#query=PREFIX%20schema%3A%20%3Chttp%3A%2F%2Fschema.org%2F%3E%0ASELECT%20%3Firi%20%3Fname%20%3FinAlbum%20%3Fauthor%20%3Fgenre%20%3Fduration%20%3FcontentSize%0AFROM%20%3Chttps%3A%2F%2Flindas.admin.ch%2Ffoag%2Fogd%3E%0AWHERE%20%7B%0A%20%20%3Firi%20a%20schema%3AMusicRecording%20.%0A%20%20%3Firi%20schema%3Aname%20%3Fname%20.%0A%20%20OPTIONAL%20%7B%20%3Firi%20schema%3AinAlbum%20%3FinAlbum%20.%20%7D%0A%20%20OPTIONAL%20%7B%20%3Firi%20schema%3Aauthor%20%3Fauthor%20.%20%7D%0A%20%20%3Firi%20schema%3Agenre%20%3Fgenre%20.%0A%20%20OPTIONAL%20%7B%20%3Firi%20schema%3Aduration%20%3Fduration%20.%20%7D%0A%20%20OPTIONAL%20%7B%20%3Firi%20schema%3AcontentSize%20%3FcontentSize%20.%20%7D%0A%7D%0ALIMIT%201000)

</div>

### Propriétés

<table style="width:99%;">
<colgroup>
<col style="width: 43%" />
<col style="width: 44%" />
<col style="width: 11%" />
</colgroup>
<thead>
<tr>
<th style="text-align: left;">Description</th>
<th style="text-align: left;">Détails</th>
<th style="text-align: right;">Cardinalité</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: left;"><strong>Nom</strong> (<a
href="http://schema.org/name">schema:name</a>): Chaque piste doit avoir
un nom.</td>
<td style="text-align: left;"><ul>
<li>Type: Chaîne de caractères (<a
href="http://www.w3.org/2001/XMLSchema#string">xsd:string</a>)</li>
<li>Longueur: 1–200 caractères</li>
</ul></td>
<td style="text-align: right;">1..1</td>
</tr>
<tr>
<td style="text-align: left;"><strong>Dans l’album</strong> (<a
href="http://schema.org/inAlbum">schema:inAlbum</a>): Une piste ne peut
appartenir qu’à un schema:MusicAlbum valide.</td>
<td style="text-align: left;"><ul>
<li>Type: <a href="#sec-nodeshape-musicalbumshape">Album de
musique</a></li>
</ul></td>
<td style="text-align: right;">0..*</td>
</tr>
<tr>
<td style="text-align: left;"><strong>Auteur</strong> (<a
href="http://schema.org/author">schema:author</a>): La personne ou le
groupe qui a écrit la piste.</td>
<td style="text-align: left;"></td>
<td style="text-align: right;">0..*</td>
</tr>
<tr>
<td style="text-align: left;"><strong>Genre</strong> (<a
href="http://schema.org/genre">schema:genre</a>)</td>
<td style="text-align: left;"><ul>
<li>Type: <a href="#sec-nodeshape-genreshape">Genre</a></li>
</ul></td>
<td style="text-align: right;">1..1</td>
</tr>
<tr>
<td style="text-align: left;"><strong>Durée</strong> (<a
href="http://schema.org/duration">schema:duration</a>): La durée doit
être exprimée en tant que schema:QuantitativeValue.</td>
<td style="text-align: left;"><ul>
<li>Type: <a href="#sec-nodeshape-quantitativevalueshape">Valeur
quantitative</a></li>
</ul></td>
<td style="text-align: right;">0..*</td>
</tr>
<tr>
<td style="text-align: left;"><strong>Taille du contenu</strong> (<a
href="http://schema.org/contentSize">schema:contentSize</a>)</td>
<td style="text-align: left;"><ul>
<li>Type: <a href="#sec-nodeshape-quantitativevalueshape">Valeur
quantitative</a></li>
</ul></td>
<td style="text-align: right;">0..*</td>
</tr>
</tbody>
</table>

## Facture

Un reçu d’achat dans le jeu de données Chinook. Une facture regroupe les
positions d’un achat. Le montant de la facture n’est pas seulement saisi
comme valeur, il est aussi vérifié par rapport à la somme des positions;
des écarts de plus de cinq centimes sont considérés comme des erreurs.
Les factures antérieures à l’an 2000 proviennent d’un ancien système et
ne sont pas admises dans ce jeu de données.

### Aperçu

<div class="ech-facts">

Shape  
[:InvoiceShape](https://agriculture.ld.admin.ch/eCH-1234/2/InvoiceShape)

Classe cible  
[schema:Invoice](http://schema.org/Invoice)

Fermée  
Non (d’autres propriétés sont admises)

Chiffres clés  
412 instances avec chacune 8 à 21 triplets (12.4 en moyenne)

Accès aux données  
[Service
SPARQL](https://lindas.admin.ch/sparql/#query=PREFIX%20schema%3A%20%3Chttp%3A%2F%2Fschema.org%2F%3E%0ASELECT%20%3Firi%20%3Fcustomer%20%3FtotalPaymentDue%20%3FhasPart%20%3FdateCreated%0AFROM%20%3Chttps%3A%2F%2Flindas.admin.ch%2Ffoag%2Fogd%3E%0AWHERE%20%7B%0A%20%20%3Firi%20a%20schema%3AInvoice%20.%0A%20%20%3Firi%20schema%3Acustomer%20%3Fcustomer%20.%0A%20%20%3Firi%20schema%3AtotalPaymentDue%20%3FtotalPaymentDue%20.%0A%20%20%3Firi%20schema%3AhasPart%20%3FhasPart%20.%0A%20%20OPTIONAL%20%7B%20%3Firi%20schema%3AdateCreated%20%3FdateCreated%20.%20%7D%0A%7D%0ALIMIT%201000)

</div>

### Propriétés

<table style="width:99%;">
<colgroup>
<col style="width: 47%" />
<col style="width: 40%" />
<col style="width: 11%" />
</colgroup>
<thead>
<tr>
<th style="text-align: left;">Description</th>
<th style="text-align: left;">Détails</th>
<th style="text-align: right;">Cardinalité</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: left;"><strong>Client</strong> (<a
href="http://schema.org/customer">schema:customer</a>): Une facture doit
être liée à exactement un client.</td>
<td style="text-align: left;"><ul>
<li>Type: <a href="#sec-nodeshape-personshape">Personne</a></li>
</ul></td>
<td style="text-align: right;">1..1</td>
</tr>
<tr>
<td style="text-align: left;"><strong>Paiement total dû</strong> (<a
href="http://schema.org/totalPaymentDue">schema:totalPaymentDue</a>):
Une facture doit définir un paiement total dû en tant que
schema:QuantitativeValue.</td>
<td style="text-align: left;"><ul>
<li>Type: <a href="#sec-nodeshape-quantitativevalueshape">Valeur
quantitative</a></li>
</ul></td>
<td style="text-align: right;">1..1</td>
</tr>
<tr>
<td style="text-align: left;"><strong>Contient</strong> (<a
href="http://schema.org/hasPart">schema:hasPart</a>): Une facture doit
avoir au moins un article (OrderItem).</td>
<td style="text-align: left;"><ul>
<li>Type: <a
href="http://schema.org/OrderItem">schema:OrderItem</a></li>
</ul></td>
<td style="text-align: right;">1..*</td>
</tr>
<tr>
<td style="text-align: left;"><strong>Date de création</strong> (<a
href="http://schema.org/dateCreated">schema:dateCreated</a>)</td>
<td style="text-align: left;"><ul>
<li>Type: Date (<a
href="http://www.w3.org/2001/XMLSchema#date">xsd:date</a>)</li>
<li>Plage de valeurs: ≥ 2000-01-01</li>
<li>Exemples: 2001-01-01, 2024-05-21</li>
</ul></td>
<td style="text-align: right;">0..*</td>
</tr>
</tbody>
</table>

### Règles (SPARQL)

#### Date de la facture

Une facture ne peut pas être datée d’avant l’année 2000.

``` sparql
SELECT $this
WHERE {
    $this schema:dateCreated ?date .
    FILTER(?date < "2000-01-01"^^xsd:date)
}
```

#### Total de la facture

Le total de la facture doit correspondre exactement à la somme de ses
lignes (tolérance de 0.05).

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

## Genre

Une catégorie musicale dans le jeu de données Chinook.

### Aperçu

<div class="ech-facts">

Shape  
[:GenreShape](https://agriculture.ld.admin.ch/eCH-1234/2/GenreShape)

Classe cible  
[:Genre](https://agriculture.ld.admin.ch/eCH-1234/2/Genre)

Fermée  
Oui (seules les propriétés énumérées sont admises)

Chiffres clés  
25 instances avec chacune 5 à 7 triplets (5.4 en moyenne)

Accès aux données  
[Service
SPARQL](https://lindas.admin.ch/sparql/#query=PREFIX%20%3A%20%3Chttps%3A%2F%2Fagriculture.ld.admin.ch%2FeCH-1234%2F2%2F%3E%0APREFIX%20schema%3A%20%3Chttp%3A%2F%2Fschema.org%2F%3E%0ASELECT%20%3Firi%20%3Fname%20%3FpartOf%20%3FalternateName%0AFROM%20%3Chttps%3A%2F%2Flindas.admin.ch%2Ffoag%2Fogd%3E%0AWHERE%20%7B%0A%20%20%3Firi%20a%20%3AGenre%20.%0A%20%20%3Firi%20schema%3Aname%20%3Fname%20.%0A%20%20OPTIONAL%20%7B%20%3Firi%20schema%3ApartOf%20%3FpartOf%20.%20%7D%0A%20%20OPTIONAL%20%7B%20%3Firi%20schema%3AalternateName%20%3FalternateName%20.%20%7D%0A%7D%0ALIMIT%201000)

</div>

### Propriétés

<table style="width:99%;">
<colgroup>
<col style="width: 39%" />
<col style="width: 49%" />
<col style="width: 9%" />
</colgroup>
<thead>
<tr>
<th style="text-align: left;">Description</th>
<th style="text-align: left;">Détails</th>
<th style="text-align: right;">Cardinalité</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: left;"><strong>Nom</strong> (<a
href="http://schema.org/name">schema:name</a>)</td>
<td style="text-align: left;"><ul>
<li>Type: Chaîne de caractères (<a
href="http://www.w3.org/2001/XMLSchema#string">xsd:string</a>)</li>
<li>Motif: <code>^[A-Z]</code></li>
<li>Longueur: 2–50 caractères</li>
</ul></td>
<td style="text-align: right;">1..1</td>
</tr>
<tr>
<td style="text-align: left;"><strong>Partie de</strong> (<a
href="http://schema.org/partOf">schema:partOf</a>)</td>
<td style="text-align: left;"><ul>
<li>Type: <a href="#sec-nodeshape-genreshape">Genre</a></li>
</ul></td>
<td style="text-align: right;">0..*</td>
</tr>
<tr>
<td style="text-align: left;"><strong>Dénomination alternative</strong>
(<a href="http://schema.org/alternateName">schema:alternateName</a>):
Dénomination traduite ou familière du genre, au plus une par
langue.</td>
<td style="text-align: left;"><ul>
<li>Type: Texte avec indication de langue (<a
href="http://www.w3.org/1999/02/22-rdf-syntax-ns#langString">rdf:langString</a>)</li>
<li>Longueur: ≤ 50 caractères</li>
<li>Langues: <code>de</code>, <code>fr</code>, <code>it</code>,
<code>en</code> (une par langue)</li>
</ul></td>
<td style="text-align: right;">0..*</td>
</tr>
</tbody>
</table>

### Règles (SPARQL)

#### Pas de hiérarchie cyclique

Un genre ne peut pas faire partie de lui-même, ni directement ni
transitivement.

``` sparql
SELECT $this
WHERE {
    $this schema:partOf+ $this .
}
```

## Organisation

Une entreprise ou organisation dans le jeu de données Chinook.

### Aperçu

<div class="ech-facts">

Shape  
[:OrganisationShape](https://agriculture.ld.admin.ch/eCH-1234/2/OrganisationShape)

Classe cible  
[schema:Organisation](http://schema.org/Organisation)

Fermée  
Non (d’autres propriétés sont admises)

Accès aux données  
Aucun (données transactionnelles, ne faisant pas partie du graphe
publié)

</div>

### Propriétés

<table style="width:99%;">
<colgroup>
<col style="width: 36%" />
<col style="width: 49%" />
<col style="width: 12%" />
</colgroup>
<thead>
<tr>
<th style="text-align: left;">Description</th>
<th style="text-align: left;">Détails</th>
<th style="text-align: right;">Cardinalité</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: left;"><strong>Nom</strong> (<a
href="http://schema.org/name">schema:name</a>): Chaque organisation doit
avoir un nom.</td>
<td style="text-align: left;"><ul>
<li>Type: Chaîne de caractères (<a
href="http://www.w3.org/2001/XMLSchema#string">xsd:string</a>)</li>
<li>Longueur: 2–100 caractères</li>
</ul></td>
<td style="text-align: right;">1..1</td>
</tr>
</tbody>
</table>

## Personne

Toute personne (employé, client ou personne personnalisée) présente dans
le jeu de données.

Les personnes sont décrites de manière uniforme, quel que soit leur
rôle: le personnel du magasin de musique, la clientèle et les personnes
saisies manuellement partagent les mêmes propriétés. Le rôle découle des
relations, par exemple `schema:worksFor` pour le personnel ou
`schema:customer` sur une facture pour la clientèle.

Les noms sont saisis tels que la personne les utilise; les titres
académiques ne font pas partie du prénom. Les adresses e-mail et les
dates de naissance sont facultatives et les infractions aux règles ne
sont signalées que comme avertissements.

### Aperçu

<div class="ech-facts">

Shape  
[:PersonShape](https://agriculture.ld.admin.ch/eCH-1234/2/PersonShape)

Classe cible  
[schema:Person](http://schema.org/Person)

Fermée  
Oui (seules les propriétés énumérées sont admises)

Chiffres clés  
383 instances avec chacune 5 à 10 triplets (5.6 en moyenne)

Accès aux données  
[Service
SPARQL](https://lindas.admin.ch/sparql/#query=PREFIX%20schema%3A%20%3Chttp%3A%2F%2Fschema.org%2F%3E%0ASELECT%20%3Firi%20%3FgivenName%20%3FfamilyName%20%3Femail%20%3FbirthDate%20%3Faddress%20%3FworksFor%20%3FjobTitle%20%3Fknows%0AFROM%20%3Chttps%3A%2F%2Flindas.admin.ch%2Ffoag%2Fogd%3E%0AWHERE%20%7B%0A%20%20%3Firi%20a%20schema%3APerson%20.%0A%20%20%3Firi%20schema%3AgivenName%20%3FgivenName%20.%0A%20%20%3Firi%20schema%3AfamilyName%20%3FfamilyName%20.%0A%20%20OPTIONAL%20%7B%20%3Firi%20schema%3Aemail%20%3Femail%20.%20%7D%0A%20%20OPTIONAL%20%7B%20%3Firi%20schema%3AbirthDate%20%3FbirthDate%20.%20%7D%0A%20%20OPTIONAL%20%7B%20%3Firi%20schema%3Aaddress%20%3Faddress%20.%20%7D%0A%20%20OPTIONAL%20%7B%20%3Firi%20schema%3AworksFor%20%3FworksFor%20.%20%7D%0A%20%20OPTIONAL%20%7B%20%3Firi%20schema%3AjobTitle%20%3FjobTitle%20.%20%7D%0A%20%20OPTIONAL%20%7B%20%3Firi%20schema%3Aknows%20%3Fknows%20.%20%7D%0A%7D%0ALIMIT%201000)

</div>

### Propriétés

<table style="width:99%;">
<colgroup>
<col style="width: 42%" />
<col style="width: 44%" />
<col style="width: 11%" />
</colgroup>
<thead>
<tr>
<th style="text-align: left;">Description</th>
<th style="text-align: left;">Détails</th>
<th style="text-align: right;">Cardinalité</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: left;"><strong>Prénom</strong> (<a
href="http://schema.org/givenName">schema:givenName</a>): Chaque
personne doit avoir un prénom.</td>
<td style="text-align: left;"><ul>
<li>Type: Chaîne de caractères (<a
href="http://www.w3.org/2001/XMLSchema#string">xsd:string</a>)</li>
</ul></td>
<td style="text-align: right;">1..1</td>
</tr>
<tr>
<td style="text-align: left;"><strong>Nom de famille</strong> (<a
href="http://schema.org/familyName">schema:familyName</a>): Chaque
personne doit avoir un nom de famille.</td>
<td style="text-align: left;"><ul>
<li>Type: Chaîne de caractères (<a
href="http://www.w3.org/2001/XMLSchema#string">xsd:string</a>)</li>
</ul></td>
<td style="text-align: right;">1..1</td>
</tr>
<tr>
<td style="text-align: left;"><strong>Adresse e-mail</strong> (<a
href="http://schema.org/email">schema:email</a>): Si une adresse e-mail
est fournie, elle doit respecter un format standard.</td>
<td style="text-align: left;"><ul>
<li>Type: Chaîne de caractères (<a
href="http://www.w3.org/2001/XMLSchema#string">xsd:string</a>)</li>
<li>Motif: <code>^.+@.+\..+$</code> (<code>i</code>)</li>
<li>Longueur: ≤ 254 caractères</li>
<li>Gravité: Avertissement</li>
</ul></td>
<td style="text-align: right;">0..*</td>
</tr>
<tr>
<td style="text-align: left;"><strong>Date de naissance</strong> (<a
href="http://schema.org/birthDate">schema:birthDate</a>): Une personne
doit avoir une date de naissance valide.</td>
<td style="text-align: left;"><ul>
<li>Type: Date (<a
href="http://www.w3.org/2001/XMLSchema#date">xsd:date</a>)</li>
<li>Plage de valeurs: ≥ 1900-01-01, ≤ 2025-12-31</li>
<li>Gravité: Avertissement</li>
</ul></td>
<td style="text-align: right;">0..*</td>
</tr>
<tr>
<td style="text-align: left;"><strong>Adresse</strong> (<a
href="http://schema.org/address">schema:address</a>)</td>
<td style="text-align: left;"><ul>
<li>Type: <a href="#sec-nodeshape-postaladdressshape">Adresse
postale</a></li>
</ul></td>
<td style="text-align: right;">0..*</td>
</tr>
<tr>
<td style="text-align: left;"><strong>Travaille pour</strong> (<a
href="http://schema.org/worksFor">schema:worksFor</a>): Un employé peut
relever d’une autre personne.</td>
<td style="text-align: left;"><ul>
<li>Type: <a href="#sec-nodeshape-personshape">Personne</a> ou <a
href="http://schema.org/Organization">schema:Organization</a></li>
</ul></td>
<td style="text-align: right;">0..*</td>
</tr>
<tr>
<td style="text-align: left;"><strong>Titre du poste</strong> (<a
href="http://schema.org/jobTitle">schema:jobTitle</a>)</td>
<td style="text-align: left;"><ul>
<li>Type: Chaîne de caractères (<a
href="http://www.w3.org/2001/XMLSchema#string">xsd:string</a>)</li>
<li>Longueur: 2–100 caractères</li>
</ul></td>
<td style="text-align: right;">0..1</td>
</tr>
<tr>
<td style="text-align: left;"><strong>Connaît</strong> (<a
href="http://schema.org/knows">schema:knows</a>)</td>
<td style="text-align: left;"><ul>
<li>Type: <a href="#sec-nodeshape-personshape">Personne</a></li>
</ul></td>
<td style="text-align: right;">0..*</td>
</tr>
</tbody>
</table>

### Règles (SPARQL)

#### Pas d’auto-subordination

Un employé ne peut pas relever de lui-même.

``` sparql
SELECT $this
WHERE {
    $this schema:worksFor $this .
}
```

## Valeur quantitative

Une valeur numérique avec une unité associée.

Les valeurs quantitatives ne sont jamais saisies comme un simple nombre,
mais toujours avec une unité du vocabulaire QUDT. Il reste ainsi clair
si une durée est exprimée en millisecondes ou une taille de fichier en
octets. Les valeurs négatives ne sont pas prévues dans ce jeu de
données.

### Aperçu

<div class="ech-facts">

Shape  
[:QuantitativeValueShape](https://agriculture.ld.admin.ch/eCH-1234/2/QuantitativeValueShape)

Classe cible  
[schema:QuantitativeValue](http://schema.org/QuantitativeValue)

Fermée  
Oui (seules les propriétés énumérées sont admises)

Chiffres clés  
15401 instances avec chacune 3 triplets

Accès aux données  
[Service
SPARQL](https://lindas.admin.ch/sparql/#query=PREFIX%20schema%3A%20%3Chttp%3A%2F%2Fschema.org%2F%3E%0ASELECT%20%3Firi%20%3Fvalue%20%3FunitCode%0AFROM%20%3Chttps%3A%2F%2Flindas.admin.ch%2Ffoag%2Fogd%3E%0AWHERE%20%7B%0A%20%20%3Firi%20a%20schema%3AQuantitativeValue%20.%0A%20%20%3Firi%20schema%3Avalue%20%3Fvalue%20.%0A%20%20%3Firi%20schema%3AunitCode%20%3FunitCode%20.%0A%7D%0ALIMIT%201000)

</div>

### Propriétés

<table style="width:99%;">
<colgroup>
<col style="width: 40%" />
<col style="width: 47%" />
<col style="width: 11%" />
</colgroup>
<thead>
<tr>
<th style="text-align: left;">Description</th>
<th style="text-align: left;">Détails</th>
<th style="text-align: right;">Cardinalité</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: left;"><strong>Valeur</strong> (<a
href="http://schema.org/value">schema:value</a>): Une valeur
quantitative doit avoir exactement une valeur numérique.</td>
<td style="text-align: left;"><ul>
<li>Type: Nombre décimal (<a
href="http://www.w3.org/2001/XMLSchema#decimal">xsd:decimal</a>) ou
Nombre entier (<a
href="http://www.w3.org/2001/XMLSchema#integer">xsd:integer</a>)</li>
<li>Plage de valeurs: ≥ 0</li>
</ul></td>
<td style="text-align: right;">1..1</td>
</tr>
<tr>
<td style="text-align: left;"><strong>Code d’unité</strong> (<a
href="http://schema.org/unitCode">schema:unitCode</a>): Une valeur
quantitative doit spécifier son unité via une URI unitCode.</td>
<td style="text-align: left;"><ul>
<li>Valeurs: <a href="http://qudt.org/vocab/unit/USD">unit:USD</a>, <a
href="http://qudt.org/vocab/unit/EA">unit:EA</a>, <a
href="http://qudt.org/vocab/unit/BYTE">unit:BYTE</a>, <a
href="http://qudt.org/vocab/unit/MilliSEC">unit:MilliSEC</a></li>
</ul></td>
<td style="text-align: right;">1..1</td>
</tr>
</tbody>
</table>

# Accès aux données

Les données de base et de référence qui sous-tendent ce document sont
disponibles sous forme de *Linked Data*.

La base technologique de cette approche est le Resource Description
Framework \[RDF, RDF\], un standard central du World Wide Web Consortium
(W3C) pour la modélisation des structures de données sur le Web. En RDF,
les informations ne sont pas représentées dans des tableaux classiques,
mais sous forme de graphes interconnectés. Chaque déclaration est
constituée de ce que l’on appelle un triplet (sujet, prédicat, objet).
Cette structure permet une description des ressources et de leurs
relations mutuelles qui soit lisible par machine, interopérable et
univoque à travers différents systèmes.

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
BASE <https://agriculture.ld.admin.ch/eCH-1234/2/>
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

# Annexe A – Références

<div id="refs" class="references csl-bib-body">

<div id="ref-berners2023semantic" class="csl-entry">

<span class="csl-left-margin">\[Berners-Lee 2023\]
</span><span class="csl-right-inline">Berners-Lee, Tim ; Hendler,
James ; Lassila, Ora: [The Semantic Web: A new form of Web content that
is meaningful to computers will unleash a revolution of new
possibilities](https://doi.org/10.1145/3591366.3591376). In: *Linking
the World’s Information: Essays on Tim Berners-Lee’s Invention of the
World Wide Web* : Association for Computing Machinery, 2023,
p. 91‑103</span>

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

# Annexe B – Collaboration et Vérification

| Nom               | Organisation                    |
|:------------------|:--------------------------------|
| Damian Oswald     | Office fédéral de l’agriculture |
| Michael Schüpbach | Office fédéral de l’agriculture |
| Lea Stauber       | Office fédéral de l’agriculture |

# Annexe C – Abréviations et glossaire

Ce glossaire est également disponible sous forme lisible par machine
comme glossaire SKOS \[SKOS\], sur [LINDAS](https://lindas.admin.ch/) et
dans le [dépôt
GitHub](https://github.com/blw-ofag-ufag/semantic-web-template/blob/main/src/rdf/data/glossary.skos.ttl).

<div id="tbl-glossary">

Table 3: Glossaire de la norme eCH-1234

<table>
<colgroup>
<col style="width: 35%" />
<col style="width: 65%" />
</colgroup>
<thead>
<tr>
<th style="text-align: left;">Terme</th>
<th style="text-align: left;">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: left;"><strong>Données liées</strong> (Linked
Data)</td>
<td style="text-align: left;"><p>Données publiées selon les principes du
Web sémantique: identifiées par des IRI, décrites en RDF et reliées
entre elles.</p>
<p><em>Terme associé</em>: Linked Data Service, Resource Description
Framework</p></td>
</tr>
<tr>
<td style="text-align: left;"><strong>Espace de noms</strong>
(Préfixe)</td>
<td style="text-align: left;"><p>Début commun d’un groupe d’IRI. En
Turtle et en SPARQL, un espace de noms est abrégé par un préfixe, par
exemple <code>schema:</code> pour <code>http://schema.org/</code>.</p>
<p><em>Terme associé</em>: Internationalized Resource
Identifier</p></td>
</tr>
<tr>
<td style="text-align: left;"><strong>Graphe</strong> (Graphe
nommé)</td>
<td style="text-align: left;"><p>Un ensemble de triplets. Un graphe
nommé est lui-même identifié par une IRI et permet de regrouper les
données dans un triple store.</p>
<p><em>Terme générique</em>: Resource Description Framework</p></td>
</tr>
<tr>
<td style="text-align: left;"><strong>Inférence</strong>
(Raisonnement)</td>
<td style="text-align: left;">La déduction automatique de nouvelles
déclarations à partir des données existantes et des axiomes d’une
ontologie, par exemple au moyen du raisonneur HermiT.</td>
</tr>
<tr>
<td style="text-align: left;"><strong>Internationalized Resource
Identifier</strong> (IRI)</td>
<td style="text-align: left;"><p>Identifiant unique au niveau mondial
d’une ressource. En RDF, les sujets, les prédicats et la plupart des
objets sont identifiés par des IRI.</p>
<p><em>Terme générique</em>: Resource Description Framework</p></td>
</tr>
<tr>
<td style="text-align: left;"><strong>JSON for Linking Data</strong>
(JSON-LD)</td>
<td style="text-align: left;"><p>Une sérialisation de RDF basée sur
JSON, particulièrement adaptée aux interfaces web.</p>
<p><em>Terme générique</em>: Sérialisation</p></td>
</tr>
<tr>
<td style="text-align: left;"><strong>Linked Data Service</strong>
(LINDAS)</td>
<td style="text-align: left;">Le service officiel de données liées de
l’administration fédérale suisse, fonctionnant comme un triple store
(magasin de triplets).</td>
</tr>
<tr>
<td style="text-align: left;"><strong>Littéral</strong></td>
<td style="text-align: left;"><p>Une valeur concrète en RDF, par exemple
une chaîne de caractères, un nombre ou une date, avec en option un type
de données ou une indication de langue.</p>
<p><em>Terme générique</em>: Resource Description Framework</p></td>
</tr>
<tr>
<td style="text-align: left;"><strong>Ontologie</strong></td>
<td style="text-align: left;"><p>Un modèle formel d’un domaine qui
décrit les classes, les propriétés et leurs relations logiques de
manière à permettre aux machines d’en tirer des conclusions.</p>
<p><em>Terme générique</em>: Vocabulaire</p>
<p><em>Terme associé</em>: Web Ontology Language</p></td>
</tr>
<tr>
<td style="text-align: left;"><strong>Point d’accès SPARQL</strong></td>
<td style="text-align: left;"><p>Une interface web par laquelle des
requêtes SPARQL peuvent être envoyées à un triple store.</p>
<p><em>Terme générique</em>: SPARQL Protocol and RDF Query
Language</p></td>
</tr>
<tr>
<td style="text-align: left;"><strong>Resource Description
Framework</strong> (RDF)</td>
<td style="text-align: left;">Une norme centrale du World Wide Web
Consortium (W3C) pour la modélisation des structures de données sur le
Web. Les informations ne sont pas représentées dans des tableaux
classiques, mais sous forme de graphes interconnectés.</td>
</tr>
<tr>
<td style="text-align: left;"><strong>Shape</strong></td>
<td style="text-align: left;"><p>Un ensemble de conditions qu’une classe
de ressources ou une propriété doit remplir, par exemple des champs
obligatoires, des types de données et des cardinalités.</p>
<p><em>Terme générique</em>: Shapes Constraint Language</p></td>
</tr>
<tr>
<td style="text-align: left;"><strong>Shapes Constraint
Language</strong> (SHACL)</td>
<td style="text-align: left;"><p>Le langage du W3C pour décrire et
valider la structure des données RDF. Le modèle de données de cette
norme est formulé en SHACL.</p>
<p><em>Terme spécifique</em>: Shape</p></td>
</tr>
<tr>
<td style="text-align: left;"><strong>Simple Knowledge Organization
System</strong> (SKOS)</td>
<td style="text-align: left;"><p>Un vocabulaire du W3C pour les
thésaurus, les classifications et les glossaires. Ce glossaire est
lui-même rédigé en SKOS.</p>
<p><em>Terme associé</em>: Vocabulaire</p></td>
</tr>
<tr>
<td style="text-align: left;"><strong>SPARQL Protocol and RDF Query
Language</strong> (SPARQL)</td>
<td style="text-align: left;"><p>Le langage de requête du W3C pour les
données RDF. SPARQL permet de lire des données dans des graphes, de les
modifier et de les échanger entre systèmes.</p>
<p><em>Terme associé</em>: Resource Description Framework</p></td>
</tr>
<tr>
<td style="text-align: left;"><strong>Sérialisation</strong></td>
<td style="text-align: left;"><p>Représentation textuelle d’un graphe
RDF dans un format défini, afin de le stocker ou de l’échanger.</p>
<p><em>Terme spécifique</em>: JSON for Linking Data, Terse RDF Triple
Language</p></td>
</tr>
<tr>
<td style="text-align: left;"><strong>Terse RDF Triple Language</strong>
(Turtle)</td>
<td style="text-align: left;"><p>Une sérialisation compacte et lisible
pour RDF. Tous les fichiers RDF de cette norme sont rédigés en
Turtle.</p>
<p><em>Terme générique</em>: Sérialisation</p></td>
</tr>
<tr>
<td style="text-align: left;"><strong>Triple store</strong> (Base de
données orientée graphe)</td>
<td style="text-align: left;"><p>Une base de données spécialisée dans le
stockage et l’interrogation de triplets RDF.</p>
<p><em>Terme associé</em>: Linked Data Service</p></td>
</tr>
<tr>
<td style="text-align: left;"><strong>Triplet</strong></td>
<td style="text-align: left;"><p>La structure de base d’une déclaration
en RDF, composée d’un sujet, d’un prédicat et d’un objet.</p>
<p><em>Terme générique</em>: Resource Description Framework</p></td>
</tr>
<tr>
<td style="text-align: left;"><strong>Vocabulaire</strong></td>
<td style="text-align: left;"><p>Un ensemble de classes et de propriétés
à la signification définie, réutilisé pour décrire des données, par
exemple schema.org.</p>
<p><em>Terme spécifique</em>: Ontologie</p></td>
</tr>
<tr>
<td style="text-align: left;"><strong>Web Ontology Language</strong>
(OWL)</td>
<td style="text-align: left;"><p>Le langage du W3C pour formuler des
ontologies. Il permet de définir des classes et des propriétés au moyen
d’axiomes logiques.</p>
<p><em>Terme associé</em>: Inférence</p></td>
</tr>
</tbody>
</table>

</div>

# Annexe D – Modifications par rapport à la version précédente

Les principales modifications de la version 2.0.0 par rapport à la
version précédente 1.4.6:

- **Modèle de document:** la sortie PDF suit désormais le modèle de
  document eCH (page de titre avec tableau des métadonnées, en-tête et
  pied de page, table des matières, annexes); le site web reprend le
  même style dans une variante claire et une variante sombre.
- **Métadonnées:** le numéro, la catégorie, le degré de maturité, la
  version, le statut et les autres indications de la norme sont saisis
  une seule fois et repris automatiquement dans toutes les versions
  linguistiques, dans la page de titre, dans le pied de page et dans
  <a href="#sec-status" class="quarto-xref">Section 1.1</a>.
- **Listes:** la table des illustrations et la liste des tableaux
  (annexes E et F) sont générées automatiquement et reliées aux
  illustrations et aux tableaux.
- **Présentation:** mise en forme uniforme des tableaux, des légendes et
  du code dans le PDF et sur le site web.

La liste complète de toutes les modifications par version se trouve dans
les [releases sur
GitHub](https://github.com/blw-ofag-ufag/semantic-web-template/releases).

# Annexe E – Table des illustrations

# Annexe F – Liste des tableaux

[^1]: Sur le site web, les notes de bas de page apparaissent dans la
    marge de droite; dans le PDF, en bas de page.

[^2]: Une seconde note de bas de page avec un lien vers
    [ech.ch](https://www.ech.ch/).
