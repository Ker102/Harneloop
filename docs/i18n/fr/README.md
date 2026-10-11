<div align="center">

<h1><img src="../../assets/harneloop-mark.svg" alt="" width="56" height="56" align="absmiddle" /> Harneloop</h1>

<p>Évolution du harness des agents IA centrée sur les artefacts.</p>

<p><a href="https://harneloop.kaelux.dev/">Site web</a> · <a href="#agent-quick-start">Démarrage rapide</a> · <a href="#documentation">Documentation</a></p>

</div>

<!-- i18n-switcher:start -->
[English](../../../README.md) | [Español](../es/README.md) | [简体中文](../zh-CN/README.md) | Français | [日本語](../ja/README.md) | [Deutsch](../de/README.md) | [Português (Brasil)](../pt-BR/README.md)
<!-- i18n-switcher:end -->

**Aidez un agent IA à apprendre de ses erreurs.**

Un agent peut terminer une tâche, annoncer sa réussite et laisser malgré tout du code cassé, un mauvais rendu ou un workflow inutilisable. Harneloop offre à votre agent existant une méthode structurée pour inspecter le résultat, revoir ses actions, identifier l’erreur probable et tester une meilleure approche.

L’agent améliore son **harness** : les instructions, outils, contexte et contrôles autour du modèle. Le modèle lui-même n’a pas besoin d’être réentraîné. Une modification proposée ne devient la version de travail qu’après validation par un test.

<a id="what-can-you-use-it-for"></a>
## À quoi peut-il servir ?

Utilisez Harneloop lorsqu’un agent répète des erreurs similaires et que vous pouvez inspecter ses productions : code et tests, workflows de navigateur, documents générés ou tâches visuelles. Le premier cas publié concerne la construction de scènes Blender avec ViperMesh ; les autres familles de tâches restent ouvertes aux tests et contributions.

<a id="how-it-works"></a>
## Comment ça fonctionne

1. **Tentez la tâche.** Conservez la production et les étapes suivies par l’agent.
2. **Inspectez le résultat.** Vérifiez l’artefact lui-même plutôt que de croire le message de fin.
3. **Revenez en arrière.** Reliez le problème à un appel d’outil, un contexte manquant, une instruction ou une décision d’environnement.
4. **Testez une amélioration.** Laissez l’agent proposer un changement et relancer les contrôles pertinents.
5. **Gardez ce qui fonctionne.** Préservez les améliorations étayées et une version restaurable.

<p align="center">
  <a href="https://harneloop.kaelux.dev/media/harneloop-how-it-works.mp4">
    <img src="https://harneloop.kaelux.dev/media/harneloop-video-poster.png" alt="Découvrez Harneloop : d’un objectif à un harness réutilisable" width="900" />
  </a>
</p>

<p align="center"><a href="https://harneloop.kaelux.dev/media/harneloop-how-it-works.mp4"><img src="../../assets/readme-play.svg" alt="" width="18" height="18" align="absmiddle" /> Découvrez le fonctionnement de Harneloop - 3:40</a></p>

Chaque famille de tâches possède une **unité de harness** : un espace portable réunissant objectif, outils, tentatives, preuves et améliorations. Vous pouvez faire une pause et reprendre plus tard sans recommencer l’enquête.

<a id="try-harneloop"></a>
## Essayer Harneloop

[Installez depuis PyPI](https://pypi.org/project/harneloop/) dans un environnement d’outil isolé :

```bash
uv tool install harneloop
harneloop setup
```

Ou utilisez `python -m pip install harneloop` dans votre environnement Python. Consultez [Installer et démarrer](#install-and-start) pour les prérequis et l’installation depuis les sources.

Donnez ensuite à un agent compétent le lien du dépôt et la tâche à améliorer. Le [démarrage rapide pour agents](#agent-quick-start) inclut un prompt prêt à l’emploi.

**État :** Alpha publique. La boucle centrale fonctionne ; les validations sur d’autres tâches et les contributions sont bienvenues. [Signaler un problème ou partager un cas d’usage](https://github.com/Ker102/Harneloop/issues).

<a id="evidence-from-a-real-case-study"></a>
## Preuves d’un cas réel

Harneloop a servi à développer l’unité personnalisée ViperMesh pour le raisonnement spatial et la construction de scènes Blender. La comparaison gardait le modèle exécutant fixe à **GPT-5.5 High** et testait le harness ViperMesh évolué face à la **référence du serveur Anthropic x Blender MCP**, isolant le harness comme principale couche système modifiée.

- ViperMesh était plus rapide sur **6 des 7** tâches réelles comparables, avec une **accélération moyenne de 2.534x**.
- L’évaluation visuelle préliminaire par un LLM neutre s’est améliorée de **8.19 points** sur sept paires de rendus réels.
- L’usage total de tokens de l’agent exécutant était **90.91% inférieur** sur sept benchmarks comparables, soit environ **175K contre 1.9M tokens** au total.

Harneloop n’a pas généré les scènes lui-même. Il a structuré la boucle de preuves et d’artefacts qui a révélé les faiblesses, guidé le développement des outils et du harness et vérifié l’amélioration du benchmark. Lisez la méthodologie, les limites et les résultats complets dans le [cas ViperMesh](https://kristoferjussmann.me/case-studies/vipermesh).

Ces résultats apportent une preuve empirique directe du fonctionnement du processus Harneloop dans un environnement réel riche en artefacts : le modèle exécutant est resté identique tandis que le harness évolué a produit des gains mesurables de vitesse, de performance visuelle et d’efficacité en tokens.

<a id="demonstration-vipermesh-mcp"></a>
### Démonstration : ViperMesh MCP

[Voir la démonstration de Harneloop avec ViperMesh MCP](https://www.youtube.com/watch?v=bs74QJ6UD5E&t=2s).

La construction de scènes Blender est un cas concret d’inspection des productions et d’amélioration des outils et instructions de l’agent. Consultez le [cas Harneloop](https://kristoferjussmann.me/case-studies/harneloop/#harneloop-demo) pour le framework et l’[étude du benchmark ViperMesh](https://kristoferjussmann.me/case-studies/vipermesh/) pour les résultats mesurés. Le [connecteur Blender public](https://github.com/Ker102/vipermesh-blender) est disponible séparément du studio complet et du harness évalué.

<a id="start-here"></a>
## Commencer ici

- **Utiliser Harneloop avec un agent :** [Démarrage rapide pour agents](#agent-quick-start)
- **Installer vous-même :** [Installer et démarrer](#install-and-start)
- **Comprendre les unités :** [Qu’est-ce qu’une unité de harness ?](#what-is-a-harness-unit)
- **Comprendre la boucle :** [Le cycle de vie simplifié](#the-lifecycle-made-simple)
- **Preuves mesurées :** [Cas ViperMesh](https://kristoferjussmann.me/case-studies/vipermesh)
- **Connecter un environnement réel :** [Configuration de l’environnement](#environment-setup)
- **Modifier les valeurs par défaut :** [Configuration](#configuration)
- **Architecture technique :** [Cycle central](docs/architecture/core-lifecycle.md), [couches d’exécution](docs/architecture/runtime-layers.md) et [concurrence](docs/architecture/concurrency.md)
- **Instructions complètes pour agents :** [Intégration des agents](docs/agent-onboarding.md)
- **Processus visuel :** [Fonctionnement](#how-it-works), [diagramme compact modifiable](docs/framework-process-compact.md) et [diagramme détaillé](docs/framework-process.md)

<a id="why-harneloop-exists"></a>
## Pourquoi Harneloop existe

Les modèles répètent souvent les mêmes échecs parce que les leçons utiles d’une tentative ne deviennent jamais une partie testée de leur environnement de travail. Un prompt plus long ou un score d’évaluation ne résout pas l’ensemble du problème.

Le modèle n’est qu’une partie des performances d’un agent. Son harness détermine le contexte visible, les outils disponibles, les interactions avec l’environnement, la mémoire, l’inspection des résultats et la transformation des erreurs en améliorations durables. Pour de nombreux problèmes spécifiques, c’est le levier d’amélioration le plus puissant : des gains importants sans réentraînement, avec des changements inspectables, testables, réversibles et portables.

Harneloop structure ce travail et le rend efficace. Au lieu d’accumuler des modifications ponctuelles de prompts, il permet à l’agent de développer plusieurs unités indépendantes, de tester par des tentatives réelles, de préserver preuves et historique, puis de poursuivre ou d’exporter chaque harness réussi comme un paquet cohérent.

Harneloop donne à l’agent opérateur une boucle d’amélioration contrôlée :

- travailler sur la tâche réelle, pas seulement sur un benchmark synthétique ;
- capturer rendus, captures d’écran, fichiers, traces, journaux, état structuré ou autres artefacts ;
- inspecter les artefacts visuellement, structurellement ou selon leur comportement ;
- rattacher les résultats faibles aux instructions, outils, contexte, recherche, environnement ou limites du modèle ;
- développer des améliorations sous forme de correctifs candidats isolés ;
- tester les candidats avec de nouvelles tentatives et des cas de régression ;
- ne promouvoir que les changements étayés par des preuves valides ;
- préserver des versions restaurables et empaqueter le harness obtenu pour le réutiliser.

L’agent reste libre de raisonner et d’expérimenter dans l’espace du harness. Harneloop contrôle les limites sensibles à l’intégrité : enregistrements, état protégé, preuves, promotion, instantanés, retour arrière et empaquetage.

<details>
<summary>Contexte de recherche : pourquoi améliorer le harness avant les poids ?</summary>

<a id="why-improve-the-harness-before-the-weights"></a>
### Pourquoi améliorer le harness avant les poids ?

Les recherches sur les interfaces d’agents, la recherche d’information, les outils et le feedback itératif montrent que modifier le système autour du modèle peut améliorer fortement les performances sans changer ses poids. Lorsque contexte, recherche, outils, feedback ou interaction avec l’environnement sont les principaux obstacles, les méthodes de harness peuvent surpasser le fine-tuning, parfois largement, en conservant les capacités générales du modèle. Harneloop est né de problèmes pratiques de construction de harness ; les travaux suivants soutiennent indépendamment cette orientation :

- [Self-Harness](https://arxiv.org/abs/2606.09498) a montré que les agents pouvaient extraire des faiblesses des traces, proposer des changements de harness, les valider par régression et améliorer les taux de réussite sur des tests réservés dans trois familles de modèles.
- [SWE-agent](https://arxiv.org/abs/2405.15793) a montré qu’une interface agent-ordinateur conçue sur mesure améliorait fortement la navigation des dépôts, l’édition de code et l’exécution des tests par les modèles de langage.
- [Reflexion](https://arxiv.org/abs/2303.11366) a amélioré les agents par essais et erreurs, feedback linguistique et mémoire épisodique, plutôt que par mises à jour des poids.
- [Self-Refine](https://arxiv.org/abs/2303.17651) a rapporté un gain absolu moyen d’environ 20 points de pourcentage sur sept tâches évaluées, par feedback et raffinement itératifs sans entraînement supplémentaire.
- [Fine-Tuning or Retrieval?](https://aclanthology.org/2024.emnlp-main.15/) a trouvé que le RAG surpassait systématiquement le fine-tuning non supervisé sur les tâches d’injection de connaissances évaluées, existantes comme nouvelles.
- [Does Fine-Tuning LLMs on New Knowledge Encourage Hallucinations?](https://arxiv.org/abs/2405.05904) a montré les difficultés d’acquisition de faits nouveaux par fine-tuning supervisé et une tendance accrue aux hallucinations lors de cet apprentissage.

Avec le cas ViperMesh, cela soutient une stratégie pratique : **optimiser d’abord le harness, mesurer le résultat et ne modifier les poids que lorsque les preuves montrent qu’il a atteint sa limite utile.** Les changements de harness sont plus rapides à inspecter, annuler, réutiliser et valider, et peuvent, sur les tâches adaptées, apporter des gains plus grands que les changements de poids sans modifier durablement le modèle de base.

Cela ne prouve pas qu’un harness surpassera toujours toute méthode de fine-tuning. Celui-ci reste utile pour le comportement, le style, la latence, les représentations spécialisées ou les capacités difficiles à fournir à l’inférence. Un bon harness et un fine-tuning bien choisi peuvent aussi se compléter.

</details>

<a id="what-is-a-harness-unit"></a>
## Qu’est-ce qu’une unité de harness ?

Une **unité de harness** est un espace portable pour améliorer une famille de tâches. Chaque unité évolue indépendamment et conserve définition de cible, carte d’environnement, matériel du harness, expériences, preuves, régressions et versions promues.

Une nouvelle unité commence avec cette structure :

```text
my-harness-unit/
  unit.yaml                 identity and current version
  UNIT_AGENT.md             instructions for agents entering the unit
  operational-map.md        current understanding of tools, artifacts, and workflow
  target/                   task goal and suggested first tests
  environment/              contract for commands, MCP tools, apps, and artifact paths
  agent-facing/             promoted instructions and context
  tools/                    unit-specific helper tools
  observers/                ways to inspect outputs
  validators/               deterministic or agent-driven checks
  regression-cases/         failures that future candidates should not repeat
  candidates/               isolated proposed harness changes
  runtime/                  local runs and captured artifacts
  versions/                 restorable promoted snapshots
  provenance/               human-readable change history
```

Ce n’est pas un modèle restrictif. Les agents peuvent ajouter recherche, scripts, données de recherche, déclarations d’infrastructure, mémoire, observateurs personnalisés ou dossiers nouveaux. Le framework ne protège que les fichiers et règles nécessaires à la compréhension et à la récupération de l’unité.

<a id="portable-unit-versus-local-working-data"></a>
### Unité portable et données de travail locales

Le matériel réutilisable appartient à l’unité portable, contrairement aux traces brutes, expériences temporaires, caches, secrets, candidats non promus et à tous les rendus historiques.

Le paquet `thin` par défaut contient les connaissances promues et contrats nécessaires pour reconstruire ou intégrer le harness. Les preuves d’exécution restent locales sauf inclusion explicite par un futur profil.

<a id="the-lifecycle-made-simple"></a>
## Le cycle de vie simplifié

1. **Décrire l’objectif.** L’utilisateur explique ce que l’agent doit améliorer.
2. **Cartographier l’environnement.** L’agent opérateur découvre l’exécution réelle et les sources de preuves utiles.
3. **Réconcilier les hypothèses.** Le contexte important est confirmé, délégué ou explicitement marqué comme inféré avant la première exécution réelle.
4. **Exécuter une référence.** L’agent tente la tâche avant de changer le harness.
5. **Inspecter et conclure.** L’agent évalue les artefacts et accepte, change, relance, demande une entrée ou s’arrête explicitement.
6. **Créer ou étendre des candidats si nécessaire.** Les changements liés s’accumulent en lots cohérents isolés ; des problèmes indépendants peuvent avoir des candidats parallèles.
7. **Valider selon le risque.** L’agent utilise des contrôles structurels, ciblés, représentatifs ou complets et joint des preuves.
8. **Promouvoir, réviser, attendre ou arrêter.** Les améliorations étayées deviennent une version ; les candidats faibles sont révisés ou rejetés.
9. **Exporter ou empaqueter.** Le harness promu peut servir à un agent de code, applicatif ou à un autre environnement compatible.

Les exécutions terminées sont immuables. Les preuves candidates sont vérifiées à l’ajout puis à la promotion : exécutions supprimées, artefacts absents ou fichiers de preuve manquants ne peuvent donc soutenir une livraison.

Les candidats ne sont pas des enveloppes par commit. Un candidat de configuration ou d’outillage peut regrouper des changements et recevoir un test fumée ciblé ; un changement de comportement peut exiger des tentatives avec artefacts réels et des régressions. Harness cible, évaluation et infrastructure peuvent avancer indépendamment. Si l’un est promu, les candidats parallèles sur l’ancienne base doivent faire un rebase et produire de nouvelles preuves avant promotion.

La vidéo en haut explique la boucle. Le [document compact](docs/framework-process-compact.md) contient un diagramme Mermaid modifiable. Le [diagramme détaillé](docs/framework-process.md) couvre les capacités manquantes, l’intervention humaine, l’attente, l’arrêt et la boucle complète centrée sur les artefacts.

<a id="what-makes-it-different"></a>
## Qu’est-ce qui le distingue ?

<a id="artifact-aware"></a>
### <img src="../../assets/readme-observe.svg" alt="" width="18" height="18" align="absmiddle" /> Centré sur les artefacts

Harneloop considère la production comme une preuve. L’agent peut inspecter une image, scène, interface, document, dépôt généré, trace d’exécution, état de base de données ou toute sortie utile plutôt que son propre rapport textuel.

<a id="harness-building-not-only-scoring"></a>
### <img src="../../assets/readme-improve.svg" alt="" width="18" height="18" align="absmiddle" /> Construire le harness, pas seulement noter

Le but n’est pas seulement de signaler un échec. L’agent opérateur le diagnostique et développe un changement concret du harness : prompts, principes, exemples, recherche, outils, observateurs, validateurs, régressions ou automatisation.

<a id="evidence-gated-self-improvement"></a>
### <img src="../../assets/readme-verify.svg" alt="" width="18" height="18" align="absmiddle" /> Auto-amélioration soumise aux preuves

L’agent actif ne peut pas réécrire librement le harness promu. Il crée un candidat, le teste, joint des preuves et le promeut via le framework. Chaque version promue peut être inspectée et restaurée.

<a id="environment-agnostic"></a>
### Indépendant de l’environnement

Le cœur ne dépend pas de Blender, des SVG, d’agents Python ou d’un fournisseur de modèles particulier. Une unité peut utiliser terminal, serveurs MCP, automatisation du navigateur, applications desktop, API, étapes manuelles ou interface d’outils personnalisée.

<a id="reasoning-remains-open-ended"></a>
### Le raisonnement reste ouvert

Harneloop structure le cycle sans transformer l’agent opérateur en script figé. L’agent choisit toujours les tests, artefacts, stratégie d’évaluation, outils et point d’arrêt adaptés.

<a id="agent-quick-start"></a>
## Démarrage rapide pour agents

Harneloop est conçu pour être utilisé principalement en dialoguant avec un agent ayant accès au système de fichiers et au terminal.

Donnez-lui le dépôt et un prompt comme celui-ci :

```text
Read this repository's README.md and docs/agent-onboarding.md.
Use Harneloop to create a harness unit that improves an agent at: [describe the task].

Inspect my existing environment before deciding how to test it. Ask only for context
that can materially change the work, and do not silently treat assumptions as confirmed.
Run a baseline, inspect its artifacts, and conclude the attempt before deciding whether
a candidate is needed. Do not promote a candidate without evidence.
```

L’agent devrait ensuite :

1. Installer Harneloop si nécessaire et exécuter `harneloop doctor`.
2. Lire `harneloop onboard --format json` ou [le guide d’intégration](docs/agent-onboarding.md).
3. Créer ou poursuivre une unité provisoire et inspecter l’environnement réel.
4. Réconcilier le contexte confirmé, délégué, inféré et inconnu au point de contrôle de collecte adaptative.
5. Mettre à jour `operational-map.md` avec la compréhension actuelle.
6. Exécuter une référence et inspecter les artefacts obtenus.
7. Conclure la tentative avant d’accepter le harness actuel ou de proposer des améliorations.

<a id="instructions-for-agents-reading-this-repository"></a>
### Instructions pour les agents lisant ce dépôt

Si vous êtes l’agent opérateur :

- Ne supposez pas que toute tâche possède une commande de test.
- Ne supposez pas que Harneloop découvre les endpoints, outils, captures ou chemins d’artefacts à votre place.
- Exécutez `harneloop brief <unit>` et lisez `AGENTS.md`, `UNIT_AGENT.md` et `operational-map.md` en entrant dans une unité ou après une perte de contexte.
- Appliquez le brief de l’unité seulement pendant son travail ; les autres projets restent hors de sa portée.
- Utilisez `harneloop intake status` pour ne faire ressortir que les questions non résolues pouvant modifier sensiblement le travail.
- Utilisez `harneloop candidate list <unit>` pour retrouver tous les travaux ouverts ; une unité n’est pas limitée à un candidat actif.
- Regroupez les changements liés en candidats cohérents et adaptez la validation à l’impact plutôt que de relancer tout le benchmark après chaque configuration.
- Séparez si possible les changements d’évaluateur et de harness cible pour garder les preuves fiables.
- Inspectez l’environnement réel et décrivez-le dans `target/` et `environment/`.
- Préférez l’inspection des artefacts réels si les contrôles déterministes ne peuvent établir la qualité.
- Séparez vos capacités des outils conçus pour l’agent cible.
- Visez le meilleur résultat vérifié, pas tout reconstruire : recherchez et réutilisez outils, skills, bibliothèques, exemples et travaux adaptés, en consignant la provenance et en respectant licences, sécurité, coûts et permissions.
- Placez les changements proposés dans un espace candidat.
- Utilisez les commandes Harneloop pour exécutions, artefacts, preuves, promotion, retour arrière, attente, arrêt et reprise.
- Demandez avant d’ajouter identifiants, services payants, accès externe, outils sensibles pour la sécurité ou infrastructure coûteuse.
- Actualisez la carte opérationnelle si hypothèses, chemins d’artefacts, outils ou automatisation changent.
- Ne vous arrêtez jamais à la fin de l’exécution : inspectez les artefacts et consignez une décision explicite avec `harneloop attempt conclude`.

L’intégration lisible par machine est disponible avec :

```bash
harneloop onboard --format json
```

<a id="install-and-start"></a>
## Installer et démarrer

Harneloop est [publié sur PyPI](https://pypi.org/project/harneloop/). Installez-le comme outil isolé via [uv](https://docs.astral.sh/uv/getting-started/installation/) ou utilisez `python -m pip install harneloop` dans votre environnement Python. La commande `harneloop` est conçue pour Windows, macOS et Linux.

```bash
uv tool install harneloop
harneloop doctor
harneloop setup
```

Pour une version non publiée depuis les sources, utilisez `uv tool install git+https://github.com/Ker102/Harneloop.git`.

Si `uv` indique que son répertoire d’outils n’est pas dans `PATH`, exécutez `uv tool update-shell` et ouvrez un nouveau terminal. Depuis un clone, les contributeurs peuvent installer la copie active avec `uv tool install --editable .` ; voir [l’environnement de développement](docs/development.md).

`harneloop setup` ouvre la CLI guidée pour les humains. Exécuter `harneloop` sans commande ouvre le menu interactif plus large dans le terminal. Les agents peuvent utiliser directement les commandes explicites non interactives.

Premières commandes utiles :

```bash
harneloop onboard
harneloop template list
harneloop units list
harneloop settings show
```

Les unités créées avec `harneloop setup` ou `harneloop init-unit` sont enregistrées automatiquement. Les unités existantes peuvent être ajoutées une fois avec :

```bash
harneloop units register /path/to/my-unit
```

Après enregistrement, utilisez l’ID ou le nom depuis n’importe quel répertoire plutôt qu’un chemin relatif :

```bash
harneloop units list
harneloop status my-unit --format markdown
harneloop environment status my-unit
```

<a id="what-the-agent-asks-you"></a>
## Ce que l’agent vous demande

L’intégration d’une nouvelle unité est volontairement courte. L’agent devrait recueillir cinq éléments :

1. Dans quel domaine ce harness doit-il aider l’agent à progresser ?
2. Où le harness sera-t-il utilisé ?
3. Définissez-vous la réussite, l’agent doit-il la proposer ou faut-il attendre la référence ?
4. La validation doit-elle privilégier qualité, preuves visuelles, équilibre ou efficacité des ressources ?
5. L’environnement de test existe-t-il, partiellement, ou doit-il être construit ?

Vous n’avez pas besoin de connaître à l’avance les tests ou artefacts parfaits. L’agent devrait les proposer après inspection lorsque c’est pertinent, et ne demander contraintes, zones protégées, coûts ou revue humaine que si ces détails comptent.

<a id="environment-setup"></a>
## Configuration de l’environnement

Harneloop consigne la cartographie de l’environnement ; l’agent opérateur la crée.

La CLI ne peut pas deviner quel outil MCP contrôle une application, où un rendu est enregistré, comment réinitialiser un workflow de navigateur ou quel état de base prouve la réussite. L’agent doit inspecter l’espace réel et rattacher ces détails à l’unité.

Trois modes de configuration sont pris en charge :

| Mode | Quand l’utiliser | Comportement de l’agent |
|---|---|---|
| `existing` | L’environnement fonctionne déjà | Le connecter et le documenter, sans le reconstruire sans raison |
| `assisted` | Certains éléments existent | Identifier et ajouter le minimum manquant pour une référence |
| `managed` | L’environnement doit être créé | Le construire explicitement et documenter les changements d’infrastructure |

Un environnement peut être piloté par commandes, MCP, étapes manuelles ou entièrement personnalisé. Un harness Blender peut par exemple utiliser un serveur MCP existant sans commande unique. L’agent appelle les outils, effectue le rendu, capture des écrans et l’état structuré de la scène, puis joint ces sorties à une exécution Harneloop.

Lisez [l’intégration de l’environnement](docs/environment-onboarding.md) pour des exemples détaillés.

<a id="configuration"></a>
## Configuration

La plupart des utilisateurs devraient commencer avec les valeurs par défaut. La première configuration utile se situe généralement dans l’unité, pas dans les réglages globaux.

<a id="harness-unit-configuration"></a>
### Configuration de l’unité de harness

| Fichier ou zone | Quand modifier |
|---|---|
| `operational-map.md` | Outils, emplacements d’artefacts, hypothèses, contraintes ou workflow changent |
| `target/brief.yaml` | Famille de tâches, définition de réussite, artefacts attendus ou risques connus changent |
| `environment/contract.yaml` | Commandes, outils MCP, modes de configuration ou d’interaction, ou chemins de sortie changent |
| `agent-facing/` | Un candidat testé promeut de nouvelles instructions ou un contexte réutilisable |
| `observers/` et `validators/` | L’unité nécessite une meilleure inspection ou des contrôles déterministes |
| `regression-cases/` | Un échec découvert doit être testé aux prochaines itérations |
| `tools/` et `infrastructure/` | De meilleures performances nécessitent des capacités ou services propres à l’unité |

Ne modifiez pas manuellement `.evolve/`, `versions/`, `provenance/`, `runtime/` ni les métadonnées candidates gérées par le framework. Utilisez les commandes CLI du cycle de vie.

<a id="global-preferences"></a>
### Préférences globales

Consultez les préférences avec `harneloop settings show` et modifiez-en une avec :

```bash
harneloop settings set validation.prefer_visual_artifacts true
harneloop settings set agent_behavior.autonomy_level balanced
harneloop settings set runtime.token_efficiency_mode false
```

Groupes importants de préférences :

- `agent_behavior` : autonomie, confirmation des actions risquées et rigueur de promotion ;
- `validation` : validation décidée par l’agent, préférence d’artefacts visuels et mode de ressources ;
- `export` : adaptateur cible et profil de paquet par défaut ;
- `runtime` : détail de télémétrie, efficacité en tokens et registre local des unités.

Dans l’alpha, les préférences sont des valeurs durables et des indications pour la CLI et l’agent opérateur. Toutes ne sont pas encore appliquées automatiquement par chaque commande du moteur. La promotion exige des preuves sauf dérogation explicite de développement.

<a id="example-use-cases"></a>
## Exemples d’utilisation

- Améliorer raisonnement spatial et construction de scènes d’un agent Blender ou CAD.
- Améliorer la génération de SVG, images, diapositives, documents ou interfaces par revue des rendus.
- Construire un harness de codage pour un dépôt avec des échecs récurrents d’implémentation ou de débogage.
- Améliorer l’automatisation du navigateur avec captures, état DOM, traces et résultats.
- Améliorer sélection d’outils et récupération d’erreurs d’un agent MCP.
- Faire évoluer recherche, exemples, validateurs et contexte pour recherche scientifique ou traitement de données.
- Construire un harness interne réutilisable et l’exporter pour Codex, Cursor ou un agent applicatif personnalisé.

Harneloop est surtout utile pour les tâches répétées, les sorties inspectables et les échecs transformables en améliorations durables. Il est inutile pour une tâche unique sans apprentissage réutilisé.

<a id="core-cli-lifecycle"></a>
## Cycle central de la CLI

Les commandes explicites sont destinées aux agents, à l’automatisation et aux utilisateurs techniques :

```bash
harneloop init-unit ./my-unit --id my-unit --name "My Harness Unit" --template artifact-review
harneloop target set my-unit --task "..." --success "..."
harneloop environment connect my-unit --name "..." --mode existing --description "..."
harneloop attempt plan my-unit --goal "..." --method "..."
harneloop run start my-unit --task "Baseline attempt"
harneloop artifact add my-unit run-0001 ./output.png --kind image
harneloop run finish my-unit run-0001 --status succeeded --summary "Baseline captured"
harneloop candidate create my-unit --summary "Improve artifact construction" --plane target_harness --validation-tier representative
harneloop run start my-unit --task "Test candidate improvement" --candidate-id cand-0001
harneloop artifact add my-unit run-0002 ./improved-output.png --kind image
harneloop run finish my-unit run-0002 --status succeeded --summary "Candidate result captured"
harneloop candidate evidence add my-unit cand-0001 --kind artifact_review --summary "..." --run-id run-0002 --artifact-id artifact-0001 --validation-tier representative
harneloop candidate stage my-unit cand-0001 ready
harneloop promote my-unit cand-0001 --version 0.1.0
harneloop export my-unit --adapter codex
harneloop package my-unit --output ./my-unit-0.1.0.tar.gz
```

Cette séquence est illustrative, pas une recette fixe. Les agents outillés peuvent effectuer de nombreuses actions entre `run start` et `run finish`, capturer plusieurs artefacts, créer plusieurs tentatives ou attendre des résultats externes.

<a id="safety-and-integrity"></a>
## Sécurité et intégrité

- Les fichiers de contrôle YAML et JSON sont écrits atomiquement.
- L’allocation concurrente des ID et les lectures-modifications-écritures utilisent des verrous locaux au harness.
- Les exécutions terminées ne peuvent être modifiées ni terminées à nouveau.
- Les couches candidates ne peuvent modifier l’état protégé du framework.
- Les références de preuves doivent exister à l’ajout et à la promotion.
- Les preuves doivent correspondre à la base actuelle et au niveau de validation déclaré du candidat.
- Les candidats parallèles survivent à une autre promotion, mais doivent faire un rebase et recueillir de nouvelles preuves avant la leur.
- Les versions promues sont conservées en instantanés restaurables.
- Le retour arrière est une action enregistrée du framework.
- Les paquets thin excluent données d’exécution, candidats, caches et fichiers courants de secrets.

<a id="documentation"></a>
## Documentation

- [Comment fonctionne Harneloop](docs/framework-process.md)
- [Intégration des agents](docs/agent-onboarding.md)
- [Intégration de l’environnement](docs/environment-onboarding.md)
- [Cycle de vie central](docs/architecture/core-lifecycle.md)
- [Couches d’exécution et future limite Rust](docs/architecture/runtime-layers.md)
- [Concurrence et sécurité des fichiers](docs/architecture/concurrency.md)
- [Principes du produit](docs/product-principles.md)
- [Démonstration locale](docs/demo-first-test.md)
- [Notes de développement](docs/development.md)

<a id="contributing"></a>
## Contribuer

Les contributions, signalements et études indépendantes d’unités sont bienvenus. Sont particulièrement utiles :

- tester Harneloop sur d’autres familles de tâches ;
- signaler des échecs reproductibles de cycle de vie, portabilité ou intégration ;
- améliorer adaptateurs d’agents cibles, validateurs, empaquetage et comportement multiplateforme ;
- contribuer à une documentation ciblée, des exemples ou des régressions.

Lisez [CONTRIBUTING.md](CONTRIBUTING.md) avant des changements importants. Ouvrez d’abord une issue pour l’architecture afin de discuter portée et compatibilité. Pour la sécurité, suivez [SECURITY.md](SECURITY.md), pas une issue publique.

<a id="development"></a>
## Développement

Exécutez les tests depuis le dépôt :

```bash
python -m unittest discover -s tests
```

Le projet utilise actuellement Python 3.11 ou plus récent. Un futur runtime Rust pourrait gérer des responsabilités renforcées de cycle de vie protégé, d’empaquetage, de surveillance de fichiers ou de distribution desktop après stabilisation.

Harneloop est l’identité retenue pour l’alpha et le lancement public. Le paquet, la CLI, les métadonnées des unités, la documentation et le dépôt utilisent le même nom.

<a id="license"></a>
## Licence

Harneloop est disponible sous la [Apache License 2.0](../../../LICENSE).
