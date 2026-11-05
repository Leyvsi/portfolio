# Guide approfondi des sept migrations Alembic

Les Petits Enquêteurs — lot 6H.21.4 — 4 novembre 2026, Europe/Paris.

**Proposition externe à lire et à approuver avant installation.** Sources : copie intégrée locale, photographiée par SHA-256 ; pas la seule version du commit Git. Analyse statique : aucun import de l’application, accès SQL, test applicatif ni migration exécutée pour cette rédaction. Les exemples sont pédagogiques et non exécutés. Leur éventuelle exécution exige un contexte temporaire distinct, préparé et autorisé ; ils ne constituent pas des scripts de démarrage du projet.

[Sommaire de soutenance](README.md) · [Correspondance avec les sources](06_CORRESPONDANCE_SOURCES.md) · [Validation documentaire](07_VALIDATION_DOCUMENTAIRE.md)

## Modèles actuels, historique et état réel : trois objets différents

models.py décrit le schéma attendu par le code courant. Une révision Alembic décrit une transition depuis un état parent. L’état d’une base réelle dépend de ce qui y a été appliqué et de ses données. Cette session étudie les deux premiers objets et ne lit pas le troisième.

`revision` identifie une étape ; `down_revision` donne son parent. Ces chaînes ne sont pas des numéros à trier lexicalement. La racine a down_revision=None ; la tête fournie est c6g200000001. `upgrade()` avance une étape, `downgrade()` tente son inverse de schéma. Alembic gère sa table de version dans son contexte d’exécution ; ce n’est pas un onzième modèle applicatif.

`create_all()` ne rejoue pas les migrations et ne convertit pas une ancienne table Report. De même, stamp marque une révision sans effectuer ses transformations : ce n’est pas une correction de schéma. Aucun de ces chemins n’est exécuté pour produire ces guides.

## Chaîne complète et identifiants pédagogiques


```text
base
  → 921687c1bd7c
  → 3111f5767fc6
  → a590c8aac613
  → 82deda84bc35
  → c6c100000001
  → c6c200000001
  → c6g200000001 (tête des sources)
```

| Révision | Parent | Module stable | Upgrade / downgrade |
|---|---|---|---|
| [921687c1bd7c](#rev-921687c1bd7c) | `None` | MAH-M005 | [MAH-F0023](04_REPERTOIRE_FONCTIONS_METHODES.md#mah-f0023) / [MAH-F0024](04_REPERTOIRE_FONCTIONS_METHODES.md#mah-f0024) |
| [3111f5767fc6](#rev-3111f5767fc6) | `921687c1bd7c` | MAH-M003 | [MAH-F0019](04_REPERTOIRE_FONCTIONS_METHODES.md#mah-f0019) / [MAH-F0020](04_REPERTOIRE_FONCTIONS_METHODES.md#mah-f0020) |
| [a590c8aac613](#rev-a590c8aac613) | `3111f5767fc6` | MAH-M006 | [MAH-F0025](04_REPERTOIRE_FONCTIONS_METHODES.md#mah-f0025) / [MAH-F0026](04_REPERTOIRE_FONCTIONS_METHODES.md#mah-f0026) |
| [82deda84bc35](#rev-82deda84bc35) | `a590c8aac613` | MAH-M004 | [MAH-F0021](04_REPERTOIRE_FONCTIONS_METHODES.md#mah-f0021) / [MAH-F0022](04_REPERTOIRE_FONCTIONS_METHODES.md#mah-f0022) |
| [c6c100000001](#rev-c6c100000001) | `82deda84bc35` | MAH-M007 | [MAH-F0027](04_REPERTOIRE_FONCTIONS_METHODES.md#mah-f0027) / [MAH-F0028](04_REPERTOIRE_FONCTIONS_METHODES.md#mah-f0028) |
| [c6c200000001](#rev-c6c200000001) | `c6c100000001` | MAH-M008 | [MAH-F0030](04_REPERTOIRE_FONCTIONS_METHODES.md#mah-f0030) / [MAH-F0031](04_REPERTOIRE_FONCTIONS_METHODES.md#mah-f0031) |
| [c6g200000001](#rev-c6g200000001) | `c6c200000001` | MAH-M009 | [MAH-F0033](04_REPERTOIRE_FONCTIONS_METHODES.md#mah-f0033) / [MAH-F0034](04_REPERTOIRE_FONCTIONS_METHODES.md#mah-f0034) |

## Évolution cumulative du schéma, sans exécution

| Après la révision | Tables applicatives | Colonnes déclarées cumulées | FK | Lecture du changement |
|---|---:|---:|---:|---|
| 921687c1bd7c | 7 | 45 | 9 | Schéma historique |
| 3111f5767fc6 | 7 | 45 | 9 | Remplacement de sept FK, pas ajout |
| a590c8aac613 | 9 | 56 | 10 | Deux tables + is_banned |
| 82deda84bc35 | 9 | 55 | 10 | Suppression du compteur comments.reports |
| c6c100000001 | 9 | 56 | 10 | Ajout d’archived_at |
| c6c200000001 | 9 | 56 | 11 | reports perd deux colonnes et en gagne une ; stories gagne une colonne |
| c6g200000001 | 10 | 60 | 13 | Quatre colonnes et deux FK de comment_likes |

Ce tableau résulte de la lecture des opérations. Ce n’est ni une introspection d’une base ni une preuve de réussite de la chaîne sur un moteur.

<a id="rev-921687c1bd7c"></a>

## 921687c1bd7c — Établir le schéma historique initial

**Fichier :** `migrations/versions/921687c1bd7c_baseline_schema.py`. **Parent :** `None`. **Points d’entrée :** [MAH-F0023](04_REPERTOIRE_FONCTIONS_METHODES.md#mah-f0023) à la ligne 22, [MAH-F0024](04_REPERTOIRE_FONCTIONS_METHODES.md#mah-f0024) à la ligne 175. Paramètres publics : aucun ; retour normal : None. Alembic fournit op et sa connexion de contexte.

### Objectif et préconditions

Cette révision sans parent est la racine de l’historique livré. Elle crée les tables historiques, pas directement les dix modèles actuels. Une base neuve doit ensuite parcourir les six autres révisions pour obtenir le schéma actuel. Le nom « baseline » ne signifie pas que l’on peut marquer sans vérification une base existante comme conforme.

La base doit correspondre à la révision parente attendue, avec le schéma et les noms de contraintes requis. Aucun chemin de découverte automatique d’une base privée n’est proposé.

### Upgrade, étape par étape

1. Créer users : id Integer PK, username String(100) UNIQUE obligatoire, email String(150) UNIQUE obligatoire, password_hash String(255) obligatoire, is_admin Boolean obligatoire et created_at DateTime obligatoire. is_banned est absent.
2. Créer categories : id Integer PK, name String(100) UNIQUE obligatoire et description Text nullable.
3. Créer stories : id PK, slug String(150) UNIQUE, title String(200), summary et content Text, image_url String(500) nullable, category_id et author_id obligatoires, created_at et updated_at DateTime obligatoires. Nommer les deux FK stories_ibfk_1 et stories_ibfk_2, sans ON DELETE explicite. archived_at et management_revision sont absents.
4. Créer theories : id PK, story_id obligatoire, user_id nullable, title String(200), content Text, likes Integer et created_at DateTime obligatoires ; deux FK nommées theories_ibfk_1/2 sans ON DELETE explicite.
5. Créer comments : id PK, story_id obligatoire, user_id et username String(100) nullables, text Text, likes Integer, reports Integer et created_at obligatoires ; FK comments_ibfk_1/2 sans ON DELETE explicite.
6. Créer votes : id PK, story_id et user_id obligatoires, created_at DateTime obligatoire, FK votes_ibfk_1/2 sans ON DELETE explicite ; contrainte unique_user_story_vote sur user_id/story_id.
7. Créer proposals : id PK, user_id obligatoire, title String(200), content Text, status String(20), created_at et updated_at DateTime obligatoires ; FK proposals_ibfk_1 sans ON DELETE explicite.

### Downgrade, étape par étape

1. Supprimer proposals, puis votes, comments et theories.
2. Supprimer stories avant categories et users, afin de retirer d’abord les dépendances prévues par cette révision.

### Conséquences sur les données

Upgrade ne crée aucun compte, récit, catégorie ou jeu de démonstration. Les colonnes obligatoires n’ont pas les callbacks Python du modèle dans ce DDL : un INSERT SQL direct doit fournir les valeurs nécessaires, dont dates, booléens et compteurs. Downgrade détruit toutes les lignes de ces sept tables ; il ne produit aucune sauvegarde.

### SQLite et MySQL : portée exacte

Les opérations utilisent les types et primitives SQLAlchemy/Alembic communs. La matérialisation des types, PK et contraintes dépend du moteur. Les noms de FK historiques sont nécessaires à la révision suivante ; une base créée autrement, notamment avec create_all, ne doit pas être supposée porter ces mêmes noms. Aucun nouveau replay SQLite ni MySQL n’est exécuté dans ce lot.

### Erreurs, limites et précautions

Une racine n’est pas une migration idempotente « create if not exists ». Si des tables homonymes existent déjà, l’opération peut échouer ou ne pas correspondre à l’historique attendu. Le downgrade total est destructif et n’est pas une manière de réinitialiser la démonstration persistante.

Les erreurs de réflexion, de contrainte, de droit, de connexion et de DDL peuvent aussi remonter via SQLAlchemy/Alembic. Une liste de raise explicites ne serait pas une liste exhaustive des exceptions possibles. Aucune exception n’a été provoquée contre une base réelle pour ce document.

### Exemple mental à raconter

Avant cette racine, aucune des sept tables n’est créée par cet historique ; après elle, le schéma existe mais pas les six récits. Les autres révisions ajoutent ce qui manque au modèle courant.

<a id="rev-3111f5767fc6"></a>

## 3111f5767fc6 — Rendre explicites les règles de suppression

**Fichier :** `migrations/versions/3111f5767fc6_ajoute_les_regles_on_delete.py`. **Parent :** `921687c1bd7c`. **Points d’entrée :** [MAH-F0019](04_REPERTOIRE_FONCTIONS_METHODES.md#mah-f0019) à la ligne 21, [MAH-F0020](04_REPERTOIRE_FONCTIONS_METHODES.md#mah-f0020) à la ligne 130. Paramètres publics : aucun ; retour normal : None. Alembic fournit op et sa connexion de contexte.

### Objectif et préconditions

Remplacer sept FK historiques de quatre tables par des FK nommées portant CASCADE ou SET NULL. Aucune nouvelle colonne, table ou valeur de compteur n’est introduite. Les clés de catégorie et d’auteur de stories ne sont pas modifiées.

La base doit correspondre à la révision parente attendue, avec le schéma et les noms de contraintes requis. Aucun chemin de découverte automatique d’une base privée n’est proposé.

### Upgrade, étape par étape

1. Dans comments, supprimer comments_ibfk_1 et comments_ibfk_2 ; créer fk_comments_story vers stories.id avec CASCADE et fk_comments_user vers users.id avec SET NULL.
2. Dans proposals, supprimer proposals_ibfk_1 ; créer fk_proposals_user vers users.id avec CASCADE.
3. Dans theories, supprimer theories_ibfk_1 et theories_ibfk_2 ; créer fk_theories_story avec CASCADE et fk_theories_user avec SET NULL.
4. Dans votes, supprimer votes_ibfk_1 et votes_ibfk_2 ; créer fk_votes_story et fk_votes_user, tous deux CASCADE. La contrainte unique du couple reste distincte.

### Downgrade, étape par étape

1. Traiter votes, theories, proposals puis comments : supprimer les sept nouvelles FK nommées.
2. Recréer les contraintes anciennes *_ibfk_* sur les mêmes colonnes et parents, sans ON DELETE explicite. Ne pas attribuer à ce retour une restauration des lignes antérieurement supprimées.

### Conséquences sur les données

Les références d’auteur déjà nullables de comments et theories permettent SET NULL sans ajouter une modification de nullable. Aucun UPDATE de contenu n’apparaît. Une reconstruction de table copie les lignes conservées. Après application, les futurs DELETE de parents peuvent produire des effets différents : le changement de contrainte a donc des conséquences métier même sans DML explicite dans la migration.

### SQLite et MySQL : portée exacte

Les quatre batch_alter_table permettent à Alembic de reconstruire une table sous SQLite lorsque l’opération le nécessite. Des dépendances entrantes peuvent rendre un DROP de table parent dangereux si les FK et cascades sont actives : l’environnement actuel encadre SQLite dans sqlite_migration_scope. Sur MySQL, ces opérations se traduisent normalement par des ALTER de contraintes ; les noms attendus doivent exister et les DDL ne sont pas une transaction globale annulable.

### Erreurs, limites et précautions

Une base présentant déjà des noms différents ou des données hors intégrité doit être examinée avant une campagne. Downgrade retire les règles, mais ne retrouve pas les enfants effacés lors d’anciens DELETE CASCADE, ni l’identité de comptes retirée par SET NULL. Ne pas assimiler inverse du schéma et restauration de données.

Les erreurs de réflexion, de contrainte, de droit, de connexion et de DDL peuvent aussi remonter via SQLAlchemy/Alembic. Une liste de raise explicites ne serait pas une liste exhaustive des exceptions possibles. Aucune exception n’a été provoquée contre une base réelle pour ce document.

### Exemple mental à raconter

Un commentaire conservé après une suppression de compte peut avoir user_id NULL ; il ne faut pas faire disparaître son texte pour simuler cette règle. La suppression d’un dossier suit au contraire CASCADE.

<a id="rev-a590c8aac613"></a>

## a590c8aac613 — Ajouter signalements, bannissement et mises à jour

**Fichier :** `migrations/versions/a590c8aac613_add_reports_bans_and_cold_case_updates.py`. **Parent :** `3111f5767fc6`. **Points d’entrée :** [MAH-F0025](04_REPERTOIRE_FONCTIONS_METHODES.md#mah-f0025) à la ligne 21, [MAH-F0026](04_REPERTOIRE_FONCTIONS_METHODES.md#mah-f0026) à la ligne 76. Paramètres publics : aucun ; retour normal : None. Alembic fournit op et sa connexion de contexte.

### Objectif et préconditions

Introduire la modération et les nouvelles informations sur dossier : reports au format générique historique, cold_case_updates, et users.is_banned. Le correctif SQLite de cette révision historique est présent dans la copie étudiée ; le code actuel ne doit pas être remplacé par le texte d’une ancienne version du lot.

La base doit correspondre à la révision parente attendue, avec le schéma et les noms de contraintes requis. Aucun chemin de découverte automatique d’une base privée n’est proposé.

### Upgrade, étape par étape

1. Identifier le dialecte. Si SQLite, refuser avant tout DDL si PRAGMA foreign_keys est actif ou si le marqueur sqlite_migration_integrity_scope est absent. L’appel doit passer par l’enveloppe de maintenance dédiée.
2. Créer reports avec id PK, type String(100), target_id String(100), reason Text, status String(20), created_at DateTime, tous obligatoires. Dans cet état intermédiaire, la cible n’est pas une FK.
3. Créer cold_case_updates : id PK, story_id Integer obligatoire avec fk_cold_case_updates_story CASCADE, content Text et created_at DateTime obligatoires.
4. Ajouter users.is_banned Boolean obligatoire avec server_default=sa.false() pour renseigner les comptes existants.
5. Retirer le défaut SQL temporaire : SQLite passe par batch_alter_table(users) avec existing_type Boolean ; les autres dialectes gardent op.alter_column(users, is_banned, server_default=None).

### Downgrade, étape par étape

1. Supprimer cold_case_updates puis reports, avec leurs lignes.
2. Supprimer users.is_banned ; l’information de bannissement est perdue.

### Conséquences sur les données

Les comptes existants reçoivent false pendant l’ajout de colonne. Le défaut SQL est ensuite retiré ; les insertions ORM ultérieures utilisent le défaut Python de User. La migration ne crée aucun signalement ni mise à jour et n’attribue aucune cible textuelle à un commentaire. Downgrade fait perdre les motifs et textes stockés dans les deux tables ainsi que l’état de bannissement.

### SQLite et MySQL : portée exacte

SQLite ne sait pas retirer un défaut de colonne par le même ALTER que MySQL ; la reconstruction de users, table parent, explique l’enveloppe qui suspend temporairement les FK et vérifie l’intégrité. La branche non SQLite reste distincte : ce n’est pas une application des PRAGMA à MySQL. L’examen de cette séparation n’est pas une exécution sur MySQL/Aiven et ne couvre pas tous les dialectes SQL possibles.

### Erreurs, limites et précautions

L’enveloppe est une condition de fonctionnement en maintenance, pas une frontière de sécurité contre du code arbitraire. Le marqueur connection.info est modifiable en Python. Un accès exclusif doit être réellement organisé pour toute future migration. Aucun essai sur la base persistante n’a lieu pour ce guide.

Les erreurs de réflexion, de contrainte, de droit, de connexion et de DDL peuvent aussi remonter via SQLAlchemy/Alembic. Une liste de raise explicites ne serait pas une liste exhaustive des exceptions possibles. Aucune exception n’a été provoquée contre une base réelle pour ce document.

### Exemple mental à raconter

Un compte antérieur gagne un indicateur de bannissement initialement faux. Le signalement ajouté à cette époque vise encore une cible textuelle sans FK ; la précision actuelle viendra plus tard.

<a id="rev-82deda84bc35"></a>

## 82deda84bc35 — Supprimer le compteur redondant de signalements

**Fichier :** `migrations/versions/82deda84bc35_remove_legacy_comment_reports_counter.py`. **Parent :** `a590c8aac613`. **Points d’entrée :** [MAH-F0021](04_REPERTOIRE_FONCTIONS_METHODES.md#mah-f0021) à la ligne 21, [MAH-F0022](04_REPERTOIRE_FONCTIONS_METHODES.md#mah-f0022) à la ligne 28. Paramètres publics : aucun ; retour normal : None. Alembic fournit op et sa connexion de contexte.

### Objectif et préconditions

Retirer comments.reports pour calculer les signalements depuis les lignes de reports. Cela évite de devoir synchroniser un compteur et une table de signalements. Cette révision se situe encore avant la conversion des cibles de reports en FK comment_id.

La base doit correspondre à la révision parente attendue, avec le schéma et les noms de contraintes requis. Aucun chemin de découverte automatique d’une base privée n’est proposé.

### Upgrade, étape par étape

1. Ouvrir un batch_alter_table sur comments.
2. Supprimer la seule colonne reports ; ne pas supprimer la table reports et ne pas toucher à comments.likes.

### Downgrade, étape par étape

1. Ouvrir un premier batch sur comments et rajouter reports Integer NOT NULL avec server_default="0".
2. Ouvrir un second batch et retirer ce défaut SQL. Il n’y a ni SELECT des signalements, ni UPDATE de recalcul du compteur.

### Conséquences sur les données

Upgrade perd les anciennes valeurs du compteur. Les lignes de la table reports restent présentes. Downgrade remplit le compteur recréé à zéro pour les lignes existantes, puis retire le défaut : il ne récupère ni les anciens nombres ni un COUNT des signalements actuels. Un ancien programme lisant ce compteur pourra donc observer zéro même si des signalements existent.

### SQLite et MySQL : portée exacte

Le batch peut reconstruire comments sous SQLite ; les enfants introduits plus tard (reports.comment_id et comment_likes.comment_id) expliquent la nécessité d’une stratégie maîtrisée pour un aller-retour complet de l’historique actuel. Sous MySQL, les opérations de colonne relèvent des DDL du serveur. Aucune réussite MySQL n’est déduite des précédents tests SQLite.

### Erreurs, limites et précautions

**Rectification pédagogique ciblée :** le contrat gelé 6H.21.1 de MAH-F0022 évoque un recalcul à partir des lignes. Le corps source n’en comporte aucun. Le présent guide et le répertoire donnent le comportement exact sans modifier le document historique ni sa numérotation. Un downgrade n’est donc pas une restauration fonctionnelle garantie de l’ancien compteur.

Les erreurs de réflexion, de contrainte, de droit, de connexion et de DDL peuvent aussi remonter via SQLAlchemy/Alembic. Une liste de raise explicites ne serait pas une liste exhaustive des exceptions possibles. Aucune exception n’a été provoquée contre une base réelle pour ce document.

### Exemple mental à raconter

Si trois lignes Report existent, supprimer la colonne compteur n’efface pas ces trois lignes. Revenir en arrière remet le compteur à zéro, et non à trois.

<a id="rev-c6c100000001"></a>

## c6c100000001 — Ajouter l’archivage logique des dossiers

**Fichier :** `migrations/versions/c6c100000001_add_story_archive_date.py`. **Parent :** `82deda84bc35`. **Points d’entrée :** [MAH-F0027](04_REPERTOIRE_FONCTIONS_METHODES.md#mah-f0027) à la ligne 16, [MAH-F0028](04_REPERTOIRE_FONCTIONS_METHODES.md#mah-f0028) à la ligne 22. Paramètres publics : aucun ; retour normal : None. Alembic fournit op et sa connexion de contexte.

### Objectif et préconditions

Distinguer un dossier actif d’un dossier archivé sans supprimer le dossier ou ses contributions. La donnée de gestion est une date nullable, pas un nouveau booléen et pas une nouvelle table.

La base doit correspondre à la révision parente attendue, avec le schéma et les noms de contraintes requis. Aucun chemin de découverte automatique d’une base privée n’est proposé.

### Upgrade, étape par étape

1. Ajouter stories.archived_at avec sa.DateTime(), nullable=True.
2. Ne définir aucun server_default et ne modifier ni FK, ni enfant, ni compteur. Les lignes existantes ont NULL dans cette nouvelle colonne.

### Downgrade, étape par étape

1. Supprimer stories.archived_at.
2. Ne pas supprimer les histoires ; constater que l’information permettant de distinguer les archives disparaît.

### Conséquences sur les données

Après upgrade, les dossiers préexistants sont considérés actifs par le code qui lit NULL comme état actif. L’archive future sera une affectation effectuée par la route de gestion. Downgrade perd les dates d’archive ; l’ancien code peut rendre visibles des dossiers auparavant archivés. Cela implique un risque de visibilité même sans suppression de texte.

### SQLite et MySQL : portée exacte

L’ajout nullable est une primitive commune Alembic ; la stratégie effective de DROP COLUMN dépend des versions du moteur et de l’implémentation du dialecte. Le script n’ajoute pas de branche spécifique MySQL ou SQLite. Le succès d’une version SQLite antérieure ne prouve pas celui d’un autre serveur ni de toutes les versions SQLite.

### Erreurs, limites et précautions

Une colonne disponible ne prouve pas que toutes les routes appliquent la visibilité. La classe Story et les vues de story_visibility/admin_stories travaillent ensemble. Cette documentation décrit le code, sans ouvrir le service pour observer son état courant.

Les erreurs de réflexion, de contrainte, de droit, de connexion et de DDL peuvent aussi remonter via SQLAlchemy/Alembic. Une liste de raise explicites ne serait pas une liste exhaustive des exceptions possibles. Aucune exception n’a été provoquée contre une base réelle pour ce document.

### Exemple mental à raconter

Un dossier préexistant reçoit NULL et reste actif. Après une archive future, retirer la colonne effacerait le seul marqueur d’archive, même si le récit existe toujours.

<a id="rev-c6c200000001"></a>

## c6c200000001 — Rendre les signalements référentiels et réviser la gestion

**Fichier :** `migrations/versions/c6c200000001_comment_reports_and_story_revision.py`. **Parent :** `c6c100000001`. **Points d’entrée :** [MAH-F0030](04_REPERTOIRE_FONCTIONS_METHODES.md#mah-f0030) à la ligne 42, [MAH-F0031](04_REPERTOIRE_FONCTIONS_METHODES.md#mah-f0031) à la ligne 65. Paramètres publics : aucun ; retour normal : None. Alembic fournit op et sa connexion de contexte.

### Objectif et préconditions

Remplacer les cibles textuelles des signalements par une vraie référence à Comment et ajouter un témoin unique de gestion aux dossiers. La migration distingue contrôle des données avant DDL et transformation du schéma. Elle refuse les références ambiguës plutôt que de les corriger arbitrairement.

La base doit correspondre à la révision parente attendue, avec le schéma et les noms de contraintes requis. Aucun chemin de découverte automatique d’une base privée n’est proposé.

### Upgrade, étape par étape

1. Appeler inspect_legacy(bind), MAH-F0029, avant le premier DDL : vérifier le type entier de comments.id, charger les anciens reports et les identifiants de commentaires ; accepter seulement type="comment" et une cible chaîne ASCII canonique [1-9][0-9]{0,9}, <=2147483647, existante.
2. Recevoir un tuple (copie du type de PK, liste de correspondances report_id/comment_id). Ajouter reports.comment_id avec ce type, d’abord nullable pour permettre le remplissage.
3. Mettre à jour chaque ligne de reports à partir de la correspondance validée, sans copier son motif dans un message d’erreur.
4. Dans le batch reports : rendre comment_id obligatoire, créer fk_reports_comment CASCADE, supprimer type et target_id, créer l’index non unique ix_reports_comment_id.
5. Ajouter stories.management_revision String(32) NOT NULL avec server_default égal à 32 zéros ; puis attribuer un uuid4().hex distinct généré à chaque dossier existant.
6. Créer uq_stories_management_revision comme index UNIQUE. Le défaut SQL sentinelle reste dans le schéma ; l’ORM génère ensuite ses propres UUID pour ses INSERT.

### Downgrade, étape par étape

1. Ajouter reports.type et reports.target_id String(100), temporairement nullables.
2. Parcourir les signalements actuels : écrire type="comment" et target_id=str(comment_id).
3. En batch : supprimer fk_reports_comment et ix_reports_comment_id, rendre les deux colonnes textuelles obligatoires, supprimer comment_id.
4. Supprimer l’index unique uq_stories_management_revision puis la colonne stories.management_revision.

### Conséquences sur les données

Les ids de signalement, motifs, statuts et dates sont conservés dans le chemin valide ; les anciennes cibles invalides provoquent un refus, pas une suppression silencieuse de signalements. Le nouveau lien rend les DELETE de commentaires cascades sur les signalements. Downgrade produit le format générique à partir des seules références actuelles ; il ne ressuscite aucune cible ou ligne supprimée auparavant. Les valeurs de révision de gestion sont perdues au retour.

### SQLite et MySQL : portée exacte

La copie du type parent aide à conserver les caractéristiques SQL de la FK, au lieu d’imposer un type supposé. Le batch reports concerne une table enfant sans FK entrante recensée par ces modèles ; la stratégie globale SQLite reste gérée par env.py. MySQL peut committer des DDL implicitement : un précontrôle réussi ne garantit pas que toute la suite soit annulable. Les écrivains concurrents doivent être drainés pour éviter que les données changent entre contrôle et transformation.

### Erreurs, limites et précautions

L’inspection charge les signalements et ids parents en mémoire : coût linéaire dans leur volume, pas une reprise paginée. Une collision UUID très improbable peut faire échouer l’unicité ; la sentinelle future n’est pas une vraie révision acceptable pour la purge. Un schéma partiellement modifié après erreur MySQL exigerait une analyse spécifique ; ne pas proposer de réexécution aveugle. Aucune de ces procédures n’est lancée ici.

Les erreurs de réflexion, de contrainte, de droit, de connexion et de DDL peuvent aussi remonter via SQLAlchemy/Alembic. Une liste de raise explicites ne serait pas une liste exhaustive des exceptions possibles. Aucune exception n’a été provoquée contre une base réelle pour ce document.

### Exemple mental à raconter

Une ancienne cible fictive "23" de type comment est convertible seulement si le commentaire 23 existe. Une cible "023" est refusée au lieu d’être interprétée silencieusement.

<a id="rev-c6g200000001"></a>

## c6g200000001 — Introduire les likes de commentaires attribuables

**Fichier :** `migrations/versions/c6g200000001_add_comment_likes.py`. **Parent :** `c6c200000001`. **Points d’entrée :** [MAH-F0033](04_REPERTOIRE_FONCTIONS_METHODES.md#mah-f0033) à la ligne 48, [MAH-F0034](04_REPERTOIRE_FONCTIONS_METHODES.md#mah-f0034) à la ligne 65. Paramètres publics : aucun ; retour normal : None. Alembic fournit op et sa connexion de contexte.

### Objectif et préconditions

Créer une association individuelle par compte et commentaire, en refusant d’inventer les auteurs des anciens compteurs. Cette dernière révision conserve la colonne historique Comment.likes et toutes les lignes Vote.

La base doit correspondre à la révision parente attendue, avec le schéma et les noms de contraintes requis. Aucun chemin de découverte automatique d’une base privée n’est proposé.

### Upgrade, étape par étape

1. Appeler inspect_legacy(bind), MAH-F0032, avant DDL. SQLite exige les FK actives, ou l’enveloppe identifiée avec foreign_key_check vide. MySQL exige foreign_key_checks=1 et les parents comments/users en InnoDB.
2. Refuser si comment_likes existe déjà ; inspecter comments.id et users.id et exiger un type dérivé de sa.Integer. Copier ces deux types dans une liste renvoyée à upgrade.
3. Lire chaque comments.likes sans cast. Exiger type(value) is int et value==0 : zéro flottant, booléen Python, texte, NULL, négatif ou positif ne passent pas ce test tel qu’écrit.
4. Créer comment_likes : id Integer PK, comment_id et user_id obligatoires avec les types parents copiés, created_at DateTime obligatoire ; deux FK CASCADE nommées fk_comment_likes_comment et fk_comment_likes_user ; unique_user_comment_like sur user_id/comment_id ; mysql_engine="InnoDB".
5. Créer ix_comment_likes_comment_id non unique. Ne faire aucun UPDATE du compteur physique et ne transférer aucun Vote.

### Downgrade, étape par étape

1. Refléter comment_likes et lire au plus un id.
2. Si une ligne existe, lever RuntimeError afin de refuser la perte de likes individuels ; sinon supprimer l’index puis la table.

### Conséquences sur les données

La table nouvelle démarre vide. Aucun ancien like n’est affecté à un utilisateur arbitraire, aucun compteur n’est remis à zéro par ce script. Une donnée historique non attribuable exige une décision humaine de reprise hors de ce lot. Le garde de downgrade évite la suppression silencieuse d’une table remplie, mais n’est pas une sauvegarde et ne protège pas contre un écrivain concurrent sans maintenance exclusive.

### SQLite et MySQL : portée exacte

Les contrôles MySQL ciblent le moteur des deux parents et l’activation des contraintes. Ils ne certifient pas la version du serveur, les privilèges, la collation globale ou la disponibilité Aiven. SQLite peut contenir une valeur de type inattendu malgré l’affinité Integer ; c’est la raison du test de type strict lu sans cast. La liste concrète des types renvoyés est déballée dans comment_type, user_type ; ce n’est pas un tuple construit par le code.

### Erreurs, limites et précautions

Cette migration n’est pas idempotente quand la table existe déjà. Le refus d’un ancien compteur non nul est volontaire et ne doit pas être « réparé » en effaçant l’information pour obtenir un succès. Les anciens écrivains doivent être exclus pendant le contrôle et le DDL ; les gardes Python ne sont pas une isolation système.

Les erreurs de réflexion, de contrainte, de droit, de connexion et de DDL peuvent aussi remonter via SQLAlchemy/Alembic. Une liste de raise explicites ne serait pas une liste exhaustive des exceptions possibles. Aucune exception n’a été provoquée contre une base réelle pour ce document.

### Exemple mental à raconter

Un ancien compteur de cinq ne permet pas de nommer les cinq comptes. Le script refuse plutôt que de créer cinq associations inventées ; une table déjà remplie empêche aussi son downgrade.

## env.py : orchestration, pas une huitième révision

get_engine retrouve le moteur configuré dans Flask-Migrate ; get_engine_url prépare son URL et échappe les pourcentages pour la configuration. Cette URL peut contenir des identifiants : ne pas l’afficher. get_metadata expose les tables attendues pour l’autogénération ; ces métadonnées ne démontrent pas la conformité de la base en service.

Le mode offline configure Alembic pour produire du SQL sans appliquer les révisions. Mais inspect_legacy des deux dernières révisions interroge les données : la chaîne complète ne doit pas être annoncée comme entièrement générable hors ligne par ces scripts sans adaptation. Produire ou compiler quelques instructions SQL ne valide pas le trajet complet.

Le mode online ouvre la connexion de migration et choisit une branche SQLite encadrée, ou la branche des autres dialectes. Son callback process_revision_directives retire une directive vide seulement dans le chemin autogenerate prévu. Il ne vérifie ni les données historiques ni les droits d’accès.

Les six fonctions d’env.py sont décrites sous MAH-F0013 à MAH-F0018 dans le [répertoire](04_REPERTOIRE_FONCTIONS_METHODES.md). Le fichier contient aussi un appel final qui choisit online/offline : **ne pas l’importer pour une analyse statique**.

## sqlite_migration_scope : lecture détaillée de l’enveloppe actuelle

Cette fonction, MAH-F0213 proposé, reçoit une connexion déjà choisie par l’appelant. Elle ne choisit pas de chemin SQLite et n’ouvre pas de base. L’appelant doit avoir préparé une maintenance exclusive réelle, sur une destination autorisée.

1. Vérifier dialect.name == sqlite ; sinon ValueError. Refuser une connexion dont in_transaction est vrai.
2. Retrouver la connexion DBAPI sous-jacente. Activer les FK et exiger un foreign_key_check initial sans ligne d’anomalie.
3. Suspendre les FK hors transaction et vérifier que la suspension a effectivement pris effet.
4. Entrer dans connection.begin ; émettre un BEGIN SQL explicite pour le comportement historique du pilote sqlite3 concernant le DDL.
5. Poser connection.info['sqlite_migration_integrity_scope']=True, puis rendre temporairement le contrôle au corps du with.
6. Au retour normal du corps, vérifier foreign_key_check avant la validation du contexte transactionnel. Une anomalie provoque RuntimeError et rollback de ce contexte.
7. Dans finally, enlever le marqueur et réactiver les FK ; si la réactivation n’est pas constatée, lever RuntimeError.

Le générateur est décoré contextmanager : l’appel produit un gestionnaire de contexte, qui fournit None au corps du with. Les vérifications initiales ont lieu à l’entrée du contexte. Une erreur avant le try n’a pas le même chemin de nettoyage qu’une erreur survenue après yield. La fiabilité du nettoyage dépend aussi d’une connexion encore utilisable ; une erreur de réactivation peut masquer l’exception initiale.

Le marqueur Python n’est ni secret ni un verrou système. L’enveloppe réduit les risques de reconstruction d’un parent en SQLite ; elle ne confine pas un programme arbitraire, ne garantit pas l’absence d’écrivains concurrents et ne remplace pas une sauvegarde autorisée et vérifiée avant une vraie maintenance. Son parcours n’est pas exécuté dans ce lot.

## Pourquoi le batch est nécessaire

Pour certaines modifications SQLite, Alembic reflète la table, crée une table de remplacement, copie les données, retire l’ancienne et renomme la nouvelle. Ce mécanisme explique le risque particulier d’une table parent avec des FK entrantes. Sur d’autres moteurs, le batch emploie généralement les ALTER ordinaires. Il faut donc raisonner sur le SQL du dialecte, pas seulement sur la forme du with Python. [Documentation officielle Alembic sur le batch](https://alembic.sqlalchemy.org/en/latest/batch.html).

Les noms des contraintes comptent : drop_constraint attend un objet existant. Les migrations de données inspectent parfois les lignes et ne peuvent pas être évaluées à partir des seules métadonnées. Les schémas créés par create_all et ceux obtenus par replay ne doivent pas être déclarés interchangeables sans comparaison appropriée.

## Ce qui a réellement été validé pour cette rédaction

| Travail | Statut dans ce lot | Portée |
|---|---|---|
| Lecture des sept fichiers complets | Effectuée | Analyse du code livré |
| Parsing AST et résolution revision/down_revision | Exécutés | Syntaxe et chaîne statique |
| Vérification des 14 entrées upgrade/downgrade et 2 inspect_legacy | Exécutée statiquement | Correspondance des symboles et identifiants |
| Rejeu de migrations SQLite | Non exécuté | Les résultats d’anciens lots restent historiques |
| Compilation SQL MySQL de la chaîne | Non exécutée | Aucun résultat nouveau annoncé |
| Migration sur MySQL/Aiven | Non exécutée | Compatibilité d’exécution non démontrée |
| Accès SQLite persistante ou au serveur 5066 | Aucun | Hors périmètre |

Les validations SQLite antérieures établissaient seulement les comportements couverts dans leur environnement. Elles ne deviennent pas des tests MySQL par lecture du présent guide. Une éventuelle campagne MySQL exigerait une base jetable autorisée, les mêmes versions et paramètres utiles, des fixtures synthétiques, les refus attendus et un contrôle après échec ; aucune commande de déploiement n’est prescrite ici.

## Préparer l’explication devant le jury

Pour chaque révision, expliquer dans l’ordre : état parent, problème résolu, opérations du schéma, transformation éventuelle des lignes, garde avant DDL, limite du retour arrière et preuve disponible. Une réponse précise peut être : « Ce chemin est présent dans le code et a été étudié ; je ne prétends pas l’avoir appliqué sur Aiven. »

Le lot 6H.21.6 pourra ajouter les copies de code à expliquer, dans le chemin proposé `docs/soutenance/code-commente-mahamadou/migrations/versions/`, avec les mêmes noms de fichiers et identifiants. Ces chemins sont prospectifs, sans lien cassé et sans fichier créé par ce lot.
