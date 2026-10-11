<a id="contributing"></a>
# Contribuer

Harneloop est actuellement en alpha publique. Les signalements et contributions ciblés sont bienvenus pendant la stabilisation de l’API publique et des formats des unités de harness.

<a id="development-setup"></a>
## Environnement de développement

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -e .
.\.venv\Scripts\python -m unittest discover -s tests
```

Sur macOS ou Linux :

```bash
python3 -m venv .venv
./.venv/bin/python -m pip install -e .
./.venv/bin/python -m unittest discover -s tests
```

<a id="pull-requests"></a>
## Pull requests

Limitez chaque pull request à un comportement ou à une partie de l’architecture.

Ouvrez une issue avant tout travail architectural important afin de convenir du problème et de son impact sur la compatibilité. Ajoutez des tests pour les changements du cycle de vie et mettez à jour la documentation destinée aux agents lorsque le comportement change.

Pour le moment, ne demandez pas de revue automatisée CodeRabbit. Si un PR est créé alors que CodeRabbit est configuré, ajoutez le label ou le tag CodeRabbit-ignore du dépôt avant de demander une revue.

<a id="standards"></a>
## Règles

- Gardez le cœur du framework indépendant de la famille de tâches.
- N’ajoutez pas d’hypothèses propres à Blender dans `src/harneloop`.
- Ajoutez ou actualisez les tests du comportement du cycle de vie.
- Gardez les fichiers destinés aux agents lisibles en Markdown, YAML ou JSON.
- Ne commitez pas de secrets, d’artefacts d’exécution locaux, d’environnements virtuels ou de paquets générés.

En contribuant, vous acceptez que votre contribution soit publiée sous la [Apache License 2.0](../../../LICENSE) du dépôt.
