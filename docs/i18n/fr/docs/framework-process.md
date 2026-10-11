<a id="how-harneloop-works"></a>
# Comment fonctionne Harneloop

Harneloop donne à l’agent opérateur une boucle persistante, soumise à des preuves, pour améliorer le harness d’un agent cible. L’agent opérateur choisit toujours sa manière de travailler : Harneloop consigne l’environnement évolutif, les artefacts, les changements candidats et l’historique des promotions sans réduire le processus à un script de test figé.

Pour une version plus petite en trois étapes, adaptée à un README ou à un graphique d’environ 4:3, consultez le [cycle de vie compact](framework-process-compact.md).

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
## Les trois rôles

**L’agent opérateur** découvre l’environnement réel, choisit les tests, utilise ou ajoute des capacités, inspecte les artefacts, diagnostique les échecs et propose des changements candidats du harness.

**L’unité de harness** porte les instructions réutilisables, outils, observateurs, validateurs, exemples, déclarations d’infrastructure, carte opérationnelle, candidats et versions promues pour une famille de tâches.

**Le moteur Harneloop** garantit l’intégrité du cycle de vie : enregistrements atomiques, exécutions terminées immuables, état protégé du framework, références de preuves validées, promotion des candidats, instantanés, retour arrière, empaquetage et exports.

<a id="what-evolves"></a>
## Ce qui évolue

Un candidat peut modifier plus qu’un prompt : outils, données de recherche, exemples, instructions d’agents, validateurs, observateurs, recherche, déclarations d’infrastructure ou automatisation de l’environnement. Il forme un lot cohérent ; les modifications liées peuvent s’accumuler sans imposer un test complet après chacune. Des candidats indépendants de harness cible, d’évaluation et d’infrastructure peuvent coexister. La promotion transforme un candidat réussi en version restaurable ; ceux sur l’ancienne base restent disponibles mais exigent un rebase et de nouvelles preuves.

<a id="what-the-diagram-leaves-open"></a>
## Ce que le diagramme laisse ouvert

L’exécution exacte et la stratégie d’évaluation sont volontairement propres à chaque unité. Une unité Blender peut utiliser un serveur MCP et inspecter rendus ou état de la scène. Une unité SVG peut effectuer les rendus dans un navigateur et comparer preuves visuelles et structurelles. Harneloop fournit le processus et les limites d’intégrité ; l’agent opérateur y rattache chaque environnement réel.
