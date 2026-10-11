<a id="contributing"></a>
# Mitwirken

Harneloop befindet sich derzeit in der öffentlichen Alpha. Gezielte Issues und Beiträge sind willkommen, während sich die öffentliche API und die Formate der Harness-Einheiten stabilisieren.

<a id="development-setup"></a>
## Entwicklungsumgebung

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -e .
.\.venv\Scripts\python -m unittest discover -s tests
```

Unter macOS oder Linux:

```bash
python3 -m venv .venv
./.venv/bin/python -m pip install -e .
./.venv/bin/python -m unittest discover -s tests
```

<a id="pull-requests"></a>
## Pull Requests

Beschränkt jeden Pull Request auf ein Verhalten oder einen Teil der Architektur.

Eröffnet vor umfangreichen Architekturarbeiten ein Issue, um Problem und Kompatibilitätsfolgen abzustimmen. Fügt Tests für Lebenszyklusänderungen hinzu und aktualisiert bei Verhaltensänderungen die agentenorientierte Dokumentation.

Fordert vorerst keine automatisierte CodeRabbit-Prüfung an. Ist CodeRabbit beim Erstellen eines PR konfiguriert, fügt vor einer Prüfanforderung das CodeRabbit-ignore-Label oder -Tag des Repositorys hinzu.

<a id="standards"></a>
## Standards

- Haltet den Framework-Kern unabhängig von der Aufgabenfamilie.
- Fügt `src/harneloop` keine Blender-spezifischen Annahmen hinzu.
- Ergänzt oder aktualisiert Tests für das Lebenszyklusverhalten.
- Haltet agentenorientierte Dateien in Markdown, YAML oder JSON lesbar.
- Committet keine Geheimnisse, lokalen Laufzeitartefakte, virtuellen Umgebungen oder erzeugten Pakete.

Mit eurem Beitrag stimmt ihr zu, dass er unter der [Apache License 2.0](../../../LICENSE) des Repositorys lizenziert wird.
