<a id="agent-onboarding"></a>
# Agenten-Einstieg

Ein Agent mit nur Repository und Nutzeraufgabe sollte Harneloop verstehen können. Der erste Schritt ist nicht, einen Validator zu schreiben oder einen Testbefehl anzunehmen, sondern genügend Kontext für einen Baseline-Versuch zu sammeln.

Für eine geführte Einrichtung für Menschen:

```powershell
harneloop setup
```

Für eine agentenlesbare Checkliste:

```powershell
harneloop onboard
```

oder aus einem Clone vor dauerhafter Werkzeuginstallation:

```powershell
uv run harneloop onboard
```

Für maschinenlesbare Ausgabe:

```powershell
harneloop onboard --format json
```

Für eine Einheit aus einer älteren Version führt einmal `harneloop upgrade-unit <unit>` aus. Es ergänzt fehlende Protokolldateien, ohne vorhandenes Harness-Material zu ersetzen.

<a id="minimal-user-questions"></a>
## Minimale Nutzerfragen

Nutzt sie als Kontextfelder, nicht als Pflichtfragebogen. Der Agent kann zuerst die vorläufige Einheit erstellen und den Arbeitsbereich prüfen, dann nur relevante Restfragen stellen:

1. Worin soll dieser Harness den Agenten verbessern?
2. Wo wird er genutzt, etwa Coding-Workflow, Anwendungsagent, Forschung oder interne Automatisierung?
3. Wie werden Erfolgskriterien behandelt?
4. Wie werden Ergebnisse validiert?
5. Existiert die Testumgebung ganz, teilweise, muss sie gebaut werden oder ist das noch unklar?

Macht den Einstieg nicht zum langen Formular. Kriterien und Artefakte sind geführte Optionen, kein erforderliches Nutzerfachwissen. Führt nach Prüfung `harneloop intake status <unit>` aus und klassifiziert wichtigen Kontext als bestätigt, delegiert, abgeleitet, unbekannt oder nicht anwendbar. Macht Ableitungen nicht still zu bestätigten Fakten.

Klärt vor dem ersten echten Lauf relevante Felder und dokumentiert ausdrückliche Bestätigung oder Delegation mit `harneloop intake acknowledge`. Können fehlende Referenz, Zielprojekt, Zugangsdaten oder Beurteilung den Test wesentlich ändern, fragt direkt danach oder wartet, statt die Lücke erst nach Einrichtung zu nennen.

Harneloop dokumentiert die Umgebung, entdeckt aber nicht selbst Testendpunkte, MCP-Werkzeuge, Befehle, Screenshot-Orte, Renderings oder Artefaktpfade. Der Einstiegsagent muss Projekt und Umgebung prüfen, Artefakterzeugung ermitteln und die Zuordnung festhalten.

Jede neue Einheit hat `operational-map.md`. Nutzt es als aktuelle Orientierung: Verbesserungsziel, Systeme und Werkzeuge, hilfreiche Artefakte und Evidenz, übliche Ausführung und Resets, Grenzen, Schwachstellen, offene Fragen, zu prüfende Annahmen und frühere Lauf- oder Evidenzorte. Aktualisiert es bei geändertem Workflow, Evidenzbedarf, Umgebungsannahmen oder Automatisierungsstrategie.

Die Übersicht ist Kontext und Navigation, kein starrer Ablauf. Der Agent muss weiterhin von der Aufgabe ausgehen, Evidenz prüfen und passende Tests oder Evaluation für den aktuellen Versuch wählen.

<a id="capability-gaps"></a>
## Fähigkeitslücken

Nehmt nicht überall Codex-Fähigkeiten an. Angepasste Hermes-, OpenClaw-, App-Agenten oder eingeschränkte Worker können Terminal-, Datei-, Browserzugriff, Paketmanager, MCP-Server, visuelle Prüfung, Datenbankzugriff oder andere nötige Fähigkeiten vermissen.

Trennt zwei Schichten:

- Fähigkeiten des operierenden Agenten: tatsächlich beim Einheitenbau nutzbare Fähigkeiten.
- Einheiten- oder Zielagentenwerkzeuge: in die Einheit eingebaute oder über den Umgebungsvertrag bereitgestellte Werkzeuge.

Fehlt eine hilfreiche Fähigkeit, dokumentiert in `operational-map.md`: was, warum, hilfreiches Werkzeug oder Abhängigkeit, Risiko-, Kosten-, Authentifizierungs- oder Sicherheitsänderungen und Alternative bei Ablehnung.

Lokale Fähigkeiten mit geringem Risiko dürfen bei passender Umgebung installiert, aktiviert oder gebaut werden. Größere Abhängigkeiten, Zugangsdaten, bezahlte APIs, Nutzerkonten, externer Zugriff, Netzerweiterungen und Sicherheitsänderungen sind vorher vorzuschlagen.

Begründet Erweiterungen mit beobachteten Engpässen, Fehlversuchen, fehlenden Artefakten oder klar erwarteter Verbesserung, nicht spekulativ.

<a id="reuse-existing-work"></a>
## Vorarbeiten wiederverwenden

Ziel ist der beste verifizierte Harness, kein Neubau. Prüft vor dem Aufbau fehlender Fähigkeiten Projektwerkzeuge, offene Bibliotheken, Skills, MCP-Server, Validatoren, Datensätze, Beispiele, Dokumentation, Forschung und wiederverwendbares Material. Geeignete Arbeit darf installiert, angepasst, kombiniert oder als Lernquelle genutzt werden, wenn sie Ergebnisse verbessert oder Aufwand spart.

Nutzt nichts blind. Dokumentiert Quelle, relevante Version oder Revision, Zweck, Lizenz oder Zuschreibung, Kompatibilitätsannahmen und Nutzennachweis. Prüft fremde ausführbare Inhalte vor Vertrauen. Fragt bei Zugangsdaten, bezahlten Diensten, externem Zugriff, größeren Downloads, restriktiven Lizenzen, sicherheitsrelevanter Ausführung oder wichtigen Umgebungsänderungen. Begründet ungeeignete Lösungen vor Ersatz.

Vorgeschlagene Erfolgsantworten:

- Der Agent soll Erfolgskriterien vorschlagen.
- Ich kenne das genaue Erfolgsergebnis.
- Nach dem ersten Baseline-Versuch entscheiden.

Vorgeschlagene Validierungsantworten:

- Beste Validierungsqualität.
- Visuelle oder artefaktorientierte Validierung.
- Ausgewogene Validierung.
- Ressourceneffiziente Validierung.
- Den Agenten je Aufgabe entscheiden lassen.

Optionale Nachfrage:

- Muss der Harness Grenzen, geschützte Bereiche, menschliche Prüfpunkte oder Kosten- und Zeitlimits beachten?

<a id="how-answers-map-into-harneloop"></a>
## Zuordnung der Antworten in Harneloop

- Ziel, Erfolgsstrategie, Validierungspräferenz und Artefakte bilden den Zielbrief: `harneloop target set`.
- Die aktuelle Arbeitsübersicht wird in `operational-map.md` erfasst und überarbeitet.
- Befehle, MCP-Server, manuelle Schritte oder eigene Werkzeuge bilden einen Umgebungsvertrag: `harneloop environment connect`.
- Der erste echte Ablauf wird zum Versuchsplan: `harneloop attempt plan`.
- Ergebnisse werden zu Laufartefakten: `harneloop run start`, `harneloop artifact add`, `harneloop run finish`.
- Ergebnisqualität und nächste Entscheidung werden mit `harneloop attempt conclude` erfasst.
- Harness-Änderungen werden Kandidaten und benötigen Evidenz vor Promotion.
- Nutzervorgaben werden mit `harneloop settings` verwaltet.
- Lokale Einheiten werden mit `harneloop units` gelistet oder registriert. Danach gelten ID oder Name in einheitenbezogenen Befehlen aus jedem Verzeichnis.

<a id="important-behavior"></a>
## Wichtige Verhaltensregeln

Nicht jede Aufgabe braucht einen direkten Testbefehl. Bei Werkzeugumgebungen wie Blender MCP oder agentengesteuertem SVG-Rendering deklariert Werkzeuge und Artefakte im Vertrag. Der Agent plant deren Nutzung, Artefakterzeugung und -prüfung sowie den Übergang von Beobachtungen zu Evidenz.

Strebt wiederholte Schleifen ohne manuelle App-Neustarts, Addon-Neuinstallationen, Service-Resets oder Dateisammlung an. Automatisiert oder dokumentiert vernünftige Wege; fragt bei Risiko, Unklarheit oder zu hohen Kosten und Zeitbedarf.

Bei verzögerten Artefakten oder menschlichen Urteilen nutzt `harneloop state wait`. Bei einer Fähigkeitsgrenze nutzt `harneloop state stop` mit konkretem Grund und nächster Aktion.

Abschließen erfasst Ausführungsstatus, nicht Qualität. Prüft Artefakte und entscheidet für jeden Versuch: Harness akzeptieren, Kandidaten erstellen, korrigiert wiederholen, Eingaben anfordern oder stoppen. Ein gutes erstes Ergebnis braucht keinen Kandidaten. Fehlende erwartete Evidenz rechtfertigt kein uneingeschränktes Bestehen.

Führt beim Einstieg oder Fortsetzen `harneloop brief <unit>` aus. Der erzeugte Brief gilt nur für diese Einheit und beeinflusst keine unverbundene Arbeit derselben Sitzung.

<a id="candidate-batching-and-parallel-work"></a>
## Kandidatenbündel und parallele Arbeit

Ein Kandidat ist eine kohärente Änderungshypothese, nicht jede Bearbeitung oder jeder Commit. Bündelt zusammen zu beurteilende Umgebungs-, Werkzeug-, Anweisungs- oder Validatoränderungen. Unverbundene Probleme bleiben getrennt; mehrere Kandidaten dürfen offen sein.

Klassifiziert jeden Kandidaten nach Auswirkungen:

- `target_harness`: ändert Eingaben oder Möglichkeiten des Zielagenten;
- `evaluation`: ändert Ergebnisbeobachtung oder -beurteilung;
- `infrastructure`: ändert Einrichtung, Ausführung, Reset oder Artefakterfassung;
- `mixed`: nur wenn Trennung die Bedeutung verlieren ließe.

Wählt Validierung proportional zum Fehlerrisiko:

- `structural`: Parsing, Schemas, statische Checks und Metadatenintegrität;
- `targeted`: gezielte Smoke-Tests für Werkzeug, Evaluator oder Infrastrukturpfad;
- `representative`: echte Versuche und relevante Regressionen für Verhaltensänderungen;
- `full`: breite Tests für starke Auswirkungen und Release-Prüfpunkte.

Wiederholt nicht jeden Vollbenchmark nach jedem Einrichtungsschritt. Sammelt einen kohärenten Kandidaten, markiert ihn `ready` und erfasst Evidenz auf deklarierter Stufe. Trennt Ziel-Harness und Evaluation möglichst, damit ein geänderter Evaluator nicht allein einen geänderten Harness beurteilt.

Promovierte Versionen bleiben linear. Nach einer Promotion markiert Harneloop Geschwister auf alter Basis `needs_rebase`. Gleicht sie ab, führt Rebase aus und sammelt neue Evidenz zur neuen Basis; alte bleibt Provenienz.
