# Lot 6G.5 — recette réelle locale dans Microsoft Edge

> Archive pédagogique datée : les résultats et descriptions ci-dessous concernent le lot indiqué. Les anciens repères de ligne ne décrivent pas la version candidate. Pour préparer la soutenance actuelle, consulter les quatre fiches et le référentiel reliés au sommaire.

> Copie publique de référence : les chemins personnels et liens de travail internes sont retirés. Les preuves et commandes historiques gardent leur date et leur périmètre ; utiliser le README actuel pour le lancement.

[Bilan 6G.4](BILAN_LOT6G4.md) · [Protocole manuel](RECETTE_MANUELLE_LOT6G4.md) · [Audit 6G.3](BILAN_LOT6G3.md)

**1er novembre 2026 — recette Edge partiellement vérifiée, clôturée après les problèmes d’interface signalés par l’utilisateur. Verdict : NO-GO pour déclarer la démonstration au jury entièrement validée en l’état.** Les écritures principales sont réelles et cohérentes dans la base synthétique. Deux corrections d’interface sont proposées : état de connexion cohérent sur les pages et contexte complet des signalements administratifs. Le cycle de like de commentaire, les sept nombres visibles du dashboard et la déconnexion volontaire restent non validés dans Edge.

**Le seul serveur lancé pour cette recette est arrêté et le port 5064 est fermé.** Les preuves et la base temporaire sont conservées. Aucun code applicatif, modèle, route, migration ou dashboard modifié ; aucun accès MySQL/Aiven ou `.env`, aucune élévation ou modification Windows, aucun CDP, commit, push ou changement de branche. Arrêt après 6G.5, en attente de validation et d’autorisation pour les corrections.

## 1. Contrôles initiaux et environnement

Bilans 6G.4 et 6G.3, protocole 6G.4 et instructions du dépôt repris intégralement. Aucun `AGENTS.md` trouvé dans le dépôt ou les parents contrôlés. Les quarante sources du manifeste 6G.4 sont vérifiées avant import applicatif ; le kit et son manifeste restent figés.

Branche `feature/frontend-api-integration`, HEAD `07a9f03ea0a3bdad4a07066fdd7bab1997cc158b`. Départ : **48 fichiers suivis modifiés, 75 non suivis, aucun indexé**. Empreintes de 135 fichiers préexistants enregistrées avant préparation, sans copie de secrets, anciennes données exclues ou bases préexistantes.

Python 3.13.0 ; les neuf dépendances installées correspondent exactement à `backend/requirements.txt` : Flask 3.1.3, flask-restx 1.3.2, Flask-Cors 6.0.5, Flask-SQLAlchemy 3.1.1, SQLAlchemy 2.0.53, PyMySQL 1.2.0, python-dotenv 1.0.1, Werkzeug 3.1.6, Flask-Migrate 4.1.0. Aucun téléchargement ou installation.

Le serveur local Flask est servi par Werkzeug, mono-thread, sans debug/reloader, à **`http://127.0.0.1:5064/`**. PID de recette : **20296**. L’ouverture et les actions Edge sont effectuées par l’utilisateur ; l’assistant ne dispose pas d’outil de pilotage manuel du navigateur et n’emploie pas d’automatisation CDP.

## 2. Base temporaire et preuve d’isolation

Le kit 6G.4 utilise exclusivement SQLite mémoire. L’autorisation 6G.5 demande une base dans un dossier temporaire dédié. Un **adaptateur de recette distinct et relu, hors dépôt**, est préparé avant toute écoute : stockage fichier unique, gardes adaptés et observation sans corps HTTP. Le périmètre applicatif reste celui du kit validé ; aucune correction de fonctionnalité n’est introduite.

Base utilisée par le serveur :

```text
[chemin local privé retiré]
```

À chaque exécution, un nouveau dossier est créé ; ce fichier doit être absent avant initialisation. Driver SQLite et chemin résolu exactement égal à ce fichier sont exigés. SQLite mémoire, autres fichiers SQLite, MySQL et ATTACH/DETACH sont refusés. `PRAGMA database_list` confirme le seul fichier autorisé ; FK actives, dix tables, `foreign_key_check` vide.

Le schéma neuf est créé depuis les modèles **uniquement dans cette base synthétique**. Aucune migration candidate ni chaîne Alembic jouée. Données initiales minimales : trois comptes fictifs, deux catégories et deux dossiers d’id 17/42, avec SVG local. Aucun commentaire, signalement ou like de remplissage. Les adresses des quatre comptes finaux appartiennent à `@example.invalid`, contrôle réalisé sans exporter leurs valeurs. Les mots de passe temporaires ne figurent pas dans les preuves HTTP/SQL ou ce rapport.

Avant import de l’application : environnement enfant minimal, secret temporaire créé une seule fois, dotenv neutralisé, six paramètres Aiven vides, URL du fichier SQLite imposée. PyMySQL et toute autre base sont bloqués. Lectures limitées aux sources/runtime/preuves ; écritures interdites dans le dépôt. Réseau externe, sous-processus applicatifs et migrations interdits ; seule l’écoute autorisée sur `127.0.0.1:5064` est admise. Aucun certificat ou identifiant réel lu.

L’adaptateur conserve la vérification des quarante sources d’origine ; ses propres changements et son empreinte sont consignés séparément dans `adapter-review.json` et `adapter.diff`. Il n’est pas présenté comme le kit mémoire 6G.4 inchangé à l’exécution. Aucun pare-feu, droit, profil Edge ou paramètre Windows modifié.

## 3. Vérifications avant l’écoute et contrôles HTTP

Sept sondes de refus réussissent dans un processus distinct : lecture privée, écriture dépôt, écriture hors preuves, base non autorisée, réseau, migration et sous-processus. Elles vérifient le blocage avant entrée/sortie ; leurs compteurs positifs sont attendus.

L’inspection sur fichier synthétique est **READY**. Un parcours WSGI de **43 requêtes/7 groupes** réussit sur une autre base fichier synthétique : compte/commentaire, likes ajoutés/retirés, unicité, CSRF, historique incompatible conservé, vrai flush puis rollback, signalement, administration et transitions autorisées. Aucun de ces essais n’est attribué à Edge. Les compteurs interdits de ces deux exécutions sont tous à zéro.

Le processus destiné à écouter crée ensuite une base propre et vérifie son isolation avant démarrage. Ses sept résultats SQL initiaux sont **2, 1, 1, 3, 0, 0, 0** : dossiers actifs, résolus, Cold Cases, comptes, commentaires, signalements, propositions pending.

Trois requêtes HTTP locales PowerShell retournent 200 : `/`, `/api/v1/stories`, `/api/v1/stats`. Elles prouvent le vrai transport local, pas un rendu navigateur. Elles restent séparées des requêtes Edge.

Un contrôle OS complémentaire par `Get-NetTCPConnection` échoue avec le refus CIM `0x80041003`. Aucun droit supplémentaire ou contournement demandé. La borne d’écoute est imposée par le constructeur du serveur et le garde de `socket.bind`, puis les réponses HTTP locales confirment son fonctionnement.

## 4. Pages et parcours réellement observés dans Edge

L’utilisateur réalise la navigation manuellement. Les traces finales contiennent **224 requêtes HTTP identifiées Edge par leur agent utilisateur, dont 164 requêtes API**. Aucun en-tête Edge n’est fabriqué par les contrôles de l’assistant. Les 224 réponses se répartissent en 177 réponses 200, 11 réponses 201, 4 réponses 401 et 32 réponses 403 ; les refus ne sont pas comptés comme succès.

Les dix pages suivantes sont réellement demandées :

```text
index.html (également par /)
inscription.html
connexion.html
histoires.html
coldcases.html
dossier.html
admin-connexion.html
admin-dashboard.html
proposer-histoire.html
theories.html
```

Les deux dernières pages sont ouvertes, mais aucune publication de proposition/théorie n’est déclarée validée depuis leur seule ouverture. L’assistant n’a pas observé directement le rendu : les affirmations visuelles ci-dessous viennent des réponses de l’utilisateur, rapprochées du transport et de SQL.

| Parcours | Preuves réelles | Conclusion et limite |
|---|---|---|
| Inscription/connexion | POST users 201, nouveau compte id 4 ; POST login 200, puis `/me` 200 | Compte et session opérationnels dans le passage observé |
| Histoires et Cold Cases | Pages et GET des dossiers 17/42 ; écritures associées à chacun | Deux catégories réellement consultées |
| Commentaires | Trois POST 201 et trois lignes SQL ; l’utilisateur confirme voir le texte dans la fiche | Publication/lecture réelles ; accès depuis l’administration peu explicite |
| Signalements | Deux POST 201 ; Report 1 → Comment 1, Report 2 → Comment 2 ; motif visible confirmé par l’utilisateur | Bonnes cibles ; contexte histoire/catégorie absent de la carte administrative |
| Like d’histoire | POST 201, DELETE 200 et réajout sur 17 ; cycles ajout/retrait sur 42 | Écritures/retraits SQL confirmés ; libellé personnel après actualisation non décrit précisément par l’utilisateur |
| Like de commentaire | Aucun POST/DELETE de cette route dans Edge ; zéro CommentLike final | **Non validé dans Edge**, pas assimilé à un échec SQL ; WSGI distinct réussi |
| Administration | Page et GET privés 200 ; consultation des rapports confirmée | Accès réel ; sept valeurs DOM non transmises pour comparaison exhaustive |
| Bannissement complémentaire | POST `/admin/users/2/ban` 200 ; compte conservé | Action observée ; reconnexion du compte banni non recettée |
| Déconnexion volontaire | Aucun POST `/logout` observé | **Non exécutée/non validée dans Edge** ; arrêt du serveur distinct d’une déconnexion |

## 5. Enregistrements, likes et absence de confusion de cibles

Relations finales des commentaires :

| Commentaire | Dossier | Auteur synthétique |
|---|---:|---:|
| 1 | 17 — histoire résolue | 4 — membre inscrit |
| 2 | 42 — Cold Case | 4 — membre inscrit |
| 3 | 42 — Cold Case | 1 — administrateur |

Les deux Report sont toujours reliés aux commentaires 1 et 2, donc respectivement aux dossiers 17 et 42. Aucune cible d’histoire n’est confondue avec un identifiant de commentaire. Les trois compteurs physiques historiques `Comment.likes` restent zéro.

Le premier cycle d’histoire, séquences 64/68/82, donne POST `/votes/17` 201 → ligne présente, DELETE 200 → ligne retirée, POST 201 → ligne réajoutée. Sur le Cold Case, des ajouts/retraits sont également observés. Les Vote finaux sont `(user_id=4, story_id=17)` et `(user_id=4, story_id=42)` ; les autres retraits n’ont pas supprimé ces contributions du membre. Aucun couple Vote en doublon. La contrainte d’unicité demeure ; un POST doublon 409 volontaire dans Edge n’a pas été reproduit.

Le cycle demandé de like individuel de commentaire n’est pas effectué malgré les instructions : aucune écriture CommentLike issue du navigateur ne figure dans les traces. Il reste à recetter après correction/clarification des interfaces. La réussite WSGI du mécanisme n’est pas substituée à cette vérification Edge.

## 6. Dashboard et sept compteurs

Valeurs finales obtenues par SELECT dans la même base de recette :

| Indicateur | Valeur SQL finale |
|---|---:|
| Dossiers actifs | 2 |
| Histoires résolues | 1 |
| Cold Cases | 1 |
| Utilisateurs | 4 |
| Commentaires | 3 |
| Signalements | 2 |
| Propositions en attente | 0 |

Les quatre comptes et trois commentaires résultent des fixtures minimales et des formulaires réellement exercés ; les deux signalements sont de vraies lignes. Aucun nombre ajouté artificiellement au DOM. Les GET administratifs aboutissent et les snapshots SQL sont cohérents, mais l’utilisateur n’a pas transmis les sept valeurs affichées : **égalité complète SQL/DOM non validée manuellement**. Les GET multiples ne constituent pas un instantané transactionnel global.

L’utilisateur confirme le texte des commentaires après **Dossiers → Consulter le dossier**, puis section Commentaires, et le motif dans **Signalements reçus** en bas du dashboard. Il signale néanmoins l’impossibilité d’identifier directement dans la carte le commentaire, l’histoire et la catégorie. Ce défaut d’accès/contexte est conservé comme résultat de recette ; le dashboard reste inchangé.

## 7. Problème de connexion : constat et diagnostic

L’utilisateur rapporte une impression de déconnexion à chaque changement de page, puis précise utiliser le compte admin. Il confirme qu’en revenant à l’accueil **sans se reconnecter**, le pseudo et « Déconnexion » sont présents.

Les traces concordent : après authentification, les GET `/api/v1/me` continuent à retourner 200 ; les opérations authentifiées fonctionnent. Aucun POST `/logout`. **Une déconnexion réelle après chaque action n’est pas reproduite.** Le défaut d’affichage est confirmé : seul `index.html` possède `session-controls`, traité par `app.js`. Les pages Histoires, Cold Cases, fiche, théories, proposition et connexion gardent un lien « Connexion » fixe, même avec une session valide. Le rôle admin ne change pas cette présentation trompeuse.

Des connexions successives à des comptes différents remplacent volontairement la session dans ce même contexte navigateur ; elles sont distinctes d’une déconnexion causée par une contribution. Le secret de recette est créé une seule fois, sans reloader. Aucun changement du stockage d’authentification ou de la base n’est justifié par les faits observés.

**Correction proposée, non appliquée :** rendre le pseudo/rôle et « Déconnexion » cohérents sur les pages en réutilisant `/me` et le mécanisme existant. Tester navigation, compte admin/membre, changement de compte et refus de session. Aucun besoin de jeton persistant dans localStorage ou de nouvelle authentification.

## 8. Problème de contexte des signalements

Le compteur Commentaires n’ouvre pas de liste générale ; les textes restent consultables dans les fiches. `frontend/admin-dashboard.js`, fonction `reportCard`, affiche type, identifiant de cible, statut, date et motif. GET `/api/v1/admin/reports` renvoie la représentation actuelle de Report, sans texte du commentaire, titre/slug du dossier ou catégorie.

**Le manque de contexte de modération est confirmé par le code et le retour humain ; les relations en base sont correctes.** Il ne s’agit pas d’une perte de commentaires ou de signalements.

**Correction ciblée proposée, non appliquée :** enrichir la lecture administrative par Report → Comment → Story → Category ; afficher dans la carte le commentaire concerné, le titre/lien du dossier et sa catégorie. Conserver permissions administrateur, ids canoniques, affichage sécurisé par texte, relations existantes et sept indicateurs. Aucun nouveau modèle/table nécessaire. Prévoir tests de bonne cible, rôles, XSS, archives/commentaire disparu et non-régression des agrégats.

Cette correction touche l’affichage du dashboard et la réponse de sa route de lecture. Elle exige une autorisation distincte : la demande 6G.5 interdit de modifier le dashboard et impose d’attendre l’accord avant toute modification applicative.

## 9. Erreurs et vérifications non réalisées

Les quatre réponses API 401 sont les contrôles `/me` avant connexion et deux tentatives login refusées, suivies de connexions 200. Le détail des identifiants saisis n’est pas conservé. Les 32 réponses 403 concernent exclusivement les demandes automatiques `/favicon.ico`, hors liste publique ; aucune correction ou ouverture de ressource non autorisée pour les masquer.

Aucun 5xx Edge observé. Les pertes réseau, timeout et refus CSRF provoqués ne sont pas reproduits dans ce navigateur ; aucun succès de ces scénarios revendiqué. Ils restent couverts par les essais isolés historiques et le parcours WSGI, catégories séparées.

**Non validés :** cycle de like de commentaire dans Edge, état personnel des likes après actualisation décrit précisément, sept valeurs DOM complètes, déconnexion volontaire, clavier/lecteur d’écran/mobile/contraste, charge et concurrence multi-connexions. Les pages propositions/théories ouvertes ne prouvent pas leurs soumissions. Archivage/restauration non exercés dans ce passage Edge. Aucun MySQL/Aiven ou déploiement validé.

Le risque 6G.3 de DDL partiellement appliqué reste documenté : table créée sans index après incident, rollback insuffisant et relance refusée possible. Aucune migration nécessaire dans la base neuve de cette recette ; aucun ancien historique converti. SQLite fichier ne prouve ni les types, ni les verrous, ni les DDL MySQL.

## 10. Résultats automatisés et statuts séparés

| Catégorie | Résultat 6G.5 |
|---|---|
| 815 tests unitaires/contrats de 6G.4 | Référence historique ; **non réexécutés**, pas ajoutés aux résultats actuels |
| Sondes d’isolation de l’adaptateur | 7 refus attendus avant entrée/sortie, processus distinct |
| Inspection SQLite fichier sans écoute | READY ; gardes à zéro |
| Parcours API WSGI sur un autre fichier fictif | 43 requêtes, 7 groupes réussis ; gardes à zéro |
| Contrôle HTTP local PowerShell | 3 réponses 200 ; pas Edge |
| Parcours humain Edge | 224 requêtes, dont 164 API ; résultats partiels et défauts décrits ci-dessus |
| Observations humaines | Textes/motif visibles aux emplacements indiqués ; compte reconnu à l’accueil ; présentation des autres pages jugée trompeuse |
| Comparaisons statiques | Sources/manifestes/relations, 135 empreintes préservées, branche/HEAD/index conservés |
| Arrêt et intégrité du fichier | Processus de recette arrêté, port fermé, `integrity_check=ok`, FK sans orphelin |

Aucun cumul entre requêtes, groupes, tests et anciennes campagnes. L’analyse des en-têtes HTTP ne remplace pas l’observation humaine des libellés visibles. Aucune preuve de réussite inventée pour les étapes manquantes.

## 11. Arrêt, conservation et preuves

Le Ctrl+C envoyé à la session de lancement n’a pas arrêté l’écoute. Après vérification du PID enregistré et de son nom Python, **seul le processus 20296 est arrêté par `Stop-Process`**, sous les droits existants. La session de lancement se termine ; le processus n’existe plus et une nouvelle connexion à `127.0.0.1:5064` est refusée. Aucun autre processus, notamment Edge, arrêté. L’utilisateur peut fermer manuellement la fenêtre InPrivate de recette.

La première sonde de fermeture, limitée à une seconde, expire ; le contrôle suivant à cinq secondes constate le refus de connexion. Aucun droit supplémentaire sollicité. Après l’arrêt ciblé, la base reste lisible en lecture seule : intégrité `ok`, FK sans orphelin, zéro doublon Vote et CommentLike. Aucun fichier supprimé.

Le reçu interne `isolation.json` de démarrage n’a pas été rafraîchi lors de cette terminaison ciblée. **Il ne constitue pas une preuve d’arrêt** et ses compteurs ne sont pas annoncés comme état final du processus. L’arrêt est attesté séparément par `shutdown-verification.json`. Les compteurs zéro retenus concernent les inspections préalables ; aucune collecte finale de ces compteurs n’est inventée. Aucun snapshot SQL du suivi n’a échoué.

Preuves temporaires conservées :

```text
[chemin local privé retiré]
```

`baseline.json`, `adapter.diff`, `adapter-review.json`, scripts de préparation/observation hors dépôt, `preflight-results.json`, dossiers séparés des sondes/inspection/parcours WSGI, `http-preflight.json`, `anomaly-1/`, `edge-evidence.json`, `live-status.json`, `user-observations.json`, `shutdown-verification.json`, `preservation.json` et `final-validation.json`. Dans `portfolio-recette6g5-3il9mmcj/` : base synthétique, reçu initial, `requests.jsonl` et `latest-sql.json`.

Le suivi conserve méthodes, chemins sans paramètres, statuts et seuls ids/agrégats synthétiques ; aucun corps HTTP, cookie, CSRF, mot de passe, pseudonyme, e-mail, commentaire ou motif brut. Les empreintes et remplacements de l’adaptateur sont contrôlables. Les artefacts temporaires sont susceptibles de nettoyage par le système ; le présent rapport est permanent.

## 12. Préservation et verdict final

Les **135 fichiers préexistants contrôlés sont identiques**, dont kit/manifeste 6G.4, backend, modèles, routes, migrations, frontend, dashboard et données historiques. Le seul fichier créé dans le dépôt est ce bilan. Branche, HEAD et index conservés. État final : **48 fichiers suivis modifiés, 76 non suivis, aucun indexé**, incluant le travail antérieur. Aucun reset, commit, push, changement de branche ou suppression.

**NO-GO pour annoncer la démonstration au jury entièrement validée en l’état.** Le lien Edge → Flask → SQLAlchemy → SQLite fichier est démontré pour les opérations enregistrées ; les défauts d’état de connexion visible et de contexte de modération doivent être traités selon la décision de l’utilisateur, et les vérifications manquantes terminées.

Suite proposée à autoriser : corriger les deux interfaces ciblées sans modifier les sept statistiques, refaire les tests isolés concernés, renouveler les manifestes seulement après revue des sources modifiées, puis réaliser une courte nouvelle recette Edge autorisée. Aucun redémarrage ni correction engagés. **Arrêt après 6G.5 et attente de validation.**
