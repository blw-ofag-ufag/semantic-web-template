#show: doc => ech-document(
$if(title)$
  title: [$title$],
$endif$
$if(date)$
  date: [$date$],
$endif$
$if(abstract)$
  abstract: [$abstract$],
$endif$
$if(lang)$
  lang: "$lang$",
$endif$
$if(region)$
  region: "$region$",
$endif$
$if(mainfont)$
  font: ("$mainfont$",),
$endif$
$if(fontsize)$
  fontsize: $fontsize$,
$endif$
$if(section-numbering)$
  sectionnumbering: "$section-numbering$",
$endif$
$if(toc)$
  toc: $toc$,
$endif$
$if(toc-title)$
  toc_title: [$toc-title$],
$endif$
  toc_depth: $toc-depth$,
  ech: (
$if(ech.number)$
    number: [$ech.number$],
$endif$
$if(ech.category)$
    category: [$ech.category$],
$endif$
$if(ech.maturity)$
    maturity: [$ech.maturity$],
$endif$
$if(ech.version)$
    version: [$ech.version$],
$endif$
$if(ech.status)$
    status: [$ech.status$],
$endif$
$if(ech.decision-date)$
    decision-date: [$ech.decision-date$],
$endif$
$if(ech.replaces)$
    replaces: [$ech.replaces$],
$endif$
$if(ech.prerequisites)$
    prerequisites: ($for(ech.prerequisites)$[$ech.prerequisites$],$endfor$),
$endif$
$if(ech.attachments)$
    attachments: ($for(ech.attachments)$[$ech.attachments$],$endfor$),
$endif$
$if(ech.languages)$
    languages: ($for(ech.languages)$[$ech.languages$],$endfor$),
$endif$
$if(ech.group)$
    group: [$ech.group$],
$endif$
$if(ech.publisher)$
    publisher: [$ech.publisher$],
$endif$
  ),
  doc,
)
