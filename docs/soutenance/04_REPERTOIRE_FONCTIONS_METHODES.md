# Répertoire complet des fonctions, méthodes et propriétés expliquées

Les Petits Enquêteurs — lot 6H.21.4 — 4 novembre 2026, Europe/Paris.

**Proposition externe à lire et à approuver avant installation.** Sources : copie intégrée locale, photographiée par SHA-256 ; pas la seule version du commit Git. Analyse statique : aucun import de l’application, accès SQL, test applicatif ni migration exécutée pour cette rédaction. Les exemples sont pédagogiques et non exécutés. Leur éventuelle exécution exige un contexte temporaire distinct, préparé et autorisé ; ils ne constituent pas des scripts de démarrage du projet.

[Sommaire de soutenance](README.md) · [Correspondance avec les sources](06_CORRESPONDANCE_SOURCES.md) · [Validation documentaire](07_VALIDATION_DOCUMENTAIRE.md)

## Portée et conventions de lecture

Ce répertoire couvre **35 entrées** : 12 dans models.py (dont un lambda), 6 dans env.py, 16 dans les sept révisions (14 upgrade/downgrade et 2 inspect_legacy), et 1 gestionnaire de contexte complémentaire. Les identifiants MAH-F0001 à MAH-F0034 sont ceux du référentiel 6H.21.1. MAH-F0213 et MAH-M028 sont une extension proposée après ses 212 fonctions et 27 modules, sans renumérotation ni installation du référentiel.

Les types ci-dessous sont des types attendus ou déduits pour l’explication. Les fonctions étudiées n’ont pas d’annotations de paramètres/retour dans ces sources ; le guide ne prétend pas en ajouter. Une exception déléguée par une bibliothèque n’apparaît pas nécessairement comme raise dans le corps source.

Pour une propriété, « lecture » et « écriture » sont deux entrées distinctes. Un lambda compte comme une fonction ; les méthodes héritées ou générées ne sont pas des définitions locales. La position commence au premier décorateur lorsqu’il existe. Les anciennes lignes demeurent des repères gelés, pas la preuve que la source actuelle possède exactement le même emplacement.

Les exemples sont des usages expliqués, non exécutés. Pour les fonctions de migration ou d’environnement, l’exemple décrit le contexte et le résultat attendu ; il ne demande jamais d’importer env.py ni d’appliquer un upgrade sur une base de démonstration.

## Table d’accès

| Identifiant | Nom qualifié | Source actuelle : déclaration à fin AST | Référentiel : début gelé |
|---|---|---|---|
| [MAH-F0001](#mah-f0001) | `User.set_password` | `backend/models.py:43–45` | 43 |
| [MAH-F0002](#mah-f0002) | `User.check_password` | `backend/models.py:48–50` | 48 |
| [MAH-F0003](#mah-f0003) | `User.to_dict` | `backend/models.py:53–63` | 53 |
| [MAH-F0004](#mah-f0004) | `Story.<lambda>#01` | `backend/models.py:100–100` | 100 |
| [MAH-F0005](#mah-f0005) | `Story.to_dict` | `backend/models.py:192–210` | 192 |
| [MAH-F0006](#mah-f0006) | `Comment.to_dict` | `backend/models.py:359–371` | 359 |
| [MAH-F0007](#mah-f0007) | `Report.type[lecture]` | `backend/models.py:529–531` | 529 |
| [MAH-F0008](#mah-f0008) | `Report.type[ecriture]` | `backend/models.py:533–536` | 533 |
| [MAH-F0009](#mah-f0009) | `Report.target_id[lecture]` | `backend/models.py:538–540` | 538 |
| [MAH-F0010](#mah-f0010) | `Report.target_id[ecriture]` | `backend/models.py:542–550` | 542 |
| [MAH-F0011](#mah-f0011) | `Report.to_dict` | `backend/models.py:570–581` | 570 |
| [MAH-F0012](#mah-f0012) | `ColdCaseUpdate.to_dict` | `backend/models.py:624–633` | 624 |
| [MAH-F0013](#mah-f0013) | `get_engine` | `migrations/env.py:21–27` | 20 |
| [MAH-F0014](#mah-f0014) | `get_engine_url` | `migrations/env.py:32–37` | 31 |
| [MAH-F0015](#mah-f0015) | `get_metadata` | `migrations/env.py:55–58` | 54 |
| [MAH-F0016](#mah-f0016) | `run_migrations_offline` | `migrations/env.py:63–81` | 62 |
| [MAH-F0017](#mah-f0017) | `run_migrations_online` | `migrations/env.py:86–124` | 85 |
| [MAH-F0018](#mah-f0018) | `run_migrations_online.process_revision_directives` | `migrations/env.py:98–103` | 97 |
| [MAH-F0019](#mah-f0019) | `upgrade` | `migrations/versions/3111f5767fc6_ajoute_les_regles_on_delete.py:21–125` | 21 |
| [MAH-F0020](#mah-f0020) | `downgrade` | `migrations/versions/3111f5767fc6_ajoute_les_regles_on_delete.py:130–221` | 130 |
| [MAH-F0021](#mah-f0021) | `upgrade` | `migrations/versions/82deda84bc35_remove_legacy_comment_reports_counter.py:21–23` | 21 |
| [MAH-F0022](#mah-f0022) | `downgrade` | `migrations/versions/82deda84bc35_remove_legacy_comment_reports_counter.py:28–43` | 28 |
| [MAH-F0023](#mah-f0023) | `upgrade` | `migrations/versions/921687c1bd7c_baseline_schema.py:22–170` | 22 |
| [MAH-F0024](#mah-f0024) | `downgrade` | `migrations/versions/921687c1bd7c_baseline_schema.py:175–182` | 175 |
| [MAH-F0025](#mah-f0025) | `upgrade` | `migrations/versions/a590c8aac613_add_reports_bans_and_cold_case_updates.py:21–71` | 21 |
| [MAH-F0026](#mah-f0026) | `downgrade` | `migrations/versions/a590c8aac613_add_reports_bans_and_cold_case_updates.py:76–83` | 67 |
| [MAH-F0027](#mah-f0027) | `upgrade` | `migrations/versions/c6c100000001_add_story_archive_date.py:16–19` | 16 |
| [MAH-F0028](#mah-f0028) | `downgrade` | `migrations/versions/c6c100000001_add_story_archive_date.py:22–25` | 22 |
| [MAH-F0029](#mah-f0029) | `inspect_legacy` | `migrations/versions/c6c200000001_comment_reports_and_story_revision.py:19–39` | 19 |
| [MAH-F0030](#mah-f0030) | `upgrade` | `migrations/versions/c6c200000001_comment_reports_and_story_revision.py:42–62` | 42 |
| [MAH-F0031](#mah-f0031) | `downgrade` | `migrations/versions/c6c200000001_comment_reports_and_story_revision.py:65–80` | 65 |
| [MAH-F0032](#mah-f0032) | `inspect_legacy` | `migrations/versions/c6g200000001_add_comment_likes.py:15–45` | 15 |
| [MAH-F0033](#mah-f0033) | `upgrade` | `migrations/versions/c6g200000001_add_comment_likes.py:48–61` | 42 |
| [MAH-F0034](#mah-f0034) | `downgrade` | `migrations/versions/c6g200000001_add_comment_likes.py:65–70` | 59 |
| [MAH-F0213](#mah-f0213) | `sqlite_migration_scope` | `migrations/sqlite_safety.py:9–35` | Extension proposée |

<a id="mah-f0001"></a>

## MAH-F0001 — User.set_password

**Emplacement exact :** `backend/models.py` ; déclaration ligne 43, def/lambda ligne 43, fin AST ligne 45. **Module :** `MAH-M001`.

**SHA-256 du fichier source :** `d9f29a20a5174e7738725fe765bcc4b1270f60de9a6f71ad43c882d5f6cc175d`. Empreinte AST de la fonction disponible dans CORRESPONDANCE_IDS.json.

**Signature des arguments dans la source :** `(self, password)`. **Décorateurs :** aucun.

### Objectif général

Transformer une saisie de mot de passe en hachage stockable.

### Paramètres, types et contexte

self : User ; password : str attendu, saisie réservée à la mémoire. Aucun paramètre n’est annoté dans la source.

### Déroulement étape par étape

1. Passer password à werkzeug.security.generate_password_hash.
2. Recevoir la chaîne de hachage, incluant les informations de méthode et le sel selon Werkzeug.
3. Affecter cette chaîne à self.password_hash. Ne pas enregistrer ni afficher la saisie.

### Valeur de retour

None (absence de return explicite).

### Interactions avec les autres composants

User et les fonctions de sécurité Werkzeug ; les routes d’inscription ou de changement de mot de passe choisissent quand utiliser cette méthode.

### Effets sur la base et sur les objets

Modifie l’objet en mémoire. Sur un objet persistant suivi, l’attribut devient une modification à écrire au flush. Aucun add, flush ou commit explicite dans cette méthode.

### Exceptions, limites et risques

Type de saisie inadapté et erreurs déléguées à Werkzeug possibles. Aucune politique de longueur ou complexité n’est imposée par ce corps. La taille du hachage doit rester compatible avec String(255) et la version de dépendance réellement utilisée.

### Exemple concret d’utilisation à expliquer

Sur un compte fictif construit dans une fixture, compte.set_password(mot_de_passe_fictif) prépare son attribut ; l’appelant doit encore ajouter/valider l’objet si nécessaire. Ne jamais imprimer la saisie ou le hachage pour la démonstration.

### Repère prévu pour le lot 6H.21.6

Chemin proposé, non créé : `docs/soutenance/code-commente-mahamadou/backend/models.py`. Même identifiant `MAH-F0001` ; plage locale future `L0001` à `L0003` pour cette déclaration, blancs inclus. Formule : ligne locale = ligne source − 43 + 1. Ce calcul situe le futur commentaire ; aucune copie ligne par ligne n’est produite ici.

<a id="mah-f0002"></a>

## MAH-F0002 — User.check_password

**Emplacement exact :** `backend/models.py` ; déclaration ligne 48, def/lambda ligne 48, fin AST ligne 50. **Module :** `MAH-M001`.

**SHA-256 du fichier source :** `d9f29a20a5174e7738725fe765bcc4b1270f60de9a6f71ad43c882d5f6cc175d`. Empreinte AST de la fonction disponible dans CORRESPONDANCE_IDS.json.

**Signature des arguments dans la source :** `(self, password)`. **Décorateurs :** aucun.

### Objectif général

Comparer une saisie au hachage d’un compte sans le déchiffrer.

### Paramètres, types et contexte

self : User avec password_hash disponible ; password : str attendu. Types documentés, non annotés dans la source.

### Déroulement étape par étape

1. Lire self.password_hash.
2. Déléguer à check_password_hash le hachage et la saisie.
3. Renvoyer directement le résultat booléen de la comparaison.

### Valeur de retour

bool pour un hachage et une saisie compatibles avec le vérificateur.

### Interactions avec les autres composants

Werkzeug réalise la comparaison ; l’API combine ce résultat avec l’existence du compte et les politiques de connexion.

### Effets sur la base et sur les objets

Aucune mutation volontaire, aucun DML explicite. Lire un hachage expiré peut demander un rafraîchissement ORM si l’objet est attaché.

### Exceptions, limites et risques

Une saisie fausse produit normalement False ; un objet incomplet ou des arguments non conformes peuvent provoquer une erreur déléguée. Les formats de hachage reconnus dépendent de Werkzeug. Ne pas exposer les détails du hachage dans une erreur HTTP.

### Exemple concret d’utilisation à expliquer

compte.check_password(saisie_fictive) donne un booléen ; un résultat True n’est pas à lui seul une session authentifiée, un contrôle de bannissement ou une autorisation administrative.

### Repère prévu pour le lot 6H.21.6

Chemin proposé, non créé : `docs/soutenance/code-commente-mahamadou/backend/models.py`. Même identifiant `MAH-F0002` ; plage locale future `L0001` à `L0003` pour cette déclaration, blancs inclus. Formule : ligne locale = ligne source − 48 + 1. Ce calcul situe le futur commentaire ; aucune copie ligne par ligne n’est produite ici.

<a id="mah-f0003"></a>

## MAH-F0003 — User.to_dict

**Emplacement exact :** `backend/models.py` ; déclaration ligne 53, def/lambda ligne 53, fin AST ligne 63. **Module :** `MAH-M001`.

**SHA-256 du fichier source :** `d9f29a20a5174e7738725fe765bcc4b1270f60de9a6f71ad43c882d5f6cc175d`. Empreinte AST de la fonction disponible dans CORRESPONDANCE_IDS.json.

**Signature des arguments dans la source :** `(self)`. **Décorateurs :** aucun.

### Objectif général

Construire la représentation dictionnaire prévue pour User.

### Paramètres, types et contexte

self : User ; aucune option, aucun paramètre de filtrage ni annotation source.

### Déroulement étape par étape

1. Lire les attributs nécessaires de User.
2. Construire un nouveau dictionnaire avec les clés exactes : id, username, email, is_admin, created_at.
3. Pour created_at, appeler isoformat si la date est présente, sinon placer None.
4. Renvoyer le dictionnaire sans add, flush ou commit explicite.

### Valeur de retour

dict Python ; pas une chaîne JSON et pas une réponse HTTP Flask. Les valeurs None deviendront éventuellement null lors d’une sérialisation JSON ultérieure.

### Interactions avec les autres composants

L’appelant choisit si ce format peut être envoyé au demandeur ; le mot « public » ne signifie pas anonymisé.

### Effets sur la base et sur les objets

Lecture d’attributs et construction de valeurs en mémoire. Aucun DML explicite. Un attribut expiré peut déclencher un SELECT de rafraîchissement. Exclut password_hash et is_banned ; conserve email.

### Exceptions, limites et risques

DetachedInstanceError si un attribut indisponible demande une Session absente ; erreurs de connexion lors d’un rafraîchissement ; AttributeError si une valeur non conforme est injectée à la place d’une date. Aucun validateur complet de construction. Les dates sans fuseau ne gagnent pas automatiquement un suffixe UTC.

### Exemple concret d’utilisation à expliquer

Pour un User complet de fixture, objet.to_dict() produit le contrat décrit. Avant flush, certains id, booléens ou dates par défaut peuvent encore être absents ; cela n’est pas la preuve d’une ligne persistée.

### Repère prévu pour le lot 6H.21.6

Chemin proposé, non créé : `docs/soutenance/code-commente-mahamadou/backend/models.py`. Même identifiant `MAH-F0003` ; plage locale future `L0001` à `L0011` pour cette déclaration, blancs inclus. Formule : ligne locale = ligne source − 53 + 1. Ce calcul situe le futur commentaire ; aucune copie ligne par ligne n’est produite ici.

<a id="mah-f0004"></a>

## MAH-F0004 — Story.<lambda>#01

**Emplacement exact :** `backend/models.py` ; déclaration ligne 100, def/lambda ligne 100, fin AST ligne 100. **Module :** `MAH-M001`.

**SHA-256 du fichier source :** `d9f29a20a5174e7738725fe765bcc4b1270f60de9a6f71ad43c882d5f6cc175d`. Empreinte AST de la fonction disponible dans CORRESPONDANCE_IDS.json.

**Signature des arguments dans la source :** `()`. **Décorateurs :** aucun.

### Objectif général

Fabriquer la valeur par défaut ORM d’une révision de gestion de Story.

### Paramètres, types et contexte

Aucun paramètre explicite ; lambda sans annotation ni argument.

### Déroulement étape par étape

1. Créer un UUID version 4 par uuid4().
2. Lire sa représentation hex, chaîne de 32 caractères sans tirets.
3. Fournir cette valeur à l’INSERT pour lequel le default est sollicité.

### Valeur de retour

str de 32 caractères hexadécimaux.

### Interactions avec les autres composants

Colonne Story.management_revision ; unicité SQL et contrôles de révision des routes de gestion.

### Effets sur la base et sur les objets

Le callback ne fait aucun appel SQL lui-même ; SQLAlchemy l’utilise au moment de préparer l’INSERT. Il ne constitue pas un onupdate et ne renouvelle pas les révisions lors de chaque modification.

### Exceptions, limites et risques

Collision très improbable mais non impossible, contrôlée par UNIQUE à l’écriture ; défaut SQL sentinelle différent si INSERT brut sans valeur. Ne pas promettre une attribution immédiate dès Story(...).

### Exemple concret d’utilisation à expliquer

Une Story complète créée sans management_revision reçoit une vraie révision lors du flush ORM. Un UPDATE ultérieur doit renouveler explicitement la révision dans le chemin de gestion prévu.

### Repère prévu pour le lot 6H.21.6

Chemin proposé, non créé : `docs/soutenance/code-commente-mahamadou/backend/models.py`. Même identifiant `MAH-F0004` ; plage locale future `L0001` à `L0001` pour cette déclaration, blancs inclus. Formule : ligne locale = ligne source − 100 + 1. Ce calcul situe le futur commentaire ; aucune copie ligne par ligne n’est produite ici.

<a id="mah-f0005"></a>

## MAH-F0005 — Story.to_dict

**Emplacement exact :** `backend/models.py` ; déclaration ligne 192, def/lambda ligne 192, fin AST ligne 210. **Module :** `MAH-M001`.

**SHA-256 du fichier source :** `d9f29a20a5174e7738725fe765bcc4b1270f60de9a6f71ad43c882d5f6cc175d`. Empreinte AST de la fonction disponible dans CORRESPONDANCE_IDS.json.

**Signature des arguments dans la source :** `(self)`. **Décorateurs :** aucun.

### Objectif général

Construire la représentation dictionnaire prévue pour Story.

### Paramètres, types et contexte

self : Story ; aucune option, aucun paramètre de filtrage ni annotation source.

### Déroulement étape par étape

1. Lire les attributs nécessaires de Story.
2. Construire un nouveau dictionnaire avec les clés exactes : id, slug, title, summary, content, image_url, category_id, author_id, created_at, updated_at.
3. Pour created_at, updated_at, appeler isoformat si la date est présente, sinon placer None.
4. Renvoyer le dictionnaire sans add, flush ou commit explicite.

### Valeur de retour

dict Python ; pas une chaîne JSON et pas une réponse HTTP Flask. Les valeurs None deviendront éventuellement null lors d’une sérialisation JSON ultérieure.

### Interactions avec les autres composants

La sélection préalable doit appliquer la visibilité ; la méthode ne masque pas d’elle-même un dossier archivé.

### Effets sur la base et sur les objets

Lecture d’attributs et construction de valeurs en mémoire. Aucun DML explicite. Un attribut expiré peut déclencher un SELECT de rafraîchissement. Exclut archived_at, management_revision et toutes les contributions imbriquées.

### Exceptions, limites et risques

DetachedInstanceError si un attribut indisponible demande une Session absente ; erreurs de connexion lors d’un rafraîchissement ; AttributeError si une valeur non conforme est injectée à la place d’une date. Aucun validateur complet de construction. Les dates sans fuseau ne gagnent pas automatiquement un suffixe UTC.

### Exemple concret d’utilisation à expliquer

Pour un Story complet de fixture, objet.to_dict() produit le contrat décrit. Avant flush, certains id, booléens ou dates par défaut peuvent encore être absents ; cela n’est pas la preuve d’une ligne persistée.

### Repère prévu pour le lot 6H.21.6

Chemin proposé, non créé : `docs/soutenance/code-commente-mahamadou/backend/models.py`. Même identifiant `MAH-F0005` ; plage locale future `L0001` à `L0019` pour cette déclaration, blancs inclus. Formule : ligne locale = ligne source − 192 + 1. Ce calcul situe le futur commentaire ; aucune copie ligne par ligne n’est produite ici.

<a id="mah-f0006"></a>

## MAH-F0006 — Comment.to_dict

**Emplacement exact :** `backend/models.py` ; déclaration ligne 359, def/lambda ligne 359, fin AST ligne 371. **Module :** `MAH-M001`.

**SHA-256 du fichier source :** `d9f29a20a5174e7738725fe765bcc4b1270f60de9a6f71ad43c882d5f6cc175d`. Empreinte AST de la fonction disponible dans CORRESPONDANCE_IDS.json.

**Signature des arguments dans la source :** `(self)`. **Décorateurs :** aucun.

### Objectif général

Construire la représentation dictionnaire prévue pour Comment.

### Paramètres, types et contexte

self : Comment ; aucune option, aucun paramètre de filtrage ni annotation source.

### Déroulement étape par étape

1. Lire les attributs nécessaires de Comment.
2. Construire un nouveau dictionnaire avec les clés exactes : id, story_id, user_id, username, text, likes, created_at.
3. Pour created_at, appeler isoformat si la date est présente, sinon placer None.
4. Renvoyer le dictionnaire sans add, flush ou commit explicite.

### Valeur de retour

dict Python ; pas une chaîne JSON et pas une réponse HTTP Flask. Les valeurs None deviendront éventuellement null lors d’une sérialisation JSON ultérieure.

### Interactions avec les autres composants

Le sérialiseur API enrichi comment_to_dict compte les likes individuels si le compteur historique est exactement l’entier zéro ; sinon il conserve la valeur historique et indique son incompatibilité. Il compte aussi les signalements ; les deux chemins ne sont pas interchangeables.

### Effets sur la base et sur les objets

Lecture d’attributs et construction de valeurs en mémoire. Aucun DML explicite. Un attribut expiré peut déclencher un SELECT de rafraîchissement. Lit le compteur physique likes ; ne calcule pas les nouveaux totaux.

### Exceptions, limites et risques

DetachedInstanceError si un attribut indisponible demande une Session absente ; erreurs de connexion lors d’un rafraîchissement ; AttributeError si une valeur non conforme est injectée à la place d’une date. Aucun validateur complet de construction. Les dates sans fuseau ne gagnent pas automatiquement un suffixe UTC.

### Exemple concret d’utilisation à expliquer

Pour un Comment complet de fixture, objet.to_dict() produit le contrat décrit. Avant flush, certains id, booléens ou dates par défaut peuvent encore être absents ; cela n’est pas la preuve d’une ligne persistée.

### Repère prévu pour le lot 6H.21.6

Chemin proposé, non créé : `docs/soutenance/code-commente-mahamadou/backend/models.py`. Même identifiant `MAH-F0006` ; plage locale future `L0001` à `L0013` pour cette déclaration, blancs inclus. Formule : ligne locale = ligne source − 359 + 1. Ce calcul situe le futur commentaire ; aucune copie ligne par ligne n’est produite ici.

<a id="mah-f0007"></a>

## MAH-F0007 — Report.type[lecture]

**Emplacement exact :** `backend/models.py` ; déclaration ligne 529, def/lambda ligne 530, fin AST ligne 531. **Module :** `MAH-M001`.

**SHA-256 du fichier source :** `d9f29a20a5174e7738725fe765bcc4b1270f60de9a6f71ad43c882d5f6cc175d`. Empreinte AST de la fonction disponible dans CORRESPONDANCE_IDS.json.

**Signature des arguments dans la source :** `(self)`. **Décorateurs :** `property`.

### Objectif général

Conserver en Python le type historique d’un signalement de commentaire.

### Paramètres, types et contexte

self : Report ; accesseur de propriété sans argument utilisateur.

### Déroulement étape par étape

1. Accéder à report.type.
2. Renvoyer la constante "comment", sans consulter une colonne type.

### Valeur de retour

str, exactement "comment".

### Interactions avec les autres composants

Report.to_dict et l’ancien contrat de représentation générique.

### Effets sur la base et sur les objets

Aucun changement ni SQL explicite ; aucune colonne type n’est ajoutée au schéma.

### Exceptions, limites et risques

Aucun raise direct. Lire cette propriété ne prouve ni que comment_id est renseigné, ni que le commentaire existe. La constante ne permet pas de créer une cible de type Story.

### Exemple concret d’utilisation à expliquer

Pour un Report en mémoire même encore incomplet, report.type vaut "comment". Sa persistance exigera un comment_id valide et les autres colonnes obligatoires.

### Repère prévu pour le lot 6H.21.6

Chemin proposé, non créé : `docs/soutenance/code-commente-mahamadou/backend/models.py`. Même identifiant `MAH-F0007` ; plage locale future `L0001` à `L0003` pour cette déclaration, blancs inclus. Formule : ligne locale = ligne source − 529 + 1. Ce calcul situe le futur commentaire ; aucune copie ligne par ligne n’est produite ici.

<a id="mah-f0008"></a>

## MAH-F0008 — Report.type[ecriture]

**Emplacement exact :** `backend/models.py` ; déclaration ligne 533, def/lambda ligne 534, fin AST ligne 536. **Module :** `MAH-M001`.

**SHA-256 du fichier source :** `d9f29a20a5174e7738725fe765bcc4b1270f60de9a6f71ad43c882d5f6cc175d`. Empreinte AST de la fonction disponible dans CORRESPONDANCE_IDS.json.

**Signature des arguments dans la source :** `(self, value)`. **Décorateurs :** `type.setter`.

### Objectif général

Accepter uniquement le type de compatibilité pris en charge.

### Paramètres, types et contexte

self : Report ; value : valeur comparée à la chaîne "comment", str attendu par le contrat. Aucun type source annoté.

### Déroulement étape par étape

1. Comparer value à "comment".
2. Si la valeur diffère, lever ValueError.
3. Si elle est acceptée, terminer sans stocker un attribut ou émettre de SQL.

### Valeur de retour

None en cas d’acceptation.

### Interactions avec les autres composants

Ancienne syntaxe de construction/affectation compatible avec Report ; cible réellement stockée par comment_id.

### Effets sur la base et sur les objets

Aucune colonne ni valeur persistante modifiée par cet accesseur.

### Exceptions, limites et risques

ValueError explicite pour "story", une valeur absente ou une autre valeur non égale à la constante. Ce contrôle ne vérifie pas la cible et ne remplace pas le contrat HTTP.

### Exemple concret d’utilisation à expliquer

report.type = "comment" est accepté ; report.type = "story" est refusé. La première affectation ne crée pas une ligne de report.

### Repère prévu pour le lot 6H.21.6

Chemin proposé, non créé : `docs/soutenance/code-commente-mahamadou/backend/models.py`. Même identifiant `MAH-F0008` ; plage locale future `L0001` à `L0004` pour cette déclaration, blancs inclus. Formule : ligne locale = ligne source − 533 + 1. Ce calcul situe le futur commentaire ; aucune copie ligne par ligne n’est produite ici.

<a id="mah-f0009"></a>

## MAH-F0009 — Report.target_id[lecture]

**Emplacement exact :** `backend/models.py` ; déclaration ligne 538, def/lambda ligne 539, fin AST ligne 540. **Module :** `MAH-M001`.

**SHA-256 du fichier source :** `d9f29a20a5174e7738725fe765bcc4b1270f60de9a6f71ad43c882d5f6cc175d`. Empreinte AST de la fonction disponible dans CORRESPONDANCE_IDS.json.

**Signature des arguments dans la source :** `(self)`. **Décorateurs :** `property`.

### Objectif général

Exposer comment_id sous la forme textuelle du contrat historique.

### Paramètres, types et contexte

self : Report ; propriété de lecture sans argument utilisateur.

### Déroulement étape par étape

1. Lire self.comment_id.
2. Appliquer str à cette valeur.
3. Renvoyer la chaîne produite, sans accès à une colonne target_id.

### Valeur de retour

str ; par exemple "23" pour comment_id=23, et "None" pour un objet incomplet avec comment_id=None.

### Interactions avec les autres composants

Report.to_dict consomme cette propriété ; le schéma physique possède comment_id.

### Effets sur la base et sur les objets

Aucun DML explicite ; un attribut ORM expiré peut nécessiter un SELECT.

### Exceptions, limites et risques

Pas de validation positive dans le getter. Il ne faut pas sérialiser un Report incomplet en supposant un identifiant numérique valide. Les risques de détachement ORM restent applicables.

### Exemple concret d’utilisation à expliquer

Sur un objet complet lié au commentaire fictif 23, lire report.target_id renvoie "23". Une requête SQL actuelle doit filtrer reports.comment_id et non reports.target_id.

### Repère prévu pour le lot 6H.21.6

Chemin proposé, non créé : `docs/soutenance/code-commente-mahamadou/backend/models.py`. Même identifiant `MAH-F0009` ; plage locale future `L0001` à `L0003` pour cette déclaration, blancs inclus. Formule : ligne locale = ligne source − 538 + 1. Ce calcul situe le futur commentaire ; aucune copie ligne par ligne n’est produite ici.

<a id="mah-f0010"></a>

## MAH-F0010 — Report.target_id[ecriture]

**Emplacement exact :** `backend/models.py` ; déclaration ligne 542, def/lambda ligne 543, fin AST ligne 550. **Module :** `MAH-M001`.

**SHA-256 du fichier source :** `d9f29a20a5174e7738725fe765bcc4b1270f60de9a6f71ad43c882d5f6cc175d`. Empreinte AST de la fonction disponible dans CORRESPONDANCE_IDS.json.

**Signature des arguments dans la source :** `(self, value)`. **Décorateurs :** `target_id.setter`.

### Objectif général

Valider une chaîne canonique d’identifiant puis la convertir en comment_id.

### Paramètres, types et contexte

self : Report ; value : str exigée, composée de chiffres décimaux ASCII, sans zéro initial, borne de 1 à 2147483647.

### Déroulement étape par étape

1. Vérifier le type str, le caractère ASCII et la présence exclusive de chiffres décimaux.
2. Refuser un début par zéro et une longueur supérieure à dix caractères.
3. Vérifier l’intervalle entier autorisé ; les conditions précédentes permettent une conversion sûre de la chaîne attendue.
4. Affecter int(value) à self.comment_id.

### Valeur de retour

None ; la valeur convertie est placée dans comment_id.

### Interactions avec les autres composants

FK reports.comment_id → comments.id ; le parseur de l’API suit son propre chemin et peut affecter directement l’entier validé.

### Effets sur la base et sur les objets

Mutation d’attribut ORM, pas de requête d’existence ni de commit. La contrainte FK sera contrôlée à la persistance si elle est active.

### Exceptions, limites et risques

ValueError pour 23 entier, "", "0", "01", "+1", " 1", "1.0", des chiffres non ASCII, ou "2147483648". Affecter directement comment_id contourne ce setter de format, sans supprimer la FK SQL.

### Exemple concret d’utilisation à expliquer

report.target_id = "23" prépare comment_id=23. Si aucun commentaire de cette PK n’existe, la validation du format réussit mais l’écriture peut échouer sur la FK.

### Repère prévu pour le lot 6H.21.6

Chemin proposé, non créé : `docs/soutenance/code-commente-mahamadou/backend/models.py`. Même identifiant `MAH-F0010` ; plage locale future `L0001` à `L0009` pour cette déclaration, blancs inclus. Formule : ligne locale = ligne source − 542 + 1. Ce calcul situe le futur commentaire ; aucune copie ligne par ligne n’est produite ici.

<a id="mah-f0011"></a>

## MAH-F0011 — Report.to_dict

**Emplacement exact :** `backend/models.py` ; déclaration ligne 570, def/lambda ligne 570, fin AST ligne 581. **Module :** `MAH-M001`.

**SHA-256 du fichier source :** `d9f29a20a5174e7738725fe765bcc4b1270f60de9a6f71ad43c882d5f6cc175d`. Empreinte AST de la fonction disponible dans CORRESPONDANCE_IDS.json.

**Signature des arguments dans la source :** `(self)`. **Décorateurs :** aucun.

### Objectif général

Construire la représentation dictionnaire prévue pour Report.

### Paramètres, types et contexte

self : Report ; aucune option, aucun paramètre de filtrage ni annotation source.

### Déroulement étape par étape

1. Lire les attributs nécessaires de Report.
2. Construire un nouveau dictionnaire avec les clés exactes : id, type, target_id, reason, status, created_at.
3. Pour created_at, appeler isoformat si la date est présente, sinon placer None.
4. Lire self.type puis self.target_id, donc les accesseurs Python, pas des colonnes SQL homonymes.
5. Renvoyer le dictionnaire sans add, flush ou commit explicite.

### Valeur de retour

dict Python ; pas une chaîne JSON et pas une réponse HTTP Flask. Les valeurs None deviendront éventuellement null lors d’une sérialisation JSON ultérieure.

### Interactions avec les autres composants

Le motif peut être sensible ; l’accès administratif ou autre filtrage reste à la charge des routes.

### Effets sur la base et sur les objets

Lecture d’attributs et construction de valeurs en mémoire. Aucun DML explicite. Un attribut expiré peut déclencher un SELECT de rafraîchissement. Calcule type et target_id via les propriétés ; n’expose pas comment_id comme clé séparée.

### Exceptions, limites et risques

DetachedInstanceError si un attribut indisponible demande une Session absente ; erreurs de connexion lors d’un rafraîchissement ; AttributeError si une valeur non conforme est injectée à la place d’une date. Aucun validateur complet de construction. Les dates sans fuseau ne gagnent pas automatiquement un suffixe UTC.

### Exemple concret d’utilisation à expliquer

Pour un Report complet de fixture, objet.to_dict() produit le contrat décrit. Un Report incomplet peut donner target_id="None" : il faut préparer un objet valide avant de l’exposer.

### Repère prévu pour le lot 6H.21.6

Chemin proposé, non créé : `docs/soutenance/code-commente-mahamadou/backend/models.py`. Même identifiant `MAH-F0011` ; plage locale future `L0001` à `L0012` pour cette déclaration, blancs inclus. Formule : ligne locale = ligne source − 570 + 1. Ce calcul situe le futur commentaire ; aucune copie ligne par ligne n’est produite ici.

<a id="mah-f0012"></a>

## MAH-F0012 — ColdCaseUpdate.to_dict

**Emplacement exact :** `backend/models.py` ; déclaration ligne 624, def/lambda ligne 624, fin AST ligne 633. **Module :** `MAH-M001`.

**SHA-256 du fichier source :** `d9f29a20a5174e7738725fe765bcc4b1270f60de9a6f71ad43c882d5f6cc175d`. Empreinte AST de la fonction disponible dans CORRESPONDANCE_IDS.json.

**Signature des arguments dans la source :** `(self)`. **Décorateurs :** aucun.

### Objectif général

Construire la représentation dictionnaire prévue pour ColdCaseUpdate.

### Paramètres, types et contexte

self : ColdCaseUpdate ; aucune option, aucun paramètre de filtrage ni annotation source.

### Déroulement étape par étape

1. Lire les attributs nécessaires de ColdCaseUpdate.
2. Construire un nouveau dictionnaire avec les clés exactes : id, story_id, content, created_at.
3. Pour created_at, appeler isoformat si la date est présente, sinon placer None.
4. Renvoyer le dictionnaire sans add, flush ou commit explicite.

### Valeur de retour

dict Python ; pas une chaîne JSON et pas une réponse HTTP Flask. Les valeurs None deviendront éventuellement null lors d’une sérialisation JSON ultérieure.

### Interactions avec les autres composants

Le dossier parent n’est pas revalidé par ce sérialiseur.

### Effets sur la base et sur les objets

Lecture d’attributs et construction de valeurs en mémoire. Aucun DML explicite. Un attribut expiré peut déclencher un SELECT de rafraîchissement. Ne produit ni auteur ni titre absent du modèle.

### Exceptions, limites et risques

DetachedInstanceError si un attribut indisponible demande une Session absente ; erreurs de connexion lors d’un rafraîchissement ; AttributeError si une valeur non conforme est injectée à la place d’une date. Aucun validateur complet de construction. Les dates sans fuseau ne gagnent pas automatiquement un suffixe UTC.

### Exemple concret d’utilisation à expliquer

Pour un ColdCaseUpdate complet de fixture, objet.to_dict() produit le contrat décrit. Avant flush, certains id, booléens ou dates par défaut peuvent encore être absents ; cela n’est pas la preuve d’une ligne persistée.

### Repère prévu pour le lot 6H.21.6

Chemin proposé, non créé : `docs/soutenance/code-commente-mahamadou/backend/models.py`. Même identifiant `MAH-F0012` ; plage locale future `L0001` à `L0010` pour cette déclaration, blancs inclus. Formule : ligne locale = ligne source − 624 + 1. Ce calcul situe le futur commentaire ; aucune copie ligne par ligne n’est produite ici.

<a id="mah-f0013"></a>

## MAH-F0013 — get_engine

**Emplacement exact :** `migrations/env.py` ; déclaration ligne 21, def/lambda ligne 21, fin AST ligne 27. **Module :** `MAH-M002`.

**SHA-256 du fichier source :** `164deb298151eaf27680109c4b54a6819aeb83ef385b57482278a2311e91031c`. Empreinte AST de la fonction disponible dans CORRESPONDANCE_IDS.json.

**Signature des arguments dans la source :** `()`. **Décorateurs :** aucun.

### Objectif général

Obtenir le moteur déjà configuré par l’extension Flask-Migrate.

### Paramètres, types et contexte

Aucun argument ; dépend de current_app dans un contexte Flask valide et de extensions["migrate"].db.

### Déroulement étape par étape

1. Essayer l’ancienne interface db.get_engine().
2. Si cet appel lève TypeError ou AttributeError, utiliser db.engine.
3. Renvoyer le moteur existant ; ne pas fabriquer un chemin de base pour la documentation.

### Valeur de retour

Engine SQLAlchemy attendu, correspondant à la configuration de l’application.

### Interactions avec les autres composants

Flask current_app, Flask-Migrate, Flask-SQLAlchemy ; utilisé par get_engine_url et run_migrations_online.

### Effets sur la base et sur les objets

Accès à la configuration du moteur ; aucun connect() explicite dans cette fonction, aucun DDL. Son résultat donne toutefois accès à une base si un appelant le connecte.

### Exceptions, limites et risques

RuntimeError hors contexte Flask ; KeyError si extension absente ; erreurs de configuration non couvertes par les deux exceptions de compatibilité. Le fallback ne masque pas toutes les erreurs.

### Exemple concret d’utilisation à expliquer

Dans un vrai contexte Alembic autorisé, run_migrations_online récupère ce moteur avant connect(). Pour ce lot, le corps est seulement parsé, pas appelé.

### Repère prévu pour le lot 6H.21.6

Chemin proposé, non créé : `docs/soutenance/code-commente-mahamadou/migrations/env.py`. Même identifiant `MAH-F0013` ; plage locale future `L0001` à `L0007` pour cette déclaration, blancs inclus. Formule : ligne locale = ligne source − 21 + 1. Ce calcul situe le futur commentaire ; aucune copie ligne par ligne n’est produite ici.

<a id="mah-f0014"></a>

## MAH-F0014 — get_engine_url

**Emplacement exact :** `migrations/env.py` ; déclaration ligne 32, def/lambda ligne 32, fin AST ligne 37. **Module :** `MAH-M002`.

**SHA-256 du fichier source :** `164deb298151eaf27680109c4b54a6819aeb83ef385b57482278a2311e91031c`. Empreinte AST de la fonction disponible dans CORRESPONDANCE_IDS.json.

**Signature des arguments dans la source :** `()`. **Décorateurs :** aucun.

### Objectif général

Préparer l’URL SQL pour la configuration d’Alembic.

### Paramètres, types et contexte

Aucun argument ; dépend de get_engine().url.

### Déroulement étape par étape

1. Demander render_as_string(hide_password=False) à l’URL du moteur.
2. Échapper chaque % en %% pour la configuration.
3. Si AttributeError, utiliser str(get_engine().url) puis le même remplacement.

### Valeur de retour

str pouvant contenir des identifiants de connexion ; valeur privée à ne pas afficher.

### Interactions avec les autres composants

get_engine et config.set_main_option("sqlalchemy.url", ...) au niveau du module env.py.

### Effets sur la base et sur les objets

Construction de chaîne ; aucun SQL exécuté directement. La configuration Alembic reçoit ensuite l’URL.

### Exceptions, limites et risques

Mêmes dépendances de contexte que get_engine ; autres erreurs d’URL/configuration possibles. Le fallback str dépend du comportement de la version concernée et ne doit pas être vanté comme un masque de sécurité. Une URL ne doit pas apparaître dans les livrables.

### Exemple concret d’utilisation à expliquer

Alembic utilise la valeur en interne pour sa connexion ou sa configuration offline. L’exemple pédagogique ne montre volontairement aucun appel print ni URL réelle.

### Repère prévu pour le lot 6H.21.6

Chemin proposé, non créé : `docs/soutenance/code-commente-mahamadou/migrations/env.py`. Même identifiant `MAH-F0014` ; plage locale future `L0001` à `L0006` pour cette déclaration, blancs inclus. Formule : ligne locale = ligne source − 32 + 1. Ce calcul situe le futur commentaire ; aucune copie ligne par ligne n’est produite ici.

<a id="mah-f0015"></a>

## MAH-F0015 — get_metadata

**Emplacement exact :** `migrations/env.py` ; déclaration ligne 55, def/lambda ligne 55, fin AST ligne 58. **Module :** `MAH-M002`.

**SHA-256 du fichier source :** `164deb298151eaf27680109c4b54a6819aeb83ef385b57482278a2311e91031c`. Empreinte AST de la fonction disponible dans CORRESPONDANCE_IDS.json.

**Signature des arguments dans la source :** `()`. **Décorateurs :** aucun.

### Objectif général

Fournir les métadonnées des modèles à Alembic.

### Paramètres, types et contexte

Aucun argument ; target_db est issu de l’extension de migration du contexte Flask.

### Déroulement étape par étape

1. Tester si target_db expose metadatas.
2. Si oui, renvoyer target_db.metadatas[None].
3. Sinon, renvoyer target_db.metadata.

### Valeur de retour

MetaData attendu pour le bind par défaut.

### Interactions avec les autres composants

Configuration d’autogenerate et des parcours offline/online.

### Effets sur la base et sur les objets

Lecture d’une structure Python ; pas d’inspection de la base en service dans cette fonction.

### Exceptions, limites et risques

KeyError si le bind None n’existe pas, attribut manquant ou extension non configurée. Aucune preuve de conformité d’une base réelle ne découle de ce retour.

### Exemple concret d’utilisation à expliquer

context.configure reçoit target_metadata=get_metadata() afin de connaître le schéma attendu. Cela n’applique pas automatiquement une différence aux tables.

### Repère prévu pour le lot 6H.21.6

Chemin proposé, non créé : `docs/soutenance/code-commente-mahamadou/migrations/env.py`. Même identifiant `MAH-F0015` ; plage locale future `L0001` à `L0004` pour cette déclaration, blancs inclus. Formule : ligne locale = ligne source − 55 + 1. Ce calcul situe le futur commentaire ; aucune copie ligne par ligne n’est produite ici.

<a id="mah-f0016"></a>

## MAH-F0016 — run_migrations_offline

**Emplacement exact :** `migrations/env.py` ; déclaration ligne 63, def/lambda ligne 63, fin AST ligne 81. **Module :** `MAH-M002`.

**SHA-256 du fichier source :** `164deb298151eaf27680109c4b54a6819aeb83ef385b57482278a2311e91031c`. Empreinte AST de la fonction disponible dans CORRESPONDANCE_IDS.json.

**Signature des arguments dans la source :** `()`. **Décorateurs :** aucun.

### Objectif général

Exécuter le parcours de génération SQL sans connexion de migration.

### Paramètres, types et contexte

Aucun argument ; config et context Alembic doivent être établis.

### Déroulement étape par étape

1. Lire sqlalchemy.url depuis config.
2. Configurer le contexte avec l’URL, les métadonnées et literal_binds=True.
3. Entrer dans context.begin_transaction puis appeler context.run_migrations.

### Valeur de retour

None normalement ; les instructions SQL sont produites par le contexte offline, pas renvoyées comme chaîne par la fonction.

### Interactions avec les autres composants

get_metadata et les fonctions des révisions parcourues par Alembic.

### Effets sur la base et sur les objets

Pas de connexion de migration créée par ce corps ; sortie SQL possible. Le chargement d’env.py dépend tout de même de la configuration Flask.

### Exceptions, limites et risques

Les inspect_legacy qui interrogent des données ne sont pas satisfaits par une simple sortie offline. Ne pas annoncer une génération complète réussie de ces sept révisions. Les erreurs de configuration restent possibles.

### Exemple concret d’utilisation à expliquer

Un parcours offline sert à examiner des DDL compatibles avec ce mode ; il ne prouve pas la convertibilité des anciens reports ni des compteurs de likes. Aucun parcours offline n’est exécuté ici.

### Repère prévu pour le lot 6H.21.6

Chemin proposé, non créé : `docs/soutenance/code-commente-mahamadou/migrations/env.py`. Même identifiant `MAH-F0016` ; plage locale future `L0001` à `L0019` pour cette déclaration, blancs inclus. Formule : ligne locale = ligne source − 63 + 1. Ce calcul situe le futur commentaire ; aucune copie ligne par ligne n’est produite ici.

<a id="mah-f0017"></a>

## MAH-F0017 — run_migrations_online

**Emplacement exact :** `migrations/env.py` ; déclaration ligne 86, def/lambda ligne 86, fin AST ligne 124. **Module :** `MAH-M002`.

**SHA-256 du fichier source :** `164deb298151eaf27680109c4b54a6819aeb83ef385b57482278a2311e91031c`. Empreinte AST de la fonction disponible dans CORRESPONDANCE_IDS.json.

**Signature des arguments dans la source :** `()`. **Décorateurs :** aucun.

### Objectif général

Configurer une connexion puis appliquer les migrations dans le contexte online.

### Paramètres, types et contexte

Aucun argument ; contexte Flask-Migrate et Alembic existant, configuration du moteur et destination autorisée.

### Déroulement étape par étape

1. Définir le callback interne process_revision_directives.
2. Lire le dictionnaire configure_args et y installer le callback seulement si aucun callback n’est déjà configuré.
3. Obtenir le moteur, puis ouvrir connectable.connect().
4. Si le dialecte est SQLite, entrer dans sqlite_migration_scope, configurer Alembic avec la connexion et les métadonnées, puis lancer les migrations dans son contexte de transaction.
5. Sinon, configurer le contexte et appeler run_migrations sous context.begin_transaction, sans l’enveloppe PRAGMA SQLite.

### Valeur de retour

None en cas de parcours normal.

### Interactions avec les autres composants

get_engine, get_metadata, callback interne, sqlite_migration_scope et tous les upgrade/downgrade choisis par Alembic.

### Effets sur la base et sur les objets

Ouvre une connexion et peut modifier schéma et données. Modifie aussi le dictionnaire configure_args en y ajoutant éventuellement le callback. Ce chemin n’est pas lancé pour la documentation.

### Exceptions, limites et risques

Connexion, configuration, exceptions des révisions et du scope ; maintenance exclusive non imposée par ce seul code. Un contexte de transaction Alembic n’assure pas l’annulation globale des DDL MySQL.

### Exemple concret d’utilisation à expliquer

Dans une campagne de migration séparément autorisée sur une fixture neuve, Alembic choisit ce chemin. Ne jamais importer env.py pour « voir » ses fonctions : son bas de fichier appelle le parcours choisi.

### Repère prévu pour le lot 6H.21.6

Chemin proposé, non créé : `docs/soutenance/code-commente-mahamadou/migrations/env.py`. Même identifiant `MAH-F0017` ; plage locale future `L0001` à `L0039` pour cette déclaration, blancs inclus. Formule : ligne locale = ligne source − 86 + 1. Ce calcul situe le futur commentaire ; aucune copie ligne par ligne n’est produite ici.

<a id="mah-f0018"></a>

## MAH-F0018 — run_migrations_online.process_revision_directives

**Emplacement exact :** `migrations/env.py` ; déclaration ligne 98, def/lambda ligne 98, fin AST ligne 103. **Module :** `MAH-M002`.

**SHA-256 du fichier source :** `164deb298151eaf27680109c4b54a6819aeb83ef385b57482278a2311e91031c`. Empreinte AST de la fonction disponible dans CORRESPONDANCE_IDS.json.

**Signature des arguments dans la source :** `(context, revision, directives)`. **Décorateurs :** aucun.

### Objectif général

Éviter une révision autogénérée vide dans le chemin prévu.

### Paramètres, types et contexte

context : MigrationContext attendu ; revision : repère de révision transmis par Alembic ; directives : liste mutable contenant normalement un MigrationScript. Les deux premiers paramètres ne sont pas utilisés par ce corps. Types documentés, non annotés.

### Déroulement étape par étape

1. Consulter le drapeau config.cmd_opts.autogenerate via getattr(..., False).
2. Si vrai, prendre directives[0].
3. Si script.upgrade_ops.is_empty(), vider la liste en place avec directives[:] = [] et journaliser un message générique.

### Valeur de retour

None ; la liste de directives est l’objet modifié.

### Interactions avec les autres composants

Fonction locale à run_migrations_online ; passe dans configure_args quand aucun callback alternatif n’existe.

### Effets sur la base et sur les objets

Mutation de liste et journalisation, sans DDL ni DML direct.

### Exceptions, limites et risques

Si le contrat Alembic n’est pas satisfait, liste vide ou objet incomplet peuvent produire IndexError/AttributeError. Ce callback ne teste ni les données, ni l’exécution future, ni l’innocuité d’un schéma.

### Exemple concret d’utilisation à expliquer

Lors d’un autogenerate qui ne détecte aucune opération, une directive vide est retirée. Si une vraie opération existe, la liste reste présente ; la migration doit encore être revue.

### Repère prévu pour le lot 6H.21.6

Chemin proposé, non créé : `docs/soutenance/code-commente-mahamadou/migrations/env.py`. Même identifiant `MAH-F0018` ; plage locale future `L0001` à `L0006` pour cette déclaration, blancs inclus. Formule : ligne locale = ligne source − 98 + 1. Ce calcul situe le futur commentaire ; aucune copie ligne par ligne n’est produite ici.

<a id="mah-f0019"></a>

## MAH-F0019 — upgrade

**Emplacement exact :** `migrations/versions/3111f5767fc6_ajoute_les_regles_on_delete.py` ; déclaration ligne 21, def/lambda ligne 21, fin AST ligne 125. **Module :** `MAH-M003`.

**SHA-256 du fichier source :** `0c03a3067099d4e3b651dbe88575462f383b37095e4407e56b95ea98b4a5aba4`. Empreinte AST de la fonction disponible dans CORRESPONDANCE_IDS.json.

**Signature des arguments dans la source :** `()`. **Décorateurs :** aucun.

### Objectif général

Appliquer la transition vers 3111f5767fc6 : Rendre explicites les règles de suppression.

### Paramètres, types et contexte

Aucun argument explicite. op est la façade Alembic du contexte courant ; op.get_bind() fournit la connexion quand le corps en a besoin. Le schéma doit être à la révision attendue et la destination temporaire autorisée.

### Déroulement étape par étape

1. Dans comments, supprimer comments_ibfk_1 et comments_ibfk_2 ; créer fk_comments_story vers stories.id avec CASCADE et fk_comments_user vers users.id avec SET NULL.
2. Dans proposals, supprimer proposals_ibfk_1 ; créer fk_proposals_user vers users.id avec CASCADE.
3. Dans theories, supprimer theories_ibfk_1 et theories_ibfk_2 ; créer fk_theories_story avec CASCADE et fk_theories_user avec SET NULL.
4. Dans votes, supprimer votes_ibfk_1 et votes_ibfk_2 ; créer fk_votes_story et fk_votes_user, tous deux CASCADE. La contrainte unique du couple reste distincte.

### Valeur de retour

None en fin normale ; les résultats sont les changements de schéma/données et l’état du contexte Alembic, pas une nouvelle liste d’objets ORM.

### Interactions avec les autres composants

Module MAH-M003 ; SQLAlchemy Core et Alembic, sans création d’instances des modèles courants. Les contraintes citent les tables parentes décrites dans le guide des relations.

### Effets sur la base et sur les objets

Les références d’auteur déjà nullables de comments et theories permettent SET NULL sans ajouter une modification de nullable. Aucun UPDATE de contenu n’apparaît. Une reconstruction de table copie les lignes conservées. Après application, les futurs DELETE de parents peuvent produire des effets différents : le changement de contrainte a donc des conséquences métier même sans DML explicite dans la migration. Le détail upgrade est explicité ci-dessus ; aucun de ces effets n’a été produit dans ce lot.

### Exceptions, limites et risques

Une base présentant déjà des noms différents ou des données hors intégrité doit être examinée avant une campagne. Downgrade retire les règles, mais ne retrouve pas les enfants effacés lors d’anciens DELETE CASCADE, ni l’identité de comptes retirée par SET NULL. Ne pas assimiler inverse du schéma et restauration de données.  Erreurs de DDL, réflexion, contrainte, droits ou connexion déléguées possibles. Sur MySQL, un échec tardif peut suivre des DDL déjà commités.

### Exemple concret d’utilisation à expliquer

Exemple de lecture, sans commande à lancer : comparer la FK comments.user_id avant et après : le parent est le même, la nouvelle action est SET NULL.

### Repère prévu pour le lot 6H.21.6

Chemin proposé, non créé : `docs/soutenance/code-commente-mahamadou/migrations/versions/3111f5767fc6_ajoute_les_regles_on_delete.py`. Même identifiant `MAH-F0019` ; plage locale future `L0001` à `L0105` pour cette déclaration, blancs inclus. Formule : ligne locale = ligne source − 21 + 1. Ce calcul situe le futur commentaire ; aucune copie ligne par ligne n’est produite ici.

<a id="mah-f0020"></a>

## MAH-F0020 — downgrade

**Emplacement exact :** `migrations/versions/3111f5767fc6_ajoute_les_regles_on_delete.py` ; déclaration ligne 130, def/lambda ligne 130, fin AST ligne 221. **Module :** `MAH-M003`.

**SHA-256 du fichier source :** `0c03a3067099d4e3b651dbe88575462f383b37095e4407e56b95ea98b4a5aba4`. Empreinte AST de la fonction disponible dans CORRESPONDANCE_IDS.json.

**Signature des arguments dans la source :** `()`. **Décorateurs :** aucun.

### Objectif général

Revenir au schéma parent de 3111f5767fc6 : Rendre explicites les règles de suppression.

### Paramètres, types et contexte

Aucun argument explicite. op est la façade Alembic du contexte courant ; op.get_bind() fournit la connexion quand le corps en a besoin. Le schéma doit être à la révision attendue et la destination temporaire autorisée.

### Déroulement étape par étape

1. Traiter votes, theories, proposals puis comments : supprimer les sept nouvelles FK nommées.
2. Recréer les contraintes anciennes *_ibfk_* sur les mêmes colonnes et parents, sans ON DELETE explicite. Ne pas attribuer à ce retour une restauration des lignes antérieurement supprimées.

### Valeur de retour

None en fin normale ; les résultats sont les changements de schéma/données et l’état du contexte Alembic, pas une nouvelle liste d’objets ORM.

### Interactions avec les autres composants

Module MAH-M003 ; SQLAlchemy Core et Alembic, sans création d’instances des modèles courants. Les contraintes citent les tables parentes décrites dans le guide des relations.

### Effets sur la base et sur les objets

Les références d’auteur déjà nullables de comments et theories permettent SET NULL sans ajouter une modification de nullable. Aucun UPDATE de contenu n’apparaît. Une reconstruction de table copie les lignes conservées. Après application, les futurs DELETE de parents peuvent produire des effets différents : le changement de contrainte a donc des conséquences métier même sans DML explicite dans la migration. Le détail downgrade est explicité ci-dessus ; aucun de ces effets n’a été produit dans ce lot.

### Exceptions, limites et risques

Une base présentant déjà des noms différents ou des données hors intégrité doit être examinée avant une campagne. Downgrade retire les règles, mais ne retrouve pas les enfants effacés lors d’anciens DELETE CASCADE, ni l’identité de comptes retirée par SET NULL. Ne pas assimiler inverse du schéma et restauration de données.  Erreurs de DDL, réflexion, contrainte, droits ou connexion déléguées possibles. Sur MySQL, un échec tardif peut suivre des DDL déjà commités.

### Exemple concret d’utilisation à expliquer

Exemple de lecture, sans commande à lancer : revenir aux anciens noms de FK sans reconstruire les enfants déjà supprimés.

### Repère prévu pour le lot 6H.21.6

Chemin proposé, non créé : `docs/soutenance/code-commente-mahamadou/migrations/versions/3111f5767fc6_ajoute_les_regles_on_delete.py`. Même identifiant `MAH-F0020` ; plage locale future `L0001` à `L0092` pour cette déclaration, blancs inclus. Formule : ligne locale = ligne source − 130 + 1. Ce calcul situe le futur commentaire ; aucune copie ligne par ligne n’est produite ici.

<a id="mah-f0021"></a>

## MAH-F0021 — upgrade

**Emplacement exact :** `migrations/versions/82deda84bc35_remove_legacy_comment_reports_counter.py` ; déclaration ligne 21, def/lambda ligne 21, fin AST ligne 23. **Module :** `MAH-M004`.

**SHA-256 du fichier source :** `cf71878fee265fe5df8522011a20e6435d60a7453757d9c406e60994603f68f2`. Empreinte AST de la fonction disponible dans CORRESPONDANCE_IDS.json.

**Signature des arguments dans la source :** `()`. **Décorateurs :** aucun.

### Objectif général

Appliquer la transition vers 82deda84bc35 : Supprimer le compteur redondant de signalements.

### Paramètres, types et contexte

Aucun argument explicite. op est la façade Alembic du contexte courant ; op.get_bind() fournit la connexion quand le corps en a besoin. Le schéma doit être à la révision attendue et la destination temporaire autorisée.

### Déroulement étape par étape

1. Ouvrir un batch_alter_table sur comments.
2. Supprimer la seule colonne reports ; ne pas supprimer la table reports et ne pas toucher à comments.likes.

### Valeur de retour

None en fin normale ; les résultats sont les changements de schéma/données et l’état du contexte Alembic, pas une nouvelle liste d’objets ORM.

### Interactions avec les autres composants

Module MAH-M004 ; SQLAlchemy Core et Alembic, sans création d’instances des modèles courants. Les contraintes citent les tables parentes décrites dans le guide des relations.

### Effets sur la base et sur les objets

Upgrade perd les anciennes valeurs du compteur. Les lignes de la table reports restent présentes. Downgrade remplit le compteur recréé à zéro pour les lignes existantes, puis retire le défaut : il ne récupère ni les anciens nombres ni un COUNT des signalements actuels. Un ancien programme lisant ce compteur pourra donc observer zéro même si des signalements existent. Le détail upgrade est explicité ci-dessus ; aucun de ces effets n’a été produit dans ce lot.

### Exceptions, limites et risques

**Rectification pédagogique ciblée :** le contrat gelé 6H.21.1 de MAH-F0022 évoque un recalcul à partir des lignes. Le corps source n’en comporte aucun. Le présent guide et le répertoire donnent le comportement exact sans modifier le document historique ni sa numérotation. Un downgrade n’est donc pas une restauration fonctionnelle garantie de l’ancien compteur.  Erreurs de DDL, réflexion, contrainte, droits ou connexion déléguées possibles. Sur MySQL, un échec tardif peut suivre des DDL déjà commités.

### Exemple concret d’utilisation à expliquer

Exemple de lecture, sans commande à lancer : distinguer la colonne comments.reports retirée de la table reports conservée.

### Repère prévu pour le lot 6H.21.6

Chemin proposé, non créé : `docs/soutenance/code-commente-mahamadou/migrations/versions/82deda84bc35_remove_legacy_comment_reports_counter.py`. Même identifiant `MAH-F0021` ; plage locale future `L0001` à `L0003` pour cette déclaration, blancs inclus. Formule : ligne locale = ligne source − 21 + 1. Ce calcul situe le futur commentaire ; aucune copie ligne par ligne n’est produite ici.

<a id="mah-f0022"></a>

## MAH-F0022 — downgrade

**Emplacement exact :** `migrations/versions/82deda84bc35_remove_legacy_comment_reports_counter.py` ; déclaration ligne 28, def/lambda ligne 28, fin AST ligne 43. **Module :** `MAH-M004`.

**SHA-256 du fichier source :** `cf71878fee265fe5df8522011a20e6435d60a7453757d9c406e60994603f68f2`. Empreinte AST de la fonction disponible dans CORRESPONDANCE_IDS.json.

**Signature des arguments dans la source :** `()`. **Décorateurs :** aucun.

### Objectif général

Revenir au schéma parent de 82deda84bc35 : Supprimer le compteur redondant de signalements.

### Paramètres, types et contexte

Aucun argument explicite. op est la façade Alembic du contexte courant ; op.get_bind() fournit la connexion quand le corps en a besoin. Le schéma doit être à la révision attendue et la destination temporaire autorisée.

### Déroulement étape par étape

1. Ouvrir un premier batch sur comments et rajouter reports Integer NOT NULL avec server_default="0".
2. Ouvrir un second batch et retirer ce défaut SQL. Il n’y a ni SELECT des signalements, ni UPDATE de recalcul du compteur.

### Valeur de retour

None en fin normale ; les résultats sont les changements de schéma/données et l’état du contexte Alembic, pas une nouvelle liste d’objets ORM.

### Interactions avec les autres composants

Module MAH-M004 ; SQLAlchemy Core et Alembic, sans création d’instances des modèles courants. Les contraintes citent les tables parentes décrites dans le guide des relations.

### Effets sur la base et sur les objets

Upgrade perd les anciennes valeurs du compteur. Les lignes de la table reports restent présentes. Downgrade remplit le compteur recréé à zéro pour les lignes existantes, puis retire le défaut : il ne récupère ni les anciens nombres ni un COUNT des signalements actuels. Un ancien programme lisant ce compteur pourra donc observer zéro même si des signalements existent. Le détail downgrade est explicité ci-dessus ; aucun de ces effets n’a été produit dans ce lot.

### Exceptions, limites et risques

**Rectification pédagogique ciblée :** le contrat gelé 6H.21.1 de MAH-F0022 évoque un recalcul à partir des lignes. Le corps source n’en comporte aucun. Le présent guide et le répertoire donnent le comportement exact sans modifier le document historique ni sa numérotation. Un downgrade n’est donc pas une restauration fonctionnelle garantie de l’ancien compteur.  Erreurs de DDL, réflexion, contrainte, droits ou connexion déléguées possibles. Sur MySQL, un échec tardif peut suivre des DDL déjà commités.

### Exemple concret d’utilisation à expliquer

Exemple de lecture, sans commande à lancer : trois signalements présents ne donnent pas un compteur trois : la colonne recréée vaut zéro.

### Repère prévu pour le lot 6H.21.6

Chemin proposé, non créé : `docs/soutenance/code-commente-mahamadou/migrations/versions/82deda84bc35_remove_legacy_comment_reports_counter.py`. Même identifiant `MAH-F0022` ; plage locale future `L0001` à `L0016` pour cette déclaration, blancs inclus. Formule : ligne locale = ligne source − 28 + 1. Ce calcul situe le futur commentaire ; aucune copie ligne par ligne n’est produite ici.

<a id="mah-f0023"></a>

## MAH-F0023 — upgrade

**Emplacement exact :** `migrations/versions/921687c1bd7c_baseline_schema.py` ; déclaration ligne 22, def/lambda ligne 22, fin AST ligne 170. **Module :** `MAH-M005`.

**SHA-256 du fichier source :** `01857725fedc755384192dfb9fb13657415e70af5bdda75ea55026bda5368cfd`. Empreinte AST de la fonction disponible dans CORRESPONDANCE_IDS.json.

**Signature des arguments dans la source :** `()`. **Décorateurs :** aucun.

### Objectif général

Appliquer la transition vers 921687c1bd7c : Établir le schéma historique initial.

### Paramètres, types et contexte

Aucun argument explicite. op est la façade Alembic du contexte courant ; op.get_bind() fournit la connexion quand le corps en a besoin. Le schéma doit être à la révision attendue et la destination temporaire autorisée.

### Déroulement étape par étape

1. Créer users : id Integer PK, username String(100) UNIQUE obligatoire, email String(150) UNIQUE obligatoire, password_hash String(255) obligatoire, is_admin Boolean obligatoire et created_at DateTime obligatoire. is_banned est absent.
2. Créer categories : id Integer PK, name String(100) UNIQUE obligatoire et description Text nullable.
3. Créer stories : id PK, slug String(150) UNIQUE, title String(200), summary et content Text, image_url String(500) nullable, category_id et author_id obligatoires, created_at et updated_at DateTime obligatoires. Nommer les deux FK stories_ibfk_1 et stories_ibfk_2, sans ON DELETE explicite. archived_at et management_revision sont absents.
4. Créer theories : id PK, story_id obligatoire, user_id nullable, title String(200), content Text, likes Integer et created_at DateTime obligatoires ; deux FK nommées theories_ibfk_1/2 sans ON DELETE explicite.
5. Créer comments : id PK, story_id obligatoire, user_id et username String(100) nullables, text Text, likes Integer, reports Integer et created_at obligatoires ; FK comments_ibfk_1/2 sans ON DELETE explicite.
6. Créer votes : id PK, story_id et user_id obligatoires, created_at DateTime obligatoire, FK votes_ibfk_1/2 sans ON DELETE explicite ; contrainte unique_user_story_vote sur user_id/story_id.
7. Créer proposals : id PK, user_id obligatoire, title String(200), content Text, status String(20), created_at et updated_at DateTime obligatoires ; FK proposals_ibfk_1 sans ON DELETE explicite.

### Valeur de retour

None en fin normale ; les résultats sont les changements de schéma/données et l’état du contexte Alembic, pas une nouvelle liste d’objets ORM.

### Interactions avec les autres composants

Module MAH-M005 ; SQLAlchemy Core et Alembic, sans création d’instances des modèles courants. Les contraintes citent les tables parentes décrites dans le guide des relations.

### Effets sur la base et sur les objets

Upgrade ne crée aucun compte, récit, catégorie ou jeu de démonstration. Les colonnes obligatoires n’ont pas les callbacks Python du modèle dans ce DDL : un INSERT SQL direct doit fournir les valeurs nécessaires, dont dates, booléens et compteurs. Downgrade détruit toutes les lignes de ces sept tables ; il ne produit aucune sauvegarde. Le détail upgrade est explicité ci-dessus ; aucun de ces effets n’a été produit dans ce lot.

### Exceptions, limites et risques

Une racine n’est pas une migration idempotente « create if not exists ». Si des tables homonymes existent déjà, l’opération peut échouer ou ne pas correspondre à l’historique attendu. Le downgrade total est destructif et n’est pas une manière de réinitialiser la démonstration persistante.  Erreurs de DDL, réflexion, contrainte, droits ou connexion déléguées possibles. Sur MySQL, un échec tardif peut suivre des DDL déjà commités.

### Exemple concret d’utilisation à expliquer

Exemple de lecture, sans commande à lancer : partir d’un schéma vide de fixture pour comprendre les sept CREATE TABLE, sans récits ajoutés.

### Repère prévu pour le lot 6H.21.6

Chemin proposé, non créé : `docs/soutenance/code-commente-mahamadou/migrations/versions/921687c1bd7c_baseline_schema.py`. Même identifiant `MAH-F0023` ; plage locale future `L0001` à `L0149` pour cette déclaration, blancs inclus. Formule : ligne locale = ligne source − 22 + 1. Ce calcul situe le futur commentaire ; aucune copie ligne par ligne n’est produite ici.

<a id="mah-f0024"></a>

## MAH-F0024 — downgrade

**Emplacement exact :** `migrations/versions/921687c1bd7c_baseline_schema.py` ; déclaration ligne 175, def/lambda ligne 175, fin AST ligne 182. **Module :** `MAH-M005`.

**SHA-256 du fichier source :** `01857725fedc755384192dfb9fb13657415e70af5bdda75ea55026bda5368cfd`. Empreinte AST de la fonction disponible dans CORRESPONDANCE_IDS.json.

**Signature des arguments dans la source :** `()`. **Décorateurs :** aucun.

### Objectif général

Revenir au schéma parent de 921687c1bd7c : Établir le schéma historique initial.

### Paramètres, types et contexte

Aucun argument explicite. op est la façade Alembic du contexte courant ; op.get_bind() fournit la connexion quand le corps en a besoin. Le schéma doit être à la révision attendue et la destination temporaire autorisée.

### Déroulement étape par étape

1. Supprimer proposals, puis votes, comments et theories.
2. Supprimer stories avant categories et users, afin de retirer d’abord les dépendances prévues par cette révision.

### Valeur de retour

None en fin normale ; les résultats sont les changements de schéma/données et l’état du contexte Alembic, pas une nouvelle liste d’objets ORM.

### Interactions avec les autres composants

Module MAH-M005 ; SQLAlchemy Core et Alembic, sans création d’instances des modèles courants. Les contraintes citent les tables parentes décrites dans le guide des relations.

### Effets sur la base et sur les objets

Upgrade ne crée aucun compte, récit, catégorie ou jeu de démonstration. Les colonnes obligatoires n’ont pas les callbacks Python du modèle dans ce DDL : un INSERT SQL direct doit fournir les valeurs nécessaires, dont dates, booléens et compteurs. Downgrade détruit toutes les lignes de ces sept tables ; il ne produit aucune sauvegarde. Le détail downgrade est explicité ci-dessus ; aucun de ces effets n’a été produit dans ce lot.

### Exceptions, limites et risques

Une racine n’est pas une migration idempotente « create if not exists ». Si des tables homonymes existent déjà, l’opération peut échouer ou ne pas correspondre à l’historique attendu. Le downgrade total est destructif et n’est pas une manière de réinitialiser la démonstration persistante.  Erreurs de DDL, réflexion, contrainte, droits ou connexion déléguées possibles. Sur MySQL, un échec tardif peut suivre des DDL déjà commités.

### Exemple concret d’utilisation à expliquer

Exemple de lecture, sans commande à lancer : le retour avant la racine retire les sept tables et leurs lignes, sans archive de restauration.

### Repère prévu pour le lot 6H.21.6

Chemin proposé, non créé : `docs/soutenance/code-commente-mahamadou/migrations/versions/921687c1bd7c_baseline_schema.py`. Même identifiant `MAH-F0024` ; plage locale future `L0001` à `L0008` pour cette déclaration, blancs inclus. Formule : ligne locale = ligne source − 175 + 1. Ce calcul situe le futur commentaire ; aucune copie ligne par ligne n’est produite ici.

<a id="mah-f0025"></a>

## MAH-F0025 — upgrade

**Emplacement exact :** `migrations/versions/a590c8aac613_add_reports_bans_and_cold_case_updates.py` ; déclaration ligne 21, def/lambda ligne 21, fin AST ligne 71. **Module :** `MAH-M006`.

**SHA-256 du fichier source :** `1bb63614fa359fe64a851590aeee6d81b4d48b32891ff8c56416e89f595e117e`. Empreinte AST de la fonction disponible dans CORRESPONDANCE_IDS.json.

**Signature des arguments dans la source :** `()`. **Décorateurs :** aucun.

### Objectif général

Appliquer la transition vers a590c8aac613 : Ajouter signalements, bannissement et mises à jour.

### Paramètres, types et contexte

Aucun argument explicite. op est la façade Alembic du contexte courant ; op.get_bind() fournit la connexion quand le corps en a besoin. Le schéma doit être à la révision attendue et la destination temporaire autorisée.

### Déroulement étape par étape

1. Identifier le dialecte. Si SQLite, refuser avant tout DDL si PRAGMA foreign_keys est actif ou si le marqueur sqlite_migration_integrity_scope est absent. L’appel doit passer par l’enveloppe de maintenance dédiée.
2. Créer reports avec id PK, type String(100), target_id String(100), reason Text, status String(20), created_at DateTime, tous obligatoires. Dans cet état intermédiaire, la cible n’est pas une FK.
3. Créer cold_case_updates : id PK, story_id Integer obligatoire avec fk_cold_case_updates_story CASCADE, content Text et created_at DateTime obligatoires.
4. Ajouter users.is_banned Boolean obligatoire avec server_default=sa.false() pour renseigner les comptes existants.
5. Retirer le défaut SQL temporaire : SQLite passe par batch_alter_table(users) avec existing_type Boolean ; les autres dialectes gardent op.alter_column(users, is_banned, server_default=None).

### Valeur de retour

None en fin normale ; les résultats sont les changements de schéma/données et l’état du contexte Alembic, pas une nouvelle liste d’objets ORM.

### Interactions avec les autres composants

Module MAH-M006 ; SQLAlchemy Core et Alembic, sans création d’instances des modèles courants. Les contraintes citent les tables parentes décrites dans le guide des relations.

### Effets sur la base et sur les objets

Les comptes existants reçoivent false pendant l’ajout de colonne. Le défaut SQL est ensuite retiré ; les insertions ORM ultérieures utilisent le défaut Python de User. La migration ne crée aucun signalement ni mise à jour et n’attribue aucune cible textuelle à un commentaire. Downgrade fait perdre les motifs et textes stockés dans les deux tables ainsi que l’état de bannissement. Le détail upgrade est explicité ci-dessus ; aucun de ces effets n’a été produit dans ce lot.

### Exceptions, limites et risques

L’enveloppe est une condition de fonctionnement en maintenance, pas une frontière de sécurité contre du code arbitraire. Le marqueur connection.info est modifiable en Python. Un accès exclusif doit être réellement organisé pour toute future migration. Aucun essai sur la base persistante n’a lieu pour ce guide. RuntimeError explicite de refus avant DDL possible. Erreurs de DDL, réflexion, contrainte, droits ou connexion déléguées possibles. Sur MySQL, un échec tardif peut suivre des DDL déjà commités.

### Exemple concret d’utilisation à expliquer

Exemple de lecture, sans commande à lancer : observer conceptuellement l’ajout de false aux comptes préexistants puis le retrait du défaut SQL.

### Repère prévu pour le lot 6H.21.6

Chemin proposé, non créé : `docs/soutenance/code-commente-mahamadou/migrations/versions/a590c8aac613_add_reports_bans_and_cold_case_updates.py`. Même identifiant `MAH-F0025` ; plage locale future `L0001` à `L0051` pour cette déclaration, blancs inclus. Formule : ligne locale = ligne source − 21 + 1. Ce calcul situe le futur commentaire ; aucune copie ligne par ligne n’est produite ici.

<a id="mah-f0026"></a>

## MAH-F0026 — downgrade

**Emplacement exact :** `migrations/versions/a590c8aac613_add_reports_bans_and_cold_case_updates.py` ; déclaration ligne 76, def/lambda ligne 76, fin AST ligne 83. **Module :** `MAH-M006`.

**SHA-256 du fichier source :** `1bb63614fa359fe64a851590aeee6d81b4d48b32891ff8c56416e89f595e117e`. Empreinte AST de la fonction disponible dans CORRESPONDANCE_IDS.json.

**Signature des arguments dans la source :** `()`. **Décorateurs :** aucun.

### Objectif général

Revenir au schéma parent de a590c8aac613 : Ajouter signalements, bannissement et mises à jour.

### Paramètres, types et contexte

Aucun argument explicite. op est la façade Alembic du contexte courant ; op.get_bind() fournit la connexion quand le corps en a besoin. Le schéma doit être à la révision attendue et la destination temporaire autorisée.

### Déroulement étape par étape

1. Supprimer cold_case_updates puis reports, avec leurs lignes.
2. Supprimer users.is_banned ; l’information de bannissement est perdue.

### Valeur de retour

None en fin normale ; les résultats sont les changements de schéma/données et l’état du contexte Alembic, pas une nouvelle liste d’objets ORM.

### Interactions avec les autres composants

Module MAH-M006 ; SQLAlchemy Core et Alembic, sans création d’instances des modèles courants. Les contraintes citent les tables parentes décrites dans le guide des relations.

### Effets sur la base et sur les objets

Les comptes existants reçoivent false pendant l’ajout de colonne. Le défaut SQL est ensuite retiré ; les insertions ORM ultérieures utilisent le défaut Python de User. La migration ne crée aucun signalement ni mise à jour et n’attribue aucune cible textuelle à un commentaire. Downgrade fait perdre les motifs et textes stockés dans les deux tables ainsi que l’état de bannissement. Le détail downgrade est explicité ci-dessus ; aucun de ces effets n’a été produit dans ce lot.

### Exceptions, limites et risques

L’enveloppe est une condition de fonctionnement en maintenance, pas une frontière de sécurité contre du code arbitraire. Le marqueur connection.info est modifiable en Python. Un accès exclusif doit être réellement organisé pour toute future migration. Aucun essai sur la base persistante n’a lieu pour ce guide. RuntimeError explicite de refus avant DDL possible. Erreurs de DDL, réflexion, contrainte, droits ou connexion déléguées possibles. Sur MySQL, un échec tardif peut suivre des DDL déjà commités.

### Exemple concret d’utilisation à expliquer

Exemple de lecture, sans commande à lancer : retirer les tables de signalement/mise à jour et perdre leurs données.

### Repère prévu pour le lot 6H.21.6

Chemin proposé, non créé : `docs/soutenance/code-commente-mahamadou/migrations/versions/a590c8aac613_add_reports_bans_and_cold_case_updates.py`. Même identifiant `MAH-F0026` ; plage locale future `L0001` à `L0008` pour cette déclaration, blancs inclus. Formule : ligne locale = ligne source − 76 + 1. Ce calcul situe le futur commentaire ; aucune copie ligne par ligne n’est produite ici.

<a id="mah-f0027"></a>

## MAH-F0027 — upgrade

**Emplacement exact :** `migrations/versions/c6c100000001_add_story_archive_date.py` ; déclaration ligne 16, def/lambda ligne 16, fin AST ligne 19. **Module :** `MAH-M007`.

**SHA-256 du fichier source :** `e10d0486ec2b6970ba95f3ce3141afc433dd2604d554281fb1a33a682f8363a5`. Empreinte AST de la fonction disponible dans CORRESPONDANCE_IDS.json.

**Signature des arguments dans la source :** `()`. **Décorateurs :** aucun.

### Objectif général

Appliquer la transition vers c6c100000001 : Ajouter l’archivage logique des dossiers.

### Paramètres, types et contexte

Aucun argument explicite. op est la façade Alembic du contexte courant ; op.get_bind() fournit la connexion quand le corps en a besoin. Le schéma doit être à la révision attendue et la destination temporaire autorisée.

### Déroulement étape par étape

1. Ajouter stories.archived_at avec sa.DateTime(), nullable=True.
2. Ne définir aucun server_default et ne modifier ni FK, ni enfant, ni compteur. Les lignes existantes ont NULL dans cette nouvelle colonne.

### Valeur de retour

None en fin normale ; les résultats sont les changements de schéma/données et l’état du contexte Alembic, pas une nouvelle liste d’objets ORM.

### Interactions avec les autres composants

Module MAH-M007 ; SQLAlchemy Core et Alembic, sans création d’instances des modèles courants. Les contraintes citent les tables parentes décrites dans le guide des relations.

### Effets sur la base et sur les objets

Après upgrade, les dossiers préexistants sont considérés actifs par le code qui lit NULL comme état actif. L’archive future sera une affectation effectuée par la route de gestion. Downgrade perd les dates d’archive ; l’ancien code peut rendre visibles des dossiers auparavant archivés. Cela implique un risque de visibilité même sans suppression de texte. Le détail upgrade est explicité ci-dessus ; aucun de ces effets n’a été produit dans ce lot.

### Exceptions, limites et risques

Une colonne disponible ne prouve pas que toutes les routes appliquent la visibilité. La classe Story et les vues de story_visibility/admin_stories travaillent ensemble. Cette documentation décrit le code, sans ouvrir le service pour observer son état courant.  Erreurs de DDL, réflexion, contrainte, droits ou connexion déléguées possibles. Sur MySQL, un échec tardif peut suivre des DDL déjà commités.

### Exemple concret d’utilisation à expliquer

Exemple de lecture, sans commande à lancer : un dossier préexistant reçoit archived_at NULL et reste actif.

### Repère prévu pour le lot 6H.21.6

Chemin proposé, non créé : `docs/soutenance/code-commente-mahamadou/migrations/versions/c6c100000001_add_story_archive_date.py`. Même identifiant `MAH-F0027` ; plage locale future `L0001` à `L0004` pour cette déclaration, blancs inclus. Formule : ligne locale = ligne source − 16 + 1. Ce calcul situe le futur commentaire ; aucune copie ligne par ligne n’est produite ici.

<a id="mah-f0028"></a>

## MAH-F0028 — downgrade

**Emplacement exact :** `migrations/versions/c6c100000001_add_story_archive_date.py` ; déclaration ligne 22, def/lambda ligne 22, fin AST ligne 25. **Module :** `MAH-M007`.

**SHA-256 du fichier source :** `e10d0486ec2b6970ba95f3ce3141afc433dd2604d554281fb1a33a682f8363a5`. Empreinte AST de la fonction disponible dans CORRESPONDANCE_IDS.json.

**Signature des arguments dans la source :** `()`. **Décorateurs :** aucun.

### Objectif général

Revenir au schéma parent de c6c100000001 : Ajouter l’archivage logique des dossiers.

### Paramètres, types et contexte

Aucun argument explicite. op est la façade Alembic du contexte courant ; op.get_bind() fournit la connexion quand le corps en a besoin. Le schéma doit être à la révision attendue et la destination temporaire autorisée.

### Déroulement étape par étape

1. Supprimer stories.archived_at.
2. Ne pas supprimer les histoires ; constater que l’information permettant de distinguer les archives disparaît.

### Valeur de retour

None en fin normale ; les résultats sont les changements de schéma/données et l’état du contexte Alembic, pas une nouvelle liste d’objets ORM.

### Interactions avec les autres composants

Module MAH-M007 ; SQLAlchemy Core et Alembic, sans création d’instances des modèles courants. Les contraintes citent les tables parentes décrites dans le guide des relations.

### Effets sur la base et sur les objets

Après upgrade, les dossiers préexistants sont considérés actifs par le code qui lit NULL comme état actif. L’archive future sera une affectation effectuée par la route de gestion. Downgrade perd les dates d’archive ; l’ancien code peut rendre visibles des dossiers auparavant archivés. Cela implique un risque de visibilité même sans suppression de texte. Le détail downgrade est explicité ci-dessus ; aucun de ces effets n’a été produit dans ce lot.

### Exceptions, limites et risques

Une colonne disponible ne prouve pas que toutes les routes appliquent la visibilité. La classe Story et les vues de story_visibility/admin_stories travaillent ensemble. Cette documentation décrit le code, sans ouvrir le service pour observer son état courant.  Erreurs de DDL, réflexion, contrainte, droits ou connexion déléguées possibles. Sur MySQL, un échec tardif peut suivre des DDL déjà commités.

### Exemple concret d’utilisation à expliquer

Exemple de lecture, sans commande à lancer : une date d’archive est perdue et l’ancien code peut réafficher le dossier.

### Repère prévu pour le lot 6H.21.6

Chemin proposé, non créé : `docs/soutenance/code-commente-mahamadou/migrations/versions/c6c100000001_add_story_archive_date.py`. Même identifiant `MAH-F0028` ; plage locale future `L0001` à `L0004` pour cette déclaration, blancs inclus. Formule : ligne locale = ligne source − 22 + 1. Ce calcul situe le futur commentaire ; aucune copie ligne par ligne n’est produite ici.

<a id="mah-f0029"></a>

## MAH-F0029 — inspect_legacy

**Emplacement exact :** `migrations/versions/c6c200000001_comment_reports_and_story_revision.py` ; déclaration ligne 19, def/lambda ligne 19, fin AST ligne 39. **Module :** `MAH-M008`.

**SHA-256 du fichier source :** `e7a4237c0213db41236a0685ace4b9453868c5e038f8804f488ce9bf01a2668f`. Empreinte AST de la fonction disponible dans CORRESPONDANCE_IDS.json.

**Signature des arguments dans la source :** `(bind)`. **Décorateurs :** aucun.

### Objectif général

Valider sans DDL les anciennes cibles de signalements avant conversion.

### Paramètres, types et contexte

bind : Connection SQLAlchemy déjà choisie par Alembic, sur la révision parente c6c100000001. Aucun type source annoté.

### Déroulement étape par étape

1. Inspecter comments.id et exiger un type sa.Integer ou dérivé.
2. Refléter reports et comments ; charger les lignes id/type/target_id de reports et l’ensemble des PK de comments.
3. Vérifier chaque type "comment", cible str conforme à [1-9][0-9]{0,9}, borne <=2147483647 et présence de l’entier dans les parents.
4. Lever un RuntimeError neutre au premier cas incompatible ; sinon construire les dictionnaires de correspondance.
5. Renvoyer une copie du type parent et la liste des correspondances.

### Valeur de retour

tuple à deux éléments : (copie du type SQL, list[dict] de {report_id, comment_id}). Ce n’est pas seulement le type de clé.

### Interactions avec les autres composants

MAH-F0030 utilise les deux résultats pour ajouter la colonne de bon type puis remplir ses valeurs.

### Effets sur la base et sur les objets

Requêtes d’inspection et SELECT sur la connexion ; aucun DDL ni UPDATE dans cette fonction. Charge les lignes et identifiants en mémoire.

### Exceptions, limites et risques

RuntimeError pour type ou cible incompatible, erreurs de réflexion/connexion et StopIteration possible si la colonne attendue manque. Les messages explicites ne recopient ni motif ni cible historique. Une lecture préalable ne protège pas d’un écrivain concurrent.

### Exemple concret d’utilisation à expliquer

Pour un ancien signalement fictif de type comment et target_id="23", présent dans la fixture, mapped contient {"report_id": id_fictif, "comment_id": 23}. La même cible "023" est refusée avant le DDL.

### Repère prévu pour le lot 6H.21.6

Chemin proposé, non créé : `docs/soutenance/code-commente-mahamadou/migrations/versions/c6c200000001_comment_reports_and_story_revision.py`. Même identifiant `MAH-F0029` ; plage locale future `L0001` à `L0021` pour cette déclaration, blancs inclus. Formule : ligne locale = ligne source − 19 + 1. Ce calcul situe le futur commentaire ; aucune copie ligne par ligne n’est produite ici.

<a id="mah-f0030"></a>

## MAH-F0030 — upgrade

**Emplacement exact :** `migrations/versions/c6c200000001_comment_reports_and_story_revision.py` ; déclaration ligne 42, def/lambda ligne 42, fin AST ligne 62. **Module :** `MAH-M008`.

**SHA-256 du fichier source :** `e7a4237c0213db41236a0685ace4b9453868c5e038f8804f488ce9bf01a2668f`. Empreinte AST de la fonction disponible dans CORRESPONDANCE_IDS.json.

**Signature des arguments dans la source :** `()`. **Décorateurs :** aucun.

### Objectif général

Appliquer la transition vers c6c200000001 : Rendre les signalements référentiels et réviser la gestion.

### Paramètres, types et contexte

Aucun argument explicite. op est la façade Alembic du contexte courant ; op.get_bind() fournit la connexion quand le corps en a besoin. Le schéma doit être à la révision attendue et la destination temporaire autorisée.

### Déroulement étape par étape

1. Appeler inspect_legacy(bind), MAH-F0029, avant le premier DDL : vérifier le type entier de comments.id, charger les anciens reports et les identifiants de commentaires ; accepter seulement type="comment" et une cible chaîne ASCII canonique [1-9][0-9]{0,9}, <=2147483647, existante.
2. Recevoir un tuple (copie du type de PK, liste de correspondances report_id/comment_id). Ajouter reports.comment_id avec ce type, d’abord nullable pour permettre le remplissage.
3. Mettre à jour chaque ligne de reports à partir de la correspondance validée, sans copier son motif dans un message d’erreur.
4. Dans le batch reports : rendre comment_id obligatoire, créer fk_reports_comment CASCADE, supprimer type et target_id, créer l’index non unique ix_reports_comment_id.
5. Ajouter stories.management_revision String(32) NOT NULL avec server_default égal à 32 zéros ; puis attribuer un uuid4().hex distinct généré à chaque dossier existant.
6. Créer uq_stories_management_revision comme index UNIQUE. Le défaut SQL sentinelle reste dans le schéma ; l’ORM génère ensuite ses propres UUID pour ses INSERT.

### Valeur de retour

None en fin normale ; les résultats sont les changements de schéma/données et l’état du contexte Alembic, pas une nouvelle liste d’objets ORM.

### Interactions avec les autres composants

Module MAH-M008 ; SQLAlchemy Core et Alembic, sans création d’instances des modèles courants. inspect_legacy est appelé dans upgrade avant tout DDL.

### Effets sur la base et sur les objets

Les ids de signalement, motifs, statuts et dates sont conservés dans le chemin valide ; les anciennes cibles invalides provoquent un refus, pas une suppression silencieuse de signalements. Le nouveau lien rend les DELETE de commentaires cascades sur les signalements. Downgrade produit le format générique à partir des seules références actuelles ; il ne ressuscite aucune cible ou ligne supprimée auparavant. Les valeurs de révision de gestion sont perdues au retour. Le détail upgrade est explicité ci-dessus ; aucun de ces effets n’a été produit dans ce lot.

### Exceptions, limites et risques

L’inspection charge les signalements et ids parents en mémoire : coût linéaire dans leur volume, pas une reprise paginée. Une collision UUID très improbable peut faire échouer l’unicité ; la sentinelle future n’est pas une vraie révision acceptable pour la purge. Un schéma partiellement modifié après erreur MySQL exigerait une analyse spécifique ; ne pas proposer de réexécution aveugle. Aucune de ces procédures n’est lancée ici. RuntimeError explicite de refus avant DDL possible. Erreurs de DDL, réflexion, contrainte, droits ou connexion déléguées possibles. Sur MySQL, un échec tardif peut suivre des DDL déjà commités.

### Exemple concret d’utilisation à expliquer

Exemple de lecture, sans commande à lancer : transformer une cible fictive "23" validée vers comment_id=23, puis générer les révisions de gestion.

### Repère prévu pour le lot 6H.21.6

Chemin proposé, non créé : `docs/soutenance/code-commente-mahamadou/migrations/versions/c6c200000001_comment_reports_and_story_revision.py`. Même identifiant `MAH-F0030` ; plage locale future `L0001` à `L0021` pour cette déclaration, blancs inclus. Formule : ligne locale = ligne source − 42 + 1. Ce calcul situe le futur commentaire ; aucune copie ligne par ligne n’est produite ici.

<a id="mah-f0031"></a>

## MAH-F0031 — downgrade

**Emplacement exact :** `migrations/versions/c6c200000001_comment_reports_and_story_revision.py` ; déclaration ligne 65, def/lambda ligne 65, fin AST ligne 80. **Module :** `MAH-M008`.

**SHA-256 du fichier source :** `e7a4237c0213db41236a0685ace4b9453868c5e038f8804f488ce9bf01a2668f`. Empreinte AST de la fonction disponible dans CORRESPONDANCE_IDS.json.

**Signature des arguments dans la source :** `()`. **Décorateurs :** aucun.

### Objectif général

Revenir au schéma parent de c6c200000001 : Rendre les signalements référentiels et réviser la gestion.

### Paramètres, types et contexte

Aucun argument explicite. op est la façade Alembic du contexte courant ; op.get_bind() fournit la connexion quand le corps en a besoin. Le schéma doit être à la révision attendue et la destination temporaire autorisée.

### Déroulement étape par étape

1. Ajouter reports.type et reports.target_id String(100), temporairement nullables.
2. Parcourir les signalements actuels : écrire type="comment" et target_id=str(comment_id).
3. En batch : supprimer fk_reports_comment et ix_reports_comment_id, rendre les deux colonnes textuelles obligatoires, supprimer comment_id.
4. Supprimer l’index unique uq_stories_management_revision puis la colonne stories.management_revision.

### Valeur de retour

None en fin normale ; les résultats sont les changements de schéma/données et l’état du contexte Alembic, pas une nouvelle liste d’objets ORM.

### Interactions avec les autres composants

Module MAH-M008 ; SQLAlchemy Core et Alembic, sans création d’instances des modèles courants. Les contraintes citent les tables parentes décrites dans le guide des relations.

### Effets sur la base et sur les objets

Les ids de signalement, motifs, statuts et dates sont conservés dans le chemin valide ; les anciennes cibles invalides provoquent un refus, pas une suppression silencieuse de signalements. Le nouveau lien rend les DELETE de commentaires cascades sur les signalements. Downgrade produit le format générique à partir des seules références actuelles ; il ne ressuscite aucune cible ou ligne supprimée auparavant. Les valeurs de révision de gestion sont perdues au retour. Le détail downgrade est explicité ci-dessus ; aucun de ces effets n’a été produit dans ce lot.

### Exceptions, limites et risques

L’inspection charge les signalements et ids parents en mémoire : coût linéaire dans leur volume, pas une reprise paginée. Une collision UUID très improbable peut faire échouer l’unicité ; la sentinelle future n’est pas une vraie révision acceptable pour la purge. Un schéma partiellement modifié après erreur MySQL exigerait une analyse spécifique ; ne pas proposer de réexécution aveugle. Aucune de ces procédures n’est lancée ici. RuntimeError explicite de refus avant DDL possible. Erreurs de DDL, réflexion, contrainte, droits ou connexion déléguées possibles. Sur MySQL, un échec tardif peut suivre des DDL déjà commités.

### Exemple concret d’utilisation à expliquer

Exemple de lecture, sans commande à lancer : la FK actuelle 23 devient target_id="23" et type="comment" ; les révisions sont retirées.

### Repère prévu pour le lot 6H.21.6

Chemin proposé, non créé : `docs/soutenance/code-commente-mahamadou/migrations/versions/c6c200000001_comment_reports_and_story_revision.py`. Même identifiant `MAH-F0031` ; plage locale future `L0001` à `L0016` pour cette déclaration, blancs inclus. Formule : ligne locale = ligne source − 65 + 1. Ce calcul situe le futur commentaire ; aucune copie ligne par ligne n’est produite ici.

<a id="mah-f0032"></a>

## MAH-F0032 — inspect_legacy

**Emplacement exact :** `migrations/versions/c6g200000001_add_comment_likes.py` ; déclaration ligne 15, def/lambda ligne 15, fin AST ligne 45. **Module :** `MAH-M009`.

**SHA-256 du fichier source :** `2be972ed42b9b95f141378916705e35c2dfe2d77bd70ca4d4a49295d2ea9d2de`. Empreinte AST de la fonction disponible dans CORRESPONDANCE_IDS.json.

**Signature des arguments dans la source :** `(bind)`. **Décorateurs :** aucun.

### Objectif général

Refuser les conditions d’intégrité ou historiques incompatibles avant création de comment_likes.

### Paramètres, types et contexte

bind : Connection SQLAlchemy du contexte Alembic, sur c6c200000001. Types des paramètres non annotés dans la source.

### Déroulement étape par étape

1. Si SQLite avec FK inactives, exiger le marqueur de scope et un foreign_key_check vide.
2. Créer l’inspecteur ; si MySQL, exiger @@foreign_key_checks=1 et comments/users en InnoDB.
3. Refuser une table comment_likes déjà présente.
4. Inspecter comments.id et users.id, exiger sa.Integer, copier leurs types dans une liste.
5. Refléter comments et lire likes sans cast ; pour chaque valeur exiger type(value) is int et value == 0.
6. Renvoyer la liste des deux types SQL copiés, dans l’ordre commentaire puis compte.

### Valeur de retour

list de deux objets de type SQL ; upgrade les déballe en comment_type, user_type. La description générique de « couple » dans le référentiel ne doit pas être lue comme une construction tuple effective.

### Interactions avec les autres composants

MAH-F0033 utilise les types et crée les associations ; l’API legacy_likes_compatible applique elle aussi un contrôle strict du compteur pour le nouveau parcours de like.

### Effets sur la base et sur les objets

Inspections et SELECT ; aucun CREATE, UPDATE ou remise à zéro. Ce contrôle ne touche pas aux votes.

### Exceptions, limites et risques

RuntimeError pour FK inactives non encadrées, moteur parent non InnoDB sur MySQL, table existante, type parent incompatible, compteur non exactement entier zéro. Erreurs de pilote, réflexion ou colonne manquante possibles en plus.

### Exemple concret d’utilisation à expliquer

Une fixture dont tous les compteurs sont l’entier 0 peut passer cette précondition. Un seul 5, -1 ou texte provoque un refus : le script ne choisit pas d’auteurs pour l’ancien compteur.

### Repère prévu pour le lot 6H.21.6

Chemin proposé, non créé : `docs/soutenance/code-commente-mahamadou/migrations/versions/c6g200000001_add_comment_likes.py`. Même identifiant `MAH-F0032` ; plage locale future `L0001` à `L0031` pour cette déclaration, blancs inclus. Formule : ligne locale = ligne source − 15 + 1. Ce calcul situe le futur commentaire ; aucune copie ligne par ligne n’est produite ici.

<a id="mah-f0033"></a>

## MAH-F0033 — upgrade

**Emplacement exact :** `migrations/versions/c6g200000001_add_comment_likes.py` ; déclaration ligne 48, def/lambda ligne 48, fin AST ligne 61. **Module :** `MAH-M009`.

**SHA-256 du fichier source :** `2be972ed42b9b95f141378916705e35c2dfe2d77bd70ca4d4a49295d2ea9d2de`. Empreinte AST de la fonction disponible dans CORRESPONDANCE_IDS.json.

**Signature des arguments dans la source :** `()`. **Décorateurs :** aucun.

### Objectif général

Appliquer la transition vers c6g200000001 : Introduire les likes de commentaires attribuables.

### Paramètres, types et contexte

Aucun argument explicite. op est la façade Alembic du contexte courant ; op.get_bind() fournit la connexion quand le corps en a besoin. Le schéma doit être à la révision attendue et la destination temporaire autorisée.

### Déroulement étape par étape

1. Appeler inspect_legacy(bind), MAH-F0032, avant DDL. SQLite exige les FK actives, ou l’enveloppe identifiée avec foreign_key_check vide. MySQL exige foreign_key_checks=1 et les parents comments/users en InnoDB.
2. Refuser si comment_likes existe déjà ; inspecter comments.id et users.id et exiger un type dérivé de sa.Integer. Copier ces deux types dans une liste renvoyée à upgrade.
3. Lire chaque comments.likes sans cast. Exiger type(value) is int et value==0 : zéro flottant, booléen Python, texte, NULL, négatif ou positif ne passent pas ce test tel qu’écrit.
4. Créer comment_likes : id Integer PK, comment_id et user_id obligatoires avec les types parents copiés, created_at DateTime obligatoire ; deux FK CASCADE nommées fk_comment_likes_comment et fk_comment_likes_user ; unique_user_comment_like sur user_id/comment_id ; mysql_engine="InnoDB".
5. Créer ix_comment_likes_comment_id non unique. Ne faire aucun UPDATE du compteur physique et ne transférer aucun Vote.

### Valeur de retour

None en fin normale ; les résultats sont les changements de schéma/données et l’état du contexte Alembic, pas une nouvelle liste d’objets ORM.

### Interactions avec les autres composants

Module MAH-M009 ; SQLAlchemy Core et Alembic, sans création d’instances des modèles courants. inspect_legacy est appelé dans upgrade avant tout DDL.

### Effets sur la base et sur les objets

La table nouvelle démarre vide. Aucun ancien like n’est affecté à un utilisateur arbitraire, aucun compteur n’est remis à zéro par ce script. Une donnée historique non attribuable exige une décision humaine de reprise hors de ce lot. Le garde de downgrade évite la suppression silencieuse d’une table remplie, mais n’est pas une sauvegarde et ne protège pas contre un écrivain concurrent sans maintenance exclusive. Le détail upgrade est explicité ci-dessus ; aucun de ces effets n’a été produit dans ce lot.

### Exceptions, limites et risques

Cette migration n’est pas idempotente quand la table existe déjà. Le refus d’un ancien compteur non nul est volontaire et ne doit pas être « réparé » en effaçant l’information pour obtenir un succès. Les anciens écrivains doivent être exclus pendant le contrôle et le DDL ; les gardes Python ne sont pas une isolation système. RuntimeError explicite de refus avant DDL possible. Erreurs de DDL, réflexion, contrainte, droits ou connexion déléguées possibles. Sur MySQL, un échec tardif peut suivre des DDL déjà commités.

### Exemple concret d’utilisation à expliquer

Exemple de lecture, sans commande à lancer : avec des compteurs historiques tous exactement entiers zéro, la table de likes créée démarre vide.

### Repère prévu pour le lot 6H.21.6

Chemin proposé, non créé : `docs/soutenance/code-commente-mahamadou/migrations/versions/c6g200000001_add_comment_likes.py`. Même identifiant `MAH-F0033` ; plage locale future `L0001` à `L0014` pour cette déclaration, blancs inclus. Formule : ligne locale = ligne source − 48 + 1. Ce calcul situe le futur commentaire ; aucune copie ligne par ligne n’est produite ici.

<a id="mah-f0034"></a>

## MAH-F0034 — downgrade

**Emplacement exact :** `migrations/versions/c6g200000001_add_comment_likes.py` ; déclaration ligne 65, def/lambda ligne 65, fin AST ligne 70. **Module :** `MAH-M009`.

**SHA-256 du fichier source :** `2be972ed42b9b95f141378916705e35c2dfe2d77bd70ca4d4a49295d2ea9d2de`. Empreinte AST de la fonction disponible dans CORRESPONDANCE_IDS.json.

**Signature des arguments dans la source :** `()`. **Décorateurs :** aucun.

### Objectif général

Revenir au schéma parent de c6g200000001 : Introduire les likes de commentaires attribuables.

### Paramètres, types et contexte

Aucun argument explicite. op est la façade Alembic du contexte courant ; op.get_bind() fournit la connexion quand le corps en a besoin. Le schéma doit être à la révision attendue et la destination temporaire autorisée.

### Déroulement étape par étape

1. Refléter comment_likes et lire au plus un id.
2. Si une ligne existe, lever RuntimeError afin de refuser la perte de likes individuels ; sinon supprimer l’index puis la table.

### Valeur de retour

None en fin normale ; les résultats sont les changements de schéma/données et l’état du contexte Alembic, pas une nouvelle liste d’objets ORM.

### Interactions avec les autres composants

Module MAH-M009 ; SQLAlchemy Core et Alembic, sans création d’instances des modèles courants. Les contraintes citent les tables parentes décrites dans le guide des relations.

### Effets sur la base et sur les objets

La table nouvelle démarre vide. Aucun ancien like n’est affecté à un utilisateur arbitraire, aucun compteur n’est remis à zéro par ce script. Une donnée historique non attribuable exige une décision humaine de reprise hors de ce lot. Le garde de downgrade évite la suppression silencieuse d’une table remplie, mais n’est pas une sauvegarde et ne protège pas contre un écrivain concurrent sans maintenance exclusive. Le détail downgrade est explicité ci-dessus ; aucun de ces effets n’a été produit dans ce lot.

### Exceptions, limites et risques

Cette migration n’est pas idempotente quand la table existe déjà. Le refus d’un ancien compteur non nul est volontaire et ne doit pas être « réparé » en effaçant l’information pour obtenir un succès. Les anciens écrivains doivent être exclus pendant le contrôle et le DDL ; les gardes Python ne sont pas une isolation système. RuntimeError explicite de refus avant DDL possible. Erreurs de DDL, réflexion, contrainte, droits ou connexion déléguées possibles. Sur MySQL, un échec tardif peut suivre des DDL déjà commités.

### Exemple concret d’utilisation à expliquer

Exemple de lecture, sans commande à lancer : une seule ligne CommentLike suffit à provoquer le refus ; une table vide peut être retirée.

### Repère prévu pour le lot 6H.21.6

Chemin proposé, non créé : `docs/soutenance/code-commente-mahamadou/migrations/versions/c6g200000001_add_comment_likes.py`. Même identifiant `MAH-F0034` ; plage locale future `L0001` à `L0006` pour cette déclaration, blancs inclus. Formule : ligne locale = ligne source − 65 + 1. Ce calcul situe le futur commentaire ; aucune copie ligne par ligne n’est produite ici.

<a id="mah-f0213"></a>

## MAH-F0213 — sqlite_migration_scope

**Emplacement exact :** `migrations/sqlite_safety.py` ; déclaration ligne 9, def/lambda ligne 10, fin AST ligne 35. **Module :** `MAH-M028`.

**SHA-256 du fichier source :** `493820897cd07a2f98f8851179a82bfed4aea4df8e8ea7d1bab6adabae63789b`. Empreinte AST de la fonction disponible dans CORRESPONDANCE_IDS.json.

**Signature des arguments dans la source :** `(connection)`. **Décorateurs :** `contextmanager`.

### Objectif général

Encadrer les reconstructions SQLite dans une transaction explicite et contrôler les FK avant/après.

### Paramètres, types et contexte

connection : Connection SQLAlchemy déjà ouverte, dialecte SQLite, sans transaction initiale. Le choix de la destination et l’exclusivité sont à la charge de l’appelant.

### Déroulement étape par étape

1. À l’entrée du with, refuser un autre dialecte et une transaction déjà ouverte.
2. Retrouver la connexion DBAPI ; activer les FK et refuser une anomalie initiale de foreign_key_check.
3. Suspendre les FK hors transaction, contrôler l’état, puis entrer dans connection.begin et émettre BEGIN explicite.
4. Poser le marqueur connection.info de portée, puis yield pour exécuter le corps utilisateur.
5. Après retour normal, contrôler foreign_key_check avant la validation de la transaction ; une anomalie entraîne une exception.
6. Dans finally, retirer le marqueur et réactiver les FK ; vérifier la réactivation et signaler son échec.

### Valeur de retour

L’appel renvoie un gestionnaire de contexte produit par contextmanager ; l’entrée du contexte fournit None via yield. À ne pas confondre avec une fonction ordinaire retournant directement None.

### Interactions avec les autres composants

run_migrations_online et les gardes SQLite de a590/c6g ; couche SQLAlchemy et connexion DBAPI sous-jacente.

### Effets sur la base et sur les objets

PRAGMA, BEGIN et transaction sur la connexion fournie. Le corps du with peut effectuer du DDL/DML. Aucun chemin ni moteur créé par la fonction ; pas d’accès système contrôlant le reste du processus.

### Exceptions, limites et risques

ValueError autre dialecte ; RuntimeError transaction déjà ouverte, intégrité initiale/finale invalide ou commutation FK impossible ; erreurs DBAPI possibles. Le try/finally commence après les contrôles initiaux et la suspension contrôlée ; une connexion cassée peut empêcher la réactivation. L’échec de nettoyage peut masquer la cause initiale.

### Exemple concret d’utilisation à expliquer

Dans une future fixture de migration explicitement autorisée, le raisonnement est « entrer dans le scope de la connexion temporaire, appliquer les étapes revues, vérifier avant de sortir ». Aucun appel réel ni nom de base n’est fourni ici ; la fonction n’est pas un confinement système.

### Repère prévu pour le lot 6H.21.6

Chemin proposé, non créé : `docs/soutenance/code-commente-mahamadou/migrations/sqlite_safety.py`. Même identifiant `MAH-F0213` ; plage locale future `L0001` à `L0027` pour cette déclaration, blancs inclus. Formule : ligne locale = ligne source − 9 + 1. Ce calcul situe le futur commentaire ; aucune copie ligne par ligne n’est produite ici.

## Précisions par rapport au référentiel gelé

MAH-F0022 : downgrade de 82deda recrée un compteur à zéro, sans aucun recalcul à partir de reports. MAH-F0029 : le résultat concret est un tuple du type copié et de la liste de correspondances, pas seulement un type. MAH-F0032 : le résultat concret est une liste de deux types, déballée ensuite, et non un tuple construit explicitement.

Les décalages de lignes dans env.py, a590 et c6g correspondent aux correctifs déjà présents. Ils ne justifient pas de renuméroter les fonctions. Le nouveau helper est expliqué comme complément ; aucun fichier du lot 6H.21.1 n’est réécrit. Les responsabilités pédagogiques de Mahamadou n’affirment pas une propriété exclusive du code partagé.

Pour les opérations DDL, le [guide des migrations](03_GUIDE_SEPT_MIGRATIONS.md) apporte l’état parent, le schéma résultant et les limites par dialecte. Pour les objets et colonnes, utiliser le [guide des modèles](01_GUIDE_DIX_MODELES.md). Les garanties SQL et les transactions sont détaillées dans le [guide des relations](02_RELATIONS_CONTRAINTES_TRANSACTIONS.md).

Le hachage et la comparaison de mots de passe sont délégués aux fonctions prévues par Werkzeug ; les détails de méthode par défaut doivent être lus selon la version réellement utilisée. Aucun algorithme n’est figé par ce guide à partir du seul appel sans option. [Documentation officielle Werkzeug](https://werkzeug.palletsprojects.com/en/stable/utils/#module-werkzeug.security).
