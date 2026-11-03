# Fiche Mahamadou — Base de données et intégration

> Etat de diffusion scolaire du 3 novembre 2026 : suivre le [guide actuel](../../LIVRAISON_SCOLAIRE.md) et la [validation scolaire](VALIDATION_SCOLAIRE.md). Les sections de campagnes anterieures et leurs commandes sont historiques ; elles ne remplacent pas la procedure actuelle. Les chemins sous `C:\chemin\utilisateur` sont des exemples anonymises. Les archives internes signalees sont conservees localement.

## État courant — 2 novembre 2026

Lire d’abord les [supports 6H.1](SUPPORT_JURY_LOT6H1.md), l’[index courant](INDEX_CODE_LOT6H1.md) et la [procédure sur un autre PC](../../LIVRAISON_SCOLAIRE.md). Le bilan actuel distingue **854 tests historiques**, recette Edge réussie en SQLite fictif et contrôles documentaires de ce lot. Le modèle actuel contient dix tables et treize FK ; le compte est partagé sur dix pages, les signalements sont contextualisés, les likes de dossier/commentaire sont individuels.

Les compléments et questions ci-dessous conservent leur contexte historique. Les anciennes mentions de fonctions absentes, de neuf tables ou de recette non exécutée ne constituent pas l’état courant. Les 76 questions/réponses historiques restent conservées. Aucun résultat MySQL ou de déploiement n’est ajouté.


## Complément courant 6G.2 — Vote et CommentLike

Bilan 6G.2 (archive interne non livree) : Vote historique inchangé ; nouvelle table CommentLike avec FK et couple unique utilisateur/commentaire. COUNT produit le nombre, pas un chiffre ajouté dans l'interface. La candidate refuse les anciens compteurs différents de zéro avant DDL ; aucune attribution inventée. La purge suit ces enfants en interne sans changer les sept indicateurs. Dix modèles et treize FK déclarées ; tests SQLite uniquement, aucune migration réelle.

## Complément courant 6C.2 — relation et migration

Report vise exclusivement Comment : comment_id entier obligatoire, FK CASCADE, relation moderation_reports. Le JSON garde type=comment et target_id calculés, mais plus ces colonnes génériques en SQL. La migration copie le type SQL réel de comments.id et refuse tout ancien type/cible incompatible avant DDL. Le cas other subsiste comme test de reprise refusée. La révision aléatoire de Story invalide les anciens aperçus ; les dix FK précédentes restent inchangées.

Les tests utilisent uniquement SQLite mémoire avec FK ON. La migration réelle, MySQL et la concurrence de production restent à vérifier ; aucun contenu purgé n’est recréé par downgrade. Aucun reçu persistant. Les réponses courtes historiques décrivant Report sans FK concernent l’état antérieur. Bilan courant (archive interne non livree).


> **Actualisation du 29 octobre 2026 — étape 5.** Les questions et réponses courtes historiques ci-dessous sont conservées. Les affirmations « non relancé ici » décrivent leur préparation antérieure : les campagnes ultérieures sont présentées dans [Tests et validation](TESTS_ET_VALIDATION.md), avec 439 réussites automatiques, la recette Edge et les dix BDD PASS. La recette Edge est automatisée, pas entièrement manuelle humaine ; Aiven et migrations restent non validés. Les repères actuels (archive interne non livree) tiennent compte des commentaires ajoutés au code. Les diagrammes révisés ont leur contrôle local dans le bilan (archive interne non livree).

## Complément lot 6C phase 1 — archivage réversible

`Story.archived_at` est une date UTC nullable : NULL signifie actif. Ce champ unique évite un booléen redondant, une nouvelle table ou une FK supplémentaire. La migration `c6c100000001` ajoute la colonne sans modifier les dix FK ni les cascades ; les dossiers existants restent actifs. Elle n’est appliquée à aucune base réelle ; son upgrade est testé sur un schéma fictif SQLite mémoire seulement.

Archiver et restaurer ne retirent aucun enfant des relations SQLAlchemy. Les tests comparent les neuf tables et conservent théories, commentaires, votes, mises à jour et signalements. La date donne la trace du retrait courant, sans journal d’acteurs ou d’historique complet. Restaurer remet NULL ; `updated_at` reflète la transition. SQLite ne prouve pas les verrous InnoDB ni le déploiement MySQL. Voir le bilan et les réserves (archive interne non livree).

[Retour au sommaire de soutenance](README.md)

Questions-réponses historiques récupérées de la réponse Codex de l’étape 15.1 du **25 octobre 2026**, fondée sur le commit `dec5c7ef4c753970bd94014b37b59b035e1877f1`. Audit de référence : étape 15.8.1 ; préparation documentaire : étape 15.8.2, au commit `857190654457b15d7324adde8c920d9fdd3db0c8`.

Les formulations des questions et des réponses courtes originales sont conservées. Les explications, exemples, identifiants de repérage et références facilitent la révision. **VALIDÉE** signifie conforme aux sources ; ce statut ne constitue pas une validation en production.

Empreinte SHA-256 du texte historique complet : `218cf13b814a1f20a4258f1f6b24ab600b296bc62baab1c23610a36905ace4cd`.

**Portée des preuves :** les résultats de tests et de rendu Mermaid sont historiques. Aucun test fonctionnel, rendu de diagramme, serveur, migration ou accès Aiven n’est exécuté pendant cette préparation. Les droits des illustrations restent à confirmer.

> **Complément 5.1 autorisé.** Réviser aussi la réponse 18 sur les métadonnées et les modes Alembic. Les scripts existants sont seulement commentés, sans opération SQL changée ni migration exécutée ; un downgrade ne restaure pas les données supprimées. Voir les [réponses orales](ORAL_JURY.md), le [suivi du jury](SUIVI_REMARQUES_JURY.md) et le bilan 5.1 (archive interne non livree).

> **Actualisation fonctionnelle 6A — 30 octobre 2026.** Les 76 questions/réponses courtes historiques sont conservées : leurs anciennes limites d’administration décrivent l’état d’avant ce lot. Le tableau dispose maintenant de la liste des utilisateurs et du bannissement des comptes ordinaires, avec confirmation, relecture serveur et refus de tous les administrateurs en 409. Le contrat compte désormais 25 opérations. Voir la [réponse orale sur le bannissement](ORAL_JURY.md#19-comment-fonctionne-le-bannissement-administrateur-), les preuves 487 tests (archive interne non livree) et l’index actuel (archive interne non livree). Aucun navigateur réel exécuté pour 6A.

> **Complément 6B — 30 octobre 2026.** La consultation administrative des dossiers est livrée : recherche par titre, filtres, catégories inconnues et fiche existante, sans modifier les données ni le bannissement 6A. Préparer la [réponse orale 20](ORAL_JURY.md#20-comment-consultez-vous-les-dossiers-dans-ladministration-), les preuves 533 tests (archive interne non livree) et les repères actuels (archive interne non livree). Les questions et réponses historiques restent conservées. Les API de lecture restent publiques ; aucun navigateur réel exécuté.

> **Complément 6D — 30 octobre 2026.** Le tableau possède sept compteurs : le nouveau total compte uniquement le statut exact `pending` de la liste administrative existante. Préparer la [réponse orale 21](ORAL_JURY.md#21-comment-comptez-vous-les-propositions-en-attente-), le bilan 6D et ses 561 tests (archive interne non livree) et les repères actuels (archive interne non livree). Mélissa explique le DOM, le chargement et le nettoyage ; Sylvie les permissions et le JSON inchangés ; Mahamadou le statut texte, les catégories et l'invariance des neuf tables après lecture. Les 76 réponses historiques sont conservées. La recette navigateur reste reportée et le verdict VM NO-GO est maintenu.

## Sommaire

- [Repères pour comprendre](#repères-pour-comprendre)
- [Questions du jury](#questions-du-jury)

Accès direct aux 18 questions :

[MAH-01](#mah-01) · [MAH-02](#mah-02) · [MAH-03](#mah-03) · [MAH-04](#mah-04) · [MAH-05](#mah-05) · [MAH-06](#mah-06)

[MAH-07](#mah-07) · [MAH-08](#mah-08) · [MAH-09](#mah-09) · [MAH-10](#mah-10) · [MAH-11](#mah-11) · [MAH-12](#mah-12)

[MAH-13](#mah-13) · [MAH-14](#mah-14) · [MAH-15](#mah-15) · [MAH-16](#mah-16) · [MAH-17](#mah-17) · [MAH-18](#mah-18)

## Repères pour comprendre

**Phrase à retenir à l’oral**

> « La base conserve les comptes, les dossiers et les contributions. SQLAlchemy permet au backend Python de manipuler ces données. Les contraintes maintiennent leur cohérence, et Alembic décrit les évolutions du schéma. »

Sources principales : [models.py](../../backend/models.py), [configuration Flask](../../backend/index.py), [migrations](../../migrations/versions).

### 1. MySQL et les neuf tables

**MySQL** est un système de gestion de base de données relationnelle. Il organise les données dans des tables reliées.

Dans le projet, il conserve les informations après la fermeture du navigateur ou du serveur. Le navigateur passe par Flask pour consulter ou modifier ces informations.

Les **neuf modèles SQLAlchemy** sont vérifiés dans les sources.

| Modèle / table | Fonction | Exemple d’information |
|---|---|---|
| `User` / `users` | Comptes des utilisateurs | Pseudo, email, mot de passe haché, rôle, bannissement |
| `Category` / `categories` | Classement des dossiers | Nom et description d’une catégorie |
| `Story` / `stories` | Dossiers d’enquête | Titre, slug, résumé, récit, référence d’image |
| `Theory` / `theories` | Analyses proposées sur un dossier | Titre, contenu, auteur, compteur de likes |
| `Comment` / `comments` | Commentaires d’un dossier | Texte, auteur, pseudo conservé, likes |
| `Vote` / `votes` | Votes des utilisateurs pour les dossiers | Utilisateur et dossier concernés |
| `Proposal` / `proposals` | Propositions de nouvelles histoires | Titre, contenu, statut |
| `Report` / `reports` | Signalements | Type, identifiant de cible, motif, statut |
| `ColdCaseUpdate` / `cold_case_updates` | Mises à jour d’un dossier | Contenu et dossier concerné |

Une proposition est distincte d’une histoire. Elle est enregistrée en `pending`. Aucun parcours d’acceptation ou de publication automatique n’est implémenté.

### 2. Clés primaires, clés étrangères et unicité

Une **clé primaire** identifie une ligne de manière unique.

Exemple réel :

```python
id = db.Column(db.Integer, primary_key=True)
```

Chaque table possède un identifiant `id`. Deux histoires peuvent avoir des titres proches, mais leurs identifiants restent différents.

Une **clé étrangère** référence une ligne d’une autre table.

Exemple réel dans `Theory` :

```python
story_id = db.Column(
    db.Integer,
    db.ForeignKey(
        "stories.id",
        name="fk_theories_story",
        ondelete="CASCADE"
    ),
    nullable=False
)
```

Cela rattache chaque théorie à une histoire existante.

Une **contrainte unique** interdit un doublon. Les unicités déclarées sont :

- `users.username` ;
- `users.email` ;
- `categories.name` ;
- `stories.slug` ;
- le couple `votes(user_id, story_id)`.

Exemple réel :

```python
db.UniqueConstraint(
    "user_id",
    "story_id",
    name="unique_user_story_vote"
)
```

Cette dernière contrainte autorise un utilisateur à voter pour plusieurs histoires. Elle interdit plusieurs votes du même utilisateur pour la même histoire.

### 3. Les dix relations et leurs cardinalités

La **cardinalité** indique combien de lignes peuvent être associées.

Dans le tableau, « plusieurs » signifie **zéro, une ou plusieurs** lignes du côté des contributions.

| Clé étrangère | Cardinalité | Suppression déclarée |
|---|---|---|
| `stories.category_id → categories.id` | Une catégorie par histoire ; plusieurs histoires par catégorie | Sans règle `ON DELETE` explicite |
| `stories.author_id → users.id` | Un auteur par histoire ; plusieurs histoires par auteur | Sans règle explicite |
| `theories.story_id → stories.id` | Une histoire par théorie ; plusieurs théories par histoire | `CASCADE` |
| `theories.user_id → users.id` | Zéro ou un utilisateur par théorie ; plusieurs théories par utilisateur | `SET NULL` |
| `comments.story_id → stories.id` | Une histoire par commentaire ; plusieurs commentaires par histoire | `CASCADE` |
| `comments.user_id → users.id` | Zéro ou un utilisateur par commentaire ; plusieurs commentaires par utilisateur | `SET NULL` |
| `votes.story_id → stories.id` | Une histoire par vote ; plusieurs votes par histoire | `CASCADE` |
| `votes.user_id → users.id` | Un utilisateur par vote ; plusieurs votes par utilisateur | `CASCADE` |
| `proposals.user_id → users.id` | Un utilisateur par proposition ; plusieurs propositions par utilisateur | `CASCADE` |
| `cold_case_updates.story_id → stories.id` | Une histoire par mise à jour ; plusieurs mises à jour par histoire | `CASCADE` |

**Point important :** `reports.target_id` est une chaîne. Ce champ n’est pas une clé étrangère. L’API contrôle l’existence du commentaire avant de créer son signalement.

#### Diagramme relationnel existant

Diagramme synchronisé avec le [README principal](../../README.md) et révisé le 29 octobre 2026. La validation du 25 octobre concernait la variante antérieure ; le bilan de l’étape 5 (archive interne non livree) précise le contrôle local actuel. Le rendu GitHub reste non attesté.

```mermaid
erDiagram
  users {
    int id PK
    string username UK
    string email UK
  }
  categories {
    int id PK
    string name UK
  }
  stories {
    int id PK
    string slug UK
    string management_revision UK
    int category_id FK
    int author_id FK
  }
  theories {
    int id PK
    int story_id FK
    int user_id FK "NULL autorisé"
  }
  comments {
    int id PK
    int story_id FK
    int user_id FK "NULL autorisé"
  }
  votes {
    int id PK
    int story_id FK
    int user_id FK "UNIQUE avec story_id"
  }
  comment_likes {
    int id PK
    int comment_id FK
    int user_id FK "UNIQUE avec comment_id"
  }
  proposals {
    int id PK
    int user_id FK
  }
  reports {
    int id PK
    int comment_id FK
  }
  cold_case_updates {
    int id PK
    int story_id FK
  }
  users ||..o{ stories : "auteur obligatoire"
  categories ||..o{ stories : "catégorie obligatoire"
  stories ||..o{ theories : "CASCADE"
  users |o..o{ theories : "SET NULL"
  stories ||..o{ comments : "CASCADE"
  users |o..o{ comments : "SET NULL"
  users ||..o{ votes : "CASCADE"
  stories ||..o{ votes : "CASCADE"
  users ||..o{ proposals : "CASCADE"
  stories ||..o{ cold_case_updates : "CASCADE"
  comments ||..o{ reports : "CASCADE"
  comments ||..o{ comment_likes : "CASCADE"
  users ||..o{ comment_likes : "CASCADE"
```

`PK` signifie clé primaire. `FK` signifie clé étrangère. `UK` indique une unicité individuelle.

### 4. `CASCADE`, `SET NULL` et relations SQLAlchemy

**`CASCADE`** supprime les lignes dépendantes lors de la suppression du parent, lorsque la contrainte SQL est effectivement appliquée.

Exemple : supprimer une histoire entraîne la suppression de ses théories selon la contrainte déclarée.

**`SET NULL`** conserve la ligne dépendante et retire sa référence au parent.

Exemple : après suppression d’un utilisateur, une théorie peut rester avec `user_id = NULL`.

Cette différence permet de conserver certaines contributions. Elle ne garantit pas une anonymisation complète : `Comment` conserve aussi un champ `username`.

Les collections de `Story` déclarent également :

```python
cascade="all, delete-orphan"
```

C’est un comportement de l’ORM. Il faut le distinguer des règles SQL `ON DELETE`. Les relations de `User` ne déclarent pas toutes une cascade ORM équivalente.

Enfin, les références `stories.author_id` et `stories.category_id` restent obligatoires, sans cascade explicite. Une suppression du parent peut donc être refusée tant que des histoires le référencent.

### 5. SQLAlchemy et les transactions

**SQLAlchemy** est un ORM : il fait correspondre des classes Python et des tables.

Exemple réel :

```python
Theory.query.filter_by(story_id=story_id)
```

Cette requête sélectionne les théories d’un dossier. Elle permet d’exprimer le filtre avec les modèles Python.

Une **transaction** regroupe des opérations sur la base.

Dans la création d’une théorie, le code suit ce principe :

```python
db.session.add(new_theory)
db.session.commit()
```

- `add()` prépare l’objet dans la session SQLAlchemy.
- `commit()` valide la transaction. L’insertion peut être envoyée pendant le flush associé.
- `rollback()` annule les changements non validés après une erreur.

Les routes d’écriture concernées interceptent les erreurs SQL et appellent `rollback()`. Cela évite de conserver une transaction en échec.

### 6. Les quatre migrations Alembic

Une **migration** est une évolution versionnée du schéma.

La chaîne présente dans le dépôt est :

```text
921687c1bd7c → 3111f5767fc6 → a590c8aac613 → 82deda84bc35
```

| Révision | Évolution |
|---|---|
| `921687c1bd7c` | Crée les sept tables initiales et leurs contraintes |
| `3111f5767fc6` | Remplace certaines clés étrangères pour ajouter `CASCADE` et `SET NULL` |
| `a590c8aac613` | Ajoute `reports`, `cold_case_updates` et `users.is_banned` |
| `82deda84bc35` | Supprime l’ancien compteur `comments.reports` |

Le nombre de signalements d’un commentaire est maintenant calculé depuis les lignes de `reports`.

**Nuance à connaître :** les modèles actuels et les migrations sont deux éléments différents. Les fichiers de migration décrivent les changements prévus. Leur présence ne prouve pas leur application sur Aiven.

Les valeurs `default=` et `onupdate=` des modèles sont appliquées par SQLAlchemy. Elles ne sont pas automatiquement des valeurs par défaut ou des déclencheurs permanents dans MySQL.

### 7. Connexion Flask, Aiven et TLS

Dans [backend/index.py](../../backend/index.py#L86), le backend lit six paramètres Aiven :

- hôte ;
- port ;
- utilisateur ;
- mot de passe ;
- nom de base ;
- chemin du certificat CA.

Les noms de variables sont `AIVEN_DB_HOST`, `AIVEN_DB_PORT`, `AIVEN_DB_USER`, `AIVEN_DB_PASSWORD`, `AIVEN_DB_NAME` et `AIVEN_CA_CERT`.

Si les six paramètres sont renseignés, Flask-SQLAlchemy utilise MySQL avec le pilote **PyMySQL**. Le code configure le certificat CA dans les options SSL et active `pool_pre_ping`.

**TLS** protège la communication avec le serveur de base de données. Le certificat CA sert à vérifier le certificat présenté par le serveur.

Si le groupe Aiven est incomplet, le backend utilise `DATABASE_URL`, ou le fichier SQLite local si cette variable est absente.

**Vérifié dans les sources :** cette logique de configuration existe.

**Non vérifié :** valeurs locales, disponibilité du certificat, connexion TLS réelle et révision déployée sur Aiven.

### 8. Intégration et différence entre SQLite et MySQL

Parcours réel d’une contribution :

1. Le formulaire recueille le titre et le contenu.
2. `app.js` valide la saisie et vérifie la session.
3. `api.js` envoie une requête JSON avec le cookie et le CSRF.
4. Flask contrôle la requête.
5. La route crée un objet SQLAlchemy.
6. SQLAlchemy écrit dans la base configurée.
7. Flask renvoie le résultat.
8. Le navigateur affiche le succès ou l’erreur.

Les tests backend utilisent **SQLite en mémoire** avec des données synthétiques. Les garde-fous lus dans les tests interdisent les connexions externes.

Ces tests utilisent notamment `db.create_all()`. Ils ne rejouent pas les quatre migrations historiques.

Ils peuvent vérifier des contrats HTTP et des écritures isolées. Ils ne prouvent pas le comportement complet de MySQL, ses contraintes déployées ou sa connexion TLS.

## Questions du jury

### MAH-01

**Question du jury**

À quoi sert MySQL ?

**Réponse courte à dire**

Il conserve durablement les comptes, dossiers et contributions. Le backend y accède pour lire et enregistrer les données.

**Explication simple**

Les informations restent enregistrées après la fermeture du navigateur ; la base choisie dépend de la configuration.

**Exemple concret**

Un dossier peut être relu lors d’une visite suivante.

**Référence technique**

[backend/index.py](../../backend/index.py#L86)

**Statut de validation**

**VALIDÉE — conforme aux sources.**

### MAH-02

**Question du jury**

Pourquoi utiliser plusieurs tables ?

**Réponse courte à dire**

Chaque table représente une notion. Par exemple, une histoire peut recevoir plusieurs théories sans recopier tout le dossier dans chaque théorie.

**Explication simple**

Séparer les sujets évite de recopier les mêmes informations partout.

**Exemple concret**

Une histoire possède plusieurs théories dans une table distincte.

**Référence technique**

[backend/models.py](../../backend/models.py#L83)

**Statut de validation**

**VALIDÉE — conforme aux sources.**

### MAH-03

**Question du jury**

Qu’est-ce qu’une clé primaire ?

**Réponse courte à dire**

C’est l’identifiant unique d’une ligne. Dans `stories`, il s’agit de `id`.

**Explication simple**

Un identifiant permet de distinguer deux lignes même si leur titre est identique.

**Exemple concret**

stories.id identifie un dossier.

**Référence technique**

[backend/models.py](../../backend/models.py#L88)

**Statut de validation**

**VALIDÉE — conforme aux sources.**

### MAH-04

**Question du jury**

Qu’est-ce qu’une clé étrangère ?

**Réponse courte à dire**

C’est une référence vers une autre table. `theories.story_id` rattache une théorie à son histoire.

**Explication simple**

La référence relie une contribution au dossier auquel elle appartient.

**Exemple concret**

Theory.story_id référence stories.id.

**Référence technique**

[backend/models.py](../../backend/models.py#L225)

**Statut de validation**

**VALIDÉE — conforme aux sources.**

### MAH-05

**Question du jury**

Quelle est la relation entre histoire et théorie ?

**Réponse courte à dire**

Une histoire peut avoir plusieurs théories. Chaque théorie appartient à une seule histoire.

**Explication simple**

Le lien est obligatoire pour la théorie ; une histoire peut n’avoir encore aucune théorie.

**Exemple concret**

Une liste de théories vide reste possible.

**Référence technique**

[backend/models.py](../../backend/models.py#L225)

**Statut de validation**

**VALIDÉE — conforme aux sources.**

### MAH-06

**Question du jury**

Pourquoi l’auteur d’une théorie peut-il être nul ?

**Réponse courte à dire**

La base prévoit `SET NULL` lors de la suppression de l’utilisateur. La contribution peut ainsi être conservée.

**Explication simple**

L’auteur est facultatif dans le modèle, et la règle SQL déclarée permet de conserver la contribution.

**Exemple concret**

theories.user_id peut devenir NULL si la contrainte est appliquée.

**Référence technique**

[backend/models.py](../../backend/models.py#L235)

**Statut de validation**

**VALIDÉE — conforme aux sources.**

### MAH-07

**Question du jury**

Quelle différence entre `CASCADE` et `SET NULL` ?

**Réponse courte à dire**

`CASCADE` supprime les lignes dépendantes. `SET NULL` conserve ces lignes et retire leur référence au parent.

**Explication simple**

Les deux règles décrivent le traitement des lignes liées quand un parent disparaît.

**Exemple concret**

Suppression d’histoire : CASCADE ; suppression d’auteur de théorie : SET NULL.

**Référence technique**

[backend/models.py](../../backend/models.py#L225)

**Statut de validation**

**VALIDÉE — conforme aux sources.**

### MAH-08

**Question du jury**

Comment empêcher deux votes identiques ?

**Réponse courte à dire**

La contrainte unique porte sur le couple utilisateur/histoire. L’API renvoie aussi `409` lorsqu’un vote existe déjà.

**Explication simple**

La même paire utilisateur-dossier ne peut être enregistrée deux fois selon la contrainte déclarée.

**Exemple concret**

POST /api/v1/votes/{story_id} renvoie 409 pour un doublon reconnu.

**Référence technique**

[backend/models.py](../../backend/models.py#L425)

**Statut de validation**

**VALIDÉE — conforme aux sources.**

### MAH-09

**Question du jury**

Pourquoi garder une contrainte SQL si l’API vérifie déjà ?

**Réponse courte à dire**

Deux requêtes peuvent arriver presque en même temps. La contrainte reste une protection au niveau de la base.

**Explication simple**

La base protège aussi contre deux demandes simultanées qui passent le premier contrôle.

**Exemple concret**

La route traite le conflit unique après rollback.

**Référence technique**

[backend/api/v1/views/histoires.py](../../backend/api/v1/views/histoires.py#L99)

**Statut de validation**

**VALIDÉE — conforme aux sources.**

### MAH-10

**Question du jury**

À quoi sert SQLAlchemy ?

**Réponse courte à dire**

Il permet de manipuler les tables avec des modèles Python. Par exemple, `filter_by(story_id=...)` sélectionne les contributions d’un dossier.

**Explication simple**

Les classes Python représentent les tables et servent à construire les requêtes.

**Exemple concret**

filter_by(story_id=story_id) limite la lecture au dossier choisi.

**Référence technique**

[backend/api/v1/views/theories.py](../../backend/api/v1/views/theories.py#L48)

**Statut de validation**

**VALIDÉE — conforme aux sources.**

### MAH-11

**Question du jury**

Que fait `commit()` ?

**Réponse courte à dire**

Il valide la transaction en cours. Dans la route de création, il rend persistante la nouvelle théorie si l’opération réussit.

**Explication simple**

La validation rend durables les changements de la transaction si l’écriture réussit.

**Exemple concret**

Création d’une théorie : add(), puis commit().

**Référence technique**

[backend/api/v1/views/theories.py](../../backend/api/v1/views/theories.py#L96)

**Statut de validation**

**VALIDÉE — conforme aux sources.**

### MAH-12

**Question du jury**

Que fait `rollback()` ?

**Réponse courte à dire**

Il annule la transaction non validée après une erreur. La route peut alors renvoyer une erreur sans laisser cette transaction bloquée.

**Explication simple**

Après un échec, la transaction en cours est abandonnée avant de répondre au client.

**Exemple concret**

La route renvoie 500 si l’écriture SQL échoue.

**Référence technique**

[backend/api/v1/views/theories.py](../../backend/api/v1/views/theories.py#L103)

**Statut de validation**

**VALIDÉE — conforme aux sources.**

### MAH-13

**Question du jury**

À quoi sert Alembic ?

**Réponse courte à dire**

Il décrit les évolutions du schéma dans un ordre versionné. Le projet possède quatre révisions successives.

**Explication simple**

Les migrations décrivent les transformations successives du schéma ; elles ne prouvent pas leur déploiement.

**Exemple concret**

Quatre révisions reliées par down_revision.

**Référence technique**

[migrations/versions/921687c1bd7c_baseline_schema.py](../../migrations/versions/921687c1bd7c_baseline_schema.py#L14)

**Statut de validation**

**VALIDÉE — conforme aux sources.**

### MAH-14

**Question du jury**

Pourquoi supprimer `comments.reports` ?

**Réponse courte à dire**

Les signalements possèdent leur propre table. Le compteur est calculé depuis cette table, ce qui évite de maintenir deux représentations du même nombre.

**Explication simple**

Le nombre affiché est calculé à partir des signalements réellement enregistrés.

**Exemple concret**

Report.query.filter_by(type='comment', target_id=...).count().

**Référence technique**

[backend/api/v1/views/comments.py](../../backend/api/v1/views/comments.py#L13)

**Statut de validation**

**VALIDÉE — conforme aux sources.**

### MAH-15

**Question du jury**

Pourquoi le certificat CA est-il utile ?

**Réponse courte à dire**

Il participe à la vérification du serveur pendant la connexion TLS. Le code transmet son chemin à PyMySQL.

**Explication simple**

Le code donne à PyMySQL le chemin du certificat CA ; la connexion réelle n’est pas testée ici.

**Exemple concret**

connect_args contient ssl.ca.

**Référence technique**

[backend/index.py](../../backend/index.py#L109)

**Statut de validation**

**VALIDÉE — conforme aux sources.**

### MAH-16

**Question du jury**

Les tests SQLite prouvent-ils que MySQL fonctionne ?

**Réponse courte à dire**

Ils apportent une preuve sur les comportements testés avec SQLite. La connexion et les contraintes MySQL doivent être vérifiées séparément.

**Explication simple**

Un comportement vérifié avec une base de test n’est pas automatiquement vérifié sur un autre serveur.

**Exemple concret**

Les tests créent leur schéma SQLite en mémoire.

**Référence technique**

[backend/tests/test_reports.py](../../backend/tests/test_reports.py#L25)

**Statut de validation**

**VALIDÉE — conforme aux sources.**

### MAH-17

**Question du jury**

`reports.target_id` est-il une clé étrangère ?

**Réponse courte à dire**

Non. C’est une chaîne ; l’API vérifie actuellement que le commentaire ciblé existe.

**Explication simple**

Un champ qui contient un identifiant n’est pas nécessairement une contrainte de référence SQL.

**Exemple concret**

La route /reports vérifie le commentaire ciblé.

**Référence technique**

[backend/models.py](../../backend/models.py#L512)

**Statut de validation**

**VALIDÉE — conforme aux sources.**

### MAH-18

**Question du jury**

Les migrations créent-elles les dossiers de démonstration ?

**Réponse courte à dire**

Non. Elles construisent ou modifient le schéma. Aucun peuplement initial complet et reproductible n’est fourni.

**Explication simple**

Créer les tables ne remplit pas automatiquement les dossiers et les comptes de démonstration.

**Exemple concret**

Il faut préparer séparément des données fictives.

**Référence technique**

[README.md](../../README.md#L535)

**Statut de validation**

**VALIDÉE — conforme aux sources.**

[Retour au sommaire de soutenance](README.md)

## Complément oral 6E.2 — hors des réponses historiques

« User porte le compte et ses états. Story exige un auteur ; théories et commentaires peuvent perdre leur lien utilisateur, mais leur texte reste. Le commentaire garde aussi un pseudo copié. Votes et propositions ont des FK CASCADE, tandis que le comportement ORM doit être vérifié séparément.

Un signalement vise désormais uniquement un commentaire par une FK entière ; aucun déclarant n'est stocké. Supprimer un compte peut donc concerner plusieurs tables, mais je ne supprime pas les dossiers partagés automatiquement. Les anciens cookies et les copies restent à traiter. Je n'ai changé ni schéma ni migration et je n'ai connecté aucune base réelle dans 6E.2. »

À distinguer devant le jury : bannir le compte, archiver le dossier, purger une archive et traiter l'effacement personnel. Voir les conséquences (archive interne non livree) et la procédure (archive interne non livree). La sauvegarde durable contient des sources sélectionnées, pas les interactions de la base ; elle est conservée sans modification.
