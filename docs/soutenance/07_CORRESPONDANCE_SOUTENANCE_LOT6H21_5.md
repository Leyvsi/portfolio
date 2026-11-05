# Correspondance avec la soutenance — lot 6H.21.5

Les Petits Enquêteurs — préparation pour Mahamadou — **5 novembre 2026, Europe/Paris**.

**Proposition documentaire externe, sans installation autorisée.** Référence : 203 fichiers de la copie intégrée, vérifiés par empreintes. Aucun module applicatif importé, aucun accès SQL, aucune migration, aucun test applicatif ni intervention sur le serveur 5066. Les exemples sont des illustrations non exécutées, pas des commandes à lancer sur une base réelle. Les responsabilités BDD de Mahamadou sont distinguées des composants partagés avec Sylvie et du frontend de Mélissa.

[Sommaire des huit guides](01_GUIDE_REQUETES_SQLALCHEMY_LOT6H21_5.md#sommaire) · [Références exactes et soutenance](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md) · [Contrôles et limites](08_VALIDATION_DOCUMENTAIRE_LOT6H21_5.md)

## Référence immuable de cette étude

La copie source est C:\Users\diarr\portfolio\_integration-main-lot6h22-7, branche integration-main-6h22-7. Ses 203 fichiers de travail sont la référence documentaire, comprenant les sept guides installés au lot 6H.21.4. HEAD est une base Git et ne suffit pas à représenter les ajouts de travail non suivis. Les empreintes avant/après établissent la préservation de l’arbre observé.

Le dépôt original Documents/portfolio ne sert pas de source de données privées ; aucune commande ni écriture ne le cible pour ce lot. Le présent dossier est durable et hors des deux dépôts. Les chemins relatifs et lignes de code ci-dessous sont valides pour cette photographie ; les numéros pourront changer après un autre lot, d’où la présence des symboles et identifiants.

## Responsabilités pédagogiques et coopération

| Périmètre | Explication principale de Mahamadou | Composants partagés à présenter avec l’équipe |
|---|---|---|
| Modèles, contraintes et requêtes | Types, PK/FK, couples uniques, relations, résultats et effets | Les validations de vues et contrats JSON sont partagées avec Sylvie |
| Transactions et persistance | Flush/commit/rollback, configurations et limites des moteurs | Lanceurs, permissions et gestion d’erreur appartiennent au parcours commun |
| Client HTTP et DOM | Comprendre l’effet d’une requête et l’origine de son id | Mélissa porte l’interface et ses états ; Sylvie le backend partagé |
| Démonstration au jury | Distinguer code, preuve historique et limite actuelle | Aucun membre ne doit s’attribuer seul un module partagé sur la seule foi d’un préfixe pédagogique |

Le référentiel 6H.21.1 définit des identifiants stables ; les noms et chemins actuels sont rapprochés de ce gel. Aucun identifiant existant n’est renuméroté. MAH-M028/MAH-F0213 reste le complément proposé au lot 6H.21.4 pour sqlite_migration_scope, sans réécriture du gel.

## Correspondance avec les dix-huit questions MAH

Les textes de questions sont extraits de « A. Question originale » et reproduits tels quels. Les compléments ci-dessous sont de nouveaux supports de compréhension, sans remplacer les réponses actuelles ou historiques de la fiche.

| Repère et question conservée | Complément lié aux sources | Guide à travailler |
|---|---|---|
| **MAH-01** — À quoi sert MySQL ? | La configuration choisit un moteur, et SQLAlchemy transmet ses opérations à celui-ci. Aiven n’est pas un modèle supplémentaire ; aucune connexion MySQL nouvelle n’est prouvée. | [Persistance et environnements](06_GUIDE_PERSISTANCE_ENVIRONNEMENTS_LOT6H21_5.md) |
| **MAH-02** — Pourquoi utiliser plusieurs tables ? | Les tables séparent comptes, dossiers et contributions. Les références portent les liens ; une requête joint ou filtre selon le besoin sans recopier toutes les identités. | [Requêtes SQLAlchemy](01_GUIDE_REQUETES_SQLALCHEMY_LOT6H21_5.md) |
| **MAH-03** — Qu’est-ce qu’une clé primaire ? | Session.get retrouve une PK de table et peut réutiliser l’identité ORM disponible. Un id ne doit pas être remplacé par le rang d’un élément du navigateur. | [Requêtes SQLAlchemy](01_GUIDE_REQUETES_SQLALCHEMY_LOT6H21_5.md) |
| **MAH-04** — Qu’est-ce qu’une clé étrangère ? | La FK assure une référence valide quand elle est installée et active. relationship gère la navigation ; la route vérifie aussi droits et visibilité. | [Transactions et intégrité](02_GUIDE_TRANSACTIONS_INTEGRITE_LOT6H21_5.md) |
| **MAH-05** — Quelle est la relation entre histoire et théorie ? | Le parcours de publication crée Theory avec story_id réel du dossier actif, titre et contenu. Il n’écrit pas dans le récit original. | [Parcours fonctionnels complets](03_GUIDE_PARCOURS_FONCTIONNELS_LOT6H21_5.md) |
| **MAH-06** — Pourquoi l’auteur d’une théorie peut-il être nul ? | user_id de Theory est nullable avec SET NULL ; la théorie et son texte peuvent subsister. Ce n’est pas un effacement de contenu personnel. | [Transactions et intégrité](02_GUIDE_TRANSACTIONS_INTEGRITE_LOT6H21_5.md) |
| **MAH-07** — Quelle différence entre `CASCADE` et `SET NULL` ? | CASCADE supprime l’enfant, SET NULL retire une référence facultative. Les cascades ORM et le SQL direct sont deux mécanismes à expliquer séparément. | [Transactions et intégrité](02_GUIDE_TRANSACTIONS_INTEGRITE_LOT6H21_5.md) |
| **MAH-08** — Comment empêcher deux votes identiques ? | Le couple user_id/story_id est unique. Le précontrôle du POST de vote et la contrainte couvrent des moments différents ; le conflit reconnu donne 409. | [Requêtes SQLAlchemy](01_GUIDE_REQUETES_SQLALCHEMY_LOT6H21_5.md) |
| **MAH-09** — Pourquoi garder une contrainte SQL si l’API vérifie déjà ? | Deux requêtes peuvent observer le même état absent. L’unicité SQL protège encore l’insertion concurrente ; un rollback remet ensuite la Session en état. | [Transactions et intégrité](02_GUIDE_TRANSACTIONS_INTEGRITE_LOT6H21_5.md) |
| **MAH-10** — À quoi sert SQLAlchemy ? | L’ORM construit des requêtes et suit les objets. Query.first et Result.first ne sont pas la même étape : l’un évalue le Query, l’autre consomme une exécution antérieure. | [Requêtes SQLAlchemy](01_GUIDE_REQUETES_SQLALCHEMY_LOT6H21_5.md) |
| **MAH-11** — Que fait `commit()` ? | Commit fait le flush nécessaire puis valide la transaction. Une réponse HTTP peut encore se perdre après cette validation. | [Transactions et intégrité](02_GUIDE_TRANSACTIONS_INTEGRITE_LOT6H21_5.md) |
| **MAH-12** — Que fait `rollback()` ? | Rollback annule une transaction active dans les limites du moteur et restaure la Session après échec ; il ne prouve pas l’annulation d’un commit dont l’accusé est perdu. | [Transactions et intégrité](02_GUIDE_TRANSACTIONS_INTEGRITE_LOT6H21_5.md) |
| **MAH-13** — À quoi sert Alembic ? | Alembic parcourt des révisions. create_all d’un lanceur crée un schéma actuel, sans reprise automatique d’une ancienne table reports. | [Persistance et environnements](06_GUIDE_PERSISTANCE_ENVIRONNEMENTS_LOT6H21_5.md) |
| **MAH-14** — Pourquoi supprimer `comments.reports` ? | Le nombre de signalements est lu depuis les lignes Report. Le compteur supprimé ne doit pas être recréé comme source fiable : son downgrade le remet à zéro sans recalcul. | [Requêtes SQLAlchemy](01_GUIDE_REQUETES_SQLALCHEMY_LOT6H21_5.md) |
| **MAH-15** — Pourquoi le certificat CA est-il utile ? | La configuration Aiven fournit un chemin de CA au pilote. Cela n’atteste ni le TLS réel, ni la vérification du nom d’hôte, ni les contraintes SQL ; aucun certificat n’est lu ici. | [Persistance et environnements](06_GUIDE_PERSISTANCE_ENVIRONNEMENTS_LOT6H21_5.md) |
| **MAH-16** — Les tests SQLite prouvent-ils que MySQL fonctionne ? | Les résultats SQLite sont circonscrits à leur environnement. Les branches et erreurs MySQL simulées ne constituent pas une campagne Aiven. | [Validation documentaire](08_VALIDATION_DOCUMENTAIRE_LOT6H21_5.md) |
| **MAH-17** — `reports.target_id` est-il une clé étrangère ? | Report.target_id est une propriété compatible avec le JSON ; comment_id est la vraie colonne FK. Les parseurs de la propriété et de la route générique ne sont pas identiques. | [Parcours fonctionnels complets](03_GUIDE_PARCOURS_FONCTIONNELS_LOT6H21_5.md) |
| **MAH-18** — Les migrations créent-elles les dossiers de démonstration ? | Les histoires viennent d’un seed ou d’une initialisation neuve explicite. Les migrations et le lancement normal de run_local ne chargent pas les six récits. | [Persistance et environnements](06_GUIDE_PERSISTANCE_ENVIRONNEMENTS_LOT6H21_5.md) |

## Correspondance avec les vingt-deux questions communes

| Repère et question conservée | Complément lié aux sources | Guide à travailler |
|---|---|---|
| **COM-01** — Quel problème votre projet traite-t-il ? | Le projet permet de lire des dossiers d’enquête et de structurer des contributions autour d’un dossier ; les parcours distinguent récits, théories, commentaires et propositions. | [Parcours fonctionnels complets](03_GUIDE_PARCOURS_FONCTIONNELS_LOT6H21_5.md) |
| **COM-02** — À qui s’adresse le site ? | La lecture publique est ouverte ; les contributions utilisent un membre actif et l’administration des permissions distinctes. L’accès technique ne détermine pas une conformité éditoriale ou juridique. | [Permissions et sécurité](05_GUIDE_PERMISSIONS_SECURITE_LOT6H21_5.md) |
| **COM-03** — Quel est le parcours principal ? | Choisir un dossier actif, lire son contenu puis, avec session, contribuer. Chaque étape peut réussir ou refuser séparément. | [Parcours fonctionnels complets](03_GUIDE_PARCOURS_FONCTIONNELS_LOT6H21_5.md) |
| **COM-04** — Comment les trois couches communiquent-elles ? | Le JavaScript envoie HTTP/JSON à Flask, qui valide puis accède à la Session SQLAlchemy et à la base choisie. Le navigateur ne se connecte pas directement à SQL. | [Intégration Flask, API et SQLAlchemy](04_GUIDE_INTEGRATION_FLASK_API_LOT6H21_5.md) |
| **COM-05** — Pourquoi séparer frontend et backend ? | Le client gère interaction et affichage ; le serveur garde validation, permissions et intégrité. Leur coopération passe par des contrats explicites. | [Intégration Flask, API et SQLAlchemy](04_GUIDE_INTEGRATION_FLASK_API_LOT6H21_5.md) |
| **COM-06** — Quel est l’intérêt de l’API ? | L’API stabilise routes, statuts et représentations. Les helpers vérifient les réponses et les panneaux traitent refus ou incertitude. | [Intégration Flask, API et SQLAlchemy](04_GUIDE_INTEGRATION_FLASK_API_LOT6H21_5.md) |
| **COM-07** — Combien de tables avez-vous ? | Dix modèles applicatifs, soixante colonnes et treize FK dans les sources actuelles ; la table de version Alembic n’est pas un onzième modèle applicatif. | [Requêtes SQLAlchemy](01_GUIDE_REQUETES_SQLALCHEMY_LOT6H21_5.md) |
| **COM-08** — Pourquoi une proposition n’est-elle pas directement une histoire ? | Proposal est enregistrée en pending et consultée par l’administration. La catégorie du formulaire est du texte dans content ; aucune publication Story automatique. | [Parcours fonctionnels complets](03_GUIDE_PARCOURS_FONCTIONNELS_LOT6H21_5.md) |
| **COM-09** — Les théories sont-elles modérées avant affichage ? | Le POST de théorie persiste et renvoie directement sa représentation. Aucun statut de modération préalable n’est présent dans ce modèle/parcours. | [Parcours fonctionnels complets](03_GUIDE_PARCOURS_FONCTIONNELS_LOT6H21_5.md) |
| **COM-10** — Peut-on contribuer sans compte ? | Les lectures publiques sont possibles sans compte. Les contributions et états personnels exigent un compte actif ; la simple présence d’un formulaire ne donne pas le droit. | [Permissions et sécurité](05_GUIDE_PERMISSIONS_SECURITE_LOT6H21_5.md) |
| **COM-11** — Comment protégez-vous les mots de passe ? | User.set_password délègue à Werkzeug ; le hachage n’est pas exposé par User.to_dict. La politique de saisie ne remplace pas une protection générale contre les essais de connexion. | [Permissions et sécurité](05_GUIDE_PERMISSIONS_SECURITE_LOT6H21_5.md) |
| **COM-12** — Qui décide qu’un compte est administrateur ? | Le rôle est fixé côté serveur/peuplement. register_user n’adopte pas is_admin envoyé par le client et admin_required relit le compte. | [Permissions et sécurité](05_GUIDE_PERMISSIONS_SECURITE_LOT6H21_5.md) |
| **COM-13** — Pourquoi protéger aussi les routes si le bouton est caché ? | Un client peut appeler l’API sans passer par un bouton. Le serveur décide du rôle, du bannissement, du CSRF et de la validité de la cible. | [Permissions et sécurité](05_GUIDE_PERMISSIONS_SECURITE_LOT6H21_5.md) |
| **COM-14** — Comment gérez-vous une API indisponible ? | apiRequest distingue HTTP, délai, réseau et JSON. Les panneaux évitent les données inventées et les lectures tardives ; un timeout peut suivre un commit. | [Intégration Flask, API et SQLAlchemy](04_GUIDE_INTEGRATION_FLASK_API_LOT6H21_5.md) |
| **COM-15** — Que faites-vous contre les doubles soumissions ? | Les états busy limitent les doubles clics ; certains composants bloquent après issue incertaine. L’API n’a pas de retry automatique, mais tous les formulaires n’ont pas un verrou identique ni une clé d’idempotence serveur. | [Parcours fonctionnels complets](03_GUIDE_PARCOURS_FONCTIONNELS_LOT6H21_5.md) |
| **COM-16** — Que prouvent les 439 tests ? | Le nombre 439 fait partie de la question historique. Il n’est pas réétiqueté comme résultat courant ; les campagnes sont citées séparément par date, environnement et unité de comptage. | [Validation documentaire](08_VALIDATION_DOCUMENTAIRE_LOT6H21_5.md) |
| **COM-17** — Ces tests prouvent-ils que toute la production fonctionne ? | Les tests synthétiques, mocks, assertions documentaires et anciennes recettes ne démontrent pas toute la production, le TLS Aiven, la charge ou la concurrence réelle MySQL. | [Validation documentaire](08_VALIDATION_DOCUMENTAIRE_LOT6H21_5.md) |
| **COM-18** — Le tableau de bord peut-il bannir ou publier ? | Le tableau peut consulter et bannir un membre, archiver/restaurer et lancer la purge conditionnelle. Accepter/publier une proposition n’est pas implémenté dans les routes lues. | [Parcours fonctionnels complets](03_GUIDE_PARCOURS_FONCTIONNELS_LOT6H21_5.md) |
| **COM-19** — Les votes et les likes suivent-ils la même règle ? | Vote et CommentLike sont des associations uniques de couple. Theory.likes est un compteur historique incrémentable sans unicité individuelle ; leurs contrats HTTP diffèrent. | [Requêtes SQLAlchemy](01_GUIDE_REQUETES_SQLALCHEMY_LOT6H21_5.md) |
| **COM-20** — Peut-on reproduire la démonstration depuis une base vide ? | Le kit mémoire neuf ou l’initialisation persistante neuve fournissent leurs données explicitement. Redémarrer serve ne doit pas refaire un seed ni restaurer une archive. | [Persistance et environnements](06_GUIDE_PERSISTANCE_ENVIRONNEMENTS_LOT6H21_5.md) |
| **COM-21** — Qu’amélioreriez-vous en priorité ? | Les limites à expliquer concernent la validation distante, la concurrence, les volumes sans pagination et les parcours de modération non développés. Ce lot documente ces écarts sans correctif applicatif. | [Validation documentaire](08_VALIDATION_DOCUMENTAIRE_LOT6H21_5.md) |
| **COM-22** — Comment avez-vous réparti le travail ? | Mahamadou porte principalement la compréhension BDD et intégration ; Sylvie et Mélissa partagent les parcours backend/frontend. Les identifiants MAH ne prouvent pas une création exclusive des modules. | [Correspondance avec la soutenance](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md) |

## Les 76 questions restent préservées

Mahamadou : 18 ; Mélissa : 18 ; Sylvie : 18 ; fiche commune : 22. Les nouvelles correspondances ciblent les 40 questions demandées, mais les quatre fichiers entiers sont conservés par SHA-256. Cela protège aussi leurs textes historiques, exemples archivés, réponses actualisées et références existantes, sans compter seulement des titres.

## Raccord aux sept guides du lot 6H.21.4

| Fichier existant | Utilisation dans le nouveau lot | Limite évitée |
|---|---|---|
| [01_GUIDE_DIX_MODELES.md](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#source-c1ca58e3c82b) | Colonnes et contrats de sérialisation | Ne pas inventer une colonne Report.target_id ou un auteur ColdCaseUpdate. |
| [02_RELATIONS_CONTRAINTES_TRANSACTIONS.md](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#source-6e0c7122c419) | PK/FK, couples uniques et cascades | Ne pas assimiler cascade ORM et suppression SQL directe. |
| [03_GUIDE_SEPT_MIGRATIONS.md](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#source-088e1fc0828a) | Chaîne et données de migrations | Ne pas appeler create_all une reprise Alembic. |
| [04_REPERTOIRE_FONCTIONS_METHODES.md](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#source-b38431dc23f1) | Contrats de modèles et fonctions Alembic | Conserver les identifiants gelés et signaler l’extension. |
| [05_DIAGRAMME_RELATIONNEL_COMMENTE.md](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#source-83e37800ea6d) | Dix tables et treize liens | Distinguer lien SQL, règle métier et droit d’accès. |
| [06_CORRESPONDANCE_SOURCES.md](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#source-a23267386b96) | Photographie des sources et précisions historiques | Garder la rectification du downgrade du compteur à zéro. |
| [07_VALIDATION_DOCUMENTAIRE.md](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#source-9f6299f08111) | Nature statique des preuves de rédaction | Ne pas annoncer une migration ou un test MySQL nouvellement exécuté. |

Aucun de ces sept fichiers n’est modifié ; ils restent installés dans le dépôt de référence. Les renvois passent par cet index interne pour que les huit nouveaux guides restent lisibles dans leur archive sans une copie implicite de l’ensemble du projet. Les fichiers du lot 6H.21.4 restent des supports externes identifiés par leur chemin et leur empreinte.

## Cohérence avec README et les référentiels gelés

[README : périmètre fonctionnel](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#source-7142c6762d80) ; [README : modèles et transactions](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#source-c7a4bd03e9d9) ; [README : responsabilités](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#source-4c0f7b528900).

Les guides conservent les distinctions du README : usage local sans nouvelle publication, six récits et PNG, propositions pending sans publication automatique, sessions Flask/CSRF, modes mémoire/persistant et MySQL non revérifié. Les comptes historiques des tests restent datés ; la formulation 439 de COM-16 n’est pas changée en un total plus récent. Les listes/compteurs et verrous sont expliqués selon le code plutôt que selon une étiquette globale de « production validée ».

Le README décrit sa copie historique feature/frontend-api-integration et certains états de livraison antérieurs ; le présent rapport distingue cette étiquette datée de la branche isolée effectivement lue. Il n’en déduit ni changement de branche ni publication de nouveaux commits. Le gel reste le gel, les compléments documentent les repères actuels.

[Référentiel pédagogique 6H.21.1](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#source-aaa596cc87f8) ; [Inventaire gelé 6H.21.1](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#source-059d056c7b7c) ; [Conventions des futures copies](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#source-5cfeab467948).

Les copies commentées ligne par ligne du lot 6H.21.6 restent futures. La présente documentation explique des mécanismes et inventorie des sites d’appel ; elle ne crée pas des modules applicatifs copiés avec commentaires et ne les ajoute pas aux imports.

## Index des références de code effectivement utilisées

Chaque lien « fonction » des guides mène à une entrée ci-dessous. L’entrée fixe chemin relatif, symbole, ligne physique actuelle et empreinte du fichier. Il faut ouvrir ce chemin sous la racine source indiquée en début de rapport ; ces références ne deviennent pas des liens cassés vers des sources absentes du ZIP. Les identifiants MAH sont conservés ; les ancres JavaScript et repères textuels sont locaux à ces guides, sans nouvelle attribution d’auteur.

| Ancre et repère | Fichier et position | Symbole vérifié | SHA-256 de la source |
|---|---|---|---|
| <a id="source-7142c6762d80"></a>repère textuel exact | `README.md:34` | `## Fonctionnalités et périmètre` | `39e3565150bf7aef9bc969aa3151105eb6b4c2c19549758b92b298efa445ca50` |
| <a id="source-c7a4bd03e9d9"></a>repère textuel exact | `README.md:173` | `## Base de données et SQLAlchemy` | `39e3565150bf7aef9bc969aa3151105eb6b4c2c19549758b92b298efa445ca50` |
| <a id="source-4c0f7b528900"></a>repère textuel exact | `README.md:954` | `## Équipe et responsabilités` | `39e3565150bf7aef9bc969aa3151105eb6b4c2c19549758b92b298efa445ca50` |
| <a id="source-ca9977daa9b1"></a>repère textuel exact | `backend/api/v1/views/__init__.py:8` | `url_prefix='/api/v1'` | `e32b9ee7d236f38c85357f3bc7244f06d5bb5efaf7f6ca13a2fef3025978258c` |
| <a id="code-mah-f0141"></a>MAH-F0141 | `backend/api/v1/views/admin_stories.py:16–28` | `archive_admin_required` | `e3d2d521cfe96937d72ee9af46e0af31abd2adf0f3d5f7f14e2826cd5adb75b5` |
| <a id="code-mah-f0143"></a>MAH-F0143 | `backend/api/v1/views/admin_stories.py:31–39` | `admin_story_data` | `e3d2d521cfe96937d72ee9af46e0af31abd2adf0f3d5f7f14e2826cd5adb75b5` |
| <a id="code-mah-f0145"></a>MAH-F0145 | `backend/api/v1/views/admin_stories.py:52–66` | `get_admin_stories` | `e3d2d521cfe96937d72ee9af46e0af31abd2adf0f3d5f7f14e2826cd5adb75b5` |
| <a id="code-mah-f0146"></a>MAH-F0146 | `backend/api/v1/views/admin_stories.py:71–89` | `get_admin_story` | `e3d2d521cfe96937d72ee9af46e0af31abd2adf0f3d5f7f14e2826cd5adb75b5` |
| <a id="code-mah-f0147"></a>MAH-F0147 | `backend/api/v1/views/admin_stories.py:92–112` | `set_story_archive` | `e3d2d521cfe96937d72ee9af46e0af31abd2adf0f3d5f7f14e2826cd5adb75b5` |
| <a id="code-mah-f0148"></a>MAH-F0148 | `backend/api/v1/views/admin_stories.py:117–118` | `archive_story` | `e3d2d521cfe96937d72ee9af46e0af31abd2adf0f3d5f7f14e2826cd5adb75b5` |
| <a id="code-mah-f0149"></a>MAH-F0149 | `backend/api/v1/views/admin_stories.py:123–124` | `restore_story` | `e3d2d521cfe96937d72ee9af46e0af31abd2adf0f3d5f7f14e2826cd5adb75b5` |
| <a id="code-mah-f0150"></a>MAH-F0150 | `backend/api/v1/views/admin_stories.py:129–131` | `get_story_deletion_preview` | `e3d2d521cfe96937d72ee9af46e0af31abd2adf0f3d5f7f14e2826cd5adb75b5` |
| <a id="code-mah-f0151"></a>MAH-F0151 | `backend/api/v1/views/admin_stories.py:136–138` | `confirm_story_deletion` | `e3d2d521cfe96937d72ee9af46e0af31abd2adf0f3d5f7f14e2826cd5adb75b5` |
| <a id="code-mah-f0152"></a>MAH-F0152 | `backend/api/v1/views/admin_stories.py:143–145` | `delete_story_permanently` | `e3d2d521cfe96937d72ee9af46e0af31abd2adf0f3d5f7f14e2826cd5adb75b5` |
| <a id="code-mah-f0153"></a>MAH-F0153 | `backend/api/v1/views/admin_users_support.py:12–13` | `admin_user_to_dict` | `8c115809bc583e4caed76dcd9c54a5bd1c3e83804295864d52a24c65e24c2ed6` |
| <a id="code-mah-f0154"></a>MAH-F0154 | `backend/api/v1/views/admin_users_support.py:19–52` | `ban_user_account` | `8c115809bc583e4caed76dcd9c54a5bd1c3e83804295864d52a24c65e24c2ed6` |
| <a id="code-mah-f0155"></a>MAH-F0155 | `backend/api/v1/views/comments.py:13–26` | `comment_to_dict` | `df80521cd40da18da973bc809a07194199a359b3e4fb81ed8ab668b8dba6f838` |
| <a id="code-mah-f0156"></a>MAH-F0156 | `backend/api/v1/views/comments.py:32–50` | `get_story_comments` | `df80521cd40da18da973bc809a07194199a359b3e4fb81ed8ab668b8dba6f838` |
| <a id="code-mah-f0157"></a>MAH-F0157 | `backend/api/v1/views/comments.py:56–97` | `post_story_comment` | `df80521cd40da18da973bc809a07194199a359b3e4fb81ed8ab668b8dba6f838` |
| <a id="code-mah-f0158"></a>MAH-F0158 | `backend/api/v1/views/comments.py:103–105` | `like_comment` | `df80521cd40da18da973bc809a07194199a359b3e4fb81ed8ab668b8dba6f838` |
| <a id="code-mah-f0159"></a>MAH-F0159 | `backend/api/v1/views/comments.py:111–149` | `report_comment` | `df80521cd40da18da973bc809a07194199a359b3e4fb81ed8ab668b8dba6f838` |
| <a id="code-mah-f0160"></a>MAH-F0160 | `backend/api/v1/views/histoires.py:14–39` | `get_stories` | `8c9188e36b0a8e72f5284ac3c3e3987fcb9b819c6adc55dfdd237658cf637764` |
| <a id="code-mah-f0161"></a>MAH-F0161 | `backend/api/v1/views/histoires.py:44–60` | `get_story_by_slug` | `8c9188e36b0a8e72f5284ac3c3e3987fcb9b819c6adc55dfdd237658cf637764` |
| <a id="code-mah-f0162"></a>MAH-F0162 | `backend/api/v1/views/histoires.py:66–118` | `post_story_vote` | `8c9188e36b0a8e72f5284ac3c3e3987fcb9b819c6adc55dfdd237658cf637764` |
| <a id="code-mah-f0163"></a>MAH-F0163 | `backend/api/v1/views/histoires.py:124–142` | `get_case_updates` | `8c9188e36b0a8e72f5284ac3c3e3987fcb9b819c6adc55dfdd237658cf637764` |
| <a id="code-mah-f0164"></a>MAH-F0164 | `backend/api/v1/views/index.py:17–97` | `post_report` | `959f1dc966c4b6379f68b0c8f0ece210ad51837dfcea764655085cc9f76ee805` |
| <a id="code-mah-f0166"></a>MAH-F0166 | `backend/api/v1/views/index.py:110–132` | `get_admin_reports` | `959f1dc966c4b6379f68b0c8f0ece210ad51837dfcea764655085cc9f76ee805` |
| <a id="code-mah-f0167"></a>MAH-F0167 | `backend/api/v1/views/index.py:139–140` | `ban_user` | `959f1dc966c4b6379f68b0c8f0ece210ad51837dfcea764655085cc9f76ee805` |
| <a id="code-mah-f0168"></a>MAH-F0168 | `backend/api/v1/views/index.py:147–148` | `ban_user_by_id` | `959f1dc966c4b6379f68b0c8f0ece210ad51837dfcea764655085cc9f76ee805` |
| <a id="code-mah-f0169"></a>MAH-F0169 | `backend/api/v1/views/index.py:153–161` | `get_swagger_json` | `959f1dc966c4b6379f68b0c8f0ece210ad51837dfcea764655085cc9f76ee805` |
| <a id="code-mah-f0170"></a>MAH-F0170 | `backend/api/v1/views/index.py:167–196` | `oauth_swagger` | `959f1dc966c4b6379f68b0c8f0ece210ad51837dfcea764655085cc9f76ee805` |
| <a id="code-mah-f0171"></a>MAH-F0171 | `backend/api/v1/views/likes.py:13–16` | `legacy_likes_compatible` | `710a0c77cc60bbcac2fd2b095df42e9a3d07cfcba3c8971bfb9dc5dabbf823b5` |
| <a id="code-mah-f0172"></a>MAH-F0172 | `backend/api/v1/views/likes.py:19–24` | `like_state` | `710a0c77cc60bbcac2fd2b095df42e9a3d07cfcba3c8971bfb9dc5dabbf823b5` |
| <a id="code-mah-f0173"></a>MAH-F0173 | `backend/api/v1/views/likes.py:27–81` | `handle_like` | `710a0c77cc60bbcac2fd2b095df42e9a3d07cfcba3c8971bfb9dc5dabbf823b5` |
| <a id="code-mah-f0174"></a>MAH-F0174 | `backend/api/v1/views/likes.py:85–86` | `personal_story_like` | `710a0c77cc60bbcac2fd2b095df42e9a3d07cfcba3c8971bfb9dc5dabbf823b5` |
| <a id="code-mah-f0175"></a>MAH-F0175 | `backend/api/v1/views/likes.py:90–91` | `personal_comment_like` | `710a0c77cc60bbcac2fd2b095df42e9a3d07cfcba3c8971bfb9dc5dabbf823b5` |
| <a id="code-mah-f0177"></a>MAH-F0177 | `backend/api/v1/views/permissions.py:10–47` | `get_authenticated_user` | `287a3477cfc7e55705e49946e10732b78c3c31a88b1fa5cb661a768b0c64ca9e` |
| <a id="code-mah-f0178"></a>MAH-F0178 | `backend/api/v1/views/permissions.py:52–69` | `admin_required` | `287a3477cfc7e55705e49946e10732b78c3c31a88b1fa5cb661a768b0c64ca9e` |
| <a id="code-mah-f0180"></a>MAH-F0180 | `backend/api/v1/views/proposals.py:15–30` | `proposal_to_dict` | `b21ba8a26bcc4b909c33318020f6f25c26e78a54b0030caed4b122761de82373` |
| <a id="code-mah-f0181"></a>MAH-F0181 | `backend/api/v1/views/proposals.py:36–46` | `get_proposals` | `b21ba8a26bcc4b909c33318020f6f25c26e78a54b0030caed4b122761de82373` |
| <a id="code-mah-f0182"></a>MAH-F0182 | `backend/api/v1/views/proposals.py:52–92` | `create_proposal` | `b21ba8a26bcc4b909c33318020f6f25c26e78a54b0030caed4b122761de82373` |
| <a id="code-mah-f0189"></a>MAH-F0189 | `backend/api/v1/views/story_deletion_support.py:74–115` | `require_integrity` | `dcd40b316cd618ded49f122bdc7e2e9e2ec1890e7d50965932182a1a87c06689` |
| <a id="code-mah-f0190"></a>MAH-F0190 | `backend/api/v1/views/story_deletion_support.py:118–151` | `snapshot` | `dcd40b316cd618ded49f122bdc7e2e9e2ec1890e7d50965932182a1a87c06689` |
| <a id="code-mah-f0196"></a>MAH-F0196 | `backend/api/v1/views/story_deletion_support.py:188–200` | `deletion_preview` | `dcd40b316cd618ded49f122bdc7e2e9e2ec1890e7d50965932182a1a87c06689` |
| <a id="code-mah-f0197"></a>MAH-F0197 | `backend/api/v1/views/story_deletion_support.py:203–217` | `confirm_deletion` | `dcd40b316cd618ded49f122bdc7e2e9e2ec1890e7d50965932182a1a87c06689` |
| <a id="code-mah-f0198"></a>MAH-F0198 | `backend/api/v1/views/story_deletion_support.py:220–277` | `delete_story` | `dcd40b316cd618ded49f122bdc7e2e9e2ec1890e7d50965932182a1a87c06689` |
| <a id="code-mah-f0199"></a>MAH-F0199 | `backend/api/v1/views/story_deletion_support.py:280–294` | `run_deletion_action` | `dcd40b316cd618ded49f122bdc7e2e9e2ec1890e7d50965932182a1a87c06689` |
| <a id="code-mah-f0200"></a>MAH-F0200 | `backend/api/v1/views/story_visibility.py:10–24` | `get_active_story` | `9c3c2cc8e2350308a7e38adfe42edbd1a8a3586cd0d4e121a280794e242cfa8b` |
| <a id="code-mah-f0201"></a>MAH-F0201 | `backend/api/v1/views/theories.py:14–27` | `theory_to_dict` | `69545134b59eabf11e13a60545411af35a65650cec7fbc7bbe0769f7c9cde02a` |
| <a id="code-mah-f0202"></a>MAH-F0202 | `backend/api/v1/views/theories.py:36–55` | `get_theories` | `69545134b59eabf11e13a60545411af35a65650cec7fbc7bbe0769f7c9cde02a` |
| <a id="code-mah-f0203"></a>MAH-F0203 | `backend/api/v1/views/theories.py:64–112` | `post_theory` | `69545134b59eabf11e13a60545411af35a65650cec7fbc7bbe0769f7c9cde02a` |
| <a id="code-mah-f0204"></a>MAH-F0204 | `backend/api/v1/views/theories.py:121–156` | `like_theory` | `69545134b59eabf11e13a60545411af35a65650cec7fbc7bbe0769f7c9cde02a` |
| <a id="code-mah-f0205"></a>MAH-F0205 | `backend/api/v1/views/users.py:14–31` | `is_valid_password` | `aa0e48757d369a3aaed2cb598639fa79bbd88b4d6dba738c47f74ed34b649e9f` |
| <a id="code-mah-f0206"></a>MAH-F0206 | `backend/api/v1/views/users.py:37–44` | `get_users` | `aa0e48757d369a3aaed2cb598639fa79bbd88b4d6dba738c47f74ed34b649e9f` |
| <a id="code-mah-f0207"></a>MAH-F0207 | `backend/api/v1/views/users.py:50–116` | `register_user` | `aa0e48757d369a3aaed2cb598639fa79bbd88b4d6dba738c47f74ed34b649e9f` |
| <a id="code-mah-f0209"></a>MAH-F0209 | `backend/api/v1/views/write_support.py:20–26` | `json_object` | `c355734f64eae4acde4cd905a45034fec9291d9b390f79f7952bc0f2e8137742` |
| <a id="code-mah-f0210"></a>MAH-F0210 | `backend/api/v1/views/write_support.py:32–45` | `required_text` | `c355734f64eae4acde4cd905a45034fec9291d9b390f79f7952bc0f2e8137742` |
| <a id="code-mah-f0212"></a>MAH-F0212 | `backend/api/v1/views/write_support.py:59–88` | `is_unique_conflict` | `c355734f64eae4acde4cd905a45034fec9291d9b390f79f7952bc0f2e8137742` |
| <a id="source-8bc47a35d18a"></a>repère textuel exact | `backend/index.py:98` | `if all([` | `ac6a4e2d3d1470dadc7a8c37896bfb5534277b59c7d573c4e6f838fcfb179379` |
| <a id="code-mah-f0037"></a>MAH-F0037 | `backend/index.py:171–213` | `protect_session_requests_from_csrf` | `ac6a4e2d3d1470dadc7a8c37896bfb5534277b59c7d573c4e6f838fcfb179379` |
| <a id="code-mah-f0040"></a>MAH-F0040 | `backend/index.py:245–262` | `get_stats` | `ac6a4e2d3d1470dadc7a8c37896bfb5534277b59c7d573c4e6f838fcfb179379` |
| <a id="code-mah-f0041"></a>MAH-F0041 | `backend/index.py:269–335` | `login_user` | `ac6a4e2d3d1470dadc7a8c37896bfb5534277b59c7d573c4e6f838fcfb179379` |
| <a id="code-mah-f0042"></a>MAH-F0042 | `backend/index.py:342–359` | `get_current_user` | `ac6a4e2d3d1470dadc7a8c37896bfb5534277b59c7d573c4e6f838fcfb179379` |
| <a id="code-mah-f0043"></a>MAH-F0043 | `backend/index.py:366–372` | `logout_user` | `ac6a4e2d3d1470dadc7a8c37896bfb5534277b59c7d573c4e6f838fcfb179379` |
| <a id="source-3fc182b88cae"></a>repère textuel exact | `backend/tests/test_csrf.py:70` | `def test_login_exemption_survives_existing_session_and_invalid_tokens(` | `aa17fbf30e684611e08b277cf52b0368c5c0aa70ca3858060d167858a376a903` |
| <a id="source-6ab55a527fa3"></a>repère textuel exact | `backend/tests/test_csrf.py:84` | `def test_missing_header_token_is_403(` | `aa17fbf30e684611e08b277cf52b0368c5c0aa70ca3858060d167858a376a903` |
| <a id="source-769e483fb4ea"></a>repère textuel exact | `backend/tests/test_users_votes.py:201` | `def test_users_mysql_sqlite_unique_conflicts_are_400(` | `d85c94c7762863901063d7efc914f25227376d1db9cdc1a7c6f75dfa3f1c436a` |
| <a id="source-5398f2d4f335"></a>repère textuel exact | `backend/tests/test_users_votes.py:224` | `def test_other_constraints_are_500_not_business_conflicts(` | `d85c94c7762863901063d7efc914f25227376d1db9cdc1a7c6f75dfa3f1c436a` |
| <a id="source-fd79be9e1201"></a>repère textuel exact | `backend/tests/test_users_votes.py:235` | `def test_users_real_sqlite_unique_error_after_precheck(` | `d85c94c7762863901063d7efc914f25227376d1db9cdc1a7c6f75dfa3f1c436a` |
| <a id="source-c1ca58e3c82b"></a>repère textuel exact | `docs/soutenance/01_GUIDE_DIX_MODELES.md:1` | `#` | `fec1d7df50c3282a041116b28b0dc3e0e2aa3653e4f2db41997d5017e72dfccc` |
| <a id="source-6e0c7122c419"></a>repère textuel exact | `docs/soutenance/02_RELATIONS_CONTRAINTES_TRANSACTIONS.md:1` | `#` | `68e8f8337a248f3bd5318dca754519c45f1b875931361ccf7936260127adcc78` |
| <a id="source-088e1fc0828a"></a>repère textuel exact | `docs/soutenance/03_GUIDE_SEPT_MIGRATIONS.md:1` | `#` | `cf8ff2e9ff7e7bce8c53a33b48df253a072a1bfcf63f47040eb06b7ff3136a34` |
| <a id="source-b38431dc23f1"></a>repère textuel exact | `docs/soutenance/04_REPERTOIRE_FONCTIONS_METHODES.md:1` | `#` | `c207f01aa3abc45270897c645bd11ff3eeb8f98dba7f0a446ce242dc544e8768` |
| <a id="source-83e37800ea6d"></a>repère textuel exact | `docs/soutenance/05_DIAGRAMME_RELATIONNEL_COMMENTE.md:1` | `#` | `64b9e71507996927de4b54e79708021d0824b3ac3d7448d199e42b90ba88ba9c` |
| <a id="source-a23267386b96"></a>repère textuel exact | `docs/soutenance/06_CORRESPONDANCE_SOURCES.md:1` | `#` | `e031f0d0b1c82dcd38e1f61b867dc04c2ff11bb78b25a2eb33515d5fa612e64f` |
| <a id="source-9f6299f08111"></a>repère textuel exact | `docs/soutenance/07_VALIDATION_DOCUMENTAIRE.md:1` | `#` | `927de1a42c840c240a6c366958a67b7f06fb655e8009ddf7b14a185c68314e6f` |
| <a id="source-5cfeab467948"></a>repère textuel exact | `docs/soutenance/CONVENTIONS_COPIES_PEDAGOGIQUES_LOT6H21_1.md:1` | `#` | `41da6bb68e6b84e827f8baed27cbd9a8edf07cd429926e45abd38ead96a43207` |
| <a id="source-059d056c7b7c"></a>repère textuel exact | `docs/soutenance/INVENTAIRE_PEDAGOGIQUE_LOT6H21_1.json:2` | `"schema_version"` | `92a9242955c2c9e006092b808b8ef5765cf50d6057396f66cd8f4e5061497b59` |
| <a id="source-aaa596cc87f8"></a>repère textuel exact | `docs/soutenance/REFERENTIEL_PEDAGOGIQUE_LOT6H21_1.md:1` | `#` | `27620938a8cdf0cef6ef42d96fcb3ca2409384d8d95c00cf99c65fb453cc8c13` |
| <a id="source-a942fcd0fb9c"></a>repère textuel exact | `docs/soutenance/preuves-lot6h4/diagrammes/diagram-3.mmd:1` | `sequenceDiagram` | `f2bf3baeed3a951de18be227ed4effa6e101b66d4c127e95ca4cf24de9fa8b27` |
| <a id="source-4fce14e1480b"></a>repère textuel exact | `frontend/admin-dashboard.js:183` | `async function loadDashboard(` | `f1e6f3f4dab6403eeb9118c5dbdaff1819c6dbf60bfd293c446d339d8140ad67` |
| <a id="source-f020605da7a7"></a>repère textuel exact | `frontend/admin-stories.js:99` | `async function permanentlyDelete(` | `d873107a9b005b27a2a1cc3872db53352f50e3e096815b539454a28262be97bf` |
| <a id="source-58a85a045582"></a>repère textuel exact | `frontend/admin-stories.js:154` | `async function change(` | `d873107a9b005b27a2a1cc3872db53352f50e3e096815b539454a28262be97bf` |
| <a id="source-9416a00b2db5"></a>repère textuel exact | `frontend/admin-users.js:116` | `async function ban(` | `c68c8447fa09cf2f814bbcbca6b52ae7a8547f298f7995625bc358e6958ee0ff` |
| <a id="js-d39f6f0be41e"></a>fonction JavaScript nommée, repérage textuel | `frontend/api.js:8` | `apiRequest` | `1a1607415b7fad2cd7c9804d190d69b9391ce135572e842fab652121a3a72f07` |
| <a id="source-926f9a641341"></a>repère textuel exact | `frontend/api.js:115` | `async function login(` | `1a1607415b7fad2cd7c9804d190d69b9391ce135572e842fab652121a3a72f07` |
| <a id="source-4d669924268c"></a>repère textuel exact | `frontend/api.js:142` | `async function register(` | `1a1607415b7fad2cd7c9804d190d69b9391ce135572e842fab652121a3a72f07` |
| <a id="source-ad345c0a77e6"></a>repère textuel exact | `frontend/api.js:150` | `async function createProposal(` | `1a1607415b7fad2cd7c9804d190d69b9391ce135572e842fab652121a3a72f07` |
| <a id="source-c6a179a6c72f"></a>repère textuel exact | `frontend/api.js:159` | `async function createTheory(` | `1a1607415b7fad2cd7c9804d190d69b9391ce135572e842fab652121a3a72f07` |
| <a id="source-ec2bafc5e576"></a>repère textuel exact | `frontend/api.js:194` | `async function getStoryBySlug(` | `1a1607415b7fad2cd7c9804d190d69b9391ce135572e842fab652121a3a72f07` |
| <a id="source-52e2a5e5d40d"></a>repère textuel exact | `frontend/api.js:222` | `async function getAdminStats(` | `1a1607415b7fad2cd7c9804d190d69b9391ce135572e842fab652121a3a72f07` |
| <a id="source-c4fd7461d759"></a>repère textuel exact | `frontend/api.js:297` | `async function banAdminUser(` | `1a1607415b7fad2cd7c9804d190d69b9391ce135572e842fab652121a3a72f07` |
| <a id="source-e5c9468a4d0a"></a>repère textuel exact | `frontend/api.js:346` | `async function changeAdminStoryArchive(` | `1a1607415b7fad2cd7c9804d190d69b9391ce135572e842fab652121a3a72f07` |
| <a id="source-19dd32ee73ca"></a>repère textuel exact | `frontend/api.js:392` | `async function deleteAdminStory(` | `1a1607415b7fad2cd7c9804d190d69b9391ce135572e842fab652121a3a72f07` |
| <a id="source-4c9a7fe22809"></a>repère textuel exact | `frontend/api.js:443` | `async function createComment(` | `1a1607415b7fad2cd7c9804d190d69b9391ce135572e842fab652121a3a72f07` |
| <a id="source-8ebdf054d05f"></a>repère textuel exact | `frontend/api.js:454` | `async function reportComment(` | `1a1607415b7fad2cd7c9804d190d69b9391ce135572e842fab652121a3a72f07` |
| <a id="source-c8b9be370f31"></a>repère textuel exact | `frontend/api.js:483` | `async function changeLike(` | `1a1607415b7fad2cd7c9804d190d69b9391ce135572e842fab652121a3a72f07` |
| <a id="source-01b06274624c"></a>repère textuel exact | `frontend/app.js:244` | `async function loadStory(` | `e9175a832bd4f35c4b531c69d7d8e8f8e6b760b97a85d83528c809f766067a3d` |
| <a id="source-f4fcc17e6b2d"></a>repère textuel exact | `frontend/app.js:349` | `theoryForm.addEventListener` | `e9175a832bd4f35c4b531c69d7d8e8f8e6b760b97a85d83528c809f766067a3d` |
| <a id="source-5ca830192df9"></a>repère textuel exact | `frontend/app.js:434` | `proposalForm.addEventListener` | `e9175a832bd4f35c4b531c69d7d8e8f8e6b760b97a85d83528c809f766067a3d` |
| <a id="source-e48b723d12c6"></a>repère textuel exact | `frontend/app.js:498` | `signupForm.addEventListener` | `e9175a832bd4f35c4b531c69d7d8e8f8e6b760b97a85d83528c809f766067a3d` |
| <a id="source-65e0e5f3c0a9"></a>repère textuel exact | `frontend/app.js:533` | `loginForm.addEventListener` | `e9175a832bd4f35c4b531c69d7d8e8f8e6b760b97a85d83528c809f766067a3d` |
| <a id="source-d3c472550f95"></a>repère textuel exact | `frontend/comments.js:144` | `async function submit(` | `6ca9ec23f8c4682e9df3e970be6f3800cd2ca76808ff5cce2e273cd67e376fac` |
| <a id="source-9b399889e3b1"></a>repère textuel exact | `frontend/likes.js:2` | `function createLikeControl(` | `a58894140569d55b7e0f749e1ac0380f18bab3d49c01ccf3cfc124e82a25b4ac` |
| <a id="code-mah-f0044"></a>MAH-F0044 | `run_local.py:17–63` | `create_local_app` | `6df80484f07b1056c0265508c32346939206ffe16a3d9f67258a3e79abaa413e` |
| <a id="code-mah-f0048"></a>MAH-F0048 | `run_local.py:68–78` | `main` | `6df80484f07b1056c0265508c32346939206ffe16a3d9f67258a3e79abaa413e` |
| <a id="code-mah-f0056"></a>MAH-F0056 | `tools/demo_persistante.py:85–96` | `Paths.checked` | `e07bcde7ab5f19b6f9190bbc03c8b22b4bed5aab4e46314fe4b565401b21220c` |
| <a id="code-mah-f0060"></a>MAH-F0060 | `tools/demo_persistante.py:184–218` | `operation_lock` | `e07bcde7ab5f19b6f9190bbc03c8b22b4bed5aab4e46314fe4b565401b21220c` |
| <a id="code-mah-f0065"></a>MAH-F0065 | `tools/demo_persistante.py:256–289` | `inspect_database` | `e07bcde7ab5f19b6f9190bbc03c8b22b4bed5aab4e46314fe4b565401b21220c` |
| <a id="code-mah-f0083"></a>MAH-F0083 | `tools/demo_persistante.py:451–484` | `initialize` | `e07bcde7ab5f19b6f9190bbc03c8b22b4bed5aab4e46314fe4b565401b21220c` |
| <a id="code-mah-f0086"></a>MAH-F0086 | `tools/demo_persistante.py:500–516` | `backup` | `e07bcde7ab5f19b6f9190bbc03c8b22b4bed5aab4e46314fe4b565401b21220c` |
| <a id="code-mah-f0087"></a>MAH-F0087 | `tools/demo_persistante.py:519–553` | `restore` | `e07bcde7ab5f19b6f9190bbc03c8b22b4bed5aab4e46314fe4b565401b21220c` |
| <a id="code-mah-f0088"></a>MAH-F0088 | `tools/demo_persistante.py:556–572` | `serve` | `e07bcde7ab5f19b6f9190bbc03c8b22b4bed5aab4e46314fe4b565401b21220c` |
| <a id="code-mah-f0113"></a>MAH-F0113 | `tools/recette_lot6g4.py:327–351` | `seed` | `06417d8d78dd85850ba814ac5963426f44a003d3dbdf9765f3308cb3969cd908` |
| <a id="code-mah-f0121"></a>MAH-F0121 | `tools/recette_lot6g4.py:474–630` | `main` | `06417d8d78dd85850ba814ac5963426f44a003d3dbdf9765f3308cb3969cd908` |

## Préparer les relances du jury

Pour une opération donnée, annoncer d’abord son intention métier, puis la route et son contrôle de droit, ensuite la requête construite, son exécution et sa limite transactionnelle. Finir par ce que l’utilisateur voit et ce qui reste incertain si l’accusé se perd. Cette démarche oblige à comprendre le code au lieu de réciter « ORM = sécurisé » ou « commit = succès du navigateur ».

Exercice : comparer un POST de proposition, un like individuel et une purge. Tous peuvent écrire en base, mais ils n’ont ni la même unicité, ni le même statut de succès, ni la même prévention de relance, ni la même gestion de l’issue de commit inconnue. Les matrices des parcours et du guide de sécurité fournissent les points de distinction.
