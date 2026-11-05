# Lot 6C.2 — conception finale de la suppression définitive

[Sommaire](README.md) · [Audit 6C](BILAN_LOT6C_AUDIT.md) · [Phase 6C.1 validée](BILAN_LOT6C_PHASE1.md) · [Matrice des 22 remarques](SUIVI_REMARQUES_JURY.md)

**31 octobre 2026 — conception documentaire uniquement.** Aucun développement applicatif, bouton, route, modèle, migration ou test de suppression créé ou exécuté. Toutes les structures, opérations et signatures proposées ci-dessous sont **inexistantes et à autoriser**. Les 604 PASS de 6C.1 sont historiques, acceptés par l’utilisateur ; ils ne sont ni relancés ni présentés comme une validation de la purge. Le lot 6E n’est pas commencé.

**Verdict : NO-GO en l’état pour commencer le développement 6C.2.** La solution technique est définie, mais la destruction des motifs de signalement, le changement de schéma des cibles, le traitement des anciennes références et le reçu transactionnel doivent être validés explicitement (§ 12). Cette conclusion ne demande aucune nouvelle permission pour l’audit : l’intervention documentaire autorisée est achevée. Une autorisation ultérieure de développement reste nécessaire, indépendamment de tout avis technique.

## 1. État du dépôt et méthode

| Contrôle avant édition | Résultat |
|---|---|
| Branche | `feature/frontend-api-integration` |
| HEAD | `07a9f03ea0a3bdad4a07066fdd7bab1997cc158b` |
| État détaillé | 37 fichiers suivis modifiés, 31 fichiers non suivis ; aucun changement indexé |
| Évolution depuis la clôture 6C.1 | **88 fichiers comparés aux empreintes de fin de phase : aucun changement détecté** dans ce périmètre, sans attribution supposée à un membre |
| Conservation de cet audit | 93 ressources publiques inventoriées et leurs SHA-256 ; copies préalables des deux documents de navigation/suivi concernés |
| Référence fonctionnelle | 254 backend + 342 frontend + 8 lanceur = **604 PASS historiques** |

Les rapports 6C/6C.1, les neuf modèles et dix FK, les cinq migrations déclarées, les routes, Swagger et les interfaces concernées sont examinés par lecture et AST uniquement. Aucune importation applicative, SQLAlchemy ou Alembic ; aucune ouverture de base. La version SQLAlchemy fixée dans les sources est 2.0.53 ; les documents officiels consultés concernent la branche 2.0. Les manuels MySQL 8.4 servent de référence technique, **pas d’attestation de la version déployée**.

Preuves hors dépôt : `$env:TEMP/portfolio-lot6c2-conception-20261031-kfdioh4w`, avec `baseline.json`, sauvegardes documentaires et `source-inventory.json`. Aucun `.env`, cookie, certificat, fichier privé ou fichier de base inclus. La comparaison à 6C.1 couvre 88 fichiers attestés, pas un historique individuel exhaustif de toutes les ressources possibles.

## 2. Périmètre recommandé et état réellement existant

**Recommandation à valider :** supprimer uniquement un dossier **déjà archivé**, histoire ou Cold Case sans différence de règles, par un administrateur existant, `is_admin=True` et `is_banned=False`, après aperçu d’impact et confirmation renforcée. Supprimer son graphe dans une seule transaction ; conserver intégralement les autres dossiers, comptes, catégories et propositions. La suppression ne pourra pas être restaurée par le bouton Restaurer de 6C.1.

Actuellement, [Story](../../backend/models.py) possède `archived_at`, mais ni identité immuable de dossier, ni compteur de version de gestion, ni reçu de suppression. [Report](../../backend/models.py) possède une cible textuelle et aucune FK. Les quatre routes de [admin_stories.py](../../backend/api/v1/views/admin_stories.py) servent uniquement liste/détail et archive/restauration. Swagger décrit **29 opérations** ; aucune route de purge ou de confirmation de purge n’existe.

La migration [c6c100000001](../../migrations/versions/c6c100000001_add_story_archive_date.py) ajoute seulement `archived_at`, après `82deda84bc35`. Elle est préparée et n’a pas été appliquée à une base réelle dans nos interventions. Sa présence ne prouve ni son déploiement ni l’intégrité des contraintes du moteur cible. Aucun ordre Alembic n’est lancé ici, même `current` ou en mode offline.

### 2.1. Conséquence sur chacun des neuf modèles

| Modèle / table actuelle | Effet recommandé de la purge du dossier archivé | Garantie et exclusion |
|---|---|---|
| Story / `stories` | Une ligne supprimée, identifiée par id **et identité immuable attendue** | Ni titre, ni catégorie, ni position dans la liste ne servent de clé de suppression |
| Theory / `theories` | Toutes les lignes de ce `story_id`, leurs textes et likes supprimés | Auteurs NULL admis ; aucune suppression de compte |
| Comment / `comments` | Toutes les lignes de ce `story_id`, textes, likes et pseudos copiés supprimés | Les reports associés sont traités avant disparition des commentaires |
| Vote / `votes` | Toutes les lignes de ce `story_id` supprimées | Autres votes et contrainte d’unicité utilisateur/dossier conservés |
| ColdCaseUpdate / `cold_case_updates` | Toutes les lignes de ce `story_id` supprimées | Même règle quelle que soit la catégorie réelle du dossier |
| Report / `reports` | **Recommandation : supprimer uniquement les reports des commentaires de ce dossier**, tous statuts et doublons compris | Nécessite la cible relationnelle proposée au § 3 ; les reports des autres commentaires restent identiques |
| User / `users` | Aucune ligne ni colonne modifiée par la purge | Auteurs, administrateurs et comptes bannis conservés ; les FK auteur ne remontent pas les suppressions |
| Category / `categories` | Aucune ligne ni colonne modifiée | Aucune suppression par catégorie, aucun changement des conventions 1/2 |
| Proposal / `proposals` | Aucune ligne ni colonne modifiée | Aucun lien SQL à Story ; ne jamais supprimer par ressemblance de titre ; pending inchangé |

Une éventuelle table de reçus serait un **dixième modèle à créer après validation**, et non un journal existant. Aucune des dix FK actuelles n’a besoin d’être retirée ou modifiée pour cette recommandation.

### 2.2. Cascades et opération SQLAlchemy retenue

Les quatre collections de Story déclarent `all, delete-orphan` et leurs FK vers Story déclarent `ON DELETE CASCADE`. `Session.delete(story)` déclencherait les mécanismes ORM ; les suppressions en masse n’utilisent pas les mêmes cascades. Ces garanties sont distinctes. [SQLAlchemy — cascades](https://docs.sqlalchemy.org/en/20/orm/cascades.html).

**Choix proposé : service de purge explicite, opérations SQLAlchemy Core ciblées par table**, sur la même session/connexion et dans une seule transaction : reports, théories, votes, mises à jour, commentaires, puis Story. Aucun retrait d’enfant d’une collection, aucune modification de cascade ORM, aucun mélange avec `Session.delete(story)`. Les cascades SQL restent une défense relationnelle supplémentaire, pas le seul mécanisme supposé du service. Le reçu et les contrôles comparent les nombres réellement affectés aux ensembles verrouillés. Les tests futurs devront couvrir séparément suppression ORM et SQL directe pour vérifier les FK, sans les confondre avec le chemin produit.

## 3. Signalements : décision centrale

### 3.1. Pourquoi la chaîne actuelle est insuffisante

[comment_to_dict](../../backend/api/v1/views/comments.py) compte `type='comment' AND target_id=str(comment.id)`. [report_comment](../../backend/api/v1/views/comments.py) et [post_report](../../backend/api/v1/views/index.py) créent cette référence depuis un commentaire existant. En 6C.1, les deux vérifient aussi le dossier actif via [get_active_story](../../backend/api/v1/views/story_visibility.py) et demandent son verrou. Cela protège les écrivains API coopérants, sans créer de contrainte entre reports et comments.

Exemple fictif : dossier 10 → commentaire 42 → report `type=comment,target_id='42'`. Il faut joindre **Report à Comment, puis Comment au dossier**. Effacer les reports de cible `'10'` confondrait l’id du dossier avec l’id de commentaire. Un simple nettoyage textuel, même dans une transaction, laisse aussi un intervalle exploitable par un écrivain ne respectant pas le verrou applicatif.

### 3.2. Comparaison des politiques

| Politique | Bénéfice | Coût / condition | Avis |
|---|---|---|---|
| Supprimer les reports concernés, FK `Report.comment_id → Comment.id ON DELETE CASCADE` | Aucune cible vivante sans commentaire ; aucune ancienne accusation conservée à réattribuer ; portée bornée au dossier | Perte définitive des motifs et statuts de modération ; décision métier explicite | **Recommandée** pour cette purge éditoriale |
| Conserver une trace détachée, FK nullable `ON DELETE SET NULL` | Préserve un historique de modération si une finalité le justifie | Retirer la cible actionnable, ajouter état explicite « cible supprimée » et identité historique non réutilisable ; définir contenu, accès et durée ; modifier contrats/UI | Alternative cohérente, plus coûteuse, **non retenue par défaut** |
| Supprimer seulement par `type/target_id` sans FK | Peu de changements de schéma | Tous les écrivains devraient coopérer ; pas de garantie relationnelle contre création tardive ou réutilisation d’id | Insuffisante pour la garantie demandée |
| Conserver les lignes actuelles après suppression de la cible | Aucun changement de modèle | Reports orphelins et réattribution possible | **Rejetée** |

Dans l’alternative de conservation, `comment_id=NULL` est un état métier explicite, pas une fausse cible encore navigable. L’ancien numéro ne pourrait pas reconstruire un lien. Conserver seulement `target_id='42'` ou des motifs dans le reçu n’est pas une solution. Le choix purge/conservation est à valider avant code ; aucune rétention implicite des accusations n’est recommandée.

### 3.3. Schéma cible recommandé pour Report — non écrit

Remplacer les colonnes physiques `type` et `target_id` par **`comment_id` entier NOT NULL, indexé, FK nommée `fk_reports_comment`, ON DELETE CASCADE**. Plusieurs reports du même commentaire restent admis : **pas d’UNIQUE sur comment_id**. Les autres champs, identifiants de report, motifs, dates et statuts restent inchangés jusqu’à une purge autorisée.

Ne garder aucune seconde référence indépendante : le JSON compatible serait calculé en lecture, `type="comment"`, `target_id=str(comment_id)`. Les deux créations continueraient d’accepter le même contrat public, mais affecteraient seulement `comment_id`. Le compteur du commentaire utiliserait cet entier ; `/admin/reports` garderait ses champs JSON et ne publierait aucune donnée supplémentaire. Les objets/tests utilisant directement `Report(type=..., target_id=...)` devront être adaptés explicitement : cette compatibilité concerne l’API HTTP, **pas les anciens appels Python**.

La nouvelle FK exige le même type/format compatible que `comments.id`, ainsi qu’un moteur et des contrôles FK effectifs. Une insertion tardive vers un commentaire disparu est alors refusée ; si elle précède la suppression, elle est prise en charge dans la transaction ou sa cascade. Une cascade MySQL n’active pas un trigger de journal : le reçu proposé ne repose donc sur aucun trigger. [MySQL — contraintes FK](https://dev.mysql.com/doc/refman/8.4/en/create-table-foreign-keys.html).

### 3.4. Reprise des anciennes cibles et limites de détection

**Aucune donnée réelle examinée ici.** Prévoir une étape ultérieure autorisée d’inventaire, puis une migration à arrêt explicite :

1. Accepter automatiquement seulement `type` exactement `comment`, cible ASCII décimale **canonique** de 1 à 2147483647, et un commentaire existant. Ne pas compter sur la collation du moteur pour décider si le type est identique.
2. Refuser le passage final si une ligne comporte un type inconnu, zéro, signe, espace, Unicode numérique, dépassement, forme non canonique telle que `00042`, cible absente ou incohérence. Aucun cast SQL permissif, suppression automatique, exclusion d’une ligne, ni report arbitrairement affecté à un autre commentaire.
3. Soumettre ces cas à une décision séparée : réparation prouvée et validée, ou autre politique explicite. Une correspondance numérique possible ne suffit pas à autoriser la correction. Tant qu’un cas reste non résolu, **pas de bascule et purge désactivée** ; ne pas laisser `comment_id` nullable comme état final de compromis.
4. Conserver tous les reports valides lors de la migration, y compris leurs doublons ; vérifier égalité des nombres et valeurs, absence d’orphelins, puis retirer les anciennes colonnes seulement après validation de la reprise.

Un id ayant **déjà** été réutilisé peut rendre une ancienne cible numériquement valide mais historiquement fausse. La seule existence du commentaire ne prouve pas la provenance ; ni cet audit ni une nouvelle FK ne réparent rétrospectivement ce cas. Toute suspicion devra être résolue à partir de preuves autorisées, sans inventer d’association. La conversion n’est pas un contrôle historique universel.

### 3.5. Réutilisation d’identifiants après bascule

SQLite peut réutiliser des ROWID supprimés ; `AUTOINCREMENT` change l’attribution automatique avec un coût, et n’interdit pas toute insertion explicite d’un ancien nombre. [SQLite — autoincrement](https://www.sqlite.org/autoinc.html). Ne pas fonder la sécurité uniquement sur le compteur MySQL ou SQLite.

La purge relationnelle élimine les anciens reports **avant** qu’un id de commentaire puisse être réutilisé après commit : aucun report de l’ancienne cible ne survit pour être réattaché. Les identifiants ne doivent pas être modifiés/réattribués par les parcours produit. Un client qui créerait délibérément un **nouveau** report sur un numéro désormais attribué à une nouvelle ressource pose un autre problème d’identité d’API ; les archives retirent les anciens boutons et les écritures prévues vérifient la cible actuelle. Si l’exigence inclut des liens publics éternellement non réutilisables, ajouter ultérieurement une identité immuable aux commentaires et une précondition à leurs écritures, avec changement de contrat à faire valider. Ne pas prétendre que la FK distingue deux incarnations successives d’un nombre dans une requête arbitraire.

## 4. Préconditions, identité du dossier et reçu proposé

### 4.1. Deux colonnes Story justifiées — à valider

| Ajout envisagé | Raison précise |
|---|---|
| `identity` UUID canonique, NOT NULL, UNIQUE, immuable | Un ancien écran/token ne doit jamais supprimer un autre dossier ayant repris le même id numérique. Backfill différent par ligne, jamais une même valeur par défaut pour toutes les lignes |
| `management_version` entier large positif, NOT NULL, départ 1 | Invalider un ancien aperçu après restauration puis réarchivage, même si une date est répétée ou a une précision insuffisante |

L’id numérique reste le paramètre de chemin, mais le token est lié à cette identité et à la version. Incrémenter la version sous verrou lors de chaque transition effective archive/restauration et de chaque écriture réussie ayant un effet sur le dossier ou ses dépendances ; aucun incrément après rollback, no-op d’archivage ou vote refusé. Les sept écrivains actuels devront participer à cette règle. Une évolution éditoriale future devra aussi le faire.

Ne pas utiliser seulement `updated_at`, un hash de titre, le cache ORM ou une date envoyée par le navigateur. Ne pas croire qu’ajouter `version_id_col` contrôlerait les opérations Core/en masse : ce mécanisme ORM est limité au flush d’objets. Le service proposé compare lui-même identité, version, validateur et graphe. [SQLAlchemy — version counters](https://docs.sqlalchemy.org/en/20/orm/versioning.html).

### 4.2. Aperçu et confirmation renforcée

Trois étapes côté serveur, sans verrou maintenu pendant la lecture humaine :

1. GET privé d’aperçu : lire et verrouiller brièvement le graphe de la même manière que la purge, vérifier qu’il est archivé, produire titre, état, identité, version et nombres exacts : 1 dossier, théories, commentaires, votes, mises à jour, reports associés. Relâcher la transaction avant réponse. Générer un `operation_id` UUID aléatoire et un jeton d’aperçu signé, **sans création de reçu ni autre écriture SQL**.
2. L’interface demande de saisir le **titre complet** affiché et d’acquitter explicitement la perte des contributions/signalements. POST privé de confirmation : vérifier le titre exact, son type/longueur, `confirm_contributions === true`, le jeton, la cible et les préconditions relues ; renvoyer un jeton final signé. Ni trim ni normalisation Unicode silencieuse ; le titre n’est jamais la clé de la suppression.
3. DELETE conditionnel : envoyer le jeton final, le validateur et la même clé d’opération ; tout revérifier sous verrou. **Pas de suppression par GET ou par le POST de confirmation.**

Validité proposée des deux jetons : **cinq minutes au total depuis l’aperçu**, durée technique à valider, jamais prolongée par la confirmation. Signature HMAC avec séparation de contexte à partir du secret configuré du serveur, sans lire ce secret pendant l’audit ; jetons liés à l’administrateur, à la session courante, à l’action, à la cible/identité/version, au validateur, à l’empreinte des dépendances et à `operation_id`. Ne stocker ni transmettre de secret brut ; ne pas journaliser jeton, CSRF ou saisie. Signature ≠ chiffrement : éviter les titres/textes dans les claims, utiliser une empreinte pour la comparaison. CSRF et confirmation restent deux protections distinctes.

Le serveur peut imposer l’envoi d’un titre exact et d’un acquittement, pas prouver qu’un humain a réellement lu un dialogue. Aucune nouvelle prétention de réauthentification, MFA ou journal déjà existant. Ces choix seraient une extension à autoriser si nécessaire.

### 4.3. Validateur fort et empreinte d’impact

Prévoir un validateur fort de la représentation administrative **de Story**, déterministe, incluant identité/version et toutes ses données sérialisées, avec enfants triés. Le GET de détail existant pourrait fournir ce `ETag`. L’aperçu transmettrait ce **validateur de la ressource cible** dans le champ `resource_etag` ; ne pas étiqueter son propre JSON variable (avec jeton aléatoire) par un ETag qui ignorerait une partie de sa représentation.

Dans DELETE, `If-Match` exige un unique validateur fort entre guillemets ; rejeter `*`, les tags faibles et les listes dans ce contrat restreint. Relire/recalculer sous verrou, sans utiliser une représentation ORM périmée. Le service vérifierait aussi une empreinte déterministe des ensembles `(table, id)` et associations `(report.id, comment_id)` verrouillés, pour détecter une substitution de dépendance même à nombre égal. Les sérialiseurs/versions de représentation devront être partagés et testés, pas dupliqués en frontend. Ces mécanismes couvrent les écritures autorisées ; aucun protocole applicatif ne résiste à un opérateur privilégié qui désactive ses contraintes et falsifie ses identités.

DELETE sans corps est retenu pour éviter de dépendre de la prise en charge d’un corps par les intermédiaires ; 200 décrit le reçu. La comparaison If-Match est forte, un changement rend la confirmation périmée. [RFC 9110 — DELETE et requêtes conditionnelles](https://www.rfc-editor.org/rfc/rfc9110.html). Le statut 428 peut exiger la précondition plutôt que traiter la suppression sans elle. [RFC 6585 — 428](https://www.rfc-editor.org/rfc/rfc6585.html#section-3).

### 4.4. Reçu transactionnel minimal — nouvelle table envisagée

Proposition `StoryDeletionReceipt` / `story_deletion_receipts`, **inexistante aujourd’hui** :

| Champ envisagé | Usage / minimisation |
|---|---|
| `operation_id` UUID, PK/unique | Rechercher l’issue exacte après réponse perdue |
| `deleted_story_identity` UUID, unique | Identifier l’incarnation supprimée sans dépendre d’un numéro réutilisé |
| `deleted_story_number` entier historique | Information de reçu ; **pas une FK vivante, pas un lien navigable**, jamais utilisé seul pour supprimer |
| `actor_id` nullable, FK User `ON DELETE SET NULL` | Attribuer l’acte sans recopier pseudo/email ; si un futur effacement de compte est autorisé, ne pas attribuer la trace à un numéro réutilisé |
| `deleted_at` UTC | Horodater la validation |
| Nombres par famille supprimée | Rendre les conséquences contrôlables, sans contenus |
| Empreinte de la demande | Détecter une réutilisation incompatible de clé, sans conserver le jeton ni le titre saisi |

Une ligne signifie **purge validée**, sans statut « succès » écrit avant commit, sans ligne de tentative persistée en dehors de la transaction. Le reçu est inséré dans la même transaction que la suppression ; si son insertion échoue, toute la suppression est annulée. Pas de titre, slug, URL, texte, motif, pseudo, email, IP, user-agent, cookie ou CSRF. Les identifiants et empreintes ne sont pas déclarés anonymes : accès admin et durée bornée à décider.

La durée précise, la finalité de l’acteur et la procédure d’expiration sont **des décisions ouvertes**, pas une conservation illimitée par défaut. La fenêtre de recherche du reçu doit couvrir le délai d’incertitude/reprise retenu ; après expiration du reçu, ne jamais inventer une preuve de succès. Pour les sauvegardes, une procédure doit empêcher de republier une incarnation purgée après restauration ; la durée du reçu seul n’en donne pas automatiquement la garantie.

Cela porterait le schéma de 9 à **10 tables**, de 10 à **12 FK** avec la FK Report et la nouvelle FK de reçu vers User, sans changer les dix existantes. Une simple ligne de log hors transaction ne fournirait ni l’atomicité ni une preuve fiable de réponse perdue ; l’alternative sans reçu est rejetée pour la garantie d’issue vérifiable demandée ici.

## 5. Algorithme transactionnel exact recommandé

**Préconditions de mise en service, non réalisées :** migration d’archivage et futur schéma appliqués sur une cible autorisée, reprise validée, contrôles FK effectifs et moteur transactionnel, reçu et durée approuvés, toutes les routes d’écriture adaptées. Si la révision/capacité requise n’est pas attestée, désactiver la purge et répondre indisponible ; aucun repli vers la seule chaîne `target_id`.

### 5.1. Périmètre de transaction et ordre des verrous

Une seule unité de travail sur la session SQLAlchemy de la requête. Les permissions actuelles lisent déjà en base et peuvent avoir commencé une transaction implicitement : ne pas ajouter aveuglément un second `session.begin()` autour d’une transaction existante, ni faire un commit intermédiaire « pour repartir ». Le service devient propriétaire du commit/rollback, sans travail métier étranger en attente. Le contexte exact devra être testé. [SQLAlchemy — Session Basics](https://docs.sqlalchemy.org/en/20/orm/session_basics.html).

Les lectures de décision, du reçu et de réconciliation post-commit devront utiliser le **primaire d’écriture**, sans cache ni réplique éventuellement retardée. Aucun routage de réplique n’est constaté ou configuré ici ; c’est une exigence du futur chemin de purge.

Ordre proposé, commun à aperçu, confirmation et purge : **User de l’acteur en verrou partagé → Story en exclusif → Comment par id croissant → Theory → Vote → ColdCaseUpdate → Report par id croissant → reçu d’opération**. Le verrou partagé User empêche une suspension/démotion pendant la validation finale sans sérialiser toutes les actions d’un même administrateur ; vérifier le support du dialecte, ou retenir un verrou exclusif plus conservateur si nécessaire. Ne pas ajouter ce verrou User après celui de Story dans un autre chemin de purge. Les écrivains enfants doivent verrouiller Story **avant toute mutation** ; une lecture initiale d’id d’enfant doit rester non verrouillante avant ce parent.

Sur InnoDB, utiliser des **lectures courantes verrouillantes**, pas des COUNT ordinaires possiblement issus d’un ancien snapshot REPEATABLE READ, pour établir les ensembles de décision. Un verrou de parent n’est pas un verrou implicite sur toutes les lignes Report ; verrouiller aussi les commentaires puis les reports concernés. Les verrous sont transactionnels et libérés au commit/rollback. [MySQL — locking reads](https://dev.mysql.com/doc/refman/8.4/en/innodb-locking-reads.html).

### 5.2. Les dix étapes de la purge

| Étape | Opération exacte prévue et arrêt sûr |
|---|---|
| 1. Authentification / autorisation | Exiger la session ; verrouiller et relire User avec rafraîchissement de l’état, vérifier compte existant, non banni et rôle admin actuel. 401/403 avant divulgation du dossier. Le rôle en session et le bouton ne sont jamais des autorisations. |
| 2. CSRF et validation | Le filtre global exige déjà CSRF pour DELETE authentifié ; conserver ce contrôle avant la vue. Valider id, tailles/formats des en-têtes, précondition présente, signature/contexte/expiration du jeton final, accord exact id/operation/session/validateur. Aucune écriture à ce stade. |
| 3. Existence et éventuel reçu | Verrouiller la Story **par id seul**, pas avec un filtre qui cacherait son état actif. Après ce verrou/recherche, chercher le reçu par `operation_id` en lecture courante. S’il prouve déjà **la même demande**, rendre son résultat existant sans suppression ; clé réutilisée pour une autre demande : 409. Sans reçu et sans Story : 404, jamais un faux succès. |
| 4. État archivé et identité | Exiger `archived_at IS NOT NULL` : sinon 409. Vérifier UUID immuable, version et cible du jeton ; une autre incarnation du même numéro donne 412, aucune action sur elle. |
| 5. Conditions et fraîcheur | Revalider l’expiration, le titre confirmé par le jeton et le validateur cible ; acquérir tous les verrous du graphe et recalculer l’impact/son empreinte. Si impact ou représentation a changé : 412, rollback, nouvel aperçu et nouvelle confirmation. Dépendance non supportée ou limite de volume dépassée : 409/503 selon cause, sans suppression partielle. |
| 6. Identification des dépendances | Définir C=comments de Story ; T, V, U=théories, votes, updates du même `story_id` ; R=reports joints à C par `comment_id`. Retenir les ids et nombres pour contrôle, sans publier de contenus dans le reçu. Ne jamais tronquer les listes ou un IN aux premières lignes. |
| 7. Signalements | Supprimer explicitement **R uniquement** par la jointure/sous-requête vers les commentaires du dossier encore présents. Comparer le nombre réellement affecté à R. Autres reports inchangés. La FK nouvelle complète la protection ; ne pas désactiver ses contrôles. |
| 8. Suppression transactionnelle | Supprimer T, V, U, C, puis une Story avec prédicat id + identité + version + état archivé. Exiger les nombres prévus et exactement une Story. Utiliser des opérations Core ciblées sur tables, dans la même session ; pas de commit par famille ou par lot. Contrôler la disparition des ensembles capturés **avant** commit, puis insérer le reçu. |
| 9. Commit / rollback | Un seul commit de l’ensemble. Toute erreur avant validation entraîne rollback complet, y compris reports et reçu. Conflit unique sur reçu : rollback d’abord, puis relire dans une nouvelle transaction ; ne rendre un replay 200 que si la même demande est prouvée. Deadlock/attente : rollback, réponse explicite ; aucune répétition destructive automatique. |
| 10. Vérification finale | Les invariants sont contrôlés dans la transaction, puis après commit accusé par une nouvelle lecture du reçu et de l’absence de l’ancienne **identité**. Expirer le cache ORM si des objets ont été chargés ; ne pas prendre ce cache pour une preuve SQL. Réponse 200 contenant le reçu seulement après validation. Si la relecture post-commit échoue, afficher une issue à vérifier, sans prétendre annuler un commit déjà validé. |

La session doit être nettoyée/expirée après les opérations Core : les collections ORM éventuellement chargées ne doivent pas être réutilisées pour afficher des enfants supprimés. Pour vérifier les reports après disparition des commentaires, utiliser les **ids de commentaires capturés** et la FK ; une jointure sur des commentaires désormais absents donnerait un faux contrôle à zéro. Les postconditions doivent rechercher les anciennes dépendances, pas seulement compter ce qui reste joignable.

Les suppressions peuvent être découpées en requêtes bornées pour respecter les limites de paramètres, mais **tous les lots restent dans la même transaction**, sans omission. Définir une limite opérationnelle configurable, refus explicite avant mutation pour un dossier trop volumineux et une procédure séparée ; pas de purge partielle ni tâche asynchrone ajoutée implicitement.

### 5.3. COMMIT incertain

Si la liaison SQL ou HTTP se coupe pendant/après COMMIT, un appel à rollback ne prouve pas que le serveur n’a rien validé. Conserver l’identifiant d’opération côté client ; réconcilier par une **nouvelle transaction** de lecture du reçu. Reçu présent = opération validée. Reçu absent = résultat de cette lecture, pouvant précéder un commit encore en cours ; **pas une preuve de non-exécution**. Dossier 404 sans reçu = absence constatée, pas preuve que cette requête l’a supprimé. En cas de lecture indisponible ou de doute, état inconnu et aucune relance automatique du DELETE.

Une fois le commit reconnu, une erreur de statistiques ou de relecture ne doit pas être présentée comme « rollback réussi ». Le reçu permet d’annoncer séparément « suppression confirmée, actualisation des listes indisponible ». Une récupération après crash devra repartir de ce même reçu, pas d’un titre ou d’un index de carte.

## 6. Cas concurrents et limites de la garantie

| Situation | Issue prévue |
|---|---|
| Deux DELETE identiques, même opération | Le verrou Story sérialise ; après le premier commit, le second fait une lecture courante du reçu et répond 200 replay si la signature/clé/demande sont encore valides ; un seul effet et un seul reçu |
| Deux administrateurs, opérations différentes | Un seul supprime ; l’autre reçoit 404 sans reçu correspondant après attente, puis peut constater l’absence ; ne pas lui attribuer le succès du premier |
| Idempotency-Key employée sur une autre cible | Refus du lien clé/jeton, puis unicité/empreinte comme défense transactionnelle ; jamais un succès copié d’un autre dossier |
| Nouvelle contribution via les sept routes | Déjà refusée tant que le parent est archivé ; si une route a lu avant, sa lecture verrouillante du parent revalide l’état ou constate la disparition avant toute mutation |
| Nouveau commentaire SQL direct conforme FK | L’insertion référence Story : elle doit se sérialiser avec sa suppression ou échouer ; aucun enfant valide après disparition du parent, sous moteur/FK effectifs |
| Nouveau report SQL direct conforme FK | Les verrous des commentaires empêchent de traverser le nettoyage : avant verrou, il entre dans l’impact relu et invalide l’aperçu si nécessaire ; après verrou, il attend puis échoue si la cible disparaît |
| Mise à jour d’un enfant/report existant | Les lignes relues/verrouillées et le validateur/empreinte détectent les modifications pertinentes intervenues avant la décision ; l’écrivain coopérant passe d’abord par Story |
| Restauration avant acquisition du verrou | La purge constate l’état actif : 409 ; si restauration puis réarchivage, version différente : 412 |
| Purge avant restauration | Restaurer attend puis reçoit 404 ; aucun dossier recréé |
| Démotion/suspension avant verrou User | Refus ; après verrou partagé, la modification du compte attend la fin de l’acte déjà autorisé |
| Erreur SQL avant/pendant suppression ou insertion du reçu | Rollback complet ; aucun état partiel considéré comme réussi |
| Timeout après commit | Lecture du reçu ; 200 replay uniquement prouvé, jamais de nouvel effet sur un numéro réutilisé |
| Clé/jeton expiré après succès | Pas de nouveau DELETE accepté ; rechercher le reçu par son GET privé. Après expiration du reçu, ne pas promettre de replay ou de preuve persistante |

**Éviter un piège d’ordre :** ne pas verrouiller une clé de reçu **absente** avant Story ; cela introduirait des verrous de plage et des inversions inutiles. L’ordre Story puis recherche courante du reçu s’applique aussi lorsque Story est absente. Tester tout de même deadlocks et attente sur index : un ordre cohérent réduit le risque sans éliminer les deadlocks de toutes opérations SQL possibles.

Ces propriétés supposent InnoDB, transactions et FK activées, index adaptés et écrivains connus coordonnés. Les opérateurs qui désactivent `foreign_key_checks`, écrivent des identités historiques ou restaurent un ancien dump contournent le protocole. Les réinsertions après restauration de sauvegarde nécessitent une procédure dédiée. Aucun changement de droits SQL, trigger ou configuration du moteur n’est exécuté ni supposé existant ici.

## 7. Contrat API proposé — pas ajouté à Swagger

Préfixe `/api/v1`, session admin et `Cache-Control: no-store` sur toutes les réponses concernées. Les quatre opérations existantes d’archives sont conservées ; quatre ajouts seraient nécessaires (**33 opérations** si ce contrat est approuvé).

| Méthode / route proposée | Entrées | Succès |
|---|---|---|
| GET `/admin/stories/{story_id}/deletion-preview` | Id du chemin, aucun effet SQL de mutation | 200 aperçu, impact, `resource_etag`, jeton d’aperçu, `operation_id`, expiration |
| POST `/admin/stories/{story_id}/deletion-confirmations` | CSRF ; JSON `preview_token`, `typed_title`, `confirm_contributions: true` ; validateur Story lié au jeton d’aperçu et revérifié par le service | 200 jeton final signé et même opération/expiration ; aucune suppression |
| DELETE `/admin/stories/{story_id}` | CSRF, `If-Match`, `Idempotency-Key` = UUID d’opération et `X-Deletion-Confirmation` = jeton final ; **aucun corps** | 200 JSON reçu, `replayed=false` ou `true` pour une demande déjà prouvée |
| GET `/admin/story-deletions/{operation_id}` | UUID canonique, admin relu ; aucune recherche publique | 200 reçu validé ; 404 si non visible/inexistant/expiré, sans conclure qu’une opération en cours ne pourra plus se valider |

Extension prévue du GET privé de détail : fournir un ETag fort et identité/version dans le DTO privé, sans ajout dans les réponses publiques. Les nouveaux helpers client doivent pouvoir passer **seulement** les en-têtes de précondition/confirmation autorisés, sans permettre d’écraser `X-CSRF-Token`, cookies ou credentials du helper actuel. Ne pas placer de jeton dans l’URL.

`If-Match` est utilisé sur **DELETE de Story**, la ressource dont il valide la représentation. Le POST de confirmation vise une autre ressource et vérifie donc le validateur Story **à travers le jeton d’aperçu**, sans lui attribuer un If-Match de ressource différente. Le jeton final autorise une intention, jamais un changement de cible.

### 7.1. Validation et statuts

| Statut / code applicatif proposé | Sens |
|---|---|
| 200 `PURGE_COMMITTED` | Reçu transactionnel de la demande, éventuellement replay ; pas de 204 qui perdrait ce reçu |
| 400 `INVALID_REQUEST` | En-tête/UUID ou objet JSON mal formé, taille excessive, champs non reconnus, accord autre qu’un vrai booléen, titre erroné, désaccord clé/jeton ; aucune donnée sensible renvoyée |
| 401 / 403 | Session absente/invalide ; rôle absent, banni, CSRF invalide, jeton dont la signature/contexte d’accès est invalide ; ne pas révéler la cible aux non-autorisés |
| 404 `STORY_NOT_FOUND` / `RECEIPT_NOT_FOUND` | Cible ou reçu absent ; id hors domaine 1..2147483647 ou chemin d’id non reconnu : 404 comme 6C.1 |
| 409 `STORY_NOT_ARCHIVED` | Le dossier actuel est actif ; archivage et nouvelle confirmation nécessaires |
| 409 `DELETE_CONDITIONS_NOT_MET` / `IDEMPOTENCY_CONFLICT` | Dépendance non supportée, incohérence métier, clé liée à une autre demande ; aucun repli permissif |
| 412 `STALE_CONFIRMATION` | Identité/version/impact/validateur modifié ou jeton expiré ; lire le reçu si doute, sinon nouvel aperçu + nouvelle confirmation |
| 428 `PRECONDITION_REQUIRED` | If-Match ou jeton/clé exigés absents ; expliquer quoi fournir, pas de suppression sans préconditions |
| 500 `PURGE_FAILED` | Erreur interne dont la transaction a été annulée de manière confirmée ; JSON générique, aucun détail SQL |
| 503 `PURGE_UNAVAILABLE` / `DELETE_STATUS_UNKNOWN` | Schéma/capacité non attesté, délai de verrou/deadlock ou issue COMMIT indéterminée ; fournir l’opération connue et une invitation à relire, sans retry destructif automatique |

Le filtre CSRF existant peut rendre 403 avant même que la vue lise ses préconditions ; l’ordre observable des contrôles devra être documenté/testé. Pour une requête autorisée et structurellement valable, l’absence d’une cible sans reçu ou son état actif sont vérifiés avant d’évaluer un validateur devenu faux. Un reçu identique peut prouver la réussite antérieure ; ne pas transformer tout échec de précondition en succès.

Bornes proposées : UUID canonique de 36 caractères, token ASCII ≤ 4096 octets, unique ETag fort au format fixé, titre UTF-8 ≤ 200 caractères, JSON de confirmation limité avant décodage ; pas de liste arbitraire d’ids envoyée par le client. Refuser les clés et champs ambigus/dupliqués de cette nouvelle commande. Les limites exactes de requête et de volume SQL sont à documenter avant implémentation, sans changer implicitement tous les contrats existants.

### 7.2. Formes JSON indicatives

Exemple fictif d’aperçu (tokens volontairement abrégés ; non utilisables) :

```json
{
  "story": {"id": 10, "identity": "00000000-0000-4000-8000-000000000010", "title": "Dossier fictif", "is_archived": true, "management_version": 7},
  "impact": {"stories": 1, "theories": 2, "comments": 3, "votes": 4, "updates": 1, "reports": 5},
  "resource_etag": "\"opaque-strong-story-validator\"",
  "preview_token": "JETON_NON_EXECUTABLE",
  "operation_id": "00000000-0000-4000-8000-000000000099",
  "expires_at": "2026-10-31T12:05:00Z"
}
```

Réponse de purge envisagée : `status="success"`, `code="PURGE_COMMITTED"`, `replayed`, et `receipt` contenant opération, identité supprimée, numéro historique, horodatage UTC et compteurs. Aucun contenu ni identité d’auteur dans le reçu HTTP. Erreur : `status="error"`, `code`, message générique et `operation_id` seulement s’il est connu et autorisé. Le schéma OpenAPI et ses exemples ne seront modifiés qu’après autorisation de développement.

## 8. Interface proposée pour Mélissa — aucune maquette/bouton livré

1. Ajouter l’action « Supprimer définitivement » **uniquement** aux cartes archivées ; la restauration reste distincte. Pas de contrôle dangereux dans la liste active, même masqué par CSS.
2. Au clic, bloquer les actions du dossier et charger un aperçu récent. Ouvrir un dialogue modal avec titre, id, état archivé, avertissement irréversible et décompte de toutes les familles, reports inclus. Construire les éléments par `textContent`.
3. Champ étiqueté de saisie du titre complet + case explicite de prise en compte des contributions. Bouton destructif désactivé tant que les deux conditions manquent. L’annulation, Échap ou fermeture ne lancent ni POST de confirmation ni DELETE et rendent le focus au bouton initial ; le GET d’aperçu reste sans mutation.
4. À validation, activer un verrou dès avant le POST de confirmation, le garder pendant DELETE puis la réconciliation. Un double clic, y compris sur un ancien bouton détaché, ne crée pas une seconde demande. La clé d’opération reste la même pour cette intention, aucun nouvel identifiant fabriqué pour contourner une réponse incertaine.
5. Après succès, timeout, JSON illisible ou déconnexion HTTP, lire d’abord le reçu autorisé et relire l’état administratif et les listes/statistiques. Reçu validé : afficher l’issue certaine même si les statistiques sont momentanément indisponibles. Reçu absent/inaccessible : indiquer l’incertitude, masquer les anciennes actions et ne pas annoncer « supprimé par votre demande » sur un simple 404.
6. Un id réutilisé avec une nouvelle identité ne doit jamais remplacer silencieusement la cible du dialogue. Après 409/412/428, fermer/invalider l’ancienne confirmation et demander un nouvel aperçu ; pas de DELETE répété automatiquement, même après 503.
7. Versionner les requêtes, annuler les lectures périmées, écarter anciens succès/401/403 et nettoyer les jetons au départ/perte d’accès. À la perte de session, masquer les données sans présumer le résultat serveur ; après reconnexion admin, rechercher le reçu avant nouvelle intention.
8. Prévoir l’accessibilité d’un `<dialog>` natif : nom/description, focus initial sur Annuler, cycle clavier, Échap, retour du focus ; après disparition de la carte, focus sur filtre/Actualiser. Boutons tactiles, texte repliable et aucun défilement horizontal forcé ; la validation réelle clavier/mobile sera une recette séparée.

La clé d’opération seule, sans titre/token/CSRF, pourrait être conservée **temporairement en sessionStorage** pour retrouver le reçu après rechargement ; elle ne serait ni un rôle, ni un secret d’authentification. Cet usage serait nouveau et à valider ; sinon le produit doit annoncer sa limite de reprise après fermeture d’onglet. Aucun jeton de confirmation, contenu ou secret dans un stockage persistant navigateur.

Statistiques après purge d’un dossier **déjà archivé** : les trois compteurs d’actifs ne diminuent pas une deuxième fois ; Archives diminue de 1 ; commentaires et signalements globaux diminuent des nombres réellement supprimés ; users et pending restent inchangés. Ne pas soustraire localement en supposant un résultat ; relire les sources conservées de 6D. Les GET indépendants ne sont toujours pas un instantané global.

## 9. Migrations envisagées pour Mahamadou — aucun fichier créé

Après `c6c100000001`, préparer ultérieurement des étapes revues séparément :

| Étape envisagée | Contenu / garde |
|---|---|
| Inventaire de reprise autorisé | Schéma réel/version/moteur/FK/index, volumes, types et cibles de reports ; données problématiques traitées par décision explicite, jamais par effacement silencieux |
| Extension transitoire | Ajouter `Report.comment_id` nullable uniquement pendant la reprise, identité Story par ligne et version ; service de purge désactivé |
| Reprise et validation | Transformer les seules cibles validées, préserver reports/contenus, vérifier bijection de chaque report et valeurs conservées ; une erreur bloque la suite |
| Bascule cible | Rendre `comment_id` NOT NULL, créer FK et index, retirer `type/target_id` physiques ; identité Story NOT NULL/UNIQUE et version initialisée/positive |
| Reçu | Créer table, unicité d’opération/identité supprimée et FK actor nullable ; dixième modèle explicitement approuvé |
| Activation | Déployer de façon coordonnée sérialiseurs et deux écrivains de reports, puis préconditions/versionnage des écrivains et archive/restauration ; vérifier le schéma avant d’activer DELETE |

Recommandation de déploiement : **fenêtre de maintenance des écritures concernées**, tous processus anciens arrêtés/drainés avant reprise. Ne pas laisser des anciens écrivains produire des `target_id` sans nouveau `comment_id`. Un déploiement progressif demanderait un vrai protocole d’expansion/double écriture et une reprise différente, non présumé nécessaire ni conçu implicitement.

Sur MySQL, les DDL peuvent provoquer des commits implicites : ne pas promettre un rollback global de plusieurs ALTER comme celui de la purge DML. [MySQL — implicit commits](https://dev.mysql.com/doc/refman/8.4/en/implicit-commit.html). Séparer étapes, sauvegarde autorisée, contrôles de reprise et procédure d’échec ; ne pas activer le service sur un schéma partiellement préparé.

Sur SQLite, une reconstruction de table Alembic peut interagir avec les FK entrantes ; son éventuelle désactivation doit être hors transaction, limitée au test de migration autorisé, puis réactivée et contrôlée avant toute preuve de purge. **Ne pas assouplir les gardes du harnais 6C.1 ni désactiver les FK dans le service produit.** Tester une stratégie de migration adaptée aux versions autorisées, pas supposer que la chaîne MySQL historique se rejoue à l’identique. [Alembic — batch et FK](https://alembic.sqlalchemy.org/en/latest/batch.html).

Un downgrade pourra reconstruire la forme textuelle pour les reports restants, mais ne recréera aucun contenu purgé, aucun motif supprimé ni reçu expiré. La suppression d’une identité/version ou du reçu invaliderait le protocole de confirmation : retirer DELETE avant tout retour arrière. Aucune révision de migration n’est numérotée ou écrite pendant cet audit.

## 10. Répartition des fichiers envisagés

Cette liste décrit **du travail futur**, pas les fichiers modifiés ici. Les responsabilités reprennent la répartition de l’équipe, sans attribuer une modification déjà réalisée.

| Membre | Fichiers actuels à étudier / futurs fichiers proposés | Fonctions ou adaptations envisagées |
|---|---|---|
| Sylvie | `backend/api/v1/views/admin_stories.py` ; nouveau `story_deletion_support.py` proposé ; import Blueprint si module séparé | `get_story_deletion_preview`, `confirm_story_deletion`, `delete_story_permanently`, `get_story_deletion_receipt` ; unité de travail unique, erreurs et reçus |
| Sylvie | `comments.py`, `index.py` | Deux créations Report et `comment_to_dict` basculés vers comment_id ; JSON type/target_id compatible ; permissions et ordre de verrous conservés |
| Sylvie | `histoires.py`, `theories.py`, `story_visibility.py`, `admin_stories.py` ; éventuellement helper de version commun | Les sept écritures et transitions incrémentent la version seulement si leur transaction réussit ; aucun accès public aux archives réintroduit |
| Sylvie | `permissions.py`, `backend/index.py`, `swagger.json` | Réutiliser rôle/CSRF ; contrôle final sous verrou dans le service, schémas et quatre opérations nouvelles documentés ; ne pas modifier le login sans besoin |
| Mahamadou | `backend/models.py`, futures migrations après `c6c100000001` | Report relationnel, identité/version de Story, reçu proposé ; FK/index et reprise sans perte des reports valides |
| Mahamadou / Sylvie | Nouveaux `backend/tests/test_story_deletion.py` et tests de migration/concurrence proposés ; suites actuelles | Comparaisons de tables, vrai flush/rollback, erreurs de COMMIT, FK SQL/ORM, ids réutilisés et moteur cible autorisé |
| Mélissa | `frontend/admin-dashboard.html`, `admin-stories.js`, `admin-dashboard.js`, `api.js` ; `styles.css` seulement si dialogue l’exige | Dialogue renforcé, helpers d’aperçu/confirmation/DELETE/reçu, en-têtes limités, verrou et réconciliation, sept compteurs/archives |
| Mélissa | Futur `frontend/tests/admin-story-deletion.test.cjs` ; suites admin actuelles | Annulation, titre/accord, clavier simulé, doubles clics, réponses tardives/ambiguës et relecture |
| Équipe | README, documents admin/tests/matrice/index et fiches ; harnais **hors dépôt à réinspecter** | Décrire uniquement la livraison réellement autorisée ; conserver les 604 historiques et recalculer les repères après futur code |

Point de non-régression explicite : la fixture 6C.1 utilise un report de type `other` pour vérifier sa conservation pendant l’archivage. Le schéma cible limité aux commentaires ne pourrait plus le construire. Après validation du choix, déplacer ce cas dans les tests **de migration refusée** et garder un report d’un autre commentaire/dossier comme témoin de non-suppression ; ne pas supprimer discrètement l’intention de test ni considérer une fixture comme une donnée réelle à purger.

## 11. Plan de tests à implémenter — tous NON EXÉCUTÉS ici

Les futures données seront entièrement fictives. Le harnais devra être **réinspecté avant toute exécution** : neutraliser dotenv/configuration Aiven avant imports, permettre seulement la cible SQLite mémoire autorisée, bloquer réseau/bases fichier et lectures privées, activer et contrôler FK hors transaction, enregistrer les sources autorisées. Le plan ci-dessous n’autorise aucun test maintenant.

| ID | Scénario futur / résultat attendu |
|---|---|
| P-01 | Visiteur 401, compte absent 401, lecteur/banni 403 ; session is_admin falsifiée refusée sur les quatre routes proposées |
| P-02 | CSRF absent, vide, faux, non ASCII sur POST confirmation et DELETE : 403 avant mutation ; GET restent sans mutation |
| P-03 | Id 0/négatif/énorme/mal formé, UUID/en-têtes/corps invalides, doublons JSON, clés inconnues et taille excessive : erreur définie et aucune autre cible touchée |
| P-04 | Dossier actif : 409 ; dossier archivé autorisé ; inexistant : 404 sans faux succès ; mêmes règles pour histoires et Cold Cases |
| P-05 | If-Match/jeton/clé absents : 428 ; tag faible, wildcard, liste interdite et formats invalides refusés ; validateur périmé : 412 |
| P-06 | Titre complet exact + vrai booléen exigés ; espaces/Unicode non normalisés arbitrairement ; jeton signé pour autre acteur/session/cible/action refusé |
| P-07 | Expiration avant confirmation, avant DELETE ou pendant attente de verrou : refus et aucun effet ; aucun prolongement implicite de cinq minutes |
| P-08 | Aperçu et confirmation sans écriture des dix tables ; titre/impact exacts, tri et ETag déterministes, jetons non mis en cache/logs |
| P-09 | Jeu complet : Story + théories/commentaires (auteurs NULL), votes, likes, updates et plusieurs reports supprimés ; User/Category/Proposal et second dossier exactement identiques |
| P-10 | Report joint par comment_id et non id de Story : collision fictive des numéros, rapports d’autres commentaires et tous statuts correctement distingués |
| P-11 | Absence de reports/certains enfants, dossier vide : nombres zéro réels, un seul dossier supprimé, reçu exact |
| P-12 | FK Report effective : insertion sans commentaire refusée, cascade après suppression directe et après ORM avec collections chargées/non chargées ; fixture FK désactivée refusée comme prérequis |
| P-13 | Reprise de reports canoniques : toutes valeurs conservées ; types inconnus, 00042, espaces, cibles absentes ou suspectes bloquent la bascule sans nettoyage automatique |
| P-14 | Comment.id réutilisé après suppression : aucun ancien report retrouvé ; ancien jeton de Story.id réutilisé : 412 et nouveau dossier intact |
| P-15 | Erreur avant suppression, après vrai DELETE reports, après vrais flush/DELETE enfants, avant Story et à insertion du reçu : rollback intégral après relecture, y compris dixième table |
| P-16 | Échec COMMIT confirmé vs COMMIT ayant réussi mais réponse perdue : issues distinctes ; reçu atomique, aucune annonce « rollback » après succès durable |
| P-17 | Deux requêtes même opération : un seul effet/reçu ; une réponse peut être replay ; même clé/demande incompatible : conflit, rollback puis relecture saine |
| P-18 | Deux administrateurs/opérations distinctes : un succès et un refus/absence cohérent, aucun double journal ni succès attribué au mauvais acteur |
| P-19 | Report inséré avant puis après verrou commentaire et nettoyage : intégré/412 ou attente puis rejet FK ; aucun orphelin après SQL direct conforme aux contraintes |
| P-20 | Création commentaire/vote/théorie et likes/signaux pendant purge : ordre parent respecté, refus sûr, aucun enfant actif après suppression |
| P-21 | Restauration concurrente, puis restauration/réarchivage entre aperçu et DELETE : 409/412 ou restauration 404 selon ordre ; pas de confirmation ancienne acceptée |
| P-22 | Démotion/suspension avant et pendant acte : rôle actuel contrôlé sous verrou ; pas d’élévation par cookie ou reçu |
| P-23 | Attente dépassée/deadlock/erreur d’intégrité inattendue : rollback, code 503/500 explicite, aucune relance destructive automatique |
| P-24 | Volume au seuil/au-dessus, lots et limites IN : refus préalable ou traitement complet dans une transaction, jamais de troncature ou commit partiel |
| P-25 | Dialogue annulé, Échap, bouton fermeture, titre incomplet ou case absente : aucun POST de confirmation/DELETE ; focus et annonce cohérents |
| P-26 | Double clic pendant aperçu, confirmation, DELETE puis réconciliation : une intention, aucune seconde soumission tardive depuis un ancien bouton |
| P-27 | Timeout/JSON illisible/réseau perdu après commit : reçu relu avant annonce ; simple 404 ou reçu absent avant commit reste incertain ; pas de nouveau DELETE automatique |
| P-28 | Réponse ancienne succès/401/403 après départ/retour ou nouveau chargement : aucune donnée/action/confirmation ancienne restaurée |
| P-29 | Reçu trouvé mais statistiques indisponibles : suppression confirmée, listes indisponibles distinctes ; reçu/lecture inaccessible : incertitude et actions masquées |
| P-30 | Sept compteurs et archives : actifs stables, archives -1, commentaires/reports selon reçu puis relecture, users/pending inchangés ; zéro distinct de — |
| P-31 | Expiration du reçu, fermeture/rechargement, nouvelle session : limites de preuve annoncées, aucun numéro historique utilisé comme lien vers un nouveau dossier |
| P-32 | Migration de schéma fictif et échec de reprise, anciennes écritures drainées, downgrade : pas de preuve de récupération des contenus purgés ni d’activation sur schéma incomplet |
| P-33 | Non-régression 6A/6B/6C.1/6D : relecture publique, bannissement, filtres/recherche, archives/restauration et compteurs ; 604 cas historiques conservés/adaptés avec justification de tout remplacement |
| P-34 | Swagger : opérations/routes/statuts/security/CSRF/headers et DTO réels cohérents ; nouveaux noms uniquement quand implémentés |
| P-35 | Textes hostiles et titre très long : textContent, pas d’injection ; clavier/focus/modal/écran étroit simulés puis recette navigateur séparément autorisée |
| P-36 | Accès privés aux reçus, minimisation, absence de token/texte dans logs, limites de rétention et procédure de restauration de sauvegarde testées sur environnement autorisé |

### 11.1. Ce que SQLite permettra et ne permettra pas de prouver

SQLite mémoire permettra ultérieurement de tester portée des DELETE, FK/cascades, absence d’orphelins, conservation des témoins, réutilisation d’id, contraintes d’unicité, migration compatible au moteur et rollback après écritures réelles. Activer `PRAGMA foreign_keys=ON` avant transaction, vérifier sa valeur à chaque connexion et `foreign_key_check` ; la configuration n’est pas à présumer. [SQLite — foreign keys](https://www.sqlite.org/foreignkeys.html).

L’actuel harnais n’autorise que `:memory:`. Deux connexions de ce type n’ont pas automatiquement les mêmes données ; deux clients WSGI séquentiels et des mocks ne prouvent pas une course multi-connexion. **Ne pas élargir discrètement aux URI partagées ou fichiers.** Les entrelacements frontend peuvent être simulés et les barrières de service préparées, en les nommant comme simulations.

Les garanties de verrouillage, visibilité des lectures courantes, vérifications FK concurrentes, deadlocks, collations/tailles/signatures de colonnes et DDL nécessitent des tests sur un moteur MySQL/InnoDB de version connue, avec connexions indépendantes et barrières déterministes, dans une base fictive **ultérieurement autorisée**. Aucun accès MySQL/Aiven pendant cet audit. Réussir SQLite autoriserait une conclusion sur SQLite, pas une certification de concurrence de production.

## 12. Décisions, risques résiduels et verdict

| Décision à valider | Recommandation concrète | Conséquence si non validée |
|---|---|---|
| D1 — Règle métier | Archive préalable obligatoire, admin actif, confirmation du titre et des contributions | Pas de purge sur dossier actif, pas d’exception implicite |
| D2 — Sort des signalements | Détruire ceux des commentaires supprimés, avec nouvelle FK CASCADE et fin de la référence textuelle physique | Sans choix explicite, **pas de code destructif** ; l’alternative de trace exige une autre conception de schéma/retention |
| D3 — Reprise des anciennes références | Migration refusée sur toute cible non canonique/inconnue/suspecte, résolution séparément validée | Pas de correction ou suppression automatique, service désactivé tant que reprise incomplète |
| D4 — Préconditions et identité | UUID immuable + version, aperçu signé cinq minutes, confirmation serveur, DELETE conditionnel sans corps | Ne pas réduire la sécurité au titre ou à une date |
| D5 — Reçu et conservation | Dixième table transactionnelle, champs minimaux du § 4.4, acteur pseudonyme avec FK nullable, finalité/durée/fenêtre de reprise bornées à fixer | Pas de journal illimité, pas de garantie d’issue attribuable sans reçu ; ces choix bloquent le démarrage du modèle proposé |
| D6 — Mise en service | Migration/code en maintenance coordonnée, capacité/FK attestées ; validation MySQL et sauvegardes séparément autorisées | Aucun déploiement/purge réelle sur la seule preuve SQLite |
| D7 — Reprise côté navigateur | Autoriser ou non le stockage temporaire de la seule clé d’opération, sans rôle/token/contenu | Sans conservation de clé, limite de recherche après fermeture explicitement affichée |

**NO-GO actuel pour commencer l’implémentation 6C.2**, en attente du choix D2, de la stratégie de reprise D3, du schéma/préconditions D4 et de la trace/rétention D5, puis de l’autorisation explicite de développement. D6 est une condition de mise en service et ne suppose pas que MySQL doive être contacté pendant la conception. Une fois ces décisions validées, le développement pourra être autorisé sur données fictives et harnais réinspecté ; son GO ne vaudra jamais autorisation d’exécuter une purge réelle.

Risques résiduels à annoncer : perte irréversible de contenus/motifs après validation ; erreurs de reprise historique non détectables par simple existence ; opérateur SQL privilégié ou sauvegarde ancienne contournant les identités ; absence de preuve InnoDB tant que les tests cible ne sont pas exécutés ; volume/verrous à dimensionner ; copies/media/caches hors transaction ; reçus expirés ne donnant plus de preuve d’attribution. Ces risques ne justifient aucune référence orpheline volontaire : une incapacité à satisfaire l’intégrité entraîne un refus de mise en service.

## 13. Cohérence des données personnelles — sans lot 6E

La purge éditoriale vise **un dossier**, pas toutes les données d’une personne. Elle effacerait les textes et pseudos copiés des commentaires de ce dossier, mais conserverait les comptes, leurs autres contributions et les propositions indépendantes. Les motifs de reports peuvent eux-mêmes contenir des informations personnelles : leur copie dans un journal irait à l’encontre de la minimisation retenue. L’acteur du reçu et les identifiants restent potentiellement personnels, avec accès limité et durée à justifier.

Une demande individuelle d’effacement nécessite d’identifier les données/situations concernées, pas seulement de supprimer une Story ; des conditions et exceptions peuvent intervenir. Ne pas présenter cette purge comme une conformité générale ou une procédure de droit déjà livrée. [CNIL — droit à l’effacement](https://www.cnil.fr/fr/comprendre-mes-droits/le-droit-leffacement-supprimer-vos-donnees-en-ligne).

Les durées des reçus, reports conservés dans l’alternative, sauvegardes et journaux techniques doivent être fixées selon leurs finalités ; aucune durée universelle ni conservation indéfinie n’est inventée. [CNIL — durées de conservation](https://www.cnil.fr/fr/passer-laction/les-durees-de-conservation-des-donnees). Sauvegardes, exports, médias partagés, caches et copies dans `donnees.js`/JSON ne sont pas supprimés par le DELETE SQL. Prévoir l’expiration et une restauration qui ne republie pas les données retirées, dans une intervention dédiée. Aucun développement du lot 6E, changement de politique de consentement ou procédure d’effacement de compte n’est commencé ici.

## 14. Clôture documentaire et opérations réellement réalisées

<!-- CONTROLES_6C2_CONCEPTION_START -->

**PASS statique documentaire.** 91 ressources publiques préexistantes conservées octet pour octet sur 93 inventoriées ; seuls le sommaire et la ligne C-05/son complément sont modifiés, un rapport créé. **9 modèles, 10 FK, 5 migrations et 29 opérations API existantes inchangés**, correspondance Swagger vérifiée par lecture/AST. **843 liens internes dans 22 Markdown**, dont 279 liens de lignes ; matrice de **22 remarques**, C-05 PARTIEL. Index et quatre fiches historiques inchangés. Branche, HEAD et index Git conservés ; contrôle des espaces Git passé. **36 scénarios futurs, aucun test fonctionnel ou destructif exécuté, aucune opération de base.** Les 604 PASS restent historiques. Reçus hors dépôt : `baseline.json`, `source-inventory.json`, `final-validation.json`, `file-inventory.json`.

<!-- CONTROLES_6C2_CONCEPTION_END -->

Fichiers de cette intervention : **un rapport créé**, ce document ; **deux documents mis à jour**, [sommaire](README.md) et [matrice](SUIVI_REMARQUES_JURY.md), pour pointer vers la conception. Sources applicatives, Swagger, modèles, migrations et tests conservés octet pour octet ; C-05 reste PARTIEL. Aucun résultat de test de purge revendiqué. Les 604 PASS restent historiques.

**Aucune suppression, aucun test destructif même fictif, aucun import/lancement Flask, aucune migration exécutée, aucun accès MySQL/Aiven, aucune lecture du `.env` privé, aucun Edge, changement Windows, commit ou push. Arrêt après conception ; attendre l’autorisation utilisateur avant tout code de suppression définitive.**
