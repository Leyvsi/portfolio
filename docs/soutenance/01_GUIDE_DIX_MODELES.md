# Guide approfondi des dix modèles SQLAlchemy

Les Petits Enquêteurs — lot 6H.21.4 — 4 novembre 2026, Europe/Paris.

**Proposition externe à lire et à approuver avant installation.** Sources : copie intégrée locale, photographiée par SHA-256 ; pas la seule version du commit Git. Analyse statique : aucun import de l’application, accès SQL, test applicatif ni migration exécutée pour cette rédaction. Les exemples sont pédagogiques et non exécutés. Leur éventuelle exécution exige un contexte temporaire distinct, préparé et autorisé ; ils ne constituent pas des scripts de démarrage du projet.

[Sommaire de soutenance](README.md) · [Correspondance avec les sources](06_CORRESPONDANCE_SOURCES.md) · [Validation documentaire](07_VALIDATION_DOCUMENTAIRE.md)

## Comment lire une déclaration de modèle

`db = SQLAlchemy()` est l’extension partagée. La déclaration des classes décrit des métadonnées et des comportements Python ; elle n’ouvre pas, à elle seule, une connexion ni ne crée les tables. `db.Model` apporte l’instrumentation ORM et un constructeur usuel par attributs nommés. Les méthodes héritées ou générées ne sont pas des fonctions écrites dans ce fichier : aucun nouvel identifiant pédagogique n’est inventé pour elles.

Une instance est un objet ; une ligne est sa représentation persistée. Modifier l’objet ne signifie pas que le SQL est déjà envoyé. Les opérations explicites de session et les autoflush doivent être expliqués séparément ; voir le [guide des transactions](02_RELATIONS_CONTRAINTES_TRANSACTIONS.md).

| Type déclaré | Valeur Python attendue | Intention de stockage et précautions |
|---|---|---|
| `db.Integer` | `int` | Identifiant ou compteur ; les FK suivent le type du parent. Le modèle n’ajoute pas de CHECK de positivité à chaque entier. SQLite emploie une affinité ; MySQL applique son type entier selon le schéma réel. |
| `db.String(n)` | `str` | Chaîne de taille annoncée n, compilée selon le dialecte. SQLite ne reproduit pas une limite VARCHAR comme un serveur MySQL ; la validation de taille de l’API reste distincte. La collation gouverne les comparaisons et unicités de texte. |
| `db.Text` | `str` | Texte long sans longueur applicative dans la déclaration. Il n’est pas illimité sur tous les moteurs ; encodage et limites en octets doivent être vérifiés sur MySQL. |
| `db.Boolean` | `bool` | Booléen abstrait, représentation propre au dialecte. La déclaration ne demande pas ici un CHECK nommé spécifique ; ne pas inventer une colonne ENUM. |
| `db.DateTime` | `datetime.datetime` | Dates sans `timezone=True`. Le callback utcnow produit de l’UTC naïf ; isoformat ne rajoute pas un suffixe Z ni une conversion locale. |

`nullable=False` interdit SQL NULL ; cela n’interdit pas une chaîne vide. `primary_key=True` implique l’identité et la non-nullité. Les identifiants entiers peuvent être générés par le moteur à l’INSERT ; ils ne sont pas attribués par `len(table)+1`, ne doivent pas être supposés continus, et peuvent rester absents sur un objet non flushé.

Ces types sont des abstractions compilées par le dialecte : [hiérarchie officielle des types SQLAlchemy](https://docs.sqlalchemy.org/en/20/core/type_basics.html). Les propriétés concrètes du serveur doivent être établies séparément ; aucune table réelle n’est inspectée ici.

Un `default` Python est utilisé à la préparation d’un INSERT si la valeur pertinente manque ; un `onupdate` concerne les UPDATE émis par SQLAlchemy ; un `server_default` appartient au schéma SQL et peut intervenir pour un INSERT extérieur à l’ORM. Ce sont trois mécanismes différents. L’unique défaut SQL permanent explicite de ces modèles est la sentinelle de `management_revision`. [Règles officielles des valeurs par défaut](https://docs.sqlalchemy.org/en/20/core/defaults.html).

**Repères quantifiés : dix classes, soixante colonnes, vingt-six attributs relationship, treize FK et sept règles d’unicité hors clés primaires.** Les tables de migration Alembic, les compteurs JSON calculés et les propriétés Python ne sont pas ajoutés à ces comptes.

## Accès aux classes

[User](#mah-c001) · [Category](#mah-c002) · [Story](#mah-c003) · [Theory](#mah-c004) · [Comment](#mah-c005) · [Vote](#mah-c006) · [CommentLike](#mah-c007) · [Proposal](#mah-c008) · [Report](#mah-c009) · [ColdCaseUpdate](#mah-c010)

<a id="mah-c001"></a>

## MAH-C001 — User : Le compte et ses permissions

**Source :** `backend/models.py:18` à `63` ; table `users` ; module `MAH-M001`.

`User` représente un compte, qu’il soit membre ou administrateur. L’identité du compte est sa clé entière, pas son pseudo ni son adresse. Le même compte peut écrire plusieurs dossiers, commentaires, théories et propositions, et aimer plusieurs contenus. Les booléens expriment deux dimensions indépendantes : être administrateur ne signifie pas être non banni.

L’API doit décider qui peut créer un compte, changer les permissions et publier une contribution. La classe n’effectue ni authentification de requête, ni validation d’adresse, ni contrôle de robustesse du mot de passe. Ne pas attribuer ces contrôles au simple fait d’hériter de `db.Model`.

### Toutes les colonnes

| Colonne | Type déclaré | NULL autorisé | PK / unicité / index | Valeurs automatiques | Sens et limites propres au projet |
|---|---|---|---|---|---|
| `id` | `db.Integer` | Non | PK | Aucune valeur automatique déclarée | Identité stable du compte ; ne pas utiliser le pseudo comme clé de relation. |
| `username` | `db.String(100)` | Non | UNIQUE individuel | Aucune valeur automatique déclarée | Pseudo unique indépendamment de l’e-mail ; une chaîne vide reste possible au niveau de ce seul schéma. |
| `email` | `db.String(150)` | Non | UNIQUE individuel | Aucune valeur automatique déclarée | Adresse unique séparément ; aucune validation syntaxique ni normalisation de casse dans cette colonne. |
| `password_hash` | `db.String(255)` | Non | — | Aucune valeur automatique déclarée | Hachage salé produit par Werkzeug ; aucun mot de passe en clair prévu dans la table. |
| `is_admin` | `db.Boolean` | Non | — | `default=False` | Permission administrative ; une valeur booléenne ne réalise pas elle-même un contrôle d’accès. |
| `is_banned` | `db.Boolean` | Non | — | `default=False` | Bannissement logique ; ne supprime ni le compte ni les contributions. |
| `created_at` | `db.DateTime` | Non | — | `default=datetime.utcnow` | Date de création renseignée côté ORM ; pas de DEFAULT SQL permanent déclaré. |

Une absence de valeur automatique déclarée n’est pas un défaut implicite à zéro ou chaîne vide. Pour `id`, la génération éventuelle relève de la clé entière et du moteur. Pour les dates, le callback est passé sans parenthèses pour être invoqué à chaque insertion concernée.

### Relations et cardinalités

| Attribut Python | Navigation | FK porteuse | Configuration ORM exacte |
|---|---|---|---|
| `User.stories` → `Story` | Collection : zéro à plusieurs enfants | `stories.author_id` | `back_populates='author'` |
| `User.comments` → `Comment` | Collection : zéro à plusieurs enfants | `comments.user_id` | `back_populates='user'` |
| `User.votes` → `Vote` | Collection : zéro à plusieurs enfants | `votes.user_id` | `back_populates='user'` |
| `User.comment_likes` → `CommentLike` | Collection : zéro à plusieurs enfants | `comment_likes.user_id` | `back_populates='user' ; cascade='all, delete-orphan' ; passive_deletes=True` |
| `User.proposals` → `Proposal` | Collection : zéro à plusieurs enfants | `proposals.user_id` | `back_populates='user'` |
| `User.theories` → `Theory` | Collection : zéro à plusieurs enfants | `theories.user_id` | `back_populates='author'` |

`back_populates` nomme l’autre côté de la même association. Il n’ajoute pas une FK supplémentaire. Les relations ne sont pas configurées pour un chargement eager systématique : naviguer peut déclencher un SELECT et demande une Session utilisable. Une collection non filtrée n’est pas un filtre d’autorisation ou de visibilité.

### Méthodes, propriétés et opérations

- [MAH-F0001](04_REPERTOIRE_FONCTIONS_METHODES.md#mah-f0001) — `User.set_password` : contrat détaillé, paramètres, retour, étapes, effets et erreurs.
- [MAH-F0002](04_REPERTOIRE_FONCTIONS_METHODES.md#mah-f0002) — `User.check_password` : contrat détaillé, paramètres, retour, étapes, effets et erreurs.
- [MAH-F0003](04_REPERTOIRE_FONCTIONS_METHODES.md#mah-f0003) — `User.to_dict` : contrat détaillé, paramètres, retour, étapes, effets et erreurs.

Clés exactes de `to_dict()` : `id`, `username`, `email`, `is_admin`, `created_at`. Les dates sont converties avec isoformat si elles existent, sinon None.

Le hachage et is_banned sont exclus ; email reste inclus. Ce dictionnaire n’est donc pas un format universellement anonyme. Une lecture d’attribut expiré peut provoquer un rafraîchissement SQL ; la méthode ne contient toutefois ni INSERT, ni DELETE, ni commit explicite.

### Cas particuliers et erreurs à savoir expliquer

Deux créations portant le même pseudo échouent à la validation SQL du second INSERT ; modifier seulement l’e-mail ne contourne pas cette unicité. La sensibilité à la casse dépend du dialecte et de la collation : le modèle n’assure pas à lui seul que « Alice » et « alice » sont traités comme deux comptes ou comme un seul.

Appeler `set_password()` sur un objet déjà chargé le rend modifié dans la Session ; le hachage n’est pas durable avant un flush suivi d’un commit réussi. `check_password()` compare une saisie au hachage, sans connexion SQL explicite. Bannir un utilisateur consiste à changer un état, pas à supprimer ses lignes.

Ne pas montrer `db.session.delete(user)` comme procédure métier supportée : les relations vers les dossiers et certaines contributions n’ont pas de cascade ORM de suppression. Une tentative de mise à NULL de références obligatoires peut échouer avant même que la cascade SQL attendue intervienne.

### Exemple Python propre à cette classe

Exemple inventé et non exécuté, à lire dans le contexte d’une fixture temporaire autorisée. Les objets parents `compte`, `categorie`, `dossier` et `commentaire` désignent les objets fictifs correspondants ; aucune connexion n’est créée. Une construction seule ne persiste pas la ligne.


```python
compte = User(username="membre-pedagogique", email="membre@example.test")
compte.set_password(mot_de_passe_fictif)
# Compte encore en mémoire : la méthode ne fait pas de commit.
verification = compte.check_password(mot_de_passe_fictif)
```

### Formulation possible devant le jury

« Le compte porte une identité et des permissions. Je conserve un hachage du mot de passe, pas sa valeur en clair. Les contributions référencent l’identifiant du compte ; les règles d’autorisation sont contrôlées dans l’API. »

<a id="mah-c002"></a>

## MAH-C002 — Category : Le classement des dossiers

**Source :** `backend/models.py:68` à `77` ; table `categories` ; module `MAH-M001`.

Une catégorie regroupe zéro, un ou plusieurs dossiers. La table évite de recopier un libellé dans chaque histoire et permet de changer ce libellé sans réécrire toutes les références. Le nom est unique ; la description est facultative.

La catégorie ne contient aucun champ `story_ids` : les identifiants de catégorie se trouvent sur les lignes `stories`. Le modèle ne fixe pas une liste fermée de catégories et ne précharge aucune catégorie. Le catalogue et les procédures de peuplement apportent ces données séparément.

### Toutes les colonnes

| Colonne | Type déclaré | NULL autorisé | PK / unicité / index | Valeurs automatiques | Sens et limites propres au projet |
|---|---|---|---|---|---|
| `id` | `db.Integer` | Non | PK | Aucune valeur automatique déclarée | Clé référencée par stories.category_id. |
| `name` | `db.String(100)` | Non | UNIQUE individuel | Aucune valeur automatique déclarée | Libellé unique, par exemple une catégorie du catalogue approuvé ; la table ne fixe pas ses valeurs. |
| `description` | `db.Text` | Oui | — | Aucune valeur automatique déclarée | Texte facultatif ; NULL signifie absence de description, différent d’une chaîne vide. |

Une absence de valeur automatique déclarée n’est pas un défaut implicite à zéro ou chaîne vide. Pour `id`, la génération éventuelle relève de la clé entière et du moteur. Pour les dates, le callback est passé sans parenthèses pour être invoqué à chaque insertion concernée.

### Relations et cardinalités

| Attribut Python | Navigation | FK porteuse | Configuration ORM exacte |
|---|---|---|---|
| `Category.stories` → `Story` | Collection : zéro à plusieurs enfants | `stories.category_id` | `back_populates='category'` |

`back_populates` nomme l’autre côté de la même association. Il n’ajoute pas une FK supplémentaire. Les relations ne sont pas configurées pour un chargement eager systématique : naviguer peut déclencher un SELECT et demande une Session utilisable. Une collection non filtrée n’est pas un filtre d’autorisation ou de visibilité.

### Méthodes, propriétés et opérations

Aucune méthode personnalisée n’est définie dans cette classe. Construction, sélection, insertion, modification et suppression passent par les capacités héritées et la Session ; elles ne sont pas des méthodes métier ajoutées implicitement au modèle.

### Cas particuliers et erreurs à savoir expliquer

Créer deux catégories avec le même nom déclenche un conflit d’unicité ; une description identique est autorisée. Supprimer une catégorie encore référencée n’a pas de cascade SQL déclarée. L’ORM peut tenter de détacher les dossiers en mettant leur FK à NULL, ce qui heurte leur obligation de catégorie. Il faut une décision métier de reclassement avant une suppression éventuelle, dans une opération séparément validée.

L’accès à `category.stories` peut émettre un SELECT si la collection n’est pas chargée. Il ne copie pas toute la table des dossiers dans la ligne de catégorie et ne prouve pas que seuls les dossiers actifs sont retournés : le filtre d’archive doit être appliqué par les requêtes appropriées.

### Exemple Python propre à cette classe

Exemple inventé et non exécuté, à lire dans le contexte d’une fixture temporaire autorisée. Les objets parents `compte`, `categorie`, `dossier` et `commentaire` désignent les objets fictifs correspondants ; aucune connexion n’est créée. Une construction seule ne persiste pas la ligne.


```python
categorie = Category(name="Catégorie pédagogique", description="Classement fictif")
# Une nouvelle catégorie peut exister sans aucun dossier.
# Les futurs dossiers porteront sa FK via Story.category.
```

### Formulation possible devant le jury

« La catégorie classe plusieurs dossiers. Chaque dossier doit en avoir une, mais une catégorie peut être vide. Supprimer une catégorie utilisée n’est pas une cascade prévue par ce schéma. »

<a id="mah-c003"></a>

## MAH-C003 — Story : Le dossier d’enquête et son état de gestion

**Source :** `backend/models.py:83` à `210` ; table `stories` ; module `MAH-M001`.

`Story` porte le contenu d’un dossier : titre, résumé, récit et référence d’illustration. Il relie obligatoirement une catégorie et un auteur. Le slug sert à retrouver une histoire par une URL lisible ; la clé primaire reste l’identifiant interne de référence des contributions.

`archived_at` permet de masquer un dossier tout en conservant ses contributions. `management_revision` est un témoin de gestion utilisé contre une décision prise sur une version devenue ancienne ; ce n’est ni une révision Alembic, ni un numéro Git, ni une signature cryptographique du contenu. Les routes de gestion renouvellent explicitement cette valeur aux transitions prévues. La déclaration de colonne ne renouvelle pas l’UUID à chaque UPDATE.

Le modèle ne garantit pas qu’un chemin d’image existe sur disque, qu’un slug correspond à un des six récits du catalogue, ni que l’auteur possède le rôle administrateur. La visibilité des dossiers actifs et l’autorisation de purge appartiennent aux services API.

### Toutes les colonnes

| Colonne | Type déclaré | NULL autorisé | PK / unicité / index | Valeurs automatiques | Sens et limites propres au projet |
|---|---|---|---|---|---|
| `id` | `db.Integer` | Non | PK | Aucune valeur automatique déclarée | Cible des commentaires, théories, votes et mises à jour. |
| `archived_at` | `db.DateTime` | Oui | — | Aucune valeur automatique déclarée | NULL : dossier actif ; date : dossier archivé. Aucun DELETE des contributions. |
| `management_revision` | `db.String(32)` | Non | UNIQUE individuel | `default=lambda: uuid4().hex` ; `server_default='00000000000000000000000000000000'` | Chaîne de 32 caractères : UUID4 hexadécimal côté ORM ; sentinelle SQL composée de 32 zéros. |
| `slug` | `db.String(150)` | Non | UNIQUE individuel | Aucune valeur automatique déclarée | Adresse lisible unique ; pas d’algorithme automatique de fabrication ni de contrôle de format ici. |
| `title` | `db.String(200)` | Non | — | Aucune valeur automatique déclarée | Titre obligatoire ; n’impose pas à lui seul une longueur minimale non nulle. |
| `summary` | `db.Text` | Non | — | Aucune valeur automatique déclarée | Résumé obligatoire, séparé du récit complet. |
| `content` | `db.Text` | Non | — | Aucune valeur automatique déclarée | Récit complet obligatoire ; ne contient pas les commentaires des lecteurs. |
| `image_url` | `db.String(500)` | Oui | — | Aucune valeur automatique déclarée | Référence facultative vers une image, pas un BLOB et pas une preuve de présence du fichier. |
| `category_id` | `db.Integer` | Non | FK → categories.id | Aucune valeur automatique déclarée | Catégorie obligatoire ; suppression du parent sans règle ON DELETE explicite. |
| `author_id` | `db.Integer` | Non | FK → users.id | Aucune valeur automatique déclarée | Compte auteur obligatoire ; aucun test SQL du rôle administrateur. |
| `created_at` | `db.DateTime` | Non | — | `default=datetime.utcnow` | Horodatage de création du dossier côté ORM. |
| `updated_at` | `db.DateTime` | Non | — | `default=datetime.utcnow` ; `onupdate=datetime.utcnow` | Horodatage recalculé par SQLAlchemy lorsqu’une mise à jour concernée est émise ; pas de trigger permanent. |

Une absence de valeur automatique déclarée n’est pas un défaut implicite à zéro ou chaîne vide. Pour `id`, la génération éventuelle relève de la clé entière et du moteur. Pour les dates, le callback est passé sans parenthèses pour être invoqué à chaque insertion concernée.

### Relations et cardinalités

| Attribut Python | Navigation | FK porteuse | Configuration ORM exacte |
|---|---|---|---|
| `Story.category` → `Category` | Un parent obligatoire après persistance | `stories.category_id` | `back_populates='stories'` |
| `Story.author` → `User` | Un parent obligatoire après persistance | `stories.author_id` | `back_populates='stories'` |
| `Story.comments` → `Comment` | Collection : zéro à plusieurs enfants | `comments.story_id` | `back_populates='story' ; cascade='all, delete-orphan'` |
| `Story.votes` → `Vote` | Collection : zéro à plusieurs enfants | `votes.story_id` | `back_populates='story' ; cascade='all, delete-orphan'` |
| `Story.theories` → `Theory` | Collection : zéro à plusieurs enfants | `theories.story_id` | `back_populates='story' ; cascade='all, delete-orphan'` |
| `Story.cold_case_updates` → `ColdCaseUpdate` | Collection : zéro à plusieurs enfants | `cold_case_updates.story_id` | `back_populates='story' ; cascade='all, delete-orphan'` |

`back_populates` nomme l’autre côté de la même association. Il n’ajoute pas une FK supplémentaire. Les relations ne sont pas configurées pour un chargement eager systématique : naviguer peut déclencher un SELECT et demande une Session utilisable. Une collection non filtrée n’est pas un filtre d’autorisation ou de visibilité.

### Méthodes, propriétés et opérations

- [MAH-F0004](04_REPERTOIRE_FONCTIONS_METHODES.md#mah-f0004) — `Story.<lambda>#01` : contrat détaillé, paramètres, retour, étapes, effets et erreurs.
- [MAH-F0005](04_REPERTOIRE_FONCTIONS_METHODES.md#mah-f0005) — `Story.to_dict` : contrat détaillé, paramètres, retour, étapes, effets et erreurs.

Clés exactes de `to_dict()` : `id`, `slug`, `title`, `summary`, `content`, `image_url`, `category_id`, `author_id`, `created_at`, `updated_at`. Les dates sont converties avec isoformat si elles existent, sinon None.

archived_at et management_revision sont exclus ; aucune liste imbriquée des contributions n’est produite. Une lecture d’attribut expiré peut provoquer un rafraîchissement SQL ; la méthode ne contient toutefois ni INSERT, ni DELETE, ni commit explicite.

### Cas particuliers et erreurs à savoir expliquer

Créer un dossier exige un auteur et une catégorie existants. Assigner `author_id` ne vérifie pas son rôle : la FK vérifie une existence, l’API décide du droit d’écriture. Un slug déjà pris provoque un conflit d’unicité. Aucune suppression de fichier image n’est déclenchée par la suppression d’une ligne Story.

Un INSERT ORM omettant la révision appelle le lambda au moment de préparer l’INSERT. Un INSERT SQL brut omettant cette colonne peut recevoir la sentinelle ; un second INSERT avec la même sentinelle peut violer l’unicité. La purge applicative refuse une sentinelle tant qu’une vraie révision n’a pas été fixée. L’UUID aléatoire rend une collision très improbable, sans garantie mathématique absolue ; la contrainte unique reste le dernier contrôle.

Une archive conserve le graphe relationnel. Une purge acceptée supprime le dossier et ses enfants selon les règles déclarées, y compris indirectement les signalements et likes de ses commentaires. La classe ne réalise pas elle-même les étapes d’aperçu, d’authentification, de contrôle de révision et de confirmation prévues par les routes de gestion.

### Exemple Python propre à cette classe

Exemple inventé et non exécuté, à lire dans le contexte d’une fixture temporaire autorisée. Les objets parents `compte`, `categorie`, `dossier` et `commentaire` désignent les objets fictifs correspondants ; aucune connexion n’est créée. Une construction seule ne persiste pas la ligne.


```python
dossier = Story(slug="dossier-pedagogique", title="Enquête fictive",
                summary="Résumé inventé", content="Récit inventé",
                author=compte, category=categorie)
# author et category sont des objets, pas des numéros devinés.
# Le défaut de management_revision intervient à l'insertion ORM.
```

### Formulation possible devant le jury

« Le dossier réunit le récit et ses références. L’archive garde les contributions ; la purge les supprime selon les cascades. La révision de gestion protège une décision devenue ancienne, sans remplacer les contrôles de droit. »

<a id="mah-c004"></a>

## MAH-C004 — Theory : Une interprétation proposée pour un dossier

**Source :** `backend/models.py:215` à `275` ; table `theories` ; module `MAH-M001`.

Une théorie contient un titre et un développement, rattachés à un dossier. Son auteur peut devenir absent de la référence SQL, car `user_id` est facultatif et porte `ON DELETE SET NULL`. Le texte subsiste alors : retirer une référence de compte ne supprime pas des données personnelles éventuellement saisies dans ce texte.

Le compteur `likes` est historique. Il n’est pas une association entre un compte et une théorie et ne possède aucune contrainte « un like par utilisateur ». La table des nouveaux likes individuels de commentaires ne s’applique pas aux théories. Aucune méthode personnalisée ne transforme une théorie en dossier.

### Toutes les colonnes

| Colonne | Type déclaré | NULL autorisé | PK / unicité / index | Valeurs automatiques | Sens et limites propres au projet |
|---|---|---|---|---|---|
| `id` | `db.Integer` | Non | PK | Aucune valeur automatique déclarée | Identité d’une théorie, distincte de l’identifiant du dossier. |
| `story_id` | `db.Integer` | Non | FK → stories.id | Aucune valeur automatique déclarée | Un dossier obligatoire ; théorie supprimée par la cascade SQL du dossier. |
| `user_id` | `db.Integer` | Oui | FK → users.id | Aucune valeur automatique déclarée | Auteur facultatif ; devient NULL si le parent est supprimé avec contraintes actives. |
| `title` | `db.String(200)` | Non | — | Aucune valeur automatique déclarée | Titre propre à la théorie, pas celui du dossier. |
| `content` | `db.Text` | Non | — | Aucune valeur automatique déclarée | Argumentation conservée même si l’auteur référencé disparaît. |
| `likes` | `db.Integer` | Non | — | `default=0` | Compteur historique entier ; aucune contrainte CHECK >= 0 ni attribution à des comptes. |
| `created_at` | `db.DateTime` | Non | — | `default=datetime.utcnow` | Date de création côté ORM. |

Une absence de valeur automatique déclarée n’est pas un défaut implicite à zéro ou chaîne vide. Pour `id`, la génération éventuelle relève de la clé entière et du moteur. Pour les dates, le callback est passé sans parenthèses pour être invoqué à chaque insertion concernée.

### Relations et cardinalités

| Attribut Python | Navigation | FK porteuse | Configuration ORM exacte |
|---|---|---|---|
| `Theory.story` → `Story` | Un parent obligatoire après persistance | `theories.story_id` | `back_populates='theories'` |
| `Theory.author` → `User` | Zéro ou un parent | `theories.user_id` | `back_populates='theories'` |

`back_populates` nomme l’autre côté de la même association. Il n’ajoute pas une FK supplémentaire. Les relations ne sont pas configurées pour un chargement eager systématique : naviguer peut déclencher un SELECT et demande une Session utilisable. Une collection non filtrée n’est pas un filtre d’autorisation ou de visibilité.

### Méthodes, propriétés et opérations

Aucune méthode personnalisée n’est définie dans cette classe. Construction, sélection, insertion, modification et suppression passent par les capacités héritées et la Session ; elles ne sont pas des méthodes métier ajoutées implicitement au modèle.

### Cas particuliers et erreurs à savoir expliquer

Sans dossier valide, l’INSERT échoue si les FK sont actives. `user_id=None` est autorisé ; `story_id=None` ne l’est pas. Supprimer le dossier supprime la théorie ; supprimer le compte par un DELETE SQL acceptable conserve la théorie avec une référence d’auteur nulle.

Un compteur positif ne révèle pas quels comptes ont aimé. Le modèle ne borne pas les valeurs négatives et ne met pas un verrou métier autour des incréments : une mise à jour concurrente naïve peut perdre un incrément. Cette observation décrit une limite de représentation, pas une instruction de modifier le code pendant ce lot.

### Exemple Python propre à cette classe

Exemple inventé et non exécuté, à lire dans le contexte d’une fixture temporaire autorisée. Les objets parents `compte`, `categorie`, `dossier` et `commentaire` désignent les objets fictifs correspondants ; aucune connexion n’est créée. Une construction seule ne persiste pas la ligne.


```python
theorie = Theory(story=dossier, author=compte,
                 title="Hypothèse pédagogique", content="Argumentation inventée")
# theorie.story relie le dossier ; author correspond à la FK user_id.
# likes n'identifie aucun lecteur ayant soutenu cette théorie.
```

### Formulation possible devant le jury

« Une théorie appartient à un dossier et peut perdre sa référence d’auteur tout en conservant son texte. Son ancien compteur de likes ne dit pas quels comptes l’ont aimée. »

<a id="mah-c005"></a>

## MAH-C005 — Comment : Le commentaire et ses dépendances de modération

**Source :** `backend/models.py:281` à `371` ; table `comments` ; module `MAH-M001`.

Le commentaire appartient à un dossier et peut référencer un compte. `username` garde une copie du pseudonyme ; ce n’est pas une relation vers `users.username`. Une modification ultérieure du pseudo du compte ne réécrit pas automatiquement cette copie.

Les signalements et likes individuels sont des lignes enfants séparées. Le champ physique `likes` reste présent pour l’historique. Le sérialiseur enrichi de l’API compte `CommentLike` lorsque ce compteur est compatible (exactement l’entier zéro) ; sinon il conserve la valeur historique et expose son incompatibilité. `Comment.to_dict()` seul renvoie encore le compteur physique. Aucun champ SQL `reports` ne subsiste dans le modèle actuel.

Une contribution dite anonyme au sens de l’interface n’est pas automatiquement anonyme au sens de la protection des personnes. Le texte et le pseudo copié peuvent rester identifiants, y compris après mise à NULL de `user_id`.

### Toutes les colonnes

| Colonne | Type déclaré | NULL autorisé | PK / unicité / index | Valeurs automatiques | Sens et limites propres au projet |
|---|---|---|---|---|---|
| `id` | `db.Integer` | Non | PK | Aucune valeur automatique déclarée | Cible des lignes reports et comment_likes. |
| `story_id` | `db.Integer` | Non | FK → stories.id | Aucune valeur automatique déclarée | Dossier obligatoire ; cascade SQL de suppression du dossier. |
| `user_id` | `db.Integer` | Oui | FK → users.id | Aucune valeur automatique déclarée | Compte facultatif ; SET NULL ne réécrit ni username ni text. |
| `username` | `db.String(100)` | Oui | — | `default='Anonyme'` | Copie du pseudonyme, défaut ORM « Anonyme » ; colonne nullable malgré ce défaut. |
| `text` | `db.Text` | Non | — | Aucune valeur automatique déclarée | Texte obligatoire ; le modèle ne filtre pas à lui seul HTML ou données personnelles. |
| `likes` | `db.Integer` | Non | — | `default=0` | Compteur physique historique ; les nouveaux likes individuels sont dans comment_likes. |
| `created_at` | `db.DateTime` | Non | — | `default=datetime.utcnow` | Date de création côté ORM. |

Une absence de valeur automatique déclarée n’est pas un défaut implicite à zéro ou chaîne vide. Pour `id`, la génération éventuelle relève de la clé entière et du moteur. Pour les dates, le callback est passé sans parenthèses pour être invoqué à chaque insertion concernée.

### Relations et cardinalités

| Attribut Python | Navigation | FK porteuse | Configuration ORM exacte |
|---|---|---|---|
| `Comment.story` → `Story` | Un parent obligatoire après persistance | `comments.story_id` | `back_populates='comments'` |
| `Comment.user` → `User` | Zéro ou un parent | `comments.user_id` | `back_populates='comments'` |
| `Comment.moderation_reports` → `Report` | Collection : zéro à plusieurs enfants | `reports.comment_id` | `back_populates='comment' ; cascade='all, delete-orphan' ; passive_deletes=True` |
| `Comment.comment_likes` → `CommentLike` | Collection : zéro à plusieurs enfants | `comment_likes.comment_id` | `back_populates='comment' ; cascade='all, delete-orphan' ; passive_deletes=True` |

`back_populates` nomme l’autre côté de la même association. Il n’ajoute pas une FK supplémentaire. Les relations ne sont pas configurées pour un chargement eager systématique : naviguer peut déclencher un SELECT et demande une Session utilisable. Une collection non filtrée n’est pas un filtre d’autorisation ou de visibilité.

### Méthodes, propriétés et opérations

- [MAH-F0006](04_REPERTOIRE_FONCTIONS_METHODES.md#mah-f0006) — `Comment.to_dict` : contrat détaillé, paramètres, retour, étapes, effets et erreurs.

Clés exactes de `to_dict()` : `id`, `story_id`, `user_id`, `username`, `text`, `likes`, `created_at`. Les dates sont converties avec isoformat si elles existent, sinon None.

Aucune requête COUNT des likes individuels ni des signalements n’est effectuée par cette méthode. Une lecture d’attribut expiré peut provoquer un rafraîchissement SQL ; la méthode ne contient toutefois ni INSERT, ni DELETE, ni commit explicite.

### Cas particuliers et erreurs à savoir expliquer

Un commentaire sans compte peut être conservé, mais doit encore appartenir à un dossier. Le défaut de pseudo n’interdit pas explicitement NULL. La suppression du commentaire entraîne celle de ses signalements et likes, sans supprimer le dossier parent ou le compte.

Retirer un objet de `comment.comment_likes` ou de `comment.moderation_reports` peut conduire à un DELETE via delete-orphan au flush ; ce n’est pas une simple suppression visuelle d’une liste Python. Le mot « all » dans la cascade décrit la propagation ORM, pas des droits illimités en base.

Le sérialiseur de base ne compte pas les nouveaux likes et n’ajoute pas les totaux de signalements. Le chemin API enrichi doit être lu pour connaître les champs réellement envoyés au frontend.

### Exemple Python propre à cette classe

Exemple inventé et non exécuté, à lire dans le contexte d’une fixture temporaire autorisée. Les objets parents `compte`, `categorie`, `dossier` et `commentaire` désignent les objets fictifs correspondants ; aucune connexion n’est créée. Une construction seule ne persiste pas la ligne.


```python
commentaire = Comment(story=dossier, user=compte,
                      username=compte.username, text="Observation inventée")
# username est copié ; il n'est pas une FK vers le pseudo.
# Les signalements et likes individuels seront des objets séparés.
```

### Formulation possible devant le jury

« Le commentaire relie un texte à un dossier et éventuellement un compte. Il conserve un pseudo copié et possède des signalements et des likes comme lignes enfants. Le compteur historique et le compte des likes individuels sont distincts. »

<a id="mah-c006"></a>

## MAH-C006 — Vote : Le like individuel d’un dossier

**Source :** `backend/models.py:376` à `430` ; table `votes` ; module `MAH-M001`.

Le nom historique `Vote` désigne une association entre un compte et un dossier. Chaque ligne dit « ce compte aime ce dossier ». Il n’existe ici ni nombre d’étoiles, ni score signé, ni champ indiquant un choix de réponse.

Le total des likes est un COUNT de lignes filtrées par dossier ; l’état personnel filtre en plus le compte authentifié. La contrainte sur le couple assure l’unicité même si deux requêtes concurrentes ont toutes deux observé l’absence d’un vote. Le contrôle préalable de l’API améliore la réponse utilisateur mais ne remplace pas la contrainte SQL.

### Toutes les colonnes

| Colonne | Type déclaré | NULL autorisé | PK / unicité / index | Valeurs automatiques | Sens et limites propres au projet |
|---|---|---|---|---|---|
| `id` | `db.Integer` | Non | PK | Aucune valeur automatique déclarée | Identité de l’association, en complément de l’unicité du couple métier. |
| `story_id` | `db.Integer` | Non | FK → stories.id | Aucune valeur automatique déclarée | Dossier aimé, obligatoire ; cascade SQL depuis stories. |
| `user_id` | `db.Integer` | Non | FK → users.id | Aucune valeur automatique déclarée | Compte aimant, obligatoire ; cascade SQL depuis users. |
| `created_at` | `db.DateTime` | Non | — | `default=datetime.utcnow` | Date du like ; aucun compteur agrégé stocké. |

Une absence de valeur automatique déclarée n’est pas un défaut implicite à zéro ou chaîne vide. Pour `id`, la génération éventuelle relève de la clé entière et du moteur. Pour les dates, le callback est passé sans parenthèses pour être invoqué à chaque insertion concernée.

### Relations et cardinalités

| Attribut Python | Navigation | FK porteuse | Configuration ORM exacte |
|---|---|---|---|
| `Vote.story` → `Story` | Un parent obligatoire après persistance | `votes.story_id` | `back_populates='votes'` |
| `Vote.user` → `User` | Un parent obligatoire après persistance | `votes.user_id` | `back_populates='votes'` |

`back_populates` nomme l’autre côté de la même association. Il n’ajoute pas une FK supplémentaire. Les relations ne sont pas configurées pour un chargement eager systématique : naviguer peut déclencher un SELECT et demande une Session utilisable. Une collection non filtrée n’est pas un filtre d’autorisation ou de visibilité.

### Contraintes complémentaires

Déclaration de table : `(db.UniqueConstraint('user_id', 'story_id', name='unique_user_story_vote'),)`.

L’unicité porte sur le couple `(user_id, story_id)`, pas sur chacune de ses composantes. `id` reste une clé primaire distincte.

### Méthodes, propriétés et opérations

Aucune méthode personnalisée n’est définie dans cette classe. Construction, sélection, insertion, modification et suppression passent par les capacités héritées et la Session ; elles ne sont pas des méthodes métier ajoutées implicitement au modèle.

### Cas particuliers et erreurs à savoir expliquer

Deux comptes peuvent aimer le même dossier et un compte peut aimer deux dossiers. Le seul doublon interdit est la répétition du même couple. Les deux FK non nulles empêchent les associations sans cible ou compte, lorsque les contraintes sont appliquées.

Si deux requêtes concurrentes insèrent le même couple, le conflit peut apparaître au flush ou au commit ; il faut rollback avant de réutiliser la Session. Ne pas transformer toute IntegrityError en « déjà aimé » : elle peut aussi indiquer une FK invalide ou une autre contrainte.

### Exemple Python propre à cette classe

Exemple inventé et non exécuté, à lire dans le contexte d’une fixture temporaire autorisée. Les objets parents `compte`, `categorie`, `dossier` et `commentaire` désignent les objets fictifs correspondants ; aucune connexion n’est créée. Une construction seule ne persiste pas la ligne.


```python
like_dossier = Vote(story=dossier, user=compte)
# Une autre ligne du même couple est interdite à l'écriture SQL.
# Le même compte pourra aimer un autre dossier.
```

### Formulation possible devant le jury

« Une ligne représente le like d’un compte pour un dossier. La base interdit deux lignes pour le même couple compte-dossier. Les totaux sont calculés par comptage. »

<a id="mah-c007"></a>

## MAH-C007 — CommentLike : Le like individuel d’un commentaire

**Source :** `backend/models.py:433` à `450` ; table `comment_likes` ; module `MAH-M001`.

Cette association précise qui aime quel commentaire. Son schéma s’inspire de celui de `Vote`, mais sa cible est `comments.id`, pas `stories.id`. Il est donc incorrect d’additionner ces deux tables pour calculer les likes d’un seul commentaire.

La migration refuse de convertir des compteurs historiques non nuls, car un entier ne permet pas de retrouver les auteurs des likes. Les routes concernées vérifient également que le compteur physique est exactement l’entier zéro. Le modèle ne réalise pas cette vérification historique lui-même.

L’option MySQL `InnoDB` de la table est une indication spécifique au dialecte. Elle ne configure ni le moteur de toutes les tables parentes déjà existantes, ni le service Aiven.

### Toutes les colonnes

| Colonne | Type déclaré | NULL autorisé | PK / unicité / index | Valeurs automatiques | Sens et limites propres au projet |
|---|---|---|---|---|---|
| `id` | `db.Integer` | Non | PK | Aucune valeur automatique déclarée | Identité technique d’une association. |
| `comment_id` | `db.Integer` | Non | index non unique ; FK → comments.id | Aucune valeur automatique déclarée | Commentaire aimé ; index non unique ix_comment_likes_comment_id via index=True. |
| `user_id` | `db.Integer` | Non | FK → users.id | Aucune valeur automatique déclarée | Compte aimant ; entre dans l’unicité du couple avec comment_id. |
| `created_at` | `db.DateTime` | Non | — | `default=datetime.utcnow` | Date d’association côté ORM. |

Une absence de valeur automatique déclarée n’est pas un défaut implicite à zéro ou chaîne vide. Pour `id`, la génération éventuelle relève de la clé entière et du moteur. Pour les dates, le callback est passé sans parenthèses pour être invoqué à chaque insertion concernée.

### Relations et cardinalités

| Attribut Python | Navigation | FK porteuse | Configuration ORM exacte |
|---|---|---|---|
| `CommentLike.comment` → `Comment` | Un parent obligatoire après persistance | `comment_likes.comment_id` | `back_populates='comment_likes'` |
| `CommentLike.user` → `User` | Un parent obligatoire après persistance | `comment_likes.user_id` | `back_populates='comment_likes'` |

`back_populates` nomme l’autre côté de la même association. Il n’ajoute pas une FK supplémentaire. Les relations ne sont pas configurées pour un chargement eager systématique : naviguer peut déclencher un SELECT et demande une Session utilisable. Une collection non filtrée n’est pas un filtre d’autorisation ou de visibilité.

### Contraintes complémentaires

Déclaration de table : `(db.UniqueConstraint('user_id', 'comment_id', name='unique_user_comment_like'), {'mysql_engine': 'InnoDB'})`.

L’unicité porte sur le couple `(user_id, comment_id)`, pas sur chacune de ses composantes. `id` reste une clé primaire distincte.

### Méthodes, propriétés et opérations

Aucune méthode personnalisée n’est définie dans cette classe. Construction, sélection, insertion, modification et suppression passent par les capacités héritées et la Session ; elles ne sont pas des méthodes métier ajoutées implicitement au modèle.

### Cas particuliers et erreurs à savoir expliquer

L’index simple sur comment_id accélère les filtrages et comptages par commentaire ; il ne rend pas un commentaire unique dans la table. C’est la contrainte du couple qui empêche les doubles likes d’un compte. Une suppression filtrée seulement par comment_id retirerait les likes de tous les comptes : l’API personnelle filtre aussi user_id.

Le modèle n’empêche pas un auteur d’aimer son propre commentaire par une contrainte SQL. Il ne remplace pas le contrôle des comptes bannis et du dossier actif. La migration et l’API refusent les compteurs historiques incompatibles au lieu d’attribuer des likes à des identités inventées.

### Exemple Python propre à cette classe

Exemple inventé et non exécuté, à lire dans le contexte d’une fixture temporaire autorisée. Les objets parents `compte`, `categorie`, `dossier` et `commentaire` désignent les objets fictifs correspondants ; aucune connexion n’est créée. Une construction seule ne persiste pas la ligne.


```python
like_commentaire = CommentLike(comment=commentaire, user=compte)
# La cible est un commentaire, pas directement le dossier.
# Cette création ne modifie pas Comment.likes.
```

### Formulation possible devant le jury

« Une ligne identifie le compte et le commentaire aimé. Le couple est unique. Un ancien compteur ne peut pas être converti en identités de lecteurs sans une décision de reprise. »

<a id="mah-c008"></a>

## MAH-C008 — Proposal : Une proposition soumise à la modération

**Source :** `backend/models.py:455` à `507` ; table `proposals` ; module `MAH-M001`.

Une proposition contient un titre, un contenu et un statut. Elle reste liée à son compte auteur, avec suppression SQL en cascade si ce compte est supprimé par une opération que la base accepte. Aucune catégorie, image ou référence de dossier publié n’est stockée ici.

Le statut initial est `pending` via le défaut ORM. Le modèle ne déclare ni ENUM, ni CHECK listant les transitions autorisées. Les routes administratives portent les décisions de modération. Accepter une proposition ne crée pas automatiquement un `Story` par un mécanisme de la classe.

### Toutes les colonnes

| Colonne | Type déclaré | NULL autorisé | PK / unicité / index | Valeurs automatiques | Sens et limites propres au projet |
|---|---|---|---|---|---|
| `id` | `db.Integer` | Non | PK | Aucune valeur automatique déclarée | Identité de la proposition, pas un identifiant de Story. |
| `user_id` | `db.Integer` | Non | FK → users.id | Aucune valeur automatique déclarée | Compte auteur obligatoire ; référence supprimée avec la ligne par CASCADE SQL. |
| `title` | `db.String(200)` | Non | — | Aucune valeur automatique déclarée | Titre proposé obligatoire ; aucun slug dans cette table. |
| `content` | `db.Text` | Non | — | Aucune valeur automatique déclarée | Texte proposé obligatoire ; aucune publication automatique. |
| `status` | `db.String(20)` | Non | — | `default='pending'` | Défaut ORM pending ; chaîne libre au niveau SQL, transitions contrôlées ailleurs. |
| `created_at` | `db.DateTime` | Non | — | `default=datetime.utcnow` | Création côté ORM. |
| `updated_at` | `db.DateTime` | Non | — | `default=datetime.utcnow` ; `onupdate=datetime.utcnow` | Dernière mise à jour côté ORM ; pas de trigger MySQL généré par cette déclaration. |

Une absence de valeur automatique déclarée n’est pas un défaut implicite à zéro ou chaîne vide. Pour `id`, la génération éventuelle relève de la clé entière et du moteur. Pour les dates, le callback est passé sans parenthèses pour être invoqué à chaque insertion concernée.

### Relations et cardinalités

| Attribut Python | Navigation | FK porteuse | Configuration ORM exacte |
|---|---|---|---|
| `Proposal.user` → `User` | Un parent obligatoire après persistance | `proposals.user_id` | `back_populates='proposals'` |

`back_populates` nomme l’autre côté de la même association. Il n’ajoute pas une FK supplémentaire. Les relations ne sont pas configurées pour un chargement eager systématique : naviguer peut déclencher un SELECT et demande une Session utilisable. Une collection non filtrée n’est pas un filtre d’autorisation ou de visibilité.

### Méthodes, propriétés et opérations

Aucune méthode personnalisée n’est définie dans cette classe. Construction, sélection, insertion, modification et suppression passent par les capacités héritées et la Session ; elles ne sont pas des méthodes métier ajoutées implicitement au modèle.

### Cas particuliers et erreurs à savoir expliquer

Modifier le statut ne déplace pas la ligne dans stories. Il n’y a pas de méthode `publish()` ni de relation `Proposal.story`. Un statut arbitraire tenant dans le type n’est pas refusé par une contrainte de domaine de ce modèle ; la validation d’entrée et des transitions est donc nécessaire dans les vues.

L’auteur obligatoire évite une proposition orpheline au niveau SQL. La suppression d’un compte et la modération d’une proposition restent des opérations distinctes, avec des droits et conséquences différents.

### Exemple Python propre à cette classe

Exemple inventé et non exécuté, à lire dans le contexte d’une fixture temporaire autorisée. Les objets parents `compte`, `categorie`, `dossier` et `commentaire` désignent les objets fictifs correspondants ; aucune connexion n’est créée. Une construction seule ne persiste pas la ligne.


```python
proposition = Proposal(user=compte, title="Sujet proposé",
                       content="Proposition entièrement inventée")
# Le défaut pending sera préparé pour l'INSERT ORM.
# Aucun Story n'est créé automatiquement.
```

### Formulation possible devant le jury

« Une proposition est une soumission à modérer, pas encore une histoire publiée. Son statut est une chaîne dont les transitions sont contrôlées par les routes. »

<a id="mah-c009"></a>

## MAH-C009 — Report : Un signalement ciblant réellement un commentaire

**Source :** `backend/models.py:512` à `581` ; table `reports` ; module `MAH-M001`.

Le stockage actuel est spécialisé : chaque signalement vise un commentaire par une vraie clé étrangère entière. `type` et `target_id` survivent dans le contrat Python et JSON pour la compatibilité, mais ne sont plus des colonnes de `reports`. On ne peut donc pas écrire une requête SQL sur une colonne actuelle `reports.target_id`.

Le modèle n’enregistre aucun `user_id` de déclarant. Il est impossible de retrouver un auteur de signalement depuis cette seule table. Cela n’exclut pas la présence de données personnelles dans `reason`, ni leur présence éventuelle dans d’autres systèmes. Il n’y a pas d’unicité par commentaire : plusieurs signalements peuvent concerner la même cible.

La propriété `target_id` valide une forme de chaîne ; assigner directement `comment_id` suit un autre chemin. Le contrat d’entrée HTTP a aussi ses propres contrôles. Ne pas confondre validation de format, existence de la cible et autorisation à signaler.

### Toutes les colonnes

| Colonne | Type déclaré | NULL autorisé | PK / unicité / index | Valeurs automatiques | Sens et limites propres au projet |
|---|---|---|---|---|---|
| `id` | `db.Integer` | Non | PK | Aucune valeur automatique déclarée | Identité du signalement ; plusieurs lignes peuvent viser le même commentaire. |
| `comment_id` | `db.Integer` | Non | index non unique ; FK → comments.id | Aucune valeur automatique déclarée | Vraie FK obligatoire ; index non unique ix_reports_comment_id, cascade SQL. |
| `reason` | `db.Text` | Non | — | Aucune valeur automatique déclarée | Motif obligatoire ; potentiellement sensible, ne pas afficher dans les journaux ou à tout visiteur. |
| `status` | `db.String(20)` | Non | — | `default='pending'` | Défaut ORM pending ; aucune liste SQL de statuts imposée. |
| `created_at` | `db.DateTime` | Non | — | `default=datetime.utcnow` | Date de signalement côté ORM. |

Une absence de valeur automatique déclarée n’est pas un défaut implicite à zéro ou chaîne vide. Pour `id`, la génération éventuelle relève de la clé entière et du moteur. Pour les dates, le callback est passé sans parenthèses pour être invoqué à chaque insertion concernée.

### Relations et cardinalités

| Attribut Python | Navigation | FK porteuse | Configuration ORM exacte |
|---|---|---|---|
| `Report.comment` → `Comment` | Un parent obligatoire après persistance | `reports.comment_id` | `back_populates='moderation_reports'` |

`back_populates` nomme l’autre côté de la même association. Il n’ajoute pas une FK supplémentaire. Les relations ne sont pas configurées pour un chargement eager systématique : naviguer peut déclencher un SELECT et demande une Session utilisable. Une collection non filtrée n’est pas un filtre d’autorisation ou de visibilité.

### Méthodes, propriétés et opérations

- [MAH-F0007](04_REPERTOIRE_FONCTIONS_METHODES.md#mah-f0007) — `Report.type[lecture]` : contrat détaillé, paramètres, retour, étapes, effets et erreurs.
- [MAH-F0008](04_REPERTOIRE_FONCTIONS_METHODES.md#mah-f0008) — `Report.type[ecriture]` : contrat détaillé, paramètres, retour, étapes, effets et erreurs.
- [MAH-F0009](04_REPERTOIRE_FONCTIONS_METHODES.md#mah-f0009) — `Report.target_id[lecture]` : contrat détaillé, paramètres, retour, étapes, effets et erreurs.
- [MAH-F0010](04_REPERTOIRE_FONCTIONS_METHODES.md#mah-f0010) — `Report.target_id[ecriture]` : contrat détaillé, paramètres, retour, étapes, effets et erreurs.
- [MAH-F0011](04_REPERTOIRE_FONCTIONS_METHODES.md#mah-f0011) — `Report.to_dict` : contrat détaillé, paramètres, retour, étapes, effets et erreurs.

Clés exactes de `to_dict()` : `id`, `type`, `target_id`, `reason`, `status`, `created_at`. Les dates sont converties avec isoformat si elles existent, sinon None.

type et target_id sont calculés par les propriétés ; comment_id n’est pas une clé exposée directement par ce dictionnaire. Une lecture d’attribut expiré peut provoquer un rafraîchissement SQL ; la méthode ne contient toutefois ni INSERT, ni DELETE, ni commit explicite.

### Cas particuliers et erreurs à savoir expliquer

`report.type = 'comment'` est accepté sans écrire de colonne type. Une autre valeur déclenche ValueError. `report.target_id = '23'` fixe comment_id à 23 mais ne prouve pas que le commentaire 23 existe ; la FK et l’API couvrent cette autre question.

Le setter refuse notamment les entiers Python, les chiffres non ASCII, les signes, espaces, décimales, « 0 », « 01 », les chaînes trop longues et les valeurs supérieures à 2147483647. Affecter directement comment_id ne passe pas par ce setter. Le type SQL Integer et la FK ne reproduisent pas exactement toutes ses règles de format.

Lire target_id sur un objet incomplet dont comment_id vaut None produit la chaîne « None ». Le sérialiseur ne doit pas être présenté comme un validateur de construction. L’absence de colonne déclarant n’autorise pas à rendre tous les motifs publics.

### Exemple Python propre à cette classe

Exemple inventé et non exécuté, à lire dans le contexte d’une fixture temporaire autorisée. Les objets parents `compte`, `categorie`, `dossier` et `commentaire` désignent les objets fictifs correspondants ; aucune connexion n’est créée. Une construction seule ne persiste pas la ligne.


```python
signalement = Report(comment=commentaire, reason="Motif fictif pour l'exercice")
# type reste une propriété constante ; comment_id portera la vraie référence.
# N'utiliser target_id pour sérialiser qu'une fois l'objet correctement préparé.
```

### Formulation possible devant le jury

« Le signalement actuel a une vraie clé étrangère comment_id. Les noms type et target_id sont des propriétés Python gardées pour le contrat JSON ; ils ne décrivent plus le stockage physique. »

<a id="mah-c010"></a>

## MAH-C010 — ColdCaseUpdate : Une nouvelle information attachée à un dossier

**Source :** `backend/models.py:586` à `633` ; table `cold_case_updates` ; module `MAH-M001`.

Cette table stocke un texte de mise à jour et sa date, liés à un dossier. Le terme « cold case » décrit l’usage métier prévu ; la clé étrangère vérifie seulement l’existence d’un `Story`. Elle ne compare pas la catégorie du dossier à une valeur imposée.

La classe ne stocke pas d’auteur de mise à jour, de titre séparé ni de statut. Il ne faut pas inventer une relation `ColdCaseUpdate.author`. L’autorisation de publier et la sélection d’un dossier actif appartiennent à la route administrative.

### Toutes les colonnes

| Colonne | Type déclaré | NULL autorisé | PK / unicité / index | Valeurs automatiques | Sens et limites propres au projet |
|---|---|---|---|---|---|
| `id` | `db.Integer` | Non | PK | Aucune valeur automatique déclarée | Identité d’une mise à jour. |
| `story_id` | `db.Integer` | Non | FK → stories.id | Aucune valeur automatique déclarée | Dossier obligatoire ; pas de contrainte SQL sur sa catégorie. |
| `content` | `db.Text` | Non | — | Aucune valeur automatique déclarée | Texte de la nouvelle information ; aucun titre séparé. |
| `created_at` | `db.DateTime` | Non | — | `default=datetime.utcnow` | Date de création côté ORM. |

Une absence de valeur automatique déclarée n’est pas un défaut implicite à zéro ou chaîne vide. Pour `id`, la génération éventuelle relève de la clé entière et du moteur. Pour les dates, le callback est passé sans parenthèses pour être invoqué à chaque insertion concernée.

### Relations et cardinalités

| Attribut Python | Navigation | FK porteuse | Configuration ORM exacte |
|---|---|---|---|
| `ColdCaseUpdate.story` → `Story` | Un parent obligatoire après persistance | `cold_case_updates.story_id` | `back_populates='cold_case_updates'` |

`back_populates` nomme l’autre côté de la même association. Il n’ajoute pas une FK supplémentaire. Les relations ne sont pas configurées pour un chargement eager systématique : naviguer peut déclencher un SELECT et demande une Session utilisable. Une collection non filtrée n’est pas un filtre d’autorisation ou de visibilité.

### Méthodes, propriétés et opérations

- [MAH-F0012](04_REPERTOIRE_FONCTIONS_METHODES.md#mah-f0012) — `ColdCaseUpdate.to_dict` : contrat détaillé, paramètres, retour, étapes, effets et erreurs.

Clés exactes de `to_dict()` : `id`, `story_id`, `content`, `created_at`. Les dates sont converties avec isoformat si elles existent, sinon None.

Aucun auteur ni titre n’est inventé lors de la sérialisation. Une lecture d’attribut expiré peut provoquer un rafraîchissement SQL ; la méthode ne contient toutefois ni INSERT, ni DELETE, ni commit explicite.

### Cas particuliers et erreurs à savoir expliquer

Une ligne peut techniquement référencer tout dossier existant. L’étiquette métier de la table n’impose aucune catégorie SQL. Le code API contrôle les droits administratifs et l’accès au dossier ; ces étapes ne sont pas des méthodes de cette classe.

Supprimer le dossier supprime la mise à jour par CASCADE. Supprimer une mise à jour ne supprime pas le dossier. L’absence d’auteur dans la table ne fournit pas un historique individuel d’édition. Une éventuelle obligation d’audit demanderait une conception séparée, hors de ce lot documentaire.

### Exemple Python propre à cette classe

Exemple inventé et non exécuté, à lire dans le contexte d’une fixture temporaire autorisée. Les objets parents `compte`, `categorie`, `dossier` et `commentaire` désignent les objets fictifs correspondants ; aucune connexion n’est créée. Une construction seule ne persiste pas la ligne.


```python
nouvelle_information = ColdCaseUpdate(story=dossier,
                                     content="Nouvel élément fictif")
# L'objet ne possède pas de relation auteur.
# Le rôle administratif et la catégorie se contrôlent dans les vues.
```

### Formulation possible devant le jury

« La mise à jour est un texte daté rattaché à un dossier. La clé étrangère garantit ce rattachement, mais elle ne vérifie pas que le dossier appartient à une catégorie cold case. »

## Parcours concret d’un dossier, sans nouvelle donnée privée

Un récit du catalogue possède un slug, un contenu et un chemin PNG ; il devient une ligne Story reliée à une catégorie et à un auteur. Un lecteur commente : une ligne Comment référence Story et éventuellement User, tout en copiant le pseudo. Un autre lecteur aime ce commentaire : une ligne CommentLike référence Comment et User. Un signalement crée Report avec comment_id ; il ne modifie pas le texte du commentaire et ne stocke pas le déclarant.

Archiver le dossier conserve ces lignes et fait intervenir les filtres de visibilité. La purge, si les contrôles administratifs l’acceptent dans une autre opération, supprime le dossier et ses dépendances. Ni les six textes ni les six illustrations ne sont lus depuis une base pour rédiger cette explication ; l’étude porte sur leurs structures de stockage.

## Lecture orientée vers le futur lot 6H.21.6

Les identifiants de classe et de fonction permettront de retrouver les futures explications de code. Chemin proposé, encore inexistant : `docs/soutenance/code-commente-mahamadou/backend/models.py`. Aucune copie commentée ligne par ligne n’est créée ici. Pour repérer la même fonction après un décalage de lignes, utiliser d’abord son identifiant et son nom qualifié, puis la table de correspondance actuelle.
