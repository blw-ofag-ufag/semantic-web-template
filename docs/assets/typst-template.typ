#let article(
  title: none,
  authors: none,
  date: none,
  abstract: none,
  abstract-title: none,
  cols: 1,
  margin: (x: 2.5cm, y: 3.5cm),
  paper: "us-letter",
  lang: "en",
  region: "US",
  font: (),
  fontsize: 11pt,
  sectionnumbering: none,
  toc: false,
  toc_title: none,
  toc_depth: none,
  toc_indent: 1.5em,
  doc,
  ..args,
) = {

  set page(
    paper: paper,
    margin: margin,
    header: context [
      #grid(
        columns: (35%, 1fr),
        align(left + bottom)[#image("../assets/ech.svg", width: 100%)],
        align(right + bottom)[Page #counter(page).display() of #counter(page).final().first()]
      )
      #v(0.25em)
      #line(length: 100%, stroke: 0.5pt + black)
    ],
    footer: [
      #line(length: 100%, stroke: 0.5pt + black)
      #v(0.25em)
      #align(left)[Verein eCH]
    ]
  )

  // Wire up the mainfont, fontsize, and language passed from Quarto's YAML
  set text(size: fontsize, lang: lang, region: region)
  set text(font: font) if font != none and font != ()
  
  set par(leading: 0.8em)
  
  // Wire up section-numbering passed from Quarto's YAML
  set heading(numbering: sectionnumbering) if sectionnumbering != none
  
  show heading.where(level: 1): it => {
    colbreak(weak: true)
    it
  }
  show heading.where(level: 1): set text(size: 16pt, weight: "bold")
  show heading.where(level: 2): set text(size: 12pt, weight: "bold")
  show heading: set block(above: 1.8em, below: 1em)
  
  show outline: set text(size: fontsize)
  show outline: set par(spacing: 1.25em)
  show figure.caption: set text(size: 10pt)
  show table.cell: set text(size: 10pt)
  show table.cell: set par(justify: false)
  show footnote.entry: set text(size: 10pt)
  show link: set text(fill: rgb("#D00D28"))
  
  set table(
    fill: (col, row) => if calc.even(row) { rgb("f2f2f2") } else { white },
    stroke: (x, y) => (
      left: none,
      right: none,
      top: if y == 0 { none } else { 0.5pt + black },
      bottom: none,
    )
  )
  show table.cell.where(y: 0): set text(weight: "bold")
  show table: it => block(
    stroke: (top: 1pt + black, bottom: 1pt + black),
    inset: (top: 0.5pt, bottom: 0.5pt),
    outset: 0pt,
    breakable: true,
    it
  )

  // Render Title
  if title != none {
    align(center)[
      #block(text(weight: "bold", size: 1.8em, title))
      #v(1em)
    ]
  }

  // Render Authors (if any)
  if authors != none {
    align(center)[#authors]
    v(1em)
  }

  // Render Date (if any)
  if date != none {
    align(center)[#block(text(size: 11pt, date))]
    v(1em)
  }

  // Render Abstract / Summary (Standalone page)
  if abstract != none {
    pagebreak(weak: true)
    
    if abstract-title != none {
      heading(level: 1, numbering: none)[#abstract-title]
    }
    
    // Abstract formatting
    block(text(size: fontsize, abstract))
  }

  // Render Table of Contents (Standalone page)
  if toc {
    pagebreak(weak: true)
    
    let title = if toc_title != none { toc_title } else { auto }
    outline(title: title, depth: toc_depth, indent: toc_indent)
  }

  // Start Main Document Body (Standalone page)
  pagebreak(weak: true)

  if cols == 1 {
    doc
  } else {
    columns(cols, doc)
  }
}