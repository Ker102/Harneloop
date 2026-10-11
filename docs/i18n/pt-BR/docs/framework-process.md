<a id="how-harneloop-works"></a>
# Como o Harneloop funciona

O Harneloop fornece ao agente operador um ciclo persistente, condicionado por evidências, para melhorar o harness de um agente-alvo. O agente operador continua escolhendo como trabalhar: o Harneloop registra a evolução do ambiente, os artefatos, as mudanças candidatas e o histórico de promoções sem reduzir o processo a um script fixo de testes.

Para uma versão menor em três etapas, adequada ao README ou a uma imagem de aproximadamente 4:3, veja o [ciclo de vida compacto](framework-process-compact.md).

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
## Os três papéis

**O agente operador** descobre o ambiente real, escolhe testes, usa ou adiciona capacidades, inspeciona artefatos, diagnostica falhas e propõe mudanças candidatas no harness.

**A unidade de harness** reúne instruções reutilizáveis, ferramentas, observadores, validadores, exemplos, declarações de infraestrutura, mapa operacional, candidatos e versões promovidas de uma família de tarefas.

**O motor Harneloop** controla a integridade do ciclo de vida: registros atômicos, execuções finalizadas imutáveis, estado protegido do framework, referências de evidências validadas, promoção de candidatos, snapshots, reversão, empacotamento e exportações.

<a id="what-evolves"></a>
## O que evolui

Um candidato pode mudar mais que um prompt. Pode adicionar ou revisar ferramentas, dados de recuperação, exemplos, instruções para agentes, validadores, observadores, pesquisa, declarações de infraestrutura ou automação do ambiente. Ele representa um lote coerente, permitindo acumular edições relacionadas sem exigir um teste completo após cada mudança. Candidatos independentes de harness-alvo, avaliação e infraestrutura podem coexistir. A promoção transforma um candidato bem-sucedido em uma versão restaurável; os demais na base antiga permanecem disponíveis, mas exigem rebase e novas evidências.

<a id="what-the-diagram-leaves-open"></a>
## O que o diagrama deixa em aberto

A execução exata da tarefa e a estratégia de avaliação são deliberadamente específicas de cada unidade. Uma unidade Blender pode usar um servidor MCP e inspecionar renders ou o estado da cena. Uma unidade SVG pode renderizar saídas no navegador e comparar evidências visuais e estruturais. O Harneloop fornece o processo e os limites de integridade; o agente operador mapeia cada ambiente real para eles.
