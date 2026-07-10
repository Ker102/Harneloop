# Harneloop Lifecycle - Compact

This version keeps only the core evidence-backed harness evolution loop. Its three stacked rows are intended to stay readable in GitHub Markdown and translate cleanly into a roughly 4:3 graphic.

```mermaid
flowchart TB
    subgraph OBSERVE["1. Observe"]
        direction LR
        G["Goal + environment"] --> A["Attempt real task"] --> I["Capture + inspect evidence"]
    end

    subgraph IMPROVE["2. Improve"]
        direction LR
        D["Trace likely failure"] --> C["Create candidate"] --> T["Retest + regressions"]
    end

    subgraph PROMOTE["3. Decide"]
        direction LR
        Q{"Improvement proven?"} -->|Yes| P["Promote version"] --> X["Continue, export, or package"]
        Q -->|No| R["Revise candidate<br/>and repeat"]
    end

    I --> D
    T --> Q
```

The promoted harness remains unchanged until the evidence gate confirms an improvement. A rejected candidate returns to diagnosis and revision without replacing the current version.

See [How Harneloop Works](framework-process.md) for the full architecture diagram.

The raw Mermaid source is available at [`docs/diagrams/framework-process-compact.mmd`](diagrams/framework-process-compact.mmd).
