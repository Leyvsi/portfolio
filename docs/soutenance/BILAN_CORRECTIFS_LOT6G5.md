# Correctifs autorisés après la recette 6G.5

> Archive pédagogique datée : les résultats et descriptions ci-dessous concernent le lot indiqué. Les anciens repères de ligne ne décrivent pas la version candidate. Pour préparer la soutenance actuelle, consulter les quatre fiches et le référentiel reliés au sommaire.

> Copie publique de référence : les chemins personnels et liens de travail internes sont retirés. Les preuves et commandes historiques gardent leur date et leur périmètre ; utiliser le README actuel pour le lancement.

Date : 1er novembre 2026. Branche : `feature/frontend-api-integration`.

Le « oui je t’autoriser » de l’utilisateur autorise les deux corrections proposées après les anomalies de la recette : affichage du compte sur les pages et contexte des signalements. Ce document complète le [bilan historique 6G.5](BILAN_LOT6G5.md), conservé sans réécriture de ses résultats. Il ne lance pas un nouveau lot fonctionnel.

## Diagnostic et résultat attendu

L’utilisateur retrouvait son pseudo et « Déconnexion » en revenant sur l’accueil. Les requêtes `/me` restaient autorisées, sans POST de déconnexion lors des navigations observées. Les liens fixes « Connexion » des autres pages donnaient un affichage contradictoire. Le commentaire était visible dans le dossier, mais le tableau des signalements ne présentait pas son texte et son dossier/catégorie.

Le contrôle partagé de `frontend/app.js` affiche désormais le pseudo, le rôle et « Déconnexion » dans les dix pages existantes. L’administrateur conserve un accès direct au tableau. `/me` est relu sans cache au chargement, au retour depuis le cache et au focus. Un refus ou une réponse indisponible ne conserve pas une identité périmée. La déconnexion relit la session et son CSRF, bloque les doubles clics et confirme la réponse serveur. Après une réponse perdue, seule une lecture est répétée. Les réponses tardives après départ sont ignorées.

La fin ou le changement de session masque immédiatement les cartes privées et les sept valeurs du tableau. L’ancien état personnel des likes est désactivé en attendant le rechargement. Les contrôles serveur existants continuent de protéger chaque écriture.

`GET /api/v1/admin/reports`, toujours réservé aux administrateurs, joint le commentaire, son dossier et sa catégorie. Chaque réponse conserve les champs antérieurs et ajoute `comment` et `story`. Les informations sont celles des relations SQL actuelles : texte du commentaire, titre/slug, catégorie et état archivé. Une référence absente reste indisponible, sans réparation. La lecture utilise des jointures anticipées et une réponse `private, no-store` ; les créations de signalements gardent leur contrat.

`frontend/admin-dashboard.js` affiche ce contexte et le motif avec `textContent`. Une fiche active reçoit un lien encodé ; une archive renvoie à la consultation privée existante. Les données incohérentes sont refusées. Une ancienne réponse sans ces nouveaux champs affiche un contexte indisponible.

## Périmètre conservé

- Aucun modèle, schéma ou fichier de migration modifié par ces correctifs.
- Aucun changement de calcul des sept compteurs, de stockage des likes, de bannissement, d’archivage ou de suppression.
- Aucun ajout de route ou de méthode HTTP ; contrat Swagger de lecture des signalements enrichi, schéma partagé `Report` conservé.
- Aucune donnée réelle, connexion MySQL/Aiven, lecture du `.env`, automatisation CDP, élévation ou modification Windows.
- Aucun commit, push, changement de branche, suppression de fichier ou remplacement du travail antérieur.

Les dix en-têtes HTML partagent des contrôles et un message de session, sans changement d’ordre des scripts. Le CSS ajouté est limité au compte et au texte de signalement. Le kit Python 6G.4 demeure inchangé et exclusivement en mémoire. Son manifeste de 40 sources a été renouvelé explicitement après revue des corrections autorisées ; il reste vérifié au lancement et n’est jamais régénéré automatiquement.

## Cause complémentaire : anciennes ressources conservées dans Edge

Après connexion réussie, l’utilisateur ne voyait toujours pas son compte sur Histoires, mais le retrouvait dans le dossier ; il précisait que la catégorie manquait dans le signalement. Le journal montrait des données rechargées sans nouvelle lecture du HTML Histoires ni du script du tableau, et les réponses de session restaient autorisées. Le contrôle HTTP du serveur révélait `Cache-Control: public` : `SharedDataMiddleware(cache=False)` désactive ses réponses conditionnelles, mais autorise encore le stockage et le cache heuristique du navigateur.

L’utilisateur a effectué `Ctrl+F5` sur Histoires puis Administration et confirmé : « Les deux affichages sont maintenant corrects. » Les lectures HTTP des pages et scripts actualisés sont enregistrées. Les symptômes restants provenaient donc des anciennes ressources conservées ; aucune perte de session n’est attestée lors de cette navigation.

`run_local.py` remplace désormais l’en-tête des ressources frontend par `Cache-Control: no-store`, sans changer le corps des fichiers, les chemins servis ou les réponses des routes API. Un test HTTP WSGI couvre pages, scripts, styles, image et relecture avec en-têtes conditionnels : réponse 200 complète, un seul en-tête `no-store`, API déléguée inchangée. Les trois suites, le parcours intégré et le kit sont réexécutés après cette modification. Les sauvegardes antérieures de `run_local.py` et de son test sont conservées.

La session manuelle PID 2888 avait déjà chargé l’ancien middleware avant cette dernière modification. Son contrôle visuel est effectué après actualisation forcée ; le nouveau comportement `no-store` est validé par le vrai middleware en WSGI et prendra effet au prochain démarrage local. Aucun redémarrage n’est imposé au milieu des essais connectés.

## Vérifications exécutées

| Campagne actuelle | Résultat | Portée |
|---|---:|---|
| Backend | 311 PASS | Vraies routes Flask, SQLite mémoire et gardes hors ligne |
| Frontend | 513 PASS | DOM/API simulés, contrôleurs réels |
| Contrats et lanceur | 30 PASS | Contrats des dix pages et du kit, cache local et service testés sans écoute |
| Total des trois suites | **854 PASS** | Zéro échec, erreur ou test ignoré dans la campagne finale après correctif de cache |
| Intégration contrôleurs → Flask → SQL → tableau | **17 groupes PASS, 99 échanges API** | HTML et scripts réels, DOM simulé, SQLite mémoire ; aucun navigateur |
| Kit 6G.4 | PASS | Inspection, sondes séparées et parcours WSGI de 43 requêtes, sans écoute |
| Adaptateur SQLite fichier | PASS | Refus sans marqueur, sondes, inspection, parcours 43 requêtes et témoin de correctifs séparé |
| Vérification humaine des deux affichages dans Edge | **PASS après actualisation complète** | Compte sur Histoires/dossier et signalement avec catégorie confirmés par l’utilisateur |
| Like d’histoire après actualisation | **PASS** | Ajout à 1 et retrait à 0 confirmés par l’utilisateur, HTTP et SQL ; unicité conservée |
| Like de commentaire après actualisation | **PASS** | POST et DELETE réels, ligne personnelle unique à 1 puis absente à 0 après rechargement, confirmations humaines |
| Sept compteurs visibles | **PASS** | Les sept valeurs attendues sont confirmées par l’utilisateur et égales à SQL |
| Déconnexion depuis Histoires | **PASS** | POST logout 200, puis `/me` 401 ; retour de Connexion et masquage du tableau confirmés |
| Arrêt et conservation de la base | **PASS** | PID absent, port fermé, intégrité OK et FK sans orphelin, lecture seule |

Les 815 PASS de 6G.4, les 853 PASS de la première campagne corrective et les résultats Edge du bilan initial sont historiques et ne sont pas additionnés à 854. Sept tests de migrations historiques restent explicitement exclus des suites exécutées. Six essais de la migration candidate des likes sont limités à une mémoire synthétique sous garde ; ils ne constituent pas une migration MySQL.

Les nouveaux tests couvrent les rôles autorisés/refusés, les deux dossiers et catégories, archives, contexte manquant, absence de modification des dix tables, cascade isolée, erreur SQL et nombre borné de SELECT. Ils vérifient également les dix pages, erreurs `/me`, CSRF frais, double clic, réponse perdue, changement de compte, cache de navigation, déconnexion en cours au retour, texte hostile et masquage immédiat du tableau/des likes.

Une première campagne avait un échec dans un nouveau test : attente asynchrone insuffisante après un retour de cache simulé. L’attente a été corrigée et les trois suites entièrement relancées avec succès. Le premier essai du parcours intégré a rencontré une ressource manquante dans la liste autorisée du harnais (`theories-list.js`) ; cette liste a été complétée puis le parcours a réussi. Ces journaux initiaux sont conservés. Les gardes des exécutions applicatives finales comptent zéro tentative interdite ; les refus volontaires des sondes sont comptabilisés séparément.

## Nouveau contrôle manuel ciblé

L’autorisation 6G.5 permet toujours un serveur local isolé et un contrôle humain dans Edge. Un nouvel adaptateur hors dépôt crée un fichier SQLite neuf, distinct de la première recette, dans un nouveau sous-dossier temporaire. Il ne peut ouvrir que ce fichier ; les autres bases et le réseau sortant sont bloqués. Les paramètres Aiven sont vidés et `dotenv` désactivé avant import applicatif. Les FK sont activées et vérifiées avant écoute sur `127.0.0.1:5064`.

Le témoin contient deux dossiers et trois comptes fictifs. Un commentaire et son signalement sont préparés par de vraies requêtes de connexion/création/déconnexion, avec CSRF. Ce peuplement est identifié comme préparation synthétique, jamais comme action humaine Edge. Ses sept valeurs SQL sont : dossiers **2**, résolues **1**, Cold Cases **1**, utilisateurs **3**, commentaires **1**, signalements **1**, propositions en attente **0**. Aucun chiffre n’est injecté dans le tableau.

Le premier serveur de contrôle a démarré après les inspections réussies : PID **19716**, session de commande **82982**, base unique `portfolio-recette6g5-qz9uqp89/recette.sqlite3`. Il a ensuite été arrêté volontairement pour préparer un accès fictif plus lisible ; la base et les preuves sont conservées. La session de commande est terminée après l’arrêt de ce seul processus Python.

Le deuxième serveur utilise une autre base neuve : `access-repair/portfolio-recette6g5-y7t6g064/recette.sqlite3`, PID **2888**, session **21442**, exclusivement sur `127.0.0.1:5064`. Les cinq contrôles d’isolation de l’adaptateur ont réussi avant lancement. Ce serveur est maintenant arrêté après les vérifications humaines ; la base est conservée.

Parcours exécuté puis confirmé par l’utilisateur :

1. Dans Edge, ouvrir la connexion administrateur sur cette origine et faire `Ctrl+F5`. Se connecter avec le compte éphémère communiqué uniquement dans la conversation.
2. Aller sur Histoires puis ouvrir Dossier fictif 17 : vérifier le pseudo, « Administrateur » et « Déconnexion » sur chaque page, sans nouvelle connexion.
3. Aller dans Administration, section Signalements reçus : vérifier le texte fictif du commentaire, Dossier fictif 17, sa catégorie Histoires résolues et le motif. Le lien doit ouvrir le bon dossier.
4. Depuis Histoires, cliquer Déconnexion : vérifier le retour de « Connexion », puis le refus/masquage du tableau après une nouvelle consultation.

Les observations humaines, échanges Edge et états SQL sont rapprochés avant validation de ces étapes et des likes décrits ci-dessous. Les créations humaines d’inscription, commentaires et signalements appartiennent au passage initial 6G.5 ; la présente fixture ne revendique pas de nouvelles créations humaines de ces objets. Les tests automatiques restent séparés des contrôles Edge.

### Retour utilisateur et accès à la version corrigée

L’utilisateur indique que les deux anomalies persistent, puis que le serveur s’est arrêté. Lors du contrôle qui suit, le processus Python 19716 est présent et la page `http://127.0.0.1:5064/admin-connexion.html` répond HTTP 200 avec les nouveaux contrôles. Le script `app.js` corrigé a également été relu en HTTP 200. Ces requêtes techniques ne constituent pas une recette Edge.

Au premier contrôle, le journal du nouveau serveur ne contenait aucune requête Edge ni navigation HTTP humaine identifiable, seulement ses inspections WSGI et les lectures techniques de contrôle. L’adresse utilisée lors du signalement des anomalies n’a pas été établie. Les anomalies étaient alors conservées comme non résolues visuellement, sans conclure à un essai réussi de la version corrigée.

Après fourniture du lien direct vers le port 5064 et demande d’actualisation complète, de vraies requêtes Edge apparaissent : page de connexion et scripts corrigés en HTTP 200, `/me` anonyme en 401, puis plusieurs connexions refusées en 401. L’utilisateur confirme que la page s’affiche et que la connexion reste refusée. Un contrôle technique avec les identifiants temporaires, dans une session HTTP indépendante en mémoire, réussit pourtant : connexion 200, rôle administrateur, contexte du signalement correct et déconnexion 200. Ce contrôle ne valide pas le rendu Edge.

Pour faciliter l’essai humain, une nouvelle fixture fournit un accès fictif plus lisible. Un diagnostic temporaire, limité à l’adaptateur hors dépôt, conserve seulement des booléens de conformité du JSON et de correspondance de l’identifiant/mot de passe attendu, sans valeur saisie, corps HTTP ou secret. Il ne change pas l’authentification ni ses refus. La connexion, la lecture administrateur du signalement et la déconnexion de ce nouvel accès ont également réussi en HTTP technique. Les nouveaux identifiants sont uniquement communiqués dans la conversation.

L’utilisateur confirme ensuite : « Le tableau administrateur s’ouvre. » Le transport Edge confirme un POST de connexion 200, `/me` 200 et les lectures administrateur 200, dont `/admin/reports`. Les booléens du diagnostic indiquent que les deux valeurs reçues correspondent à la fixture. Ce nouvel accès est donc confirmé par l’utilisateur et le serveur. Après actualisation complète, les deux affichages sont également confirmés comme décrit plus haut. Les likes, les sept valeurs et la déconnexion sont ensuite terminés comme décrit ci-dessous.

### Rapprochement des likes Edge et SQL

L’utilisateur confirme d’abord les deux cycles à 1 après ajout/actualisation et à 0 après retrait/actualisation. Les traces corroborent immédiatement celui de l’histoire : POST `/votes/17` 201, DELETE 200, nouvelles lectures de fiche et lignes personnelles SQL respectivement présentes puis absentes, sans doublon.

Pour le commentaire, aucune écriture n’apparaissait encore à cette première confirmation. Le bouton dans la carte du commentaire a donc été désigné précisément, sans assimiler le bouton du dossier à celui du commentaire. Le nouvel essai produit un POST `/comments/1/like` 200, une ligne `CommentLike(user_id=1, comment_id=1)`, puis une nouvelle lecture de fiche avec cette ligne toujours présente. L’utilisateur confirme « 1 J’aime » et le bouton de retrait dans cette carte, puis le retrait et « 0 J’aime » après actualisation. Le DELETE 200 et une nouvelle lecture de fiche avec zéro ligne personnelle corroborent ce dernier résultat.

`access-repair/like-reconciliation.json` conserve les méthodes, statuts, séquences et nombres de lignes personnelles, ainsi que les relectures après chargement de fiche. Les objets histoire et commentaire restent vérifiés séparément ; aucune requête technique n’est présentée comme un clic Edge.

### Compteurs, déconnexion et clôture

L’utilisateur confirme les sept nombres après Actualiser dans Administration :

| Compteur | Valeur visible confirmée et valeur SQL |
|---|---:|
| Dossiers actifs | 2 |
| Histoires résolues | 1 |
| Cold Cases | 1 |
| Utilisateurs | 3 |
| Commentaires | 1 |
| Signalements | 1 |
| Propositions en attente | 0 |

Ces valeurs concernent uniquement la nouvelle base fictive ; elles ne remplacent pas celles de la recette initiale. Aucun nombre ajouté artificiellement au tableau. Les likes n’ajoutent ni commentaire ni signalement.

Depuis Histoires, l’utilisateur confirme le retour de Connexion puis le masquage des données privées dans Administration après actualisation. Le journal Edge enregistre le POST `/api/v1/logout` 200, séquence 234, puis quatre GET `/me` 401. Il s’agit d’une déconnexion volontaire réelle, antérieure à l’arrêt du serveur.

Cette dernière session totalise **200 requêtes Edge, dont 134 API** : 177 réponses 200, deux 201, six 401 et quinze 403. Les 401 correspondent aux contrôles anonymes avant connexion et après déconnexion ; les quinze 403 visent exclusivement `/favicon.ico`. Aucun 5xx Edge ni snapshot SQL en échec. Ces nombres ne sont pas additionnés aux 224 requêtes de la recette initiale, aux 22 requêtes du premier serveur correctif ou aux tests WSGI.

Après confirmation humaine, seul le processus Python de recette **2888** est arrêté, sous les droits existants. La session de commande se termine ; une vérification indépendante constate l’absence du PID et le refus de connexion au port 5064. Aucun autre processus ni fichier supprimé. La base conservée est ouverte en lecture seule : `integrity_check=ok`, FK sans orphelin, zéro doublon Vote/CommentLike, zéro ligne de like finale et compteurs historiques des commentaires toujours à zéro.

Le reçu de démarrage `isolation.json` peut encore indiquer une écoute ouverte après cette terminaison ciblée. Il ne constitue pas l’état final du serveur ; `process-absence.json` et `shutdown-verification.json` attestent l’arrêt. Les gardes à zéro annoncées concernent les inspections et tests effectivement mesurés, pas des compteurs mémoire finaux inventés.

## Preuves et verdict

Preuves hors dépôt, sans corps HTTP, cookies, CSRF ni mots de passe archivés :

`[chemin local privé retiré]`

- `baseline.json`, copies `before/` et `preservation.json` : état initial, empreintes et contrôle de périmètre.
- `attempt-1/`, `attempt-2/` : commandes, sorties et comptes exacts des trois suites.
- `integration-frontend.json`, `integration-sql.json`, `integration-exchanges.json` et gardes : 17 groupes, 99 échanges et lecture SQL.
- `kit-commands.json` et sorties : contrôles du kit en mémoire.
- `adapter-review.json`, `adapter.diff`, `file-preflight-results.json` : adaptation hors dépôt vers un fichier neuf et contrôles préalables.
- `http-smoke.json`, `user-observations.json` : contrôle HTTP technique et retour utilisateur, distincts d’une validation Edge.
- `edge-evidence.json` : échanges Edge réels et dernier état SQL, sans résultat visuel déduit du transport.
- `portfolio-recette6g5-qz9uqp89/` : isolation, témoin synthétique, requêtes minimales et états SQL de la nouvelle session locale. La base brute contient uniquement la fixture fictive et n’est pas ajoutée au dépôt.
- `first-session-stop.json`, `http-auth-check.json`, `access-repair/` : arrêt ciblé du premier serveur, authentification HTTP technique, nouvelle fixture isolée et diagnostic par booléens. Aucun identifiant ni mot de passe n’est conservé dans ces résultats.
- `cache-repair/` : manifeste relu, trois suites finales à 854 PASS, parcours intégré et kit réexécutés après le correctif `no-store`.
- `access-repair/like-reconciliation.json`, `manual-validation.json`, `stop-receipt.json`, `process-absence.json`, `shutdown-verification.json` : rapprochement final, confirmations humaines, arrêt ciblé et intégrité.

**GO pour la démonstration locale isolée des parcours recettés.** Les deux défauts d’interface sont corrigés et confirmés après actualisation, les deux cycles de likes persistent après rechargement, les sept compteurs correspondent à SQL et la déconnexion masque les données privées. Les blocages fonctionnels visés par cette contre-recette sont levés. Le bilan initial reste un instantané historique avec son NO-GO d’alors.

Ce verdict repose sur la recette initiale et la contre-recette complémentaire, avec 854 tests actuels distincts des vérifications humaines. Il ne certifie pas un déploiement, MySQL/Aiven ou les migrations réelles, ni les parcours supplémentaires non exercés dans Edge (accessibilité complète, charge/concurrence, archivage/restauration et erreurs réseau/CSRF provoquées). Le nouveau `no-store` a été testé avec le vrai middleware en WSGI et sera actif au prochain démarrage ; la recette humaine a utilisé l’actualisation complète. Serveur arrêté, preuves conservées, aucun commit ou push. Arrêt après 6G.5, sans nouveau lot engagé.
