<a id="how-harneloop-works"></a>
# Cómo funciona Harneloop

Harneloop da al agente operador un ciclo persistente, condicionado por evidencia, para mejorar el harness de un agente objetivo. El agente operador sigue eligiendo cómo trabajar: Harneloop registra la evolución del entorno, los artefactos, los cambios candidatos y el historial de promociones sin reducir el proceso a un script fijo de pruebas.

Para una versión de tres etapas más pequeña, adecuada para un README o un gráfico de aproximadamente 4:3, consulta el [ciclo de vida compacto](framework-process-compact.md).

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
## Los tres roles

**El agente operador** descubre el entorno real, elige pruebas, utiliza o añade capacidades, inspecciona artefactos, diagnostica fallos y propone cambios candidatos del harness.

**La unidad de harness** contiene instrucciones reutilizables, herramientas, observadores, validadores, ejemplos, declaraciones de infraestructura, mapa operativo, candidatos y versiones promovidas para una familia de tareas.

**El motor Harneloop** controla la integridad del ciclo de vida: registros atómicos, ejecuciones terminadas inmutables, estado protegido del framework, referencias de evidencia validadas, promoción de candidatos, instantáneas, reversión, empaquetado y exportaciones.

<a id="what-evolves"></a>
## Qué evoluciona

Un candidato puede cambiar más que un prompt. Puede añadir o modificar herramientas, datos de recuperación, ejemplos, instrucciones para agentes, validadores, observadores, investigación, declaraciones de infraestructura o automatización del entorno. Es un lote coherente, por lo que los cambios relacionados pueden acumularse sin exigir una prueba completa tras cada edición. Pueden coexistir candidatos independientes del harness objetivo, evaluación e infraestructura. La promoción convierte un candidato exitoso en una versión restaurable; los candidatos con la base anterior se conservan, pero necesitan rebase y evidencia nueva.

<a id="what-the-diagram-leaves-open"></a>
## Qué deja abierto el diagrama

La ejecución exacta de la tarea y la estrategia de evaluación son deliberadamente específicas de cada unidad. Una unidad Blender puede usar un servidor MCP e inspeccionar renders o el estado de la escena. Una unidad SVG puede renderizar en un navegador y comparar evidencia visual y estructural. Harneloop aporta el proceso y los límites de integridad; el agente operador relaciona cada entorno real con ellos.
