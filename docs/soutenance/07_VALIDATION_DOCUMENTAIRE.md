# Rapport de validation documentaire du lot 6H.21.4

Les Petits Enquêteurs — lot 6H.21.4 — 4 novembre 2026, Europe/Paris.

**Proposition externe à lire et à approuver avant installation.** Sources : copie intégrée locale, photographiée par SHA-256 ; pas la seule version du commit Git. Analyse statique : aucun import de l’application, accès SQL, test applicatif ni migration exécutée pour cette rédaction. Les exemples sont pédagogiques et non exécutés. Leur éventuelle exécution exige un contexte temporaire distinct, préparé et autorisé ; ils ne constituent pas des scripts de démarrage du projet.

[Sommaire de soutenance](README.md) · [Correspondance avec les sources](06_CORRESPONDANCE_SOURCES.md) · [Validation documentaire](07_VALIDATION_DOCUMENTAIRE.md)

## Résultat et périmètre

**Validation documentaire statique réussie.** Les sept livrables sont préparés hors des dépôts, avec un sommaire, un diagramme Mermaid autonome et des annexes JSON. Ils couvrent dix modèles, soixante colonnes, vingt-six navigations ORM, treize FK, sept unicités hors PK, sept révisions et trente-cinq entrées de fonction.

Ce résultat signifie que les couvertures et correspondances vérifiées ci-dessous sont cohérentes avec les textes sources lus. Il ne constitue pas une validation applicative, un audit de sécurité complet, une preuve de déploiement ou une autorisation d’installation.

## Contrôles réellement exécutés dans ce lot

| Contrôle | Résultat | Preuve et portée |
|---|---|---|
| Huit documents présents | PASS | Sommaire et sept livrables demandés |
| Dix classes détaillées | PASS | Une section stable pour chaque modèle |
| Soixante colonnes expliquées | PASS | {"colonnes": 60, "avec_type_et_section_classe": true} |
| Vingt-six navigations cohérentes | PASS | Toutes les paires back_populates sont réciproques |
| Treize clés étrangères détaillées | PASS | {"total": 13, "CASCADE": 9, "SET NULL": 2, "non_explicite": 2} |
| Trente-cinq contrats sans doublon | PASS | 34 identifiants conservés et une extension proposée |
| Neuf rubriques par contrat | PASS | 35 contrats : objectif, types, étapes, retour, interactions, effets, risques, exemple, repère futur ; SHA du fichier présent |
| Sept révisions et quatorze points de transition | PASS | Chaîne parent/enfant unique ; détails des sept upgrade et downgrade |
| Schéma final réconcilié statiquement | PASS | Opérations AST des sept upgrade : mêmes noms de tables/colonnes, 13 références/actions et 7 unicités que models.py ; pas de preuve d’exécution SQL |
| Diagramme complet | PASS | 10 entités, 60 colonnes dans le même ordre, 13 associations ; pas de rendu graphique exécuté |
| Syntaxe des exemples Python | PASS | {"blocs_python_parses": 12, "blocs_sql_non_executes": 1} |
| Liens locaux et ancres | PASS | {"liens_valides": 154, "url_officielles_distinctes": 9, "limite": "Les URL externes ont été consultées séparément ; ce contrôleur ne les reteste pas en réseau"} |
| Aucune copie commentée créée | PASS | Chemins futurs en texte ; aucune copie source ligne par ligne dans les livrables |
| Identifiants existants conservés | PASS | {"ancien_total": 212, "nouvelle_proposition": "MAH-F0213 / MAH-M028"} |
| Raccord aux dix-huit questions | PASS | {"mahamadou": 18, "melissa": 18, "sylvie": 18, "commune": 22} |
| Copie intégrée préservée octet par octet | PASS | {"fichiers": 196, "ajoutes": [], "retires": [], "modifies": []} |
| Fiches et trois références gelées préservées | PASS | SHA identiques ; 18+18+18+22 = 76 repères de questions conservés |
| État Git préservé : git_integration | PASS | {"HEAD": "45170b7d5530c834c561afc1a19f39abf288cb74", "index_sha256": "5ee3342560e0928600bec6a70615a669c1c383dcab2ff70a29a3fa7d0bf9181b", "statut_et_refs_identiques": true} |
| État Git préservé : git_original | PASS | {"HEAD": "0d77a9ab0859f1aa6488405a4f524a399a402f30", "index_sha256": "ef2a5e94bcb12ee31eeae712b7b170ed0919f210df6e0827d38efc37cc3a8d22", "statut_et_refs_identiques": true} |
| Livraison hors des dépôts | PASS | {"sortie": "C:\\Users\\diarr\\AppData\\Local\\Temp\\lpe-pedagogie-lot6h21-4", "controle": "git rev-parse ne trouve pas de dépôt parent"} |

Les détails calculés figurent dans `VALIDATION_DOCUMENTAIRE.json` (annexe externe conservée avec la sauvegarde). La syntaxe des **12 blocs Python** a été parsée sans exécuter les exemples. Le bloc SQL est seulement relu ; aucune validation SQL par un serveur ou un parseur spécialisé n’est revendiquée. Les guides et le sommaire totalisent 36188 mots selon un comptage par espaces, hors présent rapport ; ce volume n’est pas une mesure de qualité pédagogique.

## Réconciliation indépendante du schéma par lecture des AST

Le contrôleur parcourt les upgrade dans l’ordre des parents. Il reconnaît les CREATE TABLE, ajouts/retraits de colonnes, remplacements de FK et créations d’index uniques présents dans ces sources. Il comptabilise les objets sans importer Alembic, SQLAlchemy ni le projet, et sans compiler/exécuter une instruction SQL.

Il retrouve les totaux successifs de tables/colonnes/FK : 7/45/9, 7/45/9, 9/56/10, 9/55/10, 9/56/10, 9/56/11 et 10/60/13. À la fin, les noms de tables et de colonnes, les treize couples de référence et leurs actions ON DELETE ainsi que les sept règles d’unicité correspondent aux modèles. Les noms historiques des FK non nommées dans le modèle ne sont pas artificiellement déclarés identiques.

La preuve détaillée est `SCHEMA_RECONSTRUIT_STATIQUEMENT.json` (annexe externe conservée avec la sauvegarde). Cette reconstruction ne simule ni le moteur, ni les données, ni les branches d’échec, ni les types physiques du serveur. Elle ne prouve pas la conservation effective des lignes pendant une reconstruction et ne vérifie pas l’intégralité des possibilités de l’API Alembic.

## Relecture technique des points sensibles

1. Les defaults et onupdate Python sont distingués des defaults SQL ; les dates restent des datetime sans timezone=True dans ces modèles.
2. Les relationships sont distinctes des FK ; une suppression ORM du compte n’est pas présentée comme une suppression métier universellement sûre.
3. Le compteur physique Comment.likes est distingué des likes individuels ; le sérialiseur enrichi garde une valeur historique incompatible au lieu de l’attribuer à des comptes.
4. Report.type et target_id sont des propriétés ; le getter sur objet incomplet et le contournement du setter par affectation directe sont expliqués sans promettre une validation globale.
5. Le downgrade de 82deda recrée zéro sans recalcul ; les retours de inspect_legacy sont décrits avec leur structure concrète.
6. Les migrations de données font des lectures et ne sont pas assimilées à une chaîne complètement générable offline.
7. Le scope SQLite est un mécanisme de transaction et de contrôle, avec des limites de nettoyage ; le marqueur Python n’impose pas une isolation système ou une maintenance exclusive.
8. Les suppressions de colonnes/tables et les cascades ne sont jamais présentées comme restaurables par un simple downgrade ; les DDL MySQL peuvent committer implicitement.

Cette relecture est celle de l’agent rédacteur, appuyée par les contrôles statiques. Elle n’est pas attribuée à un second relecteur indépendant ou à un test applicatif qui n’aurait pas eu lieu.

## Préservation observée

Les 196 empreintes des fichiers de travail de la copie intégrée sont identiques avant et après. Cela inclut models.py, les sept révisions, le README, les fiches et les référentiels, le catalogue et les illustrations. Les quatre fiches gardent leurs 76 repères de question ; l’égalité intégrale de leurs octets préserve aussi leurs textes historiques et réponses archivées.

Pour le dépôt original et la copie intégrée, HEAD, les références Git, le statut et l’empreinte de l’index restent identiques. Les instantanés locaux SOURCES_AVANT.json et SOURCES_APRES.json permettent de refaire cette comparaison. Les fichiers ignorés privés du dépôt original n’ont pas été lus pour construire un manifeste exhaustif ; aucune modification n’a été effectuée sur eux.

Aucune commande Git d’écriture, aucune modification de configuration globale, aucun transfert dans un dépôt et aucune publication n’ont été réalisés. Toutes les écritures documentaires et le bytecode éventuel des outils de rédaction sont confinés au dossier de livraison sous Temp par les chemins utilisés ; ce constat d’opérations n’est pas une garantie de confinement contre du code arbitraire.

## Ce qui n’a pas été exécuté et ce qui reste à décider

| Opération | État et limite |
|---|---|
| Tests backend/frontend et suites historiques | Non relancés : seuls les contrôles documentaires nécessaires ont été exécutés |
| Migration SQLite mémoire/fixture | Non exécutée dans ce lot ; anciens résultats non réétiquetés |
| Migration MySQL/Aiven ou connexion réseau SQL | Aucune ; compatibilité opérationnelle à établir séparément |
| Accès à une SQLite persistante | Aucun accès SQL ni ouverture de ce fichier |
| Serveur 5066 | Aucune requête, arrêt ou relance |
| Copie commentée ligne par ligne | Non créée ; lot 6H.21.6 futur |
| Rendu visuel du diagramme | Non exécuté ; couverture de la source Mermaid contrôlée, conventions confrontées à la documentation officielle |
| Installation dans un projet | Non effectuée ; autorisation explicite requise |
| Conservation durable | Le dossier Temp peut être nettoyé ; une archive externe est fournie |

## Confidentialité des livrables

Les exemples utilisent des données inventées et example.test. Aucun hachage, cookie, jeton, URI privée, contenu de base ou certificat n’est extrait. Les noms de colonnes et variables de configuration servent à expliquer le code public. Les motifs réels des signalements ne sont jamais consultés.

L’archive des propositions inclut seulement les Markdown, le diagramme et les JSON documentaires listés par LIVRABLES_SHA256.json. Elle exclut les instantanés Git locaux, les scripts de génération, le bytecode et toutes les sources applicatives. Un contrôle CRC de l’archive et une comparaison de chaque membre avec son SHA-256 sont exécutés après sa création ; le résultat est écrit dans CONTROLE_ARCHIVE.json, à côté de l’archive. Cette liste explicite empêche d’inclure implicitement le reste d’un répertoire de travail.

## Proposition à approuver

Les guides sont prêts pour une revue pédagogique et un choix d’emplacement de conservation. Leur installation future peut ajouter un nouveau dossier de documentation avec ses propres liens, sans remplacer les fiches historiques ou le référentiel gelé. Cette installation reste suspendue à l’autorisation explicite de l’utilisateur, conformément à sa demande. Aucun verdict de déploiement ou d’intégration main n’est déduit de cette livraison documentaire.
