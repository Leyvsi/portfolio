# Réponses courtes au jury

> Etat de diffusion scolaire du 3 novembre 2026 : suivre le [guide actuel](../../LIVRAISON_SCOLAIRE.md) et la [validation scolaire](VALIDATION_SCOLAIRE.md). Les sections de campagnes anterieures et leurs commandes sont historiques ; elles ne remplacent pas la procedure actuelle. Les chemins sous `C:\chemin\utilisateur` sont des exemples anonymises. Les archives internes signalees sont conservees localement.

## État courant — 2 novembre 2026

Lire d’abord les [supports 6H.1](SUPPORT_JURY_LOT6H1.md), l’[index courant](INDEX_CODE_LOT6H1.md) et la [procédure sur un autre PC](../../LIVRAISON_SCOLAIRE.md). Le bilan actuel distingue **854 tests historiques**, recette Edge réussie en SQLite fictif et contrôles documentaires de ce lot. Le modèle actuel contient dix tables et treize FK ; le compte est partagé sur dix pages, les signalements sont contextualisés, les likes de dossier/commentaire sont individuels.

Les compléments et questions ci-dessous conservent leur contexte historique. Les anciennes mentions de fonctions absentes, de neuf tables ou de recette non exécutée ne constituent pas l’état courant. Les 76 questions/réponses historiques restent conservées. Aucun résultat MySQL ou de déploiement n’est ajouté.


[Sommaire](README.md) · Repères exacts du code (archive interne non livree) · [Tests et commandes](TESTS_ET_VALIDATION.md)

Ces réponses complètent les 76 questions historiques conservées dans les fiches de l'équipe. Elles correspondent aux remarques de l'examen blanc et aux preuves du 29 octobre 2026. Dire « vérifié dans les sources » lorsqu'aucune exécution n'est attestée. Les compléments 5.1 ci-dessous ne constituent pas de nouvelles campagnes ; voir le [suivi du jury](SUIVI_REMARQUES_JURY.md).

## 1. Quelle est l'architecture de votre site ?

« Le navigateur exécute HTML, CSS et JavaScript. Il demande des données JSON à l'API Flask. SQLAlchemy permet au backend de lire et écrire dans la base choisie. En local, `run_local.py` sert l'interface et l'API dans un même processus. SQLite est un moteur embarqué ; MySQL est une autre cible serveur. »

Montrer [run_local.py](../../run_local.py), [la configuration Flask](../../backend/index.py) et le [diagramme d'architecture](../../README.md#architecture).

## 2. Qu'est-ce qu'une API REST ?

« C'est une interface HTTP organisée autour de ressources et de méthodes. Ici, GET lit des dossiers, POST crée par exemple une théorie, et les réponses utilisent JSON et des codes HTTP. Notre API utilise une session par cookie : je ne prétends pas qu'elle respecte une absence totale d'état serveur au sens strict de REST. »

Montrer [les routes de théories](../../backend/api/v1/views/theories.py) et le [contrat OpenAPI](../../backend/api/v1/swagger.json). La session par cookie est signée côté client ; elle reste un mécanisme de contexte d'authentification entre requêtes.

## 3. Qu'est-ce que le DOM ?

« C'est l'arbre d'objets représentant la page dans le navigateur. JavaScript y retrouve les formulaires, crée des cartes et modifie les textes sans recharger toute la page. Nous utilisons notamment `createElement`, `textContent` et `replaceChildren`. »

Montrer `makeCard` dans [app.js](../../frontend/app.js) et `theoryCard` dans [theories-list.js](../../frontend/theories-list.js).

## 4. Comment circulent les données ?

« Une saisie déclenche submit. JavaScript valide, vérifie la session puis envoie du JSON avec fetch. Flask contrôle CSRF, compte, permissions et champs, puis SQLAlchemy valide la transaction. Le statut et le JSON reviennent au navigateur qui actualise le DOM ou affiche l'erreur. »

Montrer [le flux](../../README.md#parcours-dune-théorie), [app.js](../../frontend/app.js), [apiRequest](../../frontend/api.js) et [post_theory](../../backend/api/v1/views/theories.py).

## 5. Comment les mots de passe sont-ils protégés ?

« Nous stockons le hachage salé produit par Werkzeug, pas le mot de passe brut. `check_password_hash` vérifie ensuite une saisie. Ce n'est pas un chiffrement que nous pourrions inverser. Le hash n'entre pas dans les représentations JSON publiques du compte. Cela ne dispense pas de HTTPS et d'autres protections en déploiement. »

Montrer `User.set_password`, `User.check_password` et `User.to_dict` dans [models.py](../../backend/models.py).

## 6. Qu'est-ce qu'une attaque CSRF ?

« Une autre page essaie de faire envoyer une action par un navigateur déjà connecté. Nous exigeons un jeton lié à la session dans X-CSRF-Token pour les écritures authentifiées. Le serveur le compare et refuse un jeton absent ou invalide en 403. Login est exempté, ainsi que ce filtre pour les requêtes anonymes ; les permissions restent contrôlées par les routes. »

Montrer `protect_session_requests_from_csrf` dans [index.py](../../backend/index.py) et l'ajout de l'en-tête dans [api.js](../../frontend/api.js). Voir les [exceptions exactes](ARCHITECTURE_SECURITE_RGPD.md#csrf--comportement-exact-et-exceptions).

## 7. Comment fonctionne la session Flask ?

« Après vérification du mot de passe, Flask prépare un cookie signé qui permet de retrouver user_id. Signé ne signifie pas chiffré. HttpOnly empêche sa lecture directe par JavaScript ; SameSite vaut Lax et Secure est configurable. Pour les routes protégées, nous relisons le compte et son rôle en base. Logout efface la session du navigateur. »

Montrer `login_user`, `get_current_user`, `logout_user` dans [index.py](../../backend/index.py) et [permissions.py](../../backend/api/v1/views/permissions.py). Ne pas promettre une révocation centralisée de toutes les copies du cookie.

## 8. Comment votre base est-elle organisée ?

« Neuf tables séparent comptes, catégories, dossiers, théories, commentaires, votes, propositions, signalements et mises à jour. Chaque table a une clé primaire. Dix clés étrangères relient les lignes, et des contraintes empêchent les doublons, notamment le couple utilisateur/dossier pour les votes. target_id des signalements est une chaîne contrôlée par l'API, sans clé étrangère SQL. »

Montrer [le diagramme relationnel](../../README.md#schéma-relationnel) et [models.py](../../backend/models.py).

## 9. Quel est le rôle de SQLAlchemy ?

« SQLAlchemy fait correspondre les classes Python aux tables et traduit nos requêtes en SQL pour le moteur choisi. Sa session prépare et regroupe les écritures dans une transaction. Cela facilite l'accès aux données, mais ne remplace ni les contraintes de la base, ni la validation, ni les migrations. »

Montrer la requête `Theory.query.filter_by` et `db.session.add` dans [theories.py](../../backend/api/v1/views/theories.py).

## 10. Quelle est la différence entre commit et rollback ?

« Add prépare l'objet. Flush envoie les écritures SQL dans la transaction ; commit la valide. Rollback annule ce qui n'a pas été validé et remet la session en état après une erreur. À l'étape 4, une vraie erreur d'unicité après flush a permis de vérifier qu'aucune écriture partielle ne restait. »

Montrer [create_proposal](../../backend/api/v1/views/proposals.py) et le scénario [BDD-07](TESTS_ET_VALIDATION.md#5-étape-4--base-fichier-transactions-et-persistance-réelle).

## 11. Comment prouvez-vous la persistance d'une théorie ?

« Je ne me limite pas au message de succès. Après l'envoi réel du formulaire dans Edge, je vérifie le POST 201, relis l'objet par l'API puis ses champs dans SQLite sur une autre connexion. Après arrêt et redémarrage du serveur, je retrouve le même identifiant, auteur et contenu. La reprise utilisait une session fictive signée, sans nouvelle validation du mot de passe. »

Montrer les [preuves BDD-09/BDD-10 et Edge](TESTS_ET_VALIDATION.md#5-étape-4--base-fichier-transactions-et-persistance-réelle) et l'index vers `post_theory`.

## 12. Quels tests avez-vous réalisés, avec quels outils et commandes ?

« Le 29 octobre, 205 tests backend passent avec unittest, Flask et SQLite mémoire ; 226 tests frontend passent avec node:test et DOM/API simulés ; huit tests vérifient le middleware avec un client WSGI. Total : 439, sans échec. Les commandes passent par python-offline-bootstrap.py avec backend ou launcher, et node --require du garde --test --test-isolation=none. Les argv complets et journaux sont archivés. »

Montrer [les commandes et inventaires](TESTS_ET_VALIDATION.md#3-étape-2--439-tests-automatiques-réussis). Préciser que les campagnes Edge et SQLite fichier sont distinctes, sans les ajouter aux 439.

## 13. Quels tests ont été effectués dans un vrai navigateur ?

« Edge réel a été piloté par DevTools/CDP. L'étape 3 valide navigation, connexions, sessions et consultations : 28 PASS, deux scénarios Swagger incomplets et sept non exécutés. L'étape 4 ajoute les formulaires et la persistance sur une autre SQLite. Ce sont des tests automatisés dans un vrai navigateur, pas une recette humaine complète ni une validation sur téléphone physique. »

Montrer [les bilans séparés](TESTS_ET_VALIDATION.md#4-étape-3--véritable-edge-consultation-et-sessions) et leurs limites.

## 14. Quelle est la différence entre SQLite et MySQL ?

« SQLite est embarqué et peut stocker la base dans un fichier local. MySQL fonctionne comme un serveur distinct, éventuellement hébergé chez Aiven. Les dialectes, types, collations et comportements sous concurrence peuvent différer. Nos réussites SQLite ne prouvent donc pas MySQL/Aiven. Aucun accès Aiven ni migration Alembic n'a été exécuté pendant ces campagnes. »

Montrer le choix de moteur dans [index.py](../../backend/index.py), les [modèles](../../backend/models.py) et les [migrations](../../migrations/versions/), lues seulement.

## 15. Quelles fonctionnalités manquent encore ?

« Le tableau consulte les données et permet de bannir les comptes ordinaires, avec protection de tous les administrateurs. Il permet aussi de rechercher et consulter les dossiers depuis 6B, mais pas de les éditer, archiver ou supprimer, ni de publier les propositions. Les propositions restent pending ; les commentaires, votes, likes et signalements sont seulement dans l'API. Il manque aussi récupération de mot de passe, pièces jointes, pagination et traitement complet des demandes RGPD. Les migrations et MySQL restent à vérifier séparément. Nous distinguons une fonction absente d'une fonction présente mais non validée. »

Montrer [la fiche de démonstration](DEMONSTRATION.md#disponible-partiel-et-restant) et [le constat RGPD](ARCHITECTURE_SECURITE_RGPD.md#demandes-rgpd-du-jury--existant-et-travail-restant).

## 16. Où sont stockées et servies les images, et pourquoi ce choix ?

« Nos quatre illustrations WebP et le SVG de remplacement sont des fichiers de frontend/images, suivis dans le dépôt. Story.image_url stocke une référence, pas l'image binaire. Le navigateur essaie l'image de l'API, l'illustration locale liée au slug, puis le SVG. Si tout échoue, il affiche un texte.

Pour le petit catalogue actuel, ce choix permet de livrer les visuels avec le site, sans système d'upload ni stockage supplémentaire. Il faut redéployer les fichiers pour modifier ces illustrations. WebP convient à ces visuels compressés ; les dimensions communes et les replis facilitent un affichage cohérent.

En local, Git ne sert pas les images : SharedDataMiddleware lit les fichiers et répond par HTTP. En production, un hébergement doit publier ces ressources ; un serveur web ou un stockage d'objets avec éventuellement un CDN seraient des possibilités à choisir. Aucun fournisseur ni déploiement de production n'est confirmé ici. Les URL d'images de l'API peuvent aussi pointer ailleurs. La provenance et les droits des illustrations restent à confirmer par l'équipe. »

Montrer `Story.image_url` dans [models.py](../../backend/models.py), `demoStoryImages`, `getStoryImageSources` et `createStoryImage` dans [app.js](../../frontend/app.js), puis `create_local_app` dans [run_local.py](../../run_local.py). L'[inventaire des images](../../frontend/images/README.md) précise les fichiers, attributs et réserves. Ne pas confondre dépôt GitHub, service local et hébergement du site publié.

## 17. Comment le frontend évite-t-il d'afficher une ancienne réponse ?

« Nous annulons la lecture précédente et changeons un numéro de version. Une réponse tardive ne peut modifier le DOM que si elle appartient encore à la version courante. Le délai maximal évite une attente sans fin. Annuler fetch ne garantit pas qu'une écriture aurait été annulée en base : nous ne répétons donc pas automatiquement les POST. Le tableau efface ses résultats lors d'un refus d'accès et vérifie de nouveau la session au retour depuis le cache de navigation. »

Montrer `apiRequest` dans [api.js](../../frontend/api.js), `cancelRequest`, `beginRequest` et `finishRequest` dans [theories-list.js](../../frontend/theories-list.js), puis les gestionnaires `pagehide/pageshow` dans [admin-dashboard.js](../../frontend/admin-dashboard.js). La revérification au retour n'est pas une surveillance continue de la session.

## 18. À quoi servent la sérialisation et les migrations ?

« La sérialisation prépare les champs JSON et transforme les dates en chaînes lisibles ; elle ne valide pas une transaction et n'attribue aucun droit. Les modèles décrivent le schéma courant. Les révisions Alembic décrivent son évolution, avec upgrade et downgrade. Le mode offline peut produire du SQL sans l'appliquer ; le mode online utilise une connexion. Un downgrade de schéma ne restaure pas automatiquement les données supprimées. »

Montrer `theory_to_dict` dans [theories.py](../../backend/api/v1/views/theories.py), `proposal_to_dict` dans [proposals.py](../../backend/api/v1/views/proposals.py), `get_metadata` et les deux modes dans [migrations/env.py](../../migrations/env.py). Ces fichiers sont uniquement lus et commentés à l'étape 5.1, jamais importés ou exécutés. `create_all()` et les réussites SQLite antérieures ne valident pas les migrations MySQL.

## 19. Comment fonctionne le bannissement administrateur ?

« Mélissa affiche les comptes et leur état, sans email, avec une confirmation et un blocage du double clic. Sylvie protège les deux routes par le rôle en base et le CSRF. La règle commune refuse tout administrateur, soi-même compris, en 409. Mahamadou vérifie que seul le champ is_banned change et que la transaction est annulée en cas d’erreur. Le compte et ses contributions restent présents.

La route POST par id évite les difficultés des pseudos dans une URL ; l’ancienne DELETE par pseudo appelle exactement la même fonction. Une session déjà ouverte perd ses accès protégés au prochain contrôle en base. Après un timeout, on ne sait pas si le serveur a déjà validé : la liste est relue sans répéter le POST. Nos 487 tests isolés passent ; la recette réelle du nouveau panneau n’est pas encore exécutée. »

Montrer [la logique commune](../../backend/api/v1/views/admin_users_support.py), [les routes](../../backend/api/v1/views/index.py), [le panneau](../../frontend/admin-users.js), [les tests backend](../../backend/tests/test_admin_users.py) et [frontend](../../frontend/tests/admin-users.test.cjs). Le bilan 6A (archive interne non livree) sépare preuves actuelles et limites.

## 20. Comment consultez-vous les dossiers dans l’administration ?

« Le tableau charge une fois la liste publique des histoires. Mélissa affiche les titres et catégories, puis filtre cette liste en mémoire par titre et catégorie. Le nombre de dossiers filtrés ne remplace pas les six compteurs. Le lien utilise le slug exact encodé vers la fiche existante.

Sylvie réutilise GET /stories et GET /stories/slug/{slug} : aucune nouvelle API ni permission de dossier. Les données publiques restent publiques même si leur panneau est dans l’administration. Mahamadou vérifie ids, relations et catégories sans changer le schéma. L’API ne fournit qu’un id de catégorie : les ids 1/2 suivent le classement déjà configuré ; les autres restent visibles comme inconnus, sans nom inventé. Nos fixtures sont comparées à la vraie réponse Flask et les lectures ne changent aucune ligne. Les 533 tests isolés passent, mais le navigateur réel n’a pas été relancé. »

Montrer [le panneau](../../frontend/admin-stories.js), [la coordination](../../frontend/admin-dashboard.js), [les routes existantes](../../backend/api/v1/views/histoires.py), [la fixture partagée](../../frontend/tests/fixtures/admin-stories.json) et les preuves (archive interne non livree).

## 21. Comment comptez-vous les propositions en attente ?

« Mélissa ajoute une septième carte à la grille existante et compte seulement le statut exact pending dans la liste administrative déjà chargée. Les six autres indicateurs gardent leur calcul. Une attente de chargement affiche un tiret ; zéro correspond à une réponse valide sans attente. Une erreur efface les valeurs, sans inventer un zéro. Les réponses tardives et pertes d'accès restent gérées par le coordinateur.

Sylvie conserve GET /proposals, protégé par admin_required, et son JSON à sept champs. Aucun nouvel endpoint ; /stats reste public avec seulement ses trois agrégats. Mahamadou vérifie Proposal.status : un texte de longueur 20, non nul, dont la création impose pending. Il n'y a pas d'enum SQL ni d'archive livrée. Les ids de catégories 1 et 2 gardent leur classement existant.

La campagne 6D passe 561 tests, dont la comparaison entre fixture et vraie réponse Flask et l'invariance des neuf tables après les lectures. Ce sont des tests SQLite mémoire et DOM simulé ; le navigateur réel reste reporté. »

Montrer [displayData](../../frontend/admin-dashboard.js), [la route et son sérialiseur](../../backend/api/v1/views/proposals.py), [le modèle](../../backend/models.py), [les tests API 6D](../../backend/tests/test_admin_pending_stats.py) et le bilan (archive interne non livree). Chaque membre prépare la partie qui le concerne ; ne pas s'attribuer une exécution réalisée par le harnais.

## Répartition de la préparation orale — étape 5.1

### Complément courant 6C.2 — suppression des archives

« Une archive conserve ses données. La suppression définitive, autorisée seulement après archivage, retire ce dossier et ses contributions dans une transaction. Les signalements sont liés aux commentaires par une FK ; on ne confond pas l’id du dossier avec l’id du commentaire. L’administrateur confirme le titre et les conséquences ; le serveur contrôle encore rôle, CSRF et état frais. Après timeout, nous relisons sans répéter DELETE. Aucun journal persistant n’est créé. »

Mahamadou montre la reprise qui refuse les données ambiguës avant DDL et la FK entière ; Sylvie montre verrou, empreinte, confirmation et rollback après des DELETE réels ; Mélissa montre dialogue, annulation et relecture. **657 PASS isolés ne prouvent pas MySQL ni la concurrence de production.** Migration réelle et navigateur non exécutés. Les anciennes réponses décrivant Report sans FK concernent l’état historique ; bilan courant (archive interne non livree).

### Complément courant — lot 6C phase 1

« L'archivage masque un dossier du site public tout en conservant ses données pour une restauration éventuelle. Il ne constitue pas une suppression définitive. »

Mahamadou montre la date nullable et la migration préparée, non appliquée à une base réelle. Sylvie montre les quatre routes privées, les vérifications parent des sept écritures, le CSRF et le rollback. Mélissa montre confirmation, filtre d’archives, consultation privée et relecture après réponse incertaine. Les 604 tests automatiques passent ; ils ne prouvent ni Edge réel ni les verrous MySQL. **La demande C-05 de suppression définitive reste PARTIELLE** et le lot 6E n’est pas développé. Voir le bilan 6C phase 1 (archive interne non livree). Les réponses 1 à 21 gardent leur contexte de campagne historique.

| Membre | Réponses à préparer | Repères à montrer |
|---|---|---|
| Mélissa | 3 DOM, 4 flux, 16 images, 17 réponses tardives ; 6 CSRF côté client. | `makeCard`, gestionnaires submit, `apiRequest`, `createStoryImage`, `cancelRequest` et événements de page ; [fiche Mélissa](fiche-melissa.md). |
| Sylvie | 2 REST, 5 mots de passe, 6 CSRF, 7 session, 18 JSON ; contrôles avant transaction. | `protect_session_requests_from_csrf`, `get_authenticated_user`, `admin_required`, `post_theory`, `theory_to_dict` ; [fiche Sylvie](fiche-sylvie.md). |
| Mahamadou | 8 tables, 9 ORM, 10 transactions, 11 persistance, 14 moteurs et 18 migrations ; stockage de 16. | Modèles et FK de `models.py`, add/commit/rollback des routes, `get_metadata`, `upgrade/downgrade` et preuves BDD ; [fiche Mahamadou](fiche-mahamadou.md). |

Les lignes actuelles sont regroupées dans l'index du code (archive interne non livree). Pour parler des campagnes réalisées avec des harnais, préciser son rôle personnel : « la campagne automatisée a vérifié… » si l'on n'a pas soi-même exécuté le scénario. Les scripts temporaires ne doivent pas être présentés comme des fonctionnalités du produit.

## Réponse de Mahamadou — environ 90 secondes

« J'ai testé la base sur une nouvelle SQLite temporaire, avec uniquement des données fictives et sans connexion à Aiven. J'ai créé les neuf tables avec SQLAlchemy puis activé les clés étrangères sur chaque connexion. Cela teste le schéma actuel, pas les migrations Alembic.

J'ai réalisé dix scénarios de base : créations, doublons, dix références invalides, rollback et persistance. Les dix passent. Pour le rollback, j'ai provoqué une vraie erreur d'unicité après une première écriture non validée. Une autre connexion a confirmé qu'aucune écriture partielle ne restait.

J'ai aussi utilisé un vrai Edge, piloté automatiquement, pour envoyer une théorie et une proposition depuis les formulaires. Pour prouver leur enregistrement, j'ai vérifié le POST 201, relu identifiants, auteurs et contenus par l'API puis directement en SQL. Après arrêt et redémarrage du serveur, les données étaient encore présentes. Les requêtes sans CSRF valide ont été refusées en 403.

Huit créations applicatives ont persisté et vingt tentatives ont été refusées comme prévu. La reprise utilisait des sessions fictives préparées par le harnais : elle ne revalide pas le mot de passe. Un premier démarrage Edge a échoué avant la reprise. Les POST Swagger, suppressions, MySQL/Aiven et migrations restent à vérifier. »

## Sept réponses RGPD — complément 6E.2

Ces réponses complètent les supports historiques sans les remplacer. Elles décrivent le périmètre livré et ses limites, pas une certification.

| Question du jury | Réponse simple |
|---|---|
| Qu'est-ce que le RGPD ? | Le règlement européen qui encadre les traitements de données personnelles et les droits des personnes. La sécurité technique ne suffit pas : il faut aussi des choix et une organisation confirmés. |
| Quelles données votre site collecte-t-il ? | Pseudonyme, email, hachage du mot de passe, rôle/bannissement, session et dates ; les contributions et votes sont liés aux comptes. Des signalements portent sur des commentaires et peuvent contenir des informations dans leur motif. |
| Pourquoi utilisez-vous des mots de passe hachés ? | Pour vérifier une saisie sans conserver le mot de passe en clair. Werkzeug produit un hachage salé ; ce n'est pas un chiffrement à déchiffrer et cela ne supprime pas tous les risques. |
| Qu'est-ce qu'un cookie de session ? | Une information échangée avec le navigateur pour reconnaître la connexion. Ici elle est signée, pas chiffrée ; HttpOnly, SameSite et Secure ont des rôles distincts. |
| Pourquoi n'avez-vous pas automatiquement ajouté une bannière de cookies ? | Le cookie nécessaire à la connexion se distingue des traceurs facultatifs. Aucun mécanisme identifié dans les sources examinées ne justifie une bannière automatique ; les ressources externes et le déploiement restent à vérifier. |
| Comment demander la suppression de ses données ? | Un contact suivi et une procédure manuelle sont prévus, mais le contact doit encore être validé. L'équipe vérifiera l'identité de façon proportionnée et examinera les données, tiers et copies. Aucun bouton d'effacement de compte n'est livré ici ; nous ne présentons pas le parcours comme déjà complet. |
| Pourquoi une suppression de compte peut-elle affecter plusieurs tables ? | L'auteur est relié aux dossiers, commentaires, théories, votes et propositions. Certaines FK suppriment des enfants, d'autres retirent seulement le lien ; le pseudo copié et le texte peuvent rester. Il faut préserver les contributions des autres. |

Mélissa montre les notices et le brouillon hors site ; Sylvie explique sessions et demandes ; Mahamadou explique dépendances et conservation. Les décisions (archive interne non livree), la procédure (archive interne non livree) et le bilan 6E.2 (archive interne non livree) permettent de justifier les réserves.
