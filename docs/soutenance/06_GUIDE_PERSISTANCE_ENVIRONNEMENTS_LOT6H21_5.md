# Persistance et environnements — lot 6H.21.5

Les Petits Enquêteurs — préparation pour Mahamadou — **5 novembre 2026, Europe/Paris**.

**Proposition documentaire externe, sans installation autorisée.** Référence : 203 fichiers de la copie intégrée, vérifiés par empreintes. Aucun module applicatif importé, aucun accès SQL, aucune migration, aucun test applicatif ni intervention sur le serveur 5066. Les exemples sont des illustrations non exécutées, pas des commandes à lancer sur une base réelle. Les responsabilités BDD de Mahamadou sont distinguées des composants partagés avec Sylvie et du frontend de Mélissa.

[Sommaire des huit guides](01_GUIDE_REQUETES_SQLALCHEMY_LOT6H21_5.md#sommaire) · [Références exactes et soutenance](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md) · [Contrôles et limites](08_VALIDATION_DOCUMENTAIRE_LOT6H21_5.md)

## La persistance dépend d’une destination, pas du mot « commit » seul

Commit valide une transaction dans la base sélectionnée. Il ne transforme pas une base mémoire en fichier, ne déplace pas automatiquement des données vers Aiven et ne sauvegarde pas le cookie de session. Pour expliquer un redémarrage, il faut identifier la configuration choisie, la durée de vie du stockage et la clé de signature.

| Mode | Configuration ou point d’entrée | Stockage attendu | Après arrêt/redémarrage | Ce que ce lot prouve |
|---|---|---|---|---|
| SQLite mémoire | URL :memory: imposée par le kit | Base liée à la connexion/pool et au processus préparé | Les contributions ne survivent pas au nouveau processus de démonstration ; un seed neuf prépare un autre état | Lecture du lanceur ; aucun nouveau démarrage |
| SQLite fichier du lanceur général | DATABASE_URL ou repli déclaré dans backend/index.py | Fichier choisi par la configuration | Les transactions validées peuvent survivre si le même fichier est conservé ; pas de seed automatique par run_local | Pas d’ouverture de ce fichier ni d’examen de son schéma réel |
| SQLite persistante dédiée | tools/demo_persistante.py | Fichier local reconnu et clé séparée, sous répertoire privé | Données conservées ; clé stable peut permettre la continuité des cookies du mode si autres conditions remplies | Étude du code uniquement, aucune opération sur le service existant |
| MySQL/Aiven | Groupe complet des six variables Aiven | Serveur MySQL configuré, pilote PyMySQL et CA | Les données dépendent du service et des transactions validées, pas du processus Flask local | Pas de connexion, TLS ou migration réelle validée ici |
| Kit scolaire isolé | tools/recette_lot6g4.py | Mémoire synthétique et preuves dans un répertoire temporaire | Nouvelle exécution = nouvelle base et nouveaux accès fictifs générés | Un mode de préparation de confiance, pas un confinement système |
| Serveur de démonstration 5066 | serve du mode persistant | Même destination locale initialisée | Relance prévue sans create_all/seed/migration | Aucun arrêt, requête ou redémarrage effectué dans ce lot |

## Priorité de configuration de backend/index.py

Si AIVEN_DB_HOST, PORT, USER, PASSWORD, NAME et CA_CERT sont toutes présentes, la branche Aiven est choisie en priorité. Le code construit l’URL avec quote_plus pour les identifiants et fournit connect_args.ssl.ca. Sinon DATABASE_URL est utilisée si elle existe ; à défaut le chemin SQLite de repli est construit depuis la racine du projet.

L’explication porte sur les noms des variables et les branches du code, jamais sur leurs valeurs. Aucun .env, URI privée ou certificat n’est lu pour cette étude. Dire « j’ai fixé DATABASE_URL à mémoire donc je suis isolé » serait insuffisant si un groupe Aiven complet conserve la priorité. Les lanceurs de confiance vident explicitement ce groupe avant le chargement de l’application.

db.init_app n’est pas suivi d’un create_all global dans ce module. Le lanceur run_local charge cette configuration et sert l’interface/API ; il ne crée ni ne peuple une base existante. Un serveur qui répond à une page HTML ne démontre donc pas que le schéma ou les six récits sont prêts.

Références : [Sélection de la branche Aiven](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#source-8bc47a35d18a) ; [MAH-F0048 — main](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0048).

## Le kit scolaire mémoire : préparer, vérifier, éventuellement servir

[MAH-F0121 — main](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0121) valide les sources, prépare un dossier de preuve extérieur au dépôt et remplace l’environnement par un ensemble limité. Il fixe une nouvelle clé fictive, une URL mémoire, l’origine locale attendue et les variables Aiven vides. Les chargements dotenv et les connexions réseau sont neutralisés dans le parcours de confiance.

Avant l’import applicatif, le lanceur met en place les gardes de moteur et connexion SQLite. La fabrique de connexion refuse une destination autre que mémoire, active les FK et installe un authorizer contre les opérations ATTACH/DETACH dans ce chemin. Les autres modules de gardes du projet ont leur propre périmètre et ne sont pas confondus avec une isolation imposée par le système.

Dans le contexte applicatif, create_all construit les dix tables actuelles. [MAH-F0113 — seed](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0113) crée explicitement trois comptes fictifs, deux catégories puis les dossiers. Le flush rend les dépendances utilisables avant les histoires ; commit valide les insertions. Le jeu scolaire par défaut a deux dossiers de démonstration avec identifiants dédiés ; l’option histoires-originales charge les six récits approuvés et conserve leurs vrais ids du catalogue.

Les mots de passe de ce kit sont générés à l’exécution et ne sont pas des accès à publier dans les guides. Les événements de recette et leurs rapports restent des données de démonstration contrôlées ; aucun compte de la base privée n’est copié. Le programme peut inspecter les ressources WSGI sans écoute réseau ; la branche serve exige sa propre autorisation humaine prévue par son interface. Ce lot n’emprunte aucune de ces branches.

Le port du kit est 5064 dans le code. Il n’est pas le service persistant 5066. Une fenêtre de navigateur fermée ne suffit pas à déterminer la vie du processus ; l’arrêt du processus contenant la base mémoire met fin à ses données, même après commit. Une nouvelle exécution refait un seed, pas une restauration des contributions antérieures.

## Le mode persistant dédié : quatre objets à distinguer

| Objet | Rôle | Risque de confusion |
|---|---|---|
| Fichier de base | Tables, comptes et contributions validés | Le remplacer n’est pas relancer un serveur |
| Clé de session | Signature des cookies de ce mode | La renouveler peut forcer une reconnexion sans supprimer les comptes |
| Verrou d’opération | Éviter des opérations coopératives simultanées | Ce n’est pas un verrou SQL de toutes les lignes ni un confinement hostile |
| Sauvegarde et manifeste | Copie cohérente locale + empreintes et format | Une empreinte seule ne prouve pas un stockage externe durable ou une restauration testée |

[MAH-F0056 — Paths.checked](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0056) contrôle le périmètre de chemins et refuse les redirections recensées. private_directory vérifie les droits privés ; la branche Windows crée/vérifie une DACL réservée au SID courant. Ces contrôles sont lus, sans ouvrir le répertoire privé existant ni vérifier ses droits réels pendant cette session.

[MAH-F0060 — operation_lock](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0060) utilise un verrou système de fichier non bloquant, msvcrt sous Windows ou flock sur l’autre branche. Les commandes coopératives passent sous ce verrou ; serve le garde pour sa durée, de sorte qu’une sauvegarde/check par ce même outil doit refuser pendant l’occupation prévue. Ce mécanisme n’empêche pas tout programme arbitraire du même compte de contourner le protocole.

### Initialisation : une destination neuve, pas une remise à zéro

[MAH-F0083 — initialize](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0083) refuse une destination déjà présente. Il valide les personnes saisies dans une console privée, charge le catalogue approuvé, prépare un nouveau dossier de travail, crée exclusivement le fichier et la clé puis configure l’application pour cette destination. Aucun secret de démonstration existant n’est affiché dans cette documentation.

Dans app_context, create_all crée le schéma neuf, des PRAGMA de format sont renseignés, les comptes/catégories sont ajoutés, flush établit les dépendances, les six histoires sont ajoutées et commit valide. inspect_database vérifie ensuite le contenu attendu de cette destination neuve. Le dossier de travail est renommé vers la destination seulement si aucune destination concurrente n’est apparue.

Cette séquence combine une transaction SQL et des opérations de fichiers : elle n’est pas une unique transaction ACID englobant le système de fichiers. La présence d’un finally de nettoyage ne garantit pas toutes les récupérations en cas de panne du système. L’objectif est de refuser une reprise implicite d’un état inconnu, pas de migrer automatiquement une base existante.

### Service ordinaire : pas de seed silencieux

[MAH-F0088 — serve](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0088) exige l’état reconnu via initialized puis entre dans application(paths). Il construit le serveur local autour du même wrapper statique et écoute sur 127.0.0.1:5066 sans thread concurrent de ce serveur. Un port occupé provoque un refus ; aucun processus n’est arrêté automatiquement.

Le corps de serve ne fait ni create_all, ni seed, ni upgrade Alembic. Les archives et contributions restent donc telles qu’enregistrées, sous réserve des transactions normales du service. Un redémarrage n’est pas censé réactiver un dossier archivé. La clé de session conservée et le nom de cookie spécifique participent à la séparation du mode ; rien n’autorise à réutiliser ses données privées comme fixture pédagogique.

### Inspection : lecture explicite, non effectuée ici

[MAH-F0065 — inspect_database](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0065) compare le format PRAGMA et le schéma des dix tables aux métadonnées compilées pour SQLite, demande integrity_check et foreign_key_check, impose le mode de journal prévu puis compte les lignes et compare les originaux du catalogue. Les identifiants de contenu sont des paramètres ; les noms de tables de comptage proviennent des métadonnées reconnues.

Ces étapes sont décrites, pas lancées. Le fait que check soit une lecture fonctionnelle ne l’autorise pas dans cette session : elle ouvrirait la SQLite persistante interdite. initialized lit aussi la clé et ouvre la base, donc on ne l’appelle pas pour « seulement vérifier » le serveur actuel.

### Sauvegarde et restauration : opérations distinctes du SQL métier

[MAH-F0086 — backup](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0086) prépare une destination privée et appelle _copy_database, qui utilise l’API DBAPI backup entre source et cible autorisées. Le manifeste contient format, date UTC et empreintes de base/catalogue ; le dossier de sauvegarde reçoit un identifiant temporel et aléatoire. Ce n’est pas un endpoint HTTP de contribution.

[MAH-F0087 — restore](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md#code-mah-f0087) vérifie l’identifiant de sauvegarde, le manifeste et les empreintes. Une base déjà présente impose un indicateur explicite de remplacement ; une sauvegarde de sécurité est prévue avant ce remplacement. Le renouvellement de clé est une option séparée ; des annexes SQLite présentes peuvent faire refuser le remplacement. Le code note qu’un changement de clé avant remplacement de base peut imposer une reconnexion si une étape suivante échoue.

Il serait incorrect d’assimiler restore à la route admin restore d’un dossier : l’une remplace une base locale reconnue, l’autre remet seulement archived_at à NULL sur une histoire. Aucun backup, restore, check, init ou serve n’est exécuté pour ce lot.

## MySQL/Aiven : ce qui est préparé et ce qui n’est pas vérifié

Les modèles, migrations et requêtes utilisent le dialecte MySQL dans certains contrôles et options. CommentLike déclare InnoDB ; la migration de likes vérifie les moteurs parents et foreign_key_checks. La purge vérifie les moteurs de ses tables nécessaires et les FK attendues. Les types de PK sont copiés par les migrations concernées pour les références.

La présence de ces branches n’atteste pas le moteur de chaque table déployée, les privilèges, le niveau d’isolation, la validité du CA, la vérification du nom d’hôte, le schéma installé ou la réussite de la chaîne Alembic sur Aiven. Aucun secret ni certificat n’a été consulté ; aucun socket SQL n’a été ouvert dans cette session.

Un commit réussi sur un service distant se juge dans le contexte de sa transaction et de ses réglages de stockage. La continuité après redémarrage Flask n’est pas la même question que la récupération du serveur de base après panne. Une injection d’exception MySQL dans un test Python vérifie le traitement de cette exception, pas la durabilité ni les verrous du serveur.

## Migrations, create_all et schéma réellement en service

Les sept révisions et le scope SQLite sont déjà détaillés au lot 6H.21.4. Les identifiants revision/down_revision ne changent pas dans ce lot. create_all n’avance pas une base à travers l’ancien format reports ; Migrate(app, db) n’exécute pas la migration. Un schéma créé à partir des métadonnées et un historique Alembic appliqué peuvent avoir des noms de contraintes différents malgré des règles correspondantes.

Le scope SQLite vérifie une intégrité avant/après et suspend temporairement les FK pour des reconstructions de tables dans un contexte maîtrisé. Il ne démontre pas l’exclusivité de maintenance et le marqueur connection.info n’est pas une protection contre du code arbitraire. Les DDL MySQL peuvent avoir des commits implicites ; rollback d’une transaction applicative et downgrade de schéma ne sont pas des restaurations universelles.

Le lanceur général backend/index.py ne contient pas à lui seul l’activation systématique des FK SQLite sur chaque connexion comme les deux outils de démonstration examinés. Il faut donc qualifier la configuration réelle avant de promettre les cascades. La purge refuse ses préconditions d’intégrité manquantes au lieu de supposer l’activation.

## Commandes et apprentissage sans intervention sur le service

Ce guide décrit les sous-commandes par leur nom pour comprendre leur rôle. Il ne fournit pas de séquence à lancer sur l’installation actuelle. Aucune commande d’initialisation, de restauration, de check persistant ou de migration n’est proposée comme test documentaire. L’analyse a utilisé seulement lecture de fichiers publics, AST, empreintes et métadonnées Git de lecture.

Pour une future campagne autorisée, il faudrait une destination jetable distincte, des paramètres synthétiques, des garde-fous vérifiés et une séparation des identités de session. Le besoin de confinement système doit être évalué selon le code exécuté ; des interceptions Python restent des contrôles de code de confiance, pas une frontière de sécurité générale.

## Questions de relance et réponses

« Un commit mémoire suffit-il après redémarrage ? » — Il valide l’état de la base mémoire courante ; un nouveau processus n’en conserve pas les lignes.

« Pourquoi ne pas lancer init à chaque démarrage ? » — Init crée un état neuf et refuse une destination existante ; le service ordinaire doit conserver les contributions et archives déjà présentes.

« Restaurer une histoire restaure-t-il sa sauvegarde ? » — Non : la route d’archive change un attribut de visibilité ; la restauration d’un fichier de base appartient à un autre outil et un autre risque.

« Les tests mémoire valident-ils Aiven ? » — Ils couvrent leurs comportements et fixtures. Le moteur distant, le TLS, le schéma, les DDL et la concurrence exigent une preuve séparée, absente ici.

« Les droits du répertoire Windows prouvent-ils un confinement Python ? » — Ils contrôlent l’accès à ce répertoire selon l’identité système ; ils ne limitent pas toutes les capacités d’un programme arbitraire du même compte.
