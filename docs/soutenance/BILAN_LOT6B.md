# Lot 6B — consultation administrative des histoires et Cold Cases

> Archive pédagogique datée : les résultats et descriptions ci-dessous concernent le lot indiqué. Les anciens repères de ligne ne décrivent pas la version candidate. Pour préparer la soutenance actuelle, consulter les quatre fiches et le référentiel reliés au sommaire.

[Sommaire](README.md) · [Suivi du jury](SUIVI_REMARQUES_JURY.md) · [Index](INDEX_CODE_JURY.md) · [Tests](TESTS_ET_VALIDATION.md)

Lot autorisé le **30 octobre 2026**, sur `feature/frontend-api-integration`, HEAD conservé `07a9f03ea0a3bdad4a07066fdd7bab1997cc158b`. Le travail antérieur et les fichiers non suivis sont préservés. Aucun développement 6C, 6D ou 6E.

## Fonctionnalités et accès

Le tableau possède une section **Dossiers : histoires et Cold Cases**, avec titre, catégorie, recherche par titre et filtre Tous / Histoires résolues / Cold Cases / Autres catégories. L'option Autres n'est proposée que si les données comportent une catégorie non configurée. Une liste sans dossiers et une recherche sans résultat ont des messages distincts.

Les champs natifs ont des libellés et `aria-controls`, l'attente est annoncée avec `aria-busy` et les résultats avec un statut vivant. Les contrôles restent désactivés tant que le chargement et l'accès administrateur ne sont pas validés. La grille `.cards` et les styles responsive existants sont réutilisés ; aucun CSS existant n'est modifié. Les titres sont ajoutés par `textContent`, sans HTML interprété.

Le bouton **Actualiser** du tableau recharge la même liste pour les six compteurs et le panneau. Recherche et filtres sont ensuite locaux, sans nouvelle requête ni modification des compteurs. Un nouveau chargement ou une perte d'accès remet la recherche et le filtre à zéro. Le contrôle de session, les versions de requêtes et AbortController du coordinateur empêchent les réponses anciennes de restaurer le panneau. Les 401/403, le départ de page et les erreurs effacent aussi les résultats et les données privées du lot 6A.

L'interface administrateur exige toujours `/me` et `is_admin === true`. **Les API de dossiers restent publiques** : masquer le panneau n'est pas présenté comme une protection serveur des histoires publiques. Toutes les API privées et les règles de bannissement 6A restent inchangées.

## API réellement réutilisées et catégories

| Usage | Chemin existant |
|---|---|
| Liste du tableau | `GET /api/v1/stories` |
| Fiche déjà livrée | `dossier.html?slug=...`, puis `GET /api/v1/stories/slug/{slug}` |

Le contrat Swagger et le code Flask sont relus avant développement. La liste renvoie `id`, `slug`, `title`, `summary`, `content`, `image_url`, `category_id`, `author_id`, `votes`, `created_at`. Elle ne fournit pas de nom de catégorie. Le panneau reçoit cette liste déjà chargée par `loadDashboard` ; il ne crée aucune API administrative et n'ajoute aucun champ personnel.

`getStoryCategory` dans `app.js` est réutilisée sans modification : le projet classe actuellement les ids **1** et **2** comme histoires résolues et Cold Cases. Une autre valeur entière est affichée comme **Catégorie inconnue (identifiant N)** et reste consultable avec le filtre Autres. Aucun nom supplémentaire n'est déduit de cet entier. Ce classement dépend toujours de la préparation des catégories de la base ; leur nom réel ne peut pas être déduit d'une réponse qui ne le contient pas. Aucune présence de catégorie inconnue sur une base réelle n'est affirmée pendant ce lot.

## Fiches, slugs et données invalides

Les liens conservent le slug exact et l'encodent dans le paramètre de la fiche existante. Accents, espaces et `&` sont notamment testés jusqu'à la vraie route Flask. Aucun slug n'est fabriqué à partir du titre.

Un slug vide, absent ou de mauvais type fait échouer la validation existante de `getStories` : le tableau affiche son erreur de chargement et propose Actualiser. Un slug textuel mais inutilisable pour la fiche actuelle (espaces seuls, séparateurs, `.`/`..`, caractère de contrôle, Unicode non encodable ou plus de 150 caractères) conserve une carte sans lien, avec une explication. Cette longueur correspond au modèle actuel. Les autres dossiers restent affichés dans ce second cas. Un texte ressemblant à un schéma actif reste encodé dans une URL relative de fiche, jamais utilisé comme destination arbitraire.

## Implications BDD et périmètre

Le modèle Story, les clés, relations et catégories ne changent pas. Aucun champ, migration ou action d'écriture n'est ajouté. Les filtres ne modifient ni leur tableau source ni la base. Le panneau copie seulement id, titre, catégorie et slug pour son affichage ; il conserve l'ordre de la liste API.

Les fichiers du backend applicatif, Swagger, `api.js`, `app.js`, `admin-users.js` et les règles de bannissement sont identiques à l'avant-6B. Les six compteurs sont conservés. Aucune édition, publication, suppression ou archive de dossier.

## Tests exécutés et preuves

| Suite | Résultat | Nature |
|---|---|---|
| Backend | **227 réussis** | Client Flask WSGI, SQLAlchemy et SQLite en mémoire isolée ; six nouveaux tests de lecture. |
| Frontend | **298 réussis** | Vrais scripts exécutés dans `node:vm`, DOM et API simulés ; 40 nouveaux cas dossiers. |
| Lanceur | **8 réussis** | Client WSGI ; le test des ressources sert aussi les trois scripts administrateur, sans serveur réel. |
| Total | **533 réussites**, zéro échec/erreur/ignoré | Campagne distincte ; ne pas additionner aux 487 du lot 6A ou aux 439 historiques. |

Une seule tentative des trois suites a suffi. Les scénarios de régression du bannissement, des sessions, du CSRF et des compteurs passent également.

La fixture partagée [admin-stories.json](../../frontend/tests/fixtures/admin-stories.json) contient quatre dossiers fictifs, avec les dix champs de la liste réelle : catégories 1, 2 et 17, titre contenant du HTML traité comme texte, slug accentué et caractères spéciaux. Les tests backend créent ce jeu uniquement dans une SQLite en mémoire, puis comparent **exactement** la réponse Flask à cette fixture. Ils résolvent les quatre fiches, vérifient le 404, le caractère public des lectures et comparent les neuf tables avant/après les GET. Les simulations frontend utilisent donc un jeu vérifié contre l'implémentation réelle ; les variantes invalides sont explicitement des réponses endommagées.

| Scénarios frontend | Couverture exécutée |
|---|---|
| Affichage et filtres | Tous, résolues, Cold Cases, inconnues, option Autres conditionnelle, ordre de l'API. |
| Recherche | Titre uniquement, casse/accents conservés, espaces extérieurs, recherche combinée au filtre, zéro résultat et base vide. |
| Navigation | Liens relatifs encodés, slugs absents/invalides, caractères spéciaux et texte ressemblant à un schéma actif. |
| Erreurs | Réseau simulé, HTTP 500, catégorie de mauvais type et id dupliqué ; aucun ancien résultat laissé visible. |
| Requêtes | Attente, contrôles désactivés, annulation, ancien succès ou 403 après un nouveau chargement, départ de page. |
| Accès | Rôles non administrateur ou mal formés refusés ; perte de session détectée dans le panneau utilisateurs effaçant aussi les dossiers. |
| Non-régression | Six compteurs inchangés après filtre, bannissement 6A fonctionnel et jeu de données gelé non modifié. Aucun POST sur un dossier. |

## Harnais inspecté et commandes

Le nouveau dossier de preuves est `$env:TEMP` / `portfolio-lot6b-20261030-222f5323ed5f401b9ec150ead76ffcb3`. L'instantané `baseline.json` précède les changements. Le manifeste des seuls fichiers de code/fixtures autorisés et ses empreintes sont archivés dans `preflight.json` et `attempt-1/preflight.json`.

Le bootstrap Python et les commandes sont inspectés avant les tests ; le garde Node est identique à celui inspecté en 6A. L'environnement enfant est reconstruit sans secrets hérités, les six paramètres Aiven sont vides, dotenv est neutralisé avant import et seule SQLite `:memory:` est autorisée. Les sondes bloquent avant entrée/sortie les accès privés, réseau, écritures dans le dépôt et autres bases ; les suites ne démarrent que si elles passent. Leurs compteurs positifs attendus sont séparés des suites : **zéro tentative interdite dans les suites finales**. ATTACH/DETACH et MySQL sont bloqués.

Commandes effectivement exécutées, depuis la racine, après préparation et inspection du harnais :

```powershell
# $preuves6b : dossier temporaire de cette campagne.
& .\.venv\Scripts\python.exe -I -B (Join-Path $preuves6b 'run-checks.py') --inspect
& .\.venv\Scripts\python.exe -I -B (Join-Path $preuves6b 'run-checks.py')
```

Les argv enfants exacts sont dans `attempt-1/commands.json` : sondes, bootstrap Python `backend`, sept suites Node avec `--require node-offline-guard.cjs --test --test-isolation=none`, puis bootstrap `launcher`. `attempt-1/*.stdout.txt`, `*.stderr.txt`, `backend.guard.json`, `launcher.guard.json` et `attempt-1/frontend.node-guard.json` conservent les résultats. Aucun serveur Flask/HTTP, navigateur, migration ni accès à une base réelle.

## Documentation et limites

La matrice marque C-04 terminé pour la consultation livrée et testée ; suppression/archivage et autres lots restent distincts. Les références de fonctions sont recalculées, les commentaires français sont dans le vrai code et les 76 réponses historiques sont conservées avec leurs actualisations. Les sources Mermaid restent identiques.

La recette Edge réelle, le rendu responsive sur appareil et la navigation clavier dans un navigateur ne sont **pas exécutés** sans autorisation séparée. Les tests de labels/contrôles natifs et de DOM ne remplacent pas ces contrôles. MySQL/Aiven et les catégories d'une base réelle ne sont pas consultés. Les listes ne sont pas paginées, les noms des catégories ne sont pas exposés par l'API et un chargement global défectueux masque l'ensemble des panneaux comme auparavant.

<!-- CONTROLES_6B_START -->

Contrôles statiques finaux : **PASS**. 2 fichiers Python analysés/compilés en mémoire, 3 JavaScript/CJS vérifiés par `node --check`, **25 opérations API** cohérentes avec OpenAPI, **76 questions/réponses historiques inchangées**, **six blocs Mermaid identiques à l’avant-6B**, **151 repères** dont les 141 cibles héritées recalculées et 10 ajouts. **713 liens internes dans 18 Markdown**, dont 232 liens de lignes, vérifiés sans consultation des URL externes. Les 22 remarques restent suivies. Backend applicatif, contrat API, modèles, migrations, api.js, app.js, admin-users.js et lanceur sont inchangés ; seul le test des ressources du lanceur inclut les scripts administrateur. Branche, HEAD et index Git préservés ; `diff --check` tenant compte des CRLF termine à 0. Reçus : `final-validation.json`, `documentation-updates.json` et `file-inventory.json` dans le dossier de preuves.

<!-- CONTROLES_6B_END -->

**Aucune donnée réelle modifiée. Aucun nouveau contrat API, aucune règle de bannissement changée, aucune migration, aucun commit ni push. Les lots 6C et 6D attendent une validation distincte.**

## Inventaire exact du lot 6B

17 fichiers préexistants modifiés :

```text
README.md
docs/soutenance/ARCHITECTURE_SECURITE_RGPD.md
docs/soutenance/BILAN_ETAPE5.md
docs/soutenance/DEMONSTRATION.md
docs/soutenance/INDEX_CODE_JURY.md
docs/soutenance/ORAL_JURY.md
docs/soutenance/README.md
docs/soutenance/SUIVI_REMARQUES_JURY.md
docs/soutenance/TESTS_ET_VALIDATION.md
docs/soutenance/fiche-commune.md
docs/soutenance/fiche-mahamadou.md
docs/soutenance/fiche-melissa.md
docs/soutenance/fiche-sylvie.md
frontend/README.md
frontend/admin-dashboard.html
frontend/admin-dashboard.js
tests/test_run_local.py
```

Cinq fichiers créés :

```text
backend/tests/test_admin_stories_read.py
frontend/admin-stories.js
frontend/tests/admin-stories.test.cjs
frontend/tests/fixtures/admin-stories.json
docs/soutenance/BILAN_LOT6B.md
```
