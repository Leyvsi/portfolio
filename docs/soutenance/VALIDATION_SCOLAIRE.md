# Validation scolaire et organisation des tests

État documentaire du 3 novembre 2026, après les lots 6H.11 et 6H.12. Le code `a850919` a été publié dans `Leyvsi/portfolio`, branche `feature/frontend-api-integration`. Le site reste une application locale non déployée publiquement. Le [guide scolaire](../../LIVRAISON_SCOLAIRE.md) décrit l’installation et le kit ; le [guide technique](GUIDE_TECHNIQUE.md) décrit le code.

## Résultats effectivement obtenus

| Campagne | Contrôles exécutés et résultat | Portée et limites |
|---|---|---|
| 6G.5, historique | 854 tests réussis : 311 backend, 513 frontend, 30 lanceur ; recette Edge distincte | Les tests automatiques ne sont pas des tests navigateur ; pas de preuve MySQL |
| 6H.4, documentaire | Trois diagrammes rendus et contrôlés, sources Mermaid et rendus SVG/PNG conservés | Rendu local ; aucun rendu GitHub de 6H.13 attesté |
| 6H.7, reproductibilité | Copie depuis Git et venv neuf Windows AMD64/Python 3.13.0 ; installation hors ligne et `pip check` ; 43 requêtes WSGI en sept groupes réussis | SQLite mémoire ; sans serveur ni navigateur ; pas un autre ordinateur certifié |
| 6H.11, livraison | Installation neuve hors ligne et `pip check` ; 30 tests Python ciblés, 12 tests frontend d’images, 43 requêtes WSGI en sept groupes réussis ; sept gardes à zéro | Adaptations de livraison vérifiées ; aucune réexécution générale des 854 tests |
| 6H.11, GitHub | Après push normal, branche, commit, parent et arbre de 118 fichiers rapprochés de la copie testée | Publication du code confirmée ; aucun déploiement du site |
| 6H.12, Edge | Trois connexions par les formulaires et rôles vérifiés ; commentaire, likes ajoutés/retirés, signalement, administration et bannissement ; refus de Bob suspendu | Parcours ciblé sur données fictives, sans MySQL ni migration réelle |
| 6H.12, nouvelle séance | Trois comptes et trois connexions de nouveau vérifiés ; jeu mémoire neuf préparé pour la répétition | Accès éphémères propres à ce processus ; aucune garantie sur une séance future |
| 6H.13, documentation | Liens, références au code livré, commandes relues, diagrammes et sélection publique contrôlés | Aucun test applicatif relancé, aucun serveur ou compte recréé |

Ces campagnes se recouvrent : **ne pas additionner leurs résultats**. Les preuves brutes des contrôles sont conservées en interne ; ce document en restitue les résultats sans publier d’accès ni de sorties privées.

## Organisation des suites

| Emplacement | Outils et sujets |
|---|---|
| [backend/tests](../../backend/tests/) | `unittest`, client Flask et SQLite mémoire sous harnais : authentification, permissions/CSRF, commentaires/théories, likes, utilisateurs, propositions, signalements, archives et suppression |
| [frontend/tests](../../frontend/tests/) | Node.js `node:test` et `node:vm`, DOM/API simulés : formulaires, sessions, commentaires, likes, théories, dashboard, utilisateurs, archives, suppression et images |
| [tests](../../tests/) | Lanceur WSGI, notices et refus des documents privés, contrat du kit scolaire |
| [tools/recette_lot6g4.py](../../tools/recette_lot6g4.py) | Inspection isolée et parcours WSGI synthétique, sans navigateur par défaut |

Les fixtures JSON sont dans [frontend/tests/fixtures](../../frontend/tests/fixtures/). Exemples ciblés : [authentification](../../backend/tests/test_api_errors_stats_login.py), [CSRF](../../backend/tests/test_csrf.py), [parcours de modération](../../backend/tests/test_moderation_journey.py), [likes](../../backend/tests/test_likes.py), [signalements contextualisés](../../backend/tests/test_admin_report_context.py), [images frontend](../../frontend/tests/images.test.cjs) et [contrat du kit](../../tests/test_recette_lot6g4.py).

## Commandes et isolation

Pour une nouvelle recette autorisée, la commande publique reproductible est celle du [guide scolaire](../../LIVRAISON_SCOLAIRE.md#recette-automatique-distincte). Elle n’est pas nécessaire pour finaliser la documentation et n’a pas été relancée en 6H.13.

Les campagnes backend historiques utilisaient des harnais inspectés : dotenv neutralisé avant import, paramètres Aiven vides, bases hors SQLite mémoire et accès interdits bloqués. Les seules options `-I -B` ne fournissent pas ces protections. Les enveloppes ponctuelles et leurs chemins privés ne sont pas des outils livrés ; ne pas lancer une découverte générale de tests ou importer l’application avec une configuration distante pour reproduire leurs résultats.

Les tests JavaScript utilisent principalement un DOM/API simulé : ils exécutent les scripts réels, mais ne certifient pas le rendu CSS, le clavier ou l’accessibilité d’un vrai navigateur. La recette Edge 6H.12 est une preuve supplémentaire distincte.

## Jeux de données distincts

Le mode humain `--serve` génère trois comptes : un administrateur et deux membres. Son état initial est **2 dossiers / 1 résolu / 1 Cold Case / 3 utilisateurs / 0 commentaire / 0 signalement / 0 proposition en attente**. Le scénario Edge ajoute un commentaire et un signalement, puis peut bannir un membre. Le reçu initial n’atteste pas l’état après de nouvelles actions humaines.

Le mode automatique `--check-journey` crée aussi un quatrième compte synthétique pour vérifier l’inscription. Ses 43 requêtes couvrent notamment connexion/inscription, commentaires, signalements, likes, CSRF, rollback, administration, archivage/restauration et bannissement. Ses sept valeurs rapprochées de SQL sont propres à ce scénario : **2 / 1 / 1 / 4 / 2 / 1 / 0**.

La suppression définitive n’est pas rejouée dans les 43 requêtes ciblées ni dans le parcours 6H.12. Les tests de migrations synthétiques et leurs exclusions historiques ne deviennent pas une preuve d’application sur une vraie base.

## Ce qui reste non validé

- MySQL/Aiven en production, migrations d’une base existante, concurrence réelle et durabilité après redémarrage.
- Autres systèmes/interpréteurs, couverture exhaustive des navigateurs, rendu responsive et accessibilité complète.
- Déploiement public, exploitation réelle et conformité RGPD complète.
- Les accès de tout processus autre que les séances effectivement vérifiées.

## Diagrammes et ressources

L’[index des diagrammes](README.md#diagrammes) fournit les trois sources Mermaid et les six rendus SVG/PNG. La [provenance](PROVENANCE_RESSOURCES.md) décrit le SVG livré. Aucun original exclu, bilan interne ou fichier de console privée n’est requis pour lire ces documents.
