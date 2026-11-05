# Transactions et intégrité — lot 6H.21.5

Les Petits Enquêteurs — préparation pour Mahamadou — **5 novembre 2026, Europe/Paris**.

**Proposition documentaire externe, sans installation autorisée.** Référence : 203 fichiers de la copie intégrée, vérifiés par empreintes. Aucun module applicatif importé, aucun accès SQL, aucune migration, aucun test applicatif ni intervention sur le serveur 5066. Les exemples sont des illustrations non exécutées, pas des commandes à lancer sur une base réelle. Les responsabilités BDD de Mahamadou sont distinguées des composants partagés avec Sylvie et du frontend de Mélissa.

[Sommaire des huit guides](01_GUIDE_REQUETES_SQLALCHEMY_LOT6H21_5.md#sommaire) · [Références exactes et soutenance](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md) · [Contrôles et limites](08_VALIDATION_DOCUMENTAIRE_LOT6H21_5.md)

## Distinguer trois sessions ou durées de vie

| Objet | Rôle dans le projet | Ce qu’il ne contient pas |
|---|---|---|
| Session Flask | État signé transmis par cookie : user_id, indicateur de rôle, jeton CSRF | Ce n’est pas une transaction SQL ni une table de connexions actives |
| Session SQLAlchemy | Identités ORM suivies, changements en attente et accès transactionnel | Ce n’est pas une preuve que l’utilisateur est connecté |
| Connexion/transaction du moteur | Conversation avec une base et limites de validation/annulation | Elle ne couvre pas automatiquement la saisie humaine ou la réception HTTP |

Une même requête peut lire le cookie, retrouver le compte avec db.session.get, programmer un INSERT et le valider. Le cookie peut persister plusieurs requêtes, tandis que la Session de Flask-SQLAlchemy est liée au contexte applicatif. Le contexte gère son nettoyage ; il ne commite pas les écritures métier à la place des vues. [Contexte Flask-SQLAlchemy officiel](https://flask-sqlalchemy.palletsprojects.com/en/stable/contexts/).

## Une unité de travail, pas une liste de commandes immédiatement durables

La Session maintient une identité d’objet par clé dans son contexte et suit des états : transitoire, pending, persistent, deleted/detached selon le parcours. add rend un objet éligible à l’insertion ; une affectation sur un objet suivi le rend dirty ; delete programme une suppression d’objet. Le flush synchronise ces états par DML dans une transaction.

Le code utilise des requêtes avant les écritures ; une transaction peut donc être engagée automatiquement par la Session avant le bloc try de commit. Il ne faut pas chercher un BEGIN Python explicite dans chaque vue pour conclure qu’il existe une transaction. Inversement, construire select ou where n’ouvre pas à lui seul une connexion. Les détails du début physique de transaction dépendent du pilote et du dialecte.

La distinction entre ajout, flush, validation, annulation et expiration est décrite dans les [principes officiels de Session SQLAlchemy](https://docs.sqlalchemy.org/en/20/orm/session_basics.html). Les paragraphes qui suivent l’appliquent aux branches réellement présentes du projet, sans invoquer ces fonctions sur une base.

### Opérations de Session, retour et effets

| Opération | Entrée attendue | Action immédiate à comprendre | Retour usuel | Suite nécessaire |
|---|---|---|---|---|
| add(objet) | Objet mappé | Suivi de l’objet et de cascades save-update pertinentes | None | Flush/commit par l’appelant |
| add_all(objets) | Itérable d’objets mappés | Même inscription pour plusieurs objets | None | Ne vaut pas un INSERT multiple déjà validé |
| delete(objet) | Objet suivi ou attachable pertinent | Programme sa suppression ORM et effets de relations | None | DELETE au flush ; cascades à examiner |
| flush() | Changements de la Session | Émet les DML nécessaires ; vérifie des contraintes ; obtient des PK | None | Commit pour valider, rollback si échec |
| commit() | Transaction et changements courants | Flush requis puis validation | None | Une réponse HTTP peut encore échouer |
| rollback() | État transactionnel courant | Annulation/finalisation locale et remise en état | None | Ne prouve pas qu’un COMMIT incertain côté réseau a échoué |
| refresh(objet) | Objet persistant | Recharge ses attributs avec une lecture | None | Ne crée pas un nouvel objet métier |
| expire_all() | Objets de la Session | Marque leurs valeurs comme expirées | None | Lectures ultérieures possibles, pas SELECT immédiat de toutes les tables |
| remove() | Session contextualisée | Ferme/retire la Session du contexte courant | None | Pas une validation de transaction |

Le parcours de purge actuel n’utilise pas Session.delete(story) : il exécute des DELETE Core conditionnels et vérifie leurs rowcount. La différence de mécanisme compte pour les cascades ORM et la synchronisation de l’état Python.

### Quand les valeurs automatiques deviennent disponibles

Les id générés, dates par default et UUID de gestion ne sont pas nécessairement assignés à la simple construction. Flush prépare les INSERT et rend disponibles les valeurs nécessaires au résultat selon le mapping et le moteur. Les dates default/onupdate Python ne sont pas des triggers SQL permanents ; la sentinelle SQL de management_revision est un mécanisme séparé.

Un objet construit avec des champs manquants peut exister en Python puis échouer au flush. Un to_dict sur un objet incomplet n’est pas une preuve d’INSERT ; Report.target_id peut même produire « None » si comment_id manque. Les guides du lot 6H.21.4 détaillent ces contrats sans qu’il soit nécessaire de les réécrire.

## ACID appliqué aux vrais parcours

| Principe | Sens simple | Exemple fidèle | Limite à expliquer |
|---|---|---|---|
| Atomicité | Une transaction valide un ensemble cohérent ou l’annule avant validation, selon le moteur | Réservation de révision et suppression des dépendances dans delete_story | Une réponse perdue à COMMIT peut rendre l’issue inconnue ; les DDL MySQL ont d’autres règles |
| Cohérence | Les invariants couverts restent respectés lors des opérations acceptées | FK, UNIQUE de couple, NOT NULL et contrôles d’auteur côté API | Les statuts et droits non exprimés en SQL nécessitent les contrôles serveur |
| Isolation | Les transactions concurrentes voient/interagissent selon les règles du moteur | Demande de verrou du parent avant contribution et archivage | Un test SQLite ne démontre pas une lecture FOR UPDATE InnoDB |
| Durabilité | Après validation réussie, les changements persistent selon la configuration du moteur/stockage | Un commentaire dans une base fichier peut survivre au redémarrage du service | Une base mémoire disparaît avec sa connexion/processus ; un cookie de connexion et une sauvegarde sont d’autres objets |

Ces principes ne doivent pas être récités comme une garantie universelle du framework. Le moteur, le mode de journal, les réglages de durabilité, le système de fichiers et la procédure de sauvegarde participent au résultat. Le projet ne configure pas un niveau d’isolation identique pour tous ses modes et ne fournit pas une mesure nouvelle de tenue aux pannes dans ce lot.

## Parcours de création : inscription, commentaire, théorie, proposition

Les vues valident l’entrée, récupèrent les parents pertinents, construisent l’objet et entrent dans un try contenant add puis commit. Sur exception SQL gérée, rollback remet la Session en état et la vue renvoie une erreur neutre. L’inscription distingue IntegrityError pour les uniques métier ; les contributions utilisent généralement SQLAlchemyError.

La sérialisation de plusieurs de ces parcours a lieu **après commit**, hors du try d’écriture. Un objet expiré peut être relu ; comment_to_dict effectue en outre des comptages. Une panne de cette lecture peut empêcher la réponse même si l’INSERT a déjà été validé. Il serait incorrect de promettre « erreur réseau ou 500 signifie aucun enregistrement ».

Fonctions à suivre : [MAH-F0207 — register_user](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0207), [MAH-F0157 — post_story_comment](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0157), [MAH-F0203 — post_theory](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0203) et [MAH-F0182 — create_proposal](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0182).

### Exemple Python pédagogique : conserver le point de décision

Exemple non exécuté. La Session et les classes sont fournies comme paramètres ; aucune configuration ni connexion n’est ouverte par ce document. Il reprend la structure du like de commentaire avec un résultat préparé avant commit. La route réelle effectue aussi l’authentification, la visibilité, la compatibilité historique et la reconnaissance précise des erreurs.

```python
def illustrer_association(db, CommentLike, compte_id, commentaire_id):
    from sqlalchemy.exc import SQLAlchemyError
    try:
        association = CommentLike(user_id=compte_id, comment_id=commentaire_id)
        db.session.add(association)
        db.session.flush()
        resultat = {
            "id": association.id,
            "likes": CommentLike.query.filter_by(comment_id=commentaire_id).count(),
        }
        db.session.commit()
        return resultat
    except SQLAlchemyError:
        db.session.rollback()
        raise
```

La portée try couvre ici le comptage avant commit. Elle ne rend pas la livraison du dictionnaire au navigateur transactionnelle avec l’INSERT. Un programme appelant doit toujours considérer l’échec ou la perte d’accusé après validation.

## IntegrityError : une catégorie technique, plusieurs causes

Une IntegrityError peut correspondre à UNIQUE, à une FK ou à une obligation de valeur. Le projet ne transforme en erreur métier de doublon que les formats et contraintes reconnus : noms MySQL attendus ou ensemble de colonnes SQLite attendu. Une autre contrainte doit rester un échec serveur, pas être maquillée en « déjà aimé ».

[MAH-F0212 — is_unique_conflict](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0212) reçoit l’exception et deux ensembles de contraintes autorisées. Le helper inspecte error.orig et args ; il ne se contente pas d’imprimer toute l’exception. Cela évite de divulguer des données tout en refusant des formats non reconnus. Les tests qui injectent un code MySQL 1062 vérifient le parseur d’erreurs, pas un serveur MySQL réel.

Après un échec de flush, la Session nécessite un rollback explicite avant réutilisation dans le chemin géré. Sinon une opération ultérieure peut échouer à cause de l’état transactionnel invalide, même si son SQL serait correct. Le rollback restaure le cadre de travail ; il ne doit pas servir à masquer silencieusement la cause métier.

### Sept règles UNIQUE et treize FK

Pseudo, e-mail, nom de catégorie, slug et révision de gestion sont uniques individuellement. Les likes de dossier et de commentaire ajoutent chacun une unicité de couple. Chaque table a en plus sa propre PK. Les treize FK ont neuf CASCADE, deux SET NULL et deux sans ON DELETE explicite.

L’API empêche un compte client de s’attribuer arbitrairement un auteur ; la FK vérifie l’existence d’une ligne, pas la légitimité de la requête. Les statuts de proposition et de signalement sont des chaînes ; le modèle ne fournit pas d’ENUM de toutes les transitions. Le rôle, l’archive et la catégorie restent à contrôler dans les bons services.

Les cascades ORM ne sont pas identiques à ON DELETE SQL. Les collections de Story sont delete-orphan, mais toutes celles de User ne sont pas des cascades de suppression. Supprimer un User via ORM peut provoquer une dissociation incompatible avec une FK obligatoire. La route de bannissement ne fait pas cela : elle change is_banned. SET NULL laisse les textes et pseudos copiés ; ce n’est pas un effacement personnel complet.

## Trois scénarios de concurrence

### Deux clics sur le même like individuel

Deux requêtes peuvent lire l’absence du même couple. La première écriture valide une ligne ; la seconde heurte UNIQUE si elle n’a pas été arrêtée avant. Le try d’écriture traduit seulement la contrainte attendue en conflit, rollback puis 409 pour un like. Le retrait filtre cible et compte ; zéro ligne retirée devient changed=False. Le navigateur relit l’état après un conflit plutôt que de répéter le POST.

### Une contribution face à un archivage

get_active_story(lock=True) demande une relecture verrouillante du dossier actif. set_story_archive demande le verrou du même parent avant d’affecter sa date et sa révision. Sous InnoDB, l’intention est de coordonner ces écrivains ; le comportement réel dépend de l’isolation, des index et de la transaction. SQLite ne fournit pas ce même verrou de ligne SQL. Une suite SQLite ne doit pas être présentée comme preuve d’ordonnancement MySQL.

Références : [MAH-F0200 — get_active_story](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0200) et [MAH-F0147 — set_story_archive](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0147).

### Une suppression face à une nouvelle dépendance

Le parcours de purge a plusieurs phases HTTP. Il ne garde pas de verrou pendant la saisie humaine : preview et confirmation terminent leurs lectures par rollback. À chaque étape, le code revalide les droits et l’état. Le DELETE final combine révision, hash de graphe, ETag, validité temporelle, réservation conditionnelle et vérification des nombres supprimés. Aucun de ces mécanismes isolé ne suffit à décrire le parcours entier.

Le hash contient aussi les likes de commentaires, même si le reçu public ne les affiche pas comme sixième compteur. Les contrôles finaux recherchent les ids anciens par lots, avant commit. La transaction finale est courte au regard de la saisie, mais sa durée réelle dépend du volume et du moteur.

Références : [MAH-F0196 — deletion_preview](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0196), [MAH-F0197 — confirm_deletion](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0197), [MAH-F0198 — delete_story](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0198).

## Deux familles d’échecs à ne pas mélanger

| Échec | Connaissance possible | Action du code concerné | Ce qu’on ne peut pas conclure |
|---|---|---|---|
| Validation avant DML | L’entrée ou la permission est refusée | Retour 400/401/403/404, parfois 409/428/412 selon parcours | Toute absence de permission ne produit pas forcément la même forme JSON |
| Erreur de flush gérée avant commit | L’écriture du chemin a échoué avant validation connue | Rollback et erreur adaptée | Que toutes les autres opérations du système ont été annulées |
| Échec SQL avant le try local | La vue peut ne pas avoir de traitement métier spécifique | Gestion Flask/teardown ; JSON garanti seulement par les chemins réellement couverts | Que toute SQLAlchemyError est convertie uniformément en JSON par le projet |
| Erreur de commit de purge | Un accusé a pu être perdu après validation côté base | Rollback local, 503 DELETE_STATUS_UNKNOWN | Que la base a nécessairement annulé le DELETE |
| Timeout du navigateur | Le client cesse d’attendre | Contrôles d’incertitude selon la page, pas retry automatique par apiRequest | Que le serveur a interrompu sa transaction |
| Réponse de succès illisible | La réponse n’est pas exploitable | INVALID_JSON ou validation de contrat, sans nouveau POST automatique | Que la donnée n’a pas été enregistrée |

Le code de purge traite spécialement l’issue inconnue de commit ; ce comportement ne doit pas être attribué à toutes les routes. Les vues de création ont leurs propres limites. Le frontend de proposition réactive notamment son bouton après erreur et ne possède pas le même verrou d’incertitude que commentaires et théories : une nouvelle soumission manuelle reste possible.

## SQLite, MySQL et limites de preuve

Les détails d’isolation SQLite dépendent entre autres du journal et des connexions. Il ne faut pas déduire une lecture de ligne verrouillée à partir de with_for_update en SQLite. Le mode persistant livré vérifie un journal delete ; cela ne constitue pas une mesure de tous les scénarios concurrents du site. [Isolation SQLite officielle](https://www.sqlite.org/isolation.html).

InnoDB dispose de lectures verrouillantes, dont FOR UPDATE et les variantes de verrou partagé selon serveur/dialecte. Les demandes de verrou du code ne prouvent pas leur fonctionnement sur Aiven dans cette session. [Lectures verrouillantes MySQL](https://dev.mysql.com/doc/refman/8.4/en/innodb-locking-reads.html).

Le DML transactionnel et le DDL des migrations doivent être distingués. Certaines instructions de schéma MySQL causent des commits implicites ; un with begin_transaction Alembic ne rend pas toute une chaîne de DDL annulable. Le scope SQLite des migrations emploie un BEGIN explicite et des contrôles FK, sans imposer à lui seul une maintenance exclusive système. [Commits implicites MySQL](https://dev.mysql.com/doc/refman/8.4/en/implicit-commit.html).

## Réponse longue possible à une relance du jury

« La Session représente l’unité de travail ORM. add prépare les objets ; flush envoie les changements et permet d’obtenir leurs identifiants, mais je peux encore annuler la transaction. commit réalise le flush nécessaire puis valide. En cas d’erreur gérée, rollback remet la Session en état. Je distingue aussi le succès SQL de la réponse reçue : un timeout après commit peut laisser un résultat incertain. Les contraintes UNIQUE protègent les couples même si un précontrôle a vu une absence. Les verrous dépendent du moteur : nos résultats SQLite ne prouvent pas un verrou InnoDB sur Aiven. »

## Appui sur le lot 6H.21.4

[Guide 6H.21.4 des relations et transactions](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#source-6e0c7122c419) et [Guide 6H.21.4 des migrations](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#source-088e1fc0828a) apportent les détails de chaque FK et révision. Le présent guide complète les vrais parcours, sans modifier ces sept documents ni leurs preuves historiques.
