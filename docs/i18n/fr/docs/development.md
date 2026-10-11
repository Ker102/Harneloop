<a id="development"></a>
# Développement

<a id="repository-layout"></a>
## Organisation du dépôt

```text
src/harneloop/      Python reference implementation
tests/           Unit and behavior tests
docs/            Architecture and development notes
schemas/         Language-neutral data contracts
.github/         CI and repository automation
```

<a id="local-verification"></a>
## Vérification locale

Installez une fois la copie de travail comme outil modifiable au niveau utilisateur :

```powershell
uv tool install --editable .
```

La commande `harneloop` reste alors disponible hors du dépôt tout en reflétant les modifications du code source. Lancez les vérifications avec :

```powershell
uv run python -m compileall src tests
uv run python -m unittest discover -s tests
harneloop doctor
```

<a id="devops-baseline"></a>
## Base DevOps

Le dépôt doit maintenir :

- une organisation du code source avec `src/` ;
- des tests locaux reproductibles ;
- une CI pour les versions de Python prises en charge ;
- aucun environnement virtuel ni artefact d’exécution versionné ;
- une documentation explicite sur la sécurité et les contributions ;
- des schémas indépendants du langage pour les enregistrements fondamentaux.

<a id="runtime-data"></a>
## Données d’exécution

Les traces d’exécution, artefacts copiés, enregistrements d’exécutions, plans de tentatives et expériences sont des données de travail locales. Ils ne doivent pas être inclus dans les paquets portables thin, sauf si un profil ultérieur les prévoit explicitement.

<a id="pr-review-note"></a>
## Note sur la revue des PR

Une revue CodeRabbit n’est pas nécessaire pendant le prototype initial. Si un PR est créé, ajoutez le tag ou label CodeRabbit-ignore configuré.
