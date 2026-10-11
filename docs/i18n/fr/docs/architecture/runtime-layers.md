<a id="runtime-layers"></a>
# Couches d’exécution

<a id="current-decision"></a>
## Décision actuelle

Utiliser Python pour la première implémentation de référence.

Préférer Rust à Go plus tard si Harneloop nécessite un runtime natif protégé.

<a id="why-rust-later"></a>
## Pourquoi Rust plus tard

La couche native ne devrait exister que si le framework nécessite des garanties locales plus fortes concernant :

- l’intégrité du cycle de vie ;
- les limites de l’état protégé ;
- les instantanés de versions ;
- le retour arrière ;
- le stockage adressé par contenu ;
- l’empaquetage des artefacts ;
- la surveillance des fichiers ;
- la supervision des sous-processus ;
- la distribution desktop.

Rust convient mieux que Go à ce rôle de noyau protégé pour ce type de produit.

<a id="agent-boundary"></a>
## Limite de l’agent

Rust ne doit pas devenir l’espace de conception ouvert du harness pour l’agent.

Les agents devraient continuer à travailler via :

- des instructions Markdown ;
- des manifestes YAML et JSON ;
- des schémas ;
- des répertoires de candidats ;
- des commandes CLI ;
- des contrats d’artefacts.

La règle reste :

> Les agents peuvent explorer librement dans les candidats. Le moteur contrôle la promotion.

<a id="where-go-could-still-fit"></a>
## Où Go pourrait encore convenir

Go reste un bon candidat pour de futurs services hébergés, la coordination de workers distants ou l’infrastructure de registre si Harneloop évolue dans cette direction.
