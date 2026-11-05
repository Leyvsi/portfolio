# Permissions et sécurité — lot 6H.21.5

Les Petits Enquêteurs — préparation pour Mahamadou — **5 novembre 2026, Europe/Paris**.

**Proposition documentaire externe, sans installation autorisée.** Référence : 203 fichiers de la copie intégrée, vérifiés par empreintes. Aucun module applicatif importé, aucun accès SQL, aucune migration, aucun test applicatif ni intervention sur le serveur 5066. Les exemples sont des illustrations non exécutées, pas des commandes à lancer sur une base réelle. Les responsabilités BDD de Mahamadou sont distinguées des composants partagés avec Sylvie et du frontend de Mélissa.

[Sommaire des huit guides](01_GUIDE_REQUETES_SQLALCHEMY_LOT6H21_5.md#sommaire) · [Références exactes et soutenance](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md) · [Contrôles et limites](08_VALIDATION_DOCUMENTAIRE_LOT6H21_5.md)

## La bonne question : quel contrôle, sur quel chemin ?

Une protection utile doit être rattachée à un contrôle concret, à ses entrées et à un refus observable. Le mot « sécurisé » ne suffit pas. Ce guide distingue code présent, tests déclarés, résultats historiques consultés et validations absentes. Aucun test de sécurité, compte ou endpoint n’est exercé pendant cette rédaction.

## Identité et permissions : chaîne de décision

[MAH-F0177 — get_authenticated_user](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0177) lit user_id dans la session Flask. Si absent, il renvoie un refus 401. S’il existe, il demande le compte à SQLAlchemy ; un compte disparu entraîne session.clear et 401, un compte banni session.clear et 403. Un compte actif est renvoyé à la vue avec absence d’erreur.

[MAH-F0178 — admin_required](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0178) enveloppe une vue et applique ce contrôle, puis user.is_admin. Le booléen du cookie et le menu affiché ne remplacent pas la lecture du rôle. Les écritures de contribution choisissent user.id depuis ce résultat, même si un autre user_id est transmis par le client.

La relecture par Session.get exploite la gestion d’identité de la Session ; il ne faut pas affirmer un nouveau SELECT à chaque invocation si le même objet est déjà présent non expiré dans un contexte. Les chemins demandant populate_existing/refresh explicitent un besoin de fraîcheur supplémentaire. Ces mécanismes n’établissent pas une garantie de révocation instantanée sur toutes les requêtes déjà en cours.

## Matrice des accès réellement implémentés

| Famille de routes | Anonyme | Membre actif | Administrateur actif | Contrôle particulier |
|---|---|---|---|---|
| GET stories, détail par slug, théories/commentaires, updates | Lecture publique si parent actif | Même lecture | Même lecture publique | L’archive est filtrée ; la catégorie cold case n’est pas vérifiée par la seule route updates |
| GET stats | Trois agrégats publics | Même lecture | Même endpoint, utilisé par le dashboard | Le nom getAdminStats du client ne change pas cette permission |
| POST users | Inscription publique sans session | Session existante vérifiée + CSRF | Même logique d’inscription d’un membre | Le rôle client n’est pas adopté |
| POST login | Autorisé sans CSRF de session préalable | Login reste exempté du filtre CSRF | Même route | Mot de passe et bannissement contrôlés |
| GET me | 401 | Compte courant | Compte courant | Pas de lecture libre d’un autre compte |
| POST logout | Peut vider une session anonyme | CSRF si user_id présent | Même filtre | Ne révoque pas un registre central de sessions |
| POST contribution/like/report/proposal, DELETE like | Refus authentification | Acceptable après validations | Acceptable après validations | Compte et cible serveur, CSRF pour session présente |
| GET users/proposals/admin reports | Refus | Refus 403 | Lecture autorisée | Contenus privés : e-mails, textes soumis, motifs |
| Bannissement | Refus | Refus 403 | Cible membre seulement | Toute cible administratrice est protégée par 409 |
| Archives et purge admin stories | Refus | Refus 403 | Sous préconditions | Archive, jetons, état, intégrité, expiration selon opération |

Un compte banni ne devient pas autorisé parce qu’une page est encore ouverte. Les lectures publiques restent publiques ; leur accès n’est pas systématiquement conditionné au compte affiché. Le frontend doit masquer/rafraîchir ses états personnels, et le serveur doit contrôler les écritures.

## Session Flask et cookie signé

Le module de configuration exige une clé secrète, et login commence par effacer l’ancien état de session avant de fixer le nouveau user_id, is_admin et CSRF. Le cookie Flask est signé : sa signature vise l’intégrité, pas la confidentialité de son contenu. Ni mot de passe brut ni hachage n’est ajouté par ces vues à cet état.

| Option du code | Intention | Limite concrète |
|---|---|---|
| SESSION_COOKIE_HTTPONLY=True | Empêcher l’accès direct au cookie par le JavaScript ordinaire | Ne supprime pas la capacité d’un script exécuté dans la page à émettre des requêtes avec le cookie |
| SESSION_COOKIE_SAMESITE=Lax | Limiter certains envois intersites selon le navigateur | Ne remplace pas le contrôle CSRF et ne couvre pas toute topologie de domaines |
| SESSION_COOKIE_SECURE configurable, défaut False | Réserver l’envoi à HTTPS quand activé | La démonstration HTTP locale ne prouve pas une configuration HTTPS de production |
| session.clear au logout | Faire émettre la suppression/vidange de la session courante | Pas de registre serveur révoquant toutes les copies d’un cookie signé |
| Jeton CSRF conservé en mémoire api.js | Retrouver l’en-tête pour les actions de la page | Disparaît au rechargement ; /me doit fournir un jeton pour la nouvelle page |

Le module ne définit pas ici une durée de session personnalisée assimilable au TTL de suppression. Le TTL=300 concerne les jetons de purge, pas une déconnexion automatique de tous les membres. [Sessions Flask officielles](https://flask.palletsprojects.com/en/stable/quickstart/#sessions).

## CSRF : branches et limites précises

[MAH-F0037 — protect_session_requests_from_csrf](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0037) s’exécute avant la vue. Pour POST/PUT/PATCH/DELETE, sauf chemin exact /api/v1/login, il cherche un user_id dans la session. Sans user_id, ce filtre laisse passer et la vue décide de l’accès. Avec user_id, il exige deux chaînes non vides ASCII et compare le jeton attendu au X-CSRF-Token avec secrets.compare_digest. Un refus produit 403 et une réponse JSON de CSRF.

Cela implique plusieurs distinctions :

1. Une inscription anonyme n’a pas de CSRF lié à une session authentifiée à présenter dans ce mécanisme. Une inscription avec session existante doit le présenter.
2. Login reste explicitement exempté, y compris si un ancien cookie est présent. Le guide ne lui attribue pas une protection pré-authentification qui n’existe pas dans ce filtre.
3. GET/HEAD/OPTIONS ne sont pas protégés comme des écritures par ce contrôle ; une route GET doit donc conserver une sémantique cohérente.
4. Un jeton correct ne confère pas le rôle admin, ne lève pas un bannissement et ne valide pas un motif ou une cible.
5. Le jeton CSRF est accessible au JavaScript de l’origine par la réponse JSON ; une compromission XSS peut dépasser l’objectif de ce mécanisme. HttpOnly n’est pas une immunité XSS.

apiRequest ajoute le token qu’il connaît aux méthodes d’écriture sauf login. Les panneaux qui relisent /me avant l’action réduisent certains états périmés. L’absence de retry automatique évite de multiplier involontairement les créations ; les blocages après issue incertaine sont propres aux composants, pas une propriété universelle de fetch.

## Validations serveur et champs de confiance

[MAH-F0209 — json_object](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0209) et [MAH-F0210 — required_text](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0210) imposent, dans les vues qui les utilisent, un objet JSON et un texte non vide, des limites de taille et un encodage valide. max_length compte la longueur Python du texte ; text_column contrôle en plus les octets UTF-8, à 65535. trim=False protège les espaces du mot de passe contre un nettoyage involontaire.

get_resource borne les PK dans le domaine prévu puis utilise Session.get ; get_active_story filtre l’archive. Il faut les combiner : l’existence d’un commentaire ne prouve pas la visibilité de son dossier. Le client peut choisir une cible, mais le serveur la relit et obtient l’auteur depuis sa session.

La route générique /reports possède un parseur propre : elle normalise une cible textuelle à zéros initiaux alors que Report.target_id setter les refuse. Elle ne passe pas par required_text pour le motif et ne reproduit pas toutes ses bornes UTF-8. Le guide signale cette différence existante sans modifier la route ni inventer un même validateur sur tous les chemins.

Le contrôle du mot de passe utilise un hachage salé Werkzeug ; ce n’est pas un chiffrement déchiffrable. La politique de caractères de l’inscription n’est pas une preuve de résistance générale aux tentatives de connexion. Aucun mécanisme de limitation d’essais, MFA ou récupération de compte n’est visible dans les vues de connexion étudiées ; aucune protection d’infrastructure extérieure n’est supposée.

## Injections SQL et rendu du texte

Les filtres et valeurs liés de SQLAlchemy évitent de coller directement le texte de l’utilisateur dans la syntaxe SQL. Les instructions textuelles de métadonnées dans require_integrity sont constantes. Les noms de tables concaténés par inspect_database viennent des métadonnées préalablement comparées ; les identifiants de lignes sont passés par paramètres DBAPI. Il faut toujours examiner la provenance d’un fragment SQL, même s’il est exécuté via une bibliothèque ORM.

Une valeur liée peut encore être trop longue, interdite, coûteuse à traiter ou non autorisée. Les protections d’injection ne remédient pas à une FK désactivée ou à un oubli de contrôle de rôle. Les statuts et les rôles client ne sont pas des noms de colonnes à interpoler librement dans du SQL.

Dans les composants de contributions et panneaux étudiés, les textes sont construits avec createElement/textContent plutôt qu’exécutés comme HTML de contenu. Le client vérifie aussi des schémas de réponse et bornes d’id. Le nom d’une fonction comme isStory ne constitue pas un assainissement universel de toutes les URLs d’images ou du site : chaque rendu doit être relié à son chemin réel.

## Cache, confidentialité des réponses et navigation

Le wrapper de fichiers statiques émet no-store. Les réponses admin reports portent private, no-store ; admin stories porte no-store ; les états personnels de likes portent private, no-store. api.js demande cache:no-store pour certaines lectures, dont /me et les signalements. Ne pas prétendre que ces options sont présentes identiquement sur toutes les routes.

Les panneaux administratifs effacent les données à la sortie de page, au changement de session signalé et sur refus ; le retour de cache déclenche une relecture. Un callback onAccessDenied peut masquer la zone avant de tenter de lire un JSON d’erreur. Cela limite certains affichages obsolètes, sans forcer l’effacement de copies déjà prises ou une révocation instantanée de chaque écran ouvert.

L’accès aux motifs et e-mails doit rester borné par les routes. Le public /stats fournit un total des signalements, pas leur contenu. Une agrégation publique et une liste privée ont des périmètres différents ; elles ne doivent pas être documentées sous le même mot « administration » sans cette distinction.

## Erreurs HTTP et non-divulgation

Les vues gérées répondent avec des messages neutres et rollback en cas d’erreur SQL pertinente. is_unique_conflict ne transforme que les formats métier reconnus. Le handler HTTPException normalise les erreurs du framework pour les chemins API, avec leur statut et leurs en-têtes ; il ne prouve pas que toute exception de bibliothèque devient une erreur métier uniforme.

Une sérialisation après commit peut échouer ; un accusé réseau peut se perdre. Le code de purge renvoie alors une issue inconnue spécifique dans le cas prévu, tandis que d’autres parcours ont des limites différentes. Le frontend doit distinguer « opération refusée » et « résultat non confirmé ». Il ne doit ni afficher un faux succès ni supposer systématiquement que rien n’a été enregistré.

## Trois niveaux de preuve à citer honnêtement

| Niveau | Ce qui est disponible pour cette rédaction | Ce qui n’est pas démontré |
|---|---|---|
| Code statique | Fonctions, clauses, décorateurs et règles lus dans les 203 fichiers de référence | Leur activation effective sur une instance distante |
| Sources de tests | Définitions de tests de CSRF, conflits, permissions, archive/purge et isolation lues sans exécution | Une réussite nouvelle dans ce lot |
| Rapport historique 6H.22.8 | Campagne backend rapportée à 318 tests, résultat PASS, mysql_tested=False ; source du rapport conservée par empreinte dans les preuves de ce lot | Une nouvelle campagne, une preuve MySQL réelle ou un confinement système |

La présence d’un test ne prouve pas à elle seule son exécution. Le rapport historique est cité avec sa date UTC d’origine et son périmètre jetable ; les tests injectant des erreurs MySQL couvrent leur traitement, pas une connexion Aiven. Ce lot n’emploie aucun client de test Flask, serveur ou navigateur.

## Tests déclarés : exemples de correspondance

Les symboles ci-dessous existent dans les sources de tests. Ils ne sont pas invoqués pour cette livraison ; leur nom et position sont vérifiés statiquement.

| Source de test | Définition et ligne | Lecture pédagogique |
|---|---|---|
| `backend/tests/test_csrf.py` | [test_missing_header_token_is_403](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#source-6ab55a527fa3) ; ligne 84 | Refus du jeton absent |
| `backend/tests/test_csrf.py` | [test_login_exemption_survives_existing_session_and_invalid_tokens](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#source-3fc182b88cae) ; ligne 70 | Exemption explicite de login |
| `backend/tests/test_users_votes.py` | [test_users_mysql_sqlite_unique_conflicts_are_400](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#source-769e483fb4ea) ; ligne 201 | Erreurs de contraintes injectées, pas serveur MySQL |
| `backend/tests/test_users_votes.py` | [test_users_real_sqlite_unique_error_after_precheck](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#source-fd79be9e1201) ; ligne 235 | Conflit réel SQLite après précontrôle simulé |
| `backend/tests/test_users_votes.py` | [test_other_constraints_are_500_not_business_conflicts](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#source-5398f2d4f335) ; ligne 224 | Ne pas masquer une autre erreur en doublon |

## Gardes Python, droits système et périmètre de confiance

Les lanceurs et harnais du projet interceptent certaines connexions, neutralisent dotenv/réseau et contrôlent des chemins pour des essais de code de confiance. Ils ne constituent pas une frontière de sécurité contre du code Python arbitraire. Un marqueur dans connection.info n’est ni un secret ni une autorisation système.

Le mode persistant contient des vérifications de chemins et des droits de répertoire propres au compte Windows, ainsi qu’un verrou d’opération. Ces mesures ont une finalité de confidentialité locale et d’exclusion des opérations coopératives. Elles ne transforment pas le processus Python en environnement hostile confiné ; le détenteur du même compte et un programme arbitraire conservent des capacités à considérer.

Cette session n’a besoin d’aucune contre-épreuve d’accès extérieur : elle lit le code et calcule des empreintes des fichiers publics attendus. Elle ne tente jamais d’ouvrir une base privée pour démontrer un refus.

## Réponses pour l’oral

« Une permission se vérifie dans la route serveur. Le menu admin du navigateur ne crée pas le rôle. »

« Le CSRF protège certaines écritures avec une session existante ; il ne remplace ni le mot de passe, ni l’autorisation, ni la validation des champs. Login est explicitement exempté par ce code. »

« Les paramètres de requête séparent la valeur du SQL ; ils ne rendent pas toute opération métier autorisée. »

« J’ai une preuve historique de tests SQLite et de tests de traitement d’erreurs. Je n’en fais pas une preuve d’exécution MySQL ni une garantie absolue de sécurité. »

Le [Parcours fonctionnels complets](03_GUIDE_PARCOURS_FONCTIONNELS_LOT6H21_5.md) donne les statuts et réponses de chaque parcours ; le [Persistance et environnements](06_GUIDE_PERSISTANCE_ENVIRONNEMENTS_LOT6H21_5.md) sépare les environnements et les limites des mécanismes de persistance.
