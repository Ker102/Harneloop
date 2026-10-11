<a id="agent-onboarding"></a>
# Intégration des agents

Un agent disposant seulement du dépôt et de la tâche cible doit pouvoir comprendre Harneloop. La première étape n’est pas d’écrire un validateur ou de supposer une commande de test, mais de recueillir assez de contexte pour créer une tentative de référence.

Pour une configuration guidée destinée aux humains, exécutez :

```powershell
harneloop setup
```

Pour une liste lisible par les agents, exécutez :

```powershell
harneloop onboard
```

ou, depuis un clone avant une installation persistante de l’outil :

```powershell
uv run harneloop onboard
```

Pour une sortie lisible par machine :

```powershell
harneloop onboard --format json
```

Pour une unité créée par une ancienne version, exécutez `harneloop upgrade-unit <unit>` une fois. Cela ajoute les fichiers de protocole manquants sans remplacer le matériel existant.

<a id="minimal-user-questions"></a>
## Questions minimales à l’utilisateur

Utilisez-les comme champs de contexte, pas comme questionnaire obligatoire. L’agent peut créer l’unité provisoire et inspecter l’espace d’abord, puis ne demander que ce qui reste pertinent :

1. Dans quel domaine ce harness doit-il aider l’agent à progresser ?
2. Où sera-t-il utilisé : workflow de codage, agent applicatif, recherche ou automatisation interne ?
3. Comment traiter les critères de réussite ?
4. Comment valider les résultats ?
5. L’environnement de test existe-t-il, partiellement, doit-il être construit ou est-ce encore incertain ?

Ne transformez pas l’intégration en long formulaire. Les critères et artefacts sont des choix guidés, pas une expertise exigée. Après inspection, exécutez `harneloop intake status <unit>` et classez le contexte important comme confirmé, délégué, inféré, inconnu ou non applicable. Ne transformez pas silencieusement une inférence en fait confirmé.

Avant la première exécution réelle, résolvez les champs pertinents et consignez confirmation ou délégation explicite avec `harneloop intake acknowledge`. Si une référence, un projet cible, un identifiant ou un jugement manquant peut changer sensiblement le test, demandez-le directement ou attendez plutôt que de le mentionner seulement après configuration.

Harneloop consigne la cartographie ; il ne découvre pas seul endpoints, outils MCP, commandes, captures, rendus ou chemins d’artefacts. L’agent d’intégration doit inspecter le projet et l’environnement réels, déterminer la production des artefacts et consigner cette correspondance.

Chaque unité possède `operational-map.md`. Servez-vous-en comme orientation actuelle : objectif, systèmes et outils, artefacts et preuves utiles, exécution et réinitialisation habituelles, contraintes, fragilités, questions, hypothèses à revoir et preuves antérieures. Actualisez-le si workflow, besoins de preuve, hypothèses d’environnement ou automatisation changent.

La carte est du contexte et de la navigation, pas une procédure rigide. L’agent doit toujours raisonner à partir de la tâche, inspecter les preuves et choisir la stratégie adaptée à la tentative actuelle.

<a id="capability-gaps"></a>
## Capacités manquantes

Ne supposez pas que tous les agents opérateurs ont les capacités de Codex. Un Hermes, OpenClaw, agent applicatif ou worker restreint peut manquer de terminal, fichiers, navigateur, gestionnaires de paquets, serveurs MCP, inspection visuelle, bases de données ou autres capacités nécessaires.

Séparez deux couches :

- Capacités de l’agent opérateur : ce qu’il peut réellement utiliser pour construire l’unité.
- Outils de l’unité ou de l’agent cible : ceux intégrés dans l’unité ou fournis par le contrat d’environnement.

Si une capacité utile manque, consignez dans `operational-map.md` ce qui manque, pourquoi, l’outil ou dépendance utile, les changements de risque, coût, authentification ou sécurité et le repli si l’utilisateur refuse.

Les capacités locales à faible risque peuvent être installées, activées ou construites si l’environnement le permet. Dépendances importantes, identifiants, API payantes, comptes utilisateur, accès externe, extension réseau ou changements de sécurité doivent être proposés d’abord.

Justifiez les ajouts par des obstacles observés, échecs, artefacts manquants ou une amélioration attendue claire, pas par spéculation.

<a id="reuse-existing-work"></a>
## Réutiliser le travail existant

L’objectif est le meilleur harness vérifié, pas une implémentation de zéro. Avant de créer une capacité, examinez outils du projet, bibliothèques ouvertes, skills, serveurs MCP, validateurs, données, exemples, documentation, recherche et matériel réutilisable. L’agent peut installer, adapter, combiner ou apprendre de travaux adaptés si cela améliore les résultats ou évite un effort inutile.

Ne réutilisez pas aveuglément. Consignez source, version ou révision pertinente, but, licence ou attribution, compatibilité et preuves de valeur. Examinez le matériel exécutable tiers. Demandez d’abord pour identifiants, paiements, accès externe, téléchargements importants, licences restrictives, exécution sensible ou changements significatifs. Si une solution ne convient pas, expliquez pourquoi avant de la remplacer.

Réponses suggérées sur la réussite :

- Laisser l’agent proposer les critères.
- Je connais exactement le résultat attendu.
- Décider après la première tentative de référence.

Réponses suggérées sur la validation :

- Meilleure qualité de validation.
- Validation visuelle ou centrée sur les artefacts.
- Validation équilibrée.
- Validation économe en ressources.
- Laisser l’agent décider par tâche.

Question complémentaire facultative :

- Y a-t-il des contraintes, zones protégées, revues humaines ou limites de coût ou de temps à respecter ?

<a id="how-answers-map-into-harneloop"></a>
## Traduction des réponses dans Harneloop

- Objectif, stratégie de réussite, préférence de validation et artefacts suggérés deviennent un brief cible : `harneloop target set`.
- La carte de travail actuelle est consignée et révisée dans `operational-map.md`.
- Commandes, serveurs MCP, étapes manuelles ou outils personnalisés deviennent un contrat d’environnement : `harneloop environment connect`.
- Le premier workflow réel devient un plan de tentative : `harneloop attempt plan`.
- Les sorties deviennent des artefacts d’exécution : `harneloop run start`, `harneloop artifact add`, `harneloop run finish`.
- Qualité du résultat et prochaine décision sont consignées avec `harneloop attempt conclude`.
- Les changements de harness deviennent des candidats exigeant des preuves avant promotion.
- Les valeurs par défaut utilisateur se gèrent avec `harneloop settings`.
- Les unités locales se listent ou s’enregistrent avec `harneloop units`. Leur ID ou nom fonctionne ensuite dans les commandes d’unité depuis tout répertoire.

<a id="important-behavior"></a>
## Comportements importants

Chaque tâche n’a pas besoin d’une commande de test directe. Pour un environnement outillé, comme Blender MCP ou un rendu SVG contrôlé par agent, déclarez outils et artefacts dans le contrat. L’agent planifie ensuite leur utilisation, la production et l’inspection des artefacts et la conversion des observations en preuves.

Visez des boucles répétées sans exiger redémarrages manuels d’applications, réinstallations d’addons, réinitialisations de services ou collecte de fichiers. Automatisez ou documentez si c’est raisonnable ; demandez si c’est risqué, incertain, trop coûteux ou long.

Si un artefact ou jugement requis est retardé, utilisez `harneloop state wait`. Si l’unité atteint une limite de capacité, utilisez `harneloop state stop` avec raison précise et prochaine action.

Terminer consigne le statut d’exécution, pas la qualité. Inspectez les artefacts et concluez chaque tentative : accepter le harness, créer un candidat, relancer avec un plan corrigé, demander une entrée ou arrêter. Un bon premier résultat peut être accepté sans candidat. Des preuves attendues absentes ne permettent pas une réussite sans réserve.

À l’entrée ou à la reprise, exécutez `harneloop brief <unit>`. Le brief généré est limité à cette unité et n’affecte pas les travaux sans rapport dans la même session.

<a id="candidate-batching-and-parallel-work"></a>
## Regroupement des candidats et travail parallèle

Un candidat représente une hypothèse cohérente, pas chaque édition ou commit. Regroupez les changements liés d’environnement, outils, instructions ou validateurs à juger ensemble. Séparez les problèmes indépendants ; plusieurs candidats peuvent rester ouverts.

Classez chaque candidat selon l’impact :

- `target_harness` : modifie ce que l’agent cible reçoit ou peut faire ;
- `evaluation` : modifie l’observation ou le jugement des sorties ;
- `infrastructure` : modifie configuration, exécution, réinitialisation ou collecte ;
- `mixed` : seulement si séparer les préoccupations fait perdre le sens.

Choisissez la validation proportionnellement au risque :

- `structural` : analyse, schémas, contrôles statiques et intégrité des métadonnées ;
- `targeted` : tests fumée ciblés sur un outil, évaluateur ou chemin d’infrastructure ;
- `representative` : tentatives réelles et régressions pertinentes pour changements de comportement ;
- `full` : suites larges pour changements importants et jalons de livraison.

Ne relancez pas tout le benchmark après chaque configuration. Accumulez un candidat cohérent, marquez-le `ready`, puis recueillez les preuves au niveau déclaré. Séparez si possible harness cible et évaluation pour que l’évaluateur modifié ne soit pas son seul juge.

Les versions promues restent linéaires. Si un candidat est promu et d’autres partagent l’ancienne base, Harneloop les marque `needs_rebase`. Réconciliez-les, faites un rebase et recueillez de nouvelles preuves ; les anciennes restent dans la provenance.
