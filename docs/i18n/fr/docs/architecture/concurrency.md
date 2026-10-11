<a id="concurrency-and-file-safety"></a>
# Concurrence et sécurité des fichiers

Les agents peuvent lancer les commandes Harneloop rapidement à la suite ou en parallèle. Toute commande qui lit un fichier de contrôle, calcule un ID séquentiel et réécrit le fichier doit protéger toute cette section lecture-modification-écriture.

<a id="current-rule"></a>
## Règle actuelle

- Utilisez un fichier de verrou de l’unité de harness pour les sections partagées du cycle de vie.
- Relisez le fichier YAML ou JSON concerné sous le verrou.
- Allouez le prochain ID séquentiel sous le verrou.
- Écrivez YAML et JSON par remplacement atomique d’un fichier temporaire.
- Ne libérez le verrou qu’après la mise à jour complète du fichier.

<a id="implemented-locks"></a>
## Verrous implémentés

- `runs` : alloue les ID d’exécutions.
- `run-<id>` : ajoute des artefacts et termine une exécution.
- `attempts` : alloue les ID de tentatives.
- `attempt-<id>` : ajoute des observations aux tentatives.
- `candidates` : alloue les ID de candidats.
- `candidate-<id>-evidence` : alloue les ID de preuves.
- `lifecycle` : promeut les candidats et restaure des versions antérieures.
- `state` : actualise `.evolve/state.json` et les fichiers d’état dérivés.

Les verrous résident dans `.evolve/locks/`, un état d’exécution géré par le framework et exclu des paquets portables.

<a id="rust-runtime-note"></a>
## Note sur le runtime Rust

Cela ne nécessite pas encore Rust. Les verrous de fichiers Python et le remplacement atomique suffisent pour la CLI alpha. Un futur runtime Rust pourra gérer une isolation plus stricte, la supervision des processus et une coordination concurrente des fichiers plus fiable, une fois le produit stabilisé.
