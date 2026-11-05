# Rapport de correspondance documentaire avec les sources

Les Petits Enquêteurs — lot 6H.21.4 — 4 novembre 2026, Europe/Paris.

**Proposition externe à lire et à approuver avant installation.** Sources : copie intégrée locale, photographiée par SHA-256 ; pas la seule version du commit Git. Analyse statique : aucun import de l’application, accès SQL, test applicatif ni migration exécutée pour cette rédaction. Les exemples sont pédagogiques et non exécutés. Leur éventuelle exécution exige un contexte temporaire distinct, préparé et autorisé ; ils ne constituent pas des scripts de démarrage du projet.

[Sommaire de soutenance](README.md) · [Correspondance avec les sources](06_CORRESPONDANCE_SOURCES.md) · [Validation documentaire](07_VALIDATION_DOCUMENTAIRE.md)

## Source exacte et méthode

Le chemin annoncé dans la demande, `C:\Users\diarr\portfolio_integration-main-lot6h22-7`, n’est pas présent. La copie intégrée existante utilisée est **`C:\Users\diarr\portfolio\_integration-main-lot6h22-7`**, qui contient 196 fichiers hors métadonnées Git. Aucun déplacement ni renommage n’a été réalisé. Le dépôt original `feature/frontend-api-integration` reste hors du travail de rédaction.

La copie source a pour HEAD `45170b7d5530c834c561afc1a19f39abf288cb74` et branche `integration-main-6h22-7` au relevé initial. Ce HEAD est la base Git ; il ne décrit pas à lui seul tous les fichiers de travail intégrés. Les empreintes des 196 fichiers de travail sont donc la référence de cette étude, et non une prétendue égalité avec le seul arbre de HEAD. Le contenu de main distant n’est pas réaudité dans ce lot documentaire.

Tous les fichiers Python du périmètre modèles/migrations sont lus intégralement comme texte UTF-8 et parsés avec ast.parse. Aucun module du projet n’est importé. Les imports des scripts de génération ne concernent que les outils documentaires nouvellement écrits sous Temp. Les seules commandes Git sont de lecture, avec GIT_OPTIONAL_LOCKS=0 et une option safe.directory limitée à la commande, sans modification de configuration Git.

Le statut, les références, HEAD et l’empreinte de l’index de chaque dépôt observé sont relevés avant/après. Pour l’original, cela établit la stabilité de ces observations Git ; ce n’est pas une empreinte exhaustive de tous ses fichiers privés ou ignorés. Aucun de ces fichiers privés n’est ouvert pour compléter cette documentation.

## Sources principales et empreintes actuelles

| Module stable | Fichier lu intégralement | SHA-256 des octets actuels | Comparaison avec le référentiel gelé |
|---|---|---|---|
| MAH-M001 | `backend/models.py` | `d9f29a20a5174e7738725fe765bcc4b1270f60de9a6f71ad43c882d5f6cc175d` | Identique |
| MAH-M002 | `migrations/env.py` | `164deb298151eaf27680109c4b54a6819aeb83ef385b57482278a2311e91031c` | Différent : correctif déjà présent |
| MAH-M028 proposé | `migrations/sqlite_safety.py` | `493820897cd07a2f98f8851179a82bfed4aea4df8e8ea7d1bab6adabae63789b` | Module complémentaire absent du gel |
| MAH-M003 | `migrations/versions/3111f5767fc6_ajoute_les_regles_on_delete.py` | `0c03a3067099d4e3b651dbe88575462f383b37095e4407e56b95ea98b4a5aba4` | Identique |
| MAH-M004 | `migrations/versions/82deda84bc35_remove_legacy_comment_reports_counter.py` | `cf71878fee265fe5df8522011a20e6435d60a7453757d9c406e60994603f68f2` | Identique |
| MAH-M005 | `migrations/versions/921687c1bd7c_baseline_schema.py` | `01857725fedc755384192dfb9fb13657415e70af5bdda75ea55026bda5368cfd` | Identique |
| MAH-M006 | `migrations/versions/a590c8aac613_add_reports_bans_and_cold_case_updates.py` | `1bb63614fa359fe64a851590aeee6d81b4d48b32891ff8c56416e89f595e117e` | Différent : correctif déjà présent |
| MAH-M007 | `migrations/versions/c6c100000001_add_story_archive_date.py` | `e10d0486ec2b6970ba95f3ce3141afc433dd2604d554281fb1a33a682f8363a5` | Identique |
| MAH-M008 | `migrations/versions/c6c200000001_comment_reports_and_story_revision.py` | `e7a4237c0213db41236a0685ace4b9453868c5e038f8804f488ce9bf01a2668f` | Identique |
| MAH-M009 | `migrations/versions/c6g200000001_add_comment_likes.py` | `2be972ed42b9b95f141378916705e35c2dfe2d77bd70ca4d4a49295d2ea9d2de` | Différent : correctif déjà présent |

Les différences attendues avec le gel concernent env.py, a590 et c6g ; le helper sqlite_safety est nouveau. Le document ERRATA_MIGRATIONS_LOT6H22_4.md explique ces corrections antérieures. Leur présence n’est pas une modification appliquée par le lot documentaire actuel. Les empreintes du gel restent conservées, avec leur signification historique.

Les inventaires lisibles par machine sont `INVENTAIRE_ACTUEL.json` (annexe externe conservée avec la sauvegarde), `CORRESPONDANCE_IDS.json` (annexe externe conservée avec la sauvegarde), `CONTRATS_EXPLIQUES.json` (annexe externe conservée avec la sauvegarde) et `EXTENSION_REFERENTIEL_PROPOSEE.json` (annexe externe conservée avec la sauvegarde). Les instantanés SOURCES_AVANT/APRES restent des annexes de preuve locales ; ils ne sont pas inclus dans l’archive des propositions documentaires car ils contiennent aussi des statuts et chemins de travail locaux.

## Couverture de chaque classe

| Identifiant stable | Classe | Plage actuelle du fichier models.py | Colonnes | relationship | Fonctions locales expliquées |
|---|---|---|---:|---:|---:|
| MAH-C001 | `User` | 18–63 | 7 | 6 | 3 |
| MAH-C002 | `Category` | 68–77 | 3 | 1 | 0 |
| MAH-C003 | `Story` | 83–210 | 12 | 6 | 2 |
| MAH-C004 | `Theory` | 215–275 | 7 | 2 | 0 |
| MAH-C005 | `Comment` | 281–371 | 7 | 4 | 1 |
| MAH-C006 | `Vote` | 376–430 | 4 | 2 | 0 |
| MAH-C007 | `CommentLike` | 433–450 | 4 | 2 | 0 |
| MAH-C008 | `Proposal` | 455–507 | 7 | 1 | 0 |
| MAH-C009 | `Report` | 512–581 | 5 | 1 | 5 |
| MAH-C010 | `ColdCaseUpdate` | 586–633 | 4 | 1 | 1 |

Les 60 colonnes ont toutes une ligne dédiée avec type, nullable, contraintes, défaut et explication métier. Les 26 navigations sont décrites, et les 13 FK reçoivent un repère REL-01 à REL-13 dans le guide des relations. Ces repères REL servent seulement à ce lot ; ils ne remplacent aucun identifiant du référentiel gelé.

## Conservation et extension des identifiants

Le rapprochement des fonctions repose sur le chemin de module et le nom qualifié, y compris les marqueurs [lecture]/[ecriture], la fonction imbriquée et l’ordinal de lambda. Les lignes peuvent évoluer sans renumérotation. Les 34 entrées existantes de ce périmètre sont retrouvées de façon unique ; la 35e est le helper complémentaire.

Le gel a 27 modules et 212 fonctions. L’extension externe proposée réserve MAH-M028 à migrations/sqlite_safety.py et MAH-F0213 à sqlite_migration_scope. Elle n’ajoute pas ces entrées dans les fichiers historiques du projet. Une installation future devra décider explicitement de publier le complément plutôt que de réécrire le gel.

La table complète des positions anciennes et actuelles, signatures, décorateurs et empreintes AST est fournie dans CORRESPONDANCE_IDS.json. Une empreinte AST ignore commentaires et positions ; elle peut aider à distinguer un décalage de lignes d’une modification de corps, mais ne constitue pas une preuve d’exécution ou de sécurité.

## Rectifications pédagogiques motivées par les corps sources

| Entrée | Précision nouvelle | Preuve statique |
|---|---|---|
| MAH-F0022 | Le compteur recréé vaut zéro ; aucun recalcul | Deux batch : ajout avec server_default="0", puis retrait du défaut ; aucun SELECT/UPDATE dans downgrade |
| MAH-F0029 | Retour tuple du type copié et de la liste mapped | return column['type'].copy(), mapped |
| MAH-F0032 | Retour d’une liste de deux types | parent_types=[] puis append puis return parent_types |
| MAH-F0213 proposé | Gestionnaire de contexte, valeur fournie None | Décorateur contextmanager, yield sans valeur |

Ces précisions ne sont pas des corrections applicatives. Le référentiel et les textes historiques restent inchangés. Le nouveau guide prime pour l’explication actuelle du comportement étudié, avec les limites de preuve explicites.

## Raccord aux dix-huit questions de Mahamadou

Les formulations ci-dessous sont extraites de la section « A. Question originale » de la fiche actuelle, sans changement de texte. Les compléments sont nouveaux et restent dans ce rapport externe. Ils ne remplacent ni les réponses actuelles ni les réponses historiques archivées de la fiche.

| Question stable et formulation conservée | Complément technique à travailler | Guide |
|---|---|---|
| **MAH-01** — À quoi sert MySQL ? | Le moteur exécute le SQL et impose les contraintes réellement installées. SQLAlchemy est l’interface objet ; Aiven est une cible de service configurée, pas un modèle supplémentaire. | [Lecture ciblée](02_RELATIONS_CONTRAINTES_TRANSACTIONS.md) |
| **MAH-02** — Pourquoi utiliser plusieurs tables ? | Séparer comptes, dossiers et contributions évite de recopier la même identité dans chaque objet ; les FK relient les lignes. Le pseudo de Comment est une copie volontaire distincte de sa FK. | [Lecture ciblée](01_GUIDE_DIX_MODELES.md) |
| **MAH-03** — Qu’est-ce qu’une clé primaire ? | Chaque table a son propre id entier ; l’identité n’est ni le slug, ni un index de position, ni un nombre garanti continu. | [Lecture ciblée](02_RELATIONS_CONTRAINTES_TRANSACTIONS.md) |
| **MAH-04** — Qu’est-ce qu’une clé étrangère ? | La FK est portée par l’enfant ; relationship fournit la navigation Python dans les deux sens. Un droit d’écriture ou une visibilité ne découle pas de la FK. | [Lecture ciblée](02_RELATIONS_CONTRAINTES_TRANSACTIONS.md) |
| **MAH-05** — Quelle est la relation entre histoire et théorie ? | Story.theories est une collection ; Theory.story est un parent obligatoire par story_id. Supprimer le dossier peut supprimer les théories ; supprimer une théorie ne supprime pas son dossier. | [Lecture ciblée](01_GUIDE_DIX_MODELES.md#mah-c004) |
| **MAH-06** — Pourquoi l’auteur d’une théorie peut-il être nul ? | Theory.user_id nullable porte SET NULL : le texte peut subsister sans compte référencé. Ce mécanisme ne retire pas les données personnelles éventuellement contenues dans le texte. | [Lecture ciblée](01_GUIDE_DIX_MODELES.md#mah-c004) |
| **MAH-07** — Quelle différence entre `CASCADE` et `SET NULL` ? | CASCADE supprime l’enfant ; SET NULL conserve l’enfant et retire sa référence facultative. Les règles SQL et la propagation ORM se lisent séparément. | [Lecture ciblée](02_RELATIONS_CONTRAINTES_TRANSACTIONS.md) |
| **MAH-08** — Comment empêcher deux votes identiques ? | unique_user_story_vote interdit la répétition du couple, pas plusieurs dossiers aimés par un même compte. CommentLike a sa propre unicité pour les commentaires. | [Lecture ciblée](01_GUIDE_DIX_MODELES.md#mah-c006) |
| **MAH-09** — Pourquoi garder une contrainte SQL si l’API vérifie déjà ? | Deux requêtes peuvent lire simultanément une absence. La contrainte SQL reste nécessaire ; il faut identifier le conflit et rollback après l’échec de flush ou commit. | [Lecture ciblée](02_RELATIONS_CONTRAINTES_TRANSACTIONS.md) |
| **MAH-10** — À quoi sert SQLAlchemy ? | L’ORM traduit les objets et requêtes en opérations SQL. Il gère une Session et des métadonnées ; il ne remplace ni le moteur, ni les migrations, ni les contrôles HTTP. | [Lecture ciblée](01_GUIDE_DIX_MODELES.md) |
| **MAH-11** — Que fait `commit()` ? | Commit inclut le flush nécessaire puis valide la transaction. Flush seul envoie les changements mais ne les rend pas définitivement validés. | [Lecture ciblée](02_RELATIONS_CONTRAINTES_TRANSACTIONS.md) |
| **MAH-12** — Que fait `rollback()` ? | Rollback annule la transaction encore active selon les capacités du moteur et remet la Session en état après un échec. Il ne restaure pas un commit déjà réussi ni tous les DDL MySQL. | [Lecture ciblée](02_RELATIONS_CONTRAINTES_TRANSACTIONS.md) |
| **MAH-13** — À quoi sert Alembic ? | Alembic applique une chaîne de transitions parent/enfant. create_all construit les tables manquantes du modèle courant mais ne transforme pas une ancienne cible Report. | [Lecture ciblée](03_GUIDE_SEPT_MIGRATIONS.md) |
| **MAH-14** — Pourquoi supprimer `comments.reports` ? | Le compteur redondant est retiré pour compter les lignes de signalement. Le downgrade recrée zéro sans recalcul : cette précision complète le contrat historique sans le réécrire. | [Lecture ciblée](03_GUIDE_SEPT_MIGRATIONS.md#rev-82deda84bc35) |
| **MAH-15** — Pourquoi le certificat CA est-il utile ? | Dans backend/index.py, la branche Aiven fournit le chemin de CA au pilote par connect_args.ssl.ca. Cette configuration sert au contrôle TLS de confiance côté connexion ; elle n’est ni une FK ni une preuve de connexion réussie. Aucun certificat, secret, environnement privé ou serveur n’a été ouvert pour ce lot. Les vérifications effectives de chaîne et de nom d’hôte demeurent liées au pilote et à la cible. | [Lecture ciblée](06_CORRESPONDANCE_SOURCES.md#contexte-mah-15) |
| **MAH-16** — Les tests SQLite prouvent-ils que MySQL fonctionne ? | Les moteurs et DDL diffèrent. La lecture de branches MySQL et un résultat SQLite ne prouvent pas une exécution MySQL/Aiven. Ce lot ne relance ni migration ni suite applicative. | [Lecture ciblée](03_GUIDE_SEPT_MIGRATIONS.md) |
| **MAH-17** — `reports.target_id` est-il une clé étrangère ? | La vraie FK actuelle est reports.comment_id. target_id est un getter/setter Python de compatibilité exposant une chaîne ; sa validation ne vérifie pas elle-même l’existence de la cible. | [Lecture ciblée](01_GUIDE_DIX_MODELES.md#mah-c009) |
| **MAH-18** — Les migrations créent-elles les dossiers de démonstration ? | Les révisions créent ou transforment le schéma ; elles ne chargent pas les six récits et illustrations. Le peuplement contrôlé est un autre parcours, qui n’est pas exécuté ici. | [Lecture ciblée](03_GUIDE_SEPT_MIGRATIONS.md) |

<a id="contexte-mah-15"></a>

### Contexte limité pour MAH-15 : certificat CA et connexion

Le fichier backend/index.py, dans sa configuration Aiven, lit des noms de variables d’environnement puis fournit au pilote une option ssl contenant un chemin ca. Seule la configuration source est consultée, jamais les valeurs d’environnement ni le fichier de certificat. Un certificat CA participe à la vérification de confiance TLS ; il ne remplace pas les identifiants de connexion, l’autorisation d’un utilisateur applicatif ou les contraintes d’intégrité SQL.

Ce guide n’atteste ni une négociation TLS réussie ni la vérification effective du nom d’hôte sur un serveur. Ces points exigent de contrôler le pilote, les paramètres et une cible autorisée dans une autre campagne. Aucun chemin privé de certificat ni secret n’est repris dans les exemples. La fiche MAH-15 conserve son texte et ses références détaillées.

## Sources complémentaires utilisées pour les exemples

| Chemin | Usage de lecture | Ce qui n’a pas été exécuté |
|---|---|---|
| backend/api/v1/views/likes.py | Lire handle_like, flush/commit/rollback et les filtres de retrait personnel | Aucune route ou requête |
| backend/api/v1/views/comments.py | Vérifier le rôle de comment_to_dict et des routes de commentaire | Aucun comptage SQL réel |
| backend/api/v1/views/admin_stories.py | Repérer archive/restauration et le renouvellement de révision | Aucune archive, restauration ou purge |
| backend/api/v1/views/story_deletion_support.py | Lire les contrôles de purge et la sentinelle | Aucun aperçu ni jeton créé |
| backend/index.py | Lire les options déclarées de connexion pour MAH-15 | Aucun import, chargement de .env ou accès certificat |
| backend/requirements.txt | Versions attendues des dépendances | Aucune installation |
| docs/soutenance/ERRATA_MIGRATIONS_LOT6H22_4.md | Situer les corrections de dialecte préexistantes | Aucun ancien résultat présenté comme nouveau |
| docs/soutenance/fiche-mahamadou.md | Raccorder les dix-huit questions | Aucun remplacement de texte |

Le projet épingle SQLAlchemy 2.0.53, Flask-SQLAlchemy 3.1.1, Flask-Migrate 4.1.0 et Werkzeug 3.1.6 dans backend/requirements.txt. Les documentations web officielles consultées peuvent refléter un correctif plus récent de leur branche ; elles servent à expliquer les mécanismes généraux, sans attester les versions installées ou le comportement d’un serveur non testé. Aucune nouvelle dépendance n’est installée.

## Références vers les futures copies 6H.21.6

Préfixe proposé : `docs/soutenance/code-commente-mahamadou/`. Reproduire sous ce préfixe les chemins backend/models.py, migrations/env.py, migrations/sqlite_safety.py et migrations/versions avec les noms actuels. Aucun de ces fichiers pédagogiques n’est créé dans ce lot et aucun lien actif vers un fichier inexistant n’est ajouté.

Le répertoire des fonctions calcule pour chaque déclaration la future plage L0001…Lxxxx selon le premier décorateur et la fin AST, blancs compris. La numérotation locale sert à relier la future explication au code ; elle ne constitue pas encore une correspondance source/copie puisque la copie n’existe pas.

## Proposition d’installation future, soumise à autorisation

Installer éventuellement les huit Markdown numérotés (sommaire et sept livrables) et la source Mermaid dans un nouveau sous-dossier pédagogique de docs/soutenance, après choix de son nom et revue du contenu. Conserver les anciennes fiches et les trois documents du gel. Adapter à ce moment seulement les liens d’accès que l’utilisateur autorisera.

Les JSON de couverture peuvent être conservés comme annexes pédagogiques ou preuves externes selon la décision de revue. Les instantanés Git et les scripts de génération restent hors du projet. Aucun remplacement de source, migration, README ou fiche n’est préparé comme une modification implicite. Les copies commentées du lot 6H.21.6 demanderont leur propre périmètre.

**Décision de ce lot : proposition documentaire prête à lire ; aucune installation, intégration, publication ou opération Git d’écriture autorisée ou effectuée.**
