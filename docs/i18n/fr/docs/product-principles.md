<a id="product-principles"></a>
# Principes du produit

Harneloop est l’identité produit retenue. L’architecture reste indépendante de tout benchmark ou famille de tâches particulière.

<a id="what-this-is"></a>
## Ce que c’est

Harneloop est un framework que les agents utilisent pour construire et améliorer le harness qui les entoure ou qui entoure un autre agent cible.

Le framework doit aider les agents à :

- effectuer des tentatives de tâches ;
- inspecter des artefacts réels ;
- rattacher les échecs aux exécutions ;
- maintenir une carte opérationnelle locale de l’unité avec workflow, preuves, hypothèses sur l’environnement et questions ouvertes ;
- identifier les capacités manquantes de l’agent opérateur séparément des outils de l’unité ou de l’agent cible ;
- rechercher et réutiliser des outils, skills, bibliothèques, jeux de données, exemples et travaux antérieurs adaptés ;
- proposer des correctifs candidats du harness ;
- tester les correctifs candidats ;
- ne promouvoir que des améliorations étayées par des preuves ;
- empaqueter des unités de harness portables.

<a id="what-this-is-not"></a>
## Ce que ce n’est pas

Harneloop n’est pas :

- un tableau de bord générique d’évaluation ;
- un framework de graphes d’agents figés ;
- un système propre à Blender ;
- un système d’entraînement ou de fine-tuning de modèles ;
- un simple dossier de prompts sans cycle de vie.

<a id="core-design-tension"></a>
## Tension centrale du design

Le système est conçu pour des modèles d’IA générative : il doit donc laisser place au raisonnement et à l’exploration. En même temps, le framework doit protéger l’intégrité du cycle de vie.

La règle :

> Les agents peuvent explorer librement dans les candidats. Le moteur contrôle la promotion.

`operational-map.md` conserve la compréhension de travail actuelle de l’agent sur une unité de harness sans la transformer en script figé. L’agent doit s’en servir pour s’orienter, l’actualiser avec les preuves et continuer à raisonner à partir de la tâche et des artefacts actuels.

Le framework ne doit pas supposer que l’agent qui construit une unité de harness est tout-puissant. Les capacités manquantes de l’agent opérateur doivent être identifiées, justifiées par des preuves ou une amélioration attendue claire et traitées dans les limites de permission appropriées avant d’ajouter outils, dépendances, identifiants, services payants ou accès externe élargi.

Harneloop vise les meilleures performances de tâche vérifiées, pas la reconstruction de toutes les capacités. L’agent opérateur doit examiner les solutions existantes et peut les adopter, adapter, combiner ou en tirer des enseignements si elles améliorent le harness. La réutilisation doit rester inspectable : consigner quoi et pourquoi, vérifier compatibilité et valeur observée, respecter licences et attribution, et appliquer les permissions habituelles pour sécurité, identifiants, accès externe, coût ou changements importants d’infrastructure.
