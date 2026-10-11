<a id="core-lifecycle"></a>
# Cycle de vie central

<a id="harness-unit"></a>
## Unité de harness

Une unité de harness est un répertoire portable contenant du matériel réutilisable du harness et les fichiers de contrôle du framework.

Fichiers requis :

```text
unit/
  unit.yaml
  UNIT_AGENT.md
  operational-map.md
  candidates/
  versions/
  provenance/
```

`operational-map.md` est le document d’orientation local de l’unité. Il consigne la compréhension actuelle de l’agent : ce que l’unité améliore, l’utilisation de l’environnement cible, les artefacts ou preuves utiles, les exécutions et réinitialisations habituelles, les capacités manquantes de l’agent opérateur, les outils de l’unité ou de l’agent cible, les fragilités, hypothèses, questions ouvertes et emplacements des preuves antérieures. Il doit guider sans devenir une procédure rigide.

Dossiers optionnels courants :

```text
agent-facing/
observers/
validators/
regression-cases/
infrastructure/
exports/
tools/
memory/
experiments/
```

<a id="candidates"></a>
## Candidats

Un candidat est un lot cohérent de changements ou une hypothèse, pas une modification de fichier ni un commit Git. Des changements liés de configuration, d’outils, d’instructions ou de validateurs peuvent s’accumuler dans un candidat s’ils doivent être testés et promus ensemble. Plusieurs candidats peuvent rester ouverts pour des problèmes indépendants, comme une amélioration du harness cible et une réparation distincte de l’évaluation.

```text
candidates/cand-0001/
  candidate.yaml
  rationale.md
  changes/
  validation/
  evidence/
  notes.md
```

Les changements candidats sont appliqués par le framework. Les couches de modifications ne peuvent pas éditer les chemins protégés tels que `unit.yaml`, `versions/`, `provenance/`, `.evolve/` ou `candidates/`.

Chaque candidat actuel déclare :

- un plan d’impact : `target_harness`, `evaluation`, `infrastructure` ou `mixed` ;
- un niveau de validation : `structural`, `targeted`, `representative` ou `full` ;
- une étape du cycle de vie : `accumulating`, `ready`, `validating`, `needs_rebase`, `promoted` ou `rejected` ;
- la version promue du harness sur laquelle il repose.

La validation est proportionnelle au risque. Les contrôles structurels conviennent aux métadonnées seules ; les contrôles ciblés, aux réparations isolées d’infrastructure ou d’évaluateur ; les exécutions représentatives, aux changements de comportement du harness. Les suites complètes sont réservées aux changements larges et aux jalons de livraison. L’agent peut choisir un niveau supérieur, mais ne devrait pas relancer tout le benchmark d’artefacts après chaque modification incrémentale de configuration.

Les changements d’évaluation et de harness cible devraient normalement rester dans des candidats distincts afin qu’un juge modifié ne soit pas la seule preuve d’amélioration d’un harness modifié. Un candidat peut rester `accumulating` pendant le regroupement des travaux, puis passer à `ready` une fois assez cohérent pour être validé.

<a id="promotion"></a>
## Promotion

La promotion applique une couche candidate prête à l’unité, crée un instantané restaurable sous `versions/` et actualise la provenance. Les versions promues restent linéaires même lorsque le travail candidat est parallèle.

Si deux candidats ouverts partagent la même base, la promotion de l’un marque l’autre `needs_rebase`. Ses fichiers et son historique restent intacts, mais il doit être réconcilié avec la nouvelle version et recueillir des preuves fraîches avant promotion. Les preuves précédentes restent dans la provenance et ne satisfont pas le contrôle de la nouvelle base.

L’intégrité des références de preuves est vérifiée à leur ajout puis à la promotion. L’exécution et l’artefact déclarés doivent exister, le fichier stocké de l’artefact doit être présent et tout fichier de preuve directement référencé doit exister. Les preuves narratives peuvent omettre ces références.

<a id="run-integrity"></a>
## Intégrité des exécutions

Une exécution n’est modifiable que dans l’état `running` ; des artefacts peuvent alors être ajoutés. La première transition `run finish` réussie est terminale : les ajouts ultérieurs et les tentatives de clôture répétées sont rejetés pour éviter une réécriture silencieuse du résultat initial.

<a id="rollback"></a>
## Retour arrière

Le retour arrière restaure un instantané promu antérieur. Il doit être une action du framework avec provenance, pas une copie manuelle.

<a id="wait-and-stop"></a>
## Attendre et arrêter

Le cycle de vie d’exécution permet l’attente et l’arrêt explicites.

L’attente couvre les artefacts retardés, la revue humaine, les tâches en file, les délais de refroidissement et les reconstructions d’infrastructure.

L’arrêt couvre les preuves suffisantes, les plateaux, les limites de capacités, les besoins de permission ou les cas où la prochaine étape utile dépend d’une personne ou d’un système externe.

Consultez [Comment fonctionne Harneloop](../framework-process.md) pour la boucle complète d’évolution centrée sur les artefacts.
