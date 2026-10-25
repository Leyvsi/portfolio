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
| [admin-dashboard.html](admin-dashboard.html) | Consultation administrative des compteurs, propositions et signalements |

## Scripts et présentation

| Fichier | Responsabilité |
|---|---|
| [styles.css](styles.css) | Présentation commune, grilles responsive et cadrage des images |
| [api.js](api.js) | Requêtes JSON sous `/api/v1`, cookies, CSRF, validation des réponses et erreurs |
| [app.js](app.js) | Cartes, recherche, dossiers, images, inscription, connexion, session et formulaires de contribution |
| [theories-list.js](theories-list.js) | Lecteur public des théories, sélection indépendante et actualisation |
| [admin-dashboard.js](admin-dashboard.js) | Vérification du rôle et chargement des données administratives en lecture seule |
| [donnees.js](donnees.js) | Ancien jeu de six histoires encore chargé par cinq pages, mais non consommé par les scripts actifs |

`donnees.js` n'est ni une base de données, ni un repli automatique lorsque l'API échoue. Les interfaces raccordées utilisent l'API ; une erreur produit un message.

Les pages chargent `api.js` avant `app.js`, puis leur éventuel script spécialisé.

## API et sécurité

Les pages et l'API doivent partager la même origine. `api.js` utilise `fetch` avec `credentials: 'include'`, un délai de 10 secondes par défaut et des messages d'erreur. Il ne répète pas automatiquement les soumissions.

| Usage de l'interface | Routes |
|---|---|
| Listes et fiche | `GET /api/v1/stories` ; `GET /api/v1/stories/slug/{slug}` |
| Compte et session | `POST /api/v1/users` ; `POST /api/v1/login` ; `GET /api/v1/me` ; `POST /api/v1/logout` |
| Proposition | `POST /api/v1/proposals` |
| Théories | `GET` et `POST /api/v1/stories/{story_id}/theories` |
| Consultation administrateur | `GET /api/v1/stats` ; `GET /api/v1/stories` ; `GET /api/v1/proposals` ; `GET /api/v1/admin/reports` |

La session repose sur le cookie signé de Flask : `HttpOnly`, `SameSite=Lax`, et `Secure` configurable selon HTTP local ou HTTPS. Le jeton CSRF obtenu à la connexion ou via `/me` reste en mémoire JavaScript ; il accompagne les écritures authentifiées dans `X-CSRF-Token`, sauf la connexion. Aucun stockage d'authentification dans `localStorage` ou `sessionStorage` n'est utilisé.

Le backend vérifie les comptes, leur état et les permissions. Le contrôle JavaScript du rôle ne remplace pas cette autorisation serveur. Les contenus externes affichés utilisent `textContent`.

## Propositions et théories

Les deux formulaires vérifient la session et récupèrent un CSRF à jour via `GET /api/v1/me` avant l'envoi. Ils transmettent `title` et `content` en JSON : titre obligatoire de 200 caractères maximum, contenu obligatoire limité à 65 535 octets UTF-8.

- **Proposition** : la catégorie choisie est conservée au début du contenu sous la forme « Catégorie proposée : Histoire » ou « Catégorie proposée : Cold case ». Cette métadonnée compte dans la limite UTF-8. Le backend enregistre la proposition en `pending` ; aucune pièce jointe ni publication automatique n'est prévue.
- **Théorie** : le dossier provient des identifiants numériques renvoyés par l'API. La création est liée à ce dossier et devient consultable sans étape de modération.

Le succès exige une réponse HTTP 201 avec un JSON lisible. La saisie est conservée en cas d'échec et les doubles soumissions sont bloquées pendant l'envoi.

Le lecteur « Théories publiées » est accessible sans connexion. Son sélecteur est indépendant de celui du formulaire. Il affiche titre, contenu et date, gère chargement, liste vide, erreur et dossier introuvable, et ignore les réponses devenues obsolètes. Le bouton **Actualiser** recharge la sélection ; une création ne déclenche pas de rechargement automatique du lecteur.

## Administration en lecture seule

Au chargement et avec **Actualiser**, le tableau vérifie `GET /api/v1/me` et exige `user.is_admin === true`. Il charge ensuite les statistiques, les histoires, les propositions et les signalements.

Les compteurs de dossiers et leur répartition sont calculés depuis les histoires ; les nombres d'utilisateurs, commentaires et signalements viennent de `/stats`, une route publique. Les lectures des propositions et signalements sont protégées côté serveur.

Les données sont effacées à réception de HTTP 401/403 et lorsque la page est quittée. La session n'est pas surveillée en continu : une expiration est détectée lors d'une nouvelle requête. Le fichier HTML reste accessible publiquement, sans donner accès aux données protégées.

Aucune action de suppression, bannissement, modération ou publication n'est proposée.

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
node --test --test-isolation=none frontend/tests/images.test.cjs frontend/tests/proposals.test.cjs frontend/tests/theories.test.cjs frontend/tests/theories-list.test.cjs frontend/tests/admin-dashboard.test.cjs
```

Les tests de [frontend/tests](tests/) utilisent des DOM et API simulés. Ils couvrent les images, contributions, validations, CSRF, erreurs, doubles soumissions, lecteur public et accès administrateur. Ils ne vérifient pas un navigateur réel ni MySQL Aiven. Le résultat historique de 226 tests frontend réussis est décrit dans le README principal ; cet audit documentaire ne les a pas relancés.

## Limites actuelles

- Catégories associées directement aux identifiants `1` (histoires résolues) et `2` (Cold Cases).
- Listes sans pagination et actualisation manuelle du lecteur et du tableau administrateur.
- Aucun parcours frontend pour commenter, voter, liker, signaler ou bannir, même si des API existent.
- Aucun téléchargement d'image, récupération de mot de passe ou traitement des propositions dans l'interface.
- Ancien libellé « Voir la maquette du tableau de bord » encore présent dans `admin-connexion.html`, malgré le raccordement réel du tableau.
