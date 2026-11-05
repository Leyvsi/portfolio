# Lot 6G.2 — likes individuels des dossiers et commentaires

> Archive pédagogique datée : les résultats et descriptions ci-dessous concernent le lot indiqué. Les anciens repères de ligne ne décrivent pas la version candidate. Pour préparer la soutenance actuelle, consulter les quatre fiches et le référentiel reliés au sommaire.

> Copie publique de référence : les chemins personnels et liens de travail internes sont retirés. Les preuves et commandes historiques gardent leur date et leur périmètre ; utiliser le README actuel pour le lancement.

[Sommaire](README.md) · [Conception 6G.1](BILAN_LOT6G1.md) · [Tests](TESTS_ET_VALIDATION.md) · [Index du code](INDEX_CODE_JURY.md)

**1er novembre 2026 — développement local des étapes A et B réalisé et testé dans SQLite synthétique isolée. 803 PASS : 303 backend, 484 frontend, 16 lanceur.** Un parcours supplémentaire relie les contrôleurs frontend aux vraies vues Flask/SQLAlchemy : 79 requêtes, 14 groupes réussis, DOM simulé. Aucun navigateur ou serveur HTTP lancé, aucune base réelle ouverte ou migrée.

**Étape A :** Vote conservé, ajout/retrait/état personnel sur histoires et Cold Cases. **Étape B :** CommentLike, uniquement lorsque l'ancien compteur est compatible (zéro). Tout historique non nul/invalide reste intact et bloque la migration candidate et les actions. Compatibilité démontrée sur données synthétiques ; **compatibilité des données du site inconnue**. Aucune décision de reprise des nombres non attribuables n'est prise.

## 1. Préservation et fichiers modifiés

Branche conservée `feature/frontend-api-integration`, HEAD `07a9f03ea0a3bdad4a07066fdd7bab1997cc158b`. Départ : **45 fichiers suivis modifiés, 62 non suivis, aucun indexé**. 121 sources/documents déjà examinés sont sauvegardés avec chemins et SHA-256 avant édition, hors dépôt. Les sept exclusions antérieures ne sont ni lues ni copiées. Aucun reset, changement de branche, commit ou push.

**Sept fichiers créés dans le dépôt :**

```text
backend/api/v1/views/likes.py
backend/tests/test_likes.py
backend/tests/test_comment_likes_migration.py
frontend/likes.js
frontend/tests/likes.test.cjs
migrations/versions/c6g200000001_add_comment_likes.py
docs/soutenance/BILAN_LOT6G2.md
```

**Seize sources/tests préexistants modifiés :**

```text
backend/models.py
backend/api/v1/swagger.json
backend/api/v1/views/__init__.py
backend/api/v1/views/comments.py
backend/api/v1/views/histoires.py
backend/api/v1/views/story_deletion_support.py
backend/tests/test_admin_pending_stats.py
backend/tests/test_api_errors_stats_login.py
backend/tests/test_comments_theories.py
backend/tests/test_story_deletion.py
backend/tests/test_swagger.py
frontend/api.js
frontend/app.js
frontend/comments.js
frontend/dossier.html
frontend/styles.css
```

**Documentation :** README principal et frontend ; sommaire de soutenance, démonstration, tests, matrice, index et quatre fiches. Quatre anciens documents de conception/audit (`ARRET_CONDITIONNEL_LOT6C2.md`, `BILAN_LOT6C_AUDIT.md`, `CONCEPTION_LOT6C2_SUPPRESSION.md`, `DECISIONS_FINALES_LOT6C2.md`) reçoivent uniquement l'actualisation des références de lignes. Leurs décisions/résultats historiques restent conservés. Les questions-réponses antérieures sont contextualisées, pas remplacées par de faux résultats.

Dashboard HTML/JS, panneaux utilisateurs/dossiers, sept indicateurs, routes de signalement, bannissement, mécanisme de théories et migrations historiques préservés. Le service backend de purge est étendu uniquement à la nouvelle dépendance interne.

## 2. Étape A — histoires et Cold Cases

La structure de Vote a été vérifiée : une présence binaire, sans note/polarité, un couple unique user_id/story_id et deux FK CASCADE. Un Cold Case est une Story. **La classe Vote et ses colonnes sont inchangées ; aucune migration ni conversion de ses anciennes lignes.** Un test conserve id, auteur et date d'un vote ancien après lecture et actions sur un autre dossier.

La fiche commune affiche le compte public réel `story.votes`, puis l'état du compte actif. J’aime ajoute la ligne par le POST existant (201), Retirer mon J’aime supprime uniquement le couple courant, sans toucher aux autres comptes. Retrait répété : 200 changed=false. Un doublon d'ajout reste 409, une seule ligne SQL.

Le compteur du POST est préparé après flush et avant commit, dans la gestion d'erreur, sans changer son JSON historique `message/votes`. L'interface relit ensuite l'état personnel ; elle ne fabrique aucun +1/-1 local.

## 3. Étape B — commentaires et historiques protégés

Nouveau modèle **CommentLike** : id Integer PK, comment_id et user_id Integer NOT NULL avec FK CASCADE, created_at UTC, `unique_user_comment_like(user_id, comment_id)` et index comment_id. Relations réciproques User/Comment avec suppression des enfants et passive_deletes. Le modèle cible explicitement InnoDB pour ses FK/transactions. Schéma déclaré : **10 modèles, 13 FK**, les 11 FK précédentes conservées.

Le nombre actif est COUNT(CommentLike), l'état personnel l'existence du couple. Les commentaires publics et détails administratifs passent par `comment_to_dict`. Le champ JSON additif **likes_compatible** distingue le compteur individuel d'un historique ambigu. La colonne physique **Comment.likes est conservée et n'est jamais incrémentée/remise à zéro par les nouvelles routes**.

| Ancien compteur | Lecture / comportement développé |
|---|---|
| Entier exactement zéro | Compte relationnel exposé dans likes, likes_compatible=true ; ajout/retrait personnel disponibles |
| Non nul, négatif ou incompatible | Valeur historique préservée dans la lecture publique, likes_compatible=false ; contrôle d'interface historique distinct et bloqué ; GET personnel/POST/DELETE → 409 LEGACY_LIKES_UNRESOLVED, aucune écriture |

Une valeur ORM est rechargée avant le contrôle : un objet périmé ne suffit pas à convertir ou rejeter un historique réel. Aucun pseudo/email/cookie/jeton stocké dans CommentLike, aucun utilisateur inventé pour attribuer d'anciens clics.

**Absence de blocage du développement local :** l'autorisation permet de poursuivre lorsque la compatibilité est démontrée en environnement isolé ; les schémas synthétiques à zéro passent. Les jeux positifs/négatifs/incompatibles prouvent le refus obligatoire, pas l'état de la base du site. **Si un futur inventaire réel autorisé détecte de tels historiques, la bascule B s'arrête et la décision de l'utilisateur est nécessaire.** Ne pas présenter l'ensemble comme déployé ou compatible avec des données jamais examinées.

Solutions à soumettre dans ce cas : maintenir les anciens nombres en lecture seule, ou décider explicitement d'une présentation distincte des nouveaux likes individuels. Aucun effacement, réattribution ou remplacement discret par zéro autorisé/implémenté. Les likes de théories restent des clics répétables hors périmètre.

## 4. Contrat API effectivement implémenté

Préfixe **`/api/v1`**, pas `/api/votes`. Quatre opérations ajoutées, deux POST réutilisés/adaptés : **36 opérations OpenAPI** et 35 règles Flask avec static. Aucune route de toggle ni de reçu.

| Route | Succès et règle |
|---|---|
| GET `/votes/{story_id}` | 200 état personnel et nombre de likes |
| POST `/votes/{story_id}` | 201 avec message/votes, doublon 409 conservé |
| DELETE `/votes/{story_id}` | 200, retrait du couple courant ; changed=false s'il était absent |
| GET `/comments/{comment_id}/like` | 200 état personnel/compte, historique incompatible 409 |
| POST `/comments/{comment_id}/like` | 200 avec status/comment ; nouveau couple, doublon 409 ; ancien compteur ambigu 409 |
| DELETE `/comments/{comment_id}/like` | 200 et changed ; historique incompatible 409 |

État personnel : `status`, `target_type` (story/comment), `target_id` entier, `likes` entier positif ou nul, `liked_by_me` booléen. DELETE ajoute changed. Aucun corps requis ; un corps éventuel ne choisit jamais l'auteur ou le compteur. Les deux enveloppes de succès POST sont volontairement différentes et contrôlées par le frontend.

Compte actif obligatoire sur ces six opérations, administrateur également autorisé ; GET sans CSRF, POST/DELETE avec filtre existant. `credentials: include`, cookie Flask et jeton rafraîchi par `/me`. Ids bornés 1..2147483647, cible existante et parent actif ; archive → 404, restauration retrouve les mêmes likes. Écritures sous contrôle/verrou du parent ; aucune suppression de parent/utilisateur/contribution par un retrait de like.

Codes : 401 session/compte absent ; 403 compte banni ou CSRF ; 404 cible absente/archivée/hors domaine ; 409 doublon d'ajout ou historique commentaire incompatible ; 500 erreur SQL sans détail sensible. Seule la violation unique métier reconnue est un doublon. Réponses personnelles/écritures `Cache-Control: private, no-store`. Les visiteurs conservent les comptes publics des lectures existantes, sans liste nominative de personnes ayant liké.

## 5. Migration candidate et limites

[c6g200000001_add_comment_likes.py](../../migrations/versions/c6g200000001_add_comment_likes.py), après c6c200000001. **Préparée et exercée uniquement sur SQLite mémoire synthétique ; aucun accès ou changement MySQL/Aiven.** La chaîne Alembic complète, env.py et les anciennes révisions ne sont pas exécutés.

Avant tout DDL : refuser table déjà présente, vérifier FK SQLite actives, inspecter les types des ids parents (entiers), lire les compteurs sans cast et refuser tout non-zéro/type invalide/SQL NULL. Les types physiques parents sont copiés pour les nouvelles FK. Sur une éventuelle cible MySQL, contrôler FK actives et parents InnoDB avant création InnoDB ; **cette branche n'est pas validée sur un moteur MySQL réel**.

Si le contrôle réussit : création de la seule table comment_likes et de son index. Aucun INSERT de reprise, UPDATE de compteur, DROP de colonne ou modification de Vote. Les tests comparent lignes et schéma avant/après un refus, avant même de compter sur un rollback. Downgrade : refuse toute ligne individuelle existante ; permet seulement le retour d'une table vide, sans toucher aux anciens compteurs/votes.

Avant exécution réelle, obtenir une autorisation distincte pour inventaire, sauvegarde de données, maintenance et migration. Arrêter/drainer les anciens écrivains qui incrémentent Comment.likes : ne pas déployer un mélange des deux systèmes. Aucun create_all ne met à jour une base existante ; les DDL MySQL ne sont pas promis entièrement annulables après un incident technique. Ne jamais contourner un refus historique pour faire une démonstration.

Ne pas déployer ce backend sur un schéma sans comment_likes : ce n'est pas un mode de compatibilité. Vérifier aussi l'unicité réellement déployée de Vote et ses anciennes lignes avant de conclure à la compatibilité de la cible.

## 6. Frontend et protection transactionnelle

Boutons natifs type=button, J’aime/Retirer mon J’aime, aria-pressed uniquement pour un état connu, texte sécurisé et focus visible. Un visiteur voit le nombre et l'information de connexion, sans bouton d'écriture actif. Valeur inconnue : indisponible, jamais zéro de secours. Commentaires incompatibles : ancien nombre explicitement historique, action bloquée.

Le contrôleur commun verrouille dès la vérification de session, capture l'intention explicite et relit l'état. Compte changé : nouvelle lecture sans écriture avec l'ancien choix. Intention déjà satisfaite : pas de POST superflu. Après confirmation, GET personnel pour compte/bouton. Un 409 provoque une lecture, pas une répétition.

Timeout/réseau/JSON invalide/5xx après envoi : **résultat incertain, aucune réussite supposée et aucune relance automatique** ; Vérifier les J’aime lit sans écrire. Les nouvelles écritures de ce contrôle restent bloquées dans cette instance de page ; un rechargement complet ne conserve pas ce verrou. Un GET peut précéder la fin d'une requête en cours et n'attribue pas l'état observé à une commande perdue. Succès confirmé puis lecture indisponible : distinction explicite dans le message.

Les réponses tardives sont ignorées après destruction ; l'état personnel est effacé au départ, le compte public peut rester affiché. Un retour depuis le cache demande rechargement. Les contrôles du panneau commentaires coordonnent leurs verrous : pas de brouillon perdu, pas de changement silencieux de cible de signalement. Aucun stockage de likes/jetons/identités dans localStorage/sessionStorage, aucune dépendance ajoutée.

Backend : un seul commit de l'action, rollback des écritures non validées en cas d'erreur. La contrainte unique protège au-delà du précontrôle. **Un accusé perdu après commit ne prouve pas un échec**, cas exercé après de vrais commits. SQLite/FK/unicité sont testées ; FOR UPDATE, attentes/deadlocks et toutes courses multi-connexions InnoDB ne sont pas prouvés par ces tests.

## 7. Purge, dashboard et résultats des tests

CommentLike entre dans le graphe interne signé, la jointure Comment, les contrôles FK/moteurs/orphelins, les verrous, le plafond de dépendances, le DELETE avant Comment et les vérifications finales. Un enfant changé invalide l'ancienne confirmation. Rollback testé après de vrais DELETE de likes. **Les cinq clés publiques d'impact/deleted_counts et le code du dashboard restent inchangés.** Les likes n'alimentent aucun huitième indicateur.

| Suite finale — attempt-4 | Résultat | Échecs / erreurs / ignorés |
|---|---:|---|
| Backend | **303 PASS** = 279 précédents + 18 likes + 6 candidate | 0 / 0 / 0 |
| Frontend | **484 PASS** = 428 précédents + 56 likes | 0 échec/annulé/ignoré |
| Lanceur/HTML/WSGI | **16 PASS** | 0 / 0 / 0 |
| **Total** | **803 PASS** | Aucun cumul avec les 723 historiques |

Les tests couvrent deux types de cible et deux comptes, froid/résolu, unicité SQL/FK/cascades, retrait idempotent, anciennes lignes Vote, histoires archivées, commentaire supprimé, bannis/visiteurs/ids/CSRF, vrai flush puis rollback, vrai commit puis accusé perdu, erreurs réseau/timeout/JSON, doubles clics, compte changé, réponses tardives, historique protégé et conservation des signalements/dashboard. Les 18 méthodes backend contiennent aussi plafond de purge incluant les likes et cascade SQL du propriétaire sans supprimer les contributions des autres.

Les tests historiques restent présents et sont adaptés au changement autorisé : neuf→dix tables, 33→35 règles, quatre opérations Swagger ajoutées, commentaire unique au lieu de clics répétés. Le test des répétitions garde explicitement les théories à 1→2 ; les commentaires donnent un seul like puis 409. Les anciennes injections d'erreur UPDATE sont distinguées de l'INSERT, avec assertions de rollback/conservation maintenues.

Passages conservés : attempt-1 backend 298/301 réussis, trois échecs d'attentes/injection devenues obsolètes ; attempt-2 complet 801 PASS ; attempt-3 complet 803 après deux contrôles supplémentaires ; **attempt-4 complet 803 après renforcement de la validation de confirmation et effacement de l'état personnel au départ**. Aucun échec initial effacé ou ajouté aux réussites finales.

Les **sept tests de migration historiques** restent exclus (six reports et un archivage), non exécutés et non comptés comme PASS. Les six nouveaux tests de candidate sont expressément autorisés par 6G.2 : seul son fichier peut exécuter du code de migration/DDL sur comment_likes, uniquement SQLite mémoire. Les commandes Alembic et autres révisions restent bloquées. 6 exécutions de module candidate, 10 opérations DDL autorisées ; aucun accès aux données réelles.

Harnais relu, environnement enfant minimal, dotenv neutralisé avant import, Aiven vidé, connexions exclusivement SQLite :memory: avec FK actives, ATTACH/DETACH bloqués. Réseau/DNS, sous-processus applicatifs, lectures privées et écritures du dépôt interdits ; sondes séparées. **Tous les compteurs interdits des suites finales et du parcours intégré sont à zéro.** Manifeste de 71 sources avec SHA-256.

## 8. Parcours continu et preuves

Via HTML réellement servi en WSGI et contrôleurs JS réels, DOM/transport navigateur simulés : inscription/connexion, commentaire, **ajout → retrait → réajout d'un like d'histoire puis de commentaire**, relecture/navigation, signalement, vrai refus CSRF, réponses perdues, déconnexion et consultation admin. **79 requêtes API, 14 groupes réussis**, séparés des 803 méthodes/cas des suites. donnees.js reste non lu/non exécuté, ses références anciennes sont explicitement omises comme en 6F.2 : aucune couverture intégrale de ces scripts ou recette navigateur revendiquée.

SQL final exclusivement fictif : 1 Vote sur Story 17 et 1 CommentLike sur le commentaire créé, tous deux appartenant au membre réellement inscrit/connecté ; compteur physique historique toujours 0. Les sept nombres administrateur correspondent aux SELECT : deux dossiers (un par catégorie), deux comptes, deux commentaires, deux signalements et zéro proposition pending. Ce sont des observations dans cette mémoire, jamais des valeurs injectées dans le dashboard du site.

Preuves et copies antérieures :

```text
[chemin local privé retiré]
```

`baseline.json`, `before/`, `harness-inspection.json`, `preflight.json`, `attempt-1..4/commands.json` et journaux, `backend.guard.json`, `launcher.guard.json`, gardes Node, `integration-frontend.json`, `integration-sql.json`, `integration-exchanges.json`, omissions, `line-reference-updates.json`, `final-validation.json`. Les scripts de préparation/coordination hors dépôt y restent disponibles ; aucune réponse brute contenant cookie/CSRF/mot de passe n'est journalisée.

## 9. Non validé et actions avant soutenance

**NON EXÉCUTÉS :** Edge réel, serveur HTTP, clavier/lecteur d'écran/mobile/rendu réels, gestion effective des cookies dans Edge, durabilité après arrêt/redémarrage, MySQL/Aiven/TLS, anciennes migrations et chaîne complète, courses SQL multi-connexions et déploiement. Aucune donnée réelle de présentation créée ou modifiée. Un compte/un like ne garantit pas une seule personne physique/un compte ; pas de nouvel anti-spam, traitement de signalements ou lot RGPD.

Avant une recette réelle : valider ce lot ; préparer/réinspecter un kit sur les sources 6G.2 et un jeu isolé ; obtenir l'autorisation serveur/Edge manuel ; traiter la limite du script historique exclu. **Le kit 6F.2 est figé : son manifeste refuse maintenant les sources modifiées**, comportement sûr à conserver ; ne pas le régénérer automatiquement ou lancer run_local.py avec une configuration privée.

Avant une éventuelle activation sur la cible : autoriser l'inventaire des historiques et du schéma ; s'ils sont non nuls/incompatibles, arrêter B et demander la décision de reprise. Contrôler parents/FK/InnoDB, préparer sauvegarde/maintenance/reprise et autoriser séparément la migration. Ne pas annoncer compatibilité MySQL ou données historiques validées depuis SQLite.

À l'oral : **Mélissa** explique bouton/DOM, compte réel et verrou ; **Sylvie**, GET/POST/DELETE, cookie/CSRF et réponse incertaine ; **Mahamadou**, couple unique, FK, COUNT/commit/rollback et protection de l'ancien compteur. Montrer les preuves isolées si le navigateur n'est pas autorisé ; ne jamais peupler la base du site pour embellir les statistiques.

## 10. Verdict et arrêt

**GO pour la revue du développement local A/B et des preuves synthétiques. Aucune autorisation de déploiement ou de migration réelle déduite.** Étape B fonctionnelle uniquement pour historiques compatibles ; les cas incompatibles restent bloqués et protégés jusqu'à décision humaine. La base du site n'a pas été examinée : ne pas déclarer sa reprise terminée.

Aucun changement de branche, commit/push, suppression de travail, lecture de secret/.env, accès MySQL/Aiven, modification Windows, ouverture Edge ou publication de politique RGPD incomplète. Le lot s'arrête après 6G.2, en attente de validation.

**Préservation finale vérifiée :** 31 fichiers préexistants modifiés et sept créés ; 90 autres sources/documents examinés identiques. Colonnes SQL des neuf modèles antérieurs et définition de Vote conservées ; fichiers du dashboard et 115 fichiers de sauvegarde durable identiques par SHA-256. 216 repères de code, 22 remarques jury conservées, réponses historiques des quatre fiches préservées hors liens de lignes/complément courant. 1 017 références Markdown locales et 335 références de lignes contrôlées. État final : **46 fichiers suivis modifiés, 69 non suivis, aucun indexé**, incluant le travail antérieur ; branche, HEAD et empreinte d'index préservés. Reçu final-validation.json hors dépôt.
