# Validation scolaire et périmètre des preuves

État documentaire du 3 novembre 2026. Pour installer et vérifier la démonstration actuelle, suivre le [guide scolaire](../../LIVRAISON_SCOLAIRE.md). Ce document résume des résultats obtenus ; il ne transforme pas des archives internes en pièces publiées ni des propositions en vérifications exécutées.

## Version et fonctionnement

Les sources techniques proviennent de la version scolaire validée. La livraison adapte le repli visuel et le test des documents privés, puis vérifie ces changements de façon ciblée. La branche de livraison prévue est `feature/frontend-api-integration`. Aucune installation MySQL ni ouverture publique de l'application n'est certifiée.

Le modèle actuel comporte dix tables et treize clés étrangères. Le site propose histoires et Cold Cases, commentaires, signalements contextualisés, likes individuels sur les dossiers et commentaires compatibles, session partagée et déconnexion, propositions en attente, théories, administration, bannissement des membres, archivage/restauration et suppression conditionnelle des dossiers archivés. Les sept compteurs proviennent des lectures serveur et des lignes SQL ; ils ne sont pas renseignés artificiellement.

Les propositions ne sont pas publiées automatiquement. Les anciens compteurs de likes incompatibles restent protégés : aucun auteur de clic historique n'est inventé. Les révisions Alembic sont candidates ; leur présence dans Git ne prouve pas leur application à une base existante.

## Résultats séparés

| Campagne | Résultat attesté | Limites |
|---|---|---|
| 6G.5, historique | 854 tests : 311 backend, 513 frontend, 30 lanceur ; recette Edge distincte | Ni 854 essais navigateur, ni preuve MySQL ; harnais et reçus bruts conservés en interne |
| 6H.2, historique | Installation dans une copie et un venv neufs sur le même PC, SQLite synthétique ; 43 échanges WSGI et 71 échanges HTTP | Aucun autre PC ou système certifié ; parcours distinct de 6G.5 |
| 6H.4, documentaire | Trois diagrammes rendus et contrôlés ; sources Mermaid, SVG et PNG conservés | Pas une validation automatique de l'hébergement GitHub |
| 6H.7, depuis Git | 102 fichiers de HEAD exportés, venv neuf Windows/Python 3.13.0 AMD64, roues locales vérifiées, installation hors ligne et pip check PASS | Aucun téléchargement, pas d'ancien venv réutilisé ; interpréteur et roues nécessaires hors Git |
| 6H.7, fonctionnel | Dix pages, vingt ressources du kit, six chemins refusés ; 43 requêtes WSGI, sept groupes PASS ; sept gardes à zéro | Sans serveur en écoute ni navigateur ; SQLite mémoire uniquement |
| 6H.8/6H.9 | Identité des objets techniques rapprochée des preuves antérieures ; préparation documentaire | Pas de nouvelle campagne applicative ni nouvelle recette humaine |

Le parcours WSGI contrôle inscription/connexion, histoires et Cold Cases, commentaire, signalement, ajout/retrait/réajout des likes, unicité et CSRF, refus d'un ancien compteur incompatible, rollback, administration, archivage/restauration et bannissement. Les sept valeurs rapprochées de SQL sont, pour ce scénario uniquement : 2 dossiers, 1 résolu, 1 Cold Case, 4 utilisateurs, 2 commentaires, 1 signalement, 0 proposition en attente. Ne pas les comparer aux valeurs d'une autre campagne comme si le jeu de données était identique.

La suppression définitive, les cas de concurrence MySQL et tous les scénarios visuels ne sont pas rejoués dans ces 43 requêtes. Les tests de migrations synthétiques et leurs exclusions historiques ne deviennent pas une validation DDL réelle. Ne pas lancer une découverte générale de tests sans vérifier son isolation.

## Lire les supports et leurs archives

Les quatre fiches conservent leurs 76 questions historiques et leurs compléments. Certaines sections décrivent des versions antérieures : neuf tables, fonctions autrefois absentes, campagnes de 439 ou 657 tests. Le guide et le présent état priment pour décrire la démonstration actuelle. Une commande dans une section historique n'est pas une instruction de lancement du jour J.

Les références signalées « archive interne non livrée » indiquent une pièce conservée localement, sans lien brisé ni promesse que le lecteur la possède. Les reçus bruts, chemins personnels, scripts ponctuels et accès privés ne sont pas nécessaires au fonctionnement de la version scolaire et ne sont pas publiés automatiquement. Ce résumé est une restitution des contrôles, pas une reproduction de toutes leurs preuves brutes.

## Diagrammes

| Sujet | Source | Rendu SVG | Rendu PNG |
|---|---|---|---|
| Architecture | [Mermaid](preuves-lot6h4/diagrammes/diagram-1.mmd) | [SVG](preuves-lot6h4/diagrammes/diagram-1.svg) | [PNG](preuves-lot6h4/diagrammes/diagram-1.png) |
| Relations | [Mermaid](preuves-lot6h4/diagrammes/diagram-2.mmd) | [SVG](preuves-lot6h4/diagrammes/diagram-2.svg) | [PNG](preuves-lot6h4/diagrammes/diagram-2.png) |
| Séquence | [Mermaid](preuves-lot6h4/diagrammes/diagram-3.mmd) | [SVG](preuves-lot6h4/diagrammes/diagram-3.svg) | [PNG](preuves-lot6h4/diagrammes/diagram-3.png) |

## Périmètre de livraison

La copie de livraison utilise un SVG géométrique créé pour elle. Le test de non-publication des documents privés utilise une fixture synthétique temporaire ; il ne dépend d'aucun document interne.

Les notices visibles ne constituent pas une politique RGPD définitive. Le projet est une démonstration scolaire locale. Les conditions d'une exploitation publique restent à valider séparément. Les détails d'organisation privée ne font pas partie de cette documentation.
