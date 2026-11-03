# Frontend scolaire

HTML, CSS et JavaScript sans compilation. Suivre le [guide scolaire](../LIVRAISON_SCOLAIRE.md) pour utiliser le kit SQLite mémoire.

Les dix pages couvrent accueil, listes d'histoires et Cold Cases, dossier, inscription, connexion membre/admin, proposition, théories et dashboard. Toutes partagent les contrôles de session.

| Module | Rôle |
|---|---|
| [api.js](api.js) | JSON, cookies, CSRF, délais et erreurs |
| [app.js](app.js) | Listes, recherche, dossier, formulaires et session |
| [comments.js](comments.js) | Commentaires et signalements |
| [likes.js](likes.js) | Likes individuels et relecture serveur |
| [theories-list.js](theories-list.js) | Théories publiques |
| [admin-users.js](admin-users.js) | Consultation et bannissement des membres |
| [admin-stories.js](admin-stories.js) | Dossiers, archives et suppression conditionnelle |
| [admin-dashboard.js](admin-dashboard.js) | Sept compteurs et coordination des panneaux |

Le texte reçu est affiché avec `textContent`. Le backend reste responsable des permissions. Les écritures ne sont pas automatiquement répétées après une réponse incertaine.

Les images utilisent une URL HTTP(S) fournie par l'API, puis le [SVG local](images/default-story.svg). Un échec final produit « Image indisponible », sans boucle. Les schémas actifs sont refusés. La [provenance](../docs/soutenance/PROVENANCE_RESSOURCES.md) et les [règles d'affichage](images/README.md) sont documentées.

Les [tests frontend](tests/) utilisent Node, des DOM et API simulés ; ils ne constituent pas une recette visuelle. Le test ciblé des images se lance avec `node --test frontend/tests/images.test.cjs` depuis la racine. Les tests et limites de la livraison sont résumés dans la [validation](../docs/soutenance/VALIDATION_SCOLAIRE.md).

Les propositions restent en attente ; publication automatique, pièces jointes, récupération du mot de passe et pagination ne sont pas livrées. La démonstration est locale et synthétique ; aucune politique de confidentialité finale n'est publiée par cette documentation.
