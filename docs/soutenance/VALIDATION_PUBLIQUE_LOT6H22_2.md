# Validation publique de la candidate — lot 6H.22.2

4 novembre 2026. Cette version est préparée hors du dépôt original et n’est pas encore publiée sur main. Les résultats ci-dessous ne prouvent ni déploiement public, ni MySQL, ni conformité RGPD définitive.

## Contrôles confirmés sur la copie

| Campagne de ce lot | Résultat | Limite |
|---|---|---|
| Tests RGPD distribuables | 13 réussis | Notices/formulaires et fichiers synthétiques temporaires, sans brouillon réel ni serveur. |
| Frontend complet | 590 réussis, zéro ignoré | DOM et transport simulés ; aucune nouvelle recette Edge. |
| Backend ciblé | 72 réussis, zéro ignoré | CSRF, likes et purge ; SQLite mémoire avec FK ; aucune base persistante. |
| Sondes du kit | Sept catégories de refus confirmées | Refus avant accès privé, écriture, réseau, SQL fichier, migration ou sous-processus ; pas un parcours complet. |

Ces campagnes sont distinctes et ne sont pas additionnées à un total historique. Les anciennes preuves des fiches gardent leur date et leur périmètre. Les rapports détaillés de préparation restent hors du dépôt distribué.

## Commandes de la copie publique

Après installation des dépendances dans une copie neuve :

```powershell
.\.venv\Scripts\python.exe -B -m unittest discover -s tests -p 'test_rgpd_information.py' -v
node --test 'frontend/tests/*.test.cjs'
.\.venv\Scripts\python.exe -I -B tools/valider_backend_isole.py --candidate-root . --suite test_csrf.py --suite test_likes.py --suite test_story_deletion.py
.\.venv\Scripts\python.exe -I -B tools/recette_lot6g4.py --probe-isolation
```

Le harnais cible exclusivement SQLite mémoire, active les FK, neutralise dotenv/Aiven, bloque le réseau et les sous-processus et refuse les écritures hors de son répertoire temporaire. Son rapport ne journalise pas les credentials. Aucun accès au serveur 5066 n’est requis.

Inventaire statique puis campagne backend complète proposée :

```powershell
.\.venv\Scripts\python.exe -I -B tools/valider_backend_isole.py --candidate-root . --liste
.\.venv\Scripts\python.exe -I -B tools/valider_backend_isole.py --candidate-root .
```

La campagne complète n’est pas annoncée réussie. Elle inclut les tests historiques de migrations ; ceux-ci ne sont pas masqués pour retrouver artificiellement un ancien total. Un échec doit être analysé et consigné avant publication. La validation ciblée du harnais ne démontre pas sa couverture exhaustive de tous les anciens scénarios.

## Documents internes et tests

Les tests publics vérifient les notices et créent leurs propres sondes temporaires, sans contenir ni lire de texte juridique interne. Les contrôles privés de structure des textes de préparation sont conservés séparément. Les décisions de responsable, contact, bases légales, conservation et droits restent à prendre avant ouverture publique.

Le code historique 6F.2 demeure consultable pour le référentiel pédagogique. Son manifeste est signalé comme archive non reproductible et n’est pas renouvelé pour prétendre le valider. Utiliser 6G.4 pour les contrôles actuels.

## Vérifications restantes

Installation complète depuis une copie neuve, campagne backend entière, parcours WSGI des catalogues, tests de persistance sur fichiers jetables et recette Edge restent des étapes distinctes. Ne pas utiliser les comptes ou la SQLite de démonstration existants. Les copies pédagogiques futures ne sont pas créées par ce lot.

Voir le [README principal](../../README.md), le [sommaire de soutenance](README.md) et les [tests RGPD publics](../../tests/test_rgpd_information.py).
