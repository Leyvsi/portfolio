# Lot 6D — statistiques administrateur

> Archive pédagogique datée : les résultats et descriptions ci-dessous concernent le lot indiqué. Les anciens repères de ligne ne décrivent pas la version candidate. Pour préparer la soutenance actuelle, consulter les quatre fiches et le référentiel reliés au sommaire.

[Sommaire](README.md) · [Tests](TESTS_ET_VALIDATION.md) · [Suivi des 22 remarques](SUIVI_REMARQUES_JURY.md) · [Index du code](INDEX_CODE_JURY.md) · [Oral](ORAL_JURY.md#21-comment-comptez-vous-les-propositions-en-attente-)

Développement autorisé le **30 octobre 2026**. Lot terminé pour le code et les validations automatisées ci-dessous, en attente de validation utilisateur. La recette navigateur 6A/6B reste reportée ; le verdict VM **NO-GO** est conservé.

## État Git initial et préservation

- Branche : `feature/frontend-api-integration`.
- HEAD : `07a9f03ea0a3bdad4a07066fdd7bab1997cc158b`.
- **36 fichiers suivis modifiés, 21 fichiers non suivis**, aucun changement indexé avant 6D.
- Instantané de 87 fichiers publics avant toute modification 6D, avec statut, index, contenus et empreintes des fichiers non suivis. Aucun fichier privé de configuration ni base réelle inclus.

Branche, HEAD et index sont conservés. Les changements 6D s'ajoutent au travail antérieur sans le réinitialiser. Backend applicatif, modèles, migrations, Swagger, `api.js`, `app.js`, `admin-users.js`, `admin-stories.js`, CSS et lanceur restent identiques à l'avant-6D. Les tests existants conservent leurs assertions sur les six compteurs ; leur DOM simulé accueille le septième. Les fichiers non suivis hors périmètre, dont `revision_code/mahamadou/backend/models.py`, `frontend/histoires-originales.json` et le CSV exemple, restent identiques.

## Indicateurs effectivement présents

| Indicateur | Source et calcul conservé ou ajouté |
|---|---|
| Dossiers | Nombre de lignes validées de `GET /stories`. |
| Histoires résolues | Classement existant de catégorie 1 via `getStoryCategory`. |
| Cold Cases | Classement existant de catégorie 2 via `getStoryCategory`. |
| Utilisateurs | `users` de `GET /stats`. |
| Commentaires | `comments` de `GET /stats`. |
| Signalements | `reports` de `GET /stats`, tous statuts confondus. |
| **Propositions en attente** | Nombre de lignes dont **`status === 'pending'`** dans `GET /proposals` administratif. |

`displayData` ajoute ce calcul à la même mise à jour que les six autres valeurs. Le registre `counters` inclut la nouvelle carte `admin-pending-proposals-count` ; `clearData` l'efface donc automatiquement. La carte réutilise `.panel` dans `.cards`, sans modification de navigation, filtres ou CSS.

Une liste validée sans attente donne **0**. Le chargement conserve **—** ; une erreur de lecture masque les données et remet toutes les valeurs à **—**. Un compteur de signalements peut différer du nombre de cartes si les réponses représentent des instants différents : aucune transaction globale entre GET n'est ajoutée. Ces chiffres reflètent le dernier chargement global, sans actualisation continue.

## Contrat API, statuts et modèle examinés

`GET /api/v1/proposals` existe déjà, protégé par `admin_required`. Le serveur relit le compte, refuse un visiteur (401), un lecteur ou un compte banni (403), et ne fait pas confiance à un rôle transmis dans la session. Le résultat est une liste triée par date de création décroissante, avec exactement **id, user_id, title, content, status, created_at, updated_at**. Les propositions ne sont pas ajoutées à l'API publique `/stats`, qui conserve seulement ses trois agrégats. Aucune nouvelle route ni évolution de contrat.

`getAdminProposals` valide déjà la liste, les identifiants, les textes et les dates avant le calcul. Le champ `Proposal.status` est un **String(20), non nul, défaut pending**, sans enum ni contrainte CHECK de statuts. `POST /proposals` impose explicitement `pending` et ignore un statut arbitraire envoyé par le client. L'affichage connaît aussi `approved` et `rejected` ; aucun parcours de changement de statut n'est ajouté. `resolved` et `dismissed` sont des libellés du tableau partagé avec les signalements, pas une nouvelle règle de proposition. Les autres chaînes restent exclues du compteur et affichées comme texte. Aucune valeur d'une base réelle n'a été consultée.

`Category.name` reste unique et non nul ; `Story.category_id` reste une FK obligatoire. Aucun enum de catégories ni garantie SQL liant les ids 1/2 à ces noms. Le classement frontend existant est conservé ; les autres catégories restent comptées dans le total et signalées comme inconnues.

Un archivage futur demanderait de définir quelles lignes chaque agrégat inclut, puis les lectures, permissions et contraintes associées. Aujourd'hui, aucun champ d'archive ni exclusion n'est ajouté. Une future pagination de `/proposals` imposerait également de revoir le calcul local : il ne faudrait pas présenter le nombre d'une page comme le total. Aucun développement 6C/6E.

La lecture `get_proposals` n'a pas de traitement SQL local dédié : une erreur remonte au traitement HTTP 500 de Flask et ne garantit pas un corps JSON. `apiRequest` gère aussi ce cas avec un message HTTP de secours ; aucune liste vide de remplacement n'est fabriquée. Le test backend provoque réellement cette erreur et le frontend conserve son erreur globale. Le contrat d'erreur existant reste inchangé.

## Protections conservées

- Contrôle strict `/me` avant les lectures et permissions serveur sur les routes privées.
- Même cycle groupé ; pas de zéro de secours en cas d'échec HTTP, réseau, JSON ou validation.
- Versions de requêtes et AbortController ; un ancien succès ou 403 ne remplace pas un chargement récent.
- Effacement des sept valeurs et panneaux au refus courant 401/403 et au départ de page ; nouveau contrôle après restauration du cache.
- `textContent`, catégories et slugs du panneau 6B, confirmation/CSRF/relecture et règles de bannissement 6A conservés.

La session n'est pas surveillée en continu. Les listes restent sans pagination. L'isolation des tests de code connus repose sur des gardes d'interpréteur inspectés ; elle n'est ni une VM ni une preuve de confinement d'un navigateur réel ou de code hostile.

## Tests réellement exécutés

| Suite | Résultat final | Preuve locale |
|---|---|---|
| Backend | **235 PASS**, 0 échec/erreur/ignoré | `attempt-2/backend.stdout.txt`, `backend.guard.json`. |
| Frontend | **318 PASS**, 0 échec/annulé/ignoré | `attempt-2/frontend.stdout.txt`, `attempt-2/frontend.node-guard.json`. |
| Lanceur | **8 PASS**, 0 échec/erreur/ignoré | `attempt-2/launcher.stdout.txt`, `launcher.guard.json`. |
| Total | **561 PASS, 0 FAIL final** | Nouvelle campagne, distincte des 533 historiques de 6B. |

**Huit nouveaux tests backend** : comparaison exacte de la fixture complète et de la réponse réelle, autres chaînes de statut conservées, liste vide 200, accès visiteur/lecteur/banni et rôle falsifié refusés, agrégats publics inchangés, invariance des neuf tables après les GET, création imposant pending et erreur SQL donnant 500 plutôt qu'une liste vide.

**Vingt nouveaux cas frontend** : zéro/une/plusieurs attentes et autres statuts, chaînes proches exclues, attente de toutes les lectures, rafraîchissement échoué après succès (500/réseau/JSON/statut absent ou numérique), ancien succès/403 ignoré et actualisation recalculée. La fixture gelée reste intacte ; aucune écriture ni requête supplémentaire pour le compteur. Les tests existants nettoient désormais les sept valeurs et vérifient toujours rôles, erreurs, départ/retour. Les suites 6A/6B passent également : perte d'accès depuis le panneau utilisateurs, filtres, bannissement et conservation du compteur.

La [fixture propositions](../../frontend/tests/fixtures/admin-proposals.json) contient uniquement quatre propositions fictives, dont deux pending, une approved et une rejected. Le backend vérifie les sept champs contre le vrai sérialiseur, en SQLite mémoire. Cela relie les simulations frontend au contrat existant sans consulter de base réelle. Les écritures de préparation et le POST de test se déroulent seulement dans cette base en mémoire ; les lectures statistiques ne modifient aucune des neuf tables.

## Harnais inspecté, incidents et preuves

Dossier neuf sous `$env:TEMP` : **`portfolio-lot6d-20261030-vz20got1`**. Il est distinct de la préparation navigateur 6A/6B et n'utilise aucun de ses scripts de serveur, Edge ou pare-feu.

Les gardes Python/Node ont été lus avant exécution. Le manifeste autorise 55 fichiers de code/fixtures publics et en conserve les SHA-256 ; le contrôleur refuse une source différente avant les suites. Le bootstrap minimal vide les variables Aiven, fixe SQLite `:memory:` et neutralise dotenv avant import. Il bloque bases fichier/MySQL, ATTACH/DETACH, sockets/DNS, sous-processus, lectures privées et écritures dans le dépôt. Node bloque les appels réseau et sous-processus réels ; `fetch` est simulé dans chaque contexte de test.

Les sondes vérifient des refus **avant entrée/sortie**, sans ouvrir `.env`, créer de base fichier ou essayer de connexion réseau. Leurs compteurs volontairement positifs sont séparés des suites. Au passage final, **tous les compteurs interdits sont à zéro**. Flask est appelé via son client WSGI, sans serveur ni port ouvert. Le lanceur est simulé. Aucun Edge réel.

```powershell
# $preuves6d : dossier temporaire ci-dessus, inspecté avant lancement.
& .\.venv\Scripts\python.exe -I -B (Join-Path $preuves6d 'run-checks.py') --inspect
& .\.venv\Scripts\python.exe -I -B (Join-Path $preuves6d 'run-checks.py')
```

Les argv exacts sont archivés dans `attempt-2/commands.json` : sondes Python/Node, backend, sept suites Node avec `--require node-offline-guard.cjs --test --test-isolation=none`, puis lanceur. Sources du harnais, manifeste et copies par tentative, stdout/stderr, gardes et reçus sont conservés hors dépôt.

La préparation a d'abord interrompu son remplacement contrôlé sur un motif trop large ; le motif a été précisé avant tout lancement de suite. Au premier passage des suites, les 235 assertions backend passent, mais deux tentatives de lecture implicite du formateur de traceback SQL sont bloquées : ce passage est **FAIL de sécurité**, non retenu. Le journal de cette erreur volontaire est ensuite intercepté et son appel vérifié dans le test, sans changer le traitement HTTP 500. Le frontend donne 294 PASS / 24 FAIL, dus à une réponse simulée de propositions sans date ; le DTO fictif est complété. La console du contrôleur ne pouvait imprimer les symboles Unicode et a empêché le lancement du lanceur au premier passage : sa sortie est fixée en UTF-8. Aucun garde n'est assoupli. Le manifeste n'accepte que les deux fichiers de tests réinspectés, avec reçu explicite `manifest-review-2.json`. Le deuxième passage exécute les trois suites avec succès ; les anciens journaux sont conservés.

## Documentation et limites

README principal/frontend, documentation administrateur, démonstration proposée, tests/résultats, sécurité, matrice des 22 remarques, index et quatre fiches orales actualisés. Une réponse orale 21 distingue les rôles des trois membres. Les **76 questions et réponses courtes historiques** sont conservées, avec complément 6D. Les six blocs Mermaid sont inchangés ; aucun rendu revendiqué.

**NON EXÉCUTÉ :** navigateur réel, rendu responsive/clavier, recette intégrée 6A/6B, persistance sur base fichier après redémarrage, MySQL/Aiven, migrations appliquées et déploiement. Les tests DOM ne prouvent pas ces points. La grille responsive est seulement réutilisée et vérifiée statiquement. Aucune VM n'est installée, créée ou démarrée ; aucun changement Windows, pare-feu ou politique PowerShell.

<!-- CONTROLES_6D_START -->

Contrôles statiques finaux : **PASS**. 1 fichier Python analysé/compilé en mémoire, 4 JavaScript/CJS vérifiés par `node --check`, **25 opérations API** inchangées et cohérentes avec OpenAPI ; **76 questions/réponses courtes historiques conservées**, **six blocs Mermaid inchangés**, **155 repères** dont les 151 cibles héritées recalculées et quatre ajouts. **752 liens internes dans 19 Markdown**, dont 236 liens de lignes, contrôlés localement sans consultation externe. Matrice de **22 remarques** conservée. Branche, HEAD, index et fichiers hors périmètre préservés ; `diff --check` avec prise en compte des CRLF passe. Les SHA-256 des 55 sources testées correspondent au manifeste archivé du passage final. Reçus hors dépôt : `final-validation.json`, `documentation-updates.json`, `file-inventory.json` et `final-harness-inspection.json`.

<!-- CONTROLES_6D_END -->

**Aucun accès à une base réelle, aucune lecture du `.env` privé, aucune donnée réelle copiée ou modifiée, aucune migration, aucun commit ni push, aucune branche changée. Le lot 6D attend la validation utilisateur ; aucune suite de lot n'est commencée.**

## Inventaire exact du lot 6D

19 fichiers préexistants modifiés :

```text
README.md
docs/soutenance/ARCHITECTURE_SECURITE_RGPD.md
docs/soutenance/BILAN_ETAPE5.md
docs/soutenance/DEMONSTRATION.md
docs/soutenance/INDEX_CODE_JURY.md
docs/soutenance/ORAL_JURY.md
docs/soutenance/README.md
docs/soutenance/SUIVI_REMARQUES_JURY.md
docs/soutenance/TESTS_ET_VALIDATION.md
docs/soutenance/fiche-commune.md
docs/soutenance/fiche-mahamadou.md
docs/soutenance/fiche-melissa.md
docs/soutenance/fiche-sylvie.md
frontend/README.md
frontend/admin-dashboard.html
frontend/admin-dashboard.js
frontend/tests/admin-dashboard.test.cjs
frontend/tests/admin-stories.test.cjs
frontend/tests/admin-users.test.cjs
```

Trois fichiers créés :

```text
backend/tests/test_admin_pending_stats.py
frontend/tests/fixtures/admin-proposals.json
docs/soutenance/BILAN_LOT6D.md
```
