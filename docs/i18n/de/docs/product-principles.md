<a id="product-principles"></a>
# Produktprinzipien

Harneloop ist die gewählte Produktidentität. Die Architektur bleibt unabhängig von einzelnen Benchmarks oder Aufgabenfamilien.

<a id="what-this-is"></a>
## Was es ist

Harneloop ist ein Framework, mit dem Agenten den Harness um sich selbst oder einen anderen Zielagenten bauen und verbessern.

Das Framework sollte Agenten dabei helfen:

- Aufgabenversuche durchzuführen;
- reale Artefakte zu prüfen;
- Fehler auf Ausführungen zurückzuführen;
- eine einheitenlokale Übersicht über Workflow, Evidenz, Umgebungsannahmen und offene Fragen zu pflegen;
- Fähigkeitslücken des operierenden Agenten getrennt von Einheiten- oder Zielagentenwerkzeugen zu erkennen;
- geeignete bestehende Werkzeuge, Skills, Bibliotheken, Datensätze, Beispiele und Vorarbeiten zu recherchieren und wiederzuverwenden;
- Kandidatenpatches für den Harness vorzuschlagen;
- Kandidatenpatches zu testen;
- nur evidenzgestützte Verbesserungen zu promovieren;
- portable Harness-Einheiten zu paketieren.

<a id="what-this-is-not"></a>
## Was es nicht ist

Harneloop ist nicht:

- ein allgemeines Evaluationsdashboard;
- ein Framework für feste Agentengraphen;
- ein Blender-spezifisches System;
- ein System zum Modelltraining oder Fine-Tuning;
- eine lose Sammlung von Prompts ohne Lebenszyklus.

<a id="core-design-tension"></a>
## Zentrale Designspannung

Das System ist für generative KI-Modelle gebaut und muss daher Raum für Schlussfolgern und Erkunden lassen. Gleichzeitig muss das Framework die Lebenszyklusintegrität schützen.

Die Regel:

> Agenten können innerhalb der Kandidaten frei erkunden. Die Engine kontrolliert die Promotion.

`operational-map.md` bewahrt das aktuelle Arbeitsverständnis des Agenten über eine Harness-Einheit, ohne es in ein starres Skript zu verwandeln. Der Agent sollte sich damit orientieren, es bei veränderter Evidenz aktualisieren und weiterhin von der aktuellen Aufgabe und den Artefakten ausgehen.

Das Framework sollte den Agenten, der eine Harness-Einheit baut, nicht als allmächtig betrachten. Fehlende Fähigkeiten müssen erkannt, durch Evidenz oder klar erwartete Verbesserungen begründet und unter passenden Berechtigungsgrenzen behandelt werden, bevor Werkzeuge, Abhängigkeiten, Zugangsdaten, kostenpflichtige Dienste oder breiterer externer Zugriff hinzukommen.

Harneloop optimiert die beste verifizierte Aufgabenleistung, nicht den Neuaufbau jeder Fähigkeit. Der operierende Agent sollte bestehende Lösungen prüfen und sie übernehmen, anpassen, kombinieren oder daraus lernen, wenn sie den Harness verbessern. Wiederverwendung muss prüfbar bleiben: dokumentiert was und warum, prüft Kompatibilität und beobachteten Nutzen, beachtet Lizenzen und Zuschreibung und nutzt die üblichen Berechtigungsgrenzen für Sicherheit, Zugangsdaten, externen Zugriff, Kosten oder wesentliche Infrastrukturänderungen.
