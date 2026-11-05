# Requêtes SQLAlchemy — lot 6H.21.5

Les Petits Enquêteurs — préparation pour Mahamadou — **5 novembre 2026, Europe/Paris**.

**Proposition documentaire externe, sans installation autorisée.** Référence : 203 fichiers de la copie intégrée, vérifiés par empreintes. Aucun module applicatif importé, aucun accès SQL, aucune migration, aucun test applicatif ni intervention sur le serveur 5066. Les exemples sont des illustrations non exécutées, pas des commandes à lancer sur une base réelle. Les responsabilités BDD de Mahamadou sont distinguées des composants partagés avec Sylvie et du frontend de Mélissa.

[Sommaire des huit guides](01_GUIDE_REQUETES_SQLALCHEMY_LOT6H21_5.md#sommaire) · [Références exactes et soutenance](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md) · [Contrôles et limites](08_VALIDATION_DOCUMENTAIRE_LOT6H21_5.md)

<a id="sommaire"></a>

## Sommaire des huit guides

1. [Requêtes SQLAlchemy](01_GUIDE_REQUETES_SQLALCHEMY_LOT6H21_5.md)
2. [Transactions et intégrité](02_GUIDE_TRANSACTIONS_INTEGRITE_LOT6H21_5.md)
3. [Parcours fonctionnels complets](03_GUIDE_PARCOURS_FONCTIONNELS_LOT6H21_5.md)
4. [Intégration Flask, API et SQLAlchemy](04_GUIDE_INTEGRATION_FLASK_API_LOT6H21_5.md)
5. [Permissions et sécurité](05_GUIDE_PERMISSIONS_SECURITE_LOT6H21_5.md)
6. [Persistance et environnements](06_GUIDE_PERSISTANCE_ENVIRONNEMENTS_LOT6H21_5.md)
7. [Correspondance avec la soutenance](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md)
8. [Validation documentaire](08_VALIDATION_DOCUMENTAIRE_LOT6H21_5.md)

Les huit noms de fichiers portent le suffixe LOT6H21_5 pour éviter les confusions avec les guides installés du lot 6H.21.4. Le sommaire est intégré à ce premier fichier : aucun neuvième Markdown n’est nécessaire pour l’installation future. Les annexes JSON et le ZIP restent des preuves externes tant qu’un autre périmètre n’est pas autorisé.

## Périmètre et vocabulaire d’exécution

L’inventaire joint distingue les sites d’appel statiques des instructions SQL réellement exécutées. Un appel dans une boucle peut produire plusieurs requêtes ; une chaîne filter_by/order_by/all comporte plusieurs appels Python pour une seule lecture SQL, puis des lectures de sérialisation peuvent s’ajouter. Une condition peut empêcher tout appel. Le nombre d’entrées du catalogue n’est donc pas un nombre de requêtes par page.

Les formes Query présentes restent utilisables dans les dépendances épinglées ; SQLAlchemy 2 les décrit comme API historique. Les formes Core select/update/delete coexistent avec elles dans le code. Ce guide explique ce mélange sans proposer une refonte ni prétendre modifier les sources. [API Query officielle](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html).

| Étape | Ce que le code fait | Une instruction SQL est-elle déjà partie ? |
|---|---|---|
| Modèle / constructeur | Décrire une table ou créer un objet | Pas par ce seul fait |
| Query.filter_by, select, where, order_by | Construire une requête | Pas par ces seules constructions |
| Query.first/all/count | Évaluer un Query | Généralement oui ; Session.get a sa propre gestion de l’identité |
| Session.execute(stmt) | Exécuter une instruction Core/ORM | Oui au niveau de cette exécution, sous réserve de refus/erreur préalable |
| Result.mappings/scalars | Choisir la forme de lecture | Pas une seconde exécution indépendante |
| Result.first/all/scalar | Consommer un résultat | Consommation de l’exécution déjà demandée ; ne pas la confondre avec Query.first/all |
| add / affectation / Session.delete | Préparer un état ORM | Pas forcément ; le flush envoie les DML |
| flush | Envoyer les changements ORM | Oui, dans la transaction encore ouverte |
| commit | Flusher si nécessaire puis valider | Validation distincte de la réception HTTP |
| rollback | Annuler/terminer la transaction active | Ne reconstitue pas un commit antérieur |

Un SELECT ORM peut déclencher un autoflush de changements en attente. Une navigation de relation ou un sérialiseur peut demander une lecture implicite d’attribut expiré. Affirmer « cette ligne ne contient pas execute donc aucune base n’est touchée » serait trop fort.

## Familles de requêtes expliquées de A à J

Les SQL ci-dessous sont des équivalents pédagogiques avec paramètres liés. Ils ne sont pas une sortie du compilateur, un journal de base ou un script prêt à appliquer. Les noms d’alias, détails du COUNT et clauses de verrou dépendent du dialecte. Aucun exemple n’a été exécuté.

<a id="famille-01"></a>

### Famille 01 — Lire une clé primaire

**A — Objectif et explication simple.** Retrouver le compte désigné par la session Flask, sans faire confiance à un user_id de formulaire.

**B — Syntaxe Python utilisée ou réduction fidèle.**

```python
user = db.session.get(User, user_id)
```

**C — Mécanisme et déroulement.** Le contrôle distingue session absente, compte absent et compte banni ; il vide la session Flask dans les deux derniers cas. Une identité ORM en cache n’est pas une garantie de fraîcheur de tout le système.

**D — Équivalent SQL pédagogique.**

```sql
SELECT id, username, email, password_hash, is_admin, is_banned, created_at
FROM users WHERE id = :user_id;
```

**E — Tables et colonnes.** users.id ; les autres colonnes de User constituent l’objet chargé.

**F — Résultat et moment de chargement.** Un objet User ou None ; la Session peut fournir une identité déjà présente et non expirée sans nouveau SELECT. Une lecture nécessaire ou un rafraîchissement peut interroger la base.

**G — Erreurs possibles et limites.** RuntimeError si le contexte Flask manque ; erreurs de connexion possibles. La fonction de permission ne capture pas elle-même toutes les SQLAlchemyError.

**H — Effets sur la base.** Aucun DML explicitement demandé ici. Lire le compte ne suffit pas à autoriser une action administrateur.

**I — Exemple réel et fonctions.** [MAH-F0177 — get_authenticated_user](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0177). Le chemin et la ligne actuels figurent dans la correspondance, avec l’empreinte du fichier.

**J — Formulation orale.** « Je cherche une identité de ligne. Je vérifie ensuite son état et son rôle ; une clé primaire ne donne aucun droit. »

<a id="famille-02"></a>

### Famille 02 — Filtrer plusieurs égalités

**A — Objectif et explication simple.** Lire un dossier actif par son slug, en empêchant la lecture publique d’une archive.

**B — Syntaxe Python utilisée ou réduction fidèle.**

```python
story = Story.query.filter_by(slug=slug, archived_at=None).first()
```

**C — Mécanisme et déroulement.** Le slug est encodé en segment d’URL par api.js. Un dossier archivé ou absent entraîne le 404 de cette vue. Le JSON reçu est ensuite vérifié par isStory.

**D — Équivalent SQL pédagogique.**

```sql
SELECT * FROM stories
WHERE slug = :slug AND archived_at IS NULL LIMIT 1;
```

**E — Tables et colonnes.** stories.slug et stories.archived_at ; unicité du slug indépendante du filtre d’archive.

**F — Résultat et moment de chargement.** filter_by construit un Query ; first déclenche normalement sa lecture avec limitation, renvoyant une Story ou None. None dans un filtre nullable devient IS NULL, pas = NULL.

**G — Erreurs possibles et limites.** La route ne contient pas de bloc SQLAlchemyError général ; une panne de base peut donc suivre le traitement serveur 500 plutôt qu’une réponse métier 404.

**H — Effets sur la base.** Lecture demandée ; l’autoflush de la Session peut envoyer des changements en attente avant une requête ORM. Ce parcours n’ajoute pas lui-même un objet.

**I — Exemple réel et fonctions.** [MAH-F0161 — get_story_by_slug](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0161). Le chemin et la ligne actuels figurent dans la correspondance, avec l’empreinte du fichier.

**J — Formulation orale.** « Je décris le filtre, puis first l’évalue. Le dossier doit exister et être actif ; le navigateur ne peut pas annuler ce filtre. »

<a id="famille-03"></a>

### Famille 03 — Exprimer un prédicat

**A — Objectif et explication simple.** Séparer la vue active, archivée ou complète des dossiers administratifs.

**B — Syntaxe Python utilisée ou réduction fidèle.**

```python
query = Story.query.filter(Story.archived_at.is_not(None))
rows = query.order_by(Story.created_at.desc(), Story.id.desc()).all()
```

**C — Mécanisme et déroulement.** La route accepte state=active, archived ou all. Le helper api.js de liste des archives demande spécifiquement state=archived ; cette sélection client n’étend pas les permissions.

**D — Équivalent SQL pédagogique.**

```sql
SELECT * FROM stories WHERE archived_at IS NOT NULL
ORDER BY created_at DESC, id DESC;
```

**E — Tables et colonnes.** stories.archived_at, created_at, id ; le tri par id départage des dates égales.

**F — Résultat et moment de chargement.** filter reçoit une expression SQLAlchemy ; is_ et is_not expriment NULL correctement. all matérialise une liste ; une liste vide est une lecture réussie.

**G — Erreurs possibles et limites.** État inconnu : 400. Authentification/administration : 401 ou 403. SQLAlchemyError gérée : rollback puis 500.

**H — Effets sur la base.** Lecture sans modification métier ; le tri construit une clause, pas une exécution à lui seul.

**I — Exemple réel et fonctions.** [MAH-F0145 — get_admin_stories](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0145). Le chemin et la ligne actuels figurent dans la correspondance, avec l’empreinte du fichier.

**J — Formulation orale.** « filter exprime la condition SQL ; le serveur contrôle l’accès avant de retourner même les archives. »

<a id="famille-04"></a>

### Famille 04 — Lister et trier

**A — Objectif et explication simple.** Retourner chronologiquement les commentaires d’un dossier actif.

**B — Syntaxe Python utilisée ou réduction fidèle.**

```python
rows = Comment.query.filter_by(story_id=story_id).order_by(Comment.created_at.asc()).all()
```

**C — Mécanisme et déroulement.** La sérialisation enrichie parcourt ensuite les résultats et calcule les signalements, et les likes si le compteur historique est compatible. Ce travail peut ajouter des SELECT.

**D — Équivalent SQL pédagogique.**

```sql
SELECT * FROM comments WHERE story_id = :story_id
ORDER BY created_at ASC;
```

**E — Tables et colonnes.** comments.story_id et created_at ; le parent est contrôlé par get_active_story.

**F — Résultat et moment de chargement.** all renvoie une liste d’objets. Aucun mécanisme de pagination n’est présent ici. À date identique, ce tri seul ne garantit pas un départage par id.

**G — Erreurs possibles et limites.** 404 si le parent est absent ou archivé ; liste vide 200 si le parent existe sans commentaire. Les erreurs SQL de liste ne sont pas toutes capturées localement.

**H — Effets sur la base.** Lecture, sans commit de création. Ne pas confondre le nombre de lignes retournées et le nombre de requêtes nécessaires à leurs représentations.

**I — Exemple réel et fonctions.** [MAH-F0156 — get_story_comments](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0156). Le chemin et la ligne actuels figurent dans la correspondance, avec l’empreinte du fichier.

**J — Formulation orale.** « Une collection vide n’est pas un dossier absent. Le contrôle du parent et la lecture des commentaires répondent à deux questions. »

<a id="famille-05"></a>

### Famille 05 — Compter les associations

**A — Objectif et explication simple.** Calculer le total des likes et l’état personnel du compte pour une cible choisie.

**B — Syntaxe Python utilisée ou réduction fidèle.**

```python
query = model.query.filter(predicate)
total = query.count()
liked_by_me = query.filter_by(user_id=user_id).first() is not None
```

**C — Mécanisme et déroulement.** Les deux lectures ne sont pas un unique instantané HTTP universel ; une autre transaction peut modifier les likes entre les observations selon l’isolation. Une unicité de couple empêche le doublon, pas tout changement concurrent.

**D — Équivalent SQL pédagogique.**

```sql
SELECT COUNT(*) FROM comment_likes WHERE comment_id = :comment_id;
SELECT * FROM comment_likes
WHERE comment_id = :comment_id AND user_id = :user_id LIMIT 1;
```

**E — Tables et colonnes.** CommentLike.comment_id/user_id ou Vote.story_id/user_id selon le kind interne.

**F — Résultat et moment de chargement.** Un entier pour le total et un booléen pour la présence d’une association personnelle. Query.count est une opération de lecture, souvent compilée avec une sous-requête ; le SQL donné est un équivalent pédagogique.

**G — Erreurs possibles et limites.** Erreur SQL propagée au try de handle_like ; 401/403/404 et incompatibilité historique sont contrôlés avant ce calcul dans ce parcours.

**H — Effets sur la base.** Aucun incrément d’une colonne likes dans ces deux tables ; le nombre est dérivé des lignes.

**I — Exemple réel et fonctions.** [MAH-F0172 — like_state](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0172). Le chemin et la ligne actuels figurent dans la correspondance, avec l’empreinte du fichier.

**J — Formulation orale.** « Je compte des associations et je cherche celle du compte courant. Le compteur affiché vient de la base, pas d’un clic ajouté localement. »

<a id="famille-06"></a>

### Famille 06 — Précontrôler une unicité

**A — Objectif et explication simple.** Fournir un refus compréhensible avant de tenter de créer un pseudo ou e-mail déjà utilisé.

**B — Syntaxe Python utilisée ou réduction fidèle.**

```python
exists = User.query.filter_by(username=username).first()
```

**C — Mécanisme et déroulement.** La route garde deux contraintes UNIQUE et reconnaît les conflits métier au moment de l’écriture. Le contrôle préalable d’inscription retourne 400, pas le 409 utilisé pour les likes.

**D — Équivalent SQL pédagogique.**

```sql
SELECT * FROM users WHERE username = :username LIMIT 1;
```

**E — Tables et colonnes.** users.username et, dans une seconde requête de la route, users.email.

**F — Résultat et moment de chargement.** Un compte existant ou None. L’absence au moment du SELECT ne réserve pas le pseudo : deux transactions peuvent observer la même absence.

**G — Erreurs possibles et limites.** IntegrityError sur UNIQUE, FK ou NOT NULL n’ont pas toutes la même signification. is_unique_conflict doit reconnaître la contrainte attendue avant de convertir l’erreur en doublon.

**H — Effets sur la base.** Le SELECT seul n’insère ni ne verrouille une réservation de pseudo. L’INSERT arrive lors du flush implicite du commit.

**I — Exemple réel et fonctions.** [MAH-F0207 — register_user](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0207). Le chemin et la ligne actuels figurent dans la correspondance, avec l’empreinte du fichier.

**J — Formulation orale.** « Le précontrôle améliore le message. La contrainte SQL reste décisive si un concurrent gagne entre la lecture et l’insertion. »

<a id="famille-07"></a>

### Famille 07 — Construire puis ajouter un objet

**A — Objectif et explication simple.** Préparer un commentaire attribué au compte relu côté serveur.

**B — Syntaxe Python utilisée ou réduction fidèle.**

```python
row = Comment(story_id=story_id, user_id=user.id, username=user.username, text=text)
db.session.add(row)
db.session.commit()
```

**C — Mécanisme et déroulement.** L’auteur et le pseudo viennent de la Session, pas de champs JSON libres. required_text valide le texte et sa taille UTF-8. La réponse de création demande 201.

**D — Équivalent SQL pédagogique.**

```sql
INSERT INTO comments (story_id, user_id, username, text, likes, created_at)
VALUES (:story_id, :user_id, :username, :text, :likes, :created_at);
-- Puis validation de transaction par le pilote.
```

**E — Tables et colonnes.** comments et ses références vers stories/users ; username est une copie de texte.

**F — Résultat et moment de chargement.** Le constructeur crée un objet transitoire ; add le fait suivre par la Session. Le flush écrit et peut affecter id/defaults ; commit valide. Le constructeur et add ne sont pas à eux seuls un INSERT durable.

**G — Erreurs possibles et limites.** Validation 400 ; session 401/403 ; parent indisponible 404 ; erreur d’écriture gérée 500 avec rollback. Une lecture de sérialisation après commit peut encore échouer sans annuler le commit réussi.

**H — Effets sur la base.** INSERT au flush ; FK, NOT NULL et types s’appliquent dans le moteur. La méthode to_dict ne valide pas elle-même cette transaction.

**I — Exemple réel et fonctions.** [MAH-F0157 — post_story_comment](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0157). Le chemin et la ligne actuels figurent dans la correspondance, avec l’empreinte du fichier.

**J — Formulation orale.** « Je crée un objet, je le prépare dans la Session, puis je valide l’écriture ; je n’annonce pas le succès dès la construction. »

<a id="famille-08"></a>

### Famille 08 — Modifier un objet suivi

**A — Objectif et explication simple.** Suspendre un membre en conservant son compte et ses contributions.

**B — Syntaxe Python utilisée ou réduction fidèle.**

```python
user.is_banned = True
payload = admin_user_to_dict(user)
db.session.commit()
```

**C — Mécanisme et déroulement.** La cible a été relue avec populate_existing et une demande de verrou. Le payload est préparé avant commit. Aucun DELETE n’est requis, malgré l’ancienne variante HTTP DELETE par pseudo.

**D — Équivalent SQL pédagogique.**

```sql
UPDATE users SET is_banned = :banned WHERE id = :id;
```

**E — Tables et colonnes.** users.is_banned sur la PK choisie ; les comptes administrateurs sont protégés par un refus applicatif.

**F — Résultat et moment de chargement.** L’affectation change l’état Python de l’objet suivi ; l’UPDATE est préparé au flush s’il y a une modification utile. Déjà banni reste un succès explicite de la route, sans promesse d’un nouvel UPDATE identique.

**G — Erreurs possibles et limites.** 404 cible absente ; 409 ADMIN_PROTECTED ; 500 sur erreur SQL gérée, avec rollback. L’absence d’une route de débannissement ne doit pas être remplacée par une opération inventée.

**H — Effets sur la base.** Mise à jour d’un booléen, pas effacement de lignes. La disponibilité d’un verrou dépend du dialecte.

**I — Exemple réel et fonctions.** [MAH-F0154 — ban_user_account](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0154). Le chemin et la ligne actuels figurent dans la correspondance, avec l’empreinte du fichier.

**J — Formulation orale.** « Bannir change un état vérifié aux prochains accès authentifiés ; cela ne supprime ni les contenus ni toutes les copies de cookies. »

<a id="famille-09"></a>

### Famille 09 — Envoyer un UPDATE arithmétique

**A — Objectif et explication simple.** Ajouter une mention au compteur historique sans remplacer une valeur concurrente par un calcul Python ancien.

**B — Syntaxe Python utilisée ou réduction fidèle.**

```python
stmt = update(Theory).where(Theory.id == theory.id).values(likes=Theory.likes + 1)
result = db.session.execute(stmt.execution_options(synchronize_session=False))
db.session.refresh(theory)
```

**C — Mécanisme et déroulement.** synchronize_session=False évite une synchronisation automatique de cette opération ; refresh explicite rend le compteur disponible. Ce compteur n’identifie pas les comptes et autorise des clics répétés.

**D — Équivalent SQL pédagogique.**

```sql
UPDATE theories SET likes = likes + 1 WHERE id = :theory_id;
SELECT * FROM theories WHERE id = :theory_id;
```

**E — Tables et colonnes.** theories.likes et id ; le parent actif est contrôlé avant l’écriture.

**F — Résultat et moment de chargement.** update/where/values construisent ; Session.execute envoie le DML dans la transaction. rowcount sert au refus de cible absente. refresh relit l’objet pour préparer le résultat.

**G — Erreurs possibles et limites.** 404 pour théorie/parent absent ou rowcount zéro ; rollback si échec géré. La borne maximale d’un compteur et sa contention dépendent du type/moteur.

**H — Effets sur la base.** UPDATE exécuté avant commit, puis SELECT de rafraîchissement, puis validation. Cela réduit la perte d’incrément, sans imposer un like unique par personne.

**I — Exemple réel et fonctions.** [MAH-F0204 — like_theory](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0204). Le chemin et la ligne actuels figurent dans la correspondance, avec l’empreinte du fichier.

**J — Formulation orale.** « Le calcul likes + 1 se fait dans le moteur. C’est différent d’une association individuelle comme CommentLike. »

<a id="famille-10"></a>

### Famille 10 — Retirer une association personnelle

**A — Objectif et explication simple.** Supprimer seulement le like du compte authentifié, sans supprimer les autres likes de la cible.

**B — Syntaxe Python utilisée ou réduction fidèle.**

```python
stmt = delete(model).where(predicate, model.user_id == user.id)
result = db.session.execute(stmt)
```

**C — Mécanisme et déroulement.** Cette suppression Core/ORM en masse n’est pas Session.delete sur un objet individuel. Le filtrage appartient à l’instruction ; le contexte HTTP DELETE n’en déduit pas les permissions.

**D — Équivalent SQL pédagogique.**

```sql
DELETE FROM comment_likes
WHERE comment_id = :comment_id AND user_id = :authenticated_user_id;
```

**E — Tables et colonnes.** comment_likes ou votes ; filtre sur cible et compte conjointement.

**F — Résultat et moment de chargement.** execute produit un résultat DML ; rowcount attendu 0 ou 1. changed=False signifie qu’aucune association personnelle n’a été supprimée. La cible et le compte restent.

**G — Erreurs possibles et limites.** rowcount inattendu déclenche SQLAlchemyError ; le try commun rollback puis 500. Les refus d’authentification et d’archive interviennent avant.

**H — Effets sur la base.** DELETE au execute, validation au commit. Aucune soustraction automatique du compteur historique Comment.likes.

**I — Exemple réel et fonctions.** [MAH-F0173 — handle_like](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0173). Le chemin et la ligne actuels figurent dans la correspondance, avec l’empreinte du fichier.

**J — Formulation orale.** « Je retire une ligne précisément désignée par les deux identifiants, pas tous les likes du commentaire. »

<a id="famille-11"></a>

### Famille 11 — Précharger des relations

**A — Objectif et explication simple.** Lire le contexte des signalements sans multiplier les chargements de leurs parents à chaque carte.

**B — Syntaxe Python utilisée ou réduction fidèle.**

```python
rows = Report.query.options(joinedload(Report.comment).joinedload(Comment.story).joinedload(Story.category)).order_by(Report.created_at.desc(), Report.id.desc()).all()
```

**C — Mécanisme et déroulement.** Les cartes exposent motif, commentaire et contexte seulement aux administrateurs. Un outer join conserve le signalement même si une ancienne référence est incohérente ; cela ne répare pas cette incohérence.

**D — Équivalent SQL pédagogique.**

```sql
SELECT r.*, c.*, s.*, k.* FROM reports AS r
LEFT OUTER JOIN comments AS c ON c.id = r.comment_id
LEFT OUTER JOIN stories AS s ON s.id = c.story_id
LEFT OUTER JOIN categories AS k ON k.id = s.category_id
ORDER BY r.created_at DESC, r.id DESC;
```

**E — Tables et colonnes.** reports → comments → stories → categories ; les relations sont scalaires dans cette chaîne.

**F — Résultat et moment de chargement.** options configure le chargement ; all exécute la lecture. Les alias et colonnes exactes générés diffèrent du SQL schématique. Les relations scalaires absentes sont représentées par None dans le traitement.

**G — Erreurs possibles et limites.** 401/403 au contrôle d’accès ; SQLAlchemyError gérée 500. Un joinedload de collection demanderait d’autres précautions de déduplication ; ne pas les attribuer arbitrairement à cette chaîne scalaire.

**H — Effets sur la base.** SELECT avec chargement anticipé, pas une création de FK et pas une publication publique.

**I — Exemple réel et fonctions.** [MAH-F0166 — get_admin_reports](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0166). Le chemin et la ligne actuels figurent dans la correspondance, avec l’empreinte du fichier.

**J — Formulation orale.** « La FK garantit le lien quand elle est active ; joinedload choisit comment je charge les objets liés. »

<a id="famille-12"></a>

### Famille 12 — Naviguer dans une relation

**A — Objectif et explication simple.** Construire la lecture administrative d’un dossier avec ses contributions conservées.

**B — Syntaxe Python utilisée ou réduction fidèle.**

```python
comments = [comment_to_dict(row) for row in story.comments]
```

**C — Mécanisme et déroulement.** La route administrative peut consulter une archive ; les routes publiques de contributions utilisent leur propre filtre d’activité. La relation brute n’est pas un contrôle de visibilité.

**D — Équivalent SQL pédagogique.**

```sql
SELECT * FROM comments WHERE story_id = :story_id;
-- Des COUNT peuvent suivre dans comment_to_dict.
```

**E — Tables et colonnes.** Story.comments, Story.theories et Story.cold_case_updates dans la vue détaillée.

**F — Résultat et moment de chargement.** Si une collection n’est pas chargée, sa navigation peut déclencher un SELECT lazy ; sinon elle réutilise les objets disponibles. Le guide ne promet pas une requête par accès sans observer l’état de la Session.

**G — Erreurs possibles et limites.** Objet détaché/Session absente, connexion perdue ou erreurs de sérialisation possibles. Les collections ne sont pas paginées dans ce chemin.

**H — Effets sur la base.** Lectures implicites possibles, sans ajout de contenu. Retirer un enfant d’une collection delete-orphan serait une autre opération, pouvant supprimer au flush.

**I — Exemple réel et fonctions.** [MAH-F0146 — get_admin_story](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0146). Le chemin et la ligne actuels figurent dans la correspondance, avec l’empreinte du fichier.

**J — Formulation orale.** « Une relation me permet de naviguer ; elle peut coûter une lecture et ne décide pas qui est autorisé à voir le contenu. »

<a id="famille-13"></a>

### Famille 13 — Demander un verrou et une relecture

**A — Objectif et explication simple.** Coordonner une contribution avec une transition d’archive du même dossier parent.

**B — Syntaxe Python utilisée ou réduction fidèle.**

```python
row = Story.query.filter_by(id=identifier, archived_at=None).populate_existing().with_for_update().first()
```

**C — Mécanisme et déroulement.** La branche lock=False des lectures ne demande pas ce verrou. Les écrivains de contribution utilisent lock=True ; l’archivage demande aussi le verrou de ce parent.

**D — Équivalent SQL pédagogique.**

```sql
SELECT * FROM stories
WHERE id = :id AND archived_at IS NULL FOR UPDATE;
-- Forme MySQL/InnoDB illustrative ; pas le SQL SQLite.
```

**E — Tables et colonnes.** stories.id et archived_at ; autres colonnes rechargées pour l’objet.

**F — Résultat et moment de chargement.** populate_existing demande de rafraîchir l’objet déjà présent ; with_for_update configure une lecture verrouillante sur les moteurs compatibles. first provoque la lecture, pas with_for_update seul.

**G — Erreurs possibles et limites.** Contention, deadlock, timeout et erreurs SQL possibles ; le helper rollback puis abort(500). SQLite n’implémente pas FOR UPDATE comme InnoDB.

**H — Effets sur la base.** Une lecture peut acquérir un verrou transactionnel côté moteur compatible. La durée est liée à la transaction, pas à la seule durée de la ligne Python.

**I — Exemple réel et fonctions.** [MAH-F0200 — get_active_story](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0200). Le chemin et la ligne actuels figurent dans la correspondance, avec l’empreinte du fichier.

**J — Formulation orale.** « Je demande au moteur de coordonner les écrivains sur le parent ; je ne prétends pas que SQLite a validé ce verrou MySQL. »

<a id="famille-14"></a>

### Famille 14 — Exécuter un SELECT Core et lire des mappings

**A — Objectif et explication simple.** Calculer un état comparable du dossier et de ses six familles de dépendances avant une purge.

**B — Syntaxe Python utilisée ou réduction fidèle.**

```python
stmt = sa.select(Story.__table__).where(Story.id == story_id)
row = db.session.execute(stmt).mappings().first()
```

**C — Mécanisme et déroulement.** Les dépendances sont triées par PK, limitées à MAX_DEPENDENCIES+1 par lecture et comparées à une borne globale. Un hash de l’état sert à détecter une modification entre requêtes de confirmation.

**D — Équivalent SQL pédagogique.**

```sql
SELECT * FROM stories WHERE id = :story_id;
-- FOR UPDATE est ajouté dans le chemin lock=True sur dialecte compatible.
```

**E — Tables et colonnes.** stories et les familles comments/theories/votes/updates/reports/comment_likes.

**F — Résultat et moment de chargement.** select/where construisent. execute envoie la lecture. mappings adapte les lignes en RowMapping ; first consomme au plus le premier résultat disponible. Contrairement à Query.first, Result.first n’ajoute pas lui-même LIMIT au SQL construit.

**G — Erreurs possibles et limites.** 404 dossier absent ; 409 révision invalide ou graphe trop volumineux ; pas de copie du contenu du graphe dans un journal ou un reçu persistant.

**H — Effets sur la base.** Lecture de données et calcul en mémoire ; la construction de mappings n’exécute pas une deuxième instruction SQL indépendante.

**I — Exemple réel et fonctions.** [MAH-F0190 — snapshot](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0190). Le chemin et la ligne actuels figurent dans la correspondance, avec l’empreinte du fichier.

**J — Formulation orale.** « Je distingue l’instruction, son exécution et la manière de lire ses résultats. Le hash compare un état, pas une permission. »

<a id="famille-15"></a>

### Famille 15 — Joindre et détecter des orphelins

**A — Objectif et explication simple.** Refuser une purge si d’anciennes écritures ont laissé des références incohérentes.

**B — Syntaxe Python utilisée ou réduction fidèle.**

```python
stmt = sa.select(Report.id).outerjoin(Comment, Report.comment_id == Comment.id).where(Comment.id.is_(None)).limit(1)
found = db.session.execute(stmt).first()
```

**C — Mécanisme et déroulement.** Le parcours vérifie aussi les FK, la structure de reports et les actions CASCADE nécessaires. Sur MySQL il lit les moteurs et foreign_key_checks ; sur SQLite il vérifie le PRAGMA.

**D — Équivalent SQL pédagogique.**

```sql
SELECT r.id FROM reports AS r
LEFT OUTER JOIN comments AS c ON c.id = r.comment_id
WHERE c.id IS NULL LIMIT 1;
```

**E — Tables et colonnes.** reports.comment_id → comments.id ; un second contrôle couvre les parents Comment et User des likes.

**F — Résultat et moment de chargement.** Une ligne signale au moins un orphelin ; None signifie que ce contrôle n’en a pas trouvé. L’absence d’orphelin dans ces relations ne constitue pas un audit complet de toutes les données.

**G — Erreurs possibles et limites.** Purge refusée 503 PURGE_UNAVAILABLE si préconditions absentes. L’inspection du schéma et le texte SQL constant ne sont pas une preuve d’exécution MySQL dans ce lot.

**H — Effets sur la base.** Lectures et inspections seulement, pas de réparation des lignes. Aucune base n’est effectivement inspectée pour rédiger ce guide.

**I — Exemple réel et fonctions.** [MAH-F0189 — require_integrity](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0189). Le chemin et la ligne actuels figurent dans la correspondance, avec l’empreinte du fichier.

**J — Formulation orale.** « Je vérifie ce dont la purge dépend avant de supprimer. Si je ne peux pas établir l’intégrité attendue, je refuse. »

<a id="famille-16"></a>

### Famille 16 — Comparer puis réserver une révision

**A — Objectif et explication simple.** Éviter une purge fondée sur une ancienne confirmation en réservant la révision attendue.

**B — Syntaxe Python utilisée ou réduction fidèle.**

```python
stmt = sa.update(Story.__table__).where(Story.id == story_id, Story.management_revision == expected_revision, Story.archived_at.is_not(None)).values(management_revision=reserved)
result = db.session.execute(stmt)
```

**C — Mécanisme et déroulement.** La valeur reserved est un nouvel UUID ; les DELETE suivants et leurs comptages restent dans la transaction. Aucun hash du graphe n’est écrit dans la base comme journal.

**D — Équivalent SQL pédagogique.**

```sql
UPDATE stories SET management_revision = :reserved
WHERE id = :story_id AND management_revision = :expected_revision
AND archived_at IS NOT NULL;
```

**E — Tables et colonnes.** stories.id, management_revision et archived_at ; comparaison de l’état dans le WHERE.

**F — Résultat et moment de chargement.** rowcount doit valoir exactement 1. Ce compare-and-swap complète les contrôles de jeton, ETag, hash et verrou ; il n’est pas un remplacement de leurs préconditions.

**G — Erreurs possibles et limites.** rowcount différent : 412. Conflits/erreurs de moteur : traitement PurgeError/SQLAlchemyError dans run_deletion_action. Une erreur de commit finale peut laisser une issue inconnue.

**H — Effets sur la base.** UPDATE effectif à execute, annulable avant commit si transaction moteur valide. La purge ultérieure reste conditionnée à la révision réservée.

**I — Exemple réel et fonctions.** [MAH-F0198 — delete_story](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0198). Le chemin et la ligne actuels figurent dans la correspondance, avec l’empreinte du fichier.

**J — Formulation orale.** « La condition est vérifiée dans l’écriture SQL elle-même : si la révision attendue n’est plus là, je ne peux pas continuer. »

<a id="famille-17"></a>

### Famille 17 — Supprimer avec une sous-requête

**A — Objectif et explication simple.** Retirer les signalements et likes associés aux seuls commentaires du dossier purgé.

**B — Syntaxe Python utilisée ou réduction fidèle.**

```python
predicate = Report.comment_id.in_(sa.select(Comment.id).where(Comment.story_id == story_id))
result = db.session.execute(sa.delete(Report.__table__).where(predicate))
```

**C — Mécanisme et déroulement.** Les signalements et likes sont retirés avant comments afin que la sous-requête retrouve encore les parents. Théories, votes, mises à jour et commentaires sont ensuite retirés, puis Story.

**D — Équivalent SQL pédagogique.**

```sql
DELETE FROM reports WHERE comment_id IN
(SELECT id FROM comments WHERE story_id = :story_id);
```

**E — Tables et colonnes.** reports.comment_id et comments.story_id ; même forme pour comment_likes.

**F — Résultat et moment de chargement.** La sous-requête est construite dans l’expression, pas évaluée en Python avant le DELETE. rowcount est comparé au nombre connu du snapshot pour chaque famille.

**G — Erreurs possibles et limites.** Comptages différents : 409 et rollback. Une suppression en masse ne parcourt pas les callbacks/cascades ORM par objet ; les contrôles et contraintes de la base restent déterminants.

**H — Effets sur la base.** DML dans la même transaction ; vérifications finales par lots de 500 ids avant commit. Ne pas déduire que db.session.delete(story) serait l’implémentation de ce parcours.

**I — Exemple réel et fonctions.** [MAH-F0198 — delete_story](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0198). Le chemin et la ligne actuels figurent dans la correspondance, avec l’empreinte du fichier.

**J — Formulation orale.** « Je cible les enfants par leur vraie relation au dossier et je vérifie les quantités ; je ne confonds pas id de dossier et id de commentaire. »

<a id="famille-18"></a>

### Famille 18 — Créer le schéma et peupler une destination neuve

**A — Objectif et explication simple.** Distinguer un seed de fixture, une création de tables et la migration d’une ancienne base.

**B — Syntaxe Python utilisée ou réduction fidèle.**

```python
db.create_all()
# Puis objets User/Category/Story, add/add_all, flush et commit dans le lanceur approprié.
```

**C — Mécanisme et déroulement.** Le kit démarre un schéma synthétique en mémoire. initialize persistant prépare un nouveau dossier puis le renomme seulement après validation ; serve ne recrée pas la base existante.

**D — Équivalent SQL pédagogique.**

```sql
-- CREATE TABLE est émis par les métadonnées si nécessaire.
-- Les INSERT de peuplement sont séparés ; aucun récit n’apparaît par magie dans un CREATE TABLE.
```

**E — Tables et colonnes.** Les dix tables actuelles ; le kit et le mode persistant ajoutent explicitement leurs comptes, catégories et histoires.

**F — Résultat et moment de chargement.** create_all n’est pas un parcours Alembic et ne convertit pas un ancien schéma. Le seed mémoire et initialize persistant ont des préconditions et des destinations différentes.

**G — Erreurs possibles et limites.** Refus si destination persistante déjà présente ; erreurs de configuration et schéma possibles. Aucun de ces lanceurs n’est importé ou lancé pendant ce lot.

**H — Effets sur la base.** DDL et INSERT seulement lors d’une exécution future autorisée du bon outil ; documentation de lecture ici.

**I — Exemple réel et fonctions.** [MAH-F0113 — seed](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0113) et [MAH-F0083 — initialize](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0083). Le chemin et la ligne actuels figurent dans la correspondance, avec l’empreinte du fichier.

**J — Formulation orale.** « Créer les tables, les remplir et migrer une installation sont trois opérations distinctes, avec des risques différents. »

## Paramètres liés et texte SQL constant

Les comparaisons Model.column == valeur, filter_by, where, values et les constructions de l’ORM transmettent les valeurs au pilote comme paramètres selon le dialecte. Elles évitent de fabriquer une clause SQL en collant le texte fourni par l’utilisateur. Ce mécanisme ne protège pas une autorisation absente, une recherche trop coûteuse ou du SQL textuel interpolé à tort.

Dans require_integrity, les requêtes textuelles de métadonnées et @@foreign_key_checks sont des chaînes constantes du code, pas des bouts de JSON insérés dans une requête. Dans inspect_database du mode persistant, les noms de tables concaténés proviennent des métadonnées validées, et les valeurs de lignes utilisent des paramètres DBAPI. Cette provenance doit être expliquée ; l’expression « ORM » n’est pas un certificat général d’absence d’injection pour tout texte SQL futur.

## Coûts de lecture observables statiquement

get_stories lit la liste puis compte Vote pour chaque dossier : la structure comporte un décompte par élément. comment_to_dict compte les signalements et parfois les likes de chaque commentaire. get_admin_story accède à des collections qui peuvent être chargées à la demande. Les listes n’introduisent pas de pagination dans ces fonctions. Le nombre exact de requêtes dépend du nombre d’éléments, de la Session et du dialecte ; aucune mesure SQL n’est inventée.

get_admin_reports configure un joinedload scalaire sur les trois parents de contexte. Ce choix réduit certains chargements différés sans changer les règles de permissions ni la FK. La source officielle distingue stratégies lazy et eager ; la stratégie concrète d’un objet déjà chargé reste à considérer. [Chargement des relations SQLAlchemy](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html).

## Catalogue exhaustif des formes repérées dans le périmètre

Les repères REQ21_5 identifient ce relevé documentaire ; ce ne sont pas de nouveaux identifiants de fonction du référentiel 6H.21.1. L’AST repère les appels SQLAlchemy/ORM, migrations et opérations DBAPI pertinentes. Les homonymes dict.get, mises à jour de dictionnaires et jointures de chemins sont exclus. Des appels chaînés figurent séparément ; les appels implicites ne peuvent pas être comptés par cet inventaire syntaxique.

Le fichier INVENTAIRE_STATIQUE.json conserve pour chaque entrée le chemin, la portée, les lignes, arguments et mots-clés. Le tableau ci-dessous rend toutes les formes repérées lisibles sans installer ce JSON dans le projet. « Paramètres » présente les expressions passées par le code, pas une capture de valeurs privées.

**480 sites d’appel repérés dans 29 modules Python ; aucun exécuté.**

| Repère | Fichier et ligne | Fonction / identifiant | Expression et paramètres | Effet et résultat à interpréter |
|---|---|---|---|---|
| REQ21_5-0001 | `backend/api/v1/views/admin_stories.py:26` | `archive_admin_required.wrapped / MAH-F0142` | `db.session.rollback()` | Fin/annulation de transaction en cours et remise en état de la Session ; pas annulation d’un commit déjà réussi. |
| REQ21_5-0002 | `backend/api/v1/views/admin_stories.py:37` | `admin_story_data / MAH-F0143` | `Vote.query.filter_by(story_id=story.id)` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0003 | `backend/api/v1/views/admin_stories.py:37` | `admin_story_data / MAH-F0143` | `Vote.query.filter_by(story_id=story.id).count()` | Query.count exécute un décompte ; ne pas confondre avec la construction func.count. |
| REQ21_5-0004 | `backend/api/v1/views/admin_stories.py:59` | `get_admin_stories / MAH-F0145` | `query.filter(Story.archived_at.is_(None))` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0005 | `backend/api/v1/views/admin_stories.py:61` | `get_admin_stories / MAH-F0145` | `query.filter(Story.archived_at.is_not(None))` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0006 | `backend/api/v1/views/admin_stories.py:62` | `get_admin_stories / MAH-F0145` | `query.order_by(Story.created_at.desc(), Story.id.desc())` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0007 | `backend/api/v1/views/admin_stories.py:62` | `get_admin_stories / MAH-F0145` | `query.order_by(Story.created_at.desc(), Story.id.desc()).all()` | Consomme un Query ou un résultat : voir l’expression. Query terminal peut exécuter ; Result consomme une exécution antérieure. |
| REQ21_5-0008 | `backend/api/v1/views/admin_stories.py:65` | `get_admin_stories / MAH-F0145` | `db.session.rollback()` | Fin/annulation de transaction en cours et remise en état de la Session ; pas annulation d’un commit déjà réussi. |
| REQ21_5-0009 | `backend/api/v1/views/admin_stories.py:75` | `get_admin_story / MAH-F0146` | `db.session.get(Story, story_id)` | Identité ORM ou None ; SELECT si l’état de Session l’exige. |
| REQ21_5-0010 | `backend/api/v1/views/admin_stories.py:88` | `get_admin_story / MAH-F0146` | `db.session.rollback()` | Fin/annulation de transaction en cours et remise en état de la Session ; pas annulation d’un commit déjà réussi. |
| REQ21_5-0011 | `backend/api/v1/views/admin_stories.py:99` | `set_story_archive / MAH-F0147` | `Story.query.filter_by(id=story_id)` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0012 | `backend/api/v1/views/admin_stories.py:99` | `set_story_archive / MAH-F0147` | `Story.query.filter_by(id=story_id).populate_existing()` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0013 | `backend/api/v1/views/admin_stories.py:99` | `set_story_archive / MAH-F0147` | `Story.query.filter_by(id=story_id).populate_existing().with_for_update()` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0014 | `backend/api/v1/views/admin_stories.py:99` | `set_story_archive / MAH-F0147` | `Story.query.filter_by(id=story_id).populate_existing().with_for_update().first()` | Consomme un Query ou un résultat : voir l’expression. Query terminal peut exécuter ; Result consomme une exécution antérieure. |
| REQ21_5-0015 | `backend/api/v1/views/admin_stories.py:106` | `set_story_archive / MAH-F0147` | `db.session.flush()` | DML envoyé dans la transaction ; contraintes et identifiants générés ; pas commit. |
| REQ21_5-0016 | `backend/api/v1/views/admin_stories.py:108` | `set_story_archive / MAH-F0147` | `db.session.commit()` | Flush requis puis validation ; résultat réseau ultérieur distinct de la réussite du commit. |
| REQ21_5-0017 | `backend/api/v1/views/admin_stories.py:111` | `set_story_archive / MAH-F0147` | `db.session.rollback()` | Fin/annulation de transaction en cours et remise en état de la Session ; pas annulation d’un commit déjà réussi. |
| REQ21_5-0018 | `backend/api/v1/views/admin_users_support.py:24` | `ban_user_account / MAH-F0154` | `User.query.filter_by(id=user_id)` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0019 | `backend/api/v1/views/admin_users_support.py:26` | `ban_user_account / MAH-F0154` | `User.query.filter_by(username=username)` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0020 | `backend/api/v1/views/admin_users_support.py:27` | `ban_user_account / MAH-F0154` | `query.populate_existing()` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0021 | `backend/api/v1/views/admin_users_support.py:27` | `ban_user_account / MAH-F0154` | `query.populate_existing().with_for_update()` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0022 | `backend/api/v1/views/admin_users_support.py:27` | `ban_user_account / MAH-F0154` | `query.populate_existing().with_for_update().first()` | Consomme un Query ou un résultat : voir l’expression. Query terminal peut exécuter ; Result consomme une exécution antérieure. |
| REQ21_5-0023 | `backend/api/v1/views/admin_users_support.py:43` | `ban_user_account / MAH-F0154` | `db.session.commit()` | Flush requis puis validation ; résultat réseau ultérieur distinct de la réussite du commit. |
| REQ21_5-0024 | `backend/api/v1/views/admin_users_support.py:45` | `ban_user_account / MAH-F0154` | `db.session.rollback()` | Fin/annulation de transaction en cours et remise en état de la Session ; pas annulation d’un commit déjà réussi. |
| REQ21_5-0025 | `backend/api/v1/views/comments.py:20` | `comment_to_dict / MAH-F0155` | `CommentLike.query.filter_by(comment_id=comment.id)` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0026 | `backend/api/v1/views/comments.py:20` | `comment_to_dict / MAH-F0155` | `CommentLike.query.filter_by(comment_id=comment.id).count()` | Query.count exécute un décompte ; ne pas confondre avec la construction func.count. |
| REQ21_5-0027 | `backend/api/v1/views/comments.py:22` | `comment_to_dict / MAH-F0155` | `Report.query.filter_by(comment_id=comment.id)` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0028 | `backend/api/v1/views/comments.py:22` | `comment_to_dict / MAH-F0155` | `Report.query.filter_by(comment_id=comment.id).count()` | Query.count exécute un décompte ; ne pas confondre avec la construction func.count. |
| REQ21_5-0029 | `backend/api/v1/views/comments.py:41` | `get_story_comments / MAH-F0156` | `Comment.query.filter_by(story_id=story_id)` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0030 | `backend/api/v1/views/comments.py:41` | `get_story_comments / MAH-F0156` | `Comment.query.filter_by(story_id=story_id).order_by(Comment.created_at.asc())` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0031 | `backend/api/v1/views/comments.py:41` | `get_story_comments / MAH-F0156` | `Comment.query.filter_by(story_id=story_id).order_by(Comment.created_at.asc()).all()` | Consomme un Query ou un résultat : voir l’expression. Query terminal peut exécuter ; Result consomme une exécution antérieure. |
| REQ21_5-0032 | `backend/api/v1/views/comments.py:77` | `post_story_comment / MAH-F0157` | `Comment(story_id=story_id, user_id=user.id, username=user.username, text=text)` | Objet en mémoire ; aucun INSERT par cette seule construction. Defaults/PK possibles au flush. |
| REQ21_5-0033 | `backend/api/v1/views/comments.py:88` | `post_story_comment / MAH-F0157` | `db.session.add(new_comment)` | Inscription d’objet(s) dans la Session ; écriture au flush, pas validation durable. |
| REQ21_5-0034 | `backend/api/v1/views/comments.py:89` | `post_story_comment / MAH-F0157` | `db.session.commit()` | Flush requis puis validation ; résultat réseau ultérieur distinct de la réussite du commit. |
| REQ21_5-0035 | `backend/api/v1/views/comments.py:91` | `post_story_comment / MAH-F0157` | `db.session.rollback()` | Fin/annulation de transaction en cours et remise en état de la Session ; pas annulation d’un commit déjà réussi. |
| REQ21_5-0036 | `backend/api/v1/views/comments.py:134` | `report_comment / MAH-F0159` | `Report(comment_id=comment.id, reason=reason)` | Objet en mémoire ; aucun INSERT par cette seule construction. Defaults/PK possibles au flush. |
| REQ21_5-0037 | `backend/api/v1/views/comments.py:140` | `report_comment / MAH-F0159` | `db.session.add(report)` | Inscription d’objet(s) dans la Session ; écriture au flush, pas validation durable. |
| REQ21_5-0038 | `backend/api/v1/views/comments.py:141` | `report_comment / MAH-F0159` | `db.session.commit()` | Flush requis puis validation ; résultat réseau ultérieur distinct de la réussite du commit. |
| REQ21_5-0039 | `backend/api/v1/views/comments.py:143` | `report_comment / MAH-F0159` | `db.session.rollback()` | Fin/annulation de transaction en cours et remise en état de la Session ; pas annulation d’un commit déjà réussi. |
| REQ21_5-0040 | `backend/api/v1/views/histoires.py:16` | `get_stories / MAH-F0160` | `Story.query.filter_by(archived_at=None)` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0041 | `backend/api/v1/views/histoires.py:16` | `get_stories / MAH-F0160` | `Story.query.filter_by(archived_at=None).order_by(Story.created_at.desc())` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0042 | `backend/api/v1/views/histoires.py:16` | `get_stories / MAH-F0160` | `Story.query.filter_by(archived_at=None).order_by(Story.created_at.desc()).all()` | Consomme un Query ou un résultat : voir l’expression. Query terminal peut exécuter ; Result consomme une exécution antérieure. |
| REQ21_5-0043 | `backend/api/v1/views/histoires.py:30` | `get_stories / MAH-F0160` | `Vote.query.filter_by(story_id=story.id)` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0044 | `backend/api/v1/views/histoires.py:30` | `get_stories / MAH-F0160` | `Vote.query.filter_by(story_id=story.id).count()` | Query.count exécute un décompte ; ne pas confondre avec la construction func.count. |
| REQ21_5-0045 | `backend/api/v1/views/histoires.py:46` | `get_story_by_slug / MAH-F0161` | `Story.query.filter_by(slug=slug, archived_at=None)` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0046 | `backend/api/v1/views/histoires.py:46` | `get_story_by_slug / MAH-F0161` | `Story.query.filter_by(slug=slug, archived_at=None).first()` | Consomme un Query ou un résultat : voir l’expression. Query terminal peut exécuter ; Result consomme une exécution antérieure. |
| REQ21_5-0047 | `backend/api/v1/views/histoires.py:53` | `get_story_by_slug / MAH-F0161` | `Vote.query.filter_by(story_id=story.id)` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0048 | `backend/api/v1/views/histoires.py:53` | `get_story_by_slug / MAH-F0161` | `Vote.query.filter_by(story_id=story.id).count()` | Query.count exécute un décompte ; ne pas confondre avec la construction func.count. |
| REQ21_5-0049 | `backend/api/v1/views/histoires.py:80` | `post_story_vote / MAH-F0162` | `Vote.query.filter_by(story_id=story_id, user_id=user.id)` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0050 | `backend/api/v1/views/histoires.py:80` | `post_story_vote / MAH-F0162` | `Vote.query.filter_by(story_id=story_id, user_id=user.id).first()` | Consomme un Query ou un résultat : voir l’expression. Query terminal peut exécuter ; Result consomme une exécution antérieure. |
| REQ21_5-0051 | `backend/api/v1/views/histoires.py:90` | `post_story_vote / MAH-F0162` | `Vote(story_id=story_id, user_id=user.id)` | Objet en mémoire ; aucun INSERT par cette seule construction. Defaults/PK possibles au flush. |
| REQ21_5-0052 | `backend/api/v1/views/histoires.py:99` | `post_story_vote / MAH-F0162` | `db.session.add(new_vote)` | Inscription d’objet(s) dans la Session ; écriture au flush, pas validation durable. |
| REQ21_5-0053 | `backend/api/v1/views/histoires.py:100` | `post_story_vote / MAH-F0162` | `db.session.flush()` | DML envoyé dans la transaction ; contraintes et identifiants générés ; pas commit. |
| REQ21_5-0054 | `backend/api/v1/views/histoires.py:101` | `post_story_vote / MAH-F0162` | `Vote.query.filter_by(story_id=story_id)` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0055 | `backend/api/v1/views/histoires.py:101` | `post_story_vote / MAH-F0162` | `Vote.query.filter_by(story_id=story_id).count()` | Query.count exécute un décompte ; ne pas confondre avec la construction func.count. |
| REQ21_5-0056 | `backend/api/v1/views/histoires.py:102` | `post_story_vote / MAH-F0162` | `db.session.commit()` | Flush requis puis validation ; résultat réseau ultérieur distinct de la réussite du commit. |
| REQ21_5-0057 | `backend/api/v1/views/histoires.py:104` | `post_story_vote / MAH-F0162` | `db.session.rollback()` | Fin/annulation de transaction en cours et remise en état de la Session ; pas annulation d’un commit déjà réussi. |
| REQ21_5-0058 | `backend/api/v1/views/histoires.py:112` | `post_story_vote / MAH-F0162` | `db.session.rollback()` | Fin/annulation de transaction en cours et remise en état de la Session ; pas annulation d’un commit déjà réussi. |
| REQ21_5-0059 | `backend/api/v1/views/histoires.py:133` | `get_case_updates / MAH-F0163` | `ColdCaseUpdate.query.filter_by(story_id=case_id)` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0060 | `backend/api/v1/views/histoires.py:133` | `get_case_updates / MAH-F0163` | `ColdCaseUpdate.query.filter_by(story_id=case_id).order_by(ColdCaseUpdate.created_at.asc())` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0061 | `backend/api/v1/views/histoires.py:133` | `get_case_updates / MAH-F0163` | `ColdCaseUpdate.query.filter_by(story_id=case_id).order_by(ColdCaseUpdate.created_at.asc()).all()` | Consomme un Query ou un résultat : voir l’expression. Query terminal peut exécuter ; Result consomme une exécution antérieure. |
| REQ21_5-0062 | `backend/api/v1/views/index.py:69` | `post_report / MAH-F0164` | `db.session.get(target_model, target_value)` | Identité ORM ou None ; SELECT si l’état de Session l’exige. |
| REQ21_5-0063 | `backend/api/v1/views/index.py:76` | `post_report / MAH-F0164` | `Report(comment_id=target_value, reason=values['reason'])` | Objet en mémoire ; aucun INSERT par cette seule construction. Defaults/PK possibles au flush. |
| REQ21_5-0064 | `backend/api/v1/views/index.py:85` | `post_report / MAH-F0164` | `db.session.add(report)` | Inscription d’objet(s) dans la Session ; écriture au flush, pas validation durable. |
| REQ21_5-0065 | `backend/api/v1/views/index.py:86` | `post_report / MAH-F0164` | `db.session.commit()` | Flush requis puis validation ; résultat réseau ultérieur distinct de la réussite du commit. |
| REQ21_5-0066 | `backend/api/v1/views/index.py:88` | `post_report / MAH-F0164` | `db.session.rollback()` | Fin/annulation de transaction en cours et remise en état de la Session ; pas annulation d’un commit déjà réussi. |
| REQ21_5-0067 | `backend/api/v1/views/index.py:114` | `get_admin_reports / MAH-F0166` | `Report.query.options(joinedload(Report.comment).joinedload(Comment.story).joinedload(Story.category))` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0068 | `backend/api/v1/views/index.py:114` | `get_admin_reports / MAH-F0166` | `Report.query.options(joinedload(Report.comment).joinedload(Comment.story).joinedload(Story.category)).order_by(Report.created_at.desc(), Report.id.desc())` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0069 | `backend/api/v1/views/index.py:114` | `get_admin_reports / MAH-F0166` | `Report.query.options(joinedload(Report.comment).joinedload(Comment.story).joinedload(Story.category)).order_by(Report.created_at.desc(), Report.id.desc()).all()` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0070 | `backend/api/v1/views/index.py:115` | `get_admin_reports / MAH-F0166` | `joinedload(Report.comment)` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0071 | `backend/api/v1/views/index.py:115` | `get_admin_reports / MAH-F0166` | `joinedload(Report.comment).joinedload(Comment.story)` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0072 | `backend/api/v1/views/index.py:115` | `get_admin_reports / MAH-F0166` | `joinedload(Report.comment).joinedload(Comment.story).joinedload(Story.category)` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0073 | `backend/api/v1/views/index.py:131` | `get_admin_reports / MAH-F0166` | `db.session.rollback()` | Fin/annulation de transaction en cours et remise en état de la Session ; pas annulation d’un commit déjà réussi. |
| REQ21_5-0074 | `backend/api/v1/views/likes.py:22` | `like_state / MAH-F0172` | `model.query.filter(predicate)` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0075 | `backend/api/v1/views/likes.py:24` | `like_state / MAH-F0172` | `query.count()` | Query.count exécute un décompte ; ne pas confondre avec la construction func.count. |
| REQ21_5-0076 | `backend/api/v1/views/likes.py:24` | `like_state / MAH-F0172` | `query.filter_by(user_id=user_id)` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0077 | `backend/api/v1/views/likes.py:24` | `like_state / MAH-F0172` | `query.filter_by(user_id=user_id).first()` | Consomme un Query ou un résultat : voir l’expression. Query terminal peut exécuter ; Result consomme une exécution antérieure. |
| REQ21_5-0078 | `backend/api/v1/views/likes.py:43` | `handle_like / MAH-F0173` | `db.session.refresh(target)` | SELECT de rafraîchissement d’un objet ; contrôle des attributs suivi. |
| REQ21_5-0079 | `backend/api/v1/views/likes.py:54` | `handle_like / MAH-F0173` | `model.query.filter(*own)` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0080 | `backend/api/v1/views/likes.py:54` | `handle_like / MAH-F0173` | `model.query.filter(*own).first()` | Consomme un Query ou un résultat : voir l’expression. Query terminal peut exécuter ; Result consomme une exécution antérieure. |
| REQ21_5-0081 | `backend/api/v1/views/likes.py:56` | `handle_like / MAH-F0173` | `CommentLike(comment_id=identifier, user_id=user.id)` | Objet en mémoire ; aucun INSERT par cette seule construction. Defaults/PK possibles au flush. |
| REQ21_5-0082 | `backend/api/v1/views/likes.py:56` | `handle_like / MAH-F0173` | `db.session.add(CommentLike(comment_id=identifier, user_id=user.id))` | Inscription d’objet(s) dans la Session ; écriture au flush, pas validation durable. |
| REQ21_5-0083 | `backend/api/v1/views/likes.py:57` | `handle_like / MAH-F0173` | `db.session.flush()` | DML envoyé dans la transaction ; contraintes et identifiants générés ; pas commit. |
| REQ21_5-0084 | `backend/api/v1/views/likes.py:62` | `handle_like / MAH-F0173` | `db.session.execute(delete(model).where(*own))` | Connexion, exécution ou inspection : SQL/effet exact dépend de l’expression et du contexte ; aucun appel effectué ici. |
| REQ21_5-0085 | `backend/api/v1/views/likes.py:62` | `handle_like / MAH-F0173` | `delete(model)` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0086 | `backend/api/v1/views/likes.py:62` | `handle_like / MAH-F0173` | `delete(model).where(*own)` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0087 | `backend/api/v1/views/likes.py:69` | `handle_like / MAH-F0173` | `db.session.commit()` | Flush requis puis validation ; résultat réseau ultérieur distinct de la réussite du commit. |
| REQ21_5-0088 | `backend/api/v1/views/likes.py:72` | `handle_like / MAH-F0173` | `db.session.rollback()` | Fin/annulation de transaction en cours et remise en état de la Session ; pas annulation d’un commit déjà réussi. |
| REQ21_5-0089 | `backend/api/v1/views/likes.py:80` | `handle_like / MAH-F0173` | `db.session.rollback()` | Fin/annulation de transaction en cours et remise en état de la Session ; pas annulation d’un commit déjà réussi. |
| REQ21_5-0090 | `backend/api/v1/views/permissions.py:23` | `get_authenticated_user / MAH-F0177` | `db.session.get(User, user_id)` | Identité ORM ou None ; SELECT si l’état de Session l’exige. |
| REQ21_5-0091 | `backend/api/v1/views/proposals.py:38` | `get_proposals / MAH-F0181` | `Proposal.query.order_by(Proposal.created_at.desc())` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0092 | `backend/api/v1/views/proposals.py:38` | `get_proposals / MAH-F0181` | `Proposal.query.order_by(Proposal.created_at.desc()).all()` | Consomme un Query ou un résultat : voir l’expression. Query terminal peut exécuter ; Result consomme une exécution antérieure. |
| REQ21_5-0093 | `backend/api/v1/views/proposals.py:72` | `create_proposal / MAH-F0182` | `Proposal(user_id=user.id, title=title, content=content, status='pending')` | Objet en mémoire ; aucun INSERT par cette seule construction. Defaults/PK possibles au flush. |
| REQ21_5-0094 | `backend/api/v1/views/proposals.py:83` | `create_proposal / MAH-F0182` | `db.session.add(new_proposal)` | Inscription d’objet(s) dans la Session ; écriture au flush, pas validation durable. |
| REQ21_5-0095 | `backend/api/v1/views/proposals.py:84` | `create_proposal / MAH-F0182` | `db.session.commit()` | Flush requis puis validation ; résultat réseau ultérieur distinct de la réussite du commit. |
| REQ21_5-0096 | `backend/api/v1/views/proposals.py:86` | `create_proposal / MAH-F0182` | `db.session.rollback()` | Fin/annulation de transaction en cours et remise en état de la Session ; pas annulation d’un commit déjà réussi. |
| REQ21_5-0097 | `backend/api/v1/views/story_deletion_support.py:66` | `lock_actor / MAH-F0188` | `User.query.filter_by(id=session.get('user_id'))` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0098 | `backend/api/v1/views/story_deletion_support.py:66` | `lock_actor / MAH-F0188` | `User.query.filter_by(id=session.get('user_id')).populate_existing()` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0099 | `backend/api/v1/views/story_deletion_support.py:66` | `lock_actor / MAH-F0188` | `User.query.filter_by(id=session.get('user_id')).populate_existing().with_for_update(read=True)` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0100 | `backend/api/v1/views/story_deletion_support.py:66` | `lock_actor / MAH-F0188` | `User.query.filter_by(id=session.get('user_id')).populate_existing().with_for_update(read=True).first()` | Consomme un Query ou un résultat : voir l’expression. Query terminal peut exécuter ; Result consomme une exécution antérieure. |
| REQ21_5-0101 | `backend/api/v1/views/story_deletion_support.py:75` | `require_integrity / MAH-F0189` | `db.session.connection()` | Connexion, exécution ou inspection : SQL/effet exact dépend de l’expression et du contexte ; aucun appel effectué ici. |
| REQ21_5-0102 | `backend/api/v1/views/story_deletion_support.py:78` | `require_integrity / MAH-F0189` | `connection.exec_driver_sql('PRAGMA foreign_keys')` | Connexion, exécution ou inspection : SQL/effet exact dépend de l’expression et du contexte ; aucun appel effectué ici. |
| REQ21_5-0103 | `backend/api/v1/views/story_deletion_support.py:78` | `require_integrity / MAH-F0189` | `connection.exec_driver_sql('PRAGMA foreign_keys').scalar()` | Consomme un Query ou un résultat : voir l’expression. Query terminal peut exécuter ; Result consomme une exécution antérieure. |
| REQ21_5-0104 | `backend/api/v1/views/story_deletion_support.py:81` | `require_integrity / MAH-F0189` | `db.session.execute(sa.text('SELECT @@foreign_key_checks'))` | Connexion, exécution ou inspection : SQL/effet exact dépend de l’expression et du contexte ; aucun appel effectué ici. |
| REQ21_5-0105 | `backend/api/v1/views/story_deletion_support.py:81` | `require_integrity / MAH-F0189` | `db.session.execute(sa.text('SELECT @@foreign_key_checks')).scalar()` | Consomme un Query ou un résultat : voir l’expression. Query terminal peut exécuter ; Result consomme une exécution antérieure. |
| REQ21_5-0106 | `backend/api/v1/views/story_deletion_support.py:81` | `require_integrity / MAH-F0189` | `sa.text('SELECT @@foreign_key_checks')` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0107 | `backend/api/v1/views/story_deletion_support.py:84` | `require_integrity / MAH-F0189` | `db.session.execute(sa.text('SELECT TABLE_NAME, ENGINE FROM information_schema.TABLES WHERE TABLE_SCHEMA=DATABASE()'))` | Connexion, exécution ou inspection : SQL/effet exact dépend de l’expression et du contexte ; aucun appel effectué ici. |
| REQ21_5-0108 | `backend/api/v1/views/story_deletion_support.py:84` | `require_integrity / MAH-F0189` | `db.session.execute(sa.text('SELECT TABLE_NAME, ENGINE FROM information_schema.TABLES WHERE TABLE_SCHEMA=DATABASE()')).all()` | Consomme un Query ou un résultat : voir l’expression. Query terminal peut exécuter ; Result consomme une exécution antérieure. |
| REQ21_5-0109 | `backend/api/v1/views/story_deletion_support.py:84` | `require_integrity / MAH-F0189` | `sa.text('SELECT TABLE_NAME, ENGINE FROM information_schema.TABLES WHERE TABLE_SCHEMA=DATABASE()')` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0110 | `backend/api/v1/views/story_deletion_support.py:92` | `require_integrity / MAH-F0189` | `sa.inspect(connection)` | Métadonnées de schéma inspectées/réfléchies ; requêtes selon objet et cache ; pas de preuve de base actuelle. |
| REQ21_5-0111 | `backend/api/v1/views/story_deletion_support.py:93` | `require_integrity / MAH-F0189` | `inspector.get_columns('reports')` | Connexion, exécution ou inspection : SQL/effet exact dépend de l’expression et du contexte ; aucun appel effectué ici. |
| REQ21_5-0112 | `backend/api/v1/views/story_deletion_support.py:104` | `require_integrity / MAH-F0189` | `inspector.get_foreign_keys(table)` | Connexion, exécution ou inspection : SQL/effet exact dépend de l’expression et du contexte ; aucun appel effectué ici. |
| REQ21_5-0113 | `backend/api/v1/views/story_deletion_support.py:106` | `require_integrity / MAH-F0189` | `sa.select(Report.id)` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0114 | `backend/api/v1/views/story_deletion_support.py:106` | `require_integrity / MAH-F0189` | `db.session.execute(sa.select(Report.id).outerjoin(Comment, Report.comment_id == Comment.id).where(Comment.id.is_(None)).limit(1))` | Connexion, exécution ou inspection : SQL/effet exact dépend de l’expression et du contexte ; aucun appel effectué ici. |
| REQ21_5-0115 | `backend/api/v1/views/story_deletion_support.py:106` | `require_integrity / MAH-F0189` | `db.session.execute(sa.select(Report.id).outerjoin(Comment, Report.comment_id == Comment.id).where(Comment.id.is_(None)).limit(1)).first()` | Consomme un Query ou un résultat : voir l’expression. Query terminal peut exécuter ; Result consomme une exécution antérieure. |
| REQ21_5-0116 | `backend/api/v1/views/story_deletion_support.py:106` | `require_integrity / MAH-F0189` | `sa.select(Report.id).outerjoin(Comment, Report.comment_id == Comment.id)` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0117 | `backend/api/v1/views/story_deletion_support.py:106` | `require_integrity / MAH-F0189` | `sa.select(Report.id).outerjoin(Comment, Report.comment_id == Comment.id).where(Comment.id.is_(None))` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0118 | `backend/api/v1/views/story_deletion_support.py:106` | `require_integrity / MAH-F0189` | `sa.select(Report.id).outerjoin(Comment, Report.comment_id == Comment.id).where(Comment.id.is_(None)).limit(1)` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0119 | `backend/api/v1/views/story_deletion_support.py:111` | `require_integrity / MAH-F0189` | `sa.select(CommentLike.id)` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0120 | `backend/api/v1/views/story_deletion_support.py:111` | `require_integrity / MAH-F0189` | `sa.select(CommentLike.id).outerjoin(Comment, CommentLike.comment_id == Comment.id)` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0121 | `backend/api/v1/views/story_deletion_support.py:111` | `require_integrity / MAH-F0189` | `sa.select(CommentLike.id).outerjoin(Comment, CommentLike.comment_id == Comment.id).outerjoin(User, CommentLike.user_id == User.id)` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0122 | `backend/api/v1/views/story_deletion_support.py:111` | `require_integrity / MAH-F0189` | `db.session.execute(sa.select(CommentLike.id).outerjoin(Comment, CommentLike.comment_id == Comment.id).outerjoin(User, CommentLike.user_id == User.id).where(sa.or_(Comment.id.is_(None), User.id.is_(None))).limit(1))` | Connexion, exécution ou inspection : SQL/effet exact dépend de l’expression et du contexte ; aucun appel effectué ici. |
| REQ21_5-0123 | `backend/api/v1/views/story_deletion_support.py:111` | `require_integrity / MAH-F0189` | `db.session.execute(sa.select(CommentLike.id).outerjoin(Comment, CommentLike.comment_id == Comment.id).outerjoin(User, CommentLike.user_id == User.id).where(sa.or_(Comment.id.is_(None), User.id.is_(None))).limit(1)).first()` | Consomme un Query ou un résultat : voir l’expression. Query terminal peut exécuter ; Result consomme une exécution antérieure. |
| REQ21_5-0124 | `backend/api/v1/views/story_deletion_support.py:111` | `require_integrity / MAH-F0189` | `sa.select(CommentLike.id).outerjoin(Comment, CommentLike.comment_id == Comment.id).outerjoin(User, CommentLike.user_id == User.id).where(sa.or_(Comment.id.is_(None), User.id.is_(None)))` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0125 | `backend/api/v1/views/story_deletion_support.py:111` | `require_integrity / MAH-F0189` | `sa.select(CommentLike.id).outerjoin(Comment, CommentLike.comment_id == Comment.id).outerjoin(User, CommentLike.user_id == User.id).where(sa.or_(Comment.id.is_(None), User.id.is_(None))).limit(1)` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0126 | `backend/api/v1/views/story_deletion_support.py:121` | `snapshot / MAH-F0190` | `sa.select(Story.__table__)` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0127 | `backend/api/v1/views/story_deletion_support.py:121` | `snapshot / MAH-F0190` | `sa.select(Story.__table__).where(Story.id == story_id)` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0128 | `backend/api/v1/views/story_deletion_support.py:123` | `snapshot / MAH-F0190` | `query.with_for_update()` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0129 | `backend/api/v1/views/story_deletion_support.py:124` | `snapshot / MAH-F0190` | `db.session.execute(query)` | Connexion, exécution ou inspection : SQL/effet exact dépend de l’expression et du contexte ; aucun appel effectué ici. |
| REQ21_5-0130 | `backend/api/v1/views/story_deletion_support.py:124` | `snapshot / MAH-F0190` | `db.session.execute(query).mappings()` | Adapte la présentation d’un résultat déjà obtenu ; ne constitue pas à lui seul un nouveau SELECT. |
| REQ21_5-0131 | `backend/api/v1/views/story_deletion_support.py:124` | `snapshot / MAH-F0190` | `db.session.execute(query).mappings().first()` | Consomme un Query ou un résultat : voir l’expression. Query terminal peut exécuter ; Result consomme une exécution antérieure. |
| REQ21_5-0132 | `backend/api/v1/views/story_deletion_support.py:134` | `snapshot / MAH-F0190` | `sa.select(model.__table__)` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0133 | `backend/api/v1/views/story_deletion_support.py:136` | `snapshot / MAH-F0190` | `query.join(Comment, model.comment_id == Comment.id)` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0134 | `backend/api/v1/views/story_deletion_support.py:136` | `snapshot / MAH-F0190` | `query.join(Comment, model.comment_id == Comment.id).where(Comment.story_id == story_id)` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0135 | `backend/api/v1/views/story_deletion_support.py:138` | `snapshot / MAH-F0190` | `query.where(model.story_id == story_id)` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0136 | `backend/api/v1/views/story_deletion_support.py:139` | `snapshot / MAH-F0190` | `query.order_by(model.id)` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0137 | `backend/api/v1/views/story_deletion_support.py:139` | `snapshot / MAH-F0190` | `query.order_by(model.id).limit(MAX_DEPENDENCIES + 1)` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0138 | `backend/api/v1/views/story_deletion_support.py:141` | `snapshot / MAH-F0190` | `query.with_for_update()` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0139 | `backend/api/v1/views/story_deletion_support.py:142` | `snapshot / MAH-F0190` | `db.session.execute(query)` | Connexion, exécution ou inspection : SQL/effet exact dépend de l’expression et du contexte ; aucun appel effectué ici. |
| REQ21_5-0140 | `backend/api/v1/views/story_deletion_support.py:142` | `snapshot / MAH-F0190` | `db.session.execute(query).mappings()` | Adapte la présentation d’un résultat déjà obtenu ; ne constitue pas à lui seul un nouveau SELECT. |
| REQ21_5-0141 | `backend/api/v1/views/story_deletion_support.py:199` | `deletion_preview / MAH-F0196` | `db.session.rollback()` | Fin/annulation de transaction en cours et remise en état de la Session ; pas annulation d’un commit déjà réussi. |
| REQ21_5-0142 | `backend/api/v1/views/story_deletion_support.py:215` | `confirm_deletion / MAH-F0197` | `db.session.rollback()` | Fin/annulation de transaction en cours et remise en état de la Session ; pas annulation d’un commit déjà réussi. |
| REQ21_5-0143 | `backend/api/v1/views/story_deletion_support.py:239` | `delete_story / MAH-F0198` | `sa.update(Story.__table__)` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0144 | `backend/api/v1/views/story_deletion_support.py:239` | `delete_story / MAH-F0198` | `db.session.execute(sa.update(Story.__table__).where(Story.id == story_id, Story.management_revision == story['management_revision'], Story.archived_at.is_not(None)).values(management_revision=reserved))` | Connexion, exécution ou inspection : SQL/effet exact dépend de l’expression et du contexte ; aucun appel effectué ici. |
| REQ21_5-0145 | `backend/api/v1/views/story_deletion_support.py:239` | `delete_story / MAH-F0198` | `sa.update(Story.__table__).where(Story.id == story_id, Story.management_revision == story['management_revision'], Story.archived_at.is_not(None))` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0146 | `backend/api/v1/views/story_deletion_support.py:239` | `delete_story / MAH-F0198` | `sa.update(Story.__table__).where(Story.id == story_id, Story.management_revision == story['management_revision'], Story.archived_at.is_not(None)).values(management_revision=reserved)` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0147 | `backend/api/v1/views/story_deletion_support.py:249` | `delete_story / MAH-F0198` | `sa.select(Comment.id)` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0148 | `backend/api/v1/views/story_deletion_support.py:249` | `delete_story / MAH-F0198` | `sa.select(Comment.id).where(Comment.story_id == story_id)` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0149 | `backend/api/v1/views/story_deletion_support.py:251` | `delete_story / MAH-F0198` | `db.session.execute(sa.delete(model.__table__).where(predicate))` | Connexion, exécution ou inspection : SQL/effet exact dépend de l’expression et du contexte ; aucun appel effectué ici. |
| REQ21_5-0150 | `backend/api/v1/views/story_deletion_support.py:251` | `delete_story / MAH-F0198` | `sa.delete(model.__table__)` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0151 | `backend/api/v1/views/story_deletion_support.py:251` | `delete_story / MAH-F0198` | `sa.delete(model.__table__).where(predicate)` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0152 | `backend/api/v1/views/story_deletion_support.py:254` | `delete_story / MAH-F0198` | `sa.delete(Story.__table__)` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0153 | `backend/api/v1/views/story_deletion_support.py:254` | `delete_story / MAH-F0198` | `db.session.execute(sa.delete(Story.__table__).where(Story.id == story_id, Story.management_revision == reserved, Story.archived_at.is_not(None)))` | Connexion, exécution ou inspection : SQL/effet exact dépend de l’expression et du contexte ; aucun appel effectué ici. |
| REQ21_5-0154 | `backend/api/v1/views/story_deletion_support.py:254` | `delete_story / MAH-F0198` | `sa.delete(Story.__table__).where(Story.id == story_id, Story.management_revision == reserved, Story.archived_at.is_not(None))` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0155 | `backend/api/v1/views/story_deletion_support.py:261` | `delete_story / MAH-F0198` | `db.session.execute(sa.select(model.id).where(model.id.in_(ids[offset:offset + 500])).limit(1))` | Connexion, exécution ou inspection : SQL/effet exact dépend de l’expression et du contexte ; aucun appel effectué ici. |
| REQ21_5-0156 | `backend/api/v1/views/story_deletion_support.py:261` | `delete_story / MAH-F0198` | `db.session.execute(sa.select(model.id).where(model.id.in_(ids[offset:offset + 500])).limit(1)).first()` | Consomme un Query ou un résultat : voir l’expression. Query terminal peut exécuter ; Result consomme une exécution antérieure. |
| REQ21_5-0157 | `backend/api/v1/views/story_deletion_support.py:261` | `delete_story / MAH-F0198` | `sa.select(model.id)` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0158 | `backend/api/v1/views/story_deletion_support.py:261` | `delete_story / MAH-F0198` | `sa.select(model.id).where(model.id.in_(ids[offset:offset + 500]))` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0159 | `backend/api/v1/views/story_deletion_support.py:261` | `delete_story / MAH-F0198` | `sa.select(model.id).where(model.id.in_(ids[offset:offset + 500])).limit(1)` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0160 | `backend/api/v1/views/story_deletion_support.py:269` | `delete_story / MAH-F0198` | `db.session.commit()` | Flush requis puis validation ; résultat réseau ultérieur distinct de la réussite du commit. |
| REQ21_5-0161 | `backend/api/v1/views/story_deletion_support.py:273` | `delete_story / MAH-F0198` | `db.session.rollback()` | Fin/annulation de transaction en cours et remise en état de la Session ; pas annulation d’un commit déjà réussi. |
| REQ21_5-0162 | `backend/api/v1/views/story_deletion_support.py:276` | `delete_story / MAH-F0198` | `db.session.expire_all()` | Marque les états ORM expirés ; pas une relecture immédiate de toutes les tables. |
| REQ21_5-0163 | `backend/api/v1/views/story_deletion_support.py:284` | `run_deletion_action / MAH-F0199` | `db.session.rollback()` | Fin/annulation de transaction en cours et remise en état de la Session ; pas annulation d’un commit déjà réussi. |
| REQ21_5-0164 | `backend/api/v1/views/story_deletion_support.py:287` | `run_deletion_action / MAH-F0199` | `db.session.rollback()` | Fin/annulation de transaction en cours et remise en état de la Session ; pas annulation d’un commit déjà réussi. |
| REQ21_5-0165 | `backend/api/v1/views/story_visibility.py:15` | `get_active_story / MAH-F0200` | `Story.query.filter_by(id=identifier, archived_at=None)` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0166 | `backend/api/v1/views/story_visibility.py:20` | `get_active_story / MAH-F0200` | `query.populate_existing()` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0167 | `backend/api/v1/views/story_visibility.py:20` | `get_active_story / MAH-F0200` | `query.populate_existing().with_for_update()` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0168 | `backend/api/v1/views/story_visibility.py:21` | `get_active_story / MAH-F0200` | `query.first()` | Consomme un Query ou un résultat : voir l’expression. Query terminal peut exécuter ; Result consomme une exécution antérieure. |
| REQ21_5-0169 | `backend/api/v1/views/story_visibility.py:23` | `get_active_story / MAH-F0200` | `db.session.rollback()` | Fin/annulation de transaction en cours et remise en état de la Session ; pas annulation d’un commit déjà réussi. |
| REQ21_5-0170 | `backend/api/v1/views/theories.py:46` | `get_theories / MAH-F0202` | `Theory.query.filter_by(story_id=story_id)` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0171 | `backend/api/v1/views/theories.py:46` | `get_theories / MAH-F0202` | `Theory.query.filter_by(story_id=story_id).order_by(Theory.created_at.asc())` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0172 | `backend/api/v1/views/theories.py:46` | `get_theories / MAH-F0202` | `Theory.query.filter_by(story_id=story_id).order_by(Theory.created_at.asc()).all()` | Consomme un Query ou un résultat : voir l’expression. Query terminal peut exécuter ; Result consomme une exécution antérieure. |
| REQ21_5-0173 | `backend/api/v1/views/theories.py:92` | `post_theory / MAH-F0203` | `Theory(story_id=story_id, user_id=user.id, title=title, content=content)` | Objet en mémoire ; aucun INSERT par cette seule construction. Defaults/PK possibles au flush. |
| REQ21_5-0174 | `backend/api/v1/views/theories.py:103` | `post_theory / MAH-F0203` | `db.session.add(new_theory)` | Inscription d’objet(s) dans la Session ; écriture au flush, pas validation durable. |
| REQ21_5-0175 | `backend/api/v1/views/theories.py:104` | `post_theory / MAH-F0203` | `db.session.commit()` | Flush requis puis validation ; résultat réseau ultérieur distinct de la réussite du commit. |
| REQ21_5-0176 | `backend/api/v1/views/theories.py:106` | `post_theory / MAH-F0203` | `db.session.rollback()` | Fin/annulation de transaction en cours et remise en état de la Session ; pas annulation d’un commit déjà réussi. |
| REQ21_5-0177 | `backend/api/v1/views/theories.py:137` | `like_theory / MAH-F0204` | `db.session.execute(update(Theory).where(Theory.id == theory.id).values(likes=Theory.likes + 1).execution_options(synchronize_session=False))` | Connexion, exécution ou inspection : SQL/effet exact dépend de l’expression et du contexte ; aucun appel effectué ici. |
| REQ21_5-0178 | `backend/api/v1/views/theories.py:138` | `like_theory / MAH-F0204` | `update(Theory)` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0179 | `backend/api/v1/views/theories.py:138` | `like_theory / MAH-F0204` | `update(Theory).where(Theory.id == theory.id)` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0180 | `backend/api/v1/views/theories.py:138` | `like_theory / MAH-F0204` | `update(Theory).where(Theory.id == theory.id).values(likes=Theory.likes + 1)` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0181 | `backend/api/v1/views/theories.py:138` | `like_theory / MAH-F0204` | `update(Theory).where(Theory.id == theory.id).values(likes=Theory.likes + 1).execution_options(synchronize_session=False)` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0182 | `backend/api/v1/views/theories.py:144` | `like_theory / MAH-F0204` | `db.session.rollback()` | Fin/annulation de transaction en cours et remise en état de la Session ; pas annulation d’un commit déjà réussi. |
| REQ21_5-0183 | `backend/api/v1/views/theories.py:146` | `like_theory / MAH-F0204` | `db.session.refresh(theory)` | SELECT de rafraîchissement d’un objet ; contrôle des attributs suivi. |
| REQ21_5-0184 | `backend/api/v1/views/theories.py:148` | `like_theory / MAH-F0204` | `db.session.commit()` | Flush requis puis validation ; résultat réseau ultérieur distinct de la réussite du commit. |
| REQ21_5-0185 | `backend/api/v1/views/theories.py:150` | `like_theory / MAH-F0204` | `db.session.rollback()` | Fin/annulation de transaction en cours et remise en état de la Session ; pas annulation d’un commit déjà réussi. |
| REQ21_5-0186 | `backend/api/v1/views/users.py:40` | `get_users / MAH-F0206` | `User.query.order_by(User.id.asc())` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0187 | `backend/api/v1/views/users.py:40` | `get_users / MAH-F0206` | `User.query.order_by(User.id.asc()).all()` | Consomme un Query ou un résultat : voir l’expression. Query terminal peut exécuter ; Result consomme une exécution antérieure. |
| REQ21_5-0188 | `backend/api/v1/views/users.py:43` | `get_users / MAH-F0206` | `db.session.rollback()` | Fin/annulation de transaction en cours et remise en état de la Session ; pas annulation d’un commit déjà réussi. |
| REQ21_5-0189 | `backend/api/v1/views/users.py:90` | `register_user / MAH-F0207` | `User.query.filter_by(username=username)` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0190 | `backend/api/v1/views/users.py:90` | `register_user / MAH-F0207` | `User.query.filter_by(username=username).first()` | Consomme un Query ou un résultat : voir l’expression. Query terminal peut exécuter ; Result consomme une exécution antérieure. |
| REQ21_5-0191 | `backend/api/v1/views/users.py:92` | `register_user / MAH-F0207` | `User.query.filter_by(email=email)` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0192 | `backend/api/v1/views/users.py:92` | `register_user / MAH-F0207` | `User.query.filter_by(email=email).first()` | Consomme un Query ou un résultat : voir l’expression. Query terminal peut exécuter ; Result consomme une exécution antérieure. |
| REQ21_5-0193 | `backend/api/v1/views/users.py:95` | `register_user / MAH-F0207` | `User(username=username, email=email)` | Objet en mémoire ; aucun INSERT par cette seule construction. Defaults/PK possibles au flush. |
| REQ21_5-0194 | `backend/api/v1/views/users.py:102` | `register_user / MAH-F0207` | `db.session.add(new_user)` | Inscription d’objet(s) dans la Session ; écriture au flush, pas validation durable. |
| REQ21_5-0195 | `backend/api/v1/views/users.py:103` | `register_user / MAH-F0207` | `db.session.commit()` | Flush requis puis validation ; résultat réseau ultérieur distinct de la réussite du commit. |
| REQ21_5-0196 | `backend/api/v1/views/users.py:105` | `register_user / MAH-F0207` | `db.session.rollback()` | Fin/annulation de transaction en cours et remise en état de la Session ; pas annulation d’un commit déjà réussi. |
| REQ21_5-0197 | `backend/api/v1/views/users.py:113` | `register_user / MAH-F0207` | `db.session.rollback()` | Fin/annulation de transaction en cours et remise en état de la Session ; pas annulation d’un commit déjà réussi. |
| REQ21_5-0198 | `backend/api/v1/views/write_support.py:53` | `get_resource / MAH-F0211` | `db.session.get(model, identifier)` | Identité ORM ou None ; SELECT si l’état de Session l’exige. |
| REQ21_5-0199 | `backend/index.py:98` | `<module> / déclaration de classe/module ou portée sans nouvel ID` | `all([AIVEN_DB_HOST, AIVEN_DB_PORT, AIVEN_DB_USER, AIVEN_DB_PASSWORD, AIVEN_DB_NAME, AIVEN_CA_CERT])` | Consomme un Query ou un résultat : voir l’expression. Query terminal peut exécuter ; Result consomme une exécution antérieure. |
| REQ21_5-0200 | `backend/index.py:146` | `<module> / déclaration de classe/module ou portée sans nouvel ID` | `db.init_app(app)` | Déclaration/configuration, sauf create_all qui peut créer le schéma quand appelé ; pas un seed automatique. |
| REQ21_5-0201 | `backend/index.py:247` | `get_stats / MAH-F0040` | `User.query.count()` | Query.count exécute un décompte ; ne pas confondre avec la construction func.count. |
| REQ21_5-0202 | `backend/index.py:248` | `get_stats / MAH-F0040` | `Comment.query.count()` | Query.count exécute un décompte ; ne pas confondre avec la construction func.count. |
| REQ21_5-0203 | `backend/index.py:249` | `get_stats / MAH-F0040` | `Report.query.count()` | Query.count exécute un décompte ; ne pas confondre avec la construction func.count. |
| REQ21_5-0204 | `backend/index.py:258` | `get_stats / MAH-F0040` | `db.session.rollback()` | Fin/annulation de transaction en cours et remise en état de la Session ; pas annulation d’un commit déjà réussi. |
| REQ21_5-0205 | `backend/index.py:298` | `login_user / MAH-F0041` | `User.query.filter_by(username=username)` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0206 | `backend/index.py:298` | `login_user / MAH-F0041` | `User.query.filter_by(username=username).first()` | Consomme un Query ou un résultat : voir l’expression. Query terminal peut exécuter ; Result consomme une exécution antérieure. |
| REQ21_5-0207 | `backend/models.py:31` | `User / déclaration de classe/module ou portée sans nouvel ID` | `db.relationship('Story', back_populates='author')` | Déclaration/configuration, sauf create_all qui peut créer le schéma quand appelé ; pas un seed automatique. |
| REQ21_5-0208 | `backend/models.py:32` | `User / déclaration de classe/module ou portée sans nouvel ID` | `db.relationship('Comment', back_populates='user')` | Déclaration/configuration, sauf create_all qui peut créer le schéma quand appelé ; pas un seed automatique. |
| REQ21_5-0209 | `backend/models.py:33` | `User / déclaration de classe/module ou portée sans nouvel ID` | `db.relationship('Vote', back_populates='user')` | Déclaration/configuration, sauf create_all qui peut créer le schéma quand appelé ; pas un seed automatique. |
| REQ21_5-0210 | `backend/models.py:34` | `User / déclaration de classe/module ou portée sans nouvel ID` | `db.relationship('CommentLike', back_populates='user', cascade='all, delete-orphan', passive_deletes=True)` | Déclaration/configuration, sauf create_all qui peut créer le schéma quand appelé ; pas un seed automatique. |
| REQ21_5-0211 | `backend/models.py:38` | `User / déclaration de classe/module ou portée sans nouvel ID` | `db.relationship('Proposal', back_populates='user')` | Déclaration/configuration, sauf create_all qui peut créer le schéma quand appelé ; pas un seed automatique. |
| REQ21_5-0212 | `backend/models.py:39` | `User / déclaration de classe/module ou portée sans nouvel ID` | `db.relationship('Theory', back_populates='author')` | Déclaration/configuration, sauf create_all qui peut créer le schéma quand appelé ; pas un seed automatique. |
| REQ21_5-0213 | `backend/models.py:77` | `Category / déclaration de classe/module ou portée sans nouvel ID` | `db.relationship('Story', back_populates='category')` | Déclaration/configuration, sauf create_all qui peut créer le schéma quand appelé ; pas un seed automatique. |
| REQ21_5-0214 | `backend/models.py:153` | `Story / déclaration de classe/module ou portée sans nouvel ID` | `db.relationship('Category', back_populates='stories')` | Déclaration/configuration, sauf create_all qui peut créer le schéma quand appelé ; pas un seed automatique. |
| REQ21_5-0215 | `backend/models.py:158` | `Story / déclaration de classe/module ou portée sans nouvel ID` | `db.relationship('User', back_populates='stories')` | Déclaration/configuration, sauf create_all qui peut créer le schéma quand appelé ; pas un seed automatique. |
| REQ21_5-0216 | `backend/models.py:166` | `Story / déclaration de classe/module ou portée sans nouvel ID` | `db.relationship('Comment', back_populates='story', cascade='all, delete-orphan')` | Déclaration/configuration, sauf create_all qui peut créer le schéma quand appelé ; pas un seed automatique. |
| REQ21_5-0217 | `backend/models.py:172` | `Story / déclaration de classe/module ou portée sans nouvel ID` | `db.relationship('Vote', back_populates='story', cascade='all, delete-orphan')` | Déclaration/configuration, sauf create_all qui peut créer le schéma quand appelé ; pas un seed automatique. |
| REQ21_5-0218 | `backend/models.py:178` | `Story / déclaration de classe/module ou portée sans nouvel ID` | `db.relationship('Theory', back_populates='story', cascade='all, delete-orphan')` | Déclaration/configuration, sauf create_all qui peut créer le schéma quand appelé ; pas un seed automatique. |
| REQ21_5-0219 | `backend/models.py:184` | `Story / déclaration de classe/module ou portée sans nouvel ID` | `db.relationship('ColdCaseUpdate', back_populates='story', cascade='all, delete-orphan')` | Déclaration/configuration, sauf create_all qui peut créer le schéma quand appelé ; pas un seed automatique. |
| REQ21_5-0220 | `backend/models.py:267` | `Theory / déclaration de classe/module ou portée sans nouvel ID` | `db.relationship('Story', back_populates='theories')` | Déclaration/configuration, sauf create_all qui peut créer le schéma quand appelé ; pas un seed automatique. |
| REQ21_5-0221 | `backend/models.py:272` | `Theory / déclaration de classe/module ou portée sans nouvel ID` | `db.relationship('User', back_populates='theories')` | Déclaration/configuration, sauf create_all qui peut créer le schéma quand appelé ; pas un seed automatique. |
| REQ21_5-0222 | `backend/models.py:334` | `Comment / déclaration de classe/module ou portée sans nouvel ID` | `db.relationship('Story', back_populates='comments')` | Déclaration/configuration, sauf create_all qui peut créer le schéma quand appelé ; pas un seed automatique. |
| REQ21_5-0223 | `backend/models.py:339` | `Comment / déclaration de classe/module ou portée sans nouvel ID` | `db.relationship('User', back_populates='comments')` | Déclaration/configuration, sauf create_all qui peut créer le schéma quand appelé ; pas un seed automatique. |
| REQ21_5-0224 | `backend/models.py:346` | `Comment / déclaration de classe/module ou portée sans nouvel ID` | `db.relationship('Report', back_populates='comment', cascade='all, delete-orphan', passive_deletes=True)` | Déclaration/configuration, sauf create_all qui peut créer le schéma quand appelé ; pas un seed automatique. |
| REQ21_5-0225 | `backend/models.py:352` | `Comment / déclaration de classe/module ou portée sans nouvel ID` | `db.relationship('CommentLike', back_populates='comment', cascade='all, delete-orphan', passive_deletes=True)` | Déclaration/configuration, sauf create_all qui peut créer le schéma quand appelé ; pas un seed automatique. |
| REQ21_5-0226 | `backend/models.py:412` | `Vote / déclaration de classe/module ou portée sans nouvel ID` | `db.relationship('Story', back_populates='votes')` | Déclaration/configuration, sauf create_all qui peut créer le schéma quand appelé ; pas un seed automatique. |
| REQ21_5-0227 | `backend/models.py:417` | `Vote / déclaration de classe/module ou portée sans nouvel ID` | `db.relationship('User', back_populates='votes')` | Déclaration/configuration, sauf create_all qui peut créer le schéma quand appelé ; pas un seed automatique. |
| REQ21_5-0228 | `backend/models.py:447` | `CommentLike / déclaration de classe/module ou portée sans nouvel ID` | `db.relationship('Comment', back_populates='comment_likes')` | Déclaration/configuration, sauf create_all qui peut créer le schéma quand appelé ; pas un seed automatique. |
| REQ21_5-0229 | `backend/models.py:448` | `CommentLike / déclaration de classe/module ou portée sans nouvel ID` | `db.relationship('User', back_populates='comment_likes')` | Déclaration/configuration, sauf create_all qui peut créer le schéma quand appelé ; pas un seed automatique. |
| REQ21_5-0230 | `backend/models.py:504` | `Proposal / déclaration de classe/module ou portée sans nouvel ID` | `db.relationship('User', back_populates='proposals')` | Déclaration/configuration, sauf create_all qui peut créer le schéma quand appelé ; pas un seed automatique. |
| REQ21_5-0231 | `backend/models.py:527` | `Report / déclaration de classe/module ou portée sans nouvel ID` | `db.relationship('Comment', back_populates='moderation_reports')` | Déclaration/configuration, sauf create_all qui peut créer le schéma quand appelé ; pas un seed automatique. |
| REQ21_5-0232 | `backend/models.py:617` | `ColdCaseUpdate / déclaration de classe/module ou portée sans nouvel ID` | `db.relationship('Story', back_populates='cold_case_updates')` | Déclaration/configuration, sauf create_all qui peut créer le schéma quand appelé ; pas un seed automatique. |
| REQ21_5-0233 | `migrations/env.py:111` | `run_migrations_online / MAH-F0017` | `connectable.connect()` | Connexion, exécution ou inspection : SQL/effet exact dépend de l’expression et du contexte ; aucun appel effectué ici. |
| REQ21_5-0234 | `migrations/sqlite_safety.py:17` | `sqlite_migration_scope / MAH-F0213` | `raw.execute('PRAGMA foreign_keys=ON')` | Connexion, exécution ou inspection : SQL/effet exact dépend de l’expression et du contexte ; aucun appel effectué ici. |
| REQ21_5-0235 | `migrations/sqlite_safety.py:18` | `sqlite_migration_scope / MAH-F0213` | `raw.execute('PRAGMA foreign_key_check')` | Connexion, exécution ou inspection : SQL/effet exact dépend de l’expression et du contexte ; aucun appel effectué ici. |
| REQ21_5-0236 | `migrations/sqlite_safety.py:20` | `sqlite_migration_scope / MAH-F0213` | `raw.execute('PRAGMA foreign_keys=OFF')` | Connexion, exécution ou inspection : SQL/effet exact dépend de l’expression et du contexte ; aucun appel effectué ici. |
| REQ21_5-0237 | `migrations/sqlite_safety.py:21` | `sqlite_migration_scope / MAH-F0213` | `raw.execute('PRAGMA foreign_keys')` | Connexion, exécution ou inspection : SQL/effet exact dépend de l’expression et du contexte ; aucun appel effectué ici. |
| REQ21_5-0238 | `migrations/sqlite_safety.py:24` | `sqlite_migration_scope / MAH-F0213` | `connection.begin()` | Connexion, exécution ou inspection : SQL/effet exact dépend de l’expression et du contexte ; aucun appel effectué ici. |
| REQ21_5-0239 | `migrations/sqlite_safety.py:26` | `sqlite_migration_scope / MAH-F0213` | `connection.exec_driver_sql('BEGIN')` | Connexion, exécution ou inspection : SQL/effet exact dépend de l’expression et du contexte ; aucun appel effectué ici. |
| REQ21_5-0240 | `migrations/sqlite_safety.py:29` | `sqlite_migration_scope / MAH-F0213` | `connection.exec_driver_sql('PRAGMA foreign_key_check')` | Connexion, exécution ou inspection : SQL/effet exact dépend de l’expression et du contexte ; aucun appel effectué ici. |
| REQ21_5-0241 | `migrations/sqlite_safety.py:29` | `sqlite_migration_scope / MAH-F0213` | `connection.exec_driver_sql('PRAGMA foreign_key_check').first()` | Consomme un Query ou un résultat : voir l’expression. Query terminal peut exécuter ; Result consomme une exécution antérieure. |
| REQ21_5-0242 | `migrations/sqlite_safety.py:33` | `sqlite_migration_scope / MAH-F0213` | `raw.execute('PRAGMA foreign_keys=ON')` | Connexion, exécution ou inspection : SQL/effet exact dépend de l’expression et du contexte ; aucun appel effectué ici. |
| REQ21_5-0243 | `migrations/sqlite_safety.py:34` | `sqlite_migration_scope / MAH-F0213` | `raw.execute('PRAGMA foreign_keys')` | Connexion, exécution ou inspection : SQL/effet exact dépend de l’expression et du contexte ; aucun appel effectué ici. |
| REQ21_5-0244 | `migrations/versions/3111f5767fc6_ajoute_les_regles_on_delete.py:25` | `upgrade / MAH-F0019` | `op.batch_alter_table('comments', schema=None)` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0245 | `migrations/versions/3111f5767fc6_ajoute_les_regles_on_delete.py:26` | `upgrade / MAH-F0019` | `batch_op.drop_constraint('comments_ibfk_1', type_='foreignkey')` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0246 | `migrations/versions/3111f5767fc6_ajoute_les_regles_on_delete.py:31` | `upgrade / MAH-F0019` | `batch_op.drop_constraint('comments_ibfk_2', type_='foreignkey')` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0247 | `migrations/versions/3111f5767fc6_ajoute_les_regles_on_delete.py:36` | `upgrade / MAH-F0019` | `batch_op.create_foreign_key('fk_comments_story', 'stories', ['story_id'], ['id'], ondelete='CASCADE')` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0248 | `migrations/versions/3111f5767fc6_ajoute_les_regles_on_delete.py:44` | `upgrade / MAH-F0019` | `batch_op.create_foreign_key('fk_comments_user', 'users', ['user_id'], ['id'], ondelete='SET NULL')` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0249 | `migrations/versions/3111f5767fc6_ajoute_les_regles_on_delete.py:54` | `upgrade / MAH-F0019` | `op.batch_alter_table('proposals', schema=None)` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0250 | `migrations/versions/3111f5767fc6_ajoute_les_regles_on_delete.py:55` | `upgrade / MAH-F0019` | `batch_op.drop_constraint('proposals_ibfk_1', type_='foreignkey')` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0251 | `migrations/versions/3111f5767fc6_ajoute_les_regles_on_delete.py:60` | `upgrade / MAH-F0019` | `batch_op.create_foreign_key('fk_proposals_user', 'users', ['user_id'], ['id'], ondelete='CASCADE')` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0252 | `migrations/versions/3111f5767fc6_ajoute_les_regles_on_delete.py:71` | `upgrade / MAH-F0019` | `op.batch_alter_table('theories', schema=None)` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0253 | `migrations/versions/3111f5767fc6_ajoute_les_regles_on_delete.py:72` | `upgrade / MAH-F0019` | `batch_op.drop_constraint('theories_ibfk_1', type_='foreignkey')` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0254 | `migrations/versions/3111f5767fc6_ajoute_les_regles_on_delete.py:77` | `upgrade / MAH-F0019` | `batch_op.drop_constraint('theories_ibfk_2', type_='foreignkey')` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0255 | `migrations/versions/3111f5767fc6_ajoute_les_regles_on_delete.py:82` | `upgrade / MAH-F0019` | `batch_op.create_foreign_key('fk_theories_story', 'stories', ['story_id'], ['id'], ondelete='CASCADE')` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0256 | `migrations/versions/3111f5767fc6_ajoute_les_regles_on_delete.py:90` | `upgrade / MAH-F0019` | `batch_op.create_foreign_key('fk_theories_user', 'users', ['user_id'], ['id'], ondelete='SET NULL')` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0257 | `migrations/versions/3111f5767fc6_ajoute_les_regles_on_delete.py:100` | `upgrade / MAH-F0019` | `op.batch_alter_table('votes', schema=None)` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0258 | `migrations/versions/3111f5767fc6_ajoute_les_regles_on_delete.py:101` | `upgrade / MAH-F0019` | `batch_op.drop_constraint('votes_ibfk_1', type_='foreignkey')` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0259 | `migrations/versions/3111f5767fc6_ajoute_les_regles_on_delete.py:106` | `upgrade / MAH-F0019` | `batch_op.drop_constraint('votes_ibfk_2', type_='foreignkey')` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0260 | `migrations/versions/3111f5767fc6_ajoute_les_regles_on_delete.py:111` | `upgrade / MAH-F0019` | `batch_op.create_foreign_key('fk_votes_story', 'stories', ['story_id'], ['id'], ondelete='CASCADE')` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0261 | `migrations/versions/3111f5767fc6_ajoute_les_regles_on_delete.py:119` | `upgrade / MAH-F0019` | `batch_op.create_foreign_key('fk_votes_user', 'users', ['user_id'], ['id'], ondelete='CASCADE')` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0262 | `migrations/versions/3111f5767fc6_ajoute_les_regles_on_delete.py:132` | `downgrade / MAH-F0020` | `op.batch_alter_table('votes', schema=None)` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0263 | `migrations/versions/3111f5767fc6_ajoute_les_regles_on_delete.py:133` | `downgrade / MAH-F0020` | `batch_op.drop_constraint('fk_votes_story', type_='foreignkey')` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0264 | `migrations/versions/3111f5767fc6_ajoute_les_regles_on_delete.py:138` | `downgrade / MAH-F0020` | `batch_op.drop_constraint('fk_votes_user', type_='foreignkey')` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0265 | `migrations/versions/3111f5767fc6_ajoute_les_regles_on_delete.py:143` | `downgrade / MAH-F0020` | `batch_op.create_foreign_key('votes_ibfk_1', 'stories', ['story_id'], ['id'])` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0266 | `migrations/versions/3111f5767fc6_ajoute_les_regles_on_delete.py:150` | `downgrade / MAH-F0020` | `batch_op.create_foreign_key('votes_ibfk_2', 'users', ['user_id'], ['id'])` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0267 | `migrations/versions/3111f5767fc6_ajoute_les_regles_on_delete.py:158` | `downgrade / MAH-F0020` | `op.batch_alter_table('theories', schema=None)` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0268 | `migrations/versions/3111f5767fc6_ajoute_les_regles_on_delete.py:159` | `downgrade / MAH-F0020` | `batch_op.drop_constraint('fk_theories_story', type_='foreignkey')` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0269 | `migrations/versions/3111f5767fc6_ajoute_les_regles_on_delete.py:164` | `downgrade / MAH-F0020` | `batch_op.drop_constraint('fk_theories_user', type_='foreignkey')` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0270 | `migrations/versions/3111f5767fc6_ajoute_les_regles_on_delete.py:169` | `downgrade / MAH-F0020` | `batch_op.create_foreign_key('theories_ibfk_1', 'stories', ['story_id'], ['id'])` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0271 | `migrations/versions/3111f5767fc6_ajoute_les_regles_on_delete.py:176` | `downgrade / MAH-F0020` | `batch_op.create_foreign_key('theories_ibfk_2', 'users', ['user_id'], ['id'])` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0272 | `migrations/versions/3111f5767fc6_ajoute_les_regles_on_delete.py:184` | `downgrade / MAH-F0020` | `op.batch_alter_table('proposals', schema=None)` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0273 | `migrations/versions/3111f5767fc6_ajoute_les_regles_on_delete.py:185` | `downgrade / MAH-F0020` | `batch_op.drop_constraint('fk_proposals_user', type_='foreignkey')` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0274 | `migrations/versions/3111f5767fc6_ajoute_les_regles_on_delete.py:190` | `downgrade / MAH-F0020` | `batch_op.create_foreign_key('proposals_ibfk_1', 'users', ['user_id'], ['id'])` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0275 | `migrations/versions/3111f5767fc6_ajoute_les_regles_on_delete.py:198` | `downgrade / MAH-F0020` | `op.batch_alter_table('comments', schema=None)` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0276 | `migrations/versions/3111f5767fc6_ajoute_les_regles_on_delete.py:199` | `downgrade / MAH-F0020` | `batch_op.drop_constraint('fk_comments_story', type_='foreignkey')` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0277 | `migrations/versions/3111f5767fc6_ajoute_les_regles_on_delete.py:204` | `downgrade / MAH-F0020` | `batch_op.drop_constraint('fk_comments_user', type_='foreignkey')` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0278 | `migrations/versions/3111f5767fc6_ajoute_les_regles_on_delete.py:209` | `downgrade / MAH-F0020` | `batch_op.create_foreign_key('comments_ibfk_1', 'stories', ['story_id'], ['id'])` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0279 | `migrations/versions/3111f5767fc6_ajoute_les_regles_on_delete.py:216` | `downgrade / MAH-F0020` | `batch_op.create_foreign_key('comments_ibfk_2', 'users', ['user_id'], ['id'])` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0280 | `migrations/versions/82deda84bc35_remove_legacy_comment_reports_counter.py:22` | `upgrade / MAH-F0021` | `op.batch_alter_table('comments', schema=None)` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0281 | `migrations/versions/82deda84bc35_remove_legacy_comment_reports_counter.py:23` | `upgrade / MAH-F0021` | `batch_op.drop_column('reports')` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0282 | `migrations/versions/82deda84bc35_remove_legacy_comment_reports_counter.py:29` | `downgrade / MAH-F0022` | `op.batch_alter_table('comments', schema=None)` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0283 | `migrations/versions/82deda84bc35_remove_legacy_comment_reports_counter.py:30` | `downgrade / MAH-F0022` | `batch_op.add_column(sa.Column('reports', sa.Integer(), nullable=False, server_default='0'))` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0284 | `migrations/versions/82deda84bc35_remove_legacy_comment_reports_counter.py:39` | `downgrade / MAH-F0022` | `op.batch_alter_table('comments', schema=None)` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0285 | `migrations/versions/82deda84bc35_remove_legacy_comment_reports_counter.py:40` | `downgrade / MAH-F0022` | `batch_op.alter_column('reports', server_default=None)` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0286 | `migrations/versions/921687c1bd7c_baseline_schema.py:23` | `upgrade / MAH-F0023` | `op.create_table('users', sa.Column('id', sa.Integer(), nullable=False), sa.Column('username', sa.String(length=100), nullable=False), sa.Column('email', sa.String(length=150), nullable=False), sa.Column('password_hash', sa.String(length=255), nullable=False), sa.Column('is_admin', sa.Boolean(), nullable=False), sa.Column('created_at', sa.DateTime(), nullable=False), sa.PrimaryKeyConstraint('id'), sa.UniqueConstraint('email'), sa.UniqueConstraint('username'))` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0287 | `migrations/versions/921687c1bd7c_baseline_schema.py:36` | `upgrade / MAH-F0023` | `op.create_table('categories', sa.Column('id', sa.Integer(), nullable=False), sa.Column('name', sa.String(length=100), nullable=False), sa.Column('description', sa.Text(), nullable=True), sa.PrimaryKeyConstraint('id'), sa.UniqueConstraint('name'))` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0288 | `migrations/versions/921687c1bd7c_baseline_schema.py:45` | `upgrade / MAH-F0023` | `op.create_table('stories', sa.Column('id', sa.Integer(), nullable=False), sa.Column('slug', sa.String(length=150), nullable=False), sa.Column('title', sa.String(length=200), nullable=False), sa.Column('summary', sa.Text(), nullable=False), sa.Column('content', sa.Text(), nullable=False), sa.Column('image_url', sa.String(length=500), nullable=True), sa.Column('category_id', sa.Integer(), nullable=False), sa.Column('author_id', sa.Integer(), nullable=False), sa.Column('created_at', sa.DateTime(), nullable=False), sa.Column('updated_at', sa.DateTime(), nullable=False), sa.ForeignKeyConstraint(['category_id'], ['categories.id'], name='stories_ibfk_1'), sa.ForeignKeyConstraint(['author_id'], ['users.id'], name='stories_ibfk_2'), sa.PrimaryKeyConstraint('id'), sa.UniqueConstraint('slug'))` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0289 | `migrations/versions/921687c1bd7c_baseline_schema.py:74` | `upgrade / MAH-F0023` | `op.create_table('theories', sa.Column('id', sa.Integer(), nullable=False), sa.Column('story_id', sa.Integer(), nullable=False), sa.Column('user_id', sa.Integer(), nullable=True), sa.Column('title', sa.String(length=200), nullable=False), sa.Column('content', sa.Text(), nullable=False), sa.Column('likes', sa.Integer(), nullable=False), sa.Column('created_at', sa.DateTime(), nullable=False), sa.ForeignKeyConstraint(['story_id'], ['stories.id'], name='theories_ibfk_1'), sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='theories_ibfk_2'), sa.PrimaryKeyConstraint('id'))` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0290 | `migrations/versions/921687c1bd7c_baseline_schema.py:99` | `upgrade / MAH-F0023` | `op.create_table('comments', sa.Column('id', sa.Integer(), nullable=False), sa.Column('story_id', sa.Integer(), nullable=False), sa.Column('user_id', sa.Integer(), nullable=True), sa.Column('username', sa.String(length=100), nullable=True), sa.Column('text', sa.Text(), nullable=False), sa.Column('likes', sa.Integer(), nullable=False), sa.Column('reports', sa.Integer(), nullable=False), sa.Column('created_at', sa.DateTime(), nullable=False), sa.ForeignKeyConstraint(['story_id'], ['stories.id'], name='comments_ibfk_1'), sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='comments_ibfk_2'), sa.PrimaryKeyConstraint('id'))` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0291 | `migrations/versions/921687c1bd7c_baseline_schema.py:125` | `upgrade / MAH-F0023` | `op.create_table('votes', sa.Column('id', sa.Integer(), nullable=False), sa.Column('story_id', sa.Integer(), nullable=False), sa.Column('user_id', sa.Integer(), nullable=False), sa.Column('created_at', sa.DateTime(), nullable=False), sa.ForeignKeyConstraint(['story_id'], ['stories.id'], name='votes_ibfk_1'), sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='votes_ibfk_2'), sa.PrimaryKeyConstraint('id'), sa.UniqueConstraint('user_id', 'story_id', name='unique_user_story_vote'))` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0292 | `migrations/versions/921687c1bd7c_baseline_schema.py:153` | `upgrade / MAH-F0023` | `op.create_table('proposals', sa.Column('id', sa.Integer(), nullable=False), sa.Column('user_id', sa.Integer(), nullable=False), sa.Column('title', sa.String(length=200), nullable=False), sa.Column('content', sa.Text(), nullable=False), sa.Column('status', sa.String(length=20), nullable=False), sa.Column('created_at', sa.DateTime(), nullable=False), sa.Column('updated_at', sa.DateTime(), nullable=False), sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='proposals_ibfk_1'), sa.PrimaryKeyConstraint('id'))` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0293 | `migrations/versions/921687c1bd7c_baseline_schema.py:176` | `downgrade / MAH-F0024` | `op.drop_table('proposals')` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0294 | `migrations/versions/921687c1bd7c_baseline_schema.py:177` | `downgrade / MAH-F0024` | `op.drop_table('votes')` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0295 | `migrations/versions/921687c1bd7c_baseline_schema.py:178` | `downgrade / MAH-F0024` | `op.drop_table('comments')` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0296 | `migrations/versions/921687c1bd7c_baseline_schema.py:179` | `downgrade / MAH-F0024` | `op.drop_table('theories')` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0297 | `migrations/versions/921687c1bd7c_baseline_schema.py:180` | `downgrade / MAH-F0024` | `op.drop_table('stories')` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0298 | `migrations/versions/921687c1bd7c_baseline_schema.py:181` | `downgrade / MAH-F0024` | `op.drop_table('categories')` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0299 | `migrations/versions/921687c1bd7c_baseline_schema.py:182` | `downgrade / MAH-F0024` | `op.drop_table('users')` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0300 | `migrations/versions/a590c8aac613_add_reports_bans_and_cold_case_updates.py:22` | `upgrade / MAH-F0025` | `op.get_bind()` | Récupère le bind du contexte ; ne constitue pas à lui seul un DDL, un SELECT ou un commit. |
| REQ21_5-0301 | `migrations/versions/a590c8aac613_add_reports_bans_and_cold_case_updates.py:23` | `upgrade / MAH-F0025` | `op.get_bind()` | Récupère le bind du contexte ; ne constitue pas à lui seul un DDL, un SELECT ou un commit. |
| REQ21_5-0302 | `migrations/versions/a590c8aac613_add_reports_bans_and_cold_case_updates.py:23` | `upgrade / MAH-F0025` | `op.get_bind().exec_driver_sql('PRAGMA foreign_keys')` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0303 | `migrations/versions/a590c8aac613_add_reports_bans_and_cold_case_updates.py:23` | `upgrade / MAH-F0025` | `op.get_bind().exec_driver_sql('PRAGMA foreign_keys').scalar()` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0304 | `migrations/versions/a590c8aac613_add_reports_bans_and_cold_case_updates.py:24` | `upgrade / MAH-F0025` | `op.get_bind()` | Récupère le bind du contexte ; ne constitue pas à lui seul un DDL, un SELECT ou un commit. |
| REQ21_5-0305 | `migrations/versions/a590c8aac613_add_reports_bans_and_cold_case_updates.py:28` | `upgrade / MAH-F0025` | `op.create_table('reports', sa.Column('id', sa.Integer(), nullable=False), sa.Column('type', sa.String(length=100), nullable=False), sa.Column('target_id', sa.String(length=100), nullable=False), sa.Column('reason', sa.Text(), nullable=False), sa.Column('status', sa.String(length=20), nullable=False), sa.Column('created_at', sa.DateTime(), nullable=False), sa.PrimaryKeyConstraint('id'))` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0306 | `migrations/versions/a590c8aac613_add_reports_bans_and_cold_case_updates.py:39` | `upgrade / MAH-F0025` | `op.create_table('cold_case_updates', sa.Column('id', sa.Integer(), nullable=False), sa.Column('story_id', sa.Integer(), nullable=False), sa.Column('content', sa.Text(), nullable=False), sa.Column('created_at', sa.DateTime(), nullable=False), sa.ForeignKeyConstraint(['story_id'], ['stories.id'], name='fk_cold_case_updates_story', ondelete='CASCADE'), sa.PrimaryKeyConstraint('id'))` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0307 | `migrations/versions/a590c8aac613_add_reports_bans_and_cold_case_updates.py:54` | `upgrade / MAH-F0025` | `op.add_column('users', sa.Column('is_banned', sa.Boolean(), nullable=False, server_default=sa.false()))` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0308 | `migrations/versions/a590c8aac613_add_reports_bans_and_cold_case_updates.py:67` | `upgrade / MAH-F0025` | `op.batch_alter_table('users')` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0309 | `migrations/versions/a590c8aac613_add_reports_bans_and_cold_case_updates.py:68` | `upgrade / MAH-F0025` | `batch.alter_column('is_banned', existing_type=sa.Boolean(), server_default=None)` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0310 | `migrations/versions/a590c8aac613_add_reports_bans_and_cold_case_updates.py:71` | `upgrade / MAH-F0025` | `op.alter_column('users', 'is_banned', server_default=None)` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0311 | `migrations/versions/a590c8aac613_add_reports_bans_and_cold_case_updates.py:77` | `downgrade / MAH-F0026` | `op.drop_table('cold_case_updates')` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0312 | `migrations/versions/a590c8aac613_add_reports_bans_and_cold_case_updates.py:78` | `downgrade / MAH-F0026` | `op.drop_table('reports')` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0313 | `migrations/versions/a590c8aac613_add_reports_bans_and_cold_case_updates.py:80` | `downgrade / MAH-F0026` | `op.drop_column('users', 'is_banned')` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0314 | `migrations/versions/c6c100000001_add_story_archive_date.py:19` | `upgrade / MAH-F0027` | `op.add_column('stories', sa.Column('archived_at', sa.DateTime(), nullable=True))` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0315 | `migrations/versions/c6c100000001_add_story_archive_date.py:25` | `downgrade / MAH-F0028` | `op.drop_column('stories', 'archived_at')` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0316 | `migrations/versions/c6c200000001_comment_reports_and_story_revision.py:22` | `inspect_legacy / MAH-F0029` | `sa.inspect(bind)` | Métadonnées de schéma inspectées/réfléchies ; requêtes selon objet et cache ; pas de preuve de base actuelle. |
| REQ21_5-0317 | `migrations/versions/c6c200000001_comment_reports_and_story_revision.py:23` | `inspect_legacy / MAH-F0029` | `inspector.get_columns('comments')` | Connexion, exécution ou inspection : SQL/effet exact dépend de l’expression et du contexte ; aucun appel effectué ici. |
| REQ21_5-0318 | `migrations/versions/c6c200000001_comment_reports_and_story_revision.py:27` | `inspect_legacy / MAH-F0029` | `sa.Table('reports', metadata, autoload_with=bind)` | Métadonnées de schéma inspectées/réfléchies ; requêtes selon objet et cache ; pas de preuve de base actuelle. |
| REQ21_5-0319 | `migrations/versions/c6c200000001_comment_reports_and_story_revision.py:28` | `inspect_legacy / MAH-F0029` | `sa.Table('comments', metadata, autoload_with=bind)` | Métadonnées de schéma inspectées/réfléchies ; requêtes selon objet et cache ; pas de preuve de base actuelle. |
| REQ21_5-0320 | `migrations/versions/c6c200000001_comment_reports_and_story_revision.py:29` | `inspect_legacy / MAH-F0029` | `bind.execute(sa.select(reports.c.id, reports.c.type, reports.c.target_id))` | Connexion, exécution ou inspection : SQL/effet exact dépend de l’expression et du contexte ; aucun appel effectué ici. |
| REQ21_5-0321 | `migrations/versions/c6c200000001_comment_reports_and_story_revision.py:29` | `inspect_legacy / MAH-F0029` | `bind.execute(sa.select(reports.c.id, reports.c.type, reports.c.target_id)).all()` | Consomme un Query ou un résultat : voir l’expression. Query terminal peut exécuter ; Result consomme une exécution antérieure. |
| REQ21_5-0322 | `migrations/versions/c6c200000001_comment_reports_and_story_revision.py:29` | `inspect_legacy / MAH-F0029` | `sa.select(reports.c.id, reports.c.type, reports.c.target_id)` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0323 | `migrations/versions/c6c200000001_comment_reports_and_story_revision.py:30` | `inspect_legacy / MAH-F0029` | `bind.execute(sa.select(comments.c.id))` | Connexion, exécution ou inspection : SQL/effet exact dépend de l’expression et du contexte ; aucun appel effectué ici. |
| REQ21_5-0324 | `migrations/versions/c6c200000001_comment_reports_and_story_revision.py:30` | `inspect_legacy / MAH-F0029` | `bind.execute(sa.select(comments.c.id)).scalars()` | Adapte la présentation d’un résultat déjà obtenu ; ne constitue pas à lui seul un nouveau SELECT. |
| REQ21_5-0325 | `migrations/versions/c6c200000001_comment_reports_and_story_revision.py:30` | `inspect_legacy / MAH-F0029` | `sa.select(comments.c.id)` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0326 | `migrations/versions/c6c200000001_comment_reports_and_story_revision.py:43` | `upgrade / MAH-F0030` | `op.get_bind()` | Récupère le bind du contexte ; ne constitue pas à lui seul un DDL, un SELECT ou un commit. |
| REQ21_5-0327 | `migrations/versions/c6c200000001_comment_reports_and_story_revision.py:46` | `upgrade / MAH-F0030` | `op.add_column('reports', sa.Column('comment_id', comment_type, nullable=True))` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0328 | `migrations/versions/c6c200000001_comment_reports_and_story_revision.py:49` | `upgrade / MAH-F0030` | `bind.execute(table.update().where(table.c.id == row['report_id']).values(comment_id=row['comment_id']))` | Connexion, exécution ou inspection : SQL/effet exact dépend de l’expression et du contexte ; aucun appel effectué ici. |
| REQ21_5-0329 | `migrations/versions/c6c200000001_comment_reports_and_story_revision.py:49` | `upgrade / MAH-F0030` | `table.update()` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0330 | `migrations/versions/c6c200000001_comment_reports_and_story_revision.py:49` | `upgrade / MAH-F0030` | `table.update().where(table.c.id == row['report_id'])` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0331 | `migrations/versions/c6c200000001_comment_reports_and_story_revision.py:49` | `upgrade / MAH-F0030` | `table.update().where(table.c.id == row['report_id']).values(comment_id=row['comment_id'])` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0332 | `migrations/versions/c6c200000001_comment_reports_and_story_revision.py:52` | `upgrade / MAH-F0030` | `op.batch_alter_table('reports')` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0333 | `migrations/versions/c6c200000001_comment_reports_and_story_revision.py:53` | `upgrade / MAH-F0030` | `batch.alter_column('comment_id', existing_type=comment_type, nullable=False)` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0334 | `migrations/versions/c6c200000001_comment_reports_and_story_revision.py:54` | `upgrade / MAH-F0030` | `batch.create_foreign_key('fk_reports_comment', 'comments', ['comment_id'], ['id'], ondelete='CASCADE')` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0335 | `migrations/versions/c6c200000001_comment_reports_and_story_revision.py:55` | `upgrade / MAH-F0030` | `batch.drop_column('type')` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0336 | `migrations/versions/c6c200000001_comment_reports_and_story_revision.py:56` | `upgrade / MAH-F0030` | `batch.drop_column('target_id')` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0337 | `migrations/versions/c6c200000001_comment_reports_and_story_revision.py:57` | `upgrade / MAH-F0030` | `batch.create_index('ix_reports_comment_id', ['comment_id'], unique=False)` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0338 | `migrations/versions/c6c200000001_comment_reports_and_story_revision.py:58` | `upgrade / MAH-F0030` | `op.add_column('stories', sa.Column('management_revision', sa.String(32), nullable=False, server_default=SENTINEL))` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0339 | `migrations/versions/c6c200000001_comment_reports_and_story_revision.py:60` | `upgrade / MAH-F0030` | `bind.execute(sa.select(stories.c.id))` | Connexion, exécution ou inspection : SQL/effet exact dépend de l’expression et du contexte ; aucun appel effectué ici. |
| REQ21_5-0340 | `migrations/versions/c6c200000001_comment_reports_and_story_revision.py:60` | `upgrade / MAH-F0030` | `bind.execute(sa.select(stories.c.id)).scalars()` | Adapte la présentation d’un résultat déjà obtenu ; ne constitue pas à lui seul un nouveau SELECT. |
| REQ21_5-0341 | `migrations/versions/c6c200000001_comment_reports_and_story_revision.py:60` | `upgrade / MAH-F0030` | `bind.execute(sa.select(stories.c.id)).scalars().all()` | Consomme un Query ou un résultat : voir l’expression. Query terminal peut exécuter ; Result consomme une exécution antérieure. |
| REQ21_5-0342 | `migrations/versions/c6c200000001_comment_reports_and_story_revision.py:60` | `upgrade / MAH-F0030` | `sa.select(stories.c.id)` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0343 | `migrations/versions/c6c200000001_comment_reports_and_story_revision.py:61` | `upgrade / MAH-F0030` | `bind.execute(stories.update().where(stories.c.id == identifier).values(management_revision=uuid4().hex))` | Connexion, exécution ou inspection : SQL/effet exact dépend de l’expression et du contexte ; aucun appel effectué ici. |
| REQ21_5-0344 | `migrations/versions/c6c200000001_comment_reports_and_story_revision.py:61` | `upgrade / MAH-F0030` | `stories.update()` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0345 | `migrations/versions/c6c200000001_comment_reports_and_story_revision.py:61` | `upgrade / MAH-F0030` | `stories.update().where(stories.c.id == identifier)` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0346 | `migrations/versions/c6c200000001_comment_reports_and_story_revision.py:61` | `upgrade / MAH-F0030` | `stories.update().where(stories.c.id == identifier).values(management_revision=uuid4().hex)` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0347 | `migrations/versions/c6c200000001_comment_reports_and_story_revision.py:62` | `upgrade / MAH-F0030` | `op.create_index('uq_stories_management_revision', 'stories', ['management_revision'], unique=True)` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0348 | `migrations/versions/c6c200000001_comment_reports_and_story_revision.py:67` | `downgrade / MAH-F0031` | `op.get_bind()` | Récupère le bind du contexte ; ne constitue pas à lui seul un DDL, un SELECT ou un commit. |
| REQ21_5-0349 | `migrations/versions/c6c200000001_comment_reports_and_story_revision.py:68` | `downgrade / MAH-F0031` | `op.add_column('reports', sa.Column('type', sa.String(100), nullable=True))` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0350 | `migrations/versions/c6c200000001_comment_reports_and_story_revision.py:69` | `downgrade / MAH-F0031` | `op.add_column('reports', sa.Column('target_id', sa.String(100), nullable=True))` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0351 | `migrations/versions/c6c200000001_comment_reports_and_story_revision.py:71` | `downgrade / MAH-F0031` | `bind.execute(sa.select(reports.c.id, reports.c.comment_id))` | Connexion, exécution ou inspection : SQL/effet exact dépend de l’expression et du contexte ; aucun appel effectué ici. |
| REQ21_5-0352 | `migrations/versions/c6c200000001_comment_reports_and_story_revision.py:71` | `downgrade / MAH-F0031` | `bind.execute(sa.select(reports.c.id, reports.c.comment_id)).all()` | Consomme un Query ou un résultat : voir l’expression. Query terminal peut exécuter ; Result consomme une exécution antérieure. |
| REQ21_5-0353 | `migrations/versions/c6c200000001_comment_reports_and_story_revision.py:71` | `downgrade / MAH-F0031` | `sa.select(reports.c.id, reports.c.comment_id)` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0354 | `migrations/versions/c6c200000001_comment_reports_and_story_revision.py:72` | `downgrade / MAH-F0031` | `bind.execute(reports.update().where(reports.c.id == identifier).values(type='comment', target_id=str(target)))` | Connexion, exécution ou inspection : SQL/effet exact dépend de l’expression et du contexte ; aucun appel effectué ici. |
| REQ21_5-0355 | `migrations/versions/c6c200000001_comment_reports_and_story_revision.py:72` | `downgrade / MAH-F0031` | `reports.update()` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0356 | `migrations/versions/c6c200000001_comment_reports_and_story_revision.py:72` | `downgrade / MAH-F0031` | `reports.update().where(reports.c.id == identifier)` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0357 | `migrations/versions/c6c200000001_comment_reports_and_story_revision.py:72` | `downgrade / MAH-F0031` | `reports.update().where(reports.c.id == identifier).values(type='comment', target_id=str(target))` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0358 | `migrations/versions/c6c200000001_comment_reports_and_story_revision.py:73` | `downgrade / MAH-F0031` | `op.batch_alter_table('reports')` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0359 | `migrations/versions/c6c200000001_comment_reports_and_story_revision.py:74` | `downgrade / MAH-F0031` | `batch.drop_constraint('fk_reports_comment', type_='foreignkey')` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0360 | `migrations/versions/c6c200000001_comment_reports_and_story_revision.py:75` | `downgrade / MAH-F0031` | `batch.drop_index('ix_reports_comment_id')` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0361 | `migrations/versions/c6c200000001_comment_reports_and_story_revision.py:76` | `downgrade / MAH-F0031` | `batch.alter_column('type', existing_type=sa.String(100), nullable=False)` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0362 | `migrations/versions/c6c200000001_comment_reports_and_story_revision.py:77` | `downgrade / MAH-F0031` | `batch.alter_column('target_id', existing_type=sa.String(100), nullable=False)` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0363 | `migrations/versions/c6c200000001_comment_reports_and_story_revision.py:78` | `downgrade / MAH-F0031` | `batch.drop_column('comment_id')` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0364 | `migrations/versions/c6c200000001_comment_reports_and_story_revision.py:79` | `downgrade / MAH-F0031` | `op.drop_index('uq_stories_management_revision', table_name='stories')` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0365 | `migrations/versions/c6c200000001_comment_reports_and_story_revision.py:80` | `downgrade / MAH-F0031` | `op.drop_column('stories', 'management_revision')` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0366 | `migrations/versions/c6g200000001_add_comment_likes.py:18` | `inspect_legacy / MAH-F0032` | `bind.exec_driver_sql('PRAGMA foreign_keys')` | Connexion, exécution ou inspection : SQL/effet exact dépend de l’expression et du contexte ; aucun appel effectué ici. |
| REQ21_5-0367 | `migrations/versions/c6g200000001_add_comment_likes.py:18` | `inspect_legacy / MAH-F0032` | `bind.exec_driver_sql('PRAGMA foreign_keys').scalar()` | Consomme un Query ou un résultat : voir l’expression. Query terminal peut exécuter ; Result consomme une exécution antérieure. |
| REQ21_5-0368 | `migrations/versions/c6g200000001_add_comment_likes.py:24` | `inspect_legacy / MAH-F0032` | `bind.exec_driver_sql('PRAGMA foreign_key_check')` | Connexion, exécution ou inspection : SQL/effet exact dépend de l’expression et du contexte ; aucun appel effectué ici. |
| REQ21_5-0369 | `migrations/versions/c6g200000001_add_comment_likes.py:24` | `inspect_legacy / MAH-F0032` | `bind.exec_driver_sql('PRAGMA foreign_key_check').first()` | Consomme un Query ou un résultat : voir l’expression. Query terminal peut exécuter ; Result consomme une exécution antérieure. |
| REQ21_5-0370 | `migrations/versions/c6g200000001_add_comment_likes.py:26` | `inspect_legacy / MAH-F0032` | `sa.inspect(bind)` | Métadonnées de schéma inspectées/réfléchies ; requêtes selon objet et cache ; pas de preuve de base actuelle. |
| REQ21_5-0371 | `migrations/versions/c6g200000001_add_comment_likes.py:28` | `inspect_legacy / MAH-F0032` | `bind.exec_driver_sql('SELECT @@foreign_key_checks')` | Connexion, exécution ou inspection : SQL/effet exact dépend de l’expression et du contexte ; aucun appel effectué ici. |
| REQ21_5-0372 | `migrations/versions/c6g200000001_add_comment_likes.py:28` | `inspect_legacy / MAH-F0032` | `bind.exec_driver_sql('SELECT @@foreign_key_checks').scalar()` | Consomme un Query ou un résultat : voir l’expression. Query terminal peut exécuter ; Result consomme une exécution antérieure. |
| REQ21_5-0373 | `migrations/versions/c6g200000001_add_comment_likes.py:29` | `inspect_legacy / MAH-F0032` | `inspector.get_table_options(name)` | Connexion, exécution ou inspection : SQL/effet exact dépend de l’expression et du contexte ; aucun appel effectué ici. |
| REQ21_5-0374 | `migrations/versions/c6g200000001_add_comment_likes.py:32` | `inspect_legacy / MAH-F0032` | `inspector.has_table('comment_likes')` | Connexion, exécution ou inspection : SQL/effet exact dépend de l’expression et du contexte ; aucun appel effectué ici. |
| REQ21_5-0375 | `migrations/versions/c6g200000001_add_comment_likes.py:36` | `inspect_legacy / MAH-F0032` | `inspector.get_columns(table)` | Connexion, exécution ou inspection : SQL/effet exact dépend de l’expression et du contexte ; aucun appel effectué ici. |
| REQ21_5-0376 | `migrations/versions/c6g200000001_add_comment_likes.py:40` | `inspect_legacy / MAH-F0032` | `sa.Table('comments', sa.MetaData(), autoload_with=bind)` | Métadonnées de schéma inspectées/réfléchies ; requêtes selon objet et cache ; pas de preuve de base actuelle. |
| REQ21_5-0377 | `migrations/versions/c6g200000001_add_comment_likes.py:42` | `inspect_legacy / MAH-F0032` | `bind.execute(sa.select(comments.c.likes))` | Connexion, exécution ou inspection : SQL/effet exact dépend de l’expression et du contexte ; aucun appel effectué ici. |
| REQ21_5-0378 | `migrations/versions/c6g200000001_add_comment_likes.py:42` | `inspect_legacy / MAH-F0032` | `bind.execute(sa.select(comments.c.likes)).scalars()` | Adapte la présentation d’un résultat déjà obtenu ; ne constitue pas à lui seul un nouveau SELECT. |
| REQ21_5-0379 | `migrations/versions/c6g200000001_add_comment_likes.py:42` | `inspect_legacy / MAH-F0032` | `sa.select(comments.c.likes)` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0380 | `migrations/versions/c6g200000001_add_comment_likes.py:49` | `upgrade / MAH-F0033` | `op.get_bind()` | Récupère le bind du contexte ; ne constitue pas à lui seul un DDL, un SELECT ou un commit. |
| REQ21_5-0381 | `migrations/versions/c6g200000001_add_comment_likes.py:50` | `upgrade / MAH-F0033` | `op.create_table('comment_likes', sa.Column('id', sa.Integer(), primary_key=True), sa.Column('comment_id', comment_type, nullable=False), sa.Column('user_id', user_type, nullable=False), sa.Column('created_at', sa.DateTime(), nullable=False), sa.ForeignKeyConstraint(['comment_id'], ['comments.id'], name='fk_comment_likes_comment', ondelete='CASCADE'), sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='fk_comment_likes_user', ondelete='CASCADE'), sa.UniqueConstraint('user_id', 'comment_id', name='unique_user_comment_like'), mysql_engine='InnoDB')` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0382 | `migrations/versions/c6g200000001_add_comment_likes.py:61` | `upgrade / MAH-F0033` | `op.create_index('ix_comment_likes_comment_id', 'comment_likes', ['comment_id'], unique=False)` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0383 | `migrations/versions/c6g200000001_add_comment_likes.py:66` | `downgrade / MAH-F0034` | `op.get_bind()` | Récupère le bind du contexte ; ne constitue pas à lui seul un DDL, un SELECT ou un commit. |
| REQ21_5-0384 | `migrations/versions/c6g200000001_add_comment_likes.py:66` | `downgrade / MAH-F0034` | `sa.Table('comment_likes', sa.MetaData(), autoload_with=op.get_bind())` | Métadonnées de schéma inspectées/réfléchies ; requêtes selon objet et cache ; pas de preuve de base actuelle. |
| REQ21_5-0385 | `migrations/versions/c6g200000001_add_comment_likes.py:67` | `downgrade / MAH-F0034` | `op.get_bind()` | Récupère le bind du contexte ; ne constitue pas à lui seul un DDL, un SELECT ou un commit. |
| REQ21_5-0386 | `migrations/versions/c6g200000001_add_comment_likes.py:67` | `downgrade / MAH-F0034` | `op.get_bind().execute(sa.select(table.c.id).limit(1))` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0387 | `migrations/versions/c6g200000001_add_comment_likes.py:67` | `downgrade / MAH-F0034` | `op.get_bind().execute(sa.select(table.c.id).limit(1)).first()` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0388 | `migrations/versions/c6g200000001_add_comment_likes.py:67` | `downgrade / MAH-F0034` | `sa.select(table.c.id)` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0389 | `migrations/versions/c6g200000001_add_comment_likes.py:67` | `downgrade / MAH-F0034` | `sa.select(table.c.id).limit(1)` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0390 | `migrations/versions/c6g200000001_add_comment_likes.py:69` | `downgrade / MAH-F0034` | `op.drop_index('ix_comment_likes_comment_id', table_name='comment_likes')` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0391 | `migrations/versions/c6g200000001_add_comment_likes.py:70` | `downgrade / MAH-F0034` | `op.drop_table('comment_likes')` | Opération de schéma Alembic ; effet dans un contexte de migration autorisé, non exécuté ici. |
| REQ21_5-0392 | `tools/demo_persistante.py:246` | `opened / MAH-F0064` | `sqlite3.connect(database_uri(path, 'ro' if readonly else 'rw'), uri=True, timeout=5)` | Connexion, exécution ou inspection : SQL/effet exact dépend de l’expression et du contexte ; aucun appel effectué ici. |
| REQ21_5-0393 | `tools/demo_persistante.py:248` | `opened / MAH-F0064` | `connection.execute('PRAGMA foreign_keys=ON')` | Connexion, exécution ou inspection : SQL/effet exact dépend de l’expression et du contexte ; aucun appel effectué ici. |
| REQ21_5-0394 | `tools/demo_persistante.py:249` | `opened / MAH-F0064` | `connection.execute('PRAGMA foreign_keys')` | Connexion, exécution ou inspection : SQL/effet exact dépend de l’expression et du contexte ; aucun appel effectué ici. |
| REQ21_5-0395 | `tools/demo_persistante.py:260` | `inspect_database / MAH-F0065` | `connection.execute('PRAGMA application_id')` | Connexion, exécution ou inspection : SQL/effet exact dépend de l’expression et du contexte ; aucun appel effectué ici. |
| REQ21_5-0396 | `tools/demo_persistante.py:261` | `inspect_database / MAH-F0065` | `connection.execute('PRAGMA user_version')` | Connexion, exécution ou inspection : SQL/effet exact dépend de l’expression et du contexte ; aucun appel effectué ici. |
| REQ21_5-0397 | `tools/demo_persistante.py:263` | `inspect_database / MAH-F0065` | `connection.execute("SELECT name,sql FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")` | Connexion, exécution ou inspection : SQL/effet exact dépend de l’expression et du contexte ; aucun appel effectué ici. |
| REQ21_5-0398 | `tools/demo_persistante.py:268` | `inspect_database / MAH-F0065` | `connection.execute('PRAGMA integrity_check')` | Connexion, exécution ou inspection : SQL/effet exact dépend de l’expression et du contexte ; aucun appel effectué ici. |
| REQ21_5-0399 | `tools/demo_persistante.py:269` | `inspect_database / MAH-F0065` | `connection.execute('PRAGMA foreign_key_check')` | Connexion, exécution ou inspection : SQL/effet exact dépend de l’expression et du contexte ; aucun appel effectué ici. |
| REQ21_5-0400 | `tools/demo_persistante.py:271` | `inspect_database / MAH-F0065` | `connection.execute('PRAGMA journal_mode')` | Connexion, exécution ou inspection : SQL/effet exact dépend de l’expression et du contexte ; aucun appel effectué ici. |
| REQ21_5-0401 | `tools/demo_persistante.py:273` | `inspect_database / MAH-F0065` | `connection.execute('SELECT COUNT(*) FROM ' + name)` | Connexion, exécution ou inspection : SQL/effet exact dépend de l’expression et du contexte ; aucun appel effectué ici. |
| REQ21_5-0402 | `tools/demo_persistante.py:276` | `inspect_database / MAH-F0065` | `connection.execute('SELECT ' + ','.join(FIELDS) + ',archived_at FROM stories WHERE id=?', (original['id'],))` | Connexion, exécution ou inspection : SQL/effet exact dépend de l’expression et du contexte ; aucun appel effectué ici. |
| REQ21_5-0403 | `tools/demo_persistante.py:282` | `inspect_database / MAH-F0065` | `connection.execute('SELECT username,is_admin,is_banned FROM users WHERE username IN (?,?,?)', NAMES)` | Connexion, exécution ou inspection : SQL/effet exact dépend de l’expression et du contexte ; aucun appel effectué ici. |
| REQ21_5-0404 | `tools/demo_persistante.py:339` | `application.connect / MAH-F0071` | `connection.execute('PRAGMA foreign_keys=ON')` | Connexion, exécution ou inspection : SQL/effet exact dépend de l’expression et du contexte ; aucun appel effectué ici. |
| REQ21_5-0405 | `tools/demo_persistante.py:340` | `application.connect / MAH-F0071` | `connection.execute('PRAGMA foreign_keys')` | Connexion, exécution ou inspection : SQL/effet exact dépend de l’expression et du contexte ; aucun appel effectué ici. |
| REQ21_5-0406 | `tools/demo_persistante.py:350` | `application.configure / MAH-F0073` | `init_app(app)` | Déclaration/configuration, sauf create_all qui peut créer le schéma quand appelé ; pas un seed automatique. |
| REQ21_5-0407 | `tools/demo_persistante.py:378` | `application / MAH-F0068` | `db.session.remove()` | Connexion, exécution ou inspection : SQL/effet exact dépend de l’expression et du contexte ; aucun appel effectué ici. |
| REQ21_5-0408 | `tools/demo_persistante.py:464` | `initialize / MAH-F0083` | `db.create_all()` | Déclaration/configuration, sauf create_all qui peut créer le schéma quand appelé ; pas un seed automatique. |
| REQ21_5-0409 | `tools/demo_persistante.py:465` | `initialize / MAH-F0083` | `db.session.execute(db.text(f'PRAGMA application_id={APPLICATION_ID}'))` | Connexion, exécution ou inspection : SQL/effet exact dépend de l’expression et du contexte ; aucun appel effectué ici. |
| REQ21_5-0410 | `tools/demo_persistante.py:465` | `initialize / MAH-F0083` | `db.text(f'PRAGMA application_id={APPLICATION_ID}')` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0411 | `tools/demo_persistante.py:466` | `initialize / MAH-F0083` | `db.session.execute(db.text(f'PRAGMA user_version={FORMAT}'))` | Connexion, exécution ou inspection : SQL/effet exact dépend de l’expression et du contexte ; aucun appel effectué ici. |
| REQ21_5-0412 | `tools/demo_persistante.py:466` | `initialize / MAH-F0083` | `db.text(f'PRAGMA user_version={FORMAT}')` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0413 | `tools/demo_persistante.py:468` | `initialize / MAH-F0083` | `models.User(id=identifier, username=person.username, email=person.email, is_admin=identifier == 1, is_banned=False)` | Objet en mémoire ; aucun INSERT par cette seule construction. Defaults/PK possibles au flush. |
| REQ21_5-0414 | `tools/demo_persistante.py:471` | `initialize / MAH-F0083` | `db.session.add(user)` | Inscription d’objet(s) dans la Session ; écriture au flush, pas validation durable. |
| REQ21_5-0415 | `tools/demo_persistante.py:472` | `initialize / MAH-F0083` | `db.session.add_all([models.Category(id=1, name='Histoires résolues'), models.Category(id=2, name='Cold Cases')])` | Inscription d’objet(s) dans la Session ; écriture au flush, pas validation durable. |
| REQ21_5-0416 | `tools/demo_persistante.py:472` | `initialize / MAH-F0083` | `models.Category(id=1, name='Histoires résolues')` | Objet en mémoire ; aucun INSERT par cette seule construction. Defaults/PK possibles au flush. |
| REQ21_5-0417 | `tools/demo_persistante.py:472` | `initialize / MAH-F0083` | `models.Category(id=2, name='Cold Cases')` | Objet en mémoire ; aucun INSERT par cette seule construction. Defaults/PK possibles au flush. |
| REQ21_5-0418 | `tools/demo_persistante.py:473` | `initialize / MAH-F0083` | `db.session.flush()` | DML envoyé dans la transaction ; contraintes et identifiants générés ; pas commit. |
| REQ21_5-0419 | `tools/demo_persistante.py:475` | `initialize / MAH-F0083` | `db.session.add(models.Story(**{key: row[key] for key in FIELDS}, author_id=1))` | Inscription d’objet(s) dans la Session ; écriture au flush, pas validation durable. |
| REQ21_5-0420 | `tools/demo_persistante.py:475` | `initialize / MAH-F0083` | `models.Story(**{key: row[key] for key in FIELDS}, author_id=1)` | Objet en mémoire ; aucun INSERT par cette seule construction. Defaults/PK possibles au flush. |
| REQ21_5-0421 | `tools/demo_persistante.py:476` | `initialize / MAH-F0083` | `db.session.commit()` | Flush requis puis validation ; résultat réseau ultérieur distinct de la réussite du commit. |
| REQ21_5-0422 | `tools/demo_persistante.py:496` | `_copy_database / MAH-F0085` | `reader.backup(writer)` | Copie de base par API DBAPI ; pas une requête ORM, non exécutée dans ce lot. |
| REQ21_5-0423 | `tools/recette_lot6g4.py:251` | `check_historical_journey.sql_state / MAH-F0112` | `db.func.count()` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0424 | `tools/recette_lot6g4.py:251` | `check_historical_journey.sql_state / MAH-F0112` | `db.select(db.func.count())` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0425 | `tools/recette_lot6g4.py:251` | `check_historical_journey.sql_state / MAH-F0112` | `db.select(db.func.count()).select_from(table)` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0426 | `tools/recette_lot6g4.py:251` | `check_historical_journey.sql_state / MAH-F0112` | `db.session.execute(db.select(db.func.count()).select_from(table))` | Connexion, exécution ou inspection : SQL/effet exact dépend de l’expression et du contexte ; aucun appel effectué ici. |
| REQ21_5-0427 | `tools/recette_lot6g4.py:251` | `check_historical_journey.sql_state / MAH-F0112` | `db.session.execute(db.select(db.func.count()).select_from(table)).scalar_one()` | Consomme un Query ou un résultat : voir l’expression. Query terminal peut exécuter ; Result consomme une exécution antérieure. |
| REQ21_5-0428 | `tools/recette_lot6g4.py:321` | `check_historical_journey / MAH-F0109` | `all((row[field] == source[field] for field in ('title', 'summary', 'content', 'slug', 'category_id')))` | Consomme un Query ou un résultat : voir l’expression. Query terminal peut exécuter ; Result consomme une exécution antérieure. |
| REQ21_5-0429 | `tools/recette_lot6g4.py:333` | `seed / MAH-F0113` | `models.User(id=number, username=username, email=name + '6g4@example.invalid', is_admin=name == 'admin', is_banned=False)` | Objet en mémoire ; aucun INSERT par cette seule construction. Defaults/PK possibles au flush. |
| REQ21_5-0430 | `tools/recette_lot6g4.py:336` | `seed / MAH-F0113` | `db.session.add(user)` | Inscription d’objet(s) dans la Session ; écriture au flush, pas validation durable. |
| REQ21_5-0431 | `tools/recette_lot6g4.py:338` | `seed / MAH-F0113` | `models.Category(id=1, name='Histoires résolues')` | Objet en mémoire ; aucun INSERT par cette seule construction. Defaults/PK possibles au flush. |
| REQ21_5-0432 | `tools/recette_lot6g4.py:338` | `seed / MAH-F0113` | `db.session.add_all([models.Category(id=1, name='Histoires résolues'), models.Category(id=2, name='Cold Cases')])` | Inscription d’objet(s) dans la Session ; écriture au flush, pas validation durable. |
| REQ21_5-0433 | `tools/recette_lot6g4.py:339` | `seed / MAH-F0113` | `models.Category(id=2, name='Cold Cases')` | Objet en mémoire ; aucun INSERT par cette seule construction. Defaults/PK possibles au flush. |
| REQ21_5-0434 | `tools/recette_lot6g4.py:340` | `seed / MAH-F0113` | `db.session.flush()` | DML envoyé dans la transaction ; contraintes et identifiants générés ; pas commit. |
| REQ21_5-0435 | `tools/recette_lot6g4.py:344` | `seed / MAH-F0113` | `db.session.add(models.Story(**values, author_id=1))` | Inscription d’objet(s) dans la Session ; écriture au flush, pas validation durable. |
| REQ21_5-0436 | `tools/recette_lot6g4.py:344` | `seed / MAH-F0113` | `models.Story(**values, author_id=1)` | Objet en mémoire ; aucun INSERT par cette seule construction. Defaults/PK possibles au flush. |
| REQ21_5-0437 | `tools/recette_lot6g4.py:347` | `seed / MAH-F0113` | `db.session.add(models.Story(id=identifier, slug=slug, title='Dossier fictif ' + str(identifier), summary='Démonstration isolée uniquement.', content='Contenu fictif de recette.', image_url='/images/default-story.svg', category_id=category, author_id=1))` | Inscription d’objet(s) dans la Session ; écriture au flush, pas validation durable. |
| REQ21_5-0438 | `tools/recette_lot6g4.py:347` | `seed / MAH-F0113` | `models.Story(id=identifier, slug=slug, title='Dossier fictif ' + str(identifier), summary='Démonstration isolée uniquement.', content='Contenu fictif de recette.', image_url='/images/default-story.svg', category_id=category, author_id=1)` | Objet en mémoire ; aucun INSERT par cette seule construction. Defaults/PK possibles au flush. |
| REQ21_5-0439 | `tools/recette_lot6g4.py:350` | `seed / MAH-F0113` | `db.session.commit()` | Flush requis puis validation ; résultat réseau ultérieur distinct de la réussite du commit. |
| REQ21_5-0440 | `tools/recette_lot6g4.py:355` | `seven_counts / MAH-F0114` | `models.Story.query.filter_by(archived_at=None)` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0441 | `tools/recette_lot6g4.py:355` | `seven_counts / MAH-F0114` | `models.Story.query.filter_by(archived_at=None).count()` | Query.count exécute un décompte ; ne pas confondre avec la construction func.count. |
| REQ21_5-0442 | `tools/recette_lot6g4.py:356` | `seven_counts / MAH-F0114` | `models.Story.query.filter_by(archived_at=None, category_id=1)` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0443 | `tools/recette_lot6g4.py:356` | `seven_counts / MAH-F0114` | `models.Story.query.filter_by(archived_at=None, category_id=1).count()` | Query.count exécute un décompte ; ne pas confondre avec la construction func.count. |
| REQ21_5-0444 | `tools/recette_lot6g4.py:357` | `seven_counts / MAH-F0114` | `models.Story.query.filter_by(archived_at=None, category_id=2)` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0445 | `tools/recette_lot6g4.py:357` | `seven_counts / MAH-F0114` | `models.Story.query.filter_by(archived_at=None, category_id=2).count()` | Query.count exécute un décompte ; ne pas confondre avec la construction func.count. |
| REQ21_5-0446 | `tools/recette_lot6g4.py:358` | `seven_counts / MAH-F0114` | `models.Comment.query.count()` | Query.count exécute un décompte ; ne pas confondre avec la construction func.count. |
| REQ21_5-0447 | `tools/recette_lot6g4.py:358` | `seven_counts / MAH-F0114` | `models.User.query.count()` | Query.count exécute un décompte ; ne pas confondre avec la construction func.count. |
| REQ21_5-0448 | `tools/recette_lot6g4.py:359` | `seven_counts / MAH-F0114` | `models.Report.query.count()` | Query.count exécute un décompte ; ne pas confondre avec la construction func.count. |
| REQ21_5-0449 | `tools/recette_lot6g4.py:360` | `seven_counts / MAH-F0114` | `models.Proposal.query.filter_by(status='pending')` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0450 | `tools/recette_lot6g4.py:360` | `seven_counts / MAH-F0114` | `models.Proposal.query.filter_by(status='pending').count()` | Query.count exécute un décompte ; ne pas confondre avec la construction func.count. |
| REQ21_5-0451 | `tools/recette_lot6g4.py:378` | `inspect_assets / MAH-F0115` | `all((path in PUBLIC for path in parsed.paths))` | Consomme un Query ou un résultat : voir l’expression. Query terminal peut exécuter ; Result consomme une exécution antérieure. |
| REQ21_5-0452 | `tools/recette_lot6g4.py:427` | `check_journey / MAH-F0118` | `models.Comment(story_id=42, user_id=2, username='jury6g4_alice', text='Témoin historique strictement synthétique.', likes=7)` | Objet en mémoire ; aucun INSERT par cette seule construction. Defaults/PK possibles au flush. |
| REQ21_5-0453 | `tools/recette_lot6g4.py:429` | `check_journey / MAH-F0118` | `db.session.add(legacy)` | Inscription d’objet(s) dans la Session ; écriture au flush, pas validation durable. |
| REQ21_5-0454 | `tools/recette_lot6g4.py:429` | `check_journey / MAH-F0118` | `db.session.commit()` | Flush requis puis validation ; résultat réseau ultérieur distinct de la réussite du commit. |
| REQ21_5-0455 | `tools/recette_lot6g4.py:434` | `check_journey / MAH-F0118` | `db.session.get(models.Comment, legacy_id)` | Identité ORM ou None ; SELECT si l’état de Session l’exige. |
| REQ21_5-0456 | `tools/recette_lot6g4.py:437` | `check_journey / MAH-F0118` | `db.func.count()` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0457 | `tools/recette_lot6g4.py:437` | `check_journey / MAH-F0118` | `db.select(db.func.count())` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0458 | `tools/recette_lot6g4.py:437` | `check_journey / MAH-F0118` | `db.select(db.func.count()).select_from(table)` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0459 | `tools/recette_lot6g4.py:437` | `check_journey / MAH-F0118` | `db.session.execute(db.select(db.func.count()).select_from(table))` | Connexion, exécution ou inspection : SQL/effet exact dépend de l’expression et du contexte ; aucun appel effectué ici. |
| REQ21_5-0460 | `tools/recette_lot6g4.py:437` | `check_journey / MAH-F0118` | `db.session.execute(db.select(db.func.count()).select_from(table)).scalar_one()` | Consomme un Query ou un résultat : voir l’expression. Query terminal peut exécuter ; Result consomme une exécution antérieure. |
| REQ21_5-0461 | `tools/recette_lot6g4.py:443` | `check_journey / MAH-F0118` | `db.func.count()` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0462 | `tools/recette_lot6g4.py:443` | `check_journey / MAH-F0118` | `db.select(db.func.count())` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0463 | `tools/recette_lot6g4.py:443` | `check_journey / MAH-F0118` | `db.select(db.func.count()).select_from(table)` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0464 | `tools/recette_lot6g4.py:443` | `check_journey / MAH-F0118` | `db.session.execute(db.select(db.func.count()).select_from(table))` | Connexion, exécution ou inspection : SQL/effet exact dépend de l’expression et du contexte ; aucun appel effectué ici. |
| REQ21_5-0465 | `tools/recette_lot6g4.py:443` | `check_journey / MAH-F0118` | `db.session.execute(db.select(db.func.count()).select_from(table)).scalar_one()` | Consomme un Query ou un résultat : voir l’expression. Query terminal peut exécuter ; Result consomme une exécution antérieure. |
| REQ21_5-0466 | `tools/recette_lot6g4.py:511` | `main / MAH-F0121` | `sqlite3.connect(str(evidence / 'forbidden.sqlite3'))` | Connexion, exécution ou inspection : SQL/effet exact dépend de l’expression et du contexte ; aucun appel effectué ici. |
| REQ21_5-0467 | `tools/recette_lot6g4.py:548` | `main.connect / MAH-F0129` | `connection.execute('PRAGMA foreign_keys=ON')` | Connexion, exécution ou inspection : SQL/effet exact dépend de l’expression et du contexte ; aucun appel effectué ici. |
| REQ21_5-0468 | `tools/recette_lot6g4.py:549` | `main.connect / MAH-F0129` | `connection.execute('PRAGMA foreign_keys')` | Connexion, exécution ou inspection : SQL/effet exact dépend de l’expression et du contexte ; aucun appel effectué ici. |
| REQ21_5-0469 | `tools/recette_lot6g4.py:583` | `main / MAH-F0121` | `all((not os.environ[key] for key in AIVEN))` | Consomme un Query ou un résultat : voir l’expression. Query terminal peut exécuter ; Result consomme une exécution antérieure. |
| REQ21_5-0470 | `tools/recette_lot6g4.py:584` | `main / MAH-F0121` | `db.create_all()` | Déclaration/configuration, sauf create_all qui peut créer le schéma quand appelé ; pas un seed automatique. |
| REQ21_5-0471 | `tools/recette_lot6g4.py:596` | `main / MAH-F0121` | `db.session.execute(db.text('PRAGMA foreign_keys'))` | Connexion, exécution ou inspection : SQL/effet exact dépend de l’expression et du contexte ; aucun appel effectué ici. |
| REQ21_5-0472 | `tools/recette_lot6g4.py:596` | `main / MAH-F0121` | `db.session.execute(db.text('PRAGMA foreign_keys')).scalar_one()` | Consomme un Query ou un résultat : voir l’expression. Query terminal peut exécuter ; Result consomme une exécution antérieure. |
| REQ21_5-0473 | `tools/recette_lot6g4.py:596` | `main / MAH-F0121` | `db.text('PRAGMA foreign_keys')` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0474 | `tools/recette_lot6g4.py:597` | `main / MAH-F0121` | `db.session.execute(db.text('PRAGMA foreign_key_check'))` | Connexion, exécution ou inspection : SQL/effet exact dépend de l’expression et du contexte ; aucun appel effectué ici. |
| REQ21_5-0475 | `tools/recette_lot6g4.py:597` | `main / MAH-F0121` | `db.session.execute(db.text('PRAGMA foreign_key_check')).all()` | Consomme un Query ou un résultat : voir l’expression. Query terminal peut exécuter ; Result consomme une exécution antérieure. |
| REQ21_5-0476 | `tools/recette_lot6g4.py:597` | `main / MAH-F0121` | `db.text('PRAGMA foreign_key_check')` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0477 | `tools/recette_lot6g4.py:598` | `main / MAH-F0121` | `all((row[2] == '' for row in db.session.execute(db.text('PRAGMA database_list'))))` | Consomme un Query ou un résultat : voir l’expression. Query terminal peut exécuter ; Result consomme une exécution antérieure. |
| REQ21_5-0478 | `tools/recette_lot6g4.py:598` | `main / MAH-F0121` | `db.session.execute(db.text('PRAGMA database_list'))` | Connexion, exécution ou inspection : SQL/effet exact dépend de l’expression et du contexte ; aucun appel effectué ici. |
| REQ21_5-0479 | `tools/recette_lot6g4.py:598` | `main / MAH-F0121` | `db.text('PRAGMA database_list')` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |
| REQ21_5-0480 | `tools/recette_lot6g4.py:607` | `main / MAH-F0121` | `isolation.counts.values()` | Configure une expression ou un chargement ; exécution par une opération terminale ultérieure. |

### Mutations d’attributs préparant un état ORM

| Emplacement | Fonction | Affectation repérée | Interprétation |
|---|---|---|---|
| `backend/api/v1/views/admin_stories.py:104` | `set_story_archive` | `story.archived_at = datetime.utcnow() if archived else None` | mutation Python ; SQL effectif dépend du flush ou du chemin Core |
| `backend/api/v1/views/admin_stories.py:105` | `set_story_archive` | `story.management_revision = uuid4().hex` | mutation Python ; SQL effectif dépend du flush ou du chemin Core |
| `backend/api/v1/views/admin_users_support.py:39` | `ban_user_account` | `user.is_banned = True` | mutation Python ; SQL effectif dépend du flush ou du chemin Core |
| `backend/models.py:45` | `User.set_password` | `self.password_hash = generate_password_hash(password)` | mutation Python ; SQL effectif dépend du flush ou du chemin Core |
| `backend/models.py:550` | `Report.target_id` | `self.comment_id = int(value)` | mutation Python ; SQL effectif dépend du flush ou du chemin Core |

Les mutations repérées ciblent les attributs sensibles de gestion, compteurs et compatibilité. Ce tableau n’invente pas de DML immédiat et ne prétend pas analyser toutes les mutations possibles d’objets dynamiques. Le [Transactions et intégrité](02_GUIDE_TRANSACTIONS_INTEGRITE_LOT6H21_5.md) replace ces opérations dans leurs transactions ; le [Parcours fonctionnels complets](03_GUIDE_PARCOURS_FONCTIONNELS_LOT6H21_5.md) suit chaque parcours HTTP.
