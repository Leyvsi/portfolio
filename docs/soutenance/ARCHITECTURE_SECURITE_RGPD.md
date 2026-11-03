# Architecture, sécurité et demandes RGPD

> Etat de diffusion scolaire du 3 novembre 2026 : suivre le [guide actuel](../../LIVRAISON_SCOLAIRE.md) et la [validation scolaire](VALIDATION_SCOLAIRE.md). Les sections de campagnes anterieures et leurs commandes sont historiques ; elles ne remplacent pas la procedure actuelle. Les chemins sous `C:\chemin\utilisateur` sont des exemples anonymises. Les archives internes signalees sont conservees localement.

**État courant 6E.2 — 31 octobre 2026.** Notices provisoires intégrées à trois formulaires ; politique HTML conservée hors site et procédure interne préparée. Responsable, contact et autres décisions restent à confirmer. Aucun changement du backend ou du schéma, aucune déclaration de conformité. Voir le bilan 6E.2 (archive interne non livree) et le complément en fin de document ; les constats antérieurs gardent leur contexte historique.

**État courant 6C.2.** Les signalements sont désormais exclusivement des commentaires : FK entière NOT NULL `Report.comment_id → Comment.id`, CASCADE ; type/target_id calculés pour compatibilité JSON. Les anciennes références incompatibles bloquent la migration avant toute modification du schéma, sans effacement automatique. La purge exige une archive, un admin actif relu sous verrou, CSRF, titre exact/acquittement, confirmation signée liée à la session, révision et empreinte de graphe, plus If-Match. La suppression du graphe et la réservation de révision sont atomiques ; aucune cascade vers les comptes.

**S2 simplifié est appliqué : aucun reçu persistant ni purge programmée.** Un succès JSON reçu confirme la transaction ; un COMMIT dont l’accusé manque peut rester incertain. Le client relit et ne répète jamais automatiquement DELETE ; un 404 constate une absence sans attribution. Aucune conformité RGPD ni traitement 6E déduit de cette purge éditoriale. Médias, copies statiques et sauvegardes restent hors transaction. Bilan 6C.2 (archive interne non livree). Les constats des phases antérieures ci-dessous gardent leur portée historique.

**Complément courant — lot 6C phase 1, 31 octobre 2026.** L’archivage est un état éditorial réversible (`Story.archived_at`), avec quatre routes admin documentées et aucune suppression. Un administrateur relu en base, non banni et doté du CSRF peut archiver/restaurer ; un dossier absent donne 404, un état répété donne 200 `changed=false`. Les erreurs SQL sont génériques et provoquent rollback. Les réponses privées d’archives sont `Cache-Control: no-store`.

Les lectures publiques et sept entrées de contributions vérifient l’état du parent, y compris likes et deux routes de signalement par identifiant d’enfant. Les écrivains et l’archivage demandent le même verrou Story. Cela décrit la stratégie InnoDB ; SQLite mémoire ne prouve pas son comportement concurrent sur MySQL. Les contributions et signalements sont conservés, les compteurs globaux de commentaires/signalements aussi. Aucun journal d’acteur ou historique intégral n’est ajouté ; la date trace seulement le retrait courant. L’archivage n’est ni une purge ni un mécanisme de conformité RGPD. Médias, copies statiques et contenus déjà reçus ne sont pas rappelés. Voir le bilan et les limites (archive interne non livree). Les sections 5/6A/6B/6D ci-dessous conservent leur portée historique.

[Sommaire](README.md) · Index des fonctions (archive interne non livree) · [Tests attestés](TESTS_ET_VALIDATION.md)

État des sources au 29 octobre 2026. Ce document explique l'existant ; il n'ajoute aucune fonction, migration ou garantie de conformité.

## Architecture et emplacements

Les trois diagrammes de référence sont dans le README : [architecture](../../README.md#architecture), [relations](../../README.md#schéma-relationnel) et [parcours d'une théorie](../../README.md#parcours-dune-théorie). Les copies présentes dans les fiches commune et Mahamadou sont synchronisées avec ces diagrammes.

| Élément | Où et pourquoi |
|---|---|
| HTML et CSS | Fichiers de `frontend/`, lus par le navigateur pour la structure et la présentation. |
| DOM | Arbre en mémoire du navigateur issu du HTML, modifié par JavaScript. Ce n'est ni un fichier de base ni un serveur. |
| JavaScript | `app.js`, `theories-list.js`, `admin-dashboard.js` réagissent aux événements ; `api.js` centralise `fetch`, JSON et erreurs. |
| Lanceur WSGI | `run_local.py` compose le service de ressources avec l'application Flask ; un processus Python local, une origine HTTP. |
| Système de fichiers | Conserve HTML/CSS/JS/images et le contrat Swagger. Une URL d'image en base référence une ressource ; elle ne contient pas nécessairement son fichier. |
| Flask | Reçoit les routes API, applique le filtre CSRF puis les contrôles de la vue/décorateurs et prépare JSON/statut. |
| SQLAlchemy | Convertit les objets/requêtes Python en SQL et gère les transactions sur la base configurée. Ce n'est pas un service de base indépendant. |
| SQLite | Moteur embarqué utilisant un fichier local, ou une base en mémoire pour certains tests. Il ne nécessite pas de serveur de base séparé. |
| MySQL/Aiven | Autre cible possible : moteur serveur accessible avec PyMySQL et options TLS. Sa configuration existe ; les campagnes 2 à 4 n'y ont pas accédé. |

[create_local_app](../../run_local.py) confie à `SharedDataMiddleware` les GET/HEAD des fichiers autorisés de `frontend/`. `/` correspond à `index.html`. Les chemins API et les autres méthodes passent à Flask. Seuls les fichiers racine HTML/CSS/JS et les images avec extensions prévues sont proposés par cette composition ; `.env`, backend, certificats et migrations ne sont pas publiés par ce chemin. Les tests WSGI vérifient aussi les traversées de chemins.

`main()` charge normalement la configuration locale puis écoute sur **127.0.0.1:5000**, sans debug/reloader. Le démarrage direct de `backend/index.py` contient encore une entrée de développement avec debug et écoute large : ce n'est pas la commande de démonstration retenue. Aucun démarrage n'est effectué à l'étape 5.

## Images : dépôt, service local et production

Les quatre WebP et le SVG de `frontend/images/` sont suivis dans Git. `Story.image_url` conserve une référence de ressource ; les octets des images ne sont pas enregistrés dans cette colonne. `getStoryImageSources()` essaie une URL se résolvant en HTTP(S), le fichier associé au slug, puis le SVG ; `createStoryImage()` avance sur erreur et finit par un texte si toutes les sources échouent.

Ce choix statique permet de livrer le petit catalogue actuel avec les pages, sans service d'upload ni stockage supplémentaire. Les fichiers versionnés évoluent avec le déploiement ; ce choix n'est pas présenté comme une solution déjà dimensionnée pour un grand catalogue ou des dépôts de fichiers par les utilisateurs. Les dimensions communes et WebP conviennent aux illustrations actuelles ; ils ne justifient pas à eux seuls le choix d'un hébergeur.

En local, `SharedDataMiddleware` lit les fichiers publics et répond aux URL `/images/...` par HTTP. Le navigateur ne consulte pas directement le chemin Windows ni le dépôt Git. En production, il faudra publier ces ressources sur l'infrastructure retenue ; serveur web, stockage d'objets et CDN sont des possibilités, pas des services actuellement attestés. Les images référencées par l'API peuvent provenir d'une autre origine. Aucun fournisseur, domaine de production ou stockage persistant déployé n'est confirmé ici.

Voir l'[inventaire et les réserves de droits](../../frontend/images/README.md), la [réponse orale 16](ORAL_JURY.md#16-où-sont-stockées-et-servies-les-images-et-pourquoi-ce-choix-) et le [suivi I-01/I-02](SUIVI_REMARQUES_JURY.md). Ni origine ni licence n'est déduite de la seule présence d'une image dans Git.

## Réserves des diagrammes — étape 5.1

La liaison d'architecture indique désormais `SharedDataMiddleware → frontend/ : lit les fichiers publics` : elle représente l'action de lecture du middleware, afin d'éviter la remontée du connecteur qui traversait Flask. Le flux conserve son sens ; le texte de la note finale est réparti sur trois lignes. Les copies de la fiche commune sont synchronisées. Le diagramme relationnel et sa copie sont conservés à l'identique.

Ces corrections de sources sont contrôlées statiquement et les trois sources passent le parseur Mermaid local ; **aucun nouveau rendu ni contrôle visuel n'est effectué à l'étape 5.1**. Leur effet sur les deux défauts reste à confirmer dans un rendu local autorisé. Le bilan 5 (archive interne non livree) conserve les verdicts visuels historiques ; le bilan 5.1 (archive interne non livree) décrit les changements actuels.

## Flux d'une contribution

1. Le DOM contient le formulaire. L'événement `submit` déclenche le gestionnaire de `app.js` ; `preventDefault()` permet de gérer l'envoi en JavaScript.
2. Le script valide la saisie et verrouille les doubles soumissions pendant l'attente. Le serveur devra refaire ses propres contrôles.
3. `GET /api/v1/me` vérifie la session et fournit un CSRF à jour, gardé en mémoire JavaScript.
4. `api.js` envoie le JSON par HTTP avec `credentials: 'include'` et `X-CSRF-Token` pour l'écriture.
5. Flask applique `protect_session_requests_from_csrf()` avant la vue. La route relit ensuite le compte autorisé, la ressource cible et les champs. Une route administrateur ajoute `admin_required`.
6. La route prépare l'objet avec l'auteur issu de la session. `add()` le place dans la session SQLAlchemy ; le flush associé à `commit()` émet les écritures, puis COMMIT les valide.
7. En cas d'erreur SQL interceptée, `rollback()` annule les changements non validés et remet la session dans un état utilisable. La route renvoie l'erreur prévue.
8. Flask renvoie un statut et du JSON. `fetch` ne rejette pas automatiquement un 400/500 : `apiRequest` le transforme en erreur exploitable.
9. Après 201 et JSON lisible, le formulaire est réinitialisé. En cas d'échec, la contribution saisie reste dans le DOM, sans sauvegarde durable. Le lecteur de théories nécessite encore une actualisation explicite.

Les paragraphes et cartes utilisent `textContent`, pour traiter les données comme texte. Cela ne dispense pas de vérifier les URL, la validation serveur ou les autres surfaces de sécurité. Les requêtes tardives du lecteur/tableau sont écartées par version et annulation, afin de ne pas remplacer une sélection actuelle par une ancienne réponse.

## Base relationnelle et transactions

Les neuf tables sont `users`, `categories`, `stories`, `theories`, `comments`, `votes`, `proposals`, `reports`, `cold_case_updates`. [models.py](../../backend/models.py) définit neuf PK `id` et dix FK. Le [tableau du README](../../README.md#schéma-relationnel) précise les cardinalités et règles de suppression.

- `username`, `email`, nom de catégorie et slug sont uniques individuellement. Dans `votes`, **seul le couple** `(user_id, story_id)` est unique : chaque utilisateur peut voter pour plusieurs dossiers.
- `CASCADE` et `SET NULL` sont des règles de contraintes SQL, effectives seulement si la base les applique. `Story` déclare aussi `all, delete-orphan` sur ses quatre collections : c'est un mécanisme ORM distinct.
- `stories.author_id` et `stories.category_id` sont obligatoires sans règle ON DELETE explicite. Une suppression du parent peut être refusée.
- `reports.target_id` est une chaîne sans FK. La route vérifie actuellement une cible de type commentaire ; son compteur est calculé à partir des lignes `reports`.
- `Comment.username` est une copie du pseudo. Mettre `user_id` à NULL ne retire pas cette copie ni les renseignements éventuels contenus dans les textes.

Les quatre migrations décrivent un historique de schéma ; `Migrate(app, db)` expose les commandes, sans les exécuter au démarrage. `db.create_all()` crée le schéma courant des modèles mais ne démontre pas cet historique. Aucune migration modifiée ou exécutée ici. Les campagnes SQLite ne valident ni le dialecte, ni les collations, ni les contraintes déployées de MySQL/Aiven.

## Mots de passe, session et rôles

`User.set_password()` appelle `generate_password_hash()` de Werkzeug ; `check_password()` appelle `check_password_hash()`. Le hachage salé sert à vérifier une saisie ultérieure et n'est pas un chiffrement réversible. `User.to_dict()` exclut le hachage. L'inscription vérifie longueur/composition, email et doublons ; elle ne permet pas de choisir `is_admin`. Aucun contrôle de débit de connexion n'est implémenté dans les sources examinées.

À la connexion, Flask vérifie le compte, son mot de passe et son état, efface l'ancien état de session puis conserve `user_id`, `is_admin` et le CSRF dans la session signée. **Signé ne signifie pas chiffré** : aucune donnée secrète ne doit être placée dans le cookie.

| Paramètre | Comportement exact et limite |
|---|---|
| `HttpOnly=True` | Le JavaScript de la page ne lit pas directement le cookie de session ; le navigateur peut l'envoyer avec les requêtes. |
| `SameSite=Lax` | Limite certains envois intersites, sans remplacer le CSRF ni les permissions. |
| `Secure` configurable | Réserve l'envoi à HTTPS quand activé. Le HTTP loopback de recette utilisait `false`. |
| Déconnexion | `session.clear()` fait supprimer le cookie côté navigateur. Aucun registre central de révocation de toutes ses copies n'est présent. |

`get_authenticated_user()` relit le compte par `user_id` et refuse/efface une session de compte absent ou banni. `admin_required()` vérifie ensuite `user.is_admin` **en base** ; il ne fait pas confiance à un rôle JSON ni au seul booléen du cookie. Authentification = reconnaître le compte ; autorisation = déterminer les actions permises. La restriction JavaScript du tableau est un accompagnement d'interface, pas la frontière de sécurité.

## CSRF : comportement exact et exceptions

Une attaque CSRF tente de faire envoyer par le navigateur une action utilisant son cookie de session à son insu. Ici, un jeton aléatoire lié à la session doit correspondre à `X-CSRF-Token`. Le filtre exige deux chaînes ASCII non vides, puis utilise `secrets.compare_digest()` ; sinon il renvoie **403** avant la vue.

| Cas | Filtre CSRF réel |
|---|---|
| GET, HEAD, OPTIONS | Pas de contrôle CSRF dans ce filtre. Les routes de lecture peuvent rester soumises à authentification/rôle. |
| POST/PUT/PATCH/DELETE avec `user_id` de session | Jeton requis, sauf `/api/v1/login`. Toutes ces méthodes ne correspondent pas nécessairement à une route existante. |
| `POST /api/v1/login` | Exemption explicite, même si une session existait. Ne pas annoncer que tous les POST sont protégés. |
| Requête sans `user_id` de session | Filtre traversé sans CSRF ; les routes membres refusent encore l'anonyme via leur contrôle d'authentification. |
| Inscription/déconnexion anonymes | Acceptées sans ce jeton. Avec une session existante, leur contrôle CSRF s'applique. L'inscription vérifie aussi le compte de cette session. |

GET est généralement destiné à lire, tandis que POST/DELETE peuvent modifier un état : c'est pourquoi ce filtre cible les écritures authentifiées. La méthode seule ne garantit pas l'absence d'effet : `/me` peut notamment créer un jeton dans la session. Le CSRF ne remplace pas le contrôle du compte et du rôle. Le bannissement utilise DELETE mais met seulement `is_banned=True`, sans effacer le compte.

`api.js` garde le jeton en mémoire, sans `localStorage` ni `sessionStorage`, et l'envoie avec les écritures prévues. `HttpOnly` reste compatible : le script reçoit le CSRF via le JSON de login/me sans lire le cookie. CORS définit les origines autorisées ; il ne constitue ni une autorisation serveur ni une protection CSRF complète.

Swagger UI ne comporte pas d'intercepteur ajoutant ce jeton aux POST. Son nom de fonction `oauth_swagger` est historique : aucun parcours OAuth n'y est implémenté. Voir les [limites d'exécution Swagger](TESTS_ET_VALIDATION.md#4-étape-3--véritable-edge-consultation-et-sessions).

## Confidentialité et limites observées

Les routes de listes utilisateurs/propositions/signalements sont administrateur ; `/me` renvoie le compte courant. `/stats` est public et renvoie des compteurs. Les dossiers, théories et commentaires disposent de lectures publiques : ne pas les présenter comme des espaces privés. Les champs libres peuvent contenir des informations que les validations de type/taille ne détectent pas.

Les règles Git excluent `.env`, certificats, cookies et bases locales, mais une règle d'exclusion n'est pas une preuve d'absence de secret dans tout historique. Les valeurs privées n'ont pas été lues pour cette étape. Les mots de passe, cookies, clés et CSRF restent hors des supports publiables ; le modèle de démonstration ne contient que des identités fictives et des espaces à renseigner dans une copie privée.

## Demandes RGPD du jury : existant et travail restant

Cette section est un constat technique des sources, **pas une déclaration de conformité RGPD ni une analyse juridique**. Les éléments de sécurité ci-dessus ne suffisent pas à démontrer une conformité.

| Sujet à présenter au jury | Existant réellement observé | À définir ou développer séparément |
|---|---|---|
| Données du compte | Pseudo, email, hachage, rôle, état et dates dans `User`. | Information claire sur finalités, responsables, destinataires et durées ; décisions de l'équipe à formaliser. |
| Accès/export des données | `/me` restitue certains champs du compte ; listes admin protégées. | Parcours complet de demande et d'export des données associées, absent. |
| Rectification/effacement | Aucun parcours utilisateur de modification/suppression de compte. Bannir ne supprime pas. | Traitement des demandes, vérification du demandeur et règles de conservation. Aucun DELETE de ce type ajouté ici. |
| Contributions et anonymisation | FK nullable/SET NULL pour certains auteurs, mais textes et pseudo de commentaire conservés. | Stratégie complète concernant copies du pseudo, contenus libres, archives et signalements. Ne pas confondre SET NULL et anonymisation garantie. |
| Cookies et consentement | Cookie fonctionnel de session Flask ; pas de gestionnaire de consentement dans les sources. | Inventorier les usages réels et documenter les choix nécessaires avant un mécanisme adapté ; aucune bannière ou collecte nouvelle ajoutée ici. |
| Ressources externes | Images HTTP(S) possibles et CDN Swagger déclaré. | Examiner et expliquer les flux réels lors d'un déploiement ; la recette hors ligne ne prouve pas leur absence en production. |
| Conservation et suivi | Dates dans les modèles ; aucune politique automatique de purge repérée. | Définir durée, procédures de demande, sauvegardes et preuves de traitement. |

L'étape 5 ajoute uniquement des explications. Les fonctions d'administration, consentement, export, effacement et anonymisation demandent une conception et une autorisation de développement ultérieures.

## Gestion des utilisateurs — lot 6A, 30 octobre 2026

Le panneau `admin-users.js` est coordonné par le tableau existant et le même mécanisme d’effacement des données privées. Les deux entrées de bannissement utilisent [admin_users_support.py](../../backend/api/v1/views/admin_users_support.py), sans changement de modèle ni migration. `admin_user_to_dict` réserve `is_banned` aux réponses administrateur ; inscription et `/me` restent inchangés.

`admin_required` et le filtre CSRF protègent POST par id et DELETE par pseudo. La cible est relue avec une demande de verrou ; tous les administrateurs sont refusés en 409, sans perte de session de l’auteur. Le helper ne valide que `is_banned=True`, avec rollback en cas d’erreur SQL. Les contrôles des accès protégés ultérieurs détectent la suspension d’une session déjà ouverte. Les données reçues auparavant ne sont pas rappelées.

La confirmation et le verrou de soumission accompagnent les règles serveur. Après résultat incertain, le panneau relit la liste sans répéter l’écriture et écarte les réponses anciennes. Les preuves du bilan 6A (archive interne non livree) restent SQLite/DOM simulé : aucun navigateur, réseau ou MySQL. Consentement, droits d’effacement et autres lots ne sont pas développés ; bannir n’efface ni le compte ni les contributions.

## Statistiques administrateur — lot 6D

Le septième compteur provient du `GET /proposals` administratif existant ; seul le texte exact `pending` compte. `/stats` conserve ses trois agrégats publics utilisateurs/commentaires/signalements et n'expose aucune proposition. `admin_required` relit le compte, son bannissement et son rôle en base. La vérification `/me` côté navigateur sert aussi au nettoyage, sans remplacer ces permissions.

Les sept compteurs utilisent le même cycle de chargement, refus et annulation. Une liste vide validée permet zéro ; une lecture échouée efface les valeurs et masque les panneaux. Les réponses anciennes sont ignorées ; aucune surveillance continue du rôle n'est ajoutée. Ce calcul ne modifie ni ligne, ni statut, ni publication. Une future archive ou pagination demanderait un contrat explicite avant de modifier la définition des compteurs ; aucun archivage n'est développé.

Le bilan 6D (archive interne non livree) consigne 561 tests isolés et leurs gardes, pas une preuve de confinement d'Edge. Aucun réseau Windows, pare-feu, VM ou base réelle n'est utilisé pour cette campagne.

## Consultation des dossiers — lot 6B

`admin-stories.js` reçoit la réponse de `getStories` déjà utilisée par les compteurs. Il ne fait aucun fetch ni écriture ; les filtres restent locaux. `loadDashboard` vérifie la session et la version avant de transmettre les données. Annulation, 401/403 et départ de page effacent aussi ce panneau. L’interface est réservée au rôle administrateur ; les deux lectures de dossiers restent des API publiques, avec les mêmes réponses et données personnelles qu’avant.

Aucun modèle ni contrat changé. Le classement 1/2 est celui existant dans le frontend, tandis que les autres ids sont indiqués comme inconnus. Titres affichés comme texte, slugs encodés vers la fiche relative existante ; les liens inutilisables sont omis. Les tests 6B (archive interne non livree) comparent la fixture frontend à Flask et les neuf tables avant/après les lectures. Aucun accès à une base réelle, nouveau traceur, rendu Mermaid ou développement RGPD.

## État 6E.2 — informations intégrées et limites maintenues

La procédure interne finalisée pour cette phase (archive interne non livree) couvre réception, identité proportionnée, données/tiers et réponse sécurisée, avec accès, copie, rectification, effacement et contestation de contenu. Son activation attend responsable, contact et organisation confirmés ; aucune demande réelle n'est traitée. La politique et les bases légales ne sont pas réputées validées par une notice pédagogique.

### Cookies vérifiés dans les sources, sans lire la configuration privée

| Élément | Constat de code et limite |
|---|---|
| Session Flask | Cookie signé contenant user_id, is_admin et le CSRF ; aucun mot de passe. La signature protège l'intégrité, pas la confidentialité du contenu. |
| HttpOnly | True dans le code : empêche la lecture directe du cookie par JavaScript. Le navigateur peut toujours l'envoyer ; cela ne supprime pas tous les risques XSS. |
| SameSite | Lax dans le code. Ce réglage ne remplace pas le filtre CSRF et les permissions serveur. |
| Secure | Lu par env_to_bool, avec défaut False. Quand activé, réserve l'envoi du cookie à HTTPS. Valeur effective et HTTPS déployé non vérifiés ici. |
| Durée et révocation | Aucune durée métier explicite identifiée dans les sources examinées ; pas de registre central révoquant toutes les copies du cookie. Ne pas inventer de durée. |
| Consentement | Le cookie nécessaire à la connexion se distingue des traceurs facultatifs. Aucun mécanisme publicitaire ou de mesure d'audience identifié dans les sources examinées ne motive l'ajout automatique d'une bannière. Les fichiers statiques non examinés et le déploiement restent hors preuve. |
| Ressources externes | Swagger charge cdnjs ; les images peuvent utiliser des URL distantes. Aucun réseau réel utilisé pour les vérifier dans ce lot. |

Le code de sessions, CSRF, CORS et permissions reste identique. Une déconnexion locale ne prouve pas la révocation de tous les anciens cookies. Avant un futur effacement de compte, traiter aussi la réutilisation possible d'un id SQLite. Ces limites ne sont pas corrigées par une page d'information.

### Relations actuelles à expliquer — neuf modèles et onze FK

Les descriptions antérieures des dix FK et de la cible textuelle de report gardent leur contexte historique. Depuis 6C.2, Report.comment_id est un Integer obligatoire, FK vers Comment.id avec CASCADE. Les propriétés type/target_id assurent la compatibilité JSON sans second lien stocké. Aucun déclarant de signalement n'est enregistré.

User contient id, pseudonyme/email uniques, hachage, rôle, bannissement et création. Story.author_id est obligatoire sans règle ON DELETE ; Theory/Comment utilisent SET NULL vers User, mais le texte et Comment.username copié restent. Vote/Proposal utilisent CASCADE SQL vers User. Les relations ORM de User ne déclarent pas les cascades rendant un simple delete du compte suffisant. Préserver les autres contributions exige une décision ciblée et une opération testée, pas une cascade globale.

Bannissement = restriction d'accès ; archivage = retrait public avec conservation ; purge 6C.2 = suppression d'un dossier archivé et de son graphe ; effacement personnel = examen d'une personne, de ses textes/liens et des copies. Aucun schéma, migration, mécanisme de suppression ou journal persistant nouveau. Étude des conséquences (archive interne non livree).

Les références CNIL déjà utilisées en 6E.1 restent disponibles dans la procédure (archive interne non livree). Aucune nouvelle vérification de lien externe, démarche juridique ou validation de déploiement n'est revendiquée.
