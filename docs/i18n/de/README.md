<div align="center">

<h1><img src="../../assets/harneloop-mark.svg" alt="" width="56" height="56" align="absmiddle" /> Harneloop</h1>

<p>Artefaktbewusste Harness-Entwicklung für KI-Agenten.</p>

<p><a href="https://harneloop.kaelux.dev/">Website</a> · <a href="#agent-quick-start">Schnellstart</a> · <a href="#documentation">Dokumentation</a></p>

</div>

<!-- i18n-switcher:start -->
[English](../../../README.md) | [Español](../es/README.md) | [简体中文](../zh-CN/README.md) | [Français](../fr/README.md) | [日本語](../ja/README.md) | Deutsch | [Português (Brasil)](../pt-BR/README.md)
<!-- i18n-switcher:end -->

**Helft einem KI-Agenten, aus Fehlern zu lernen.**

Ein Agent kann eine Aufgabe abschließen, Erfolg melden und trotzdem defekten Code, ein schlechtes Rendering oder einen unbrauchbaren Workflow hinterlassen. Harneloop gibt eurem bestehenden Agenten eine strukturierte Möglichkeit, das Ergebnis zu prüfen, seine Aktionen nachzuvollziehen, den wahrscheinlichen Fehler zu finden und einen besseren Ansatz zu testen.

Der Agent verbessert seinen **Harness**: Anweisungen, Werkzeuge, Kontext und Prüfungen rund um das Modell. Das Modell selbst muss nicht neu trainiert werden. Ein vorgeschlagener Wechsel wird erst zur Arbeitsversion, wenn ein Test ihn stützt.

<a id="what-can-you-use-it-for"></a>
## Wofür könnt ihr es nutzen?

Nutzt Harneloop, wenn ein Agent ähnliche Fehler wiederholt und ihr seine Ergebnisse prüfen könnt. Beispiele sind Code und Tests, Browser-Workflows, erzeugte Dokumente und visuelle Aufgaben. Die erste veröffentlichte Fallstudie ist Blender-Szenenbau mit ViperMesh; andere Aufgabenfamilien bleiben Möglichkeiten für Tests und Beiträge.

<a id="how-it-works"></a>
## Funktionsweise

1. **Aufgabe versuchen.** Bewahrt Ergebnis und Schritte des Agenten auf.
2. **Ergebnis prüfen.** Prüft das Artefakt selbst statt der Abschlussmeldung zu vertrauen.
3. **Zurückblicken.** Verknüpft das Problem mit Werkzeugaufrufen, fehlendem Kontext, Anweisungen oder Umgebungsentscheidungen.
4. **Verbesserung testen.** Lasst den Agenten eine Änderung vorschlagen und relevante Prüfungen wiederholen.
5. **Bewährtes behalten.** Bewahrt gestützte Verbesserungen und eine wiederherstellbare Version.

<p align="center">
  <a href="https://harneloop.kaelux.dev/media/harneloop-how-it-works.mp4">
    <img src="https://harneloop.kaelux.dev/media/harneloop-video-poster.png" alt="So funktioniert Harneloop: vom Ziel zum wiederverwendbaren Harness" width="900" />
  </a>
</p>

<p align="center"><a href="https://harneloop.kaelux.dev/media/harneloop-how-it-works.mp4"><img src="../../assets/readme-play.svg" alt="" width="18" height="18" align="absmiddle" /> Harneloop in Aktion ansehen - 3:40</a></p>

Jede Aufgabenfamilie hat eine **Harness-Einheit**: einen portablen Arbeitsbereich für Ziel, Werkzeuge, Versuche, Evidenz und Verbesserungen. Ihr könnt pausieren und später fortsetzen, ohne die Untersuchung neu zu beginnen.

<a id="try-harneloop"></a>
## Harneloop ausprobieren

[Von PyPI installieren](https://pypi.org/project/harneloop/), in einer isolierten Werkzeugumgebung:

```bash
uv tool install harneloop
harneloop setup
```

Oder nutzt `python -m pip install harneloop` in eurer Python-Umgebung. Anforderungen und Quellcodeinstallation stehen unter [Installieren und starten](#install-and-start).

Gebt anschließend einem geeigneten Agenten den Repository-Link und die zu verbessernde Aufgabe. Der [Agenten-Schnellstart](#agent-quick-start) enthält einen fertigen Prompt.

**Status:** Öffentliche Alpha. Die Kernschleife funktioniert; breitere Aufgabenvalidierung und Beiträge sind willkommen. [Problem melden oder Anwendungsfall teilen](https://github.com/Ker102/Harneloop/issues).

<a id="evidence-from-a-real-case-study"></a>
## Evidenz aus einer realen Fallstudie

Harneloop wurde zur Entwicklung der angepassten ViperMesh-Harness-Einheit für Blender-Raumverständnis und Szenenbau eingesetzt. Der Vergleich hielt das ausführende Modell bei **GPT-5.5 High** konstant und testete den entwickelten ViperMesh-Harness gegen die **Anthropic x Blender MCP server baseline**, sodass der Harness die hauptsächlich geänderte Systemschicht war.

- ViperMesh war bei **6 von 7** vergleichbaren Live-Aufgaben schneller, mit einer **mittleren Beschleunigung von 2.534x**.
- Die vorläufige neutrale visuelle LLM-Bewertung stieg über sieben Live-Rendering-Paare um **8.19 Punkte**.
- Der gesamte Tokenverbrauch des ausführenden Agenten war über sieben vergleichbare Benchmarks **90.91% niedriger**, insgesamt etwa **175K gegenüber 1.9M Tokens**.

Harneloop erzeugte die Szenen nicht selbst. Es strukturierte die Evidenz- und Artefaktschleife, die Schwächen aufdeckte, Werkzeug- und Harness-Entwicklung leitete und die Benchmark-Verbesserung prüfte. Methodik, Grenzen und vollständige Ergebnisse stehen in der [ViperMesh-Fallstudie](https://kristoferjussmann.me/case-studies/vipermesh).

Diese Ergebnisse liefern direkte empirische Evidenz für Harneloops Prozess in einer realen, artefaktreichen Agentenumgebung: Das ausführende Modell blieb gleich, während der weiterentwickelte Harness messbare Gewinne bei Geschwindigkeit, visueller Leistung und Tokeneffizienz erzielte.

<a id="demonstration-vipermesh-mcp"></a>
### Demonstration: ViperMesh MCP

[Harneloop-Demonstration mit ViperMesh MCP ansehen](https://www.youtube.com/watch?v=bs74QJ6UD5E&t=2s).

Blender-Szenenbau ist ein konkreter Fall für Ergebnisprüfung und Verbesserung der Agentenwerkzeuge und -anweisungen. Lest die [Harneloop-Fallstudie](https://kristoferjussmann.me/case-studies/harneloop/#harneloop-demo) zum Framework und die [ViperMesh-Benchmarkstudie](https://kristoferjussmann.me/case-studies/vipermesh/) für Messwerte. Der [öffentliche Blender-Connector](https://github.com/Ker102/vipermesh-blender) ist getrennt vom vollständigen Studio und dem getesteten Harness verfügbar.

<a id="start-here"></a>
## Hier beginnen

- **Harneloop über einen Agenten nutzen:** [Agenten-Schnellstart](#agent-quick-start)
- **Selbst installieren:** [Installieren und starten](#install-and-start)
- **Harness-Einheiten verstehen:** [Was ist eine Harness-Einheit?](#what-is-a-harness-unit)
- **Die Schleife verstehen:** [Der Lebenszyklus, einfach erklärt](#the-lifecycle-made-simple)
- **Gemessener Nachweis:** [ViperMesh-Fallstudie](https://kristoferjussmann.me/case-studies/vipermesh)
- **Eine reale Umgebung verbinden:** [Umgebung einrichten](#environment-setup)
- **Vorgaben ändern:** [Konfiguration](#configuration)
- **Technische Architektur:** [Kernlebenszyklus](docs/architecture/core-lifecycle.md), [Laufzeitschichten](docs/architecture/runtime-layers.md) und [Nebenläufigkeit](docs/architecture/concurrency.md)
- **Vollständige Agentenanweisungen:** [Agenten-Einstieg](docs/agent-onboarding.md)
- **Visueller Prozess:** [Funktionsweise](#how-it-works), [editierbares Kompaktdiagramm](docs/framework-process-compact.md) und [detailliertes Framework-Diagramm](docs/framework-process.md)

<a id="why-harneloop-exists"></a>
## Warum Harneloop existiert

Modelle wiederholen häufig dieselben Fehler, weil hilfreiche Erkenntnisse aus einem Versuch nie zum getesteten Teil ihrer Arbeitsumgebung werden. Ein längerer Prompt oder ein Evaluationsscore löst nicht das ganze Problem.

Das Modell ist nur ein Teil der Agentenleistung. Der Harness bestimmt sichtbaren Kontext, verfügbare Werkzeuge, Umgebungsinteraktion, Erinnerung, Ergebnisprüfung und ob Fehler zu dauerhaften Verbesserungen werden. Bei vielen aufgabenspezifischen Problemen ist er daher der stärkste Verbesserungshebel: deutliche Gewinne ohne Modellneutraining, wobei jede Änderung prüfbar, testbar, reversibel und portabel bleibt.

Harneloop strukturiert diese Arbeit und macht sie effizient. Statt einmalige Prompt-Änderungen anzuhäufen, kann ein Agent mehrere unabhängige Einheiten entwickeln, Änderungen in realen Versuchen testen, Evidenz und Historie bewahren und jeden erfolgreichen Harness als zusammenhängendes Paket fortführen oder exportieren.

Harneloop gibt dem operierenden Agenten eine kontrollierte Verbesserungsschleife:

- an der realen Aufgabe statt nur einem synthetischen Benchmark arbeiten;
- Renderings, Screenshots, Dateien, Traces, Logs, strukturierten Zustand oder andere Artefakte erfassen;
- Artefakte visuell, strukturell oder hinsichtlich ihres Verhaltens prüfen;
- schwache Ergebnisse auf Anweisungen, Werkzeuge, Kontext, Retrieval, Umgebung oder Modellgrenzen zurückführen;
- Verbesserungen als isolierte Kandidatenpatches entwickeln;
- Kandidaten gegen neue Versuche und Regressionsfälle testen;
- nur Änderungen mit gültiger Evidenz promovieren;
- wiederherstellbare Versionen bewahren und den resultierenden Harness zur Wiederverwendung paketieren.

Der Agent darf im Harness-Arbeitsbereich frei schlussfolgern und experimentieren. Harneloop kontrolliert integritätssensible Grenzen: Datensätze, geschützten Zustand, Evidenz, Promotion, Snapshots, Rollback und Paketierung.

<details>
<summary>Forschungshintergrund: Warum den Harness vor den Gewichten verbessern?</summary>

<a id="why-improve-the-harness-before-the-weights"></a>
### Warum den Harness vor den Gewichten verbessern?

Forschung zu Agentenschnittstellen, Retrieval, Werkzeugen und iterativem Feedback zeigt, dass Änderungen am System um ein Modell dessen Aufgabenleistung deutlich verbessern können, ohne Gewichte zu verändern. Sind Kontext, Retrieval, Werkzeuge, Feedback oder Umgebungsinteraktion die Hauptengpässe, können Harness-Methoden Fine-Tuning teils deutlich übertreffen und allgemeine Modellfähigkeiten bewahren. Harneloop entstand aus praktischen Problemen beim Harness-Bau; folgende Arbeiten stützen unabhängig seine Harness-first-Ausrichtung:

- [Self-Harness](https://arxiv.org/abs/2606.09498) zeigte, dass Agenten Schwächen aus Ausführungsspuren gewinnen, Harness-Änderungen vorschlagen, mit Regressionstests validieren und zurückgehaltene Erfolgsraten in drei Modellfamilien verbessern konnten.
- [SWE-agent](https://arxiv.org/abs/2405.15793) zeigte, dass eine zweckentwickelte Agenten-Computer-Schnittstelle Repository-Navigation, Codebearbeitung und Testausführung durch Sprachmodelle deutlich verbesserte.
- [Reflexion](https://arxiv.org/abs/2303.11366) verbesserte Agenten durch Versuch und Irrtum, sprachliches Feedback und episodisches Gedächtnis statt Gewichtsänderungen.
- [Self-Refine](https://arxiv.org/abs/2303.17651) berichtete über sieben evaluierte Aufgaben eine mittlere absolute Verbesserung von etwa 20 Prozentpunkten durch iteratives Feedback und Verfeinerung ohne zusätzliches Training.
- [Fine-Tuning or Retrieval?](https://aclanthology.org/2024.emnlp-main.15/) fand, dass RAG unüberwachtes Fine-Tuning bei den untersuchten Wissensinjektionsaufgaben für bestehendes und neues Wissen konsistent übertraf.
- [Does Fine-Tuning LLMs on New Knowledge Encourage Hallucinations?](https://arxiv.org/abs/2405.05904) fand Schwierigkeiten beim Erwerb neuer Fakten durch überwachtes Fine-Tuning und eine steigende Halluzinationsneigung beim Lernen dieses Wissens.

Zusammen mit ViperMesh stützt das eine praktische Strategie: **zuerst den Harness optimieren, Ergebnisse messen und Modellgewichte erst ändern, wenn Evidenz seine sinnvolle Grenze zeigt.** Harness-Änderungen sind schneller zu prüfen, zurückzunehmen, wiederzuverwenden und zu validieren und können bei passenden Aufgaben größere Gewinne als Gewichtsänderungen erzielen, ohne das Basismodell dauerhaft zu ändern.

Das belegt nicht, dass ein Harness jede mögliche Fine-Tuning-Methode immer übertrifft. Fine-Tuning kann für Verhalten, Stil, Latenz, spezialisierte Repräsentationen oder zur Inferenzzeit schwer bereitstellbare Fähigkeiten wertvoll bleiben. Ein starker Harness und ein passendes Fine-Tuning können sich ergänzen.

</details>

<a id="what-is-a-harness-unit"></a>
## Was ist eine Harness-Einheit?

Eine **Harness-Einheit** ist ein portabler Arbeitsbereich zur Verbesserung einer Aufgabenfamilie. Jede entwickelt sich unabhängig und bewahrt Zieldefinition, Umgebungsübersicht, Harness-Material, Experimente, Evidenz, Regressionsfälle und promovierte Versionen.

Eine neue Einheit beginnt mit dieser Struktur:

```text
my-harness-unit/
  unit.yaml                 identity and current version
  UNIT_AGENT.md             instructions for agents entering the unit
  operational-map.md        current understanding of tools, artifacts, and workflow
  target/                   task goal and suggested first tests
  environment/              contract for commands, MCP tools, apps, and artifact paths
  agent-facing/             promoted instructions and context
  tools/                    unit-specific helper tools
  observers/                ways to inspect outputs
  validators/               deterministic or agent-driven checks
  regression-cases/         failures that future candidates should not repeat
  candidates/               isolated proposed harness changes
  runtime/                  local runs and captured artifacts
  versions/                 restorable promoted snapshots
  provenance/               human-readable change history
```

Das ist keine einschränkende Vorlage. Agenten dürfen Forschung, Skripte, Retrieval-Daten, Infrastrukturdeklarationen, Gedächtnis, eigene Beobachter oder neue Verzeichnisse ergänzen. Das Framework schützt nur die Dateien und Lebenszyklusregeln für Verständlichkeit und Wiederherstellbarkeit.

<a id="portable-unit-versus-local-working-data"></a>
### Portable Einheit und lokale Arbeitsdaten

Wiederverwendbares Harness-Material gehört in die portable Einheit. Rohe Traces, temporäre Experimente, Caches, Geheimnisse, unpromovierte Kandidaten und sämtliche historischen Renderings nicht.

Das standardmäßige `thin`-Paket enthält promoviertes Wissen und Verträge zum Wiederaufbau oder zur Integration des Harness. Laufzeitevidenz bleibt lokal, sofern ein späteres Paketprofil sie nicht ausdrücklich einschließt.

<a id="the-lifecycle-made-simple"></a>
## Der Lebenszyklus, einfach erklärt

1. **Ziel beschreiben.** Der Nutzer erklärt, worin der Agent besser werden soll.
2. **Umgebung erfassen.** Der operierende Agent erkundet Aufgabenausführung und hilfreiche Evidenzquellen.
3. **Annahmen abgleichen.** Wichtiger Kontext wird vor dem ersten echten Lauf bestätigt, delegiert oder klar als abgeleitet markiert.
4. **Baseline ausführen.** Der Agent versucht die Aufgabe vor einer Harness-Änderung.
5. **Prüfen und abschließen.** Artefakte bewerten und ausdrücklich akzeptieren, ändern, wiederholen, Eingaben anfordern oder stoppen.
6. **Kandidaten bei Bedarf erstellen oder erweitern.** Verwandte Änderungen sammeln sich in isolierten Bündeln; unabhängige Probleme können parallele Kandidaten haben.
7. **Risikoproportional validieren.** Strukturelle, gezielte, repräsentative oder vollständige Prüfungen mit Evidenz verwenden.
8. **Promovieren, überarbeiten, warten oder stoppen.** Gestützte Verbesserungen werden zur Version, schwache Kandidaten überarbeitet oder abgelehnt.
9. **Exportieren oder paketieren.** Der promovierte Harness passt zu Coding-Agenten, Anwendungsagenten oder anderen kompatiblen Umgebungen.

Abgeschlossene Ausführungen sind unveränderlich. Kandidatenevidenz wird beim Anhängen und erneut bei Promotion geprüft; gelöschte Läufe, fehlende Artefakte oder Evidenzdateien können keinen Release stützen.

Kandidaten sind keine Hüllen pro Commit. Ein Konfigurations- oder Werkzeugkandidat kann verwandte Änderungen sammeln und gezielt smoke-getestet werden; ein verhaltensändernder Harness-Kandidat kann reale Artefaktversuche und Regressionen benötigen. Ziel-Harness, Evaluation und Infrastruktur können unabhängig voranschreiten. Nach einer Promotion müssen parallele Kandidaten auf der alten Basis einen Rebase durchführen und frische Evidenz liefern.

Das Video oben erklärt die Schleife. Das [Kompaktdokument](docs/framework-process-compact.md) enthält ein editierbares Mermaid-Diagramm. Das [Detaildiagramm](docs/framework-process.md) deckt Fähigkeitslücken, menschliche Eingaben, Warten, Stoppen und die vollständige artefaktbewusste Schleife ab.

<a id="what-makes-it-different"></a>
## Was macht es anders?

<a id="artifact-aware"></a>
### <img src="../../assets/readme-observe.svg" alt="" width="18" height="18" align="absmiddle" /> Artefaktbewusst

Harneloop behandelt das Erzeugte als Evidenz. Der Agent kann Bilder, Szenen, UIs, Dokumente, generierte Repositorys, Laufzeitspuren, Datenbankzustände oder andere hilfreiche Ergebnisse prüfen statt seinem Textbericht zu vertrauen.

<a id="harness-building-not-only-scoring"></a>
### <img src="../../assets/readme-improve.svg" alt="" width="18" height="18" align="absmiddle" /> Harness-Bau, nicht nur Bewertung

Es geht nicht nur darum, Agentenfehler zu melden. Der operierende Agent diagnostiziert sie und entwickelt konkrete Harness-Änderungen mit Prompts, Prinzipien, Beispielen, Retrieval, Werkzeugen, Beobachtern, Validatoren, Regressionsfällen oder Umgebungsautomatisierung.

<a id="evidence-gated-self-improvement"></a>
### <img src="../../assets/readme-verify.svg" alt="" width="18" height="18" align="absmiddle" /> Evidenzgebundene Selbstverbesserung

Der aktive Agent darf den promovierten Harness nicht frei überschreiben. Er erstellt und testet einen Kandidaten, hängt Evidenz an und promoviert über das Framework. Jede promovierte Version ist prüfbar und wiederherstellbar.

<a id="environment-agnostic"></a>
### Umgebungsunabhängig

Der Kern hängt nicht von Blender, SVGs, Python-Agenten oder bestimmten Modellanbietern ab. Eine Einheit kann Terminalbefehle, MCP-Server, Browserautomatisierung, Desktop-Apps, APIs, manuelle Schritte oder eigene Werkzeugschnittstellen nutzen.

<a id="reasoning-remains-open-ended"></a>
### Schlussfolgern bleibt offen

Harneloop strukturiert den Lebenszyklus, ohne den operierenden Agenten in ein festes Skript zu verwandeln. Tests, Artefakte, Evaluation, Werkzeuge und Endpunkt wählt weiterhin der Agent passend zur Aufgabe.

<a id="agent-quick-start"></a>
## Agenten-Schnellstart

Harneloop ist hauptsächlich für die Nutzung im Gespräch mit einem Agenten mit Dateisystem- und Terminalzugriff gedacht.

Gebt dem Agenten das Repository und einen Prompt wie diesen:

```text
Read this repository's README.md and docs/agent-onboarding.md.
Use Harneloop to create a harness unit that improves an agent at: [describe the task].

Inspect my existing environment before deciding how to test it. Ask only for context
that can materially change the work, and do not silently treat assumptions as confirmed.
Run a baseline, inspect its artifacts, and conclude the attempt before deciding whether
a candidate is needed. Do not promote a candidate without evidence.
```

Der Agent sollte dann:

1. Harneloop bei Bedarf installieren und `harneloop doctor` ausführen.
2. `harneloop onboard --format json` oder [den Einstiegsguide](docs/agent-onboarding.md) lesen.
3. Eine vorläufige Einheit erstellen oder fortsetzen und die reale Umgebung prüfen.
4. Bestätigten, delegierten, abgeleiteten und unbekannten Kontext am adaptiven Erfassungsprüfpunkt abgleichen.
5. `operational-map.md` mit dem aktuellen Verständnis aktualisieren.
6. Eine Baseline durchführen und die resultierenden Artefakte prüfen.
7. Den Versuch abschließen, bevor der aktuelle Harness akzeptiert oder Verbesserungen vorgeschlagen werden.

<a id="instructions-for-agents-reading-this-repository"></a>
### Anweisungen für Agenten, die dieses Repository lesen

Wenn ihr der operierende Agent seid:

- Nehmt nicht an, dass jede Aufgabe einen Testbefehl hat.
- Nehmt nicht an, dass Harneloop Endpunkte, Werkzeuge, Screenshots oder Artefaktpfade für euch entdeckt.
- Führt beim Betreten einer Einheit oder nach Kontextverlust `harneloop brief <unit>` aus und lest `AGENTS.md`, `UNIT_AGENT.md` und `operational-map.md`.
- Wendet den Einheitenbrief nur auf die Arbeit an dieser Einheit an; unverbundene Projektarbeit bleibt außerhalb.
- Nutzt `harneloop intake status`, um nur offene Fragen mit wesentlichem Einfluss auf die Arbeit aufzuzeigen.
- Nutzt `harneloop candidate list <unit>`, um alle offenen Arbeiten wiederzufinden; eine Einheit kann mehrere aktive Kandidaten haben.
- Bündelt verwandte Änderungen in kohärenten Kandidaten und skaliert Prüfungen nach Auswirkungen statt nach jedem Einrichtungsschritt den Vollbenchmark auszuführen.
- Trennt Evaluator- und Ziel-Harness-Änderungen möglichst, damit Evidenz vertrauenswürdig bleibt.
- Prüft die reale Umgebung und bildet sie in `target/` und `environment/` ab.
- Bevorzugt reale Artefaktprüfung, wenn deterministische Checks Qualität nicht feststellen können.
- Trennt eigene Fähigkeiten von den Werkzeugen, die für den Zielagenten entworfen werden.
- Optimiert das beste verifizierte Ergebnis statt alles neu zu bauen: recherchiert und nutzt geeignete Werkzeuge, Skills, Bibliotheken, Beispiele und Vorarbeiten; dokumentiert Provenienz und beachtet Lizenz-, Sicherheits-, Kosten- und Berechtigungsgrenzen.
- Legt vorgeschlagene Harness-Änderungen in einen Kandidatenarbeitsbereich.
- Nutzt Harneloop-Befehle für Läufe, Artefakte, Evidenz, Promotion, Rollback, Warten, Stoppen und Fortsetzen.
- Fragt vor Zugangsdaten, kostenpflichtigen Diensten, externem Zugriff, sicherheitsrelevanten Werkzeugen oder teurer Infrastruktur.
- Aktualisiert die Arbeitsübersicht bei geänderten Annahmen, Artefaktpfaden, Werkzeugen oder Automatisierung.
- Stoppt niemals allein nach Laufabschluss: prüft Artefakte und erfasst eine ausdrückliche Entscheidung mit `harneloop attempt conclude`.

Maschinenlesbarer Einstieg ist verfügbar mit:

```bash
harneloop onboard --format json
```

<a id="install-and-start"></a>
## Installieren und starten

Harneloop ist [auf PyPI veröffentlicht](https://pypi.org/project/harneloop/). Installiert es isoliert über [uv](https://docs.astral.sh/uv/getting-started/installation/) oder nutzt `python -m pip install harneloop` in der Python-Umgebung. Der Befehl `harneloop` ist für Windows, macOS und Linux ausgelegt.

```bash
uv tool install harneloop
harneloop doctor
harneloop setup
```

Für einen unveröffentlichten Quellcode-Build nutzt `uv tool install git+https://github.com/Ker102/Harneloop.git`.

Meldet `uv`, dass sein Werkzeugverzeichnis nicht im `PATH` liegt, führt `uv tool update-shell` aus und öffnet ein neues Terminal. Mitwirkende können den aktiven Clone mit `uv tool install --editable .` installieren; siehe [Entwicklungseinrichtung](docs/development.md).

`harneloop setup` öffnet die geführte CLI für Menschen. `harneloop` ohne Unterbefehl öffnet im Terminal das umfassendere interaktive Menü. Agenten können explizite nichtinteraktive Befehle direkt nutzen.

Hilfreiche erste Befehle:

```bash
harneloop onboard
harneloop template list
harneloop units list
harneloop settings show
```

Mit `harneloop setup` oder `harneloop init-unit` erstellte Einheiten werden automatisch registriert. Bestehende lassen sich einmal hinzufügen mit:

```bash
harneloop units register /path/to/my-unit
```

Nach der Registrierung nutzt ihr ID oder Namen aus jedem Verzeichnis statt eines relativen Pfads:

```bash
harneloop units list
harneloop status my-unit --format markdown
harneloop environment status my-unit
```

<a id="what-the-agent-asks-you"></a>
## Was der Agent euch fragt

Der Einstieg neuer Einheiten ist bewusst kurz. Der Agent sollte fünf Kontextangaben sammeln:

1. Worin soll dieser Harness den Agenten verbessern?
2. Wo wird der Harness eingesetzt?
3. Definiert ihr Erfolg, soll der Agent ihn vorschlagen oder entscheidet ihr nach der Baseline?
4. Priorisiert Validierung Qualität, visuelle Evidenz, Ausgewogenheit oder Ressourceneffizienz?
5. Existiert die Testumgebung ganz, teilweise oder muss sie gebaut werden?

Ihr müsst ideale Tests oder Artefakte nicht vorab kennen. Der Agent sollte sie nach Prüfung von Aufgabe und Umgebung passend vorschlagen und nur bei Relevanz nach Grenzen, geschützten Bereichen, Kostenlimits oder menschlicher Prüfung fragen.

<a id="environment-setup"></a>
## Umgebung einrichten

Harneloop dokumentiert die Umgebungszuordnung; der operierende Agent erstellt sie.

Die CLI kann nicht magisch wissen, welches MCP-Werkzeug eine App steuert, wo Renderings liegen, wie Browserabläufe zurückgesetzt werden oder welcher Datenbankzustand Erfolg belegt. Der Agent muss den echten Arbeitsbereich prüfen und diese Details der Einheit zuordnen.

Drei Einrichtungsmodi werden unterstützt:

| Modus | Einsatzfall | Agentenverhalten |
|---|---|---|
| `existing` | Umgebung funktioniert bereits | Verbinden und dokumentieren, nicht grundlos neu bauen |
| `assisted` | Teile existieren | Minimale fehlende Einrichtung für eine Baseline ergänzen |
| `managed` | Umgebung muss entstehen | Explizit bauen und Infrastrukturänderungen dokumentieren |

Eine Umgebung kann befehls-, MCP-gesteuert, manuell oder vollständig individuell sein. Ein Blender-Harness kann etwa einen bestehenden MCP-Server ohne einzelnen Laufbefehl nutzen. Der Agent ruft Werkzeuge auf, rendert, erfasst Screenshots und strukturierten Szenenzustand und hängt sie an eine Harneloop-Ausführung an.

Detaillierte Beispiele stehen unter [Umgebungseinstieg](docs/environment-onboarding.md).

<a id="configuration"></a>
## Konfiguration

Die meisten Nutzer sollten mit Vorgaben beginnen. Die erste hilfreiche Konfiguration liegt meist in der Einheit, nicht in globalen Einstellungen.

<a id="harness-unit-configuration"></a>
### Harness-Einheitenkonfiguration

| Datei oder Bereich | Wann ändern |
|---|---|
| `operational-map.md` | Werkzeuge, Artefaktorte, Annahmen, Grenzen oder Workflow ändern sich |
| `target/brief.yaml` | Aufgabenfamilie, Erfolgsdefinition, erwartete Artefakte oder bekannte Risiken ändern sich |
| `environment/contract.yaml` | Befehle, MCP-Werkzeuge, Einrichtungs- oder Interaktionsmodus oder Ausgabepfade ändern sich |
| `agent-facing/` | Getesteter Kandidat promoviert neue Anweisungen oder wiederverwendbaren Kontext |
| `observers/` und `validators/` | Bessere Artefaktprüfung oder deterministische Checks erforderlich |
| `regression-cases/` | Entdeckter Fehler soll künftig getestet werden |
| `tools/` und `infrastructure/` | Bessere Leistung erfordert einheitenspezifische Fähigkeiten oder Dienste |

Bearbeitet frameworkeigene `.evolve/`, `versions/`, `provenance/`, `runtime/` oder Kandidatenmetadaten nicht manuell. Nutzt CLI-Lebenszyklusbefehle.

<a id="global-preferences"></a>
### Globale Einstellungen

Zeigt Einstellungen mit `harneloop settings show` an und ändert eine mit:

```bash
harneloop settings set validation.prefer_visual_artifacts true
harneloop settings set agent_behavior.autonomy_level balanced
harneloop settings set runtime.token_efficiency_mode false
```

Wichtige Einstellungsgruppen:

- `agent_behavior`: Autonomie, Risikobestätigung und Promotionsstrenge;
- `validation`: agentenentschiedene Validierung, visuelle Artefaktpräferenz und Ressourcenmodus;
- `export`: Standard-Zieladapter und Paketprofil;
- `runtime`: Telemetriedetail, Tokeneffizienzmodus und lokale Einheitenregistrierung.

In der Alpha sind Einstellungen dauerhafte Vorgaben und Hinweise für CLI und operierenden Agenten. Noch setzt nicht jeder Engine-Befehl jede Einstellung automatisch durch. Evidenzpflichtige Promotion wird erzwungen, außer beim ausdrücklichen Entwicklungs-Override.

<a id="example-use-cases"></a>
## Beispielanwendungen

- Raumverständnis und Szenenbau eines Blender- oder CAD-Agenten verbessern.
- SVG-, Bild-, Folien-, Dokument- oder UI-Erzeugung durch gerenderte Artefaktprüfung verbessern.
- Einen Coding-Harness für ein Repository mit wiederkehrenden Implementierungs- oder Debuggingfehlern bauen.
- Browserautomatisierung mit Screenshots, DOM-Zustand, Traces und Ergebnissen verbessern.
- Werkzeugauswahl und Wiederherstellungsverhalten eines MCP-Agenten verbessern.
- Retrieval, Beispiele, Validatoren und Kontext für Forschungs- oder Datenverarbeitungsabläufe entwickeln.
- Einen wiederverwendbaren internen Harness bauen und für Codex, Cursor oder einen eigenen Anwendungsagenten exportieren.

Harneloop ist am nützlichsten bei wiederholten Aufgaben, prüfbaren Ausgaben und Fehlern, die zu dauerhaften Verbesserungen werden können. Für einmalige Aufgaben ohne wiederverwendetes Lernen ist es unnötig.

<a id="core-cli-lifecycle"></a>
## Kernlebenszyklus der CLI

Die expliziten Befehle richten sich an Agenten, Automatisierung und technische Nutzer:

```bash
harneloop init-unit ./my-unit --id my-unit --name "My Harness Unit" --template artifact-review
harneloop target set my-unit --task "..." --success "..."
harneloop environment connect my-unit --name "..." --mode existing --description "..."
harneloop attempt plan my-unit --goal "..." --method "..."
harneloop run start my-unit --task "Baseline attempt"
harneloop artifact add my-unit run-0001 ./output.png --kind image
harneloop run finish my-unit run-0001 --status succeeded --summary "Baseline captured"
harneloop candidate create my-unit --summary "Improve artifact construction" --plane target_harness --validation-tier representative
harneloop run start my-unit --task "Test candidate improvement" --candidate-id cand-0001
harneloop artifact add my-unit run-0002 ./improved-output.png --kind image
harneloop run finish my-unit run-0002 --status succeeded --summary "Candidate result captured"
harneloop candidate evidence add my-unit cand-0001 --kind artifact_review --summary "..." --run-id run-0002 --artifact-id artifact-0001 --validation-tier representative
harneloop candidate stage my-unit cand-0001 ready
harneloop promote my-unit cand-0001 --version 0.1.0
harneloop export my-unit --adapter codex
harneloop package my-unit --output ./my-unit-0.1.0.tar.gz
```

Diese Folge ist beispielhaft, kein fester Ablauf. Werkzeugagenten können zwischen `run start` und `run finish` viele Aktionen ausführen, mehrere Artefakte erfassen, Versuche erstellen oder externe Ergebnisse abwarten.

<a id="safety-and-integrity"></a>
## Sicherheit und Integrität

- YAML- und JSON-Steuerdateien werden atomar geschrieben.
- Nebenläufige ID-Vergabe und Lese-Änderungs-Schreibvorgänge nutzen Harness-lokale Sperren.
- Abgeschlossene Läufe können nicht geändert oder erneut beendet werden.
- Kandidaten-Overlays dürfen geschützten Framework-Zustand nicht ändern.
- Evidenzreferenzen müssen beim Anhängen und bei Promotion existieren.
- Kandidatenevidenz muss zu aktueller Basisversion und deklarierter Validierungsstufe passen.
- Parallele Kandidaten bleiben nach anderer Promotion erhalten, benötigen aber Rebase und frische Evidenz vor eigener Promotion.
- Promovierte Versionen werden als wiederherstellbare Snapshots gespeichert.
- Rollback ist eine protokollierte Framework-Aktion.
- Thin-Pakete schließen Laufzeitdaten, Kandidaten, Caches und gängige Geheimnisdateien aus.

<a id="documentation"></a>
## Dokumentation

- [Wie Harneloop funktioniert](docs/framework-process.md)
- [Agenten-Einstieg](docs/agent-onboarding.md)
- [Umgebungseinstieg](docs/environment-onboarding.md)
- [Kernlebenszyklus](docs/architecture/core-lifecycle.md)
- [Laufzeitschichten und künftige Rust-Grenze](docs/architecture/runtime-layers.md)
- [Nebenläufigkeit und Dateisicherheit](docs/architecture/concurrency.md)
- [Produktprinzipien](docs/product-principles.md)
- [Lokale Demo](docs/demo-first-test.md)
- [Entwicklungsnotizen](docs/development.md)

<a id="contributing"></a>
## Mitwirken

Beiträge, Issues und unabhängige Harness-Fallstudien sind willkommen. Besonders hilfreich sind:

- Harneloop jenseits der bisherigen Aufgabenfamilie testen;
- reproduzierbare Lebenszyklus-, Portabilitäts- oder Einstiegsfehler melden;
- Zielagentenadapter, Validatoren, Paketierung und plattformübergreifendes Verhalten verbessern;
- gezielte Dokumentation, Beispiele oder Regressionstests beitragen.

Lest vor größeren Änderungen [CONTRIBUTING.md](CONTRIBUTING.md). Architekturarbeit beginnt mit einem Issue zu Umfang und Kompatibilität. Sicherheitsprobleme folgen [SECURITY.md](SECURITY.md), nicht einem öffentlichen Issue.

<a id="development"></a>
## Entwicklung

Führt die Tests aus dem Repository aus:

```bash
python -m unittest discover -s tests
```

Das Projekt nutzt derzeit Python 3.11 oder neuer. Eine künftige Rust-Laufzeit kann nach Produktstabilisierung stärkere geschützte Lebenszyklus-, Paketierungs-, Dateiüberwachungs- oder Desktop-Verteilungsaufgaben übernehmen.

Harneloop ist die gewählte Produktidentität für Alpha und öffentlichen Start. Paket, CLI, Harness-Metadaten, Dokumentation und Repository verwenden denselben Namen.

<a id="license"></a>
## Lizenz

Harneloop ist unter der [Apache License 2.0](../../../LICENSE) verfügbar.
