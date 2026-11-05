# Index du code pour le jury

> Archive pédagogique datée : les résultats et descriptions ci-dessous concernent le lot indiqué. Les anciens repères de ligne ne décrivent pas la version candidate. Pour préparer la soutenance actuelle, consulter les quatre fiches et le référentiel reliés au sommaire.

> Copie publique de référence : les chemins personnels et liens de travail internes sont retirés. Les preuves et commandes historiques gardent leur date et leur périmètre ; utiliser le README actuel pour le lancement.

## État courant — 2 novembre 2026

Lire d’abord les [supports 6H.1](SUPPORT_JURY_LOT6H1.md), l’[index courant](INDEX_CODE_LOT6H1.md) et la [procédure sur un autre PC](LANCEMENT_AUTRE_PC_LOT6H1.md). Le bilan actuel distingue **854 tests historiques**, recette Edge réussie en SQLite fictif et contrôles documentaires de ce lot. Le modèle actuel contient dix tables et treize FK ; le compte est partagé sur dix pages, les signalements sont contextualisés, les likes de dossier/commentaire sont individuels.

Les compléments et questions ci-dessous conservent leur contexte historique. Les anciennes mentions de fonctions absentes, de neuf tables ou de recette non exécutée ne constituent pas l’état courant. Les 76 questions/réponses historiques restent conservées. Aucun résultat MySQL ou de déploiement n’est ajouté.


[Sommaire](README.md) · [Tests](TESTS_ET_VALIDATION.md) · [Réponses orales](ORAL_JURY.md)

Repères vérifiés **après les commentaires français des étapes 5, 5.1 et des lots 6A/6B/6D, 6C.1, 6C.2 et 6E.2, le 31 octobre 2026**. Les liens ouvrent les fichiers ; aucune ancienne coordonnée de ligne n’est revendiquée actuelle. Les lignes visent la définition, l’événement ou le bloc HTML réel, pas un commentaire ajouté. Elles devront être recalculées si le code évolue ensuite. Les gestionnaires anonymes sont explicitement identifiés comme tels : aucun nom de fonction n’est inventé. Les compléments 5.1 se trouvent en fin d'index.

Les tests et migrations ne sont pas exécutés en ouvrant cet index. Les harnais de recette hors dépôt restent référencés dans le document de tests, pas présentés comme du code livré.

## Serveur, sessions et permissions

| Question possible | Fichier (repère historique) | Nom exact / repère | Rôle | À dire simplement |
|---|---|---|---|---|
| Qui sert le frontend et l’API ? | [run_local.py](../../run_local.py) | `create_local_app` | Compose les ressources publiques et le routage API en WSGI. | « Un processus et une origine ; le middleware distribue les fichiers, Flask traite l’API. » |
| Quelle commande démarre le site ? | [run_local.py](../../run_local.py) | `main` | Charge la configuration et démarre Flask sur loopback. | « run_local.py écoute localement, sans debug, sans migration ni peuplement. » |
| Comment régler Secure ? | [backend/index.py](../../backend/index.py) | `env_to_bool` | Interprète les valeurs textuelles de configuration. | « La chaîne false doit être interprétée, pas seulement testée comme chaîne non vide. » |
| D’où vient le CSRF ? | [backend/index.py](../../backend/index.py) | `get_csrf_token` | Crée un jeton aléatoire lié à la session. | « Login ou me fournit le jeton ; je ne le journalise jamais. » |
| Quels POST sont protégés ? | [backend/index.py](../../backend/index.py) | `protect_session_requests_from_csrf` | Vérifie le CSRF des écritures portant user_id, avec exceptions. | « Le filtre passe GET, login et anonymes ; les vues appliquent encore leurs permissions. » |
| Comment vérifiez-vous une connexion ? | [backend/index.py](../../backend/index.py) | `login_user` | Vérifie le compte/mot de passe puis prépare la session. | « Je vérifie le hash et le bannissement avant de retenir user_id. » |
| Pourquoi appeler me ? | [backend/index.py](../../backend/index.py) | `get_current_user` | Relit le compte courant et renvoie son CSRF. | « Le frontend vérifie encore la session avant une contribution. » |
| Que fait la déconnexion ? | [backend/index.py](../../backend/index.py) | `logout_user` | Vide la session du navigateur. | « Cela ne constitue pas un registre central de révocation de copies du cookie. » |
| Les compteurs sont-ils privés ? | [backend/index.py](../../backend/index.py) | `get_stats` | Retourne trois comptes agrégés par une route publique. | « Les données détaillées protégées passent par d’autres routes. » |
| Comment répondre à une route absente ? | [backend/index.py](../../backend/index.py) | `not_found` | Produit une erreur JSON 404. | « Je distingue ressource absente et liste vide. » |
| Comment traiter les erreurs du framework ? | [backend/index.py](../../backend/index.py) | `handle_api_http_error` | Normalise le JSON API en conservant statut et en-têtes. | « Une erreur HTTP doit rester interprétable par le frontend. » |
| Peut-on faire confiance au cookie seul ? | [backend/api/v1/views/permissions.py](../../backend/api/v1/views/permissions.py) | `get_authenticated_user` | Relit User et refuse le compte absent ou banni. | « La signature protège la session ; la base donne encore l’état actuel du compte. » |
| Qui décide du rôle ? | [backend/api/v1/views/permissions.py](../../backend/api/v1/views/permissions.py) | `admin_required` | Décore une vue et exige le rôle en base. | « Cacher un bouton ne protège pas une route ; Flask contrôle user.is_admin. » |
| Quelle base est choisie ? | [backend/index.py](../../backend/index.py) | `configuration du module (hors fonction)` | Le groupe Aiven complet est prioritaire ; sinon DATABASE_URL ou SQLite. | « Une URL SQLite seule ne neutralise pas une configuration Aiven complète. » |
| Où est le préfixe API ? | [backend/api/v1/views/__init__.py](../../backend/api/v1/views/__init__.py) | `app_views (Blueprint, hors fonction)` | Regroupe les routes sous /api/v1. | « Les modules enregistrent leurs vues sur un seul Blueprint. » |
| Existe-t-il deux applications Flask ? | [backend/api/v1/app.py](../../backend/api/v1/app.py) | `réexport app (hors fonction)` | Réexporte la même application configurée. | « Ce module de compatibilité ne crée pas un second backend. » |

## Modèles, relations et données

| Question possible | Fichier (repère historique) | Nom exact / repère | Rôle | À dire simplement |
|---|---|---|---|---|
| À quoi sert User ? | [backend/models.py](../../backend/models.py) | `User` | Comptes, unicité pseudo/email, hash et états. | « Un compte référence plusieurs contributions ; le client ne choisit pas son rôle. » |
| À quoi sert Category ? | [backend/models.py](../../backend/models.py) | `Category` | Catégories de dossiers, nom unique. | « Une catégorie peut classer plusieurs histoires. » |
| À quoi sert Story ? | [backend/models.py](../../backend/models.py) | `Story` | Dossier, slug unique, auteur/catégorie obligatoires et quatre collections ORM. | « Les collections et les FK ont des responsabilités différentes. » |
| À quoi sert Theory ? | [backend/models.py](../../backend/models.py) | `Theory` | Théorie rattachée au dossier, auteur nullable. | « CASCADE concerne le dossier, SET NULL la référence de l’auteur. » |
| À quoi sert Comment ? | [backend/models.py](../../backend/models.py) | `Comment` | Commentaire avec références et copie du pseudo. | « SET NULL ne supprime pas le pseudo copié ni le contenu. » |
| À quoi sert Vote ? | [backend/models.py](../../backend/models.py) | `Vote` | Vote avec unicité composite utilisateur/dossier. | « Chaque compte peut voter pour plusieurs dossiers, une fois par dossier. » |
| À quoi sert Proposal ? | [backend/models.py](../../backend/models.py) | `Proposal` | Proposition distincte d’une Story, statut pending. | « Il manque encore le parcours d’acceptation/publication. » |
| À quoi sert Report ? | [backend/models.py](../../backend/models.py) | `Report` | FK entière obligatoire vers Comment ; type/target_id calculés pour le JSON. | « Les signalements ne visent que les commentaires et suivent leur suppression ; aucun déclarant n’est stocké. » |
| À quoi sert ColdCaseUpdate ? | [backend/models.py](../../backend/models.py) | `ColdCaseUpdate` | Mise à jour dépendant d’une Story. | « Sa FK seule ne vérifie pas la catégorie Cold Case. » |
| Stockez-vous le mot de passe ? | [backend/models.py](../../backend/models.py) | `User.set_password` | Produit le hash salé avec Werkzeug. | « Le mot de passe brut n’est pas conservé dans la colonne de hash. » |
| Comment comparer une saisie ? | [backend/models.py](../../backend/models.py) | `User.check_password` | Vérifie le mot de passe avec Werkzeug. | « Je ne déchiffre pas un hash pour le comparer. » |
| Le hash sort-il dans le JSON ? | [backend/models.py](../../backend/models.py) | `User.to_dict` | Sérialise seulement les champs publics prévus du compte. | « password_hash est exclu de cette représentation. » |

## Routes API, validation et transactions

| Question possible | Fichier (repère historique) | Nom exact / repère | Rôle | À dire simplement |
|---|---|---|---|---|
| Pourquoi is_valid_password ? | [backend/api/v1/views/users.py](../../backend/api/v1/views/users.py) | `is_valid_password` | Vérifie longueur/composition. | « Cette politique de saisie complète le hachage, sans bloquer à elle seule la force brute. » |
| Pourquoi register_user ? | [backend/api/v1/views/users.py](../../backend/api/v1/views/users.py) | `register_user` | POST users : validation, hash et transaction. | « Le précontrôle aide l’utilisateur ; UNIQUE protège encore le commit. » |
| Pourquoi get_users ? | [backend/api/v1/views/users.py](../../backend/api/v1/views/users.py) | `get_users` | GET users réservé aux administrateurs. | « Les emails de tous les comptes ne sont pas une liste publique. » |
| Pourquoi get_stories ? | [backend/api/v1/views/histoires.py](../../backend/api/v1/views/histoires.py) | `get_stories` | GET public des dossiers et votes. | « Le comptage par dossier fonctionne mais multiplie les requêtes. » |
| Pourquoi get_story_by_slug ? | [backend/api/v1/views/histoires.py](../../backend/api/v1/views/histoires.py) | `get_story_by_slug` | GET public d’un dossier par slug. | « Un slug absent donne 404. » |
| Pourquoi post_story_vote ? | [backend/api/v1/views/histoires.py](../../backend/api/v1/views/histoires.py) | `post_story_vote` | POST vote : auteur de session et unicité. | « Un doublon connu est refusé en 409, une autre erreur reste 500. » |
| Pourquoi get_case_updates ? | [backend/api/v1/views/histoires.py](../../backend/api/v1/views/histoires.py) | `get_case_updates` | GET des mises à jour d’un dossier existant. | « La catégorie Cold Case n’est pas contrôlée ici. » |
| Pourquoi get_theories ? | [backend/api/v1/views/theories.py](../../backend/api/v1/views/theories.py) | `get_theories` | GET public des théories chronologiques. | « Vérifier l’histoire distingue liste vide et dossier absent. » |
| Pourquoi post_theory ? | [backend/api/v1/views/theories.py](../../backend/api/v1/views/theories.py) | `post_theory` | POST théorie : compte, dossier, validation et commit/rollback. | « Add prépare ; commit valide ; rollback annule les changements non validés. » |
| Pourquoi like_theory ? | [backend/api/v1/views/theories.py](../../backend/api/v1/views/theories.py) | `like_theory` | POST incrémente le compteur en SQL. | « Cela évite une écriture de compteur obsolète, mais les likes répétés restent permis. » |
| Pourquoi comment_to_dict ? | [backend/api/v1/views/comments.py](../../backend/api/v1/views/comments.py) | `comment_to_dict` | Ajoute le nombre de signalements à la représentation. | « Le compteur est calculé depuis reports, pas depuis une ancienne colonne comments.reports. » |
| Pourquoi get_story_comments ? | [backend/api/v1/views/comments.py](../../backend/api/v1/views/comments.py) | `get_story_comments` | GET public des commentaires. | « Les commentaires utilisent une lecture publique. » |
| Pourquoi post_story_comment ? | [backend/api/v1/views/comments.py](../../backend/api/v1/views/comments.py) | `post_story_comment` | POST commentaire avec auteur de session. | « Un username arbitraire envoyé par le client ne choisit pas l’auteur. » |
| Pourquoi like_comment ? | [backend/api/v1/views/comments.py](../../backend/api/v1/views/comments.py) | `like_comment` | POST délégué au traitement du couple unique compte/commentaire. | « CommentLike distingue le nouveau like individuel de l'ancien compteur non attribuable. » |
| Pourquoi report_comment ? | [backend/api/v1/views/comments.py](../../backend/api/v1/views/comments.py) | `report_comment` | POST de signalement par identifiant de commentaire. | « Je vérifie cible et motif avant l’insertion. » |
| Pourquoi get_proposals ? | [backend/api/v1/views/proposals.py](../../backend/api/v1/views/proposals.py) | `get_proposals` | GET privé des propositions. | « Le tableau consulte les propositions après contrôle admin. » |
| Pourquoi create_proposal ? | [backend/api/v1/views/proposals.py](../../backend/api/v1/views/proposals.py) | `create_proposal` | POST crée une proposition pending avec transaction. | « Créer une proposition ne publie pas une nouvelle histoire. » |
| Pourquoi post_report ? | [backend/api/v1/views/index.py](../../backend/api/v1/views/index.py) | `post_report` | POST générique acceptant une cible commentaire. | « Le contrôle API est indispensable car target_id n’a pas de FK. » |
| Pourquoi get_admin_reports ? | [backend/api/v1/views/index.py](../../backend/api/v1/views/index.py) | `get_admin_reports` | GET réservé aux administrateurs. | « Les motifs de signalement ne sont pas une lecture publique. » |
| Pourquoi ban_user ? | [backend/api/v1/views/index.py](../../backend/api/v1/views/index.py) | `ban_user` | DELETE marque is_banned sans supprimer la ligne. | « Bannir ne correspond ni à une suppression de compte ni à un effacement RGPD. » |
| Pourquoi get_swagger_json ? | [backend/api/v1/views/index.py](../../backend/api/v1/views/index.py) | `get_swagger_json` | GET du fichier de contrat OpenAPI. | « Un contrat décrit les opérations ; il ne prouve pas leur exécution. » |
| Pourquoi oauth_swagger ? | [backend/api/v1/views/index.py](../../backend/api/v1/views/index.py) | `oauth_swagger` | GET de Swagger UI et configuration CDN. | « Le nom ne signifie pas OAuth ; aucun ajout automatique du CSRF aux POST n’y figure. » |
| Pourquoi json_object ? | [backend/api/v1/views/write_support.py](../../backend/api/v1/views/write_support.py) | `json_object` | Exige un corps JSON objet. | « Une liste peut être du JSON valide mais rester invalide pour cette route. » |
| Pourquoi required_text ? | [backend/api/v1/views/write_support.py](../../backend/api/v1/views/write_support.py) | `required_text` | Contrôle type, caractères, UTF-8 et taille des textes. | « Un caractère peut occuper plusieurs octets ; les deux limites sont distinctes. » |
| Pourquoi get_resource ? | [backend/api/v1/views/write_support.py](../../backend/api/v1/views/write_support.py) | `get_resource` | Borne l’identifiant puis lit par PK. | « La validation précède la requête de ressource. » |
| Pourquoi is_unique_conflict ? | [backend/api/v1/views/write_support.py](../../backend/api/v1/views/write_support.py) | `is_unique_conflict` | Reconnaît les conflits uniques métier SQLite/MySQL. | « Les erreurs MySQL injectées en test ne prouvent aucune connexion Aiven. » |

## Frontend, DOM et échanges HTTP

| Question possible | Fichier (repère historique) | Nom exact / repère | Rôle | À dire simplement |
|---|---|---|---|---|
| Comment fonctionne apiRequest ? | [frontend/api.js](../../frontend/api.js) | `apiRequest` | Centralise fetch, cookies, CSRF, délais, JSON et erreurs. | « Un HTTP 400 ne rejette pas automatiquement fetch ; nous examinons le statut. » |
| Comment fonctionne login ? | [frontend/api.js](../../frontend/api.js) | `login` | Envoie les identifiants et conserve le CSRF en mémoire. | « Le cookie est géré par le navigateur, pas lu directement par JavaScript. » |
| Comment fonctionne getCurrentUser ? | [frontend/api.js](../../frontend/api.js) | `getCurrentUser` | Lit me et rafraîchit le CSRF. | « Les formulaires vérifient la session avant de créer. » |
| Comment fonctionne logout ? | [frontend/api.js](../../frontend/api.js) | `logout` | Appelle logout et vide le CSRF local après succès. | « Le frontend attend la confirmation serveur. » |
| Comment fonctionne register ? | [frontend/api.js](../../frontend/api.js) | `register` | Demande l’inscription classique et attend 201. | « L’inscription ne donne pas le rôle administrateur. » |
| Comment fonctionne createProposal ? | [frontend/api.js](../../frontend/api.js) | `createProposal` | POST JSON titre/contenu, attendu 201. | « La catégorie proposée est déjà incluse dans le contenu. » |
| Comment fonctionne createTheory ? | [frontend/api.js](../../frontend/api.js) | `createTheory` | Vérifie l’id et envoie le POST de théorie. | « L’id est celui du dossier renvoyé par l’API. » |
| Comment fonctionne getStories ? | [frontend/api.js](../../frontend/api.js) | `getStories` | Valide la liste de dossiers reçue. | « Une réponse incohérente ne doit pas être affichée comme une donnée correcte. » |
| Comment fonctionne getStoryBySlug ? | [frontend/api.js](../../frontend/api.js) | `getStoryBySlug` | Encode le slug et valide la réponse. | « Le chemin HTTP ne doit pas être assemblé avec un slug non encodé. » |
| Comment fonctionne getStoryTheories ? | [frontend/api.js](../../frontend/api.js) | `getStoryTheories` | Valide les théories du dossier et leurs id. | « Je refuse les doublons et une réponse portant un autre story_id. » |
| Comment fonctionne getAdminStats ? | [frontend/api.js](../../frontend/api.js) | `getAdminStats` | Valide les trois compteurs de stats. | « Le nom du helper n’ajoute pas une permission à la route publique. » |
| Comment fonctionne getAdminProposals ? | [frontend/api.js](../../frontend/api.js) | `getAdminProposals` | Lit les propositions via la route privée. | « Flask garde le dernier mot sur les droits. » |
| Comment fonctionne getAdminReports ? | [frontend/api.js](../../frontend/api.js) | `getAdminReports` | Lit les signalements via la route privée. | « Le format de réponse est aussi contrôlé côté interface. » |
| Comment fonctionne getStoryCategory ? | [frontend/app.js](../../frontend/app.js) | `getStoryCategory` | Associe les catégories fixes 1 et 2. | « Cette hypothèse dépend de la préparation des données. » |
| Comment fonctionne getStoryImageSources ? | [frontend/app.js](../../frontend/app.js) | `getStoryImageSources` | Prépare les sources d’image et replis. | « Les URL acceptées se résolvent en HTTP(S), puis viennent les sources locales. » |
| Comment fonctionne createStoryImage ? | [frontend/app.js](../../frontend/app.js) | `createStoryImage` | Gère les erreurs d’image sans boucle de repli. | « Après la dernière source, un texte indique l’indisponibilité. » |
| Comment fonctionne makeCard ? | [frontend/app.js](../../frontend/app.js) | `makeCard` | Crée les éléments DOM d’une carte. | « textContent affiche les valeurs comme texte, pas comme HTML. » |
| Comment fonctionne loadStories ? | [frontend/app.js](../../frontend/app.js) | `loadStories` | Charge puis filtre les dossiers selon la page. | « La recherche porte ensuite sur les données déjà chargées. » |
| Comment fonctionne loadStory ? | [frontend/app.js](../../frontend/app.js) | `loadStory` | Charge un dossier par son slug et affiche le récit. | « Une absence donne un message de dossier introuvable. » |
| Comment fonctionne loadTheoryStories ? | [frontend/app.js](../../frontend/app.js) | `loadTheoryStories` | Alimente le sélecteur de création avec les vrais id. | « Le rang d’une option n’est pas l’identifiant de la base. » |
| Comment fonctionne cancelRequest ? | [frontend/theories-list.js](../../frontend/theories-list.js) | `cancelRequest` | Invalide et annule les lectures précédentes. | « Le compteur empêche une ancienne réponse de remplacer la sélection actuelle. » |
| Comment fonctionne theoryCard ? | [frontend/theories-list.js](../../frontend/theories-list.js) | `theoryCard` | Construit une contribution en texte dans le DOM. | « Le contenu reçu n’est pas injecté comme HTML. » |
| Comment fonctionne loadSelectedTheories ? | [frontend/theories-list.js](../../frontend/theories-list.js) | `loadSelectedTheories` | Charge la lecture publique sélectionnée. | « Le lecteur est indépendant du formulaire et s’actualise explicitement. » |
| Comment fonctionne loadDossiers ? | [frontend/theories-list.js](../../frontend/theories-list.js) | `loadDossiers` | Charge les choix et gère l’état vide/erreur. | « Une erreur de chargement n’est pas remplacée par donnees.js. » |
| Comment fonctionne clearData ? | [frontend/admin-dashboard.js](../../frontend/admin-dashboard.js) | `clearData` | Masque et vide les résultats précédents. | « Après un refus, je ne laisse pas les anciennes données admin visibles. » |
| Comment fonctionne blockAccess ? | [frontend/admin-dashboard.js](../../frontend/admin-dashboard.js) | `blockAccess` | Annule le chargement après 401/403 courant. | « Un refus de session ou de rôle nettoie l’interface. » |
| Comment fonctionne displayData ? | [frontend/admin-dashboard.js](../../frontend/admin-dashboard.js) | `displayData` | Affiche compteurs, propositions et signalements. | « Ce tableau est une consultation, pas un outil de publication. » |
| Comment fonctionne loadDashboard ? | [frontend/admin-dashboard.js](../../frontend/admin-dashboard.js) | `loadDashboard` | Vérifie le rôle puis charge en parallèle. | « La vérification client accompagne les protections serveur, elle ne les remplace pas. » |
| La recherche appelle-t-elle la base à chaque frappe ? | [frontend/app.js](../../frontend/app.js) | `gestionnaire anonyme input de recherche` | Filtre pageStories en mémoire. | « Le titre et le résumé sont comparés au texte saisi. » |
| Comment évitez-vous le double POST ? | [frontend/app.js](../../frontend/app.js) | `gestionnaire anonyme submit de theory-form` | Valide, verrouille, relit me puis crée la théorie. | « Le booléen sending protège pendant l’attente ; le lecteur reste à actualiser. » |
| Pourquoi la catégorie figure-t-elle dans le texte ? | [frontend/app.js](../../frontend/app.js) | `gestionnaire anonyme submit de proposal-form` | Prépare le contenu puis crée une proposition. | « Il n’y a pas de category_id de proposition ni de pièce jointe. » |
| Pourquoi me avant inscription ? | [frontend/app.js](../../frontend/app.js) | `gestionnaire anonyme submit de signup-form` | Gère aussi l’inscription avec une session préexistante. | « Si me répond 401, l’inscription anonyme reste possible. » |
| Comment fonctionne l’entrée administrateur ? | [frontend/app.js](../../frontend/app.js) | `gestionnaire anonyme submit de login-form` | Appelle le même login puis contrôle la redirection. | « Le rôle JavaScript guide ; le serveur protège les routes. » |
| Où est le bouton de déconnexion ? | [frontend/app.js](../../frontend/app.js) | `bloc sessionControls (hors fonction nommée)` | Restaure la zone de session lorsqu’elle est présente. | « L’accueil contient cette zone ; toutes les pages ne l’affichent pas. » |

## Tests : repères de preuve, pas de nouvelle exécution

| Question possible | Fichier (repère historique) | Nom exact / repère | Rôle | À dire simplement |
|---|---|---|---|---|
| Comment les tests isolent-ils Flask ? | [backend/tests/test_reports.py](../../backend/tests/test_reports.py) | `ReportTests.setUpClass` | Configure l’environnement et les gardes de la suite de référence. | « SQLite mémoire et données synthétiques ; les gardes ne sont pas une preuve Aiven. » |
| Qu’assertent les tests API ? | [backend/tests/test_users_votes.py](../../backend/tests/test_users_votes.py) | `UsersVotesTests.test_users_rejects_nonobject_and_absent_json` | Vérifie les réponses de refus aux corps invalides. | « Une réponse et son statut doivent correspondre au contrat. » |
| Le lanceur ouvre-t-il un port en test ? | [tests/test_run_local.py](../../tests/test_run_local.py) | `LocalFrontendTests.setUpClass` | Interdit sockets et SQL, puis importe le lanceur. | « Le client de test est WSGI, pas un serveur HTTP réel. » |
| Comment prouvez-vous les fichiers servis ? | [tests/test_run_local.py](../../tests/test_run_local.py) | `LocalFrontendTests.test_root_serves_existing_homepage` | Compare les octets de réponse avec le fichier de l’accueil. | « Le middleware rend les vrais fichiers avec une API factice. » |
| Où le DOM est-il simulé ? | [frontend/tests/proposals.test.cjs](../../frontend/tests/proposals.test.cjs) | `mount` | Fabrique formulaire, gestionnaires et API pour exécuter les scripts. | « node:vm ne remplace pas un navigateur réel. » |


## Compléments de repérage — étape 5.1

| Question possible | Fichier (repère historique) | Nom exact / repère | Rôle | À dire simplement |
|---|---|---|---|---|
| Quels champs partent vers le lecteur ? | [backend/api/v1/views/theories.py](../../backend/api/v1/views/theories.py) | `theory_to_dict` | Prépare les champs JSON et la date ISO. | « Sérialiser ne valide pas une transaction. » |
| Comment représenter une proposition ? | [backend/api/v1/views/proposals.py](../../backend/api/v1/views/proposals.py) | `proposal_to_dict` | Prépare champs et dates pour JSON. | « Les permissions sont contrôlées par la route. » |
| Le dossier contient-il ses contributions ? | [backend/models.py](../../backend/models.py) | `Story.to_dict` | Sérialise les colonnes sans collections liées. | « Les contributions ont leurs routes de lecture. » |
| Le pseudo disparaît-il avec la FK ? | [backend/models.py](../../backend/models.py) | `Comment.to_dict` | Conserve le pseudo copié dans le JSON. | « SET NULL ne supprime pas cette copie. » |
| La cible devient-elle une FK ? | [backend/models.py](../../backend/models.py) | `Report.to_dict` | Expose une cible textuelle. | « La conversion JSON ne crée pas de contrainte SQL. » |
| Une mise à jour change-t-elle la catégorie ? | [backend/models.py](../../backend/models.py) | `ColdCaseUpdate.to_dict` | Prépare les champs de lecture. | « Sérialiser ne modifie pas le dossier. » |
| Pourquoi vérifier la forme des dossiers ? | [frontend/api.js](../../frontend/api.js) | `isStory` | Vérifie les champs utilisés pour le DOM. | « Une réponse incohérente provoque une erreur. » |
| Pourquoi vérifier les listes admin ? | [frontend/api.js](../../frontend/api.js) | `isAdminList` | Contrôle identifiants, textes et dates. | « Le format ne remplace pas les droits serveur. » |
| Comment démarrer une attente visible ? | [frontend/theories-list.js](../../frontend/theories-list.js) | `beginRequest` | Prépare contrôleur, version et état DOM. | « Le bouton et aria-busy indiquent le chargement. » |
| Qui peut terminer le chargement ? | [frontend/theories-list.js](../../frontend/theories-list.js) | `finishRequest` | Ne termine que la version courante. | « Une ancienne réponse ne réactive pas le bouton. » |
| Quel fuseau pour les théories ? | [frontend/theories-list.js](../../frontend/theories-list.js) | `publicationDate` | Applique UTC puis affiche Paris. | « Les dates API sans suffixe suivent une convention. » |
| Comment invalider le tableau précédent ? | [frontend/admin-dashboard.js](../../frontend/admin-dashboard.js) | `cancelRequest` | Annule et incrémente la version. | « Annulation et version ont des rôles complémentaires. » |
| Les dates stockées sont-elles modifiées ? | [frontend/admin-dashboard.js](../../frontend/admin-dashboard.js) | `publicationDate` | Convertit uniquement leur affichage. | « La base reste inchangée. » |
| Une carte admin publie-t-elle ? | [frontend/admin-dashboard.js](../../frontend/admin-dashboard.js) | `proposalCard` | Construit une carte de consultation en texte. | « Afficher un statut ne déclenche aucune action. » |
| Consulter traite-t-il le signalement ? | [frontend/admin-dashboard.js](../../frontend/admin-dashboard.js) | `reportCard` | Affiche cible, motif et statut. | « Aucun changement de statut ne se produit ici. » |
| Que faire en quittant le tableau ? | [frontend/admin-dashboard.js](../../frontend/admin-dashboard.js) | `pagehide (gestionnaire anonyme)` | Annule et efface les résultats. | « Ce gestionnaire est anonyme. » |
| Que faire au retour depuis le cache ? | [frontend/admin-dashboard.js](../../frontend/admin-dashboard.js) | `pageshow (gestionnaire anonyme)` | Recharge après restauration de page. | « La session est revérifiée, sans surveillance continue. » |
| Quel moteur utilise Alembic ? | [migrations/env.py](../../migrations/env.py) | `get_engine` | Retrouve le moteur configuré par Flask-Migrate. | « Ne pas importer ce module pour une lecture statique. » |
| Peut-on afficher cette URL ? | [migrations/env.py](../../migrations/env.py) | `get_engine_url` | Prépare une URL complète pour Alembic. | « Elle peut contenir des identifiants privés. » |
| Que comparent les migrations ? | [migrations/env.py](../../migrations/env.py) | `get_metadata` | Retourne les métadonnées des modèles. | « Elles ne prouvent pas le schéma déployé. » |
| Que signifie offline ? | [migrations/env.py](../../migrations/env.py) | `run_migrations_offline` | Produit le SQL sans connexion à la base. | « Produire du SQL ne signifie pas appliquer une migration. » |
| Que signifie online ? | [migrations/env.py](../../migrations/env.py) | `run_migrations_online` | Ouvre la connexion et le contexte Alembic. | « Ce chemin reste non exécuté en 5.1. » |
| Pourquoi éviter une révision vide ? | [migrations/env.py](../../migrations/env.py) | `run_migrations_online.process_revision_directives` | Retire les directives sans changement détecté. | « Cela concerne autogenerate. » |
| Que fait upgrade dans 3111f5767fc6 ? | [migrations/versions/3111f5767fc6_ajoute_les_regles_on_delete.py](../../migrations/versions/3111f5767fc6_ajoute_les_regles_on_delete.py) | `upgrade` | Décrit une évolution du schéma. | « Aucune exécution attestée ici ; le schéma inverse ne restaure pas les données. » |
| Que fait downgrade dans 3111f5767fc6 ? | [migrations/versions/3111f5767fc6_ajoute_les_regles_on_delete.py](../../migrations/versions/3111f5767fc6_ajoute_les_regles_on_delete.py) | `downgrade` | Décrit son évolution inverse. | « Aucune exécution attestée ici ; le schéma inverse ne restaure pas les données. » |
| Que fait upgrade dans 82deda84bc35 ? | [migrations/versions/82deda84bc35_remove_legacy_comment_reports_counter.py](../../migrations/versions/82deda84bc35_remove_legacy_comment_reports_counter.py) | `upgrade` | Décrit une évolution du schéma. | « Aucune exécution attestée ici ; le schéma inverse ne restaure pas les données. » |
| Que fait downgrade dans 82deda84bc35 ? | [migrations/versions/82deda84bc35_remove_legacy_comment_reports_counter.py](../../migrations/versions/82deda84bc35_remove_legacy_comment_reports_counter.py) | `downgrade` | Décrit son évolution inverse. | « Aucune exécution attestée ici ; le schéma inverse ne restaure pas les données. » |
| Que fait upgrade dans 921687c1bd7c ? | [migrations/versions/921687c1bd7c_baseline_schema.py](../../migrations/versions/921687c1bd7c_baseline_schema.py) | `upgrade` | Décrit une évolution du schéma. | « Aucune exécution attestée ici ; le schéma inverse ne restaure pas les données. » |
| Que fait downgrade dans 921687c1bd7c ? | [migrations/versions/921687c1bd7c_baseline_schema.py](../../migrations/versions/921687c1bd7c_baseline_schema.py) | `downgrade` | Décrit son évolution inverse. | « Aucune exécution attestée ici ; le schéma inverse ne restaure pas les données. » |
| Que fait upgrade dans a590c8aac613 ? | [migrations/versions/a590c8aac613_add_reports_bans_and_cold_case_updates.py](../../migrations/versions/a590c8aac613_add_reports_bans_and_cold_case_updates.py) | `upgrade` | Décrit une évolution du schéma. | « Aucune exécution attestée ici ; le schéma inverse ne restaure pas les données. » |
| Que fait downgrade dans a590c8aac613 ? | [migrations/versions/a590c8aac613_add_reports_bans_and_cold_case_updates.py](../../migrations/versions/a590c8aac613_add_reports_bans_and_cold_case_updates.py) | `downgrade` | Décrit son évolution inverse. | « Aucune exécution attestée ici ; le schéma inverse ne restaure pas les données. » |

## Lot 6A — utilisateurs et bannissement

| Question possible | Fichier (repère historique) | Nom exact / repère | Rôle | À dire simplement |
|---|---|---|---|---|
| Quels champs sont réservés à l’administration ? | [backend/api/v1/views/admin_users_support.py](../../backend/api/v1/views/admin_users_support.py) | `admin_user_to_dict` | Sérialise le compte avec is_banned. | « La réponse publique reste inchangée. » |
| Où est la règle de bannissement commune ? | [backend/api/v1/views/admin_users_support.py](../../backend/api/v1/views/admin_users_support.py) | `ban_user_account` | Vérifie la cible et valide ou annule la transaction. | « Les deux routes refusent tous les administrateurs. » |
| Pourquoi une route par identifiant ? | [backend/api/v1/views/index.py](../../backend/api/v1/views/index.py) | `ban_user_by_id` | POST admin par id stable. | « Un pseudo peut contenir une barre oblique. » |
| Quel format de compte accepte le panneau ? | [frontend/api.js](../../frontend/api.js) | `isAdminUser` | Contrôle id, pseudo et booléens. | « Le rôle affiché ne remplace pas le serveur. » |
| Comment lire la liste privée ? | [frontend/api.js](../../frontend/api.js) | `getAdminUsers` | GET users et validation de la liste. | « Les doublons et formats incohérents sont refusés. » |
| Comment demander le bannissement ? | [frontend/api.js](../../frontend/api.js) | `banAdminUser` | POST par id, attendu 200 et statut valide. | « Aucune répétition automatique du POST. » |
| Comment intégrer le panneau au tableau ? | [frontend/admin-users.js](../../frontend/admin-users.js) | `createAdminUsersPanel` | Expose load et clear au coordinateur existant. | « Les six compteurs sont conservés. » |
| Comment effacer les comptes au refus ? | [frontend/admin-users.js](../../frontend/admin-users.js) | `clear` | Annule et vide les données privées. | « Une ancienne réponse ne les restaure pas. » |
| Comment bloquer les doubles clics ? | [frontend/admin-users.js](../../frontend/admin-users.js) | `begin` | Prépare une version et un chargement exclusif. | « Le verrou est posé avant la première attente. » |
| Qui traite un 401 ou 403 ? | [frontend/admin-users.js](../../frontend/admin-users.js) | `accessOptions` | Nettoie puis prévient le tableau global. | « Un 409 reste un refus métier local. » |
| Quand réactiver Actualiser ? | [frontend/admin-users.js](../../frontend/admin-users.js) | `finish` | Termine seulement la version courante. | « Une ancienne requête ne change pas l’état actuel. » |
| Comment afficher les comptes ? | [frontend/admin-users.js](../../frontend/admin-users.js) | `displayUsers` | DOM et textContent, bouton seulement si éligible. | « Les emails ne sont pas montrés. » |
| Comment vérifier le statut après action ? | [frontend/admin-users.js](../../frontend/admin-users.js) | `readUsers` | Relit et affiche la liste du serveur. | « Une réponse tardive est écartée. » |
| Comment recharger le panneau ? | [frontend/admin-users.js](../../frontend/admin-users.js) | `load` | Revérifie la session et charge les utilisateurs. | « Le rôle doit être strictement true. » |
| Que faire si le résultat est incertain ? | [frontend/admin-users.js](../../frontend/admin-users.js) | `ban` | Confirmation, POST unique et relecture. | « Un timeout ne prouve pas un rollback serveur. » |
| Comment prouver la conservation des contributions ? | [backend/tests/test_admin_users.py](../../backend/tests/test_admin_users.py) | `AdminUsersTests` | Comparaison des neuf tables et tests des deux routes. | « Seul is_banned doit changer. » |
| Comment tester le panneau sans navigateur ? | [frontend/tests/admin-users.test.cjs](../../frontend/tests/admin-users.test.cjs) | `mount` | Exécute les vrais scripts avec DOM et API fictifs. | « Les réponses tardives et le timeout sont pilotés. » |

## Lot 6B — consultation des dossiers

| Question possible | Fichier (repère historique) | Nom exact / repère | Rôle | À dire simplement |
|---|---|---|---|---|
| Comment ajouter la consultation sans nouvelle API ? | [frontend/admin-stories.js](../../frontend/admin-stories.js) | `createAdminStoriesPanel` | Reçoit la liste validée du coordinateur. | « Aucun fetch ni écriture de dossier. » |
| Que faire à la perte d’accès ? | [frontend/admin-stories.js](../../frontend/admin-stories.js) | `clear` | Vide les dossiers et désactive les contrôles. | « Le tableau nettoie aussi les utilisateurs. » |
| Comment annoncer le chargement ? | [frontend/admin-stories.js](../../frontend/admin-stories.js) | `begin` | Prépare attente, message et aria-busy. | « Aucun ancien dossier ne reste visible. » |
| Que montrer pour un id inconnu ? | [frontend/admin-stories.js](../../frontend/admin-stories.js) | `category` | Réutilise le classement 1/2 et indique les autres ids. | « Le nom réel n’est pas fourni par cette API. » |
| Comment utiliser un slug sûr ? | [frontend/admin-stories.js](../../frontend/admin-stories.js) | `detailLink` | Encode le slug exact vers la fiche relative. | « Aucun slug fabriqué à partir du titre. » |
| Comment afficher un titre non fiable ? | [frontend/admin-stories.js](../../frontend/admin-stories.js) | `card` | Crée le DOM avec textContent. | « Le contenu reçu reste du texte. » |
| La recherche modifie-t-elle les données ? | [frontend/admin-stories.js](../../frontend/admin-stories.js) | `render` | Combine titre et catégorie en mémoire. | « Les compteurs et la base ne changent pas. » |
| Quand activer les contrôles ? | [frontend/admin-stories.js](../../frontend/admin-stories.js) | `display` | Valide et copie les champs utiles, puis affiche. | « Le coordinateur vérifie session et version. » |
| La fixture correspond-elle à Flask ? | [backend/tests/test_admin_stories_read.py](../../backend/tests/test_admin_stories_read.py) | `AdminStoriesReadTests` | Compare la réponse réelle et les neuf tables. | « Les lectures ne changent aucune ligne. » |
| Comment tester toute la coordination ? | [frontend/tests/admin-stories.test.cjs](../../frontend/tests/admin-stories.test.cjs) | `mount` | Charge les vrais scripts avec la fixture partagée. | « Compte les requêtes et pilote les réponses tardives. » |

## Lot 6D — propositions en attente

| Question possible | Fichier (repère historique) | Nom exact / repère | Rôle | À dire simplement |
|---|---|---|---|---|
| Comment compter uniquement les propositions en attente ? | [frontend/admin-dashboard.js](../../frontend/admin-dashboard.js) | `Calcul dans displayData` | Réutilise le GET privé validé et teste le statut exact pending. | « Aucun fetch ni écriture supplémentaire. » |
| Quel contrat API soutient le compteur ? | [backend/tests/test_admin_pending_stats.py](../../backend/tests/test_admin_pending_stats.py) | `AdminPendingStatsTests` | Exerce permissions, statuts et contrat public inchangé. | « SQLite mémoire fictive, sans serveur. » |
| La fixture correspond-elle à la réponse réelle ? | [backend/tests/test_admin_pending_stats.py](../../backend/tests/test_admin_pending_stats.py) | `test_private_list_matches_complete_shared_frontend_fixture` | Compare exactement les sept champs de GET /proposals. | « Deux pending, approved et rejected. » |
| Comment vérifier que les GET ne changent aucune donnée ? | [backend/tests/test_admin_pending_stats.py](../../backend/tests/test_admin_pending_stats.py) | `snapshot` | Capture les neuf tables pour comparaison avant/après. | « Seules les lectures sont comparées, préparation fictive distincte. » |

## Archivage réversible — lot 6C phase 1

| Sujet | Fichier (repère historique) | Repère exact | Rôle |
|---|---|---|---|
| État minimal | [backend/models.py](../../backend/models.py) | `archived_at = db.Column(db.DateTime, nullable=True)` | Date UTC nullable ; NULL signifie actif. |
| Visibilité et parent | [backend/api/v1/views/story_visibility.py](../../backend/api/v1/views/story_visibility.py) | `def get_active_story(identifier, *, lock=False):` | Filtrer les actifs ; demander le verrou parent pour les contributions. |
| Accès administratif | [backend/api/v1/views/admin_stories.py](../../backend/api/v1/views/admin_stories.py) | `def archive_admin_required(view):` | Réutiliser le rôle en base et normaliser les erreurs SQL du contrôle. |
| Liste privée | [backend/api/v1/views/admin_stories.py](../../backend/api/v1/views/admin_stories.py) | `def get_admin_stories():` | Actifs, archives ou tous ; filtre state validé. |
| Contenu privé | [backend/api/v1/views/admin_stories.py](../../backend/api/v1/views/admin_stories.py) | `def get_admin_story(story_id):` | Lire le récit et ses contributions conservées. |
| Transaction | [backend/api/v1/views/admin_stories.py](../../backend/api/v1/views/admin_stories.py) | `def set_story_archive(story_id, *, archived):` | Verrou, idempotence, flush, commit et rollback. |
| Archiver | [backend/api/v1/views/admin_stories.py](../../backend/api/v1/views/admin_stories.py) | `def archive_story(story_id):` | POST privé protégé par session/rôle et CSRF global. |
| Restaurer | [backend/api/v1/views/admin_stories.py](../../backend/api/v1/views/admin_stories.py) | `def restore_story(story_id):` | Remettre le même dossier actif sans recréer ses enfants. |
| Contrat archives | [frontend/api.js](../../frontend/api.js) | `async function getAdminStories({ signal, onAccessDenied } = {}) {` | Valider la liste administrative et ses dates/états. |
| Contrat détail | [frontend/api.js](../../frontend/api.js) | `async function getAdminStory(storyId, { signal, onAccessDenied } = {}) {` | Valider la cible et les contributions de la lecture privée. |
| Contrat écriture | [frontend/api.js](../../frontend/api.js) | `async function changeAdminStoryArchive(storyId, archived, { signal, onAccessDenied } = {}) {` | POST unique, CSRF, validation du reçu, aucun retry. |
| Confirmation et verrou | [frontend/admin-stories.js](../../frontend/admin-stories.js) | `async function change(story) {` | Confirmer, bloquer les doubles clics et demander la relecture globale. |
| Afficher une archive | [frontend/admin-stories.js](../../frontend/admin-stories.js) | `async function readArchive(story, button, container) {` | Lire le contenu privé et construire des paragraphes de texte. |
| Relecture et statistiques | [frontend/admin-dashboard.js](../../frontend/admin-dashboard.js) | `async function loadDashboard(outcome = null) {` | Relire les sources, refuser les doublons et afficher l’état constaté. |
| Migration préparée | [migrations/versions/c6c100000001_add_story_archive_date.py](../../migrations/versions/c6c100000001_add_story_archive_date.py) | `def upgrade():` | Ajouter la date nullable ; aucune application à une base réelle. |
| Preuves serveur | [backend/tests/test_story_archiving.py](../../backend/tests/test_story_archiving.py) | `class StoryArchivingTests(unittest.TestCase):` | Données fictives, FK SQLite, conservation, accès et rollback réel. |
| Preuves interface | [frontend/tests/admin-archives.test.cjs](../../frontend/tests/admin-archives.test.cjs) | `test('double submission stays locked through write and global re-read', async () => {` | Une seule écriture pendant POST puis relecture. |

## Suppression définitive — lot 6C.2 livré

| Sujet | Fichier (repère historique) | Repère exact | Rôle |
|---|---|---|---|
| Révision de confirmation | [backend/models.py](../../backend/models.py) | `management_revision = db.Column(` | Une seule révision aléatoire, sans reçu ni historique. |
| Relation des signalements | [backend/models.py](../../backend/models.py) | `moderation_reports = db.relationship(` | Collection nommée sans recréer l’ancien compteur reports. |
| Cible unique | [backend/models.py](../../backend/models.py) | `comment_id = db.Column(` | FK entière obligatoire vers Comment avec CASCADE. |
| Préconditions SQL | [backend/api/v1/views/story_deletion_support.py](../../backend/api/v1/views/story_deletion_support.py) | `def require_integrity():` | FK activées, schéma achevé, moteur et anciennes références contrôlés. |
| État de confirmation | [backend/api/v1/views/story_deletion_support.py](../../backend/api/v1/views/story_deletion_support.py) | `def snapshot(story_id, *, lock=True):` | Graphe ordonné/verrouillé, limite et empreinte complète. |
| Aperçu | [backend/api/v1/views/story_deletion_support.py](../../backend/api/v1/views/story_deletion_support.py) | `def deletion_preview(story_id):` | Lecture sans écriture, titre/impact et signature de cinq minutes. |
| Accord renforcé | [backend/api/v1/views/story_deletion_support.py](../../backend/api/v1/views/story_deletion_support.py) | `def confirm_deletion(story_id):` | Titre exact et acquittement, sans prolonger le délai. |
| Transaction de purge | [backend/api/v1/views/story_deletion_support.py](../../backend/api/v1/views/story_deletion_support.py) | `def delete_story(story_id):` | Réserver la révision, supprimer le graphe, contrôler puis commit unique. |
| Erreurs explicites | [backend/api/v1/views/story_deletion_support.py](../../backend/api/v1/views/story_deletion_support.py) | `def run_deletion_action(action, story_id):` | Rollback et JSON sans détail SQL ; contention distinguée. |
| Route définitive | [backend/api/v1/views/admin_stories.py](../../backend/api/v1/views/admin_stories.py) | `def delete_story_permanently(story_id):` | DELETE privé avec protection rôle et CSRF global. |
| Reprise refusée | [migrations/versions/c6c200000001_comment_reports_and_story_revision.py](../../migrations/versions/c6c200000001_comment_reports_and_story_revision.py) | `def inspect_legacy(bind):` | Valider toutes les anciennes cibles avant le premier DDL. |
| Migration préparée | [migrations/versions/c6c200000001_comment_reports_and_story_revision.py](../../migrations/versions/c6c200000001_comment_reports_and_story_revision.py) | `def upgrade():` | Cible relationnelle et révision ; aucune base réelle migrée. |
| Contrat d’aperçu | [frontend/api.js](../../frontend/api.js) | `async function getStoryDeletionPreview(storyId, { signal, onAccessDenied } = {}) {` | Valider la réponse avant ouverture du dialogue. |
| DELETE conditionnel | [frontend/api.js](../../frontend/api.js) | `async function deleteAdminStory(storyId, preview, token, { signal, onAccessDenied } = {}) {` | Deux en-têtes autorisés, CSRF protégé, résultat vérifié. |
| Après timeout | [frontend/api.js](../../frontend/api.js) | `async function verifyAdminStoryState(storyId, { signal, onAccessDenied } = {}) {` | Relire présence/absence sans attribuer une opération perdue. |
| Dialogue | [frontend/admin-stories.js](../../frontend/admin-stories.js) | `function askPermanentDeletion(preview) {` | Titre, décompte et accord en texte ; annulation sans effet. |
| Verrou d’interface | [frontend/admin-stories.js](../../frontend/admin-stories.js) | `async function permanentlyDelete(story) {` | Une intention jusqu’à relecture, aucune relance de DELETE. |
| Preuves de reprise | [backend/tests/test_report_migration.py](../../backend/tests/test_report_migration.py) | `class ReportMigrationTests(unittest.TestCase):` | Schéma fictif et FK ON, anomalies refusées avant DDL. |
| Preuves de transaction | [backend/tests/test_story_deletion.py](../../backend/tests/test_story_deletion.py) | `class StoryDeletionTests(unittest.TestCase):` | Témoins, rollback réel et COMMIT incertain. |

## Repères ajoutés en 6E.2 — 31 octobre 2026

Les fonctions applicatives JavaScript/Python restent inchangées ; aucun nom n'est inventé pour les blocs HTML. Les repères historiques sont conservés ; les attributs accessibles n'ajoutent aucun traitement de données.

| Question | Fichier (repère historique) | Repère réel | Rôle |
|---|---|---|---|
| Que voit-on avant l'inscription ? | [inscription.html](../../frontend/inscription.html) | paragraphe signup-data-notice | Informations provisoires avant les champs |
| Pourquoi la théorie peut-elle être publique ? | [theories.html](../../frontend/theories.html) | paragraphe theory-data-notice | Information avant envoi, sans modifier chargement ou validation |
| Une proposition est-elle publiée ? | [proposer-histoire.html](../../frontend/proposer-histoire.html) | paragraphe proposal-data-notice | Envoi administratif, sans publication automatique |
| Comment présenter les notices ? | [styles.css](../../frontend/styles.css) | classe data-notice, hors fonction | Style ajouté sans changement des sélecteurs existants |
| Où reste la page non publiable ? | projet de confidentialité (pièce interne non diffusée) | main confidentialite-contenu, bloc statique | Page de revue hors des fichiers servis |
| Qu'est-ce qui protège les contrats HTML ? | [test_rgpd_information.py](../../tests/test_rgpd_information.py) | PrivacyInformationTests | Huit tests de contrôles, notices et non-publication ; pas une fonction du produit |

La procédure manuelle (archive interne non diffusée) et le [bilan](BILAN_LOT6E2.md) donnent les décisions non validées, limites et preuves.

## Parcours de modération 6E.3 — 1er novembre 2026

| Question | Fichier (repère historique) | Repère réel | Rôle |
|---|---|---|---|
| Comment prouver qu'un signalement affichable correspond à la base de test ? | [test_moderation_journey.py](../../backend/tests/test_moderation_journey.py) | ModerationJourneyTests.test_real_api_writes_match_test_database_and_admin_data_sources | Requêtes WSGI, vrais commits SQLite mémoire, lectures et FK ; aucune fonction ajoutée au produit |

Les 197 cibles précédentes sont conservées ; ce repère porte l'index à 198. La preuve ne montre pas une interface publique de commentaire/signalement inexistante. [Résultats et limites](BILAN_LOT6E3.md).

## Interface publique 6F.1 — 1er novembre 2026

Les mentions d'interface absente ci-dessus décrivent l'état historique de 6E.3. Les formulaires sont maintenant développés ; leur recette navigateur reste non exécutée.

| Question | Fichier (repère historique) | Repère réel | Rôle |
|---|---|---|---|
| Où commence le parcours public ? | [comments.js](../../frontend/comments.js) | mountStoryComments | Panneau démarré seulement après réception du dossier réel |
| Comment respecter le champ TEXT ? | [comments.js](../../frontend/comments.js) | validatedText | Texte requis, UTF-8 et Unicode valides ; le serveur revalide |
| Pourquoi aucun double envoi ni faux succès ? | [comments.js](../../frontend/comments.js) | submit | Verrou, session/CSRF, confirmation et résultats incertains |
| Comment lire les commentaires ? | [api.js](../../frontend/api.js) | getStoryComments | GET public, structure et dossier vérifiés |
| Comment publier un commentaire ? | [api.js](../../frontend/api.js) | createComment | POST text, 201 et commentaire du bon dossier |
| Comment garantir la bonne cible ? | [api.js](../../frontend/api.js) | reportComment | POST reason sur le commentaire, réponse type/target_id vérifiée |

Les 198 cibles antérieures sont conservées, avec leurs lignes actualisées lorsque nécessaire : **204 repères**. [Bilan et preuves](BILAN_LOT6F1.md).

## Préparation de recette 6F.2

[Bilan d'intégration](BILAN_LOT6F2.md), [protocole Edge](RECETTE_MANUELLE_LOT6F2.md), [scénario oral](SCENARIO_SOUTENANCE_LOT6F2.md), [kit de vérification isolé](../../tools/recette_lot6f2.py) et [manifeste de sources](../../tools/recette_lot6f2_sources.json). Ces scripts préparent les essais ; ils ne constituent pas une nouvelle architecture applicative. Les **204 repères de code produit restent inchangés**. Aucun serveur ou navigateur n'est lancé pendant 6F.2.

## Likes individuels 6G.2

| Question | Fichier (repère historique) | Repère |
|---|---|---|
| Pourquoi une nouvelle relation ? | [models.py](../../backend/models.py) | CommentLike |
| Comment préserver les compteurs historiques ? | [likes.py](../../backend/api/v1/views/likes.py) | legacy_likes_compatible |
| Où sont contrôlés identité et retrait ? | [likes.py](../../backend/api/v1/views/likes.py) | handle_like |
| Comment lire/retirer le like d’un dossier ? | [likes.py](../../backend/api/v1/views/likes.py) | personal_story_like |
| Comment lire/retirer le like d’un commentaire ? | [likes.py](../../backend/api/v1/views/likes.py) | personal_comment_like |
| Comment éviter les doubles envois ? | [likes.js](../../frontend/likes.js) | createLikeControl |
| Comment vérifier la réponse personnelle ? | [api.js](../../frontend/api.js) | getLikeState |
| Comment envoyer une intention explicite ? | [api.js](../../frontend/api.js) | changeLike |
| Pourquoi bloquer une migration ambiguë ? | [c6g200000001_add_comment_likes.py](../../migrations/versions/c6g200000001_add_comment_likes.py) | inspect_legacy |
| Quelle migration est candidate ? | [c6g200000001_add_comment_likes.py](../../migrations/versions/c6g200000001_add_comment_likes.py) | upgrade |
| Quelles preuves API et SQL ? | [test_likes.py](../../backend/tests/test_likes.py) | LikesTests |
| Quelles preuves de reprise synthétique ? | [test_comment_likes_migration.py](../../backend/tests/test_comment_likes_migration.py) | CommentLikesMigrationTests |

216 repères : les 204 antérieurs sont conservés et leurs lignes actualisées, 12 nouveaux ajoutés. [Bilan 6G.2](BILAN_LOT6G2.md). Les mentions historiques de clics répétés ne décrivent plus le contrat courant des commentaires ; les théories conservent leur mécanisme.
