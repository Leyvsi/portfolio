# Tests et validation — preuves pour le jury

> Etat de diffusion scolaire du 3 novembre 2026 : suivre le [guide actuel](../../LIVRAISON_SCOLAIRE.md) et la [validation scolaire](VALIDATION_SCOLAIRE.md). Les sections de campagnes anterieures et leurs commandes sont historiques ; elles ne remplacent pas la procedure actuelle. Les chemins sous `C:\chemin\utilisateur` sont des exemples anonymises. Les archives internes signalees sont conservees localement.

## État courant — 2 novembre 2026

Lire d’abord les [supports 6H.1](SUPPORT_JURY_LOT6H1.md), l’[index courant](INDEX_CODE_LOT6H1.md) et la [procédure sur un autre PC](../../LIVRAISON_SCOLAIRE.md). Le bilan actuel distingue **854 tests historiques**, recette Edge réussie en SQLite fictif et contrôles documentaires de ce lot. Le modèle actuel contient dix tables et treize FK ; le compte est partagé sur dix pages, les signalements sont contextualisés, les likes de dossier/commentaire sont individuels.

Les compléments et questions ci-dessous conservent leur contexte historique. Les anciennes mentions de fonctions absentes, de neuf tables ou de recette non exécutée ne constituent pas l’état courant. Les 76 questions/réponses historiques restent conservées. Aucun résultat MySQL ou de déploiement n’est ajouté.


**État courant 6C.2 — 31 octobre 2026 : 285 backend + 364 frontend + 8 lanceur = 657 PASS**, zéro échec/erreur/ignoré final. Les 604 de 6C.1 ci-dessous sont la référence historique, non une validation du nouveau code. Bilan, commandes et limites (archive interne non livree) ; [tests de purge](../../backend/tests/test_story_deletion.py), [migration contrôlée](../../backend/tests/test_report_migration.py), [dialogue et réponses incertaines](../../frontend/tests/admin-deletion.test.cjs).

Les 31 nouvelles méthodes backend couvrent notamment le graphe complet et vide, le dossier témoin, la FK, l’ancien type other refusé avant DDL, les cibles invalides/non canoniques, le vrai rollback après DELETE de reports/commentaires, la perte d’accusé COMMIT, la réutilisation d’id, deux administrateurs séquentiels et le deadlock simulé. Vingt-deux cas frontend vérifient confirmation/annulation, titre/accord, doubles clics, timeout avant/après commit simulé, relecture, accès, réponses tardives et compteurs. Le test other n’est pas effacé : déplacé vers la reprise refusée, avec un report d’un autre dossier conservé comme témoin en 6C.1.

Le harnais inspecté reste hors dépôt : `$env:TEMP/portfolio-lot6c2-implementation-20261031-bpf4frum`. Aiven/variables privées neutralisés et dotenv désactivé avant import ; réseau, MySQL/bases fichier, ATTACH/DETACH, sous-processus applicatifs, lectures privées et écritures du dépôt bloqués. **Renforcement : FK SQLite activées et assertées à chaque connexion de toutes les suites**, y compris migration. Toutes les données sont fictives et en mémoire. Les compteurs interdits du passage final restent à zéro. La migration n’importe pas env.py. Aucun Edge/serveur réel.

La campagne ne prouve ni MySQL/Aiven, ni une véritable concurrence SQL multi-connexion, ni la chaîne historique complète de migrations. Deux clients séquentiels et les erreurs simulées sont nommés comme tels. Les détails et la couverture des 36 scénarios figurent dans le bilan courant.

**État le 31 octobre 2026 :** lot 6C phase 1 (archive interne non livree), **254 backend + 342 frontend + 8 lanceur = 604 PASS**, aucun échec final, erreur ou test ignoré. Les résultats des campagnes antérieures ci-dessous restent historiques. Les tests d’archivage sont dans [test_story_archiving.py](../../backend/tests/test_story_archiving.py) et [admin-archives.test.cjs](../../frontend/tests/admin-archives.test.cjs).

Les vingt exigences de tests sont reliées aux scénarios dans le bilan : autorisations, CSRF, cibles invalides, idempotence, toutes les lectures/écritures publiques, conservation des neuf tables, restauration, compteurs, annulation, doubles clics, timeout, relecture et rollback après un vrai flush. La migration préparée est exercée sur un schéma historique minimal fictif en SQLite mémoire ; ni la chaîne Alembic complète ni une base réelle ne sont utilisées.

Harnais inspecté hors dépôt : `$env:TEMP/portfolio-lot6c-phase1-20261030-673diw95`. Les gardes de 6D restent identiques ; cinq nouvelles sources sont explicitement ajoutées au manifeste, puis les corrections sont revues dans `manifest-review-2.json`. Dotenv est neutralisé et les paramètres distants supprimés avant tout import. Seules les bases SQLite `:memory:` sont permises ; réseau, sous-processus applicatifs, fichiers privés et écritures du dépôt sont bloqués. Les compteurs interdits de toutes les suites sont à zéro. Voir `attempt-2/commands.json`, stdout/stderr, `backend.guard.json`, `launcher.guard.json` et `attempt-2/frontend.node-guard.json`.

```powershell
# Le dossier de preuves contient le harnais inspecté ; ne pas lancer Flask.
$preuves6c = Join-Path $env:TEMP 'portfolio-lot6c-phase1-20261030-673diw95'
& .\.venv\Scripts\python.exe -I -B (Join-Path $preuves6c 'run-checks.py') --inspect
& .\.venv\Scripts\python.exe -I -B (Join-Path $preuves6c 'run-checks.py')
```

**Limites 6C :** clients WSGI séquentiels et entrelacements frontend simulés ; aucune preuve de concurrence SQL multi-connexion ou de verrouillage InnoDB. FK SQLite activées et contrôlées dans la suite 6C. Edge réel, clavier/responsive réels, MySQL/Aiven, migration réelle et durabilité après redémarrage restent NON EXÉCUTÉS. La référence 561 PASS du lot 6D ne s’ajoute pas aux 604 PASS actuels.

[Sommaire](README.md) · Index du code (archive interne non livree) · [Démonstration](DEMONSTRATION.md)

Mise à jour documentaire du **29 octobre 2026**, à partir des rapports, matrices JSON/CSV, métadonnées et journaux locaux des étapes 2 à 4. Référence testée : branche `feature/frontend-api-integration`, HEAD `07a9f03ea0a3bdad4a07066fdd7bab1997cc158b`. Les commentaires de l'étape 5 sont postérieurs à ces exécutions : les 439 tests ne sont pas présentés comme relancés sur les fichiers commentés.

La campagne actuelle du **lot 6D, le 30 octobre 2026**, est décrite en section 10 : **561 réussites** sur les nouvelles sources. Les campagnes antérieures ci-dessous restent identifiées séparément.

## 1. Ce que les termes désignent ici

| Type | Preuve et périmètre réel |
|---|---|
| Test unitaire | Fonction ou règle examinée isolément : validation, sélection d'image, classification d'une erreur. Tous les tests backend ne sont pas unitaires. |
| Test d'intégration | Plusieurs composants réels ensemble : Flask, permissions, SQLAlchemy et SQLite ; ou middleware WSGI et fichiers statiques. |
| Test API | Requête/réponse : méthodes, JSON, codes HTTP, permissions et effets en base. Le client Flask travaille en processus, sans ouvrir de serveur TCP. |
| Test frontend simulé | `node:test`, `assert/strict` et `node:vm` exécutent les vrais scripts avec DOM et `fetch` fabriqués. Cela ne prouve pas un cookie ou un rendu navigateur réel. |
| Navigateur réel automatisé | Microsoft Edge, vrai DOM et HTTP local, pilotés par Node.js et DevTools/CDP. L'API Flask et SQLite sont réelles. Ce n'est pas une recette humaine. |
| Test manuel humain | Une personne exécute et observe un scénario. Aucun scénario entièrement manuel humain n'est revendiqué dans ces campagnes. |
| Test Swagger | Distinguer le contrat OpenAPI vérifié automatiquement, le chargement de Swagger UI et une opération réellement exécutée avec « Try it out ». Un affichage réussi ne valide pas un POST. |
| Persistance SQL | Après un commit, relire les champs métier sur une nouvelle connexion, puis après redémarrage du serveur. Une notification de succès seule ne suffit pas. |
| Vérification statique | Lire ou analyser les sources, syntaxe, liens, contraintes déclarées et AST sans démarrer l'application. Ne prouve pas un parcours en exécution. |

## 2. Environnement attesté

Windows 11, build 26300 (certaines métadonnées utilisent la version noyau Windows 10.0), PowerShell 5.1, Python **3.13.0** dans `.venv`, Node.js **v24.16.0**, Edge **156.0.4314.42**, SQLite **3.45.3** pour l'étape 4.

Les neuf dépendances Python directes sont fixées dans [requirements.txt](../../backend/requirements.txt) : Flask 3.1.3, flask-restx 1.3.2, Flask-Cors 6.0.5, Flask-SQLAlchemy 3.1.1, SQLAlchemy 2.0.53, PyMySQL 1.2.0, python-dotenv 1.0.1, Werkzeug 3.1.6 et Flask-Migrate 4.1.0. PyMySQL installé ne signifie pas connexion MySQL effectuée. Swagger UI utilise la version 4.15.5.

Depuis PowerShell à la racine, les campagnes ont utilisé des environnements enfants reconstruits, des paramètres Aiven vides, `load_dotenv` neutralisé avant import et des protections contre les lectures privées, les autres bases et les connexions sortantes. Python `-I` isole son démarrage et `-B` évite les écritures de bytecode ; **ces deux options ne suffisent pas seules à bloquer le réseau ou `.env`**.

La priorité de configuration Aiven rend insuffisant le seul réglage de `DATABASE_URL`. Les harnais contrôlent aussi SQLAlchemy, sqlite3 et PyMySQL. Des sondes séparées ont vérifié les refus avant accès. Aucun secret, cookie ou jeton valide n'a été enregistré dans les sorties textuelles publiables.

## 3. Étape 2 — 439 tests automatiques réussis

Campagne retenue le **29/10/2026, 16:34:06 à 16:34:23, heure de Paris**. Durée totale 16,848 s. Chaque suite termine avec le code **0**, sans échec, erreur, test ignoré ni annulation. Les sorties complètes confirment les comptes, indépendamment du rapport.

| Suite | Outils et type | Réussites | Limites |
|---|---|---:|---|
| Backend | `unittest`, client Flask, SQLAlchemy, vraie SQLite en mémoire ; surtout intégration/API, quelques helpers isolés | 205 | Pas de serveur TCP, Aiven/TLS ni migrations ; certaines erreurs injectées. |
| Frontend | `node:test`, `assert/strict`, `node:vm`, DOM/API simulés | 226 | Pas de navigateur ni cookie réel. |
| Lanceur | `unittest`, client WSGI Werkzeug, API factice et démarrage simulé | 8 | Pas de serveur HTTP ni de connexion SQL. |
| **Campagne automatique** | | **439** | Aucun pourcentage de couverture mesuré. |

La campagne historique du 25 octobre rapportait les mêmes nombres. La réexécution du 29 confirme ces nombres pour les scénarios couverts, sans transformer l'historique en nouvelle preuve MySQL.

### Inventaire backend et assertions

| Fichier | Méthodes exécutées | Scénarios et assertions principales |
|---|---:|---|
| [test_api_errors_stats_login.py](../../backend/tests/test_api_errors_stats_login.py) | 14 | Statistiques, connexion, erreurs API et codes/réponses JSON. |
| [test_comments_theories.py](../../backend/tests/test_comments_theories.py) | 37 | Lecture/création, likes, signalements, champs, compteurs, erreurs SQL et état des lignes. |
| [test_csrf.py](../../backend/tests/test_csrf.py) | 29 | Session, jetons absents/invalides, méthodes, exceptions login/anonymes, refus 403 et absence d'effet interdit. |
| [test_proposals_ban.py](../../backend/tests/test_proposals_ban.py) | 42 | Propositions, rôle, bannissement, validations, transactions et erreurs injectées. |
| [test_reports.py](../../backend/tests/test_reports.py) | 22 | Signalements, cible/type, permissions, compteur, JSON et SQLite isolée. |
| [test_swagger.py](../../backend/tests/test_swagger.py) | 32 | Contrat OpenAPI/Flask, champs, statuts, sécurité déclarée et HTML Swagger ; pas de navigateur/CDN. |
| [test_users_votes.py](../../backend/tests/test_users_votes.py) | 29 | Inscription, mot de passe, email, unicité, vote, conflits SQL et rollback. |

Les sous-cas `subTest` ne sont pas ajoutés au nombre de méthodes. Les assertions vérifient notamment 200/201/400/401/403/404/405/409/415/500, les données JSON, les lignes créées ou absentes et les appels transactionnels. Les erreurs MySQL testées sont des objets injectés, sans service MySQL. `db.create_all()` crée le schéma de test ; cette suite ne démontre pas toutes les FK/cascades effectives.

### Inventaire frontend et lanceur

| Fichier | Cas retenus | Ce qui est vérifié |
|---|---:|---|
| [images.test.cjs](../../frontend/tests/images.test.cjs) | 12 | Sources d'images, replis et DOM fabriqué. |
| [proposals.test.cjs](../../frontend/tests/proposals.test.cjs) | 35 | JSON, validations, CSRF, erreurs et doubles soumissions. |
| [theories.test.cjs](../../frontend/tests/theories.test.cjs) | 61 | Identifiants réels simulés, limites, session/CSRF, saisie conservée et statut 201. |
| [theories-list.test.cjs](../../frontend/tests/theories-list.test.cjs) | 48 | Lecture publique, états vide/erreur, actualisation et réponses tardives. |
| [admin-dashboard.test.cjs](../../frontend/tests/admin-dashboard.test.cjs) | 70 | Rôle, compteurs, lectures, annulation et nettoyage après refus. |
| [test_run_local.py](../../tests/test_run_local.py) | 8 | Octets HTML/CSS/JS/SVG, chemins API, fichiers privés/traversées et arguments du démarrage simulé. |

Les cas frontend sont paramétrés : le nombre de déclarations `test(...)` lues statiquement n'est pas le nombre des cas TAP exécutés.

### Commandes réellement utilisées à l'étape 2

Les chemins privés absolus originaux sont conservés dans `*.metadata.json` hors dépôt. Les variables ci-dessous représentent **les mêmes chemins et arguments**, avec la racine courante et le répertoire temporaire de cette machine. Il s'agit du relevé de campagne, pas d'une nouvelle exécution pendant l'étape 5.

```powershell
$python = (Resolve-Path '.\.venv\Scripts\python.exe').Path
$node = (Get-Command node).Source
$preuves2 = Join-Path $env:TEMP 'portfolio-tests-20261029-8cf89b61c7c146089d55aaabfb838240-verified'
& $python -I -B (Join-Path $preuves2 'python-offline-bootstrap.py') backend
& $node --require (Join-Path $preuves2 'node-offline-guard.cjs') --test --test-isolation=none --test-reporter=tap frontend/tests/images.test.cjs frontend/tests/proposals.test.cjs frontend/tests/theories.test.cjs frontend/tests/theories-list.test.cjs frontend/tests/admin-dashboard.test.cjs
& $python -I -B (Join-Path $preuves2 'python-offline-bootstrap.py') launcher
```

Ces enfants sont normalement lancés par `campaign.py` avec un environnement nettoyé, pas depuis un environnement applicatif hérité. Le script local `reproduce.ps1` prépare un nouveau dossier, puis les phases `prepare`, `probe`, `run`. Les protections historiques dépendent du HEAD et des empreintes examinées : ne pas les contourner ou réutiliser les sorties anciennes pour annoncer une nouvelle validation.

Les commandes de découverte du README antérieur restent des **points d'entrée des suites**, distincts des argv protégés réellement archivés :

```powershell
.\.venv\Scripts\python.exe -B -m unittest discover -s backend/tests -p 'test_*.py' -v
.\.venv\Scripts\python.exe -B -m unittest discover -s tests -p 'test_run_local.py' -v
node --test --test-isolation=none frontend/tests/images.test.cjs frontend/tests/proposals.test.cjs frontend/tests/theories.test.cjs frontend/tests/theories-list.test.cjs frontend/tests/admin-dashboard.test.cjs
```

Ne les assimiler ni à une protection complète, ni à une commande relancée pendant l'étape 5. Une nouvelle campagne demande une nouvelle revue d'isolation et de nouvelles preuves.

Un premier essai avait obtenu 205 réussites backend mais un code de bootstrap 1 : des sondes Windows d'une dépendance (`platform.machine`, nom d'hôte et périphérique NUL) avaient déclenché les gardes. Le bootstrap temporaire a été adapté pendant l'import de dépendances ; la campagne complète ci-dessus a ensuite passé ses protections. Ce premier essai n'ajoute pas 205 au bilan de 439.

## 4. Étape 3 — véritable Edge, consultation et sessions

Campagne principale du **29/10/2026, 18:11:37 à 18:12:31, Paris** : **28 PASS, 2 FAIL, 0 BLOQUÉ, 7 NON EXÉCUTÉS**, soit 37 scénarios suivis. Les 30 scénarios tentés utilisent Edge réel automatisé par CDP ; aucune recette entièrement manuelle humaine.

Une base SQLite temporaire dédiée contenait **14 lignes fictives**. Après initialisation, elle était verrouillée en lecture seule ; seuls les POST de connexion/déconnexion étaient autorisés. Aucun contenu supplémentaire, bannissement ou DELETE n'a été exécuté.

| Groupe | Scénarios effectivement examinés | Preuve et limite |
|---|---|---|
| Navigation | Accueil, listes, recherche, slug présent/absent, images et liens | DOM réel, captures et GET 200/404. |
| Comptes | Connexions lecteur/admin, conservation puis perte de session, déconnexion | POST login/logout 200 ; `/me` 200 ou 401. La perte de cookie provoquée n'est pas un test d'expiration dans le temps. |
| Sécurité | Anonyme, lecteur face aux routes admin, CSRF négatif sur logout | 401/403 attendus ; aucun jeton enregistré. |
| Administration | Compteurs, propositions et signalements déjà initialisés | GET réels et valeurs attendues ; aucune action de modération. |
| Affichage | Ordinateur, viewport mobile émulé, Tab, exceptions et réseau CDP | Pas de téléphone physique, lecteur d'écran ni audit humain complet. |
| Swagger | Interface et contrat chargés ; GET des histoires réussi dans les reprises | Deux scénarios complets « Try it out » incomplets, conservés FAIL de harnais. Cela ne prouve pas un échec métier de l'API. |

Les sept NON EXÉCUTÉS étaient L04/L05 (créations), SW04/SW05 (POST Swagger), SW06/SW07 (DELETE/bannissement) et P01 (persistance d'une création). L'étape 4 a ensuite produit ses propres preuves de création/persistance, sans modifier ce bilan historique.

```powershell
$preuves3 = Join-Path $env:TEMP 'portfolio-recette-execution-20261029-02918114311943e4aaa2a42052410ede'
& $node (Join-Path $preuves3 'recipe.cjs') run-resume
# Enfant serveur protégé, environnement et secrets éphémères fournis par le contrôleur :
& $python -I -B (Join-Path $preuves3 'isolated-server.py') serve-existing-fixtures
# Reprises anonymes Swagger en lecture seule, également archivées :
& $node (Join-Path $preuves3 'recipe.cjs') swagger-readonly
```

Les scripts appelaient réellement `run_local.main()` et Flask sur `127.0.0.1:5000`, sans debug/reloader, avec profil Edge neuf. Les trois assets publics Swagger déjà acquis étaient servis par interception locale ; leur chargement ne valide pas la disponibilité future du CDN. Les arguments Edge complets sont dans les fichiers `actual-commands.json` locaux.

Les incidents d'environnement et de pilotage sont conservés : précision des dates nanosecondes côté JS, résolution inverse loopback bloquée au premier démarrage, mauvais sélecteur de clic Swagger puis scénarios paramétrés inachevés. Les adaptations portaient sur les harnais hors dépôt. Le rapport garde les deux FAIL malgré les succès partiels de GET.

## 5. Étape 4 — base fichier, transactions et persistance réelle

Le **29/10/2026**, initialisation/tests SQL vers **18:42:59–18:43:00**, reprise Edge et redémarrage vers **18:47:35–18:47:43**, Paris. Une **nouvelle** SQLite temporaire a été créée ; la base de l'étape 3 est restée inchangée.

Les dix scénarios BDD passent. Bilan fonctionnel : **15 PASS, 0 FAIL, 0 BLOQUÉ, 1 NON EXÉCUTÉ**. Avec le premier échec de démarrage Edge conservé comme incident H-EDGE01 : **15 PASS, 1 FAIL, 0 BLOQUÉ, 1 NON EXÉCUTÉ**. Les quatre sondes préalables d'isolation sont séparées de ces totaux.

| ID | Assertions réellement vérifiées |
|---|---|
| BDD-01 | Utilisateur créé en 201 ; identifiant, pseudo et email relus sur une connexion SQL indépendante. |
| BDD-02 | Pseudo/email doublons : deux refus API 400 et deux vraies erreurs SQL UNIQUE ; aucun ajout. |
| BDD-03 | Théorie liée au bon utilisateur et au bon dossier, contenu enregistré. |
| BDD-04 | Auteur, contenu et statut `pending` de la proposition enregistrés. |
| BDD-05 | Commentaire + signalement, cible texte cohérente, compteur 1 ; cible absente refusée 404. |
| BDD-06 | Vote 201 ; doublon API 409 et contrainte SQL UNIQUE ; un seul vote conservé. |
| BDD-07 | Proposition réellement flushée, puis vrai doublon SQL provoqué ; HTTP 500 attendu, rollback réel appelé une fois, aucun effet partiel conservé. |
| BDD-08 | Dix INSERT à FK invalides refusés par SQLite ; `PRAGMA foreign_keys=1` et `foreign_key_check` vide. |
| BDD-09 | Session SQLAlchemy retirée, pool libéré, nouvelle connexion physique : mêmes 11 lignes déjà validées. |
| BDD-10 | Après les formulaires Edge, arrêt propre puis nouveau processus serveur : mêmes champs métier et compteurs des 13 lignes, GET 200. Aucun réamorçage. |

BDD-01 à BDD-09 utilisent le client Flask en processus et une SQLite fichier réelle. BDD-07 ajoute temporairement un listener `before_commit` qui déclenche le vrai conflit après flush ; l'erreur n'est pas un objet simulé. L'espion sur rollback appelle la vraie méthode. Cela démontre l'annulation dans ce cas contrôlé, sans prétendre reproduire toutes les pannes possibles.

Les parcours supplémentaires ont utilisé **les vrais formulaires dans Edge** : théorie et proposition créées en 201, puis relues par API et SQL. Deux POST sans CSRF valide ont donné 403 sans création. Swagger s'est affiché avec ses 24 opérations ; **aucun POST Swagger tenté** : le paramètre CSRF n'apparaissait pas dans l'opération proposition inspectée et le harnais ne le renseignait pas.

Le premier démarrage Edge n'avait pas fourni `DevToolsActivePort` ; la reprise avec un profil neuf a réussi. Les mots de passe éphémères n'étant plus disponibles, elle a utilisé des **sessions fictives signées initialisées par le harnais**, transmises uniquement en mémoire. Aucun compte existant n'a été modifié. Les POST et CSRF des formulaires étaient réels, mais **cette reprise ne revalide pas le mot de passe ni le formulaire de connexion**.

**8 créations applicatives persistées** : six via les routes Flask, deux via les formulaires. Avec cinq lignes de préparation, total final **13 lignes**. **20 refus distincts** : 14 erreurs SQL (4 UNIQUE, 10 FK) et 6 refus applicatifs sans création. Le 500 volontaire de BDD-07 est déjà compris dans les 14 erreurs SQL ; ne pas le compter deux fois.

```powershell
$preuves4 = Join-Path $env:TEMP 'portfolio-bdd-etape4-20261029-e71f1246f3bb4615a69e76773cb8e276'
& $node (Join-Path $preuves4 'controller.cjs') run
# Code 1 : démarrage Edge initial ; neuf scénarios SQL déjà PASS.
& $node (Join-Path $preuves4 'controller-resume.cjs') run
# Code 0 : formulaires, CSRF, relecture et redémarrage.
# Enfants exécutés avec environnement protégé et paramètres éphémères sur stdin :
& $python -I -B (Join-Path $preuves4 'worker.py') init-serve
& $python -I -B (Join-Path $preuves4 'worker-resume.py') resume-serve
& $python -I -B (Join-Path $preuves4 'worker-resume.py') restart-serve
```

Ces relevés ne sont pas un kit de redémarrage autonome : les secrets étaient éphémères et l'initialisation refuse une base existante. Les sorties originales restent intactes ; `command-clarifications.json` précise un ancien nom de script resté dans le premier reçu et distingue PID des lanceurs Windows et des vrais serveurs Python. Les deux vrais processus du redémarrage étaient 16156 puis 28340 ; chaque arrêt a terminé à 0.

`db.create_all()` a créé les neuf tables, sans migration Alembic. Les dix FK ont été testées avec des références invalides. Les effets DELETE de CASCADE/SET NULL et de `delete-orphan` n'ont **pas** été exécutés. L'unicité du nom de catégorie, du slug et les PK ont été inspectées, pas toutes provoquées en erreur. `reports.target_id` n'est pas une FK SQL.

## 6. Où sont les preuves ?

Les répertoires sont locaux et hors Git, sous le dossier temporaire Windows de l'opérateur. Ils peuvent disparaître au nettoyage de Windows ; leur existence ne rend pas les artefacts disponibles dans un clone GitHub. Ne pas publier les bases brutes, profils, secrets ni journaux privés.

| Dossier sous `$env:TEMP` | Pièces à présenter localement |
|---|---|
| `portfolio-tests-20261029-8cf89b61c7c146089d55aaabfb838240-verified` | `rapport-jury.md`, `campaign.json`, trois `*.metadata.json`, stdout/stderr complets, gardes, empreintes et `after.json`. |
| `portfolio-recette-etape3-20261029-e7da04ff75774e0fa83a5975441e7cba` | Matrice préparatoire JSON/CSV ; distinguer prévu et exécuté. |
| `portfolio-recette-execution-20261029-02918114311943e4aaa2a42052410ede` | `rapport-final-etape3.md`, `scenario-results.json/csv`, `browser-results.json`, captures, commandes, journaux serveur, reprises Swagger et vérification finale. |
| `portfolio-bdd-etape4-20261029-e71f1246f3bb4615a69e76773cb8e276` | `rapport-etape4.md`, `traceability.json`, `database-tests.json`, `resume-browser-results.json`, snapshots SQL avant/après redémarrage, reçus serveur et d'arrêt, empreintes. |

Les campagnes anciennes évoquant **39 contrôles d'authentification** et **31 contrôles d'enregistrements réels** restent distinctes : elles n'ont pas été rejouées dans les campagnes ci-dessus. Aucune commande supplémentaire n'est déduite de ces seuls nombres.

## 7. Ce qui reste à vérifier

Ne pas additionner la recette Edge et les scénarios BDD aux **439 tests automatiques** : les unités de comptage et les campagnes sont différentes. Un refus attendu n'est pas un test échoué ; un scénario non exécuté n'est pas une réussite.

- MySQL/Aiven réel, TLS, contraintes déployées et concurrence MySQL : **non testés**.
- Migrations Alembic, upgrade/downgrade, révision distante : **non exécutés** ; `create_all()` ne les valide pas.
- Cascades de suppression, bans et opérations DELETE de recette : autorisation distincte nécessaire ; leurs tests isolés historiques ne les autorisent pas sur une base réelle.
- Swagger : POST authentifié et scénarios complets encore incomplets ; une page accessible ne suffit pas.
- Recette humaine, appareils physiques, accessibilité exhaustive, charge, crash brutal et sauvegarde/restauration : non attestés.
- Une installation complète depuis un clone vierge et un peuplement reproductible livré dans le dépôt restent à établir. Les harnais temporaires ne sont pas un script de peuplement produit.

L'étape 5 vérifie uniquement les commentaires, la syntaxe, la cohérence documentaire, les liens, repères et diagrammes locaux. Elle ne démarre pas le site, ne lit pas le `.env`, ne modifie aucune base et ne revendique aucune nouvelle campagne fonctionnelle.

## 8. Lot 6A — 30 octobre 2026

**221 backend + 258 frontend + 8 lanceur = 487 tests réussis**, sans échec final ni test ignoré. Cette campagne ne remplace pas les journaux historiques et ne s’additionne pas aux 439 de l’étape 2. Le bilan 6A (archive interne non livree) donne les commandes exactes, tentatives, preuves et limites.

Seize nouveaux tests Python (avec sous-cas sur les deux routes) couvrent liste, rôles, CSRF, comptes protégés, persistance, sessions ouvertes, invariance des neuf tables et rollback après flush. Trente-deux nouveaux cas frontend couvrent confirmation, doubles clics, statuts, erreurs/timeout, relecture, données affichées en texte et réponses tardives. Le test historique d’auto-ban est remplacé explicitement ; le test du nombre de règles Flask est adapté à l’opération supplémentaire. Le contrat compte 25 opérations et 26 règles Flask avec la route statique.

Le harnais hors dépôt est inspecté avant exécution ; dotenv est neutralisé et les paramètres Aiven sont vides. Il ne permet que SQLite en mémoire, bloque les connexions/réseau, lectures privées et écritures dans le dépôt. Les sondes vérifient le refus avant entrée/sortie ; leurs compteurs attendus sont séparés des suites, dont les compteurs interdits sont à zéro. Le frontend simule DOM/API ; Flask est testé par client WSGI sans serveur. La recette Edge, la durabilité après redémarrage et les locks MySQL ne sont pas exécutés. Aucun compte réel, migration ou accès Aiven.

## 9. Lot 6B — 30 octobre 2026

**227 backend + 298 frontend + 8 lanceur = 533 réussites**, zéro échec/erreur/ignoré, dès la première tentative. Les 487 de 6A et les 439 historiques restent des campagnes distinctes, non additionnées. Voir le bilan 6B (archive interne non livree) pour les argv, gardes et reçus.

Six tests Python supplémentaires créent la [fixture partagée](../../frontend/tests/fixtures/admin-stories.json) dans SQLite mémoire et comparent exactement sa forme et ses valeurs à GET /stories. Les slugs spéciaux sont réellement lus par la route Flask existante ; les neuf tables restent identiques avant/après. Quarante nouveaux cas frontend exécutent les vrais scripts avec cette fixture, couvrant tous les filtres, recherche, slugs invalides, erreurs, annulations/réponses tardives, accès et non-régression 6A. Le test WSGI du lanceur sert aussi admin-stories.js et les autres scripts du tableau.

Le harnais est inspecté, les variables Aiven vides et dotenv neutralisé avant exécution. Les sondes bloquent les opérations interdites avant entrée/sortie ; les compteurs des suites sont à zéro. Pas de navigateur réel, serveur HTTP, MySQL, migration ou donnée réelle utilisée. Les API, schémas et modèles restent identiques ; la recette responsive/clavier réelle attend une autorisation séparée.

## 10. Lot 6D — 30 octobre 2026

| Suite réellement réexécutée | Résultat retenu | Évolution depuis 6B |
|---|---|---|
| Backend | **235 PASS**, 0 échec/erreur/ignoré | Huit nouveaux tests dans [test_admin_pending_stats.py](../../backend/tests/test_admin_pending_stats.py). |
| Frontend | **318 PASS**, 0 échec/annulé/ignoré | Vingt nouveaux cas dans [admin-dashboard.test.cjs](../../frontend/tests/admin-dashboard.test.cjs) et assertions étendues dans les suites 6A/6B. |
| Lanceur | **8 PASS**, 0 échec/erreur/ignoré | Suite existante inchangée, exécutée à nouveau. |
| Total | **561 PASS**, **0 FAIL final** | Les 533 historiques sont une référence, sans addition aux résultats actuels. |

Scénarios exécutés : six agrégats conservés ; septième à zéro/une/plusieurs attentes ; autres statuts et égalité stricte ; réponse vide ; chargement et actualisation ; HTTP 500, erreur réseau/JSON simulée et statut invalide ; ancienne réponse succès/403 ignorée ; nettoyage des sept valeurs au départ et après refus ; filtres et bannissement toujours fonctionnels. Données simulées gelées non modifiées. Les anciennes assertions de nettoyage portent désormais aussi sur le septième compteur.

La [fixture à sept champs](../../frontend/tests/fixtures/admin-proposals.json) est comparée exactement au vrai GET Flask privé : permissions visiteur/lecteur/banni et rôle de session falsifié, contrat public de `/stats` inchangé, création imposant pending et erreur SQL ne devenant pas une liste vide. Comparaison des **neuf tables avant/après GET**. Les données de préparation et le POST de contrôle sont exclusivement fictifs et en mémoire.

Le harnais inspecté refuse les empreintes différentes du manifeste des 55 sources autorisées. Environnement minimal, dotenv neutralisé avant import, paramètres Aiven vides ; sockets/DNS/sous-processus et bases autres que SQLite `:memory:` bloqués, ATTACH/DETACH interdits. Les deux sondes de gardes précèdent les suites. Les compteurs interdits du passage final sont tous à zéro. Client Flask WSGI sans écoute réseau, scripts frontend dans `node:vm`, lanceur simulé ; aucun confinement d'Edge n'est revendiqué.

Preuves dans `$env:TEMP/portfolio-lot6d-20261030-vz20got1` : `attempt-2/commands.json`, stdout/stderr, manifeste archivé, `backend.guard.json`, `launcher.guard.json` et `attempt-2/frontend.node-guard.json`. Premier passage non retenu : fixture 6B incomplète, lectures de sources de traceback bloquées et sortie console Unicode du contrôleur ; diagnostics et corrections conservés. Aucun garde assoupli.

```powershell
# $preuves6d désigne le dossier temporaire ci-dessus, inspecté avant lancement.
& .\.venv\Scripts\python.exe -I -B (Join-Path $preuves6d 'run-checks.py') --inspect
& .\.venv\Scripts\python.exe -I -B (Join-Path $preuves6d 'run-checks.py')
```

**NON EXÉCUTÉ :** Edge réel, responsive/clavier réels, campagne navigateur 6A/6B, base fichier/persistance après redémarrage, MySQL/Aiven et migrations. Aucun changement Windows ou préparation de VM. Voir le bilan 6D (archive interne non livree).

## Campagne 6E.2 — périmètre HTML et non-publication

Les 657 PASS de 6C.2 restent historiques. Pour 6E.2, les suites frontend et lanceur sont exécutées sous harnais inspecté ; le backend n'est pas réexécuté, ses sources étant conservées par empreintes. Aucun test de migration n'est appelé. Voir les résultats exacts et reçus dans le bilan 6E.2 (archive interne non livree).

Les huit nouveaux [tests HTML/WSGI](../../tests/test_rgpd_information.py) vérifient les champs/contraintes d'inscription, théorie et proposition, les notices visibles et reliées aux formulaires/boutons, les scripts inchangés, l'absence de collecte/consentement supplémentaire, le brouillon hors des liens publics, ses refus GET/HEAD et le service effectif des trois pages. Ces échanges WSGI ne démarrent pas de serveur.

Trois tests frontend de HTML figé sont adaptés : les attributs et contraintes historiques restent vérifiés, et la comparaison du formulaire originel est conservée en retirant uniquement les ajouts de notice autorisés. Les tests de soumission, CSRF, erreurs, non-double-envoi et fonctions administratives restent présents.

Le harnais bloque réseau/DNS, sous-processus applicatifs, lectures privées, écritures du dépôt et bases hors SQLite mémoire ; dotenv est neutralisé avant tout import qui l'utiliserait. Les sondes sont séparées des compteurs des suites. Aucun navigateur, paquet téléchargé, base réelle ou migration. Les deux anciennes entrées inutilisées donnees.js et ancien_app.py sont retirées du manifeste sans les lire.

Non attestés : recette clavier/lecteur d'écran/navigateur, CSS/rendu mobile réel, contrôle juridique, hébergement/TLS/cookies effectifs, traitement d'une vraie demande, persistance réelle et compatibilité MySQL/Aiven. Un contrôle statique d'ARIA ou de lien n'est pas une preuve d'accessibilité exhaustive.

## Campagne 6E.3 — 1er novembre 2026

**279 backend + 364 frontend + 16 lanceur = 659 PASS**, aucune erreur/échec/ignoré dans les suites sélectionnées. Un passage complet sous harnais inspecté : aucun code applicatif changé. Les 657 de 6C.2 et 380 de 6E.2 restent historiques.

Parmi les 285 cas backend historiques, 278 sont réexécutés. Les six cas du module test_report_migration et le cas de migration d'archivage ne sont ni exécutés ni comptés comme PASS. Un [nouveau parcours API/SQL](../../backend/tests/test_moderation_journey.py) ajoute un cas, soit 279. Aucune ancienne assertion n'est supprimée ; les exclusions relèvent du harnais hors dépôt.

Le harnais 6E.3 interdit aussi les commandes/opérations Alembic et l'exécution des révisions ; leurs sources ne sont pas autorisées dans le manifeste. Les paramètres Aiven sont vides, dotenv neutralisé, réseau/lectures privées/écritures du dépôt/base non mémoire bloqués. Les FK sont activées ; le nouveau parcours vérifie database_list sans fichier, relation Report/Comment, insertion orpheline refusée et rollback du savepoint. Les sondes sont séparées ; les compteurs des suites, migrations comprises, restent à zéro.

Le bilan (archive interne non livree) donne les treize modules exécutés, les sept non-sélections, les preuves et les étapes. Le nouveau test appelle les vues réelles et la base mémoire, tandis que les 364 tests frontend utilisent un DOM/API simulés. Aucune recette continue navigateur/API/BDD, aucun Edge, MySQL/Aiven, migration ou redémarrage de base réelle n'est attesté.

## Campagne 6F.1 — commentaires et signalements publics

**279 backend + 428 frontend + 16 lanceur = 723 PASS**, aucun échec/erreur/annulé/ignoré dans la campagne complète finale `attempt-2`. Les 428 comprennent les 364 tests frontend existants inchangés et 64 nouveaux cas dans [comments.test.cjs](../../frontend/tests/comments.test.cjs). Un premier passage frontend `attempt-1` avait 425 PASS avant ajout de trois cas ; les campagnes ne sont pas additionnées. Les 659 PASS de 6E.3 restent historiques.

Les nouveaux tests exécutent `api.js`, `comments.js` et, pour l'intégration de la fiche, `app.js` dans un DOM/API simulés : liste publique, données invalides, création/relecture, cible exacte du signalement, confirmation/annulation, session et CSRF, UTF-8 et Unicode invalides, refus HTTP, XSS, doubles clics durant session et POST, timeout/réseau/JSON/5xx incertains, navigation et dossier archivé/restauré. Ils interdisent les routes publiques arbitraires, administratives et les statistiques dans ce contrôleur.

Les suites administratives existantes passent encore avec les sept compteurs. Les 279 cas backend incluent la preuve réelle Flask/SQLAlchemy/SQLite mémoire commentaire → signalement → consultation administrative et comparaison des agrégats aux lignes SQL, sans changer ce test. Les sept tests de migration restent exclus, sans être comptés comme réussis.

Harnais relu et inspecté avant exécution, manifeste de 65 sources avec SHA-256, environnement minimal, dotenv neutralisé, SQLite `:memory:` exclusivement et FK activées. Réseau/DNS, MySQL, bases fichier, migration, sous-processus applicatifs, lectures privées et écritures du dépôt bloqués. Tous les compteurs interdits des suites sont à zéro ; sondes distinctes. Preuves :

```text
C:\chemin\utilisateur\AppData\Local\Temp\portfolio-lot6f1-20261101-a83d216e
```

Le bilan complet (archive interne non livree) donne contrats, limites, commandes enregistrées et contrôles de préservation. **NON EXÉCUTÉS** : navigateur/Edge, serveur, rendu/clavier/lecteur d'écran réels, parcours continu navigateur/API/base de présentation, redémarrage, MySQL/Aiven et migrations. Les tests simulés et SQLite ne prouvent pas ces propriétés.

## Campagne 6F.2 — non-régression et raccordement sans réseau

**279 backend + 428 frontend + 16 lanceur = 723 PASS réexécutés**, aucun échec/erreur/annulé/ignoré dans la sélection. Sept tests de migration toujours exclus, sans modification des tests ou du code applicatif. Un seul passage complet, `attempt-1` ; les résultats de 6F.1 restent une campagne historique distincte.

Une vérification supplémentaire relie les vrais HTML servis par le middleware, leurs contrôleurs frontend relus, les vraies vues Flask et SQLAlchemy, puis le DOM administratif et les lectures SQL. Node et le client WSGI gardé échangent par stdin/stdout ; aucun port ou serveur HTTP. **42 requêtes API, 12 groupes de contrôles réussis**, comptés séparément des 723 tests. Les réponses backend ne sont pas simulées ; le DOM et le transport navigateur le sont. Le fichier historique donnees.js n'est ni lu ni exécuté, malgré ses trois références dans les pages de compte : cette omission est documentée et exclut toute revendication de couverture intégrale de leurs scripts.

Inscription/connexion, création/relecture du commentaire, cible de signalement, administration et sept compteurs égaux aux SELECT passent. Le harnais retire le CSRF pour obtenir un vrai 403 sans insertion et fait perdre deux réponses après de vrais commits : l'interface annonce un résultat incertain et ne renvoie pas automatiquement. Après déconnexion, l'envoi et l'actualisation de l'ancien dashboard sont refusés ; cartes et sept valeurs sont nettoyées au nouveau contrôle.

Deux essais initiaux du nouveau relais sont conservés comme échecs de préparation : arrêt sur le script exclu avant exécution frontend, puis encodage stdin Windows incorrect. La sélection explicite des seuls scripts relus et stdin UTF-8 ont corrigé le harnais, sans modifier l'application ni ses assertions. Le troisième passage intégré réussit. Le kit manuel a aussi nécessité l'autorisation de lecture des caches Python des seules sources relues, comme le garde historique ; son dernier contrôle sans serveur est READY. Ces essais initiaux ne sont pas comptés comme PASS.

Preuves dans `C:\chemin\utilisateur\AppData\Local\Temp\portfolio-lot6f2-20261101-72b1d59a` : résultats de `attempt-1`, gardes, dépendances, `integration-frontend.json`, `integration-sql.json`, `integration-exchanges.json`, omissions et erreurs initiales. Tous les compteurs interdits des suites et du passage intégré retenu sont à zéro. Aucun contenu de cookie, mot de passe ou jeton n'est conservé dans les reçus du protocole.

Le bilan 6F.2 (archive interne non livree) distingue les vérifications statiques, WSGI/DOM et le kit manuel (archive interne non livree) inspecté sans serveur. **Edge, branche d'écoute du kit, rendu/clavier réels, MySQL/Aiven, migrations et persistance après redémarrage : NON EXÉCUTÉS.**

## Campagne 6G.2 — deux systèmes de likes

**303 backend + 484 frontend + 16 lanceur = 803 PASS**, aucune erreur/échec/annulé/ignoré dans `attempt-4`, dernière campagne complète. Les 723 de 6F.2 restent historiques. Ajouts : 18 méthodes backend likes, six méthodes de migration candidate et 56 cas frontend ; adaptations explicites des contrats de nombre de tables/règles/Swagger et de l'unicité commentaire, sans supprimer les assertions de conservation ou de rollback. Les théories gardent leurs likes répétables.

Le premier passage backend exécutait 301 méthodes, avec trois échecs de tests historiques : deux attentes de neuf tables au lieu de dix et une injection d'erreur sur l'ancien UPDATE, devenu INSERT pour les commentaires. Les comparaisons de toutes les tables et les tests d'erreur ont été conservés et adaptés au métier autorisé. `attempt-2` : 801 PASS. Deux contrôles supplémentaires vérifient cascade d'auteur en SQL et plafond interne de purge ; InnoDB/FK de la candidate sont précisés avant `attempt-3` : 803 PASS. Aucune addition entre campagnes.

`attempt-4` confirme 803 PASS après validation renforcée de la confirmation commentaire et suppression de l'état personnel au départ de page. Les compteurs publics restent issus des réponses serveur ; les deux contrôles frontend de cycle complet vérifient aussi cet effacement au départ.

Les suites couvrent ajout/retrait/idempotence/doublon, identité, CSRF, anonymes/bannis/ids/archives, vrais INSERT/DELETE suivis de rollback, commit effectué puis accusé perdu, FK/unicité/cascades, témoins d'autres dossiers, historique non nul préservé, graphe signé/plafond et cinq clés publiques de purge. Le frontend couvre compteur/état, session, doubles clics, réseau/timeout/JSON, compte changé et réponses tardives, ainsi que commentaires/signalements préservés.

**Candidate seule** `c6g200000001_add_comment_likes.py` exercée en SQLite synthétique mémoire : compteurs à zéro, reprise refusée avant DDL pour non-zéro/SQL NULL/négatif/texte/types parents incompatibles, contraintes et rollback de savepoint, downgrade vide ou refus de perte de données. Gardes : seul ce fichier peut exécuter du code de migration et des opérations DDL sur `comment_likes` en mémoire. Les commandes Alembic, autres révisions et **sept tests de migration historiques** restent bloqués/exclus. Aucun schéma réel ou chaîne historique complète migré.

Vérification continue supplémentaire : contrôleurs réels depuis HTML servi en WSGI, puis vraies vues Flask/SQLAlchemy et comparaison SQL/DOM ; **79 requêtes, 14 groupes de contrôles réussis**. Ajout/retrait/réajout de chaque type, likes relus après navigation et compteurs administrateur toujours égaux à SQL. DOM/transport navigateur simulés ; donnees.js reste explicitement exclu. Ces groupes ne sont pas ajoutés comme méthodes unittest aux 803.

Preuves sous `C:\chemin\utilisateur\AppData\Local\Temp\portfolio-lot6g2-20261101-c47e19a2` : manifeste de 71 sources, commandes/journaux par tentative, gardes et reçus, comparaisons SQL et bilan (archive interne non livree). Configuration minimale, dotenv neutralisé, Aiven vide, SQLite mémoire/FK actives, réseau/lectures privées/écritures dépôt/bases réelles/sous-processus applicatifs bloqués ; compteurs interdits à zéro. **NON EXÉCUTÉS :** Edge, serveur HTTP, responsive/clavier/accessibilité réels, MySQL/InnoDB réel, migration réelle, courses SQL multi-connexions et durabilité après redémarrage.
