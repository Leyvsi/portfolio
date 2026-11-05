# Relations, contraintes et transactions SQL expliquées

Les Petits Enquêteurs — lot 6H.21.4 — 4 novembre 2026, Europe/Paris.

**Proposition externe à lire et à approuver avant installation.** Sources : copie intégrée locale, photographiée par SHA-256 ; pas la seule version du commit Git. Analyse statique : aucun import de l’application, accès SQL, test applicatif ni migration exécutée pour cette rédaction. Les exemples sont pédagogiques et non exécutés. Leur éventuelle exécution exige un contexte temporaire distinct, préparé et autorisé ; ils ne constituent pas des scripts de démarrage du projet.

[Sommaire de soutenance](README.md) · [Correspondance avec les sources](06_CORRESPONDANCE_SOURCES.md) · [Validation documentaire](07_VALIDATION_DOCUMENTAIRE.md)

## Quatre niveaux qui coopèrent

| Niveau | Exemple réel | Ce qu’il garantit | Ce qu’il ne garantit pas |
|---|---|---|---|
| Métier/API | Filtrer un dossier actif, contrôler le compte | La politique appliquée par le chemin de requête examiné | L’existence d’une contrainte SQL équivalente pour tout écrivain |
| Objet Python | Report.target_id, User.set_password | Le calcul ou la validation lorsqu’on appelle précisément ce code | Une protection contre un accès SQL direct ou un autre chemin d’affectation |
| ORM | relationship, cascade, Session | Navigation et propagation des opérations ORM configurées | Un déclenchement identique pour DELETE SQL direct ou suppression en masse |
| Base | PK, FK, UNIQUE, NOT NULL | Les contraintes réellement installées et activées dans ce moteur | L’autorisation HTTP, la catégorie métier, l’anonymisation du texte |

Dans l’application, une règle ne doit être annoncée comme garantie SQL que si une contrainte correspondante existe. Une contrainte déclarée dans le fichier models.py ne démontre pas à elle seule qu’elle a été installée sur une base déployée. Cette session ne consulte aucune base pour le déterminer.

## Les dix clés primaires

Chaque table possède une colonne entière `id` comme clé primaire : users, categories, stories, theories, comments, votes, comment_likes, proposals, reports, cold_case_updates. Une PK identifie une ligne, ne peut pas être NULL et ne peut pas être dupliquée dans sa table. Le même entier peut apparaître dans deux tables distinctes : users.id=7 et stories.id=7 ne désignent pas la même entité.

Les enfants stockent la valeur de la clé du parent. Ils ne stockent pas l’objet Python parent. Un changement du titre d’un dossier ne change pas sa PK ; ses commentaires restent rattachés. Aucune règle ON UPDATE CASCADE n’est spécifiée ici. Les PK ne doivent pas être renumérotées pour obtenir une liste continue ; un trou dans la numérotation n’est pas une corruption.

## Les treize clés étrangères, une par une

**Comptage : neuf CASCADE, deux SET NULL, deux sans ON DELETE explicite.** Les 26 relationship représentent les deux navigations de ces 13 associations, pas 26 contraintes.

| Repère | Enfant → parent | NULL enfant | Enfant vers parent / parent vers enfants | ON DELETE | Nom explicite dans le modèle |
|---|---|---|---|---|---|
| REL-01 | `stories.category_id` → `categories.id` | Non | 1 / 0..n | Non explicité | `Non nommé ici` |
| REL-02 | `stories.author_id` → `users.id` | Non | 1 / 0..n | Non explicité | `Non nommé ici` |
| REL-03 | `theories.story_id` → `stories.id` | Non | 1 / 0..n | CASCADE | `fk_theories_story` |
| REL-04 | `theories.user_id` → `users.id` | Oui | 0..1 / 0..n | SET NULL | `fk_theories_user` |
| REL-05 | `comments.story_id` → `stories.id` | Non | 1 / 0..n | CASCADE | `fk_comments_story` |
| REL-06 | `comments.user_id` → `users.id` | Oui | 0..1 / 0..n | SET NULL | `fk_comments_user` |
| REL-07 | `votes.story_id` → `stories.id` | Non | 1 / 0..n | CASCADE | `fk_votes_story` |
| REL-08 | `votes.user_id` → `users.id` | Non | 1 / 0..n | CASCADE | `fk_votes_user` |
| REL-09 | `comment_likes.comment_id` → `comments.id` | Non | 1 / 0..n | CASCADE | `fk_comment_likes_comment` |
| REL-10 | `comment_likes.user_id` → `users.id` | Non | 1 / 0..n | CASCADE | `fk_comment_likes_user` |
| REL-11 | `proposals.user_id` → `users.id` | Non | 1 / 0..n | CASCADE | `fk_proposals_user` |
| REL-12 | `reports.comment_id` → `comments.id` | Non | 1 / 0..n | CASCADE | `fk_reports_comment` |
| REL-13 | `cold_case_updates.story_id` → `stories.id` | Non | 1 / 0..n | CASCADE | `fk_cold_case_updates_story` |

### REL-01 — stories.category_id

La catégorie classe le dossier. Une catégorie peut rester vide ; un dossier persisté ne peut pas se retrouver sans catégorie. Le schéma ne prévoit pas de suppression automatique du dossier avec sa catégorie.

La déclaration se trouve dans `backend/models.py:128`. Une valeur absente est refusée par NOT NULL ; une valeur non nulle sans parent doit être refusée lorsque la FK est active. La cardinalité 0..n du parent n’impose pas un nombre minimal d’enfants.

### REL-02 — stories.author_id

L’auteur doit exister, mais il n’est pas nécessairement administrateur par la seule FK. Supprimer un compte auteur encore référencé peut être refusé. Il faut préserver ou réaffecter cette dépendance dans une procédure métier distincte.

La déclaration se trouve dans `backend/models.py:134`. Une valeur absente est refusée par NOT NULL ; une valeur non nulle sans parent doit être refusée lorsque la FK est active. La cardinalité 0..n du parent n’impose pas un nombre minimal d’enfants.

### REL-03 — theories.story_id

Une théorie n’a pas de sens persistant sans son dossier. Supprimer le dossier emporte la théorie ; supprimer la théorie ne supprime jamais le dossier.

La déclaration se trouve dans `backend/models.py:225`. Une valeur absente est refusée par NOT NULL ; une valeur non nulle sans parent doit être refusée lorsque la FK est active. La cardinalité 0..n du parent n’impose pas un nombre minimal d’enfants.

### REL-04 — theories.user_id

Le compte peut disparaître et la théorie rester avec user_id NULL. Le titre, le contenu et le compteur ne sont pas anonymisés ni effacés par cette règle.

La déclaration se trouve dans `backend/models.py:235`. Une valeur absente est permise par cette colonne ; une valeur non nulle sans parent doit être refusée lorsque la FK est active. La cardinalité 0..n du parent n’impose pas un nombre minimal d’enfants.

### REL-05 — comments.story_id

Le commentaire dépend du dossier. Sa suppression par cascade peut à son tour entraîner celles des signalements et likes qui le ciblent.

La déclaration se trouve dans `backend/models.py:291`. Une valeur absente est refusée par NOT NULL ; une valeur non nulle sans parent doit être refusée lorsque la FK est active. La cardinalité 0..n du parent n’impose pas un nombre minimal d’enfants.

### REL-06 — comments.user_id

Le commentaire est conservé si sa référence de compte est retirée par SET NULL. Le pseudo copié et le texte ne sont pas changés : SET NULL ne signifie pas effacement personnel complet.

La déclaration se trouve dans `backend/models.py:301`. Une valeur absente est permise par cette colonne ; une valeur non nulle sans parent doit être refusée lorsque la FK est active. La cardinalité 0..n du parent n’impose pas un nombre minimal d’enfants.

### REL-07 — votes.story_id

Les likes de dossier n’existent que tant que leur dossier existe. Le total est un agrégat de ces lignes, pas une colonne de Story.

La déclaration se trouve dans `backend/models.py:386`. Une valeur absente est refusée par NOT NULL ; une valeur non nulle sans parent doit être refusée lorsque la FK est active. La cardinalité 0..n du parent n’impose pas un nombre minimal d’enfants.

### REL-08 — votes.user_id

Un like individuel ne survit pas à une suppression SQL acceptable de son compte. Cela ne fournit pas une procédure complète de suppression de User, dont les autres dépendances peuvent bloquer.

La déclaration se trouve dans `backend/models.py:396`. Une valeur absente est refusée par NOT NULL ; une valeur non nulle sans parent doit être refusée lorsque la FK est active. La cardinalité 0..n du parent n’impose pas un nombre minimal d’enfants.

### REL-09 — comment_likes.comment_id

Le like d’un commentaire disparaît avec ce commentaire. L’index de cible facilite son comptage ; il est indépendant de l’unicité du couple.

La déclaration se trouve dans `backend/models.py:438`. Une valeur absente est refusée par NOT NULL ; une valeur non nulle sans parent doit être refusée lorsque la FK est active. La cardinalité 0..n du parent n’impose pas un nombre minimal d’enfants.

### REL-10 — comment_likes.user_id

Le compte ne peut avoir qu’une association pour une même cible. La suppression de cette association ne change pas le compteur historique Comment.likes.

La déclaration se trouve dans `backend/models.py:442`. Une valeur absente est refusée par NOT NULL ; une valeur non nulle sans parent doit être refusée lorsque la FK est active. La cardinalité 0..n du parent n’impose pas un nombre minimal d’enfants.

### REL-11 — proposals.user_id

La proposition est une dépendance du compte. Cette cascade SQL ne crée aucune histoire et ne valide aucun changement de statut.

La déclaration se trouve dans `backend/models.py:465`. Une valeur absente est refusée par NOT NULL ; une valeur non nulle sans parent doit être refusée lorsque la FK est active. La cardinalité 0..n du parent n’impose pas un nombre minimal d’enfants.

### REL-12 — reports.comment_id

Le signalement référence une ligne réelle, à la différence de l’ancien couple textuel type/target_id. La FK ne mémorise pas la personne qui signale.

La déclaration se trouve dans `backend/models.py:522`. Une valeur absente est refusée par NOT NULL ; une valeur non nulle sans parent doit être refusée lorsque la FK est active. La cardinalité 0..n du parent n’impose pas un nombre minimal d’enfants.

### REL-13 — cold_case_updates.story_id

La mise à jour disparaît avec le dossier. La FK ne vérifie ni la catégorie cold case ni le rôle du demandeur.

La déclaration se trouve dans `backend/models.py:596`. Une valeur absente est refusée par NOT NULL ; une valeur non nulle sans parent doit être refusée lorsque la FK est active. La cardinalité 0..n du parent n’impose pas un nombre minimal d’enfants.

## Les sept règles UNIQUE en plus des PK

| Cible | Portée | Exemple conceptuel de doublon refusé | Nuance |
|---|---|---|---|
| users.username | Une colonne | Deux comptes avec le même pseudo selon la collation | Pas une clé étrangère ; normalisation non déclarée |
| users.email | Une colonne | Deux comptes avec la même adresse selon la collation | Distinct de l’unicité du pseudo |
| categories.name | Une colonne | Deux catégories avec le même libellé selon la collation | Description non unique |
| stories.slug | Une colonne | Deux dossiers de même slug | Titre non unique |
| stories.management_revision | Une colonne | Deux dossiers avec la même révision, y compris la sentinelle | Modèle unique=True ; migration : index unique nommé uq_stories_management_revision |
| votes(user_id, story_id) | Couple | Même compte et même dossier deux fois | unique_user_story_vote |
| comment_likes(user_id, comment_id) | Couple | Même compte et même commentaire deux fois | unique_user_comment_like |

Les noms automatiques des unicités simples dépendent du schéma et du dialecte ; ne pas inventer un nom de contrainte en lisant unique=True. L’index unique nommé de la migration de révision n’est pas nommé dans la colonne du modèle. La sémantique d’unicité peut correspondre alors que le nom ou la forme de l’objet de schéma diffère ; ce guide ne certifie pas une absence de différence autogenerate sur un serveur non consulté.

Exemple fictif de couples : `(compte A, dossier X)` et `(compte A, dossier Y)` sont autorisés ; `(compte B, dossier X)` aussi ; une seconde occurrence exacte de `(compte A, dossier X)` est refusée. L’index simple ix_reports_comment_id ne rend pas un commentaire signalable une seule fois : il sert au filtrage et au comptage.

## CASCADE SQL et cascade ORM : lire le chemin de suppression

### Propagation configurée dans les objets

| Collection ORM | Cascade déclarée | passive_deletes | Conséquence à expliquer |
|---|---|---|---|
| Story.comments, votes, theories, cold_case_updates | all, delete-orphan | Non précisé, donc comportement par défaut | Suppression du parent propagée aux enfants ORM ; retirer un enfant de la collection peut le supprimer au flush |
| Comment.moderation_reports, comment_likes | all, delete-orphan | True | Des enfants non chargés peuvent être laissés à la cascade SQL ; des enfants chargés restent concernés par la gestion ORM |
| User.comment_likes | all, delete-orphan | True | Même principe, à partir du compte |
| User.stories, comments, votes, proposals, theories | Non précisée | Non précisé | Pas de cascade ORM delete déclarée ; l’ORM peut tenter une dissociation par FK NULL |
| Category.stories | Non précisée | Non précisé | Une dissociation heurte la FK obligatoire de Story |

La cascade par défaut des relationships n’est pas une cascade de suppression. `passive_deletes=True` ne désactive pas les contraintes et ne signifie pas qu’aucun DELETE ORM n’arrivera pour les objets chargés. Les suppressions en masse et SQL direct ne parcourent pas les mêmes cascades par objets. [Référence SQLAlchemy sur les cascades](https://docs.sqlalchemy.org/en/20/orm/cascades.html).

### Deux scénarios différents

**Purge d’un dossier acceptée par l’API.** Les collections de Story propagent la suppression ORM. La base impose les cascades des quatre types d’enfants ; les commentaires possèdent eux-mêmes des likes et signalements dépendants. Les comptes, catégories et fichiers PNG ne sont pas supprimés par ces FK. La purge applicative inclut des contrôles préalables qui dépassent ces mécanismes.

**Suppression d’un compte.** Les dossiers de cet auteur ont une FK obligatoire sans ON DELETE explicite. Cette dépendance peut bloquer le DELETE SQL du compte. En ORM, les collections dépourvues de cascade delete peuvent conduire à des affectations NULL incompatibles avec certaines FK obligatoires. Il serait faux d’annoncer « supprimer User efface proprement toutes ses traces » à partir du seul tableau CASCADE. Les valeurs SET NULL conservent de plus des textes et pseudos.

### Archive et retrait d’une collection

Archiver affecte une date au dossier et renouvelle sa révision selon le code de gestion. Ce n’est pas `Session.delete(story)`. Les contributions restent en base ; les requêtes publiques doivent les cacher en vérifiant l’état du parent.

Retirer un enfant d’une collection configurée delete-orphan peut programmer sa suppression. Pour déplacer une contribution entre dossiers, il faudrait une opération métier explicite et cohérente ; manipuler une liste sans comprendre son mapping peut perdre une ligne au flush.

## Intégrité réellement active selon le moteur

SQLite exige l’activation des FK pour chaque connexion pertinente. Lire seulement une déclaration ForeignKey ne prouve pas l’activation. La suspension utilisée pour reconstruire certaines tables pendant une migration est entourée de contrôles et d’une transaction dans sqlite_migration_scope ; elle ne doit pas être reprise comme configuration d’exploitation. Le PRAGMA ne se commute pas comme prévu au milieu d’une transaction déjà ouverte. [Documentation SQLite des clés étrangères](https://www.sqlite.org/foreignkeys.html).

Pour MySQL, le script des likes exige foreign_key_checks actif et les parents comments/users en InnoDB. Il copie le type des clés parentes pour éviter une incompatibilité de référence. Ces contrôles sont lus statiquement ; aucune interrogation MySQL/Aiven n’a été réalisée dans ce lot. Les droits, versions, collations, moteurs effectifs et données de la cible restent à vérifier dans une campagne séparée.

Une FK ne garantit ni que l’histoire est active, ni que le compte est autorisé, ni que le contenu est acceptable. Un index accélère un chemin d’accès ; il ne remplace pas ces politiques. Une contrainte UNIQUE ne résout pas à elle seule le message HTTP ou l’expérience en cas de réseau interrompu.

## Le cycle d’une Session et les trois opérations décisives

| Étape | Objet et SQL | Durabilité | Erreur typique à éviter |
|---|---|---|---|
| Construction | Objet transitoire, attributs renseignés | Rien de nouveau en base | Croire que tous les défauts et id sont déjà disponibles |
| add(objet) | Objet en attente de persistance dans la Session | Pas encore de commit | Annoncer qu’un add constitue l’enregistrement durable |
| flush() | Envoie les INSERT/UPDATE/DELETE nécessaires ; obtient les PK générées | Transaction ouverte, modifications encore annulables si moteur transactionnel | Appeler flush un commit ou ignorer une contrainte levée ici |
| Requête avec autoflush | Peut envoyer des changements avant un SELECT | Pas un commit | Croire qu’un SELECT est toujours sans effet sur les changements en attente |
| commit() | Déclenche le flush requis puis valide la transaction | Validation SQL réussie, sans promesse sur la réception du réseau | Affirmer qu’un message HTTP perdu signifie absence d’enregistrement |
| rollback() | Annule la transaction active selon le moteur et remet la Session en état utilisable | N’annule pas un commit déjà réussi | Oublier rollback après échec de flush |

Le code de like de commentaire dans `backend/api/v1/views/likes.py`, fonction handle_like, illustre ce cycle : ajout, flush, construction du résultat, commit ; sur IntegrityError ou SQLAlchemyError, rollback. La distinction de conflit unique utilise un contrôleur de contrainte, pas seulement le nom général de l’exception.

Le commit expire normalement les objets de session selon la configuration ; une lecture ultérieure peut nécessiter un SELECT. Les sérialiseurs du modèle n’ouvrent pas de transaction d’écriture explicite, mais lire un objet expiré peut rafraîchir ses attributs. Un objet détaché dont les attributs ne sont pas disponibles peut lever DetachedInstanceError. [Cycle de Session documenté par SQLAlchemy](https://docs.sqlalchemy.org/en/20/orm/session_basics.html).

### Exemple Python : une association et son décompte dans la même transaction

**Exemple à lire, non exécuté.** `compte` et `commentaire` représentent des objets fictifs persistés dans une fixture jetable autorisée, avec contraintes actives ; aucune connexion n’est construite ci-dessous. La route réelle ajoute en plus authentification, visibilité, compatibilité du compteur historique et traduction des erreurs HTTP.

```python
from sqlalchemy.exc import IntegrityError

def illustrer_like(db, CommentLike, compte, commentaire):
    try:
        association = CommentLike(user_id=compte.id, comment_id=commentaire.id)
        db.session.add(association)
        db.session.flush()  # Le SQL est envoyé, sans valider définitivement.
        total = CommentLike.query.filter_by(comment_id=commentaire.id).count()
        resultat = {"comment_id": commentaire.id, "likes": total}
        db.session.commit()
        return resultat
    except IntegrityError:
        db.session.rollback()
        raise  # L'appelant doit identifier la contrainte, pas supposer un doublon.
    except Exception:
        db.session.rollback()
        raise
```

Le COUNT voit l’association ajoutée dans la transaction après flush. Il ne prédit pas toutes les modifications concurrentes et ne constitue pas un verrou global. L’unicité du couple résout le conflit d’insertion ; l’API décide comment le présenter. Les données d’une Session ne doivent pas être partagées librement entre requêtes ou threads.

### Exemple Python : construire un graphe sans deviner les PK

On veut expliquer pourquoi flush est utile avant d’utiliser un identifiant. Les données ci-dessous sont entièrement inventées ; la fonction ne crée ni moteur ni fichier de base. Le mot de passe reste un paramètre local, jamais imprimé. Elle n’est pas une routine d’initialisation du service.

```python
def illustrer_graphe(db, User, Category, Story, mot_de_passe_fictif):
    try:
        auteur = User(username="lecteur-exemple", email="lecteur@example.test")
        auteur.set_password(mot_de_passe_fictif)
        categorie = Category(name="Catégorie pédagogique")
        dossier = Story(slug="enigme-pedagogique", title="Dossier fictif",
                        summary="Résumé inventé", content="Récit inventé",
                        author=auteur, category=categorie)
        db.session.add_all([auteur, categorie, dossier])
        db.session.flush()
        identifiant = dossier.id
        revision = dossier.management_revision
        db.session.commit()
        return identifiant, revision
    except Exception:
        db.session.rollback()
        raise
```

On assigne des relations à des objets existants dans le graphe, plutôt que d’inventer des entiers de PK. Le flush ordonne les opérations selon les dépendances. L’exemple n’est pas idempotent : le rejouer dans la même fixture peut heurter les unicités de pseudo, e-mail, catégorie et slug. Un rollback après erreur n’efface pas les données d’une exécution précédente déjà commitée.

### Exemples SQL fidèles aux tables actuelles

Les paramètres nommés représentent des valeurs fictives liées par le pilote. Le SQL reste illustratif : syntaxe de paramètres à adapter au driver, aucun identifiant réel de compte, aucune exécution. Les dates nécessaires aux INSERT sont explicites parce que les defaults Python du modèle ne sont pas des defaults SQL permanents.

```sql
-- Liste des dossiers actifs et de leur catégorie.
SELECT s.id, s.slug, s.title, c.name AS category_name
FROM stories AS s
JOIN categories AS c ON c.id = s.category_id
WHERE s.archived_at IS NULL
ORDER BY s.created_at DESC;

-- Comptage courant des likes individuels d'un commentaire.
SELECT COUNT(*) AS likes
FROM comment_likes
WHERE comment_id = :comment_id;

-- Nouveau signalement : type et target_id ne sont pas des colonnes SQL actuelles.
INSERT INTO reports (comment_id, reason, status, created_at)
VALUES (:comment_id, :reason, 'pending', :created_at);

-- Retrait personnel : conserver les likes des autres comptes.
DELETE FROM comment_likes
WHERE comment_id = :comment_id AND user_id = :authenticated_user_id;
```

Le JOIN de catégorie ne charge pas les contributions et ne démontre aucune autorisation administrative. Le DELETE personnel n’autorise pas à faire confiance à un user_id envoyé par le client : l’API doit obtenir celui du compte authentifié. L’INSERT dans reports doit avoir une cible réelle ; la FK seule ne contrôle pas si le dossier est archivé.

### Lire SET NULL et CASCADE en SQL sans lancer une suppression

Si un DELETE SQL de User est accepté après résolution de toutes les dépendances bloquantes, les FK SET NULL conservent ses commentaires et théories avec une référence absente, et les FK CASCADE concernent votes, comment_likes et proposals. La présence de stories.author_id peut empêcher l’opération entière. Cette condition est essentielle : il n’existe pas ici de démonstration destructive exécutée.

Un DELETE SQL de Story déclenche les cascades vers ses enfants lorsque la base les applique. Le chemin ORM peut charger et supprimer lui-même des objets. Dans les deux cas, supprimer le dossier ne supprime pas ses parents User et Category : les références ont une direction.

## Erreurs, concurrence et portée de la transaction

| Situation | Couche susceptible d’échouer | Réponse à expliquer |
|---|---|---|
| FK vers une cible absente | flush ou commit selon contraintes | IntegrityError ; rollback, puis traiter l’absence de cible |
| Couple de like déjà présent | Contrainte UNIQUE, souvent au flush | Identifier précisément le conflit ; ne pas masquer une autre erreur |
| Colonne obligatoire absente | NOT NULL lors de l’INSERT | Corriger la construction ; default Python ne couvre pas toute entrée invalide |
| target_id non canonique | Setter Python de Report | ValueError avant DML si ce setter est bien utilisé |
| Accès sans contexte Flask | Session/extension configurée par Flask | RuntimeError possible ; ne pas créer un faux contexte sur la base persistante |
| Connexion indisponible | Pilote/moteur SQL | SQLAlchemyError et sous-classes ; message public neutre, journal sans secrets |
| Objet expiré détaché | Instrumentation ORM | DetachedInstanceError possible à la lecture |

Une transaction SQL ne couvre pas l’envoi d’un courriel, un fichier écrit hors base ou l’arrivée d’une réponse HTTP. Le commit n’efface pas les sauvegardes antérieures. Le rollback ne reconstitue pas un historique de données supprimées puis commitées.

Pour MySQL, les instructions DDL telles que des ALTER TABLE et CREATE TABLE peuvent entraîner des commits implicites. Une migration comportant plusieurs DDL ne devient pas entièrement annulable parce qu’elle se trouve sous context.begin_transaction. Les précontrôles des données réduisent certains risques avant DDL, sans assurer une atomicité globale. [Manuel MySQL sur les commits implicites](https://dev.mysql.com/doc/refman/8.4/en/implicit-commit.html).

## Petits exercices pour préparer l’oral

1. Pourquoi un compte peut-il aimer deux dossiers malgré UNIQUE ? Parce que la contrainte porte sur le couple, qui diffère quand le dossier change.
2. SET NULL rend-il un commentaire anonyme ? Il retire sa FK de compte ; ni le pseudo copié ni le texte ne sont effacés.
3. Un add remplit-il immédiatement les dates ? Pas nécessairement : les callbacks d’insertion interviennent lors de la préparation de l’INSERT.
4. Pourquoi flush avant sérialisation ? Pour envoyer les changements et obtenir les identifiants ou valeurs générées nécessaires au résultat, tout en conservant la possibilité de rollback avant commit.
5. Une FK prouve-t-elle qu’un dossier est actif ? Elle prouve un rattachement à une ligne existante lorsque la contrainte est appliquée ; l’archive relève d’un autre attribut et des filtres API.
6. Peut-on rejouer les sept migrations sur la démonstration pour apprendre ? Ce lot ne l’autorise pas. L’étude est statique ; toute future campagne doit utiliser une destination jetable distincte et contrôlée.

Les réponses détaillées s’appuient sur les fichiers du projet, pas sur une observation de sa base privée. Le [diagramme commenté](05_DIAGRAMME_RELATIONNEL_COMMENTE.md) sert à suivre les chemins de dépendance.
