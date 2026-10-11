<a id="how-harneloop-works"></a>
# Wie Harneloop funktioniert

Harneloop gibt einem operierenden Agenten eine dauerhafte, evidenzgebundene Schleife zur Verbesserung des Harness eines Zielagenten. Der Agent wählt weiterhin seine Arbeitsweise: Harneloop dokumentiert die sich entwickelnde Umgebung, Artefakte, Kandidatenänderungen und Promotionshistorie, ohne den Prozess auf ein festes Testskript zu reduzieren.

Eine kleinere dreistufige Version für das README oder eine Grafik von ungefähr 4:3 findet ihr im [kompakten Lebenszyklus](framework-process-compact.md).

```mermaid
flowchart TD
    U["User goal and context"] --> M["Operational map<br/>tools, environment, evidence, assumptions"]

    subgraph W["Artifact-aware work loop"]
        direction TB
        P["Plan an attempt"] --> X["Target agent performs the task"]
        X --> A["Capture real artifacts<br/>renders, screenshots, files, traces, state"]
        A --> I["Inspect and reason about the result<br/>visual, structural, behavioral"]
        I --> D{"What limited the result?"}
        D -->|"Harness or environment"| C["Create or extend a classified candidate batch"]
        D -->|"Missing capability"| G["Enable, build, or request a tool"]
        D -->|"Model frontier or plateau"| S["Record confidence, limits, and stop or wait"]
        G --> P
    end

    M --> P
    C --> T["Validate in proportion to impact<br/>structural, targeted, representative, or full"]
    T --> E["Attach verified run, artifact, and review evidence"]
    E --> Q{"Evidence gate"}
    Q -->|"Improved and credible"| V["Promote a restorable harness version"]
    Q -->|"Failed, regressed, or uncertain"| R["Revise or reject candidate"]
    R --> P
    V --> O["Export or package the harness unit"]
    V --> P

    H["Human input<br/>goals, permissions, uncertain judgments"] -.-> M
    H -.-> G
    H -.-> Q

    classDef context fill:#e8f0fe,stroke:#3563a9,color:#17233b;
    classDef work fill:#eef7ee,stroke:#3e7550,color:#173822;
    classDef gate fill:#fff3d6,stroke:#9a6b16,color:#4d3509;
    classDef version fill:#f1eafa,stroke:#70519a,color:#342249;
    classDef human fill:#f7eeee,stroke:#9a5656,color:#492222;
    class U,M context;
    class P,X,A,I,C,G,T,E,R work;
    class D,Q,S gate;
    class V,O version;
    class H human;
```

<a id="the-three-roles"></a>
## Die drei Rollen

**Der operierende Agent** erkundet die reale Umgebung, wählt Tests, nutzt oder ergänzt Fähigkeiten, prüft Artefakte, diagnostiziert Fehler und schlägt Harness-Kandidatenänderungen vor.

**Die Harness-Einheit** trägt wiederverwendbare Anweisungen, Werkzeuge, Beobachter, Validatoren, Beispiele, Infrastrukturdeklarationen, die Arbeitsübersicht, Kandidaten und promovierte Versionen für eine Aufgabenfamilie.

**Die Harneloop-Engine** verantwortet die Lebenszyklusintegrität: atomare Datensätze, unveränderliche abgeschlossene Ausführungen, geschützten Framework-Zustand, geprüfte Evidenzreferenzen, Kandidatenpromotion, Snapshots, Rollback, Paketierung und Exporte.

<a id="what-evolves"></a>
## Was sich entwickelt

Ein Kandidat kann mehr als einen Prompt ändern: Werkzeuge, Retrieval-Daten, Beispiele, Agentenanweisungen, Validatoren, Beobachter, Forschung, Infrastrukturdeklarationen oder Umgebungsautomatisierung. Er ist ein zusammenhängendes Bündel, sodass verwandte Änderungen ohne Volltest nach jedem Schritt gesammelt werden können. Unabhängige Ziel-Harness-, Evaluations- und Infrastrukturkandidaten können koexistieren. Promotion macht einen erfolgreichen Kandidaten zu einer wiederherstellbaren Version; Kandidaten auf der alten Basis bleiben verfügbar, benötigen aber Rebase und neue Evidenz.

<a id="what-the-diagram-leaves-open"></a>
## Was das Diagramm offenlässt

Die konkrete Aufgabenausführung und Evaluationsstrategie sind bewusst einheitenspezifisch. Eine Blender-Einheit kann einen MCP-Server nutzen und Renderings oder Szenenzustand prüfen. Eine SVG-Einheit kann im Browser rendern und visuelle mit struktureller Evidenz vergleichen. Harneloop liefert Prozess und Integritätsgrenzen; der operierende Agent bildet die realen Umgebungen darauf ab.
