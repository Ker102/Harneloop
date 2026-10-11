<a id="runtime-layers"></a>
# Laufzeitschichten

<a id="current-decision"></a>
## Aktuelle Entscheidung

Python für die erste Referenzimplementierung verwenden.

Später Rust gegenüber Go bevorzugen, falls Harneloop eine geschützte native Laufzeit benötigt.

<a id="why-rust-later"></a>
## Warum später Rust

Die native Schicht sollte nur entstehen, wenn das Framework stärkere lokale Garantien benötigt für:

- Lebenszyklusintegrität;
- geschützte Zustandsgrenzen;
- Versionssnapshots;
- Rollback;
- inhaltsadressierten Speicher;
- Artefaktpaketierung;
- Dateiüberwachung;
- Unterprozessüberwachung;
- Desktop-Paketierung.

Rust passt für diese Produktform besser als Go zur Rolle eines geschützten Kerns.

<a id="agent-boundary"></a>
## Agentengrenze

Rust sollte nicht zum offenen Harness-Design-Arbeitsbereich des Agenten werden.

Agenten sollten weiterhin arbeiten über:

- Markdown-Anweisungen;
- YAML- und JSON-Manifeste;
- Schemas;
- Kandidatenverzeichnisse;
- CLI-Befehle;
- Artefaktverträge.

Die Regel bleibt:

> Agenten können innerhalb der Kandidaten frei erkunden. Die Engine kontrolliert die Promotion.

<a id="where-go-could-still-fit"></a>
## Wo Go weiterhin passen könnte

Go bleibt ein guter Kandidat für künftige gehostete Dienste, die Koordination entfernter Worker oder Registry-Infrastruktur, falls sich Harneloop in diese Richtung entwickelt.
