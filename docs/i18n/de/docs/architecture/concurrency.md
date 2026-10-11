<a id="concurrency-and-file-safety"></a>
# Nebenläufigkeit und Dateisicherheit

Agenten können Harneloop-Befehle kurz nacheinander oder parallel starten. Jeder Befehl, der eine Steuerdatei liest, eine fortlaufende ID berechnet und die Datei zurückschreibt, muss den gesamten Lese-Änderungs-Schreibabschnitt schützen.

<a id="current-rule"></a>
## Aktuelle Regel

- Nutzt eine Harness-Einheiten-Sperrdatei für gemeinsame Lebenszyklusabschnitte.
- Lest die relevante YAML- oder JSON-Datei innerhalb der Sperre erneut.
- Vergebt die nächste fortlaufende ID innerhalb der Sperre.
- Schreibt YAML und JSON durch atomaren Austausch temporärer Dateien.
- Gebt die Sperre erst nach abgeschlossener Dateiaktualisierung frei.

<a id="implemented-locks"></a>
## Implementierte Sperren

- `runs`: vergibt Ausführungs-IDs.
- `run-<id>`: fügt Artefakte hinzu und beendet eine Ausführung.
- `attempts`: vergibt Versuchs-IDs.
- `attempt-<id>`: ergänzt Versuchsbeobachtungen.
- `candidates`: vergibt Kandidaten-IDs.
- `candidate-<id>-evidence`: vergibt Evidenz-IDs.
- `lifecycle`: promoviert Kandidaten und führt Versionsrollbacks aus.
- `state`: aktualisiert `.evolve/state.json` und abgeleitete Zustandsdateien.

Sperren liegen unter `.evolve/locks/`, einem frameworkeigenen Laufzeitzustand, der von portablen Paketen ausgeschlossen ist.

<a id="rust-runtime-note"></a>
## Hinweis zur Rust-Laufzeit

Dafür ist noch kein Rust nötig. Python-Dateisperren und atomarer Austausch reichen für die Alpha-CLI. Eine spätere Rust-Laufzeit kann strengere Sandbox-Isolation, Prozessüberwachung und zuverlässigere nebenläufige Dateikoordination übernehmen, sobald die Produktoberfläche stabil ist.
