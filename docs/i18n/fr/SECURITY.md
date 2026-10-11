<a id="security"></a>
# Sécurité

Harneloop est un framework privilégiant le fonctionnement local pour les unités de harness construites par des agents. Les limites de sécurité sont importantes, car les agents peuvent créer des outils, exécuter des commandes et empaqueter des unités réutilisables.

<a id="current-status"></a>
## État actuel

Il s’agit d’une alpha publique précoce. Ne considérez pas Harneloop ni une unité de harness comme un bac à sable renforcé ou une limite de sécurité.

<a id="rules"></a>
## Règles

- Ne stockez jamais de secrets dans les unités de harness.
- N’empaquetez pas par défaut les fichiers `.env`, clés privées, identifiants, caches ou traces d’exécution brutes.
- Traitez les outils de candidats générés comme non fiables tant qu’ils n’ont pas été inspectés.
- Utilisez les commandes du framework pour la promotion, le retour arrière et l’empaquetage.
- Exigez l’approbation explicite de l’utilisateur avant toute action destructive.

<a id="reporting"></a>
## Signalement

Ne divulguez pas de vulnérabilités suspectées dans une issue publique. Utilisez le formulaire privé de signalement de vulnérabilités de GitHub s’il est disponible pour ce dépôt. Sinon, contactez le propriétaire en privé via le profil GitHub lié, en précisant les étapes de reproduction, les versions affectées et l’impact potentiel.
