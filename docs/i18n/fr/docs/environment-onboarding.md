<a id="target-and-environment-onboarding"></a>
# Intégration de la cible et de l’environnement

Harneloop ne doit pas supposer qu’il possède l’environnement de test de l’utilisateur.

Il ne doit pas non plus laisser entendre que la CLI découvre l’environnement automatiquement. Harneloop stocke la cartographie. L’agent doit inspecter espace réel, outils, serveurs MCP, scripts, endpoints, dossiers de sortie et chemins d’artefacts, puis consigner la correspondance dans l’unité.

La compréhension de travail commence dans `operational-map.md`. Actualisez objectif, exécution et réinitialisation habituelles, artefacts utiles, hypothèses fragiles et points à explorer. La carte doit orienter, pas imposer une seule recette d’évaluation.

Consignez aussi les capacités manquantes. Les outils de l’agent opérateur sont distincts de ceux de l’unité ou de l’environnement cible. Un agent restreint peut manquer de terminal, navigateur, fichiers, MCP, gestionnaire de paquets, inspection visuelle, bases ou réseau. Si cela bloque ou affaiblit la construction, consignez manque, raison, outil ou dépendance utile et repli.

Le framework doit d’abord aider l’agent à comprendre :

- pour quelle tâche le harness est construit ;
- ce qui compte comme réussite ;
- quels artefacts recueillir ;
- quels motifs d’échec comptent ;
- si un environnement de test existe déjà.

L’agent crée ensuite un plan de tentative. Ce n’est pas une commande déterministe, mais un workflow rédigé pour produire et inspecter quelque chose de pertinent pour la tâche cible.

<a id="setup-modes"></a>
## Modes de configuration

<a id="existing"></a>
### Existant

À utiliser si l’utilisateur a déjà un environnement fonctionnel.

Exemple : un projet Blender possède déjà des scripts d’exécution, de capture et d’export de journaux.

L’agent doit le connecter en documentant :

- la commande d’exécution ;
- les chemins de sortie des artefacts ;
- les captures, rendus, journaux ou résumés structurés à recueillir ;
- toute note propre à l’environnement.

Ne reconstruisez pas l’environnement sauf échec des contrôles ou demande utilisateur.

Réduisez les tâches manuelles répétées. Si redémarrer les services, réinitialiser les apps, recueillir les artefacts ou préparer l’environnement peut être automatisé sans risque, implémentez ou documentez. Sinon, en cas de risque, d’incertitude ou de coût élevé, demandez.

Les ajouts doivent être étayés. L’outillage local peu risqué peut être installé, activé ou construit si permis. Proposez d’abord dépendances importantes, identifiants, API payantes, accès externe, comptes utilisateur, extension réseau ou changements de sécurité.

Configuration gérée ou assistée ne signifie pas tout reconstruire. Cherchez dans le projet puis, si utile, documentation externe, outils ouverts, skills, bibliothèques, validateurs, données, exemples et travaux antérieurs. Préférez une solution maintenue si elle améliore le résultat ou évite du travail. Consignez source, version, but, licence ou attribution, compatibilité et contribution mesurée. Examinez les exécutables tiers et respectez les permissions habituelles de risque, coût, identifiants, accès et sécurité.

Les environnements existants peuvent être pilotés par commandes ou outils.

Piloté par commandes signifie une commande directe à lancer. Piloté par outils signifie agir via serveur MCP, automatisation du navigateur, plugin de design ou API d’addon Blender.

<a id="assisted"></a>
### Assisté

À utiliser si une partie existe mais qu’il faut identifier les manques.

Proposez la configuration minimale manquante pour une référence et sa collecte d’artefacts.

<a id="managed"></a>
### Géré

À utiliser si Harneloop ou l’agent doit créer davantage de l’environnement de zéro.

Les changements d’infrastructure doivent être explicites et étayés. La configuration gérée sera utile plus tard, mais pas par défaut pour les projets déjà fonctionnels.

<a id="attempt-plans"></a>
## Plans de tentatives

Beaucoup de tâches ne se réduisent pas à `run this command`.

L’agent cible peut devoir :

- utiliser des outils MCP ;
- éditer des fichiers ;
- créer des scènes ;
- construire une interface ;
- lancer un navigateur ;
- demander à un modèle de générer un artefact ;
- inspecter visuellement la sortie ;
- exporter des résumés structurés ;
- décider des preuves complémentaires pertinentes.

Harneloop le consigne comme plan de tentative :

```powershell
harneloop attempt plan .\unit `
  --goal "Build a Blender scene with a cube on a table." `
  --method "Use Blender MCP tools to create objects, render, and export scene summary." `
  --action "Create table, cube, camera, and light." `
  --action "Render and capture screenshot." `
  --expected-artifact render `
  --expected-artifact scene_summary `
  --success-check "Cube rests on table." `
  --success-check "Objects are visible to camera."
```

Une exécution peut ensuite référencer cette tentative :

```powershell
harneloop run start .\unit --task "Baseline Blender spatial scene" --attempt-id attempt-0001
```

Après la collecte des artefacts, ajoutez les observations :

```powershell
harneloop attempt observe .\unit attempt-0001 `
  --run-id run-0001 `
  --outcome failed `
  --summary "Render exists but cube floats above the table." `
  --finding "Likely z-coordinate placement issue."
```

Ces observations peuvent devenir des preuves candidates ou des régressions.

<a id="agent-questions"></a>
## Questions de l’agent

Au démarrage d’un harness réel, ne demandez que les informations manquantes :

- Quelle est la famille de tâches cible ?
- Quels artefacts de sortie comptent ?
- Avez-vous un environnement de test fonctionnel ?
- L’environnement est-il piloté par commandes, outils, manuel ou personnalisé ?
- Si par commandes : laquelle lance le test ou la tâche ?
- Si par outils : lesquels l’agent utilise-t-il ?
- Où sont écrits captures, rendus, journaux ou résumés structurés ?
- Quels échecs fréquents doivent devenir des régressions ?

<a id="blender-case"></a>
## Cas Blender

Pour le projet Blender existant, le mode probable est `existing`.

Le mode d’interaction peut être `mcp`, pas `command`.

Il peut n’y avoir aucune commande de test directe. L’agent cible utilise Blender MCP et l’addon pour modifier la scène, effectuer des rendus, capturer, inspecter les objets ou exporter des résumés.

La première étape n’est pas d’installer Blender ou un nouvel exécuteur, mais de connecter Harneloop à :

- l’interface MCP ou outils existante ;
- les outils à utiliser ;
- les chemins des rendus, captures, journaux et résumés de scène ;
- le workflow de référence pour créer une scène et recueillir les artefacts.

Exemple :

```powershell
harneloop environment connect .\blender-unit `
  --name "Existing Blender MCP environment" `
  --mode existing `
  --interaction-mode mcp `
  --description "Agent interacts with Blender through an MCP server and addon tools." `
  --tool create_object `
  --tool render_scene `
  --tool capture_screenshot `
  --tool export_scene_summary `
  --artifact-path "outputs/renders/*.png" `
  --note "Use MCP tools instead of looking for a single run command."
```

Ensuite, Harneloop consigne les exécutions, recueille les artefacts, stocke les preuves et promeut les changements. Blender MCP reste l’interface d’exécution.
