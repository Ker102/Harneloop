<a id="target-and-environment-onboarding"></a>
# Ziel- und Umgebungseinstieg

Harneloop sollte nicht annehmen, die Testumgebung des Nutzers zu besitzen.

Auch darf es keine automatische Umgebungserkundung durch die CLI suggerieren. Harneloop speichert die Zuordnung. Der Agent muss Arbeitsbereich, Werkzeuge, MCP-Server, Skripte, App-Endpunkte, Ausgabeordner und Artefaktpfade prüfen und in der Einheit erfassen.

Das Arbeitsverständnis beginnt in `operational-map.md`. Haltet Verbesserungsziel, übliche Ausführung und Resets, hilfreiche Artefakte, fragile Annahmen und offene Untersuchungen aktuell. Die Übersicht soll orientieren, nicht eine Evaluationsschablone erzwingen.

Erfasst auch Fähigkeitslücken. Werkzeuge des operierenden Agenten sind getrennt von Einheiten- oder Zielumgebungswerkzeugen. Eingeschränkte Agenten können Terminal, Browser, Dateien, MCP, Paketmanager, visuelle Prüfung, Datenbanken oder Netzwerk vermissen. Blockiert oder schwächt das den Aufbau, dokumentiert Lücke, Grund, hilfreiches Werkzeug oder Abhängigkeit und Alternative.

Zuerst sollte das Framework dem Agenten helfen zu verstehen:

- für welche Aufgabe der Harness entsteht;
- was als Erfolg zählt;
- welche Artefakte zu erfassen sind;
- welche Fehlermuster relevant sind;
- ob eine Testumgebung existiert.

Danach erstellt der Agent einen Versuchsplan. Das ist kein deterministischer Testbefehl, sondern ein agentenerstellter Ablauf zur Erzeugung und Prüfung aufgabenrelevanter Ergebnisse.

<a id="setup-modes"></a>
## Einrichtungsmodi

<a id="existing"></a>
### Bestehend

Nutzen, wenn der Nutzer bereits eine funktionierende Umgebung hat.

Beispiel: Ein Blender-Projekt hat bereits Skripte für Szenenausführung, Screenshots und Logexport.

Der Agent sollte die Verbindung dokumentieren durch:

- den Laufbefehl;
- Artefaktausgabepfade;
- zu erfassende Screenshots, Renderings, Logs oder strukturierte Zusammenfassungen;
- umgebungsspezifische Hinweise.

Nicht neu bauen, außer bei fehlgeschlagenen Prüfungen oder Nutzerwunsch.

Reduziert wiederholte Handarbeit. Automatisiert oder dokumentiert sichere Service-Neustarts, App-Resets, Artefakterfassung und Vorbereitung. Fragt bei Risiko, Unklarheit oder hohen Kosten.

Erweiterungen brauchen Evidenz. Lokale Werkzeuge mit geringem Risiko dürfen bei passender Umgebung installiert, aktiviert oder gebaut werden. Größere Abhängigkeiten, Zugangsdaten, bezahlte APIs, externer Zugriff, Nutzerkonten, Netzerweiterungen und Sicherheitsänderungen sind vorher vorzuschlagen.

Verwaltete oder unterstützte Einrichtung heißt nicht alles neu bauen. Sucht im Projekt und bei Nutzen in externer Dokumentation, offenen Werkzeugen, Skills, Bibliotheken, Validatoren, Datensätzen, Beispielen und Vorarbeiten. Bevorzugt gepflegte Lösungen, wenn sie Ergebnisse verbessern oder Arbeit sparen. Dokumentiert Quelle, Version, Zweck, Lizenz oder Zuschreibung, Kompatibilität und gemessenen Beitrag. Prüft fremde ausführbare Inhalte und beachtet übliche Risiko-, Kosten-, Zugangsdaten-, Zugriffs- und Sicherheitsberechtigungen.

Bestehende Umgebungen können befehls- oder werkzeuggesteuert sein.

Befehlsgesteuert heißt ein direkter Laufbefehl. Werkzeuggesteuert heißt Aufgaben über MCP-Server, Browserautomatisierung, Design-Plugins oder Blender-Addon-API ausführen.

<a id="assisted"></a>
### Unterstützt

Nutzen, wenn Teile existieren, aber Lücken zu identifizieren sind.

Schlagt die minimale fehlende Einrichtung für Baseline und Artefakterfassung vor.

<a id="managed"></a>
### Verwaltet

Nutzen, wenn Harneloop oder der Agent mehr Umgebung neu erstellen soll.

Infrastrukturänderungen müssen explizit und evidenzgestützt sein. Verwaltete Einrichtung ist später hilfreich, aber kein Standard für bereits funktionierende Projekte.

<a id="attempt-plans"></a>
## Versuchspläne

Viele Harness-Aufgaben lassen sich nicht auf `run this command` reduzieren.

Der Zielagent muss möglicherweise:

- MCP-Werkzeuge nutzen;
- Dateien bearbeiten;
- Szenen erstellen;
- UIs bauen;
- einen Browser ausführen;
- ein Modell ein Artefakt erzeugen lassen;
- Ausgaben visuell prüfen;
- strukturierte Zusammenfassungen exportieren;
- relevante Folgeevidenz bestimmen.

Harneloop erfasst dies als Versuchsplan:

```powershell
harneloop attempt plan .\unit `
  --goal "Build a Blender scene with a cube on a table." `
  --method "Use Blender MCP tools to create objects, render, and export scene summary." `
  --action "Create table, cube, camera, and light." `
  --action "Render and capture screenshot." `
  --expected-artifact render `
  --expected-artifact scene_summary `
  --success-check "Cube rests on table." `
  --success-check "Objects are visible to camera."
```

Ein Lauf kann dann auf den Versuch verweisen:

```powershell
harneloop run start .\unit --task "Baseline Blender spatial scene" --attempt-id attempt-0001
```

Nach Artefakterfassung werden Beobachtungen ergänzt:

```powershell
harneloop attempt observe .\unit attempt-0001 `
  --run-id run-0001 `
  --outcome failed `
  --summary "Render exists but cube floats above the table." `
  --finding "Likely z-coordinate placement issue."
```

Beobachtungen können Kandidatenevidenz oder Regressionsfälle werden.

<a id="agent-questions"></a>
## Agentenfragen

Fragt beim Start eines echten Harness nur nach fehlenden Angaben:

- Was ist die Zielaufgabenfamilie?
- Welche Ausgabeartefakte zählen?
- Gibt es eine funktionierende Testumgebung?
- Ist die Umgebung befehls-, werkzeuggesteuert, manuell oder individuell?
- Bei Befehlen: welcher startet Test oder Aufgabe?
- Bei Werkzeugen: welche nutzt der Agent?
- Wo landen Screenshots, Renderings, Logs oder Zusammenfassungen?
- Welche häufigen Fehler sollen Regressionsfälle werden?

<a id="blender-case"></a>
## Blender-Fall

Beim bestehenden Blender-Projekt ist der Modus wahrscheinlich `existing`.

Der Interaktionsmodus kann `mcp` statt `command` sein.

Es kann keinen direkten Testbefehl geben. Der Zielagent nutzt Blender MCP und Addon-Werkzeuge für Szenenänderung, Renderings, Screenshots, Objektprüfung oder Szenenzusammenfassungen.

Zuerst nicht Blender installieren oder einen Runner bauen, sondern Harneloop verbinden mit:

- bestehender MCP- oder Werkzeugschnittstelle;
- den vom Agenten zu nutzenden Werkzeugen;
- Artefaktpfaden für Renderings, Screenshots, Logs und Szenenzusammenfassungen;
- dem Baseline-Ablauf für Szenenbau und Artefakterfassung.

Beispiel:

```powershell
harneloop environment connect .\blender-unit `
  --name "Existing Blender MCP environment" `
  --mode existing `
  --interaction-mode mcp `
  --description "Agent interacts with Blender through an MCP server and addon tools." `
  --tool create_object `
  --tool render_scene `
  --tool capture_screenshot `
  --tool export_scene_summary `
  --artifact-path "outputs/renders/*.png" `
  --note "Use MCP tools instead of looking for a single run command."
```

Danach erfasst Harneloop Läufe und Artefakte, speichert Evidenz und promoviert Änderungen. Der Blender-MCP-Server bleibt Ausführungsschnittstelle.
