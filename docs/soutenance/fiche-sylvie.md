# Fiche Sylvie — Backend Flask et API REST

[Retour au sommaire de soutenance](README.md)

Questions-réponses historiques récupérées de la réponse Codex de l’étape 15.1 du **25 octobre 2026**, fondée sur le commit `dec5c7ef4c753970bd94014b37b59b035e1877f1`. Audit de référence : étape 15.8.1 ; préparation documentaire : étape 15.8.2, au commit `857190654457b15d7324adde8c920d9fdd3db0c8`.

Les formulations des questions et des réponses courtes originales sont conservées. Les explications, exemples, identifiants de repérage et références facilitent la révision. **VALIDÉE** signifie conforme aux sources ; ce statut ne constitue pas une validation en production.

Empreinte SHA-256 du texte historique complet : `218cf13b814a1f20a4258f1f6b24ab600b296bc62baab1c23610a36905ace4cd`.

**Portée des preuves :** les résultats de tests et de rendu Mermaid sont historiques. Aucun test fonctionnel, rendu de diagramme, serveur, migration ou accès Aiven n’est exécuté pendant cette préparation. Les droits des illustrations restent à confirmer.

## Sommaire

- [Repères pour comprendre](#repères-pour-comprendre)
- [Questions du jury](#questions-du-jury)

Accès direct aux 18 questions :

[SYL-01](#syl-01) · [SYL-02](#syl-02) · [SYL-03](#syl-03) · [SYL-04](#syl-04) · [SYL-05](#syl-05) · [SYL-06](#syl-06)

[SYL-07](#syl-07) · [SYL-08](#syl-08) · [SYL-09](#syl-09) · [SYL-10](#syl-10) · [SYL-11](#syl-11) · [SYL-12](#syl-12)

[SYL-13](#syl-13) · [SYL-14](#syl-14) · [SYL-15](#syl-15) · [SYL-16](#syl-16) · [SYL-17](#syl-17) · [SYL-18](#syl-18)

## Repères pour comprendre

**Phrase à retenir à l’oral**

> « Flask reçoit les requêtes, contrôle les données et les permissions, puis utilise SQLAlchemy. L’API renvoie un résultat et un code HTTP que le frontend peut interpréter. »

Sources : [backend/index.py](../../backend/index.py), [routes](../../backend/api/v1/views), [permissions.py](../../backend/api/v1/views/permissions.py), [Swagger](../../backend/api/v1/swagger.json).

### 1. Flask et l’organisation des routes

**Flask** est le framework Python qui reçoit les requêtes HTTP et construit les réponses.

Exemple : `POST /api/v1/login` lit les identifiants, vérifie le compte et prépare la session.

Un **Blueprint** regroupe des routes.

Le projet possède un Blueprint principal :

```python
app_views = Blueprint(
    'app_views',
    __name__,
    url_prefix='/api/v1'
)
```

Il importe les fichiers de routes : utilisateurs, histoires, théories, commentaires, propositions et administration.

Les routes `/login`, `/me`, `/logout` et `/stats` sont déclarées directement dans `backend/index.py`, avec leur préfixe `/api/v1`.

`backend/api/v1/app.py` réexporte l’application configurée dans `index.py`. Ce fichier ne définit pas un second backend indépendant.

### 2. Méthodes HTTP et 24 opérations

- **GET** demande une lecture.
- **POST** déclenche ici une création ou une action.
- **DELETE** sert ici au bannissement d’un utilisateur.

La route de bannissement utilise `DELETE`, mais son implémentation positionne `is_banned = True`. Elle ne supprime pas le compte.

Les **24 opérations** sont vérifiées dans les déclarations de routes et dans OpenAPI. Les méthodes automatiques `HEAD` et `OPTIONS` ne sont pas comptées.

Tous les chemins ci-dessous commencent par **`/api/v1`**.

| Nº | Méthode et chemin | Accès | Fonction |
|---:|---|---|---|
| 1 | `POST /users` | Public¹ | Inscription |
| 2 | `GET /users` | Administrateur | Liste des comptes |
| 3 | `POST /login` | Public | Connexion |
| 4 | `GET /me` | Membre | Compte courant et CSRF |
| 5 | `POST /logout` | Public¹ | Déconnexion |
| 6 | `GET /stories` | Public | Liste des histoires |
| 7 | `GET /stories/slug/{slug}` | Public | Lecture d’une histoire |
| 8 | `GET /coldcases/{case_id}/updates` | Public | Mises à jour du dossier |
| 9 | `GET /stories/{story_id}/theories` | Public | Liste des théories |
| 10 | `POST /stories/{story_id}/theories` | Membre | Création d’une théorie |
| 11 | `POST /theories/{theory_id}/like` | Membre | Ajout d’un like |
| 12 | `GET /stories/{story_id}/comments` | Public | Liste des commentaires |
| 13 | `POST /stories/{story_id}/comments` | Membre | Création d’un commentaire |
| 14 | `POST /comments/{comment_id}/like` | Membre | Ajout d’un like |
| 15 | `POST /votes/{story_id}` | Membre | Vote pour une histoire |
| 16 | `POST /proposals` | Membre | Proposition en `pending` |
| 17 | `GET /proposals` | Administrateur | Liste des propositions |
| 18 | `POST /comments/{comment_id}/report` | Membre | Signalement d’un commentaire |
| 19 | `POST /reports` | Membre | Signalement générique, type `comment` seulement |
| 20 | `GET /admin/reports` | Administrateur | Liste des signalements |
| 21 | `DELETE /admin/users/{username}/ban` | Administrateur | Bannissement |
| 22 | `GET /stats` | Public | Compteurs |
| 23 | `GET /swagger.json` | Public | Document OpenAPI |
| 24 | `GET /swagger` | Public | Interface Swagger UI |

¹ L’inscription et la déconnexion acceptent les requêtes anonymes. Avec une session existante, le contrôle CSRF s’applique. L’inscription vérifie aussi le compte associé à cette session.

« Membre » signifie compte connecté et non banni. « Administrateur » ajoute la vérification du rôle en base.

La route des mises à jour vérifie l’existence d’une histoire. Elle ne vérifie pas que sa catégorie est Cold Case.

### 3. Modèles et requêtes SQLAlchemy

Une **requête ORM** demande des données au moyen des modèles.

Exemples réels :

| Expression | Fonction | Utilité |
|---|---|---|
| `User.query.filter_by(username=username).first()` | Chercher le compte par pseudo | Connexion |
| `db.session.get(Story, story_id)` | Chercher une histoire par clé primaire | Vérifier le dossier |
| `Theory.query.filter_by(story_id=story_id)` | Filtrer les théories | Lecture par dossier |
| `.order_by(Theory.created_at.asc())` | Trier par date croissante | Présenter les contributions dans l’ordre |
| `Report.query.filter_by(type="comment", target_id=str(comment.id)).count()` | Compter les signalements | Produire le compteur d’un commentaire |

Les likes utilisent une instruction SQL d’incrémentation :

```python
.values(likes=Theory.likes + 1)
```

Cela évite d’écraser un compteur avec une ancienne valeur lue par une autre requête.

Les likes répétés restent autorisés. Il n’existe pas de table attribuant un like unique à chaque utilisateur.

### 4. Inscription et connexion

#### Inscription

Le serveur vérifie notamment :

- corps JSON de type objet ;
- champs requis ;
- pseudo de 100 caractères maximum ;
- email de 150 caractères maximum et format contrôlé ;
- mot de passe de 8 à 50 caractères ;
- présence d’une majuscule, minuscule, chiffre et caractère spécial ;
- absence de doublon pour le pseudo et l’email.

Le client ne choisit pas son rôle administrateur.

Le mot de passe est transmis à `set_password()`, puis le compte est ajouté et la transaction validée. La réponse de création est `201`.

L’inscription ne connecte pas automatiquement le compte.

#### Connexion

Le serveur :

1. lit le pseudo et le mot de passe ;
2. recherche le compte ;
3. vérifie le mot de passe ;
4. refuse les comptes bannis ;
5. efface l’ancienne session ;
6. inscrit l’identifiant du compte dans la session ;
7. crée le jeton CSRF ;
8. renvoie les informations du compte.

Le mot de passe est conservé tel que fourni pour sa vérification. Le code ne lui applique pas le même nettoyage que pour le pseudo.

### 5. Hachage, session et autorisations

Le **hachage** transforme le mot de passe en une valeur adaptée à sa vérification.

Le modèle utilise :

```python
generate_password_hash(password)
check_password_hash(self.password_hash, password)
```

Le mot de passe d’origine n’est pas stocké dans la colonne `password_hash`. Le hachage n’est pas un chiffrement destiné à être inversé.

Une **session Flask signée** conserve un état associé au navigateur. La signature permet de détecter une modification du cookie.

**Signé ne signifie pas chiffré.** Le contenu du cookie ne doit pas être considéré comme secret.

Pour les routes protégées, `get_authenticated_user()` :

- lit `user_id` dans la session ;
- recherche le compte en base ;
- refuse un compte absent ;
- refuse un compte banni ;
- efface la session dans ces deux derniers cas.

Le décorateur `admin_required` relit ensuite `user.is_admin`. Le rôle déclaré par le navigateur ou présent dans l’affichage ne suffit pas.

L’auteur d’une théorie, d’une proposition, d’un commentaire ou d’un vote provient du compte authentifié.

### 6. CSRF et CORS

Une attaque **CSRF** cherche à faire exécuter une action par un navigateur qui possède déjà un cookie de session.

Le contrôle `before_request` vérifie les méthodes d’écriture lorsqu’un `user_id` est présent dans la session.

Il compare le jeton de session à l’en-tête `X-CSRF-Token` avec `secrets.compare_digest()`.

La connexion est explicitement exemptée. Une requête anonyme ne passe pas ce contrôle de session, mais une route membre vérifie toujours l’authentification.

**CORS** définit les origines autorisées pour les échanges du navigateur. La configuration autorise les credentials pour les origines prévues.

CORS, CSRF et permissions répondent à des besoins différents. Aucun de ces contrôles ne remplace les autres.

### 7. Codes HTTP

| Code | Signification | Exemple réel |
|---|---|---|
| `200` | Opération réussie | Lecture des théories ou connexion |
| `201` | Création réussie | Compte, théorie, proposition ou vote |
| `400` | Entrées invalides | Titre vide, JSON invalide, email refusé |
| `401` | Authentification absente ou invalide | `/me` sans session |
| `403` | Accès refusé | Compte banni, rôle insuffisant ou mauvais CSRF |
| `404` | Ressource absente | Histoire ou commentaire introuvable |
| `409` | Conflit | Vote déjà enregistré |
| `500` | Erreur serveur | Échec SQL géré pendant une écriture |

Un doublon de pseudo ou d’email est renvoyé en **400** dans l’implémentation actuelle. Le **409** correspond ici au vote déjà présent.

### 8. Validations et transactions

La validation serveur est nécessaire parce qu’une requête peut être envoyée sans utiliser le formulaire officiel.

Les fonctions partagées contrôlent notamment :

- forme du JSON ;
- chaînes obligatoires ;
- limites de longueur ;
- encodage UTF-8 ;
- taille des champs texte ;
- identifiants de ressources.

Pour les propositions et théories :

- titre : **200 caractères maximum** ;
- contenu : **65 535 octets UTF-8 maximum**.

Un caractère peut occuper plusieurs octets. La taille en octets est donc différente du nombre de caractères.

Les contrôles ne sont pas strictement identiques dans toutes les routes. La route générique `/reports` possède par exemple sa propre validation du type et de l’identifiant cible.

Les écritures concernées utilisent `commit()`. Les erreurs SQL interceptées déclenchent `rollback()` et une réponse d’erreur.

Pour les votes et inscriptions, le code distingue certains conflits uniques connus des autres erreurs d’intégrité. Toutes les erreurs SQL ne doivent pas devenir un conflit métier.

### 9. Tests, Swagger et limites

**Preuve historique**, consignée dans le [README principal](../../README.md#L540) :

| Suite | Résultat rapporté |
|---|---:|
| Backend Python | 205 réussis |
| Frontend JavaScript | 226 réussis |
| Lanceur local | 8 réussis |
| **Total** | **439 réussis** |

La campagne est datée du **25 octobre 2026** dans le README. Elle n’a pas été relancée ici. Aucun receipt brut supplémentaire n’a été examiné pour confirmer cette exécution.

Les sources des tests couvrent notamment les permissions, CSRF, validations, erreurs, transactions et contrats OpenAPI.

**Swagger** décrit l’API et permet de l’explorer. Le document est au format OpenAPI `3.0.3`.

Swagger UI utilise des ressources CDN. Le chargement de la page ne prouve donc pas, à lui seul, que ces ressources externes sont disponibles.

Les fonctions présentes uniquement dans l’API sont :

- commentaires ;
- votes ;
- likes ;
- signalements ;
- liste administrative des utilisateurs ;
- bannissement ;
- consultation des mises à jour d’un dossier.

## Questions du jury

### SYL-01

**Question du jury**

À quoi sert Flask ?

**Réponse courte à dire**

Il reçoit les requêtes et produit les réponses. Dans la connexion, il lit le JSON, contrôle le compte et prépare la session.

**Explication simple**

Flask associe une adresse et une méthode HTTP à une fonction qui prépare une réponse.

**Exemple concret**

POST /api/v1/login vérifie le mot de passe.

**Référence technique**

[backend/index.py](../../backend/index.py#L241)

**Statut de validation**

**VALIDÉE — conforme aux sources.**

### SYL-02

**Question du jury**

Qu’est-ce qu’un Blueprint ?

**Réponse courte à dire**

C’est un groupe de routes. `app_views` rassemble les routes métier sous `/api/v1`.

**Explication simple**

Regrouper les routes évite de tout déclarer dans un seul fichier.

**Exemple concret**

app_views porte le préfixe /api/v1.

**Référence technique**

[backend/api/v1/views/__init__.py](../../backend/api/v1/views/__init__.py#L3)

**Statut de validation**

**VALIDÉE — conforme aux sources.**

### SYL-03

**Question du jury**

Combien de Blueprints principaux sont présents ?

**Réponse courte à dire**

Un Blueprint `app_views` est déclaré. Certaines routes sont directement attachées à l’application Flask.

**Explication simple**

Le regroupement métier et les routes directes appartiennent à la même application.

**Exemple concret**

app.py réexporte l’application de backend/index.py.

**Référence technique**

[backend/api/v1/app.py](../../backend/api/v1/app.py#L1)

**Statut de validation**

**VALIDÉE — conforme aux sources.**

### SYL-04

**Question du jury**

Pourquoi compter 24 opérations plutôt que 24 URL ?

**Réponse courte à dire**

Une même URL peut accepter plusieurs méthodes. `GET /users` et `POST /users` constituent deux opérations.

**Explication simple**

La méthode fait partie du contrat, même lorsque le chemin est identique.

**Exemple concret**

GET /users liste ; POST /users inscrit.

**Référence technique**

[backend/api/v1/views/users.py](../../backend/api/v1/views/users.py#L31)

**Statut de validation**

**VALIDÉE — conforme aux sources.**

### SYL-05

**Question du jury**

Que fait la route `DELETE .../ban` ?

**Réponse courte à dire**

Elle marque le compte comme banni. Elle ne supprime pas sa ligne.

**Explication simple**

Le nom d’une méthode HTTP ne suffit pas à décrire son effet : il faut lire le traitement.

**Exemple concret**

Le compte reçoit is_banned = True.

**Référence technique**

[backend/api/v1/views/index.py](../../backend/api/v1/views/index.py#L104)

**Statut de validation**

**VALIDÉE — conforme aux sources.**

### SYL-06

**Question du jury**

Comment le mot de passe est-il stocké ?

**Réponse courte à dire**

Le modèle stocke le hachage produit par Werkzeug. La connexion compare le mot de passe fourni à ce hachage.

**Explication simple**

Le serveur vérifie le mot de passe avec une fonction de hachage ; il ne le stocke pas en clair.

**Exemple concret**

set_password() et check_password().

**Référence technique**

[backend/models.py](../../backend/models.py#L29)

**Statut de validation**

**VALIDÉE — conforme aux sources.**

### SYL-07

**Question du jury**

Un cookie signé est-il confidentiel ?

**Réponse courte à dire**

La signature protège son intégrité. Elle ne chiffre pas son contenu.

**Explication simple**

La signature détecte une modification du cookie mais ne cache pas son contenu.

**Exemple concret**

La session contient notamment user_id.

**Référence technique**

[backend/index.py](../../backend/index.py#L289)

**Statut de validation**

**VALIDÉE — conforme aux sources.**

### SYL-08

**Question du jury**

Pourquoi relire le compte en base ?

**Réponse courte à dire**

Son rôle ou son état peut avoir changé depuis la connexion. La vérification permet notamment de refuser un compte banni.

**Explication simple**

Un compte peut être banni ou perdre son rôle après sa connexion.

**Exemple concret**

get_authenticated_user() relit User.

**Référence technique**

[backend/api/v1/views/permissions.py](../../backend/api/v1/views/permissions.py#L8)

**Statut de validation**

**VALIDÉE — conforme aux sources.**

### SYL-09

**Question du jury**

Peut-on devenir administrateur en modifiant le JavaScript ?

**Réponse courte à dire**

Les routes administrateur vérifient `user.is_admin` côté serveur. Modifier l’affichage ne donne pas cette permission.

**Explication simple**

Le rôle est vérifié sur le compte en base avant l’exécution des routes protégées.

**Exemple concret**

admin_required vérifie user.is_admin.

**Référence technique**

[backend/api/v1/views/permissions.py](../../backend/api/v1/views/permissions.py#L47)

**Statut de validation**

**VALIDÉE — conforme aux sources.**

### SYL-10

**Question du jury**

Pourquoi utiliser un jeton CSRF ?

**Réponse courte à dire**

Le navigateur envoie son cookie automatiquement. Le jeton permet de contrôler les écritures utilisant cette session.

**Explication simple**

Le cookie peut accompagner automatiquement une requête ; le serveur attend aussi le jeton prévu.

**Exemple concret**

secrets.compare_digest() compare les jetons.

**Référence technique**

[backend/index.py](../../backend/index.py#L152)

**Statut de validation**

**VALIDÉE — conforme aux sources.**

### SYL-11

**Question du jury**

Toutes les routes POST exigent-elles ce jeton ?

**Réponse courte à dire**

Le contrôle dépend de la présence d’une session authentifiée. La connexion est exemptée ; l’inscription et la déconnexion anonymes restent possibles.

**Explication simple**

Le contrôle CSRF s’applique quand user_id est présent dans la session, avec une exemption pour login.

**Exemple concret**

Une inscription anonyme reste possible ; une route membre vérifie aussi le compte.

**Référence technique**

[backend/index.py](../../backend/index.py#L152)

**Statut de validation**

**VALIDÉE — conforme aux sources.**

### SYL-12

**Question du jury**

Quelle différence entre 401 et 403 ?

**Réponse courte à dire**

`401` indique que l’authentification est absente ou invalide. `403` indique un refus, par exemple pour le rôle, le bannissement ou le CSRF.

**Explication simple**

Le code HTTP permet au frontend de distinguer une absence de connexion d’un refus d’accès.

**Exemple concret**

401 sans session ; 403 pour un compte banni.

**Référence technique**

[backend/api/v1/views/permissions.py](../../backend/api/v1/views/permissions.py#L8)

**Statut de validation**

**VALIDÉE — conforme aux sources.**

### SYL-13

**Question du jury**

Pourquoi valider aussi dans Flask ?

**Réponse courte à dire**

Le client peut être contourné. Le serveur doit protéger ses données indépendamment de l’interface.

**Explication simple**

Le serveur protège les données même si la requête ne vient pas de l’interface officielle.

**Exemple concret**

La création de théorie vérifie le dossier, le titre et le contenu.

**Référence technique**

[backend/api/v1/views/write_support.py](../../backend/api/v1/views/write_support.py#L27)

**Statut de validation**

**VALIDÉE — conforme aux sources.**

### SYL-14

**Question du jury**

Comment éviter un double vote ?

**Réponse courte à dire**

La route vérifie le vote existant et la base possède une contrainte unique. Le doublon reconnu donne une réponse `409`.

**Explication simple**

Le contrôle préalable améliore la réponse ; la contrainte unique reste la barrière en base.

**Exemple concret**

Un doublon reconnu renvoie 409.

**Référence technique**

[backend/api/v1/views/histoires.py](../../backend/api/v1/views/histoires.py#L59)

**Statut de validation**

**VALIDÉE — conforme aux sources.**

### SYL-15

**Question du jury**

Un utilisateur peut-il liker plusieurs fois ?

**Réponse courte à dire**

Oui. Les routes incrémentent un compteur sans unicité par utilisateur.

**Explication simple**

Aucun enregistrement n’associe chaque like à un utilisateur unique.

**Exemple concret**

La route incrémente Theory.likes.

**Référence technique**

[backend/api/v1/views/theories.py](../../backend/api/v1/views/theories.py#L109)

**Statut de validation**

**VALIDÉE — conforme aux sources.**

### SYL-16

**Question du jury**

Que se passe-t-il si l’écriture SQL échoue ?

**Réponse courte à dire**

Dans les blocs prévus, le serveur appelle `rollback()` et renvoie une erreur. Il ne confirme pas la création.

**Explication simple**

La création n’est confirmée qu’après la validation SQL ; les erreurs gérées annulent la transaction.

**Exemple concret**

Une erreur SQL produit rollback() et une réponse 500.

**Référence technique**

[backend/api/v1/views/proposals.py](../../backend/api/v1/views/proposals.py#L77)

**Statut de validation**

**VALIDÉE — conforme aux sources.**

### SYL-17

**Question du jury**

Que prouvent les tests backend ?

**Réponse courte à dire**

La campagne historique rapporte 205 réussites dans un environnement SQLite isolé. Elle ne constitue pas une validation complète d’Aiven ou des migrations MySQL.

**Explication simple**

Le résultat mentionné est historique et concerne un environnement isolé, sans nouvelle exécution ici.

**Exemple concret**

205 tests backend rapportés ; Aiven non revalidé.

**Référence technique**

[README.md](../../README.md#L546)

**Statut de validation**

**VALIDÉE — preuve historique rapportée dans le README, sans nouvelle exécution.**

### SYL-18

**Question du jury**

Swagger exécute-t-il les tests ?

**Réponse courte à dire**

Non. Il documente et permet d’explorer les opérations. Les tests automatisés sont des fichiers distincts.

**Explication simple**

La documentation interactive et les suites automatisées ont des rôles différents.

**Exemple concret**

Swagger décrit les routes ; backend/tests contient les tests.

**Référence technique**

[backend/api/v1/views/index.py](../../backend/api/v1/views/index.py#L128)

**Statut de validation**

**VALIDÉE — conforme aux sources.**

[Retour au sommaire de soutenance](README.md)
