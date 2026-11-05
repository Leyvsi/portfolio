# Lot 6G.1 — conception des likes d'histoires et de commentaires

> Archive pédagogique datée : les résultats et descriptions ci-dessous concernent le lot indiqué. Les anciens repères de ligne ne décrivent pas la version candidate. Pour préparer la soutenance actuelle, consulter les quatre fiches et le référentiel reliés au sommaire.

> Copie publique de référence : les chemins personnels et liens de travail internes sont retirés. Les preuves et commandes historiques gardent leur date et leur périmètre ; utiliser le README actuel pour le lancement.

[Sommaire](README.md) · [Bilan 6F.2](BILAN_LOT6F2.md) · [Modèles](../../backend/models.py) · [Contrat actuel](../../backend/api/v1/swagger.json)

**1er novembre 2026. Audit et conception uniquement.** Vote convient à l'ajout d'un like par compte sur une histoire ou un Cold Case ; retrait et état personnel manquent. Les likes de commentaires comptent actuellement des clics sans identifier leurs auteurs : une relation individuelle est nécessaire pour garantir unicité et retrait personnel.

**Aucun code applicatif, modèle, test, Swagger ou migration modifié. Les 723 PASS de 6F.2 restent historiques : aucune suite réexécutée.** Les contrôles réalisés ici sont statiques ; aucune base, même SQLite, n'est ouverte.

## 1. État local et sources examinées

Branche conservée `feature/frontend-api-integration`, HEAD `07a9f03ea0a3bdad4a07066fdd7bab1997cc158b`. Départ : **45 fichiers suivis modifiés, 61 non suivis, aucun indexé**. Empreintes de 120 sources/documents déjà examinés, statut et index enregistrés avant édition.

Examinés : bilan 6F.2 ; User/Story/Comment/Vote et leurs relations ; Blueprint et application chargée ; vues histoires/commentaires/théories, visibilité, permissions et CSRF ; Swagger ; service de purge et détail administratif ; dossier.html, app.js, api.js, comments.js, styles et tests associés ; tests users/votes, commentaires/théories, CSRF, archives/purge. Le contrôle AST lit décorateurs/contraintes sans importer l'application ou SQLAlchemy. Les sept exclusions antérieures, notamment **donnees.js**, ne sont ni lues, modifiées ou exécutées.

Preuves : `baseline.json`, `static-audit.json`, `final-validation.json` dans :

```text
[chemin local privé retiré]
```

## 2. Routes réellement disponibles

Le [Blueprint](../../backend/api/v1/views/__init__.py) porte le préfixe **`/api/v1`**, enregistré par backend/index.py. **`/api/votes` n'est pas une route enregistrée dans cette application.** Il n'existe pas non plus de collection GET `/api/v1/votes`.

| Route active | Comportement confirmé dans les sources |
|---|---|
| `POST /api/v1/votes/{story_id}` | Compte actif/session/CSRF, parent actif ; crée Vote avec l'auteur de session. 201 `{"message":"Vote pris en compte !","votes":N}` ; doublon 409 ; corps éventuel ignoré |
| `GET /api/v1/stories` et `/stories/slug/{slug}` | Publics ; dossiers actifs ; `votes` calculé par COUNT des lignes Vote du dossier |
| `GET /api/v1/stories/{story_id}/comments` | Public pour dossier actif ; `likes` vient actuellement de Comment.likes ; pas d'état personnel |
| `POST /api/v1/comments/{comment_id}/like` | Compte actif/CSRF/commentaire et parent actif ; UPDATE `likes = likes + 1` puis commit ; 200 `{"status":"success","comment":{...}}` ; plusieurs clics du même compte augmentent plusieurs fois le compteur |
| `POST /api/v1/theories/{theory_id}/like` | Autre compteur incrémental, **hors périmètre** et à préserver |

Sources : [histoires.py](../../backend/api/v1/views/histoires.py), [comments.py](../../backend/api/v1/views/comments.py), [theories.py](../../backend/api/v1/views/theories.py). Aucun GET d'état personnel ni DELETE de like n'est déclaré pour histoires/commentaires. Aucun bouton/helper d'action correspondant dans la fiche 6F.1.

Les écritures existantes refusent visiteur/compte absent (401), banni ou CSRF invalide (403), cible absente/hors domaine/archivée (404). Le vote traite la violation unique métier comme 409, les autres erreurs SQL comme 500 avec rollback. Le comptage des votes a lieu après commit : une panne à cette étape peut produire une erreur alors que le vote est déjà enregistré.

## 3. Histoires et Cold Cases : réutiliser Vote

Vote contient **id Integer PK, story_id Integer NOT NULL FK stories.id CASCADE, user_id Integer NOT NULL FK users.id CASCADE, created_at DateTime UTC**. `unique_user_story_vote(user_id, story_id)` impose un seul couple dans le schéma déclaré. User.votes et Story.votes relient les objets ; la collection Story.votes conserve sa cascade ORM.

Pas de note, polarité ou type de cible : présence d'une ligne = vote binaire, adapté à un like. **Un Cold Case est une Story**, sans restriction de catégorie sur la route de vote. Vote ne possède aucun comment_id : un id de commentaire ne doit jamais être envoyé au endpoint d'histoire.

**Proposition : conserver intégralement les anciens Vote, ids, auteurs et dates, et les présenter comme les likes d'histoires.** Aucune nouvelle table ni migration nécessaire pour cette réutilisation. Ajouter seulement lecture de « mon like » et retrait du couple courant. L'état des FK/contraintes d'une base réellement déployée n'est pas attesté ici.

## 4. Commentaires : relation et reprise historique

Comment.likes est un Integer NOT NULL, défaut 0. L'UPDATE actuel évite de perdre un incrément concurrent ; il ne mémorise aucun auteur et n'empêche pas les répétitions. **On ne peut pas reconstruire qui a liké à partir de ce seul nombre**, ni retirer fiablement le like d'un compte.

Table minimale proposée, sur le modèle de Vote :

| Élément | Structure proposée |
|---|---|
| `comment_likes.id` | Integer PK |
| `comment_id` | Type SQL exact de Comment.id, NOT NULL, FK comments.id ON DELETE CASCADE ; index `ix_comment_likes_comment_id` pour comptage/purge |
| `user_id` | Type SQL exact de User.id, NOT NULL, FK users.id ON DELETE CASCADE |
| `created_at` | DateTime UTC NOT NULL, date réelle du nouveau like |
| Unicité | `unique_user_comment_like(user_id, comment_id)` ; aucune unicité sur chaque colonne isolée |
| Relations ORM | Comment.comment_likes ↔ CommentLike.comment ; User.comment_likes ↔ CommentLike.user ; cascade des enfants et passive_deletes adaptées/testées pour ne pas mettre une FK obligatoire à NULL |

Les modèles actuels utilisent Integer. Une future migration doit toutefois vérifier/reprendre les types physiques des deux parents, notamment les attributs MySQL éventuels. Ni cible polymorphe textuelle, ni story_id redondant, ni pseudo/email copié. Le compteur actif sera **COUNT des lignes CommentLike**, l'état personnel l'existence du couple courant. Le champ JSON `likes` garde son nom ; `comment_to_dict`, déjà utilisé par le détail administratif, devra fournir ce compte réel.

Généraliser Vote aux commentaires demanderait de modifier sa FK d'histoire obligatoire, d'imposer une seule cible parmi deux et de revoir les unicités. Une petite table dédiée réutilise son principe sans fragiliser les votes historiques ni introduire ce schéma polymorphe.

**Reprise à décider avant activation, valeurs réelles inconnues :**

1. Dans une intervention ultérieure autorisée, inventorier compteurs différents de zéro, valeurs SQL NULL/négatives/incompatibles et contraintes, sans contenu personnel superflu. Arrêter/drainer les anciens écrivains avant contrôle final et bascule.
2. Si tous les compteurs sont valides et nuls : table vide, aucun faux like à créer ; garder temporairement la colonne historique en lecture seule. Le sérialiseur expose le compte relationnel ; l'ancien compteur n'est plus incrémenté.
3. **Si un compteur est non nul ou incompatible : bloquer migration/bascule avant DDL.** Aucun reset, suppression, utilisateur inventé, réattribution ou conversion silencieuse de clics en comptes.
4. L'équipe devra alors choisir explicitement la conservation et la présentation de l'historique, par exemple un nombre historique distinct des nouveaux likes individuels. Ce choix n'est pas adopté ici ; remplacer discrètement un ancien total par zéro serait incorrect. Recommandation immédiate : bloquer cette reprise jusqu'à arbitrage.

Suppression de la colonne historique seulement dans une étape ultérieure autorisée. Le bannissement conserve les likes existants, comme les votes actuels, mais interdit de nouvelles actions au compte banni. Aucune route de suppression de compte/RGPD ajoutée.

## 5. Contrat minimal proposé — non implémenté

**Quatre opérations nouvelles**, deux POST réutilisés. Pas de toggle serveur ou PUT supplémentaire : ajouter et retirer sont des intentions distinctes.

| Cible | Méthode / chemin sous `/api/v1` | Réponse retenue pour la proposition |
|---|---|---|
| Histoire/Cold Case | GET `/votes/{story_id}` — nouveau | 200 état personnel et compteur |
| Histoire/Cold Case | POST `/votes/{story_id}` — existant | 201 et JSON `message/votes` conservés ; doublon 409 conservé |
| Histoire/Cold Case | DELETE `/votes/{story_id}` — nouveau | 200 état absent ; répétition 200 changed=false |
| Commentaire | GET `/comments/{comment_id}/like` — nouveau | 200 état personnel et compteur |
| Commentaire | POST `/comments/{comment_id}/like` — à adapter après autorisation | 200 et enveloppe `status/comment` conservés pour un nouvel ajout ; **doublon 409**, changement métier à documenter |
| Commentaire | DELETE `/comments/{comment_id}/like` — nouveau | 200 état absent ; répétition 200 changed=false |

Toutes ces opérations personnelles exigent un **compte actif**, sans privilège administrateur. GET sans CSRF ; POST/DELETE avec protection CSRF globale. Aucun user_id, compteur ou type fourni par le client ne détermine l'auteur. Aucun corps requis ; les POST existants continuent d'ignorer un corps éventuel. Ids bornés à **1..2147483647**, puis existence/parent actif vérifiés ; verrou parent pour les écritures. Retrait sur archive : 404 comme l'ajout ; likes conservés et retrouvés à la restauration.

Exemple illustratif du nouveau GET, **pas une donnée réelle** :

```json
{"status":"success","target_type":"story","target_id":17,"likes":3,"liked_by_me":true}
```

Pour un commentaire : target_type=comment, target_id entier du commentaire. DELETE : même structure, liked_by_me=false et changed=true/false. Le frontend vérifie cible, entier de compteur positif ou nul et booléen d'état. Réponses personnelles/écritures : `Cache-Control: private, no-store`.

Le visiteur voit déjà les nombres via les **GET publics existants** (`story.votes`, `comment.likes`) ; GET personnels/écritures donnent 401. Aucun état nominatif ajouté aux réponses publiques, aucune liste de comptes ayant liké publiée.

Codes : 200 lecture/retrait/commentaire ajouté ; 201 histoire ajoutée ; 401 session/compte absent ; 403 banni/CSRF ; 404 cible absente/hors domaine/archivée ; 409 ajout déjà présent ; 500 erreur SQL avec rollback si non validée. Ne reconnaître comme doublon que la contrainte unique métier connue ; autre IntegrityError reste une erreur. Timeout/5xx après commit : résultat incertain, aucune réussite ou absence d'écriture inventée.

## 6. Transactions, concurrence et purge 6C.2

- Ajout : compte courant, contrôle/verrou Story selon `get_active_story(..., lock=True)`, cible, insertion du couple et flush/commit unique. Le précontrôle ne remplace pas l'unicité SQL.
- Retrait : mêmes contrôles ; DELETE filtré par **user_id courant et cible** ; zéro ou une ligne. Ne supprimer ni parent, compte ou like d'un tiers. Erreur avant commit validé : rollback intégral.
- Ne pas traiter un problème de réponse/comptage après commit comme preuve de rollback. Relire l'état serveur ; aucun compteur DOM augmenté/diminué localement par supposition.
- SQLite : FK à activer ; unicité/transactions vérifiables, FOR UPDATE sans verrou de ligne MySQL. InnoDB : ordre stable des verrous, gestion des attentes/deadlocks, aucun rejeu automatique d'intention. Les compteurs décrivent l'état lu et peuvent évoluer entre requêtes ; SQLite ne prouvera pas toutes les courses MySQL.

**Purge : une FK CASCADE seule ne suffit pas.** [story_deletion_support.py](../../backend/api/v1/views/story_deletion_support.py) vérifie tables/moteurs/FK et signe un graphe de cinq familles. La nouvelle dépendance doit entrer dans ses contrôles d'intégrité, la jointure Comment, l'empreinte, le plafond, les verrous, le DELETE avant Comment et les vérifications/rollback.

Proposition compatible dashboard : suivre les lignes CommentLike **en interne**, tout en conservant les **cinq clés publiques** d'impact/résultat (`comments`, `theories`, `votes`, `updates`, `reports`). Les likes restent des sous-dépendances des commentaires ; aucune nouvelle carte ou indicateur admin. Un changement de ces enfants invalide l'empreinte. Tests requis : absence d'orphelins, plafond, rollback et autres dossiers/utilisateurs conservés. Archives/restaurations conservent les lignes ; écritures refusées sur archive.

## 7. Préparation frontend — sans code ajouté

| Fichier pressenti | Intervention future |
|---|---|
| `frontend/dossier.html`, `app.js` | Compteur et bouton sous le récit, commun Histoires/Cold Cases, vrai Story.id après résolution du slug |
| `frontend/comments.js` | Compteur et bouton propre à chaque commentaire, distinct de Signaler ; préserver motifs, cibles et brouillons |
| `frontend/api.js` | Helpers GET personnel/POST/DELETE, cookies/CSRF/délai/erreurs existants ; codes POST différents respectés |
| `frontend/likes.js` — petit contrôleur possible | Logique commune aux deux types, sans framework ou nouvelle dépendance |
| `frontend/styles.css` et tests ciblés | Styles limités aux likes, focus/contrôles natifs ; aucun changement de dashboard |

Logique proposée :

1. Compteur valide de la bonne cible, sinon « Indisponible », jamais zéro de secours. Visiteur : compte public visible, bouton désactivé/lien Connexion. État personnel inconnu jusqu'à `/me` et GET personnel réussis.
2. Après connexion/rechargement/retour : relire session puis états ; aucun état persisté dans localStorage. La lecture personnelle ne bloque pas les commentaires publics. Requêtes par commentaire dans ce contrat minimal ; mesurer avant d'ajouter une éventuelle lecture groupée sur longues listes.
3. Au clic : capturer l'intention ajouter/retirer, verrouiller dès `/me`. Si le compte a changé, relire sans écrire avec l'ancien choix. Ne pas inverser aveuglément un état périmé. Si l'intention est déjà satisfaite, afficher l'état sans écrire.
4. Un seul POST/DELETE avec CSRF ; attendre code/JSON, puis GET personnel pour compteur/aria-pressed. Un 409 d'ajout déclenche une lecture, aucun autre POST ni réussite supposée.
5. Succès confirmé puis lecture échouée : « Action enregistrée, état actuel indisponible ». Résultat incertain : pas de renvoi automatique, action bloquée jusqu'à vérification ; un GET peut précéder la fin d'un POST. Ne pas attribuer l'état observé à une demande perdue.
6. Session perdue/bannie : effacer l'état personnel/désactiver l'écriture ; garder la lecture publique. Versions/annulation écartent les réponses d'une ancienne session. Boutons type=button, aria-pressed, libellés, statut vivant et focus clavier.

`comments.js.controls` agit aujourd'hui sur **tous** les boutons de la liste : coordonner les verrous pour ne pas réactiver un like pendant un signalement. Actualiser seulement le compteur concerné, sans reconstruire la carte et perdre le formulaire de signalement. Aucun fonctionnement de donnees.js supposé ou intégré.

Les validateurs actuels `isStory`/`isStoryComment` ne contrôlent pas les compteurs de likes : ajouter une validation explicite des nombres utilisés par ces nouveaux contrôles, sans exiger inutilement un nouveau champ des lecteurs existants.

## 8. Tests nécessaires — non exécutés

| Groupe | Scénarios indispensables futurs |
|---|---|
| Identité et lecture | Visiteur/compte actif, état après reconnexion/rechargement, compte banni/absent, auteur client falsifié ignoré, compteurs publics et cache personnel |
| Unicité et retrait | Premier ajout, doublon 409/une ligne, violation SQL réelle après précontrôle, deux comptes indépendants, retrait personnel, retrait absent/répété, réajout |
| Sécurité/cibles | CSRF absent/vide/faux/non ASCII sur POST/DELETE ; ids invalides/hors domaine ; Story.id=Comment.id sans mélange ; cible disparue ; archive/restauration |
| Transaction | Vrais INSERT/DELETE puis erreur avant commit : rollback et témoins conservés ; erreurs uniques reconnues, autres contraintes/SQL non déguisées en doublons |
| UI et réseau | Double clic pendant session/action/relecture ; commit réel puis réponse perdue pour ajout/retrait ; relecture échouée après succès ; JSON/code/cible/compteur/état invalides ; réponses tardives/changement de compte/déconnexion |
| Accessibilité/6F.1 | Clavier, labels, aria-pressed, disabled et XSS ; commenter/signaler/annuler reste fonctionnel, brouillons/cibles conservés. Edge réel à autoriser séparément |
| Reprise | Migration future fictive avec compteurs à zéro ; historiques différents de zéro/SQL NULL/négatifs/incompatibles refusés avant DDL ; schéma et données comparés, anciens Vote/colonne conservés |
| Purge | Nouvelle famille interne, empreinte périmée, plafond, absence d'orphelins, rollback et contrat public cinq clés inchangé |
| Non-régression | Suites backend/frontend/lanceur, sept compteurs, signalements FK, archives/purge et Theory.likes inchangés |

Le test `test_votes_success_then_duplicate` attend déjà 201 puis 409 et une ligne. **`test_likes_allow_repeated_likes_from_same_user` attend volontairement deux succès et 1→2 pour commentaires et théories.** Après autorisation du nouveau métier, adapter seulement le commentaire vers l'unicité ; conserver la couverture des théories et de l'historique. Distinguer tests d'UPDATE/refresh existants et nouveaux INSERT/DELETE, sans supprimer des assertions pour masquer les incompatibilités.

Les futurs essais de migration exigent une autorisation SQLite fictive ; aucune migration exécutée ici. Les **sept tests de migration historiques exclus** restent non exécutés sans accord nouveau. Les 723 PASS ne valident aucune nouvelle route proposée ; compter les résultats futurs après exécution, sans annoncer un total prévu comme acquis.

## 9. Plan du lot 6G.2 à autoriser

| Ordre / responsable | Travail et condition de sortie |
|---|---|
| 1 — Tous | Valider votes existants=likes, contrats GET/DELETE, doublon commentaire 409, conservation historique et contrat de purge. Pas de bascule commentaires avec historiques non nuls non arbitrés |
| 2 — Mahamadou / Sylvie | Préparer CommentLike et migration contrôlée, types/FK/unicité/index/blocage avant DDL ; aucune application réelle. Préparer la bascule avec anciens écrivains arrêtés |
| 3 — Sylvie | Quatre opérations nouvelles, POST commentaire/sérialiseur adaptés ; POST vote/Theory.likes préservés ; auth/CSRF/erreurs/rollback ; Swagger actualisé après contrat autorisé |
| 4 — Sylvie / Mahamadou | Étendre graphe/intégrité/transaction de purge en interne, conserver contrat public et dashboard ; valider cette non-régression avant activation |
| 5 — Mélissa | Boutons/compteurs de fiche et commentaires, contrôleur léger, session/relecture/erreurs, sans perte des formulaires 6F.1 |
| 6 — Tous | Harnais réinspecté, SQLite isolée FK actives, tests ciblés puis non-régression ; manifestes renouvelés après revue des sources, pas automatiquement |
| 7 — Tous | Résultats exacts, limites et recette manuelle intégrée ; serveur/Edge, vérification MySQL/Aiven et migration réelle restent des autorisations séparées |

Backend pressenti : `models.py`, vues histoires/commentaires, `story_deletion_support.py`, Swagger, tests ciblés et future révision Alembic. Réutiliser permissions/CSRF existants ; aucun nouveau principe de session nécessaire. Ne pas lancer l'ancien incrément de Comment.likes après activation de la nouvelle relation.

Préparer une migration et l'exécuter sont deux opérations distinctes. `create_all` ne transforme pas une base existante. Les DDL MySQL ne sont pas promis entièrement annulables après incident : inventaire, sauvegarde de données, maintenance et contrôle de reprise seront requis avant une opération réelle autorisée. Aucun lot RGPD, journal de reçus, service ou refonte supplémentaire justifié.

## 10. Décisions et verdict

**GO pour soumettre la conception. Implémentation 6G.2 en attente d'autorisation. Migration/bascule commentaires NO-GO si les historiques ne sont pas arbitrés.**

- Histoires/Cold Cases : Vote réutilisable, anciens enregistrements conservés ; pas de nouveau schéma nécessaire.
- Commentaires : table individuelle justifiée ; ancien compteur non attribuable, aucune reprise silencieuse.
- Purge : nouvelle dépendance à protéger en interne, cinq clés publiques et sept compteurs admin conservés.
- Sécurité : unicité par compte, pas garantie « une personne physique/un seul compte » ; aucune promesse anti-spam globale ou compatibilité MySQL attestée.
- Preuve actuelle : contrôles statiques ; aucun test applicatif, navigateur ou base exécuté pendant 6G.1.

Livraison documentaire uniquement : présent rapport créé et sommaire complété. Aucun secret/.env, accès MySQL/Aiven, migration, modification Windows/dashboard, serveur/navigateur, changement de branche, commit, push ou suppression. Arrêt après 6G.1, en attente de validation.

**Préservation statique finale :** 119 des 120 fichiers examinés préexistants identiques par SHA-256 ; seul le sommaire est complété, un rapport créé. 54 références documentaires locales contrôlées. État final : 45 fichiers suivis modifiés, 62 non suivis, aucun indexé ; branche, HEAD et empreinte de l'index conservés. Reçu `final-validation.json` dans le dossier de preuves.
