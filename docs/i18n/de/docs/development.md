<a id="development"></a>
# Entwicklung

<a id="repository-layout"></a>
## Repository-Struktur

```text
src/harneloop/      Python reference implementation
tests/           Unit and behavior tests
docs/            Architecture and development notes
schemas/         Language-neutral data contracts
.github/         CI and repository automation
```

<a id="local-verification"></a>
## Lokale Prüfung

Installiert den Checkout einmal als editierbares Werkzeug auf Nutzerebene:

```powershell
uv tool install --editable .
```

Der Befehl `harneloop` bleibt dann außerhalb des Repositorys verfügbar und berücksichtigt Quellcodeänderungen. Prüft mit:

```powershell
uv run python -m compileall src tests
uv run python -m unittest discover -s tests
harneloop doctor
```

<a id="devops-baseline"></a>
## DevOps-Grundlage

Das Repository sollte Folgendes beibehalten:

- Quellcode-Struktur mit `src/`;
- wiederholbare lokale Tests;
- CI für unterstützte Python-Versionen;
- keine eingecheckten virtuellen Umgebungen oder Laufzeitartefakte;
- ausdrückliche Sicherheits- und Beitragsdokumentation;
- sprachunabhängige Schemas für Kerndatensätze.

<a id="runtime-data"></a>
## Laufzeitdaten

Laufzeitspuren, kopierte Artefakte, Ausführungsdatensätze, Versuchspläne und Experimente sind lokale Arbeitsdaten. Sie gehören nicht in portable thin-Pakete, sofern ein späteres Paketprofil sie nicht ausdrücklich einschließt.

<a id="pr-review-note"></a>
## Hinweis zur PR-Prüfung

Während des frühen Prototyps ist keine CodeRabbit-Prüfung nötig. Fügt bei einem PR das konfigurierte CodeRabbit-ignore-Tag oder -Label hinzu.
