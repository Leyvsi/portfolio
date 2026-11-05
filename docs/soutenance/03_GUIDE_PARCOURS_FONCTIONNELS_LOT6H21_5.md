# Parcours fonctionnels complets — lot 6H.21.5

Les Petits Enquêteurs — préparation pour Mahamadou — **5 novembre 2026, Europe/Paris**.

**Proposition documentaire externe, sans installation autorisée.** Référence : 203 fichiers de la copie intégrée, vérifiés par empreintes. Aucun module applicatif importé, aucun accès SQL, aucune migration, aucun test applicatif ni intervention sur le serveur 5066. Les exemples sont des illustrations non exécutées, pas des commandes à lancer sur une base réelle. Les responsabilités BDD de Mahamadou sont distinguées des composants partagés avec Sylvie et du frontend de Mélissa.

[Sommaire des huit guides](01_GUIDE_REQUETES_SQLALCHEMY_LOT6H21_5.md#sommaire) · [Références exactes et soutenance](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md) · [Contrôles et limites](08_VALIDATION_DOCUMENTAIRE_LOT6H21_5.md)

## Trame commune et lecture des preuves

Chaque parcours suit l’action du navigateur jusqu’au résultat. L’ordre d’un décorateur, du filtre before_request et du try local compte : un refus peut arriver avant l’écriture, et une lecture de réponse peut arriver après le commit. Les statuts ci-dessous décrivent les branches explicites, sans prétendre couvrir toutes les pannes de proxy, de transport ou du pilote.

La liste complète des routes est fournie dans le guide d’intégration, d’après leurs déclarations AST et l’enregistrement du Blueprint. Elle n’est pas issue d’un import Flask ou d’un essai HTTP nouveau. Les exemples de JSON sont des descriptions de clés ; aucun utilisateur réel, jeton ou motif privé n’est lu.

## Accès aux douze parcours

[01](#parcours-01) · [02](#parcours-02) · [03](#parcours-03) · [04](#parcours-04) · [05](#parcours-05) · [06](#parcours-06) · [07](#parcours-07) · [08](#parcours-08) · [09](#parcours-09) · [10](#parcours-10) · [11](#parcours-11) · [12](#parcours-12)

<a id="parcours-01"></a>

## Parcours 01 — Inscription et création d’un compte

### Fichiers JavaScript et entrée de l’interface

[frontend/app.js:498](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#source-e48b723d12c6) ; [frontend/api.js:142](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#source-4d669924268c).

### Requêtes HTTP et routes Flask réellement déclarées

| Méthode | Route déclarée | Fonction actuelle |
|---|---|---|
| POST | `/api/v1/users` | [MAH-F0207 — register_user](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0207) |

**Fonctions de coopération :** [MAH-F0207 — register_user](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0207), [MAH-F0205 — is_valid_password](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0205), [MAH-F0210 — required_text](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0210), [MAH-F0212 — is_unique_conflict](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0212).

### Action initiale

Le formulaire signup-form de inscription.html intercepte submit. Le bouton est désactivé pendant l’envoi ; la saisie du mot de passe n’est pas modifiée par trim.

### Authentification et autorisation

Le navigateur tente GET /me avant l’inscription. Un 401 est accepté comme état anonyme ; un autre refus arrête le parcours client. La route users POST est publique si aucune session n’est présente. Si un user_id de session existe, get_authenticated_user doit accepter le compte ; le filtre global exige alors aussi le CSRF.

### Validation des données

Le corps doit être un objet JSON. required_text impose username <=100, email <=150, password <=50, non vides et encodables. Pseudo et e-mail sont nettoyés ; trim=False préserve le mot de passe. La politique exige 8–50 caractères, majuscule, minuscule, chiffre et caractère spécial reconnu. Le serveur contrôle la forme de l’adresse et les tailles de ses composantes. Les contrôles HTML ne remplacent pas ceux-ci.

### Requêtes et résultats SQLAlchemy

Deux SELECT préalables cherchent pseudo et e-mail. User est construit sans rôle client ; set_password calcule le hachage. add puis commit provoquent l’INSERT. Le constructeur n’émet pas ce SQL à lui seul.

### Tables et contraintes applicables

users.username et users.email sont uniques séparément, colonnes obligatoires ; le rôle initial est le défaut ORM membre et le bannissement faux. Les champs is_admin/is_banned fournis par le client ne pilotent pas cette construction.

### Limites transactionnelles

Le try d’écriture couvre add et commit. IntegrityError et SQLAlchemyError provoquent rollback ; seuls les doublons métier reconnus sont traduits en refus de doublon. La sérialisation new_user.to_dict a lieu après commit.

### Erreurs et codes HTTP

201 succès ; 400 pour entrée invalide ou doublon reconnu, y compris le doublon apparu après précontrôle ; 401/403 si une session déjà présente est invalide ou interdite, et 403 CSRF si applicable ; autre erreur SQL gérée 500. Une panne du précontrôle hors try peut suivre un autre chemin serveur 500.

### Réponse JSON

status="success", user avec id, username, email, is_admin, created_at ; aucun password_hash. Pas de jeton CSRF créé par cette route d’inscription.

### Traitement côté navigateur

register attend 201 et un JSON lisible. Le formulaire est remis à zéro après réussite ; le mot de passe est vidé dans finally, le bouton reste désactivé après création confirmée. L’utilisateur est invité à se connecter. Le traitement ne crée pas automatiquement une session pour le nouveau compte.

### Étapes absentes et réserves

Pas d’activation par e-mail, récupération de mot de passe ou attribution de rôle administrateur dans ce parcours. Après une réponse perdue, le frontend n’a pas un verrou d’incertitude identique à celui des commentaires ; les contraintes restent nécessaires.

### Réponse utilisable à l’oral

« L’inscription crée un membre avec un hachage et des unicités SQL. Elle ne connecte pas automatiquement le compte et n’accepte pas un rôle envoyé par le navigateur. »

<a id="parcours-02"></a>

## Parcours 02 — Connexion, lecture de session et déconnexion

### Fichiers JavaScript et entrée de l’interface

[frontend/app.js:533](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#source-65e0e5f3c0a9) ; [frontend/api.js:115](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#source-926f9a641341).

### Requêtes HTTP et routes Flask réellement déclarées

| Méthode | Route déclarée | Fonction actuelle |
|---|---|---|
| POST | `/api/v1/login` | [MAH-F0041 — login_user](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0041) |
| GET | `/api/v1/me` | [MAH-F0042 — get_current_user](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0042) |
| POST | `/api/v1/logout` | [MAH-F0043 — logout_user](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0043) |

**Fonctions de coopération :** [MAH-F0177 — get_authenticated_user](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0177).

### Action initiale

Les pages connexion.html et admin-connexion.html partagent login-form ; un attribut distingue la redirection administrative. app.js gère aussi la zone de session et relit /me au focus ou au retour de cache selon les branches.

### Authentification et autorisation

Login est exempté du filtre CSRF global et n’exige pas un compte déjà connecté. /me utilise get_authenticated_user, qui relit User et refuse absence, compte supprimé ou banni. Logout efface la session Flask ; si un user_id était présent, le filtre CSRF exige le jeton pour ce POST.

### Validation des données

Login attend des chaînes username/password non vides ; seul le pseudo est trimé. Les deux sont vérifiés encodables en UTF-8. Le hachage est comparé par User.check_password, puis is_banned contrôlé. Le rôle affiché ne suffit pas à autoriser une route administrative.

### Requêtes et résultats SQLAlchemy

Login fait User.query.filter_by(username=...).first ; /me utilise Session.get(User, user_id). Les changements du cookie ne sont pas des UPDATE users. Un cookie stocke user_id, is_admin et csrf_token ; aucun mot de passe n’y est ajouté.

### Tables et contraintes applicables

L’unicité du pseudo permet d’identifier le compte. L’authentification dépend du hachage, de SECRET_KEY pour le cookie et de la relecture de l’état ; il n’existe pas une table SQL de sessions ajoutée par ces vues.

### Limites transactionnelles

Aucun commit de création de compte dans login/me/logout. Les lectures peuvent engager une transaction SQL de Session ; son nettoyage de contexte ne transforme pas la lecture en écriture métier. session.clear est l’objet Flask, distinct de db.session.rollback.

### Erreurs et codes HTTP

Login : 400 entrée absente/invalide, 401 identifiants incorrects, 403 compte banni, 200 succès. /me : 401 session absente ou compte absent, 403 banni, 200 compte actif. Logout : 200 succès si le filtre global laisse entrer. Les erreurs SQL de login ne sont pas toutes interceptées localement comme SQLAlchemyError.

### Réponse JSON

Login renvoie status, message, user{id,username,email,is_admin}, csrf_token. /me renvoie status, user et csrf_token. Logout renvoie status et message, sans objet utilisateur.

### Traitement côté navigateur

api.js conserve le jeton CSRF seulement en mémoire JavaScript. Une nouvelle page retrouve le jeton via /me. La page admin vérifie is_admin avant redirection ; la route reste protégée côté serveur. La zone de session compare l’identité affichée avant logout, émet session-ended quand l’état affiché change et relit après une issue inconnue sans répéter automatiquement le POST.

### Étapes absentes et réserves

Pas de JWT, refresh token, session SQL persistée ou révocation centrale de toutes les copies de cookie. Le cookie est signé, pas chiffré. La page admin peut refuser une redirection pour un membre alors que le login serveur a déjà réussi pour ce membre.

### Réponse utilisable à l’oral

« Le cookie signé permet de retrouver une identité ; le serveur relit le compte. La session HTTP n’est pas la Session SQLAlchemy. »

<a id="parcours-03"></a>

## Parcours 03 — Consultation d’un dossier actif

### Fichiers JavaScript et entrée de l’interface

[frontend/app.js:244](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#source-01b06274624c) ; [frontend/api.js:194](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#source-ec2bafc5e576).

### Requêtes HTTP et routes Flask réellement déclarées

| Méthode | Route déclarée | Fonction actuelle |
|---|---|---|
| GET | `/api/v1/stories` | [MAH-F0160 — get_stories](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0160) |
| GET | `/api/v1/stories/slug/<string:slug>` | [MAH-F0161 — get_story_by_slug](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0161) |

**Fonctions de coopération :** [MAH-F0160 — get_stories](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0160), [MAH-F0161 — get_story_by_slug](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0161).

### Action initiale

Les listes sont construites depuis getStories ; dossier.html transmet le slug de sa query string à loadStory. La fonction ne transforme pas le rang d’une carte en PK de base.

### Authentification et autorisation

Les deux GET sont publics et ne nécessitent pas de CSRF. Le filtre archived_at=None est appliqué dans les requêtes serveur. Les lectures administratives d’archives ont d’autres routes et permissions.

### Validation des données

getStoryBySlug encode le slug comme segment avec encodeURIComponent ; isStory vérifie plusieurs champs du résultat. Le serveur utilise une égalité de colonne liée, pas une concaténation SQL du slug.

### Requêtes et résultats SQLAlchemy

La liste filtre les dossiers actifs, les trie par created_at décroissant puis les charge avec all. Pour chacun, un COUNT Vote calcule votes. Le détail filtre slug et état actif, first, puis COUNT Vote. Story.to_dict fournit le détail ; ce sérialiseur n’expose pas la révision de gestion ou archived_at.

### Tables et contraintes applicables

slug est unique ; chaque Story possède auteur et catégorie obligatoires. La référence image_url est une chaîne, pas un BLOB ; la lecture d’image est une autre requête statique du navigateur.

### Limites transactionnelles

Aucun add, UPDATE métier ou commit dans ces deux vues. Les listes peuvent entraîner plusieurs requêtes ; aucun instantané transactionnel unique du navigateur n’est garanti pour tous ses appels.

### Erreurs et codes HTTP

200 liste, y compris vide ; 404 pour détail absent ou archivé. Une panne SQL peut produire 500 sans traitement SQLAlchemyError spécifique local. L’interface distingue dossier introuvable et lecture impossible.

### Réponse JSON

La liste renvoie des objets avec id, slug, title, summary, content, image_url, category_id, author_id, votes et created_at. Le détail ajoute votes au dictionnaire Story qui comporte aussi updated_at. Ce n’est pas le même contrat que la vue administrative enrichie.

### Traitement côté navigateur

loadStory affiche les textes par textContent, sépare les paragraphes, choisit les illustrations selon les fonctions de app.js et monte les commentaires/likes avec l’id reçu. Le chargement du récit ne publie pas une nouvelle histoire et ne copie pas le contenu dans localStorage.

### Étapes absentes et réserves

Pas de pagination dans ces fonctions, pas de GET public par PK inventé pour remplacer la route par slug. Une catégorie inconnue est affichée comme telle ; elle n’est pas fabriquée à partir du numéro.

### Réponse utilisable à l’oral

« Le slug retrouve un dossier actif ; les contributions utilisent ensuite son vrai id. L’archive est filtrée côté serveur. »

<a id="parcours-04"></a>

## Parcours 04 — Création et lecture d’un commentaire

### Fichiers JavaScript et entrée de l’interface

[frontend/comments.js:144](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#source-d3c472550f95) ; [frontend/api.js:443](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#source-4c9a7fe22809).

### Requêtes HTTP et routes Flask réellement déclarées

| Méthode | Route déclarée | Fonction actuelle |
|---|---|---|
| GET | `/api/v1/stories/<int:story_id>/comments` | [MAH-F0156 — get_story_comments](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0156) |
| POST | `/api/v1/stories/<int:story_id>/comments` | [MAH-F0157 — post_story_comment](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0157) |

**Fonctions de coopération :** [MAH-F0156 — get_story_comments](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0156), [MAH-F0157 — post_story_comment](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0157), [MAH-F0155 — comment_to_dict](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0155), [MAH-F0200 — get_active_story](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0200).

### Action initiale

Le composant mountStoryComments lit d’abord la liste puis intercepte le formulaire de commentaire. Il bloque les envois concurrents sur la page et préserve le brouillon en cas de refus.

### Authentification et autorisation

GET public sur dossier actif. POST : /me préalable côté navigateur, CSRF si session présente, get_authenticated_user côté serveur et get_active_story(lock=True). user_id et username viennent du compte relu, pas du JSON.

### Validation des données

Le client contrôle un texte non vide, son encodage et 65535 octets UTF-8 ; le serveur appelle json_object et required_text(text_column=True), avec son propre contrôle d’encodage et de taille. La borne d’identifiant est vérifiée par le helper de dossier.

### Requêtes et résultats SQLAlchemy

SELECT parent actif, éventuelle demande de verrou, construction Comment avec copie du pseudo, add puis commit. La liste est filtrée par story_id et triée created_at croissant. comment_to_dict compte Report et, si likes historique vaut exactement l’entier zéro, CommentLike.

### Tables et contraintes applicables

comments.story_id obligatoire CASCADE ; user_id nullable SET NULL ; texte obligatoire. Le pseudo copié peut subsister si l’auteur perd sa référence SQL. Aucun auteur arbitraire reçu du navigateur n’est adopté.

### Limites transactionnelles

La création valide dans le try d’écriture puis sérialise après commit. Les lectures de comptage peuvent donc se produire après validation. Le GET ne crée aucune contribution.

### Erreurs et codes HTTP

201 succès de création ; 200 liste ; 400 texte/JSON invalide ; 401/403 accès ; 404 parent absent/archivé ; 500 écriture gérée. Un 403 peut être un bannissement ou une protection CSRF, selon le chemin.

### Réponse JSON

POST renvoie status et comment{id,story_id,user_id,username,text,likes,created_at,likes_compatible,reports}. La valeur likes est soit le décompte individuel compatible, soit la valeur physique historique préservée. GET renvoie une liste de ces représentations.

### Traitement côté navigateur

createComment attend 201 et vérifie le rattachement au dossier. Après réussite, le composant ajoute/remplace le commentaire par son id, affiche le succès et efface le champ. Après résultat incertain (réseau, JSON incohérent, 5xx), uncertainComment bloque un nouvel envoi de même type sur cette page ; une actualisation sert à vérifier, sans répéter le POST.

### Étapes absentes et réserves

Pas de modification ou suppression libre de commentaires dans ce parcours. Ni SET NULL ni le libellé Anonyme ne garantissent un effacement des données personnelles du texte ou du pseudo.

### Réponse utilisable à l’oral

« L’auteur vient de la session serveur, le parent doit être actif et le succès est confirmé seulement après le contrat 201. Une réponse perdue peut laisser une création effective. »

<a id="parcours-05"></a>

## Parcours 05 — Publication d’une théorie

### Fichiers JavaScript et entrée de l’interface

[frontend/app.js:349](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#source-f4fcc17e6b2d) ; [frontend/api.js:159](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#source-c6a179a6c72f).

### Requêtes HTTP et routes Flask réellement déclarées

| Méthode | Route déclarée | Fonction actuelle |
|---|---|---|
| GET | `/api/v1/stories/<int:story_id>/theories` | [MAH-F0202 — get_theories](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0202) |
| POST | `/api/v1/stories/<int:story_id>/theories` | [MAH-F0203 — post_theory](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0203) |
| POST | `/api/v1/theories/<int:theory_id>/like` | [MAH-F0204 — like_theory](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0204) |

**Fonctions de coopération :** [MAH-F0202 — get_theories](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0202), [MAH-F0203 — post_theory](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0203), [MAH-F0201 — theory_to_dict](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0201), [MAH-F0204 — like_theory](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0204).

### Action initiale

La page theories.html charge les dossiers actifs pour remplir le sélecteur avec de vrais id. Le formulaire de publication et le lecteur theories-list.js sont deux composants distincts.

### Authentification et autorisation

Lecture publique des théories d’un dossier actif. Publication et like de théorie : authentification, CSRF pour une session présente et dossier parent actif relu avec demande de verrou. L’auteur de la publication est le compte serveur.

### Validation des données

Titre non vide <=200 selon la colonne, contenu non vide encodable dans la limite TEXT. Le client valide que l’id sélectionné appartient aux dossiers reçus ; le serveur revalide le parent pour couvrir un archivage concurrent.

### Requêtes et résultats SQLAlchemy

POST construit Theory puis add/commit ; GET filtre story_id et trie created_at. Le like historique fait UPDATE theories SET likes=likes+1 sous condition id, refresh, préparation du payload puis commit. Il n’ajoute pas une ligne CommentLike ou Vote.

### Tables et contraintes applicables

story_id obligatoire CASCADE ; user_id nullable SET NULL ; titre et contenu obligatoires. Aucun couple unique compte/théorie ne limite le compteur de likes historique.

### Limites transactionnelles

Publication : commit avant sérialisation de réponse. Like historique : execute UPDATE, rowcount, refresh et payload avant commit. Un échec SQL géré déclenche rollback.

### Erreurs et codes HTTP

201 théorie créée ; 200 liste ou compteur modifié ; 400 données invalides ; 401/403 accès ; 404 cible/parent indisponible ; 500 écriture gérée. Une liste vide est distincte d’un dossier absent.

### Réponse JSON

Publication : status, theory{id,story_id,user_id,title,content,likes,created_at}. Le GET renvoie une liste de ces dictionnaires. Le like historique renvoie status et theory avec compteur relu.

### Traitement côté navigateur

Le formulaire vérifie /me, conserve la saisie sur refus et marque uncertainTheory après issue incertaine pour empêcher une relance sur cette page. Après création confirmée il se remet à zéro. Le lecteur charge/actualise séparément les théories ; aucun rechargement automatique de toutes les listes n’est inventé.

### Étapes absentes et réserves

Aucune table de likes individuels de théorie ni retrait personnel symétrique dans ces routes. L’existence de like_theory ne prouve pas qu’un bouton actif de toutes les pages l’appelle : le lecteur doit être examiné séparément.

### Réponse utilisable à l’oral

« La théorie est un enfant du dossier. Son compteur historique et les likes individuels de commentaires ont des modèles de données différents. »

<a id="parcours-06"></a>

## Parcours 06 — Ajout, lecture et retrait d’un like individuel

### Fichiers JavaScript et entrée de l’interface

[frontend/likes.js:2](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#source-9b399889e3b1) ; [frontend/api.js:483](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#source-c8b9be370f31).

### Requêtes HTTP et routes Flask réellement déclarées

| Méthode | Route déclarée | Fonction actuelle |
|---|---|---|
| POST | `/api/v1/votes/<int:story_id>` | [MAH-F0162 — post_story_vote](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0162) |
| GET | `/api/v1/votes/<int:story_id>` | [MAH-F0174 — personal_story_like](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0174) |
| DELETE | `/api/v1/votes/<int:story_id>` | [MAH-F0174 — personal_story_like](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0174) |
| POST | `/api/v1/comments/<int:comment_id>/like` | [MAH-F0158 — like_comment](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0158) |
| GET | `/api/v1/comments/<int:comment_id>/like` | [MAH-F0175 — personal_comment_like](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0175) |
| DELETE | `/api/v1/comments/<int:comment_id>/like` | [MAH-F0175 — personal_comment_like](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0175) |

**Fonctions de coopération :** [MAH-F0162 — post_story_vote](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0162), [MAH-F0158 — like_comment](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0158), [MAH-F0173 — handle_like](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0173), [MAH-F0172 — like_state](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0172), [MAH-F0171 — legacy_likes_compatible](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0171).

### Action initiale

Le contrôle commun capture l’intention ajouter/retirer, relit /me puis l’état personnel et vérifie que le compte n’a pas changé avant d’envoyer. Les clics se fondent sur l’état serveur, pas seulement un compteur local.

### Authentification et autorisation

Toutes ces routes personnelles exigent un compte actif. GET ne requiert pas CSRF ; POST et DELETE avec session le requièrent. Les écritures vérifient le dossier actif avec lock=True. La lecture de commentaire recharge son compteur historique et refuse un état non attribuable.

### Validation des données

kind est choisi par le code entre story et comment ; l’id est borné. Les corps de POST de like de dossier ne servent pas à définir l’auteur ; le serveur emploie user.id. legacy_likes_compatible exige type(likes) is int et likes==0 pour le nouveau parcours de commentaire.

### Requêtes et résultats SQLAlchemy

Ajout dossier : précontrôle Vote du couple, construction Vote, add, flush, count, commit. Ajout commentaire : précontrôle CommentLike, add, flush, comment_to_dict, commit. Lecture personnelle : COUNT cible puis recherche du couple. Retrait : DELETE sur cible ET compte, vérification rowcount 0/1, état relu avant commit.

### Tables et contraintes applicables

unique_user_story_vote(user_id,story_id) et unique_user_comment_like(user_id,comment_id) empêchent les doublons concurrents. Toutes les FK de ces associations sont obligatoires CASCADE. Le filtre de retrait préserve les likes d’autres comptes.

### Limites transactionnelles

Les ajouts ont un flush explicite pour compter la ligne dans la transaction. Les payloads de like sont préparés avant commit dans les chemins examinés. Le GET ne commite pas de modification métier ; le retrait valide après son DELETE et ses lectures.

### Erreurs et codes HTTP

Ajout dossier 201 ; ajout commentaire 200 ; lectures/retraits 200, y compris retrait déjà absent avec changed=False. Doublon 409 ; commentaire historique incompatible 409 LEGACY_LIKES_UNRESOLVED ; 401/403 accès ; 404 cible/parent indisponible ; 500 erreur SQL non reconnue.

### Réponse JSON

GET : status, target_type, target_id entier, likes, liked_by_me. DELETE ajoute changed. POST dossier : message et votes. POST commentaire : status et comment enrichi. Les validateurs du client respectent ces contrats différents.

### Traitement côté navigateur

Après écriture confirmée, le contrôle relit l’état. Sur 409 il relit sans réémettre. Après timeout ou issue incertaine, uncertain bloque l’envoi sur la page ; « Vérifier les J’aime » peut actualiser le décompte sans affirmer que la demande initiale a échoué. Un compteur historique incompatible désactive les likes individuels de commentaire.

### Étapes absentes et réserves

L’ajout dossier ne passe pas par la branche add de handle_like : il a sa route dédiée post_story_vote. Le contrôle partagé ne permet pas de conclure que tous les likes ont la même forme JSON ou le même statut HTTP.

### Réponse utilisable à l’oral

« Une ligne par couple exprime l’intention d’un compte. Je relis l’état après l’action et je n’attribue pas un ancien compteur à des identités inventées. »

<a id="parcours-07"></a>

## Parcours 07 — Proposition d’une histoire

### Fichiers JavaScript et entrée de l’interface

[frontend/app.js:434](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#source-5ca830192df9) ; [frontend/api.js:150](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#source-ad345c0a77e6).

### Requêtes HTTP et routes Flask réellement déclarées

| Méthode | Route déclarée | Fonction actuelle |
|---|---|---|
| POST | `/api/v1/proposals` | [MAH-F0182 — create_proposal](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0182) |
| GET | `/api/v1/proposals` | [MAH-F0181 — get_proposals](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0181) |

**Fonctions de coopération :** [MAH-F0182 — create_proposal](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0182), [MAH-F0181 — get_proposals](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0181), [MAH-F0180 — proposal_to_dict](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0180).

### Action initiale

Le formulaire proposer-histoire.html recueille titre, catégorie proposée et présentation. Le JavaScript compose content en préfixant « Catégorie proposée : … » ; il n’envoie pas category_id.

### Authentification et autorisation

Le POST exige un compte actif et le CSRF si session présente. Le client relit /me avant de soumettre. Le GET de propositions est administratif et ne devient pas public parce que le formulaire est accessible.

### Validation des données

Titre nettoyé et limité à 200 ; contenu non vide et borné en UTF-8 côté serveur. Le client n’accepte que les deux libellés proposés dans le sélecteur ; le serveur reçoit finalement du texte, pas une FK de catégorie.

### Requêtes et résultats SQLAlchemy

Construction Proposal(user_id=user.id,title,content,status="pending"), add et commit. La lecture administrative trie created_at décroissant puis all. Aucun INSERT Story n’est présent dans la route d’envoi.

### Tables et contraintes applicables

FK user_id obligatoire CASCADE, titre/contenu/statut/dates obligatoires. Le modèle ne fournit pas une contrainte UNIQUE qui empêcherait deux propositions textuellement identiques.

### Limites transactionnelles

Le try gère l’écriture et rollback sur SQLAlchemyError. proposal_to_dict est appelé après commit. La catégorie incluse dans content est persistée comme texte et non normalisée par relation SQL.

### Erreurs et codes HTTP

POST 201 ; GET 200 ; 400 entrée invalide ; 401/403 compte/CSRF ou rôle de lecture ; 500 écriture gérée. Un échec de réponse après commit ne prouve pas l’absence de proposition.

### Réponse JSON

status et proposal{id,user_id,title,content,status,created_at,updated_at}. Le GET administratif renvoie une liste de ces dictionnaires.

### Traitement côté navigateur

createProposal exige 201. Le formulaire n’est remis à zéro qu’après succès ; les champs sont désactivés pendant l’envoi. Après erreur, finally réactive le bouton. Il n’existe pas ici de variable uncertainProposal bloquant une nouvelle soumission manuelle comme pour les commentaires.

### Étapes absentes et réserves

Pas d’approbation/rejet de proposition ni conversion automatique en Story implémentés dans ce module. Le mot « examinée » dans l’interface ne prouve pas l’existence d’une route de publication.

### Réponse utilisable à l’oral

« Je transmets une proposition pending privée à l’administration. C’est une soumission, pas la création d’un dossier public. »

<a id="parcours-08"></a>

## Parcours 08 — Signalement d’un commentaire

### Fichiers JavaScript et entrée de l’interface

[frontend/comments.js:144](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#source-d3c472550f95) ; [frontend/api.js:454](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#source-8ebdf054d05f).

### Requêtes HTTP et routes Flask réellement déclarées

| Méthode | Route déclarée | Fonction actuelle |
|---|---|---|
| POST | `/api/v1/comments/<int:comment_id>/report` | [MAH-F0159 — report_comment](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0159) |
| POST | `/api/v1/reports` | [MAH-F0164 — post_report](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0164) |
| GET | `/api/v1/admin/reports` | [MAH-F0166 — get_admin_reports](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0166) |

**Fonctions de coopération :** [MAH-F0159 — report_comment](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0159), [MAH-F0164 — post_report](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0164), [MAH-F0166 — get_admin_reports](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0166).

### Action initiale

L’utilisateur choisit un commentaire de la liste reçue puis un motif. Le formulaire monté par comments.js capture son id réel ; l’envoi principal du navigateur utilise la route spécialisée /comments/{id}/report.

### Authentification et autorisation

POST : compte actif, CSRF et dossier actif de la cible. GET /admin/reports : admin_required, compte relu et rôle administrateur. Le client ne peut pas rendre la liste de motifs publique en affichant un menu.

### Validation des données

Route spécialisée : json_object et required_text(reason,text_column=True). Route générique /reports : type, target_id et reason doivent être des chaînes non vides ; type comment seulement ; cible décimale ASCII normalisée en retirant les zéros initiaux, bornée et existante. Ce parseur n’est pas le setter Python Report.target_id, qui refuse les zéros initiaux. La route générique n’appelle pas required_text et n’applique pas exactement sa borne UTF-8 au motif.

### Requêtes et résultats SQLAlchemy

SELECT du commentaire et du dossier actif, puis Report(comment_id=entier,reason), add/commit. La lecture administrative charge Report.comment → Comment.story → Story.category avec joinedload, trie date/id décroissants et construit le contexte sans réécrire les cibles.

### Tables et contraintes applicables

reports.comment_id est la vraie FK obligatoire CASCADE. type et target_id sont des propriétés de compatibilité, non des colonnes actuelles. Aucune colonne de déclarant ni unicité par commentaire n’est stockée.

### Limites transactionnelles

Chaque POST valide le Report dans son try ; la réponse est sérialisée après commit. Le GET administratif capture ses erreurs SQL et rollback, sans traitement de modération. Des écarts de données historiques restent une condition de lecture, pas une réparation.

### Erreurs et codes HTTP

201 succès de POST ; 400 format/type/motif refusé ; 401/403 accès ; 404 cible ou dossier indisponible ; 500 erreur SQL gérée. Les deux parseurs d’entrée ne doivent pas être annoncés identiques.

### Réponse JSON

POST : status et report{id,type="comment",target_id chaîne,reason,status,created_at}. GET admin ajoute comment{id,story_id,text} et story{id,slug,title,category_id,category_name,is_archived}, avec None pour un contexte absent reconnu.

### Traitement côté navigateur

reportComment exige 201 et vérifie que le target_id textuel correspond au commentaire choisi. Après succès le formulaire de signalement se ferme ; après issue incertaine uncertainReport bloque une relance de ce type sur la page et conseille la vérification administrative. L’interface n’invente pas un id de dossier comme cible du signalement.

### Étapes absentes et réserves

Le navigateur actif n’utilise pas la route générique pour ce bouton. Aucun statut « traité » n’est automatiquement posé par la lecture administrative ; aucune suppression du commentaire n’est déclenchée par l’envoi d’un signalement.

### Réponse utilisable à l’oral

« Je signale un commentaire existant par sa vraie FK. Le format JSON reste compatible avec target_id, mais le stockage ne l’utilise plus comme chaîne générique. »

<a id="parcours-09"></a>

## Parcours 09 — Bannissement d’un membre

### Fichiers JavaScript et entrée de l’interface

[frontend/admin-users.js:116](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#source-9416a00b2db5) ; [frontend/api.js:297](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#source-c4fd7461d759).

### Requêtes HTTP et routes Flask réellement déclarées

| Méthode | Route déclarée | Fonction actuelle |
|---|---|---|
| POST | `/api/v1/admin/users/<int:user_id>/ban` | [MAH-F0168 — ban_user_by_id](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0168) |
| DELETE | `/api/v1/admin/users/<string:username>/ban` | [MAH-F0167 — ban_user](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0167) |
| GET | `/api/v1/users` | [MAH-F0206 — get_users](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0206) |

**Fonctions de coopération :** [MAH-F0168 — ban_user_by_id](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0168), [MAH-F0167 — ban_user](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0167), [MAH-F0154 — ban_user_account](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0154), [MAH-F0153 — admin_user_to_dict](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0153).

### Action initiale

Le panneau administratif montre les comptes et un bouton pour les cibles éligibles. Une confirmation native affiche le pseudo comme texte. Le chemin client moderne utilise l’id stable.

### Authentification et autorisation

admin_required vérifie le compte courant et son rôle ; la session présente impose CSRF sur POST/DELETE. Le panneau relit /me, mais cette vérification visuelle n’est pas le contrôle de sécurité principal.

### Validation des données

La cible numérique est bornée. La fonction commune relit User avec populate_existing et demande FOR UPDATE. Une cible administratrice est toujours protégée, même si elle est le compte de l’acteur ; la protection ne se limite pas à comparer les deux id.

### Requêtes et résultats SQLAlchemy

SELECT cible par id ou pseudo, contrôle du rôle, affectation is_banned=True, préparation du dictionnaire administratif puis commit. GET users trie id croissant. Aucun DELETE de la table users n’est effectué par la variante HTTP DELETE.

### Tables et contraintes applicables

User.id/username identifient la cible ; les FK de contributions ne sont pas parcourues en suppression. Une répétition sur membre déjà banni reste un succès avec message adapté.

### Limites transactionnelles

La fonction commune gère sa transaction et ses erreurs SQL. La relecture de permission du décorateur n’est pas nécessairement couverte par le try de cette fonction : ne pas généraliser la capture SQL de archive_admin_required à toutes les routes admin.

### Erreurs et codes HTTP

200 compte banni ou déjà banni ; 401/403 acteur ; 404 cible ; 409 ADMIN_PROTECTED ; 500 erreur SQL gérée. L’état du cookie de la cible n’est pas contacté instantanément par cette requête.

### Réponse JSON

status, message, user avec le dictionnaire User enrichi de is_banned. La réponse attend is_admin=False et is_banned=True pour la cible traitée par le client.

### Traitement côté navigateur

Le panneau bloque avant la première attente et relit la liste même après une réponse incertaine ; il ne renvoie pas automatiquement le POST. Les anciens résultats sont écartés par un compteur de version. La cible sera refusée aux prochains contrôles serveur authentifiés.

### Étapes absentes et réserves

Aucune route de débannissement dans les modules examinés. Bannissement n’est ni suppression de compte, ni anonymisation, ni effacement de toutes les contributions, ni révocation centrale des copies du cookie.

### Réponse utilisable à l’oral

« La route change un état en base. Le rôle et le bannissement sont relus côté serveur ; la méthode HTTP historique ne décrit pas à elle seule l’effet SQL. »

<a id="parcours-10"></a>

## Parcours 10 — Archivage et restauration d’un dossier

### Fichiers JavaScript et entrée de l’interface

[frontend/admin-stories.js:154](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#source-58a85a045582) ; [frontend/api.js:346](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#source-e5c9468a4d0a).

### Requêtes HTTP et routes Flask réellement déclarées

| Méthode | Route déclarée | Fonction actuelle |
|---|---|---|
| POST | `/api/v1/admin/stories/<int:story_id>/archive` | [MAH-F0148 — archive_story](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0148) |
| POST | `/api/v1/admin/stories/<int:story_id>/restore` | [MAH-F0149 — restore_story](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0149) |
| GET | `/api/v1/admin/stories` | [MAH-F0145 — get_admin_stories](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0145) |
| GET | `/api/v1/admin/stories/<int:story_id>` | [MAH-F0146 — get_admin_story](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0146) |

**Fonctions de coopération :** [MAH-F0141 — archive_admin_required](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0141), [MAH-F0147 — set_story_archive](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0147), [MAH-F0143 — admin_story_data](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0143), [MAH-F0146 — get_admin_story](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0146).

### Action initiale

Le panneau demande une confirmation d’archive/restauration, désactive les actions pendant l’opération puis recharge les listes et compteurs. Les archives peuvent être lues via le détail administratif.

### Authentification et autorisation

archive_admin_required enveloppe admin_required et capture aussi une erreur SQL pendant la relecture du rôle. Les POST passent par le CSRF global ; les GET sont administratifs sans CSRF requis pour la lecture.

### Validation des données

story_id est borné. get_admin_stories accepte seulement state=active, archived ou all. set_story_archive relit le parent avec verrou demandé et calcule changed en comparant l’état actuel à l’intention.

### Requêtes et résultats SQLAlchemy

SELECT de la cible, affectation de archived_at à UTC naïf pour archiver ou None pour restaurer, UUID de gestion renouvelé seulement si transition ; flush, sérialisation administrative avec COUNT Vote, commit. Le détail accède aux collections et enrichit les commentaires.

### Tables et contraintes applicables

archived_at nullable est le marqueur d’état ; management_revision est unique et doit être une vraie révision pour la purge ultérieure. Les FK et textes d’enfants ne sont pas supprimés par l’archive.

### Limites transactionnelles

Flush avant la construction de data, puis commit. Deux intentions d’archive identiques ne doivent pas refaire une nouvelle date/révision : changed=False indique l’état déjà demandé. La coordination des contributions dépend du même parent et du moteur.

### Erreurs et codes HTTP

200 succès avec changed booléen ; 400 filtre invalide ; 401/403 acteur/CSRF ; 404 cible absente ; 500 erreur SQL gérée. Un timeout ne donne pas la certitude d’une absence de transition.

### Réponse JSON

status, changed, story avec données de Story plus archived_at, is_archived, management_revision et votes. GET détail ajoute comments, theories et updates ; les motifs restent dans /admin/reports.

### Traitement côté navigateur

changeAdminStoryArchive vérifie l’état demandé dans la réponse. Le panneau recharge ensuite le dashboard même après une erreur non liée à l’accès et conserve un libellé d’incertitude. Il ne répète pas automatiquement le POST. Les contrôles de doublon actif/archive entre deux GET évitent d’afficher un dossier dans les deux listes.

### Étapes absentes et réserves

Restaurer est une remise en visibilité des mêmes lignes, pas une restauration de sauvegarde SQLite. Aucun texte supprimé définitivement ne peut être récupéré par cette route.

### Réponse utilisable à l’oral

« L’archive garde les données et change la visibilité. La restauration remet la date à NULL ; elle ne rejoue pas un seed. »

<a id="parcours-11"></a>

## Parcours 11 — Suppression conditionnelle d’un dossier

### Fichiers JavaScript et entrée de l’interface

[frontend/admin-stories.js:99](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#source-f020605da7a7) ; [frontend/api.js:392](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#source-19dd32ee73ca).

### Requêtes HTTP et routes Flask réellement déclarées

| Méthode | Route déclarée | Fonction actuelle |
|---|---|---|
| GET | `/api/v1/admin/stories/<int:story_id>/deletion-preview` | [MAH-F0150 — get_story_deletion_preview](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0150) |
| POST | `/api/v1/admin/stories/<int:story_id>/deletion-confirmations` | [MAH-F0151 — confirm_story_deletion](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0151) |
| DELETE | `/api/v1/admin/stories/<int:story_id>` | [MAH-F0152 — delete_story_permanently](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0152) |

**Fonctions de coopération :** [MAH-F0196 — deletion_preview](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0196), [MAH-F0197 — confirm_deletion](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0197), [MAH-F0198 — delete_story](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0198), [MAH-F0189 — require_integrity](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0189), [MAH-F0190 — snapshot](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0190), [MAH-F0199 — run_deletion_action](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0199).

### Action initiale

Sur un dossier archivé, le panneau demande un aperçu, ouvre une boîte de dialogue avec titre exact et accord sur les contributions, demande un jeton de confirmation puis envoie un seul DELETE conditionnel. Annuler le dialogue n’envoie pas le DELETE.

### Authentification et autorisation

archive_admin_required puis lock_actor relisent l’administrateur actif. CSRF sur POST/DELETE. Les jetons sont liés au compte, à la session via une empreinte du CSRF, au dossier, au but preview/delete et à une expiration. Un lien d’interface ne remplace aucun de ces contrôles.

### Validation des données

La cible est bornée et doit être archivée avec révision hexadécimale non sentinelle. Le corps de confirmation JSON est limité à 16384 octets et refuse les clés répétées ou champs imprévus ; typed_title doit être une chaîne <=200 et correspondre exactement, confirm_contributions doit être True. DELETE n’accepte pas de corps, exige un If-Match fort exact et X-Deletion-Confirmation.

### Requêtes et résultats SQLAlchemy

Le scope vérifie l’intégrité et les moteurs nécessaires. Snapshot charge Story puis six familles, avec jointure des signalements et likes via Comment, tri, limites et hash du contenu. Au DELETE final : UPDATE conditionnel réserve une révision ; DELETE reports/comment_likes, theories, votes, updates, comments puis Story ; chaque rowcount est comparé au snapshot ; contrôle final des anciens ids par lots de 500 et de l’expiration.

### Tables et contraintes applicables

FK réelles et CASCADE vérifiées avant opération ; compteur public d’impact comporte cinq familles, le graphe interne en comporte six avec CommentLike. La borne totale est 10000 dépendances. Il ne s’agit pas d’un simple Session.delete(story).

### Limites transactionnelles

Preview et confirmation terminent par rollback pour libérer les verrous pendant la saisie humaine. La confirmation conserve l’échéance de l’aperçu initial, TTL=300 s. La suppression finale regroupe réservation et DELETE dans une transaction ; commit peut renvoyer une issue inconnue, traitée spécifiquement en 503 DELETE_STATUS_UNKNOWN. expire_all suit le commit confirmé.

### Erreurs et codes HTTP

200 pour aperçu, confirmation ou suppression confirmée ; 400 format/titre/en-têtes ; 401/403 acteur/jeton/CSRF ; 404 dossier ; 409 état non archivé, révision incompatible, dépendances modifiées ou volume excessif ; 412 confirmation périmée/état modifié ; 428 précondition absente ; 503 intégrité indisponible, contention reconnue ou issue de commit inconnue ; autre erreur SQL 500. Les conditions exactes sont celles des fonctions, pas une hiérarchie universelle de tous les refus.

### Réponse JSON

Aperçu : story minimal, impact{comments,theories,votes,updates,reports}, resource_etag, preview_token, expires_at. Confirmation : status, confirmation_token, expires_at inchangé. Succès DELETE : status, code STORY_DELETED, deleted_story avec ancienne révision et deleted_counts des cinq familles publiques.

### Traitement côté navigateur

Le client transmet seulement les deux en-têtes conditionnels autorisés par apiRequest en plus du CSRF commun. Il relit l’état et recharge le dashboard après tentative, sans répéter le DELETE. Une absence observée ne prouve pas que cette demande précise l’a causée. Sans reçu persistant, la réponse perdue ne peut pas être reconstruite comme preuve d’attribution.

### Étapes absentes et réserves

Aucun journal de suppression persistant, aucune fonction de récupération du récit purgé et aucune extension de durée à chaque confirmation. Les verrous demandés et gardes Python ne sont pas un confinement système contre du code arbitraire.

### Réponse utilisable à l’oral

« Je revalide un état signé et récent, je réserve sa révision et je vérifie chaque suppression. Je libère les verrous pendant la saisie et je distingue une issue inconnue d’une réussite. »

<a id="parcours-12"></a>

## Parcours 12 — Chargement des statistiques et du tableau administratif

### Fichiers JavaScript et entrée de l’interface

[frontend/admin-dashboard.js:183](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#source-4fce14e1480b) ; [frontend/api.js:222](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#source-52e2a5e5d40d).

### Requêtes HTTP et routes Flask réellement déclarées

| Méthode | Route déclarée | Fonction actuelle |
|---|---|---|
| GET | `/api/v1/stats` | [MAH-F0040 — get_stats](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0040) |

### Action initiale

Le dashboard efface les anciennes données, vérifie /me et is_admin, puis lance les lectures parallèles : stats, dossiers actifs, propositions, signalements et archives. Il charge ensuite le panneau des utilisateurs.

### Authentification et autorisation

L’interface exige un administrateur avant son chargement privé. Mais GET /stats lui-même est public et renvoie seulement trois agrégats. Proposals GET, admin/reports, admin/stories et users GET imposent les permissions serveur de leurs routes respectives.

### Validation des données

api.js vérifie des compteurs entiers sûrs positifs ou nuls, des listes bien formées et des identifiants distincts. Le dashboard utilise getStoryCategory pour classer les dossiers ; une catégorie inconnue est signalée, pas convertie en catégorie inventée.

### Requêtes et résultats SQLAlchemy

get_stats exécute User.query.count, Comment.query.count et Report.query.count, sans filtre d’archive. Les quatre autres indicateurs principaux viennent du navigateur : nombre de dossiers actifs reçus, sous-ensembles résolus/cold cases et propositions de statut exactement pending. Les listes peuvent produire leurs propres comptages et jointures.

### Tables et contraintes applicables

Aucune FK ou table de statistiques distincte. Les nombres users/comments/reports comptent les lignes globales, y compris des contributions conservées sous archive. Les nombres de dossiers affichés sont issus de la liste active ; ces périmètres ne sont pas tous identiques.

### Limites transactionnelles

Plusieurs GET parallèles ne forment pas une transaction SQL unique entre réponses. Des modifications concurrentes peuvent survenir entre les lectures ; le contrôle de doublon actif/archive détecte certains états incohérents sans prouver un instantané général.

### Erreurs et codes HTTP

200 agrégats publics ; 500 si la lecture SQL gérée de stats échoue, avec rollback. L’accès préalable /me ou les listes privées peuvent refuser 401/403. Un timeout ou une liste incohérente efface l’affichage protégé au lieu d’inventer des zéros.

### Réponse JSON

GET /stats : {users: entier, comments: entier, reports: entier}. Aucun endpoint renvoyant à lui seul les sept indicateurs n’est créé par le code. La page assemble ses informations depuis plusieurs contrats.

### Traitement côté navigateur

Promise.all coordonne le chargement. Les compteurs de version et AbortController évitent de réafficher un ancien résultat après une nouvelle demande. pagehide/session-ended nettoient, pageshow depuis cache relit ; cela ne constitue pas une surveillance permanente de toutes les sessions.

### Étapes absentes et réserves

Pas de transaction HTTP globale, cache serveur d’agrégats ou route administrative unique « sept statistiques ». La lecture de propositions/signalements reste une consultation ; aucun bouton d’acceptation n’est inventé.

### Réponse utilisable à l’oral

« La page est administrative, mais /stats est public et ne fournit que trois nombres. Les autres indicateurs sont calculés depuis des listes contrôlées. »

## Traverser un échec sans inventer de succès

Les erreurs 401 et 403 déclenchent des nettoyages d’interface dans les panneaux concernés ; un rôle stocké côté client ne prolonge pas une autorisation. L’annulation d’une lecture peut éliminer un résultat obsolète, mais l’annulation d’un envoi ne prouve pas un rollback serveur. Les protections contre une nouvelle soumission sont différentes selon les composants, comme indiqué pour les commentaires, théories, likes et propositions.

Pour préparer une relance du jury, choisir un seul parcours et expliquer explicitement le premier SELECT, la construction éventuelle, le flush, le commit et la première lecture après commit. Le [Transactions et intégrité](02_GUIDE_TRANSACTIONS_INTEGRITE_LOT6H21_5.md) donne les règles de transaction ; le [Permissions et sécurité](05_GUIDE_PERMISSIONS_SECURITE_LOT6H21_5.md) détaille les permissions et leurs limites.
