# Les Petits Enquêteurs — Frontend

Interface HTML, CSS et JavaScript, sans compilation frontend. La configuration du backend et l'installation sont décrites dans le [README principal](../README.md).

## Pages

| Page | Fonction |
|---|---|
| [index.html](index.html) | Accueil : jusqu'à trois dossiers et contrôle de session avec déconnexion |
| [histoires.html](histoires.html) | Histoires résolues ; recherche locale dans les titres et résumés |
| [coldcases.html](coldcases.html) | Dossiers non résolus |
| [dossier.html](dossier.html) | Lecture d'un dossier par le paramètre `?slug=…` |
| [connexion.html](connexion.html) | Connexion membre |
| [admin-connexion.html](admin-connexion.html) | Connexion et contrôle du rôle administrateur |
| [inscription.html](inscription.html) | Création d'un compte, puis connexion séparée |
| [proposer-histoire.html](proposer-histoire.html) | Proposition d'histoire par un membre connecté |
| [theories.html](theories.html) | Création d'une théorie et consultation publique par dossier |
| [admin-dashboard.html](admin-dashboard.html) | Consultation et recherche des dossiers, compteurs, propositions/signalements et gestion des utilisateurs |

## Scripts et présentation

| Fichier | Responsabilité |
|---|---|
| [styles.css](styles.css) | Présentation commune, grilles responsive et cadrage des images |
| [api.js](api.js) | Requêtes JSON sous `/api/v1`, cookies, CSRF, validation des réponses et erreurs |
| [app.js](app.js) | Cartes, recherche, dossiers, images, inscription, connexion, session et formulaires de contribution |
| [theories-list.js](theories-list.js) | Lecteur public des théories, sélection indépendante et actualisation |
| [admin-users.js](admin-users.js) | Liste des comptes, confirmation du bannissement, statut serveur et réponses incertaines |
| [admin-stories.js](admin-stories.js) | Recherche et filtres locaux des dossiers déjà chargés, catégories inconnues et liens de détail |
| [admin-dashboard.js](admin-dashboard.js) | Vérification du rôle, sept compteurs et coordination des panneaux privés |
| [donnees.js](donnees.js) | Ancien jeu de données public conservé depuis main ; aucune page active ne le charge depuis 6G.4 |

`donnees.js` n'est ni une base de données, ni un repli automatique lorsque l'API échoue. Les interfaces raccordées utilisent l'API ; une erreur produit un message.

Les cinq anciennes balises ont été retirées après analyse locale sans exécution : inscription, connexion, connexion administrateur, proposition et théories. Le [protocole 6G.4](../docs/soutenance/RECETTE_MANUELLE_LOT6G4.md) utilise un nouveau kit avec `likes.js` et SQLite mémoire, sans lecture de configuration privée. Lancement serveur et Edge manuel sous autorisation distincte.

## Archivage et restauration — lot 6C, phase 1

**Extension actuelle 6C.2 :** un bouton Supprimer définitivement est proposé seulement pour les archives. Un dialogue natif affiche les nombres de contributions/signalements, exige le titre complet et une case d’accord. La confirmation serveur précède le DELETE conditionnel ; doubles soumissions verrouillées jusqu’à la relecture. Une réponse perdue ne déclenche aucune seconde suppression. Sans reçu persistant, le message distingue succès reconnu, présence/absence constatée et état non vérifié. Un succès reconnu n’est pas transformé en « rollback » si les statistiques deviennent indisponibles. Voir le [bilan 6C.2](../docs/soutenance/BILAN_LOT6C2_IMPLEMENTATION.md).

Le tableau ajoute un filtre Actifs / Archives / Tous, un statut et une confirmation native avant Archiver ou Restaurer. Les titres et contributions restent du texte (`textContent`). Les archives s’ouvrent par une lecture administrative ; leur lien public est retiré. L’action verrouille les soumissions jusqu’à la relecture globale des listes et compteurs. Une réponse incertaine déclenche cette relecture, sans retry du POST ; si elle échoue, les données et actions sont masquées et les compteurs affichent `—`. Le focus revient sur Actualiser.

`getAdminStories` lit `GET /admin/stories?state=archived`, `getAdminStory` lit `GET /admin/stories/{story_id}` et `changeAdminStoryArchive` appelle les POST `archive` / `restore`. La liste publique reste la source des trois compteurs de dossiers actifs ; les quatre autres compteurs conservent leur définition et le nombre d’archives est séparé. Les filtres de titre et catégorie restent locaux. Les réponses anciennes et pertes d’accès nettoient aussi les archives.

L’archivage conserve les données pour une restauration ; la suppression définitive reste à développer. Voir le [bilan 6C phase 1](../docs/soutenance/BILAN_LOT6C_PHASE1.md). Clavier et responsive sont vérifiés par structure native et DOM simulé ; aucune nouvelle recette navigateur réel n’est revendiquée.

Les pages chargent `api.js` avant `app.js`, puis leur éventuel script spécialisé. Le tableau charge `admin-users.js` et `admin-stories.js` avant `admin-dashboard.js`, qui instancie et nettoie les deux panneaux.

## API et sécurité

**Actualisation 6G.2 :** les fiches histoires/Cold Cases et chaque commentaire compatible disposent de J’aime / Retirer mon J’aime, compteur réel et état personnel. Voir le [bilan et les limites](../docs/soutenance/BILAN_LOT6G2.md). Les sections historiques ci-dessous conservent leur contexte de livraison.

Les pages et l'API doivent partager la même origine. `api.js` utilise `fetch` avec `credentials: 'include'`, un délai de 10 secondes par défaut et des messages d'erreur. Il ne répète pas automatiquement les soumissions.

| Usage de l'interface | Routes |
|---|---|
| Listes et fiche | `GET /api/v1/stories` ; `GET /api/v1/stories/slug/{slug}` |
| Compte et session | `POST /api/v1/users` ; `POST /api/v1/login` ; `GET /api/v1/me` ; `POST /api/v1/logout` |
| Proposition | `POST /api/v1/proposals` |
| Théories | `GET` et `POST /api/v1/stories/{story_id}/theories` |
| Commentaires sur un dossier | `GET` et `POST /api/v1/stories/{story_id}/comments` |
| Signalement d'un commentaire | `POST /api/v1/comments/{comment_id}/report` |
| J’aime d'une histoire/Cold Case | `GET`, `POST`, `DELETE /api/v1/votes/{story_id}` |
| J’aime d'un commentaire | `GET`, `POST`, `DELETE /api/v1/comments/{comment_id}/like` |
| Consultation administrateur | `GET /api/v1/stats` ; `GET /api/v1/stories` ; `GET /api/v1/proposals` ; `GET /api/v1/admin/reports` |

La session repose sur le cookie signé de Flask : `HttpOnly`, `SameSite=Lax`, et `Secure` configurable selon HTTP local ou HTTPS. Le jeton CSRF obtenu à la connexion ou via `/me` reste en mémoire JavaScript ; il accompagne les écritures authentifiées dans `X-CSRF-Token`, sauf la connexion. Aucun stockage d'authentification dans `localStorage` ou `sessionStorage` n'est utilisé.

Le backend vérifie les comptes, leur état et les permissions. Le contrôle JavaScript du rôle ne remplace pas cette autorisation serveur. Les contenus externes affichés utilisent `textContent`.

## J’aime individuels — lot 6G.2

`dossier.html` charge `api.js`, `likes.js`, `comments.js`, puis `app.js`. Le contrôleur commun affiche les compteurs publics (`votes` de Story, `likes` de Comment), puis lit `/me` et l'état personnel pour activer le bouton. Un visiteur voit le compte mais doit se connecter pour agir. Aucun nombre n'est augmenté/diminué par supposition dans le DOM.

Chaque action vérifie à nouveau session/état, envoie un seul POST ou DELETE avec CSRF puis relit le serveur. POST histoire exige 201, POST commentaire 200, doublon 409 ; DELETE 200 est idempotent. Un compte changé provoque une relecture sans action. Double clic bloqué dès `/me`, réponses tardives ignorées au départ, aria-pressed et bouton natif. Les brouillons et cibles des signalements restent conservés pendant les likes.

Une réponse perdue peut suivre un commit : résultat incertain, Vérifier les J’aime relit sans renvoyer ; aucune nouvelle écriture sur ce contrôle pendant cette instance de page. Ce verrou ne persiste pas au rechargement complet. Un succès confirmé suivi d'une panne de lecture reste distingué d'un échec d'écriture.

Les likes de commentaires sont enregistrés dans CommentLike ; le compteur historique physique reste inchangé. Un historique non nul/invalide affiche une information distincte et bloque les actions (409 côté API). Aucune conversion silencieuse. Les votes historiques restent dans Vote. Les likes de théories gardent leur comportement antérieur. Dashboard et sept indicateurs inchangés ; aucun navigateur réel validé.

## Commentaires et signalements — lot 6F.1

La fiche `dossier.html?slug=...`, commune aux histoires et Cold Cases, charge `api.js`, `comments.js`, puis `app.js`. Après résolution du dossier réel, `app.js` démarre le panneau de commentaires. Sa lecture est publique ; **Actualiser les commentaires** relit l'API. Aucune donnée narrative locale ne remplace une erreur serveur.

**Publier le commentaire** vérifie `/me`, récupère son CSRF puis envoie seulement `text`. Le texte et le motif de signalement sont obligatoires, limités à 65 535 octets UTF-8 après retrait des espaces aux extrémités ; le backend revalide. L'auteur du commentaire est déduit de la session. Un HTTP 201, un statut `success` et une réponse cohérente sont nécessaires avant affichage confirmé et effacement de la saisie.

**Signaler** sélectionne un commentaire de la liste et affiche sa cible. L'utilisateur saisit le motif puis clique **Confirmer le signalement** ; seul `reason` est envoyé sur la route de ce commentaire. Annuler n'enregistre rien. Le retour doit confirmer exactement `type: "comment"` et le `target_id` sélectionné. Aucun signalement d'histoire, accès public aux motifs administratifs ou masquage automatique du commentaire. Le backend autorise plusieurs signalements ; aucune règle de doublon n'est inventée.

Les notices précisent commentaire/pseudonyme publics et motif destiné à l'administration, sans publier la politique incomplète. Tous les textes restent du texte DOM. Les doubles clics sont bloqués dès `/me` et pendant le POST, sans retry. Un résultat incertain conserve le brouillon et bloque les nouveaux envois du même type sur cette page : relire les commentaires ou faire vérifier le signalement par l'administration avant tout nouvel envoi. Le verrou ne survit pas à un rechargement complet. Aucune table de reçus ni stockage navigateur ajouté.

[Bilan et limites 6F.1](../docs/soutenance/BILAN_LOT6F1.md) : 723 PASS, dont 64 nouveaux tests frontend ; navigateur réel et MySQL non vérifiés. Dashboard et sept compteurs conservés.

## Propositions et théories

Les deux formulaires vérifient la session et récupèrent un CSRF à jour via `GET /api/v1/me` avant l'envoi. Ils transmettent `title` et `content` en JSON : titre obligatoire de 200 caractères maximum, contenu obligatoire limité à 65 535 octets UTF-8.

- **Proposition** : la catégorie choisie est conservée au début du contenu sous la forme « Catégorie proposée : Histoire » ou « Catégorie proposée : Cold case ». Cette métadonnée compte dans la limite UTF-8. Le backend enregistre la proposition en `pending` ; aucune pièce jointe ni publication automatique n'est prévue.
- **Théorie** : le dossier provient des identifiants numériques renvoyés par l'API. La création est liée à ce dossier et devient consultable sans étape de modération.

Le succès exige une réponse HTTP 201 avec un JSON lisible. La saisie est conservée en cas d'échec et les doubles soumissions sont bloquées pendant l'envoi.

Le lecteur « Théories publiées » est accessible sans connexion. Son sélecteur est indépendant de celui du formulaire. Il affiche titre, contenu et date, gère chargement, liste vide, erreur et dossier introuvable, et ignore les réponses devenues obsolètes. Le bouton **Actualiser** recharge la sélection ; une création ne déclenche pas de rechargement automatique du lecteur.

## Administration et bannissement

Au chargement et avec **Actualiser**, le tableau vérifie `GET /api/v1/me` et exige `user.is_admin === true`. Il charge ensuite les statistiques, les histoires, les propositions et les signalements.

Les compteurs de dossiers et leur répartition sont calculés depuis les histoires ; les nombres d'utilisateurs, commentaires et signalements viennent de `/stats`, une route publique. Les lectures des propositions et signalements sont protégées côté serveur.

Les données sont effacées à réception de HTTP 401/403, lorsque la page est quittée et dès que le contrôle partagé signale une fin ou un changement de session. Ce contrôle relit `/me` au chargement, au retour depuis le cache et à la reprise de focus ; il ne fonctionne pas par interrogation périodique. Le fichier HTML reste accessible publiquement, sans donner accès aux données protégées.

Le panneau utilisateurs affiche pseudo, rôle et statut, sans email. Seuls les comptes ordinaires actifs proposent **Bannir cet utilisateur**. Une confirmation indique que compte et contributions sont conservés. Les administrateurs sont protégés côté serveur (409), y compris contre leur propre bannissement.

La liste vient de `GET /api/v1/users` ; le bouton utilise `POST /api/v1/admin/users/{user_id}/ban`, avec session et CSRF. L’ancienne route DELETE par pseudo reste compatible et applique la même règle. Les 401/403 effacent aussi ce panneau ; un 409 reste un message métier.

Pendant l’action, les doubles clics sont bloqués. Après succès ou réponse incertaine, la liste est relue sur le serveur, sans répétition automatique du POST. Si cette relecture échoue, aucune ancienne carte n’est réaffichée ; utiliser **Actualiser les utilisateurs**. La consultation des dossiers est ajoutée en 6B ; aucun débannissement, édition, suppression, archivage ou publication n’est proposé.

## Propositions en attente — lot 6D

Les **sept indicateurs** sont dossiers, histoires résolues, Cold Cases, utilisateurs, commentaires, signalements et propositions en attente. Le dernier est calculé dans `displayData` depuis la réponse administrative déjà validée de `getAdminProposals`, avec le statut exact `pending`. Aucun autre statut textuel n'est assimilé à une attente ; les cartes des autres statuts restent visibles.

`clearData` remet aussi ce compteur à `—`. `0` signifie une liste reçue et validée sans proposition en attente ; une erreur de réseau, HTTP ou JSON affiche l'erreur globale et masque les données. Les versions, AbortController, 401/403, départ de page et contrôle après retour protègent les sept valeurs. La grille responsive existante est réutilisée sans changement de CSS.

Les filtres 6B et les actions 6A conservent leur fonctionnement. Les chiffres reflètent le dernier chargement global : une action de bannissement ne recalcule pas ces agrégats. Le tableau ne surveille pas la session en continu. Les listes sont sans pagination ; une future pagination imposerait de revoir ce total.

**318 tests frontend**, **235 backend**, **8 lanceur**, soit **561 réussites** dans la campagne 6D. Les 533 du lot 6B restent historiques. La [fixture propositions](tests/fixtures/admin-proposals.json) est comparée à la réponse réelle Flask en mémoire. Voir le [bilan 6D](../docs/soutenance/BILAN_LOT6D.md). Edge, rendu responsive et clavier réels sont **NON EXÉCUTÉS**, la recette 6A/6B reste reportée et aucune VM n'est préparée.

## Images

Les cartes et fiches essaient successivement `image_url`, l'illustration locale associée au slug, puis le SVG de remplacement. Si toutes les sources échouent, « Image indisponible » est affiché. Les cinq ressources locales et leurs règles d'affichage sont documentées dans le [README des images](images/README.md).

## Lancement local

Depuis la racine, après installation et configuration selon le README principal :

```powershell
.\.venv\Scripts\python.exe -B run_local.py
```

Ouvrir `http://127.0.0.1:5000/` ; arrêter avec **Ctrl+C**. Le lanceur sert les pages et l'API dans un seul processus, sans debug ni reloader. Il ne crée aucune donnée et n'exécute aucune migration. Ouvrir directement les fichiers HTML ne raccorde pas l'API.

## Tests frontend

Depuis la racine, avec Node.js 24 comme dans la campagne de référence :

```powershell
# Après revue du harnais 6D et de son manifeste incluant les deux fixtures :
& .\.venv\Scripts\python.exe -I -B (Join-Path $preuves6d 'run-checks.py') --only=frontend
```

Les tests de [frontend/tests](tests/) utilisent des DOM et API simulés. Ils couvrent les images, contributions, validations, CSRF, erreurs, doubles soumissions, lecteur public et accès administrateur. Ils ne vérifient pas un navigateur réel ni MySQL Aiven. Les journaux du 29 octobre 2026 confirment **226 réussites** (étape 2). Les parcours ultérieurs dans Edge réel constituent une autre campagne : ils ne changent pas la nature simulée de cette suite. Les [tests, commandes, preuves et limites](../docs/soutenance/TESTS_ET_VALIDATION.md) les présentent séparément ; l’étape 5 ne les relance pas.

## Limites actuelles

- Catégories associées directement aux identifiants `1` (histoires résolues) et `2` (Cold Cases).
- Listes sans pagination et actualisation manuelle du lecteur et du tableau administrateur.
- Les commentaires, signalements et likes individuels de dossiers/commentaires sont raccordés depuis 6F.1/6G.2 ; les likes de théories restent accessibles uniquement par API. Le bannissement des utilisateurs ordinaires est disponible depuis le lot 6A.
- Aucun téléchargement d'image, récupération de mot de passe ou traitement des propositions dans l'interface.
- Ancien libellé « Voir la maquette du tableau de bord » encore présent dans `admin-connexion.html`, malgré le raccordement réel du tableau.

## Réviser pour le jury

Consulter l’[index des fonctions après commentaires](../docs/soutenance/INDEX_CODE_JURY.md), la [démonstration](../docs/soutenance/DEMONSTRATION.md) et les [explications de sécurité/RGPD](../docs/soutenance/ARCHITECTURE_SECURITE_RGPD.md). Les commentaires français expliquent DOM, fetch, session/CSRF et réponses tardives. Les étapes 5/5.1 ne modifiaient que les commentaires ; le lot 6A ajoute le fonctionnement autorisé de gestion des utilisateurs.

## Complément de soutenance 5.1

Les [réponses orales](../docs/soutenance/ORAL_JURY.md) expliquent le DOM, les requêtes tardives et la distinction entre stockage des images, service HTTP local et hébergement de production. Le [suivi du jury](../docs/soutenance/SUIVI_REMARQUES_JURY.md) sépare les fonctions présentes des demandes restantes. Les corrections Mermaid de source restent sans nouveau rendu visuel.

## Résultat du lot 6A — 30 octobre 2026

Les **258 tests frontend** passent, dont 32 nouveaux cas du panneau utilisateurs. Avec 221 backend et huit lanceur, le bilan consolidé est de **487 réussites**. Les 226 réussites du 29 octobre restent historiques. Voir les [commandes, gardes et preuves](../docs/soutenance/BILAN_LOT6A.md). Aucun navigateur réel n’a été lancé pour ce lot.

## Dossiers administrateur — lot 6B

Le panneau affiche titre et catégorie, recherche uniquement dans le titre et combine cette recherche avec Tous / Résolues / Cold Cases / Autres. Le filtre Autres apparaît si nécessaire. `GET /stories` fournit `category_id`, pas un nom : les ids 1/2 utilisent le classement existant de `app.js` ; toute autre valeur entière est indiquée comme inconnue avec son id, sans catégorie inventée.

Les liens encodent le slug exact dans la fiche existante. Un slug textuel inutilisable ne produit aucun lien et affiche une explication ; une réponse API non conforme est refusée par la validation existante. Les filtres restent en mémoire et ne changent ni compteurs ni données. **Actualiser** recharge le tableau, réinitialise recherche et filtre et conserve la gestion des utilisateurs. Un 401/403 ou un départ de page efface les deux panneaux.

Les contrôles natifs sont libellés, désactivés pendant le chargement et associés à un message vivant ; la grille responsive existante est réutilisée. Les droits des API publiques et privées restent distincts. Aucun CSS, modèle, route ou contrat n’est modifié.

Bilan : **298 tests frontend**, **227 backend** et **8 lanceur**, soit **533 réussites**. La fixture partagée est comparée exactement à la vraie réponse Flask dans SQLite mémoire. Les données et catégories réelles de production ne sont pas consultées ; aucun navigateur réel lancé. Voir le [bilan 6B](../docs/soutenance/BILAN_LOT6B.md) et ses commandes protégées.

## Lot 6E.2 — information provisoire et politique non publiée

Les formulaires d'inscription, de théorie et de proposition affichent une notice avant les champs. Le formulaire et son bouton d'envoi référencent cette notice par aria-describedby. Aucun champ, validation, script applicatif, consentement obligatoire ou traceur ajouté. Les liens et contrôles natifs restent utilisables au clavier ; la recette réelle avec lecteur d'écran ou navigateur reste distincte des contrôles statiques.

La politique publique de confidentialité reste à finaliser après les décisions juridiques nécessaires. Les notices présentes décrivent les mécanismes applicatifs ; elles ne constituent pas une conformité RGPD définitive. Aucun document interne de préparation n’est distribué avec cette version candidate.

Commentaires et signalements : leurs API existent, mais aucun formulaire public correspondant n'est ajouté. Les [textes préparés](../docs/soutenance/BILAN_LOT6E2.md#notices-pour-les-formulaires-non-existants) restent internes jusqu'à une intégration autorisée. La procédure de droits (archive interne non diffusée) prépare le circuit manuel, sans route d'effacement/export.

Les sept compteurs, gestion/bannissement, consultation/recherche/filtres, archivage/restauration et purge restent inchangés. Les chiffres doivent venir des interactions réelles ; aucune fixture des tests n'est injectée dans la base du site. Voir le [bilan 6E.2 et les limites de validation](../docs/soutenance/BILAN_LOT6E2.md).

## Correctifs autorisés après la recette 6G.5

Les dix pages partagent maintenant le même affichage de compte dans `app.js` : pseudo, rôle, déconnexion et accès au tableau pour l’administrateur. L’état vient de `/me` sans cache. La déconnexion vérifie la session et le CSRF, bloque le double clic et exige une confirmation serveur ; une réponse perdue entraîne une relecture sans second POST. Un état indisponible affiche une vérification explicite. La déconnexion masque immédiatement les données privées du tableau et désactive l’ancien état personnel des likes jusqu’à rechargement.

Chaque signalement affiche le commentaire concerné, le titre du dossier, sa catégorie issue de la relation SQL et le motif. Le lien vers la fiche utilise un slug encodé ; une archive dirige le lecteur vers la consultation privée existante. Les textes passent par `textContent`. Un contexte absent est indiqué sans attribution inventée. Les sept calculs du tableau restent identiques.

**513 tests frontend, 311 backend et 30 contrats/lanceur réussis**, soit **854** après le correctif de cache local. L’utilisateur confirme les deux affichages dans Edge après `Ctrl+F5` sur Histoires et Administration, les deux cycles de likes après actualisation, les sept compteurs et la déconnexion avec masquage des données privées. Le serveur local utilisera `Cache-Control: no-store` pour les ressources frontend à son prochain démarrage ; un ancien cache nécessite cette actualisation initiale. Le [bilan des correctifs](../docs/soutenance/BILAN_CORRECTIFS_LOT6G5.md) distingue tests, intégration et recette humaine, conclut au GO pour les parcours démontrés en local isolé et consigne l’arrêt du serveur.

## Préparation de livraison 6H.1

Utiliser les [supports courants](../docs/soutenance/SUPPORT_JURY_LOT6H1.md) et le [guide sur un autre PC](../docs/soutenance/LANCEMENT_AUTRE_PC_LOT6H1.md). Les anciens résultats et limites restent datés ; le contrôle documentaire 6H.1 ne relance ni les 854 tests ni Edge.
