// eCH document template for Quarto's Typst (PDF) output.
//
// The layout follows the eCH Word template (eCH-0003 V11.1.0, attachment
// "XXXX_d_DRA_JJJJ-MM-TT_eCH-0XXX_Vx.x.x_Titel.docx") and the published eCH
// standards: a title page with the metadata table and the summary, the table
// of contents on a new page, a header with the eCH logo, the tagline and the
// page count, and a two-line footer with the document identification.
//
// Metadata is passed from the document front matter via typst-show.typ:
//
//   title, date, abstract, lang    standard Quarto fields
//   ech.number                     eCH-0000
//   ech.category                   Standard, Best Practice, Hilfsmittel, ...
//   ech.maturity                   Reifegrad
//   ech.version                    x.y.z
//   ech.status                     In Arbeit, Entwurf, Vorschlag, Genehmigt, ...
//   ech.decision-date              Beschluss am (date is used as Ausgabedatum)
//   ech.replaces                   Ersetzt Version
//   ech.prerequisites              Voraussetzungen (string or list)
//   ech.attachments                Beilagen (string or list)
//   ech.languages                  Sprachen (string or list)
//   ech.group                      Fachgruppe
//   ech.publisher                  Herausgeber / Vertrieb (defaults to Verein eCH)
//
// Missing fields are shown as "---", as in published eCH documents.

// Labels of the eCH template in its three languages, selected by `lang`.
#let ech-labels = (
  de: (
    tagline: "E-Government Standards",
    page: (current, total) => [Seite #current von #total],
    organisation: "Verein eCH",
    publisher: [
      Verein eCH, Affolternstrasse 52, 8050 Zürich \
      T 044 388 74 64 / #link("mailto:info@ech.ch", "info@ech.ch") / #link("https://www.ech.ch", "www.ech.ch")
    ],
    summary: "Zusammenfassung",
    fields: (
      name: "Name",
      number: "eCH-Nummer",
      category: "Kategorie",
      maturity: "Reifegrad",
      version: "Version",
      status: "Status",
      decision-date: "Beschluss am",
      issue-date: "Ausgabedatum",
      replaces: "Ersetzt Version",
      prerequisites: "Voraussetzungen",
      attachments: "Beilagen",
      languages: "Sprachen",
      group: "Fachgruppe",
      publisher: "Herausgeber / Vertrieb",
    ),
  ),
  fr: (
    tagline: "Normes en cyberadministration",
    page: (current, total) => [page #current sur #total],
    organisation: "Association eCH",
    publisher: [
      Association eCH, Affolternstrasse 52, 8050 Zurich \
      T 044 388 74 64 / #link("mailto:info@ech.ch", "info@ech.ch") / #link("https://www.ech.ch", "www.ech.ch")
    ],
    summary: "Résumé",
    fields: (
      name: "Nom",
      number: "Numéro eCH",
      category: "Catégorie",
      maturity: "Degré de maturité",
      version: "Version",
      status: "Statut",
      decision-date: "Date de décision",
      issue-date: "Date de publication",
      replaces: "Remplace la version",
      prerequisites: "Conditions préalables",
      attachments: "Annexes",
      languages: "Langues",
      group: "Groupe spécialisé",
      publisher: "Éditeur / distribution",
    ),
  ),
  en: (
    tagline: "E-Government Standards",
    page: (current, total) => [Page #current of #total],
    organisation: "eCH registered association",
    publisher: [
      eCH registered association, Affolternstrasse 52, 8050 Zurich \
      T 044 388 74 64 / #link("mailto:info@ech.ch", "info@ech.ch") / #link("https://www.ech.ch", "www.ech.ch")
    ],
    summary: "Summary",
    fields: (
      name: "Name",
      number: "eCH-number",
      category: "Category",
      maturity: "Quality stage",
      version: "Version",
      status: "Status",
      decision-date: "Decision on",
      issue-date: "Date of issue",
      replaces: "Replaces version",
      prerequisites: "Requirements",
      attachments: "Annexes",
      languages: "Languages",
      group: "Technical Unit",
      publisher: "Editor / Distribution",
    ),
  ),
)

// Renders a metadata value: "---" when missing, a bullet list when several.
#let ech-value(value) = {
  if value == none { return "---" }
  if type(value) == array {
    if value.len() == 0 { return "---" }
    if value.len() == 1 { return value.first() }
    return list(..value)
  }
  value
}

#let ech-document(
  title: none,
  date: none,
  abstract: none,
  lang: "de",
  region: none,
  font: ("Nimbus Sans",),
  fontsize: 11pt,
  sectionnumbering: "1.1.1",
  toc: true,
  toc_title: none,
  toc_depth: 3,
  ech: (:),
  doc,
) = {
  let labels = ech-labels.at(lang, default: ech-labels.en)
  let ech = if type(ech) == dictionary { ech } else { (:) }
  let meta(key) = ech.at(key, default: none)

  let number = meta("number")
  let full-title = if number == none { title } else [#number – #title]
  let identification = [
    #full-title / #ech-value(meta("version")) / *#ech-value(meta("status"))* / #ech-value(date)
  ]

  // Document ----------------------------------------------------------------

  set document(title: full-title)
  set text(font: font, size: fontsize, lang: lang, hyphenate: true)
  set text(region: region) if region != none
  set par(justify: true, leading: 0.65em, spacing: 1.2em)
  set heading(numbering: sectionnumbering)

  // Page: A4 with 2 cm left and 1.5 cm right margin; header and footer are
  // separated from the body by a thin rule.
  set page(
    margin: (top: 3.1cm, bottom: 3.2cm, left: 2cm, right: 1.5cm),
    header-ascent: 0.5cm,
    footer-descent: 0.5cm,
    header: context {
      set text(size: 11pt)
      grid(
        columns: (auto, 1fr, auto),
        column-gutter: 0.45cm,
        align: bottom,
        image("../assets/ech.svg", height: 1.14cm),
        labels.tagline,
        (labels.page)(counter(page).display(), counter(page).final().first()),
      )
      v(0.3cm)
      line(length: 100%, stroke: 0.5pt)
    },
    footer: {
      set text(size: 10pt)
      set par(leading: 0.5em, justify: false)
      show link: underline
      line(length: 100%, stroke: 0.5pt)
      v(0.2cm)
      grid(
        columns: (1fr, auto),
        row-gutter: 0.6em,
        labels.organisation,
        [#link("https://www.ech.ch", "www.ech.ch") / #link("mailto:info@ech.ch", "info@ech.ch")],
        grid.cell(colspan: 2, identification),
      )
    },
  )

  // Headings: numbered chapters and the first appendix start on a new page,
  // the remaining appendices and other unnumbered chapters do not.
  let previous-numbered = state("ech-previous-numbered", false)
  show heading.where(level: 1): it => {
    context if it.numbering != none or previous-numbered.get() { pagebreak(weak: true) }
    previous-numbered.update(it.numbering != none)
    it
  }
  show heading.where(level: 1): set text(size: 16pt)
  show heading.where(level: 2): set text(size: 12pt)
  show heading.where(level: 3): set text(size: 11pt)
  show heading: set block(above: 1.8em, below: 1em)
  show heading.where(level: 1): set block(below: 1.4em)

  // Table of contents: levels 1 and 2 bold, numbers in a fixed column,
  // unnumbered chapters (appendices) across the full width.
  show outline.entry: it => {
    set text(size: if it.level == 1 { 12pt } else { 11pt })
    set text(weight: "bold") if it.level <= 2
    show link: set text(fill: black)
    let cells = if it.prefix() == none {
      (grid.cell(colspan: 2, it.inner()),)
    } else {
      (it.prefix(), it.inner())
    }
    link(it.element.location(), grid(columns: (1.5cm, 1fr), ..cells))
  }
  show outline.entry.where(level: 1): set block(above: 1.2em)
  show outline: set par(spacing: 0.7em)

  // Links, code, figures, footnotes.
  show link: set text(fill: rgb("#D00D28"))
  show link: it => {
    show raw: underline.with(stroke: 0.75pt, offset: 1.25pt)
    it
  }
  show raw.where(block: false): it => {
    // Allow line breaks inside long inline code such as URIs.
    show text: t => {
      let clean = t.text.replace("\u{200b}", "")
      let spaced = clean.clusters().join("\u{200b}")
      if t.text == spaced { t } else { spaced }
    }
    it
  }
  show figure.caption: set text(size: 10pt)
  show footnote.entry: set text(size: 10pt)

  // Tables: bold header row, zebra stripes, rules above and below.
  show table.cell: set text(size: 10pt)
  show table.cell: set par(justify: false)
  show table.cell.where(y: 0): set text(weight: "bold")
  set table(fill: (col, row) => if calc.even(row) { rgb("f2f2f2") } else { white })
  show table: it => block(
    stroke: (top: 1pt + black, bottom: 1pt + black),
    inset: (top: 0.5pt, bottom: 0.5pt),
    outset: 0pt,
    breakable: true,
    it,
  )

  // Title page ----------------------------------------------------------------

  {
    set par(justify: false, leading: 0.45em)
    set text(size: 18pt, weight: "bold")
    block(below: 1cm, full-title)
  }

  {
    set par(justify: false)
    show link: underline
    let publisher = if meta("publisher") == none { labels.publisher } else { meta("publisher") }
    let rows = (
      (labels.fields.name, title),
      (labels.fields.number, number),
      (labels.fields.category, meta("category")),
      (labels.fields.maturity, meta("maturity")),
      (labels.fields.version, meta("version")),
      (labels.fields.status, meta("status")),
      (labels.fields.decision-date, meta("decision-date")),
      (labels.fields.issue-date, date),
      (labels.fields.replaces, meta("replaces")),
      (labels.fields.prerequisites, meta("prerequisites")),
      (labels.fields.attachments, meta("attachments")),
      (labels.fields.languages, meta("languages")),
      (labels.fields.group, meta("group")),
      (labels.fields.publisher, publisher),
    )
    grid(
      columns: (4.6cm, 1fr),
      stroke: 0.5pt,
      inset: (x: 4pt, y: 7pt),
      align: (x, y) => if x == 0 { horizon } else { top },
      ..rows.map(((label, value)) => (strong(label), ech-value(value))).flatten(),
    )
  }

  if abstract != none {
    block(above: 1.1cm, below: 0.6cm, text(size: 16pt, weight: "bold", labels.summary))
    abstract
  }

  pagebreak()

  // Table of contents and body --------------------------------------------------

  if toc {
    outline(title: toc_title, depth: toc_depth, indent: 0pt)
  }

  doc
}

#set table(
  inset: 6pt,
  stroke: none
)
