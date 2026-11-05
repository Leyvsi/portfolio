# Lot 6G.3 — audit d’intégration et fiabilité des likes

> Archive pédagogique datée : les résultats et descriptions ci-dessous concernent le lot indiqué. Les anciens repères de ligne ne décrivent pas la version candidate. Pour préparer la soutenance actuelle, consulter les quatre fiches et le référentiel reliés au sommaire.

> Copie publique de référence : les chemins personnels et liens de travail internes sont retirés. Les preuves et commandes historiques gardent leur date et leur périmètre ; utiliser le README actuel pour le lancement.

[Bilan 6G.2](BILAN_LOT6G2.md) · [Conception 6G.1](BILAN_LOT6G1.md) · [Bilan 6F.2](BILAN_LOT6F2.md)

**1er novembre 2026. Audit local uniquement. 803 tests de référence réexécutés et réussis, neuf contrôles complémentaires réussis, parcours intégré de 79 requêtes réussi. Aucune correction applicative ou de migration effectuée. NO-GO en l’état pour la recette navigateur avec base de test isolée : le kit disponible est obsolète et le périmètre des scripts des pages de compte reste incomplet.**

Ce verdict porte sur la préparation opérationnelle de la recette, pas sur un échec constaté des likes dans les essais isolés. Aucun Edge, serveur HTTP/Flask en écoute, CDP, MySQL/Aiven ou base réelle utilisé. L’application Flask est exercée uniquement par client WSGI de test, sans port ouvert. Arrêt après ce rapport, en attente de validation.

## 1. État Git, périmètre et fichiers examinés

Bilans 6G.2, 6G.1 et 6F.2 lus intégralement. Aucun `AGENTS.md` trouvé dans le dépôt ou les parents contrôlés. Les consignes de préservation, d’exclusion et d’isolation décrites par ces bilans sont conservées. Les sept exclusions antérieures — `donnees.js`, `histoires-originales.json`, CSV de comptes et quatre images WebP — restent non lues/non exécutées ; même exclusion pour les secrets, `.env`, cookies, certificats et bases privées.

Branche initiale : `feature/frontend-api-integration`. HEAD : `07a9f03ea0a3bdad4a07066fdd7bab1997cc158b`. État initial : **46 fichiers suivis modifiés, 69 fichiers non suivis, aucun indexé**. Ces modifications viennent des lots précédents ; le diff contre HEAD ne permet pas de les attribuer toutes à 6G.2.

Les **38 fichiers propres à 6G.2** ont été identifiés par comparaison avec sa sauvegarde `before/`, son manifeste initial et son reçu final : **31 fichiers préexistants modifiés, sept créés**. Leurs empreintes actuelles correspondent toutes au reçu final 6G.2. Les différences ont été examinées séparément des changements plus anciens.

**Application et migration : 14 fichiers.**

```text
backend/models.py
backend/api/v1/swagger.json
backend/api/v1/views/__init__.py
backend/api/v1/views/comments.py
backend/api/v1/views/histoires.py
backend/api/v1/views/likes.py                         [créé]
backend/api/v1/views/story_deletion_support.py
frontend/api.js
frontend/app.js
frontend/comments.js
frontend/dossier.html
frontend/likes.js                                   [créé]
frontend/styles.css
migrations/versions/c6g200000001_add_comment_likes.py  [créé]
```

**Tests : huit fichiers.**

```text
backend/tests/test_admin_pending_stats.py
backend/tests/test_api_errors_stats_login.py
backend/tests/test_comments_theories.py
backend/tests/test_story_deletion.py
backend/tests/test_swagger.py
backend/tests/test_likes.py                          [créé]
backend/tests/test_comment_likes_migration.py         [créé]
frontend/tests/likes.test.cjs                        [créé]
```

**Documentation : 16 fichiers.**

```text
README.md
frontend/README.md
docs/soutenance/ARRET_CONDITIONNEL_LOT6C2.md
docs/soutenance/BILAN_LOT6C_AUDIT.md
docs/soutenance/BILAN_LOT6G2.md                       [créé]
docs/soutenance/CONCEPTION_LOT6C2_SUPPRESSION.md
docs/soutenance/DECISIONS_FINALES_LOT6C2.md
docs/soutenance/DEMONSTRATION.md
docs/soutenance/INDEX_CODE_JURY.md
docs/soutenance/README.md
docs/soutenance/SUIVI_REMARQUES_JURY.md
docs/soutenance/TESTS_ET_VALIDATION.md
docs/soutenance/fiche-commune.md
docs/soutenance/fiche-mahamadou.md
docs/soutenance/fiche-melissa.md
docs/soutenance/fiche-sylvie.md
```

Les quatre anciens documents de conception/suppression ne reçoivent que des mises à jour de liens de lignes. Les compléments des fiches distinguent contrat courant et réponses historiques. Les modifications des tests correspondent à dix tables, aux routes ajoutées et au passage du compteur de clics vers l’unicité du commentaire ; les assertions de conservation/rollback et les répétitions des likes de théories restent présentes.

Sources de support également contrôlées : permissions, validation/CSRF/session, visibilité des dossiers, vues et contrôleurs administratifs, tests historiques sélectionnés, `backend/index.py`, `run_local.py`, dépendances, kit et manifeste 6F.2. Les six migrations antérieures et `migrations/env.py` ont été examinés statiquement, jamais exécutés. **128 fichiers préexistants sont suivis par empreinte ; 46 fichiers Python passent l’analyse syntaxique AST.** Une empreinte ou une analyse syntaxique ne vaut pas audit fonctionnel intégral.

**Scripts temporaires hors dépôt.** Les harnais 6G.2 restent dans leur dossier de preuves d’origine. Pour 6G.3, des copies inspectées de `run-checks.py`, des gardes Python/Node, de `run-integration.py` et des workers WSGI/DOM sont utilisées dans un nouveau dossier temporaire. `audit-static.py` et `additional/audit_cases.py` y ajoutent inventaire et contrôles ciblés ; ils ne font pas partie des 38 fichiers livrés en 6G.2. Aucun de ces scripts n’est installé dans l’application.

## 2. Histoires et Cold Cases : fonctionnement réel

[histoires.py](../../backend/api/v1/views/histoires.py) et [likes.py](../../backend/api/v1/views/likes.py) utilisent réellement **Vote**. Un Cold Case est une Story ; les deux catégories suivent les mêmes règles. L’AST complet de Vote et les colonnes des neuf anciens modèles sont identiques à 6G.1. Les votes historiques ne sont ni convertis ni recréés.

| Opération sous `/api/v1` | Résultat vérifié |
|---|---|
| GET `/votes/{story_id}` | État du compte courant et COUNT des Vote de la cible ; 200 |
| POST `/votes/{story_id}` | Insertion avec l’utilisateur de session ; 201 ; doublon 409 |
| DELETE `/votes/{story_id}` | Suppression filtrée par cible **et** utilisateur courant ; 200 ; répétition `changed=false` |
| GET public de dossier | `votes` vient du comptage SQL ; aucun état personnel public |

Ajout, retrait, réajout, deux comptes/deux cibles, unicité SQL, relecture et conservation des anciens id/auteur/date sont couverts. Une archive rend ces opérations indisponibles en 404 et conserve les likes ; une restauration les retrouve. Le contrôle complémentaire fait ce parcours sur un Cold Case avec deux comptes. La purge supprime les likes du dossier et conserve ceux des autres dossiers.

Visiteur : 401 pour l’état personnel et les écritures ; banni : 403 ; compte disparu : 401 ; cible absente, archivée ou identifiant hors domaine : 404. Les corps clients ne choisissent ni auteur ni compteur. Après déconnexion réelle, l’écriture est refusée et le vote existant reste enregistré.

## 3. Commentaires, signalements et suppressions

Les trois méthodes de `/api/v1/comments/{comment_id}/like` utilisent **CommentLike**, avec couple SQL unique `(user_id, comment_id)`, deux FK obligatoires CASCADE et index sur `comment_id`. Le POST renvoie 200, un doublon 409, le retrait 200 et `changed=false` s’il était déjà absent. Un contrôle 6G.3 masque volontairement le précontrôle : le véritable INSERT heurte encore la contrainte SQL, donne 409 et ne crée aucune seconde ligne. C’est une simulation de précontrôle périmé, pas une course multi-connexions.

[comment_to_dict](../../backend/api/v1/views/comments.py) expose COUNT(CommentLike) uniquement lorsque le compteur physique historique est un entier exactement égal à zéro. La colonne `Comment.likes` reste intacte. Une valeur non nulle, négative ou incompatible reste historique, avec `likes_compatible=false` ; GET personnel/POST/DELETE sont refusés en 409 `LEGACY_LIKES_UNRESOLVED`. SQL NULL est également refusé par la migration. Aucun ancien nombre n’est remis à zéro, attribué à un compte inventé ou supprimé pour réussir un test.

Les essais vérifient l’association au bon commentaire, les deux comptes indépendants et les id de cibles distincts. Après suppression du commentaire, ses likes disparaissent par FK et les actions donnent 404. Le retrait d’un like ne supprime ni commentaire, ni compte, ni signalement.

Le contrôle complémentaire confirme les deux sens de la relation : supprimer des **Report** synthétiques conserve commentaire et likes ; supprimer ensuite le commentaire supprime ses Report et CommentLike, en conservant ceux de l’autre dossier. Aucune route de suppression individuelle des signalements n’a été ajoutée : cette vérification porte sur SQL/FK, pas sur une nouvelle action de dashboard.

La purge définitive suit CommentLike dans le graphe interne, l’empreinte signée, les contrôles d’orphelins/FK, le plafond de dépendances, les verrous, les DELETE et les contrôles finaux. Elle supprime ces enfants avant Comment. Changer un like invalide l’ancienne confirmation. Un échec après de vrais DELETE de likes annule les écritures non validées et conserve le dossier. Les cinq clés publiques d’impact/résultat restent `comments`, `theories`, `votes`, `updates`, `reports`.

## 4. Session, erreurs et frontend

Les auteurs sont déterminés par la session Flask ; le rôle ou l’id envoyés par le client ne donnent aucun droit. POST/DELETE passent le filtre CSRF existant ; GET personnel ne requiert pas de CSRF. Le frontend utilise `credentials: include`, le jeton obtenu par `/me` et des réponses personnelles `private, no-store`.

Dans [dossier.html](../../frontend/dossier.html), l’ordre est `api.js`, `likes.js`, `comments.js`, `app.js`. Le dossier est résolu par son vrai slug/id avant montage. Le contrôle d’histoire est sous le récit ; chaque carte de commentaire possède son propre contrôle. Les changements CSS 6G.2 sont limités à `.like-control` et reprennent le design existant. Aucune appréciation du rendu réel n’est déduite de la lecture CSS.

Les boutons natifs `type=button`, leurs libellés, `aria-pressed`, le statut vivant et le focus visible sont présents. Cela prépare l’usage clavier ; **Tab/Entrée/Espace, contraste, lecteur d’écran et rendu Edge restent à observer réellement**. Le visiteur garde le compteur public et reçoit une invitation à se connecter. Une valeur inconnue n’est jamais remplacée par un faux zéro.

Le verrou commence dès la vérification de session et couvre action/relecture. Les tests DOM couvrent les doubles clics à ces trois moments, le compte changé, la cible/confirmation incohérente, la déconnexion, les réponses tardives, les historiques protégés et la coordination avec commentaires/signalements. Le brouillon de commentaire est conservé ; la sélection d’un signalement bloque les likes jusqu’à annulation/envoi, sans changer silencieusement sa cible.

Le compteur affiché vient des réponses serveur, jamais d’un `+1/-1` supposé. Un 409 entraîne une lecture, pas un second POST. Erreur réseau, timeout, JSON invalide ou 5xx après envoi : résultat incertain, aucune réussite annoncée et aucune relance automatique. Une confirmation suivie d’une panne de relecture est explicitement distinguée. Les vrais commits suivis d’un accusé perdu sont couverts côté backend. Un rollback local après un commit accompli ne défait pas ce commit.

Limites conservées : le verrou d’incertitude ne survit pas au rechargement complet ; une lecture peut précéder la fin d’une écriture ; aucune révocation/synchronisation instantanée entre onglets n’est attestée. Les compteurs peuvent évoluer entre deux requêtes. Le nombre de lectures par commentaire mérite une mesure sur de longues listes ; aucun test de charge n’a été exécuté.

## 5. Références à `donnees.js` et préparation navigateur

Le fichier lui-même n’a été ni ouvert ni exécuté. Les balises des fichiers HTML autorisés établissent **cinq pages concernées**, et pas seulement les trois pages du parcours 6F.2 :

| Page | Ligne de la balise |
|---|---:|
| `frontend/connexion.html` | 45 |
| `frontend/admin-connexion.html` | 45 |
| `frontend/inscription.html` | 48 |
| `frontend/proposer-histoire.html` | 50 |
| `frontend/theories.html` | 64 |

`dossier.html` ne charge pas ce script. Les contrôleurs de likes relus n’y font pas appel. Le README frontend le décrit comme ancien jeu de données, mais cette description ne permet pas de certifier son contenu ou ses effets. Le parcours intégré omet explicitement ces balises sur les pages de compte ; il ne valide donc pas tous leurs scripts.

Le [kit 6F.2](../../tools/recette_lot6f2.py) présente deux obstacles techniques vérifiés statiquement : **16 empreintes ne correspondent plus aux sources**, et `likes.js` est absent à la fois de son manifeste et de sa liste de ressources publiques. Renouveler seulement les empreintes ne suffirait pas à servir le nouveau module. Aucun contournement ou renouvellement silencieux de ce kit n’a été effectué.

Pour une recette complète, il faut une décision explicite sur les références au script exclu : autoriser leur revue ou autoriser un retrait ciblé après analyse des dépendances. Une recette restreinte qui bloque ce fichier doit être acceptée comme telle et ne doit pas être présentée comme validation complète des pages.

## 6. Migration candidate et risques de données

[c6g200000001_add_comment_likes.py](../../migrations/versions/c6g200000001_add_comment_likes.py) dépend de `c6c200000001`. Seule cette candidate est exécutée sur SQLite synthétique mémoire. `env.py`, les six anciennes révisions et la chaîne Alembic complète ne sont pas exécutés. Les anciennes migrations examinées montrent notamment que la référence relationnelle Report et la révision de gestion Story sont des prérequis distincts.

| Vérification synthétique | Résultat |
|---|---|
| Schéma parent minimal, anciens compteurs zéro et Vote témoin | Candidate appliquée ; anciennes valeurs conservées ; unicité/FK actives |
| Prédécesseur complet synthétique de neuf tables, décrit sans jouer les anciennes révisions | Passage à dix tables ; lignes des neuf tables identiques ; vraie API commentaire fonctionnelle ensuite |
| SQL NULL, entier positif/négatif ou texte historique | Refus avant DDL ; ancien compteur conservé |
| Type parent non entier ou table déjà présente | Refus, sans écrasement |
| FK SQLite désactivées | Refus avant DDL ; schéma et valeur historique identiques |
| Suppression SQL commentaire/utilisateur sur table migrée | Cascade des likes ; témoins préservés ; absence d’orphelins |
| Downgrade avec likes existants | Refus sans perte ; table vide seule rétrogradable |

Le test à neuf tables part des métadonnées du prédécesseur attendu, pas d’une installation historique migrée depuis zéro. Il ne valide ni l’état ni la révision d’une base existante.

**Incident DDL reproduit en 6G.3 :** une erreur synthétique est injectée à `create_index`, après `create_table`. Après rollback, avec Python 3.13/SQLite du poste, `comment_likes` existe encore, sans index secondaire ; le compteur historique vaut toujours zéro et le Vote témoin garde son id 99. La relance est refusée car la table existe déjà. Ce contrôle réussit en constatant le risque, il ne prouve pas l’atomicité de la migration. Aucun nettoyage automatique n’est ajouté. Après un tel incident, arrêter, inventorier l’état atteint et faire autoriser la reprise ; ne pas supprimer aveuglément une table ni marquer la révision comme appliquée.

**Différences SQLite/MySQL à conserver dans les conclusions :** SQLite requiert `PRAGMA foreign_keys=ON`, n’impose pas les mêmes types physiques et ne prouve pas les verrous de ligne `FOR UPDATE`. Les tests sont en mémoire et ne démontrent aucune durabilité après redémarrage. Sur MySQL, la candidate vérifie FK actives et parents InnoDB, copie les types physiques des id parents et demande InnoDB pour la table créée ; cette branche n’a pas été exécutée. Types/signature des FK, index, transactions, DDL avec commits implicites, visibilité des COUNT, attentes/deadlocks et courses multi-connexions doivent être validés séparément sur un MySQL de test autorisé. **Une réussite SQLite n’est pas une validation MySQL/Aiven.**

Les prérequis avant migration sont : révision parente réellement confirmée, schéma/FK/unicités vérifiés, anciens écrivains arrêtés/drainés, inventaire sans cast des historiques, sauvegarde vérifiée et procédure de reprise. Tout historique non nul/invalide impose un arrêt et une décision humaine ; aucun choix de conversion n’est pris ici. `create_all` ne met pas à niveau une base existante. Déployer le backend actuel sans `comment_likes` peut faire échouer les lectures de commentaires et la purge : ce n’est pas un mode de compatibilité.

## 7. Dashboard et autres fonctionnalités

Les empreintes de `admin-dashboard.html`, `admin-dashboard.js`, `admin-users.js` et `admin-stories.js` sont identiques à l’avant-6G.2 et au début de cet audit. La CSS ajoutée cible les likes ; aucune carte administrative ajoutée.

Les sept indicateurs restent : dossiers actifs, histoires résolues, Cold Cases, utilisateurs, commentaires, signalements et propositions en attente. Aucun huitième compteur de likes. Dans le parcours intégré, leurs valeurs DOM sont toutes comparées aux SELECT de la mémoire synthétique : **2, 1, 1, 2, 2, 2, 0**. Ces nombres sont des résultats de cette fixture et de ses formulaires, jamais des constantes ajoutées au dashboard.

Les suites de listes utilisateurs, bannissement, signalements, propositions, archives/restaurations, purge, théories, images et lanceur passent. Le contrôle complémentaire bannit par la vraie route un compte possédant des likes : ses lignes restent conservées et GET/POST/DELETE de likes sont ensuite refusés en 403. Une suppression définitive entraîne normalement la baisse des nombres de commentaires/signalements concernés ; l’archivage change la liste des dossiers actifs sans effacer leurs contributions.

Les GET administratifs ne constituent pas un instantané transactionnel global ; l’égalité SQL/DOM observée sans écriture concurrente ne garantit pas tous les entrelacements possibles. Aucune absence de régression n’est revendiquée dans les scripts exclus ou le navigateur non exécuté.

## 8. Tests exécutés, résultats et preuves

Le manifeste **inchangé de 71 sources** de la dernière campagne 6G.2 correspond toujours aux sources actuelles. Gardes relus avant exécution : environnement enfant minimal, dotenv neutralisé avant import, six paramètres Aiven vides, connexion uniquement à SQLite `:memory:`, FK actives à chaque connexion, ATTACH/DETACH interdits. Réseau/DNS, sous-processus applicatifs, lectures privées, bases fichier/MySQL et écritures du dépôt sont bloqués. Seule la candidate peut utiliser les opérations Alembic ciblées sur `comment_likes` en mémoire. Les sondes de refus sont exécutées dans des processus séparés et ne sont pas comptées comme tests applicatifs.

| Vérification 6G.3 | Résultat final | Échecs / erreurs / ignorés |
|---|---:|---|
| Backend de référence, dont 18 méthodes likes et six candidate | **303 PASS** | 0 / 0 / 0 |
| Frontend de référence, dont 56 cas likes | **484 PASS** | 0 / 0 / 0 ; aucun annulé |
| Lanceur/HTML/WSGI | **16 PASS** | 0 / 0 / 0 |
| **Réexécution de la référence 6G.2** | **803 PASS** | Aucun cumul avec les résultats historiques |
| Contrôles complémentaires temporaires 6G.3 | **9 PASS** | 0 / 0 / 0 |
| Parcours continu contrôleurs réels → WSGI → SQL → DOM simulé | **79 requêtes, 14 groupes réussis** | Distinct des méthodes unitaires |

Les neuf contrôles complémentaires couvrent : doublon SQL malgré précontrôle manqué ; autre erreur d’intégrité renvoyée en 500 avec rollback ; indépendance suppression Report/CommentLike puis cascades ; bannissement avec conservation ; Cold Case archivé/restauré et deux comptes ; schéma complet neuf tables puis candidate/API ; FK désactivées refusées ; cascade utilisateur de la table migrée ; échec entre table et index. Une première sélection de huit contrôles a passé, puis un passage de neuf après ajout du scénario complet de migration ; les huit ne sont pas additionnés une seconde fois.

Le parcours intégré réexécuté utilise les vrais HTML et contrôleurs avec transport/DOM simulés : inscription/connexion, commentaire, ajout-retrait-réajout d’un like de dossier et de commentaire, relecture, signalement, vrai refus CSRF, réponses de commentaire/signalement perdues après commit, déconnexion et administration. SQL final : un Vote et un CommentLike appartenant au membre du test ; compteur physique historique zéro. Les cookies sont gérés par le client WSGI, ce qui ne valide pas leur comportement Edge.

**Tous les compteurs d’opérations interdites des suites, des neuf contrôles et du parcours intégré valent zéro.** Les six tests candidate de référence comptent six exécutions de module et dix opérations Alembic ciblées ; le passage complémentaire final en compte quatre et cinq. Aucun accès réel ni ancienne révision exécutée.

**Tests applicatifs échoués : aucun.** Un contrôle statique `git diff --check` brut signale les CR de fins de ligne de fichiers préexistants ; le même contrôle avec l’option ponctuelle `-c core.whitespace=cr-at-eol` réussit. Aucune configuration Git permanente ou fin de ligne n’est modifiée. Ce résultat est séparé des tests applicatifs.

**NON EXÉCUTÉS :** les six tests historiques de `test_report_migration.py` et le test de migration de `test_story_archiving.py`, soit sept tests exclus ; chaîne Alembic complète ; MySQL/Aiven ; vraie concurrence SQL multi-connexions ; Edge/HTTP/CDP ; rendu/clavier/lecteur d’écran/mobile réels ; durabilité après arrêt/redémarrage. Les cas séquentiels multi-utilisateurs, précontrôle manqué et doubles clics ne sont pas présentés comme une validation de concurrence InnoDB.

Preuves nouvelles, séparées des campagnes historiques :

```text
[chemin local privé retiré]
```

`baseline.json`, `static-audit.json`, `diffs/`, `preflight.json`, `attempt-1/commands.json` et journaux, `backend.guard.json`, `launcher.guard.json`, garde Node frontend, `integration-frontend.json`, `integration-sql.json`, `integration-exchanges.json`, `integration-omissions.json`, gardes intégrés, `additional/audit_cases.py`, `additional/backend.guard.json`, `additional/partial-ddl-observation.json` et `final-validation.json`. Les échanges archivés se limitent aux statuts, chemins, booléens et résultats fictifs nécessaires ; aucun cookie/jeton/mot de passe brut du protocole conservé. Les preuves temporaires peuvent être nettoyées par le système ; le présent rapport est le livrable permanent.

## 9. Recette jury préparée — non exécutée

Préparer ultérieurement un **nouveau kit isolé inspecté**, avec sources actuelles figées, ressource `likes.js` autorisée et décision sur les scripts exclus. Ne pas lancer le kit 6F.2 en forçant ses empreintes, ni `run_local.py` qui charge `.env` et peut privilégier le groupe Aiven.

Jeu prévu uniquement pour la démonstration isolée, **non inséré ici dans une base réelle** :

| Élément à préparer | Usage |
|---|---|
| `jury6g3_admin`, `admin6g3@example.invalid`, admin actif | Consultation de l’administration |
| `jury6g3_alice`, `alice6g3@example.invalid`, membre actif | Histoire, likes et publication du commentaire |
| `jury6g3_bob`, `bob6g3@example.invalid`, membre actif | Vérification du second compte et signalement |
| Une Story catégorie 1, slug `recette-6g3` | Histoire fictive, active |
| Une Story catégorie 2, slug `recette-coldcase-6g3` | Cold Case fictif, actif |
| Aucun commentaire/like/signalement de remplissage | Les lignes visibles seront créées par les actions démontrées |

Les mots de passe seront générés temporairement par le futur kit, hachés avec le mécanisme normal et non réutilisés. Pas de CSV privé ni de compte réel importé. Catégories, auteur des dossiers et révisions de gestion doivent être valides. Chaque compteur affiché sera vérifié à partir des lignes effectivement présentes, pas imposé dans le DOM.

**Prérequis de schéma avant toute démonstration :** disposer de `comment_likes`, de ses unicités/index/FK actifs et d’historiques compatibles. Pour une mémoire neuve créée depuis les modèles, annoncer explicitement « schéma neuf de démonstration » ; cela ne prouve pas une migration. Pour montrer la candidate, utiliser un prédécesseur strictement synthétique, appliquer uniquement la candidate sous garde puis vérifier schéma et témoins avant de commencer. Ne jamais tenter la migration pendant la présentation sur la base du site. Arrêter en cas de NULL/non-zéro/valeur invalide ou de schéma partiel.

| Étape | Action manuelle future | Résultat et explication attendus |
|---|---|---|
| 1 — Connexion | Alice se connecte depuis le formulaire | Session réelle ; aucun cookie/CSRF affiché ou capturé |
| 2 — Histoire | Ouvrir `dossier.html?slug=recette-6g3` | Récit et vrais compteurs ; Mélissa montre le contrôle sous le récit |
| 3 — Like d’histoire | Cliquer J’aime, actualiser, puis Retirer mon J’aime | Une ligne Vote puis zéro pour Alice ; nombre et `aria-pressed` relus ; Sylvie explique GET/POST/DELETE |
| 4 — Commentaire | Publier un texte fictif unique | Confirmation 201 ; bon auteur et bon dossier ; le brouillon disparaît après confirmation |
| 5 — Like de commentaire | Aimer le commentaire créé | Une ligne CommentLike d’Alice ; compteur historique physique inchangé |
| 6 — Actualisation | Recharger la fiche ; retirer puis réajouter si utile | Le nombre et l’état personnel viennent toujours de SQL ; Mahamadou explique couple unique/FK/COUNT |
| 7 — Signalement | Déconnecter Alice, connecter Bob, sélectionner ce commentaire et saisir un motif fictif | Bonne cible, confirmation 201 ; likes/commentaire conservés ; ne pas renvoyer après résultat incertain |
| 8 — Administration | Déconnecter Bob, connecter l’admin et actualiser le dashboard | Signalement retrouvé par son id de commentaire ; sept indicateurs correspondant aux données réelles de cette mémoire |

Compléments après le parcours principal : avec Bob, vérifier que son like personnel est distinct de celui d’Alice ; vérifier le Cold Case ; tester Tab/Entrée/Espace et focus visible ; après déconnexion, vérifier le refus d’écriture. Toute démonstration d’archive/restauration ou purge doit viser une copie synthétique sacrifiable et conserver un dossier témoin. Aucun besoin de purger pour réussir les huit étapes.

En cas d’erreur après envoi, conserver le message d’incertitude, vérifier l’état sans répéter automatiquement l’action. Ne pas redémarrer une mémoire de démonstration pour prétendre prouver la persistance : son contenu disparaît à l’arrêt. Si l’autorisation navigateur manque, présenter les preuves WSGI/DOM comme telles, sans annoncer une recette Edge accomplie.

## 10. Blocages, corrections possibles et autorisations suivantes

| Point | État / suite nécessaire |
|---|---|
| Likes dans les sources relues et les essais isolés | Aucun défaut fonctionnel bloquant reproduit ; conserver l’implémentation auditée |
| Kit 6F.2 périmé, module `likes.js` absent de sa liste publique/manifeste | **Bloquant pour utiliser ce kit.** Autoriser une nouvelle version du kit et son inspection sans serveur avant lancement |
| Cinq références au script exclu | **Couverture complète bloquée.** Autoriser revue ou modification ciblée ; sinon accepter expressément une recette restreinte avec ressource bloquée |
| Échec entre table et index | Risque de schéma partiel reproduit ; préparer/valider une procédure de reprise. Toute modification de la candidate exige une autorisation distincte |
| Historiques et schéma de la base du site | Inconnus. Inventaire réel distinct à autoriser ; arrêt obligatoire si incompatibilité. Aucun effacement/conversion proposé comme correction automatique |
| MySQL/InnoDB | Validation distincte sur base synthétique MySQL à autoriser, notamment verrous, comptes concurrents et DDL ; aucun accès Aiven déduit de cet audit |
| Edge et serveur local | Autorisation nouvelle nécessaire après kit prêt, pour écoute locale bornée et Edge manuel, sans CDP ni changement des protections Windows |
| Déploiement/migration réelle | Autorisations séparées pour sauvegarde, maintenance, inventaire, migration et reprise ; aucune action réelle couverte par le GO éventuel d’une recette isolée |

Le seul fichier créé dans le dépôt par 6G.3 est ce rapport. Les **128 fichiers préexistants contrôlés sont identiques par SHA-256** ; branche, HEAD et index sont conservés. État final attendu et vérifié dans le reçu : **46 fichiers suivis modifiés, 70 non suivis, aucun indexé**, soit uniquement ce rapport ajouté au travail antérieur. Aucun commit, push, changement de branche, suppression de fichiers, changement des protections Windows ou correction applicative/migration.

**Verdict : NO-GO pour la recette navigateur avec base de test isolée en l’état.** Les likes passent les vérifications isolées ; la levée du NO-GO demande un kit actualisé et inspecté, une décision sur le script exclu et l’autorisation explicite de lancement local/Edge. Aucune de ces étapes n’est lancée dans 6G.3. Arrêt et attente de validation.
