<a id="core-lifecycle"></a>
# Kernlebenszyklus

<a id="harness-unit"></a>
## Harness-Einheit

Eine Harness-Einheit ist ein portables Verzeichnis mit wiederverwendbarem Harness-Material und Framework-Steuerdateien.

Erforderliche Dateien:

```text
unit/
  unit.yaml
  UNIT_AGENT.md
  operational-map.md
  candidates/
  versions/
  provenance/
```

`operational-map.md` ist das einheitenlokale Orientierungsdokument. Es erfasst das aktuelle Verständnis des Agenten: Verbesserungsziel, Nutzung der Zielumgebung, hilfreiche Artefakte oder Evidenz, übliche Ausführungs- und Reset-Wege, Fähigkeitslücken des operierenden Agenten, Einheiten- oder Zielagentenwerkzeuge, bekannte Schwachstellen, Annahmen, offene Fragen und frühere Evidenzablagen. Es soll orientieren, ohne zum starren Ablauf zu werden.

Übliche optionale Verzeichnisse:

```text
agent-facing/
observers/
validators/
regression-cases/
infrastructure/
exports/
tools/
memory/
experiments/
```

<a id="candidates"></a>
## Kandidaten

Ein Kandidat ist ein zusammenhängendes Änderungsbündel oder eine Hypothese, nicht eine Dateibearbeitung oder ein Git-Commit. Zusammen zu testende und zu promovierende Konfigurations-, Werkzeug-, Anweisungs- oder Validatoränderungen können in einem Kandidaten gesammelt werden. Für unabhängige Probleme dürfen mehrere Kandidaten offenbleiben, etwa eine Ziel-Harness-Verbesserung und eine separate Evaluationsreparatur.

```text
candidates/cand-0001/
  candidate.yaml
  rationale.md
  changes/
  validation/
  evidence/
  notes.md
```

Kandidatenänderungen werden durch das Framework angewandt. Kandidaten-Overlays dürfen geschützte Pfade wie `unit.yaml`, `versions/`, `provenance/`, `.evolve/` oder `candidates/` nicht ändern.

Jeder aktuelle Kandidat deklariert:

- eine Auswirkungsebene: `target_harness`, `evaluation`, `infrastructure` oder `mixed`;
- eine Validierungsstufe: `structural`, `targeted`, `representative` oder `full`;
- eine Lebenszyklusphase: `accumulating`, `ready`, `validating`, `needs_rebase`, `promoted` oder `rejected`;
- die promovierte Harness-Version, auf der er basiert.

Validierung ist risikoproportional. Strukturelle Prüfungen passen zu reinen Metadatenänderungen, gezielte Prüfungen zu isolierten Infrastruktur- oder Evaluatorreparaturen, repräsentative Ausführungen zu Harness-Verhaltensänderungen. Vollständige Regressionen bleiben breiten Änderungen und Release-Prüfpunkten vorbehalten. Der Agent kann stärker prüfen, sollte aber nicht für jede kleine Konfigurationsänderung den gesamten Artefaktbenchmark wiederholen.

Evaluations- und Ziel-Harness-Änderungen sollten normalerweise getrennte Kandidaten bleiben, damit ein geänderter Bewerter nicht der alleinige Verbesserungsnachweis für einen geänderten Harness ist. Ein Kandidat kann beim Sammeln verwandter Arbeit `accumulating` bleiben und zu `ready` wechseln, sobald er zusammenhängend genug für die Validierung ist.

<a id="promotion"></a>
## Promotion

Promotion wendet ein bereites Kandidaten-Overlay auf die Einheit an, erzeugt unter `versions/` einen wiederherstellbaren Snapshot und aktualisiert die Provenienz. Promovierte Versionen bleiben linear, auch bei paralleler Kandidatenarbeit.

Teilen zwei offene Kandidaten dieselbe Basis, markiert die Promotion eines Kandidaten den anderen als `needs_rebase`. Dateien und Historie bleiben intakt, aber vor Promotion muss er mit der neuen Version abgeglichen werden und frische Evidenz sammeln. Frühere Evidenz bleibt Provenienz und erfüllt nicht die Prüfung der neuen Basisversion.

Evidenzreferenzen werden beim Anhängen und erneut bei Promotion auf Integrität geprüft. Deklarierte Ausführung und Artefakt müssen existieren, die gespeicherte Artefaktdatei muss noch vorliegen und direkt referenzierte Evidenzdateien müssen existieren. Narrative Evidenz darf diese Referenzen auslassen.

<a id="run-integrity"></a>
## Ausführungsintegrität

Eine Ausführung ist nur im Status `running` veränderbar; in dieser Phase lassen sich Artefakte anhängen. Der erste erfolgreiche `run finish`-Übergang ist endgültig: spätere Artefaktzugaben und wiederholte Abschlussversuche werden abgewiesen, damit das Originalergebnis nicht still überschrieben werden kann.

<a id="rollback"></a>
## Rollback

Rollback stellt einen früheren promovierten Snapshot wieder her. Es sollte eine Framework-Aktion mit Provenienz sein, keine manuelle Kopie.

<a id="wait-and-stop"></a>
## Warten und Stoppen

Der Laufzeitlebenszyklus unterstützt ausdrückliches Warten und Stoppen.

Warten deckt verzögerte Artefakte, menschliche Prüfung, wartende Jobs, Abkühlzeiten und Infrastrukturneubauten ab.

Stoppen deckt ausreichende Evidenz, Plateaus, Fähigkeitsgrenzen, Berechtigungsbedarf oder Fälle ab, in denen der nächste hilfreiche Schritt von Menschen oder externen Systemen abhängt.

Die vollständige artefaktorientierte Entwicklungsschleife findet ihr unter [Wie Harneloop funktioniert](../framework-process.md).
