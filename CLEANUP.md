# Schritt-für-Schritt-Anleitung: Template bereinigen und Fachprojekt einrichten

Dieses Repository dient als Vorlage (*Template*) für Semantic-Web-Pipelines. Es enthält eine funktionale Demo-Pipeline auf Basis der Chinook-Musikdatenbank (ca. 120'000 Tripel) inklusive ETL, OWL-Reasoning, SPARQL-Regeln, SHACL-Validierung, Quarto-Dokumentation und LINDAS-Deployment.

Folge dieser Anleitung, um die Demo-Komponenten schrittweise zu entfernen und durch dein eigenes Fachmodell zu ersetzen.

---

## 1. Lokale Entwicklungsumgebung initialisieren

### 1.1 Systemvoraussetzungen prüfen
Stelle sicher, dass folgende Werkzeuge auf deinem System installiert sind:

* **Python 3** (>= 3.10)
* **Java JRE/JDK** (>= 11, erforderlich für ROBOT und HermiT-Reasoning)
* **Quarto CLI** (für das Rendern der Dokumentation)
* **curl** (für das LINDAS-Deployment)

Prüfung im Terminal:
```bash
python3 --version
java -version
quarto --version
```

### 1.2 Automatisches Setup via Makefile
Das Repository verwaltet seine Python-Umgebung und externe Binärdateien autonom. Es wird keine manuelle `requirements.txt` auf Root-Ebene gepflegt. Führe im Projektverzeichnis aus:

```bash
make setup
```

**Was dieser Befehl automatisch ausführt:**
* Erstellt eine isolierte virtuelle Python-Umgebung im Verzeichnis `venv/`.
* Aktualisiert pip und installiert alle benötigten Pakete (rdflib, pyshacl, pytest etc.) aus `src/python/requirements.txt`.
* Lädt das Werkzeug `robot.jar` (v1.9.5) für OWL-Reasoning und Merging direkt nach `venv/bin/robot.jar` herunter.

> **Hinweis für Posit Workbench / Pfade mit Sonderzeichen (`@`):**  
> Sollte VS Code `Unable to handle .../.venv` melden, setze den Python-Interpreter manuell über die Befehlspalette:  
> `Ctrl + Shift + P` -> `Python: Select Interpreter` -> `Enter interpreter path...` -> `venv/bin/python` eingeben.

---

## 2. Demo-Daten entfernen und Fachmodell aufbauen

Passe die Dateien in `src/` schrittweise an dein Projekt an:

### 2.1 Vokabular & Basis-Namensräume (src/rdf/prefixes.ttl)

Die Datei (src/rdf/prefixes.ttl) dient für alle im Projekt verwendeten Namensräume und QNames. 

> **Wichtig:** Halte nach Möglichkeit  alle Präfixe des Projekts in dieser Datei fest. 

---

#### Die 3 Blöcke der Datei verstehen und anpassen

Die Datei ist in drei klar abgegrenzte Zonen unterteilt:

 **Block 1 (`# Project-specific`):** / Ersetzen. 

Lösche die Demo-Präfixe (`album:`, `artist:`, `track:` etc.)und trage dort deine eigene Projekt-Basis-URI sowie die Sub-Namensräume für Instanzen ein.

 **Block 2 (`# LINDAS-specific`):** / Optional stehen lassen.

Diese Präfixe (`cube:`, `org:`, `meta:` etc.) werden eingesetzt, wenn du Daten speziell für LINDAS strukturierst (z. B. für multidimensionale Datenwürfel/Cubes). 

 **Block 3 (`# Globally used`):** / Beibehalten.

Enthält W3C- und QUDT-Standards (`rdf:`, `owl:`, `sh:`, `skos:`, `xsd:` etc.), die das Build-System und die Validierung zwingend voraussetzen.

**Schreibweisen (Casing):**

  - Klassen und Individuen: Werden in `PascalCase` geschrieben 
  (z. B. `ex:LandwirtschaftlicherBetrieb`).
  - Properties: Werden in `camelCase` ohne vorangestellte Verben geschrieben 
  (z. B. `ex:betriebsNummer`, nicht `ex:hasBetriebsNummer`).

---

### 2.2 Ontologie (`src/rdf/ontology/model.owl.ttl`)
1. Entferne die Klassen und Eigenschaften der Chinook-Demo.
2. Definiere dein eigenes OWL-Modell unter Einhaltung der Namenskonventionen:
   - **Klassen (`owl:Class`):** Verwende `PascalCase` (z. B. `ex:Betrieb`).
   - **Properties (`owl:ObjectProperty`, `owl:DatatypeProperty`):** Verwende `camelCase` ohne vorangestelltes Verb (z. B. `ex:betriebsNummer`, nicht `ex:hasBetriebsNummer`).

---

### 2.3 SKOS-Glossar (`src/rdf/data/glossary.skos.ttl`)
- **Wichtig:** Diese Datei darf **nicht gelöscht** werden, da der Quarto-Generator `src/python/utils/generate_glossary_docs.py` zwingend darauf zugreift.
- Ersetze die Demo-Konzepte durch deine fachspezifischen SKOS-Konzepte (`skos:ConceptScheme`, `skos:Concept`).

---

### 2.4 SHACL-Validierungsregeln (`src/rdf/shapes/model.shacl.ttl`)
1. Entferne die Demo-Shapes (Artist, Album, Track, Invoice).
2. Definiere `sh:NodeShape` und Property-Constraints für deine neuen Ontologie-Klassen, um Pflichtfelder, Datentypen und Kardinalitäten abzusichern.

---

### 2.5 Statische Instanzdaten (`src/rdf/data/*.ttl`)
- Lösche alle Demo-Dateien in `src/rdf/data/` (ausser `glossary.skos.ttl`).
- Hinterlege hier statische Turtle-Dateien mit Stammdaten oder festen Vokabularen.

---

### 2.6 Datenintegration & ETL-Pipeline (`src/python/pipeline/`)

Das Template ermöglicht es, externe Datenquellen wie relationale Datenbanken, APIs oder CSV-Dateien über Python abzufragen und als RDF-Tripel in den Build einzuspeisen.

Alle Python-Skripte im Verzeichnis `src/python/pipeline/` werden vom Makefile alphabetisch sortiert ausgeführt. Jedes Skript erhält dabei den CLI-Parameter `--output build/rdf/00-integrated.ttl`.

Wähle je nach Anwendungsfall eine der beiden Varianten:

#### Option A: Mit ETL-Pipeline (Dynamische Datenquellen)
1. Lösche das Chinook-Demo-Skript:
   ```bash
   rm src/python/pipeline/01_integrate_example_data.py
   ```
2. Hinterlege dein eigenes Import-Skript im selben Ordner (z. B. `src/python/pipeline/01_import_daten.py`).
3. Dein Skript muss das Argument `--output <zielpfad>` akzeptieren (z. B. via `argparse`) und die serialisierten Tripel als Turtle an diesen Pfad schreiben.

#### Option B: Ohne ETL-Pipeline (Reine statische Turtle-Dateien)
1. Lösche alle Python-Dateien im Verzeichnis:
   ```bash
   rm -f src/python/pipeline/*.py
   ```
2. Das Makefile erkennt automatisch, dass keine Skripte vorhanden sind, und erzeugt eine leere Datei.

---

### 2.7 SPARQL-Post-Processing (`src/sparql/processing/`)

In diesem Schritt können nach dem Reasoning (HermiT) gezielte Graph-Transformationen, Datenbereinigungen oder Berechnungen durchgeführt werden. 

Das Makefile übergibt alle .rq -Dateien in `src/sparql/processing/` an das Werkzeug ROBOT 
Das Ergebnis wird als `build/rdf/03-processed.ttl` serialisiert und bildet die Grundlage für die anschliessende SHACL-Validierung.

#### Demo-Dateien bereinigen
Lösche bestehende Demo-Abfragen:
```bash
rm -f src/sparql/processing/*.rq
```

#### Auswahl: Mit oder ohne SPARQL-Updates

* **Option A: Ohne SPARQL-Updates (Standard)**  
  Wenn dein Modell keine nachgelagerten Graph-Updates benötigt, bleibt der Ordner `src/sparql/processing/` einfach leer. Das Makefile erkennt dies automatisch und kopiert die Daten ohne Transformation weiter (`02-inferred.ttl` zu `03-processed.ttl`).

* **Option B: Mit SPARQL-Updates (Eigene Regeln anhängen)**  
  Wenn du eigene Graph-Modifikationen benötigst, gehst du wie folgt vor:

  1. Datei anlegen: Erstelle eine Datei im Ordner `src/sparql/processing/` mit der Endung `.rq` (z. B. `src/sparql/processing/01_berechne_status.rq`).
  2. Update-Syntax verwenden: Verwende ausschliesslich SPARQL 1.1 Update Befehle (`INSERT`, `DELETE` oder `DELETE/INSERT`). Reine Lese-Abfragen (`SELECT`) führen zu einem Build-Abbruch.
  3. Präfixe deklarieren: Definiere alle benötigten Präfixe direkt am Anfang der `.rq`-Datei.

  Sobald die Datei gespeichert ist, wendet `make test` dieses Update bei jedem Build automatisch auf den Wissensgraphen an.

---

## 3. Projektdokumentation anpassen (`docs/`)

Das Template generiert mit Quarto eine mehrsprachige Dokumentations-Website unter `build/docs/`. 

Damit die Dokumentation vollständig zum eigenen Projekt passt und fehlerfrei baut, muss verstanden werden, welche Teile automatisch entstehen und welche zwingend von Hand bearbeitet werden müssen:

* **Automatisch generiert:** Die Seiten `entities.qmd` (aus `model.shacl.ttl`) und `glossary.qmd` (aus `glossary.skos.ttl`) werden bei jedem Aufruf von `make docs` neu aus deinen RDF-Modelldateien erzeugt. Hier muss nichts manuell editiert werden.
* **Manuell zu pflegen:** Die globale Konfiguration (`_quarto.yml`) und die Startseiten (`index.qmd`) in den Sprachordnern müssen zwingend selbst angepasst werden. Werden sie nicht bearbeitet, zeigt die fertige Website weiterhin alte Vorlagentexte an.

---

### 3.1 Website-Gerüst konfigurieren (`docs/_quarto.yml`)

Die Datei `docs/_quarto.yml` steuert das Design, die Menüleiste und die Exportformate.

Passe die Metadaten an dein Projekt an:
* **`website.title`:** Titel deines Projekts.
* **`website.repo-url`:** Link zu deinem GitHub-Repository.
* **`website.announcement`:** Text des oberen Hinweises anpassen oder den Block entfernen, falls kein Banner gewünscht ist.
* **`navbar`:** Links zu GitHub, E-Mail-Adresse und die Sprachumschalter prüfen.

> **Wichtiger Bugfix für `make docs`:**  
> In der Vorlage ist unter dem Format `docx:` ein Verweis auf ein externes Word-Template hinterlegt (`reference-doc: https://s.zazuko.com/MHXTkQ`). Diese URL liefert einen HTTP-404-Fehler und bricht den Build ab.  
> Kommentiere diese Zeile in `docs/_quarto.yml` zwingend aus:
> ```yaml
>   docx:
>     toc: true
>     toc-depth: 2
>     number-sections: true
>     # reference-doc: [https://s.zazuko.com/MHXTkQ](https://s.zazuko.com/MHXTkQ)
>     link-citations: true
> ```

---

### 3.2 Startseiten austauschen (`docs/{de,en,fr}/index.qmd`)

In den Sprachordnern liegt jeweils eine manuell gepflegte Einstiegsseite:
* `docs/de/index.qmd` (Deutsch)
* `docs/en/index.qmd` (Englisch)
* `docs/fr/index.qmd` (Französisch)

Ersetze die Vorlagentexte durch deine eigene Projektbeschreibung (Einleitung, Modellübersicht, Fachkontext).

#### Vorgaben der Testsuite für `index.qmd`
Damit `tests/test_translations.py` fehlerfrei durchläuft, gelten zwei feste Regeln:

1. **Überschriften-Referenzen:** Jede Überschrift muss eine feste ID besitzen.
2. **Strukturgleichheit:** Die Überschriften-IDs müssen in allen gepflegten Sprachdateien (`de`, `en`, `fr`) synchron vorhanden sein.

---

### 3.3 Sprachumfang festlegen (Mehrsprachig vs. Einsprachig)

Standardmässig ist das Template auf Dreisprachigkeit ausgelegt (`de`, `en`, `fr`):

* **Projekt bleibt mehrsprachig:**  
  Pflege alle drei Startseiten (`docs/de/`, `docs/en/`, `docs/fr/`) und stelle sicher, dass alle Labels und Fehlermeldungen in `model.shacl.ttl` mit Sprach-Tags (`@de`, `@en`, `@fr`) versehen sind.
* **Projekt wird rein deutsch geführt:**  
  1. Lösche die nicht benötigten Sprachverzeichnisse:
     ```bash
     rm -rf docs/en docs/fr
     ```
  2. Entferne die gelöschten Pfade (`- fr/index.qmd`, `- en/index.qmd`) unter `render:` in der Datei `docs/_quarto.yml`.  
  Die Testsuite und Quarto erkennen die verbleibende Sprache automatisch.

---

### 3.4 Dokumentation lokal bauen und prüfen

Führe den Build-Befehl im Terminal aus:

```bash
make docs
```

Das Makefile führt automatisch die Skripte `generate-shacl-docs` und `generate-glossary-docs` aus und kompiliert die Website mit Quarto.


---

## 4. Lokale Pipeline ausführen und validieren

Nachdem alle Modelldateien, Daten und Texte hinterlegt sind, wird der gesamte Build über das Makefile getestet.

### 4.1 Build-Schritte im Terminal

Führe die Schritte der Reihe nach aus:

1. Vorherige Build-Artefakte entfernen:
   Löscht alte Zwischenstände, temporäre Dateien und Log-Protokolle restlos aus dem Arbeitsverzeichnis:
   ```bash
   make clean
   ```

2. Pipeline ausführen und validieren: 
   Startet die Datenintegration, führt die Syntax-Prüfung aus, mergt alle RDF-Dateien mit ROBOT, berechnet Inferenzen mit HermiT, wendet SPARQL-Regeln an und prüft den Graphen via pySHACL und Pytest:
   ```bash
   make test
   ```

3. Dokumentation generieren: 
   Erzeugt automatisch die Tabellen aus den SHACL-Shapes, baut den SKOS-Katalog auf und rendert die Quarto-Website nach `build/docs/`:
   ```bash
   make docs
   ```

4. Vollständigen Standard-Build ausführen:
   Führt als Standard-Ziel `make test` gefolgt von `make docs` am Stück aus:
   ```bash
   make
   ```

---

### 4.2 Log-Dateien zur gezielten Fehlersuche

Das Makefile leitet Zwischenausgaben in Log-Dateien um, damit das Terminal übersichtlich bleibt. Schlägt ein Schritt fehl, enthält das Verzeichnis `build/log/` die detaillierten Fehlermeldungen:

* **`build/log/01-merge.log`:** Fehler beim ROBOT-Merge (z. B. ungebundene Präfixe oder Syntaxfehler in einzelnen.Dateien).
* **`build/log/02-infer.log`:** Logische Inkonsistenzen beim HermiT-Reasoning (z. B. widersprüchliche.OWL-Disjointness-Axiome).
* **`build/log/03-query.log`:** Syntax- oder Laufzeitfehler in deinen SPARQL-Update-Queries (`src/sparql/processing/*.rq`).
* **`build/log/04-shacl.log`:** Detaillierter pySHACL-Bericht über Validierungsverstösse mit betroffenen Subjekten. und Pfaden.
* **`build/log/05-quarto.log`:** Pandoc- und Quarto-Fehler beim Kompilieren der Markdown- und HTML-Seiten.

## 5. Deployment auf LINDAS

Das Repository unterstützt sowohl das automatische Release über GitHub Actions als auch manuelle Uploads von der lokalen Workstation.

### 5.1 Zugangsdaten & Konfiguration

Für den Zugriff auf LINDAS werden vier zentrale Verbindungsparameter benötigt:

| Parameter | Beschreibung | Beispielwert |
| :--- | :--- | :--- |
| `ENDPOINT` | SPARQL-Update-Endpunkt von LINDAS | `https://test.lindas.admin.ch/sparql` |
| `USER` | Technischer Service-Benutzer | `blw-service-account` |
| `PASSWORD` | Passwort des Service-Benutzers | `mein-sicheres-passwort` |
| `GRAPH` | Vollständige URI des Ziel-Named-Graphs | `https://agriculture.ld.admin.ch/foag/mein-projekt` |

* **Für automatisches Deployment (Standard):**  
  Hinterlege die vier Variablen in deinem GitHub-Repository unter:  
  `Settings > Secrets and variables > Actions > New repository secret`.
* **Für manuelle Direkt-Uploads (Optional):**  
  Erstelle im Root-Verzeichnis eine Datei `.env` (wird von Git ignoriert) und trage die Werte dort ein:
  ```dotenv
  ENDPOINT="[https://test.lindas.admin.ch/sparql](https://test.lindas.admin.ch/sparql)"
  USER="blw-service-account"
  PASSWORD="mein-sicheres-passwort"
  GRAPH="[https://agriculture.ld.admin.ch/foag/mein-projekt](https://agriculture.ld.admin.ch/foag/mein-projekt)"
  ```

---

### 5.2 Automatisches Deployment (GitHub Actions)

Das Repository enthält eine CI/CD-Pipeline, die bei jedem Push oder Pull-Request-Merge auf den Branch `main` automatisch aktiv wird. Sobald die GitHub Secrets hinterlegt sind, führt der GitHub-Runner die Testsuite aus und publiziert den Wissensgraphen bei Erfolg automatisch auf LINDAS.

---

### 5.3 Manuelle Publikation

Sobald `make test` lokal fehlerfrei durchläuft und die Datei `.env` gepflegt ist, stehen folgende Befehle zur Verfügung:

1. **Graphen auf LINDAS publizieren:**  
   Führt automatisch `make test` aus, leert den Ziel-Named-Graph auf LINDAS und lädt `build/rdf/03-processed.ttl` hoch:
   ```bash
   make publish
   ```

2. **Bestehenden Remote-Graphen leeren:**  
   Löscht ausschliesslich die Daten im angegebenen Named Graph auf LINDAS, ohne neue Tripel hochzuladen:
   ```bash
   make delete
   ```

---

Damit ist die Bereinigung und Ersteinrichtung des Repositories abgeschlossen. Das Template ist nun vollständig auf dein eigenes Datenmodell umgestellt, lokal validiert und bereit für die produktive Weiterentwicklung sowie automatische Releases auf LINDAS.

