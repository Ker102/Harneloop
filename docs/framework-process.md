# How Harneloop Works

Harneloop gives an operating agent a persistent, evidence-gated loop for improving the harness around a target agent. The operating agent still chooses how to work: Harneloop records the evolving environment, artifacts, candidate changes, and promotion history without reducing the process to a fixed test script.

For a smaller three-stage version suitable for README placement or a roughly 4:3 graphic, see the [compact lifecycle](framework-process-compact.md).

```mermaid
flowchart TD
    U["User goal and context"] --> M["Operational map<br/>tools, environment, evidence, assumptions"]

    subgraph W["Artifact-aware work loop"]
        direction TB
        P["Plan an attempt"] --> X["Target agent performs the task"]
        X --> A["Capture real artifacts<br/>renders, screenshots, files, traces, state"]
        A --> I["Inspect and reason about the result<br/>visual, structural, behavioral"]
        I --> D{"What limited the result?"}
        D -->|"Harness or environment"| C["Create a candidate harness patch"]
        D -->|"Missing capability"| G["Enable, build, or request a tool"]
        D -->|"Model frontier or plateau"| S["Record confidence, limits, and stop or wait"]
        G --> P
    end

    M --> P
    C --> T["Test candidate on relevant and regression tasks"]
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

## The Three Roles

**The operating agent** discovers the real environment, chooses tests, uses or adds capabilities, inspects artifacts, diagnoses failures, and proposes candidate harness changes.

**The harness unit** carries the reusable instructions, tools, observers, validators, examples, infrastructure declarations, operational map, candidates, and promoted versions for one task family.

**The Harneloop engine** owns lifecycle integrity: atomic records, immutable finished runs, protected framework state, validated evidence references, candidate promotion, snapshots, rollback, packaging, and exports.

## What Evolves

A candidate can change more than a prompt. It may add or revise tools, retrieval data, examples, agent instructions, validators, observers, research, infrastructure declarations, or environment automation. Promotion turns the successful candidate into a restorable harness version; unsuccessful experiments remain outside the promoted unit.

## What The Diagram Leaves Open

The exact task execution and evaluation strategy are deliberately unit-specific. A Blender unit may use an MCP server and inspect renders or scene state. An SVG unit may render outputs in a browser and compare visual and structural evidence. Harneloop supplies the process and integrity boundaries; the operating agent maps each real environment into them.
