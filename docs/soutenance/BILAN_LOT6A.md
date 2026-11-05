# Lot 6A — gestion et bannissement des utilisateurs

> Archive pédagogique datée : les résultats et descriptions ci-dessous concernent le lot indiqué. Les anciens repères de ligne ne décrivent pas la version candidate. Pour préparer la soutenance actuelle, consulter les quatre fiches et le référentiel reliés au sommaire.

[Sommaire](README.md) · [Suivi du jury](SUIVI_REMARQUES_JURY.md) · [Index du code](INDEX_CODE_JURY.md) · [Tests](TESTS_ET_VALIDATION.md)

Lot autorisé le **30 octobre 2026**, branche `feature/frontend-api-integration`, HEAD conservé `07a9f03ea0a3bdad4a07066fdd7bab1997cc158b`. Le travail antérieur est préservé ; les lots 6B à 6E ne sont pas développés.

## Comportement livré

Le tableau conserve ses six compteurs, propositions et signalements. La section **Gestion des utilisateurs** affiche pseudo, rôle et statut à partir de l'API. Elle ne montre pas les emails. Seul un utilisateur ordinaire non banni possède un bouton de bannissement. Une confirmation indique explicitement que le compte et ses contributions seront conservés.

Le panneau utilise les styles existants, `textContent` et des éléments DOM créés en JavaScript. Chargement et action en cours sont signalés avec un message et `aria-busy`. Les doubles clics sont bloqués. La liste est relue après l'action, y compris après timeout, réponse illisible ou erreur réseau ; aucun POST n'est rejoué automatiquement. Si la relecture échoue, aucune ancienne carte actionable n'est laissée visible et une actualisation explicite est proposée.

Un 401/403 efface toutes les données privées du tableau. Un 409 de cible protégée conserve l'accès administrateur et actualise la liste. Quitter la page efface aussi les utilisateurs ; des versions de requêtes empêchent une réponse tardive de restaurer des données anciennes.

## API et règles serveur

| Méthode | Chemin sous `/api/v1` | Résultat |
|---|---|---|
| GET | `/users` | Liste administrateur triée par id, avec `is_banned`. La réponse publique de l'inscription reste inchangée. |
| POST | `/admin/users/{user_id}/ban` | Nouvelle entrée par identifiant stable ; aucun corps JSON requis. |
| DELETE | `/admin/users/{username}/ban` | Entrée historique conservée ; appelle exactement la même logique et les mêmes protections. |

`admin_required` relit le compte et son rôle en base. Le filtre global vérifie le CSRF avant les écritures authentifiées. Les deux routes appellent `ban_user_account` dans [admin_users_support.py](../../backend/api/v1/views/admin_users_support.py). Ce helper vérifie la cible, refuse **tout administrateur**, puis ne modifie que `User.is_banned`. La représentation administrative est centralisée dans `admin_user_to_dict` ; `User.to_dict` n'est pas enrichie de ce statut.

| Code | Signification |
|---|---|
| 200 | Utilisateur ordinaire banni, ou déjà banni ; JSON `status`, `message`, `user` avec le statut serveur. |
| 401 | Session absente ou compte de session introuvable. |
| 403 | Auteur non administrateur, banni, ou CSRF refusé. |
| 404 | Compte ciblé absent ou identifiant hors domaine accepté. |
| 409 | Cible administrateur protégée, avec `code=ADMIN_PROTECTED` ; ce n'est pas une perte d'authentification de l'auteur. |
| 500 | Erreur SQL gérée, rollback et message public sans détail SQL. |

Le helper demande un verrou de ligne pour les moteurs compatibles ; les tests SQLite ne prouvent pas la concurrence MySQL. Le payload de succès est préparé avant le commit pour éviter une lecture ORM implicite après validation. Le commit et le rollback restent dans le même traitement d'erreur. Les accès authentifiés ultérieurs relisent déjà le compte : les anciennes sessions sont donc refusées après bannissement. Les lectures publiques restent publiques.

Aucun débannissement, suppression, nouvelle table, nouvelle migration, motif/durée de bannissement ou journal persistant n'est ajouté. La route historique adopte intentionnellement le nouveau refus 409 des comptes administrateur. Le test historique autorisant l'auto-ban est explicitement remplacé par un test de refus et de maintien de l'accès administrateur.

## Tests réellement exécutés

| Suite | Résultat final retenu | Preuve locale |
|---|---|---|
| Backend | **221 réussis**, aucun échec/erreur/ignoré | `attempt-5/backend.stdout.txt`, `backend.guard.json` |
| Frontend | **258 réussis**, aucun échec/annulé/ignoré | `attempt-2/frontend.stdout.txt`, `attempt-2/frontend.node-guard.json` |
| Lanceur | **8 réussis**, aucun échec/erreur/ignoré | `attempt-2/launcher.stdout.txt`, `launcher.guard.json` |
| Total consolidé | **487 réussites** | Suites distinctes ; ne pas additionner les tentatives échouées ni les 439 historiques. |

Les 16 nouveaux tests Python emploient des sous-cas pour les deux routes. Les 32 nouveaux cas frontend exécutent les vrais scripts dans un DOM et une API simulés. Les tests du tableau historique sont conservés et vérifient toujours les six compteurs.

| Demande | Scénarios exécutés |
|---|---|
| Lecture et confidentialité | Admin accepté ; visiteur/lecteur/banni et rôle de cookie falsifié refusés ; statut booléen réservé aux réponses administrateur ; aucun hash dans le JSON. |
| Action | Succès et répétition idempotente sur POST et DELETE ; cible absente ; id hors domaine ; pseudo contenant une barre oblique géré par la route par id. |
| Comptes protégés | Auto-ban et autre administrateur, même déjà banni, refusés en 409 sans commit ni changement des tables. |
| CSRF | Jeton absent, erroné, vide et non ASCII refusé sur les deux routes. |
| Sessions ouvertes | Deux connexions fictives avant bannissement ; `/me` et création protégée ensuite refusés ; session vidée et nouvelle connexion refusée. |
| Persistance et intégrité | Après commit et retrait de la session ORM, statut relu en base ; comparaison des neuf tables. Le compte ciblé possède réellement histoire, commentaire, théorie, proposition et vote dans la fixture, avec signalement et mise à jour liés ; seul son drapeau peut changer. |
| Transactions | Erreur de commit simulée ; vrai flush de l'UPDATE puis erreur avant commit ; rollback vérifié sans modification des autres données. |
| Interface | Confirmation annulée, double clic, cible devenue protégée/absente, erreurs réseau/500/JSON, timeout après commit simulé, relecture échouée, réponses tardives et nettoyage au départ de page. |
| Régression | Contrat OpenAPI des 25 opérations, sessions, CSRF, statistiques, contributions, lecteurs, images et lanceur. |

## Isolation inspectée avant exécution

Le harnais a été préparé dans un nouveau dossier temporaire, à partir des gardes précédemment inspectés. L'environnement enfant minimal ne conserve pas les secrets hérités. Les six variables Aiven sont vides ; `DATABASE_URL` désigne SQLite en mémoire ; dotenv est neutralisé avant import applicatif. Les connexions MySQL, bases autres que `:memory:`, ATTACH/DETACH, sockets, DNS et sous-processus sont bloqués. Les lectures privées et écritures dans le dépôt sont refusées.

Les sondes Python et Node bloquent les opérations interdites **avant toute entrée/sortie réelle**. Leurs compteurs positifs attendus sont séparés des suites applicatives : les suites retenues enregistrent **zéro tentative interdite**. Le client Flask est WSGI en processus, sans serveur HTTP. Les tests frontend utilisent `node:vm`, sans navigateur réel. Le test du lanceur simule son démarrage.

Chemin de preuves sous `$env:TEMP` : `portfolio-lot6a-20261030-deff2edeaacc4ac1816be956311fe295`. Il contient l'instantané avant modification, le manifeste des seuls fichiers autorisés, les commandes inspectées, stdout/stderr, gardes et reçus. Les comptes, clés et mots de passe du harnais sont fictifs ; aucune donnée de configuration privée n'est copiée.

Les commandes effectivement archivées utilisent les formes suivantes, exécutées depuis la racine, avec les chemins du dossier ci-dessus :

```powershell
# $preuves6a désigne le dossier temporaire de cette campagne déjà inspecté.
& .\.venv\Scripts\python.exe -I -B (Join-Path $preuves6a 'run-checks.py') --inspect
& .\.venv\Scripts\python.exe -I -B (Join-Path $preuves6a 'run-checks.py')
& .\.venv\Scripts\python.exe -I -B (Join-Path $preuves6a 'run-checks.py') --only=backend
```

Le contrôleur lance les sondes avant les suites et archive chaque tentative séparément. Ses argv enfants exacts figurent dans `attempt-*/commands.json` : bootstrap Python `backend` ou `launcher`, et Node avec `--require node-offline-guard.cjs --test --test-isolation=none` suivi des six suites frontend. Ces chemins temporaires ne constituent pas un lanceur de production ni un kit livré dans Git.

Le premier essai a interrompu le contrôleur avant les suites : les sondes étaient bloquantes, mais le chemin d'écriture du reçu Node était construit incorrectement. Seul l'archivage a été corrigé. Au passage suivant, 16 tests backend ont révélé l'oubli d'un alias d'authentification dans la nouvelle fixture et un ancien test attendait encore 25 règles Flask au lieu de 26 ; ces tests ont été corrigés explicitement. Les 258 tests frontend et huit tests du lanceur passaient déjà. Le passage backend suivant confirme les 221 réussites. Un dernier contrôle backend, également à 221 réussites, couvre la conservation de l'ancien champ `error` sur les 404 de l'entrée historique, en complément des nouveaux champs normalisés. Tous les journaux d'échec restent conservés.

## Documentation, limites et validation restante

README principal/frontend, démonstration, sécurité, matrice, fiches individuelles et réponses orales décrivent désormais le lot 6A. Les 76 questions-réponses historiques sont conservées avec un avertissement d'actualisation ; leurs repères et l'index sont recalculés. Les trois sources Mermaid restent inchangées : ce lot ne revendique aucun nouveau rendu.

La recette dans Edge réel n'est **pas exécutée**, faute d'autorisation distincte. Ni durabilité après redémarrage d'une base fichier, ni contraintes/locks MySQL déployés ne sont prouvés par ces tests en mémoire. Les listes restent sans pagination. Il n'y a pas de surveillance continue des sessions, de débannissement ou de journal persistant. Une réponse incertaine peut nécessiter une actualisation supplémentaire si le serveur termine l'action après la première relecture.

Le risque principal de compatibilité est le nouveau refus des administrateurs sur l'ancienne route. Les réponses publiques restent inchangées et la réponse administrateur est enrichie. Les contrôles statiques finaux, l'inventaire exact et les empreintes sont décrits dans les reçus de clôture.

<!-- CONTROLES_6A_START -->

Contrôles statiques finaux : **PASS**. 7 fichiers Python analysés/compilés en mémoire, 4 JavaScript/CJS vérifiés par `node --check`, **25 opérations API** cohérentes avec OpenAPI, **76 questions/réponses historiques inchangées**, **six blocs Mermaid identiques à l’avant-6A**, **141 repères** dont les 124 cibles héritées recalculées et 17 ajouts. **670 liens internes dans 17 Markdown**, dont 222 liens de lignes, vérifiés sans consultation des URL externes. Les 22 remarques restent suivies. Modèles, migrations, permissions communes, lanceur et code des autres lots sont inchangés. Branche, HEAD et index Git préservés ; `diff --check` tenant compte des CRLF termine à 0. Reçus : `final-validation.json`, `documentation-updates.json` et `file-inventory.json` dans le dossier de preuves.

<!-- CONTROLES_6A_END -->

**Aucune donnée réelle modifiée, aucun accès Aiven, aucune migration, aucun serveur ou navigateur réel lancé, aucun commit ni push. Le lot 6B attend la validation de l'utilisateur.**

## Inventaire exact du lot 6A

22 fichiers préexistants modifiés :

```text
README.md
backend/api/v1/swagger.json
backend/api/v1/views/index.py
backend/api/v1/views/users.py
backend/tests/test_api_errors_stats_login.py
backend/tests/test_proposals_ban.py
backend/tests/test_swagger.py
docs/soutenance/ARCHITECTURE_SECURITE_RGPD.md
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
frontend/api.js
```

Cinq fichiers créés :

```text
backend/api/v1/views/admin_users_support.py
backend/tests/test_admin_users.py
frontend/admin-users.js
frontend/tests/admin-users.test.cjs
docs/soutenance/BILAN_LOT6A.md
```
