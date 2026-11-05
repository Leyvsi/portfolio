# Lot 6C.2 — suppression définitive sécurisée des archives

> Archive pédagogique datée : les résultats et descriptions ci-dessous concernent le lot indiqué. Les anciens repères de ligne ne décrivent pas la version candidate. Pour préparer la soutenance actuelle, consulter les quatre fiches et le référentiel reliés au sommaire.

[Sommaire](README.md) · [Contrat OpenAPI](../../backend/api/v1/swagger.json) · [Tests](TESTS_ET_VALIDATION.md) · [Index](INDEX_CODE_JURY.md) · [Matrice du jury](SUIVI_REMARQUES_JURY.md)

**31 octobre 2026 — implémentation locale après levée explicite de S1.** Report est désormais limité aux commentaires. Suppression des dossiers déjà archivés, sans reçu persistant conformément à S2. **285 backend + 364 frontend + 8 lanceur = 657 PASS**, aucune base réelle modifiée. Les documents antérieurs de conception/NO-GO décrivent les décisions précédentes ; la présente livraison les actualise sans réécrire leurs preuves historiques.

## 1. Autorisation et préservation

Branche conservée : `feature/frontend-api-integration`, HEAD `07a9f03ea0a3bdad4a07066fdd7bab1997cc158b`. Le travail local antérieur, suivi et non suivi, est conservé. Inventaire avant édition : 96 ressources publiques et leurs SHA-256 ; sauvegarde ciblée de 27 fichiers dans `$env:TEMP/portfolio-lot6c2-implementation-20261031-bpf4frum/backup`. Statut, index Git et périmètre prévisionnel dans `baseline.json`. Aucun secret, `.env`, cookie, certificat ou fichier de base copié.

L’autorisation a levé le blocage du modèle générique : seules les routes visaient des commentaires auparavant, tandis que le modèle acceptait notamment la fixture other. La restriction du modèle a donc été **autorisée comme changement de périmètre**, et non déduite d’une inspection de données réelles. Aucun compte rendu n’affirme avoir lu une base de production.

## 2. Modèle, relations et contrat des signalements

- `Report.comment_id` : Integer obligatoire, FK nommée `fk_reports_comment → comments.id`, ON DELETE CASCADE, index non unique. Plusieurs signalements du même commentaire restent possibles.
- `Comment.moderation_reports` / `Report.comment` : relation explicite ; le nom évite de recréer l’ancien compteur `Comment.reports`. Aucune des dix FK préexistantes n’est modifiée ; **9 tables, 11 FK**, aucun modèle de reçu ajouté.
- Colonnes physiques `type` et `target_id` retirées. Le JSON historique reste identique : `type="comment"` et `target_id=str(comment_id)`. Des propriétés Python compatibles acceptent uniquement le type comment et une chaîne d’id canonique ; un nouveau type other lève une erreur, aucun second lien stocké.
- Les deux créations Flask écrivent directement comment_id, conservent validation/session/CSRF et refus des parents archivés. La FK empêche une création dont le commentaire n’existe pas, y compris hors du précontrôle applicatif.

Les déclarations actuelles de Comment.id et Report.comment_id sont Integer. La migration **réfléchit le type SQL de comments.id avant tout DDL**, vérifie qu’il est entier et le copie pour la nouvelle colonne. Cela ne prétend pas attester le type d’une base MySQL non consultée.

### Fixture historique other conservée comme preuve négative

`test_story_archiving.py` conserve un troisième report comme témoin sur **l’autre dossier**, avec vérification de sa conservation. L’ancien cas other est exercé dans `test_report_migration.py` : insertion fictive de la forme historique, migration refusée, puis comparaison du schéma et des lignes **avant même rollback**. Aucune suppression d’assertion destinée à dissimuler une incompatibilité. Les assertions Python type/target_id et les formes HTTP historiques continuent de passer.

## 3. Migration préparée et limites

[c6c200000001_comment_reports_and_story_revision.py](../../migrations/versions/c6c200000001_comment_reports_and_story_revision.py) suit `c6c100000001`. **Exercée uniquement en SQLite mémoire fictive, jamais sur une base réelle ; env.py n’est pas chargé dans ces tests.**

1. Avant **tout** ajout/modification de colonne, contrôler tous les reports : type exactement comment, cible ASCII canonique positive ≤ 2147483647, commentaire existant. Aucun trim, cast permissif ou réparation de valeur historique.
2. Valeur incompatible, type réel non entier ou cible absente : RuntimeError explicite sans contenu sensible, **aucune modification de schéma ni reprise partielle pour ces anomalies**. Les tests couvrent other, story/Comment, cible absente, zéro/négatif, Unicode numérique, espaces, zéros initiaux et dépassement.
3. Après validation, ajouter comment_id transitoire, affecter les correspondances approuvées, puis rendre obligatoire, ajouter FK/index et retirer les deux anciennes colonnes. Motifs/statuts/dates/ids et doublons préservés.
4. Ajouter `Story.management_revision`, remplir chaque dossier existant d’une révision aléatoire différente, puis créer son index unique. Aucun changement des enfants ni de la catégorie.

**FK SQLite ON pendant les tests de migration**, sans désactivation temporaire. Seule la table enfant reports est reconstruite ; stories reçoit une colonne/index sans reconstruction de la table référencée. Le downgrade est exercé sur le schéma fictif : il restitue la représentation textuelle des reports restants, sans recréer de données déjà purgées.

Le défaut SQL de la révision est la sentinelle de 32 zéros pour permettre l’ajout NOT NULL aux lignes existantes sans reconstruire stories ; la migration la remplace dans toutes les anciennes lignes. Le défaut Python des nouvelles créations ORM génère une vraie révision. **Une insertion SQL extérieure qui omettrait cette révision ne devient pas purgeable : la sentinelle est refusée**. Les futurs écrivains SQL devront fournir une révision conforme ; le chemin produit ne crée pas cette sentinelle.

La garantie « données incompatibles → aucun DDL » suppose un inventaire stable : **maintenance et anciens écrivains arrêtés/drainés sont obligatoires avant toute exécution réelle**. Les DDL MySQL ne sont pas promis atomiques en cas d’incident technique survenant après les contrôles. Ne pas activer le code sur un schéma partiellement migré ; contrôler reprise et contraintes, et résoudre toute anomalie avant de poursuivre. Une migration valide ne peut pas prouver la provenance d’une référence historiquement déjà mal attribuée.

## 4. Précondition simple et transaction

La conception à identité + compteur + reçu a été simplifiée pour le besoin autorisé : **une seule révision aléatoire de gestion**, plus une empreinte du dossier et de son graphe. Ce n’est ni un secret d’authentification ni un journal. Elle change à la création et à chaque transition archive/restauration effective ; les no-op la conservent. Cela invalide une ancienne confirmation après restauration/réarchivage, même si les dates sont identiques, ou après réutilisation d’un numéro.

Les sept écrivains de contributions conservent leur contrôle/verrou Story et refusent déjà les archives. Une confirmation de purge n’existe donc pas pour un dossier actif ; son prochain archivage renouvelle la révision. L’empreinte SHA-256 inclut en plus toutes les colonnes et ids des dépendances triées, y compris les reports : changer un motif ou un enfant à nombre égal invalide aussi la confirmation. Aucun contenu n’est mis dans un reçu ou un log.

Le service [story_deletion_support.py](../../backend/api/v1/views/story_deletion_support.py) réalise :

1. Relire sous verrou partagé le compte administrateur actif ; conserver le contrôle CSRF global avant la vue.
2. Vérifier FK activées et schéma attendu, dont comment_id NOT NULL et absence des anciennes colonnes. Refuser un report orphelin historique ; sa portée inconnue impose un refus sûr. Sous MySQL, vérifier les tables concernées en InnoDB et foreign_key_checks actif, sans prétendre que cette branche est testée sur le moteur réel.
3. Verrouiller Story par id, puis commentaires, théories, votes, mises à jour et reports ; lectures courantes et ordre stable. Vérifier existence, archive et révision conforme. Limite globale : 10 000 dépendances, refus sans écriture au-delà, jamais de troncature silencieuse.
4. Contrôler confirmation signée HMAC SHA-256, acteur/session/action/cible/expiration, empreinte et If-Match exact.
5. Réserver une nouvelle révision par UPDATE conditionnel id + ancienne révision + état archivé ; exiger une ligne. La réservation complète les verrous et fait partie du rollback.
6. Supprimer explicitement reports joints aux commentaires du dossier, théories, votes, updates, commentaires, puis Story avec la révision réservée. Comparer tous les nombres, vérifier l’absence des ids capturés, puis **un seul commit**. Aucune suppression remontante vers User/Category/Proposal, aucun commit intermédiaire.
7. Toute erreur avant commit validé annule réservation et toutes les suppressions. Les tests injectent l’erreur **après de vrais DELETE** de reports ou de commentaires et comparent les neuf tables relues. Si l’accusé de COMMIT est perdu, répondre 503 DELETE_STATUS_UNKNOWN : un rollback local ne prouve pas un échec serveur. Aucun reçu ni replay de succès inventé.

Les opérations Core ciblées ne dépendent pas de la suppression ORM des collections. Les FK restent actives comme défense relationnelle ; le code ne désactive aucune contrainte et expire la session après succès. Les verrous SQL réels et leurs interactions sur InnoDB restent à valider sur une cible autorisée.

## 5. Routes, réponses et interface

Préfixe `/api/v1`. Trois nouvelles opérations ; **32 opérations OpenAPI, 33 règles Flask avec static et les règles distinctes GET/DELETE du détail**. Toutes privées, réponses Cache-Control no-store.

| Route | Contrat |
|---|---|
| GET `/admin/stories/{story_id}/deletion-preview` | Archive seulement ; titre/révision, cinq compteurs, resource_etag, preview_token et expiration ; lecture sans écriture ni verrou conservé pendant le dialogue |
| POST `/admin/stories/{story_id}/deletion-confirmations` | JSON exact preview_token, typed_title, confirm_contributions=true ; titre exact et état frais relus ; renvoie confirmation_token avec la même expiration |
| DELETE `/admin/stories/{story_id}` | Aucun corps ; CSRF, If-Match fort exact, X-Deletion-Confirmation ; succès 200 avec code STORY_DELETED, deleted_story (id/révision) et deleted_counts |

Les signatures sont valables **300 secondes au total depuis l’aperçu**, liées à la session et non prolongées par le POST. JSON de confirmation ≤ 16 Kio, titre ≤ 200 caractères, tokens ASCII ≤ 4096 octets ; champs inconnus et clés JSON dupliquées refusés. If-Match n’accepte ni wildcard, ni liste, ni tag faible. Pas d’Idempotency-Key ni table de reçus dans cette solution S2. Le validateur porte sur l’état de la Story ; le POST intermédiaire le contrôle dans le jeton, pas par un If-Match de ressource différente.

Statuts explicites : 400 requête/titre invalide ; 401 session absente ; 403 rôle/bannissement/CSRF/signature ; 404 cible absente ou id hors domaine ; 409 dossier actif, dépendances/révision incompatibles ou volume dépassé ; 412 confirmation/état périmé ; 428 précondition absente ; 500 erreur SQL annulée sans détail brut ; 503 intégrité/moteur indisponible, verrou/délai reconnu ou COMMIT indéterminé. Le filtre CSRF peut refuser avant la vue. Une répétition après suppression donne **404**, jamais un faux reçu 200.

Le tableau propose Supprimer définitivement **uniquement dans les archives**. Dialogue natif, titre et nombres des dépendances, saisie exacte, case d’acquittement, Annuler/Échap et focus ; texte externe construit avec textContent. Une seule intention en cours, verrou jusqu’à la relecture globale ; anciennes réponses/403 écartés après départ/retour. Aucun jeton en localStorage/sessionStorage ni conservation programmée.

### S2 : lecture après timeout et absence de journal

Après DELETE, succès reconnu ou réponse incertaine, relire le détail administratif puis les listes/statistiques. **Aucun DELETE automatique**. Si le serveur confirme explicitement le succès, distinguer ce succès d’une actualisation échouée. Sinon, annoncer présence/absence constatée ou état non vérifié : **sans journal persistant, il n’est pas possible d’attribuer avec certitude cette suppression à la demande ayant perdu sa réponse**. Une présence peut aussi précéder la fin d’une requête encore en cours. Perte de droits : masquer données/actions, ne pas inférer l’issue.

Après purge d’une archive : actifs/résolues/Cold Cases ne diminuent pas une deuxième fois ; Archives -1 ; commentaires et reports globaux diminuent des lignes réellement supprimées ; users et pending restent identiques. Relire les nombres, pas de soustraction locale supposée. Les GET indépendants ne sont pas un instantané global.

## 6. Tests et couverture réellement exécutés

| Suite finale | Résultat |
|---|---|
| Backend | **285 PASS**, 0 échec/erreur/ignoré |
| Frontend | **364 PASS**, 0 échec/annulé/ignoré |
| Lanceur | **8 PASS**, 0 échec/erreur/ignoré |
| Total | **657 PASS** ; les 604 précédents sont historiques, pas additionnés |

**31 nouvelles méthodes backend :** 25 tests de suppression, 6 de migration. **22 nouveaux cas frontend.** Les suites précédentes sont réexécutées avec FK ON partout. Assertions de structure adaptées explicitement : 32 opérations/33 règles, trois protections supplémentaires et remplacement de « aucune route DELETE » par « aucun DELETE sans confirmation ». Le contrat Python/HTTP des signalements reste vérifié. Aucun échec final détecté ; tous les passages exécutés ont réussi.

| Groupes du plan P-01 à P-36 | Preuves et limites actuelles |
|---|---|
| Permissions, CSRF, archive, validation, préconditions, signature/session, titre/accord et expiration | Tests WSGI réels ; corps doublonné et en-têtes faibles/multiples/wildcard refusés |
| Graphe complet/vide, témoins, FK, références historiques incompatibles, type réel et reprise | Migration upgrade/downgrade sur schéma historique minimal fictif ; comparaison avant DDL et sans désactiver les FK ; pas de chaîne historique complète ni de base réelle |
| Rollback après écritures et COMMIT incertain | DELETE réels puis erreur ; neuf tables comparées ; commit réellement réussi puis accusé simulé perdu → 503, absence relue |
| Suppressions répétées, deux administrateurs et restauration/réarchivage | Clients séquentiels, réutilisation d’id et dates remises aux valeurs initiales ; révision distincte invalide le jeton ; **pas de preuve de course multi-connexion** |
| Erreur de verrou/charge | Deadlock simulé sans connexion MySQL ; seuil de volume abaissé pour exercer le refus, pas de test de charge de production |
| Confirmation, annulation, Échap, doubles clics, réponses perdues, anciennes réponses, compteurs | Vrais scripts dans DOM/fetch simulés ; 404 sans attribution, aucune relance, UI nettoyée et succès connu distingué d’une panne de statistiques |
| Reçus, durée et journal d’acteur du plan initial | **Non retenus par S2** : tests d’absence de table/route de reçus ; pas de cycle 30 jours développé |
| Non-régression 6A/6B/6C.1/6D et Swagger | Suites consolidées, fixtures publiques exactes, utilisateurs/bannissement, recherche/filtres et sept compteurs conservés |

NON EXÉCUTÉS : véritables courses SQL multi-connexions et insertions SQL concurrentes, chargements ORM de toutes variantes de cascade, MySQL/Aiven/TLS, migration réelle, déploiement, persistance après redémarrage, navigateur réel/clavier/mobile/accessibilité exhaustive, charge et restauration de sauvegarde. Les FK/cascades et erreurs fictives ne prouvent pas ces points. Les anciens 36 scénarios restent un guide ; le tableau ci-dessus ne revendique pas une exécution exhaustive de chacun.

## 7. Harnais inspecté et preuves

Sources de gardes 6C.1 lues puis copiées dans un dossier neuf. Le seul renforcement Python active/assert les FK à chaque connexion SQLite mémoire ; aucune garde réseau/fichier/secret n’est relâchée. Node garde les mêmes interdictions. Dotenv neutralisé et variables Aiven vidées avant import ; SQLAlchemy/PyMySQL ne peuvent pas ouvrir une base non mémoire. ATTACH/DETACH, sockets/DNS, sous-processus applicatifs, lectures privées et écritures du dépôt bloqués. Sondes séparées avant suites ; **tous les compteurs interdits des suites sont à zéro**. Flask est exercé par WSGI, sans écoute réseau, lanceur simulé.

Les sources ajoutées sont explicitement relues et autorisées dans le manifeste, avec SHA-256. Passages : attempt-1 backend 281 ; attempt-2 complet 653 ; attempt-3 complet 657 après renforcement des cas limites ; attempt-4 complet 657 après sélection explicite de HMAC SHA-256. Ces nombres ne sont pas additionnés. Reçus : `harness-inspection.json`, `manifest-review-2/3/4.json`, `attempt-4/commands.json`, stdout/stderr, `backend.guard.json`, `launcher.guard.json`, `attempt-4/frontend.node-guard.json`.

```powershell
# Dossier de preuves inspecté, hors dépôt ; aucune commande Flask/Alembic réelle.
$preuves6c2 = Join-Path $env:TEMP 'portfolio-lot6c2-implementation-20261031-bpf4frum'
& .\.venv\Scripts\python.exe -I -B (Join-Path $preuves6c2 'run-checks.py') --inspect
& .\.venv\Scripts\python.exe -I -B (Join-Path $preuves6c2 'run-checks.py')
```

## 8. Validation nécessaire avant déploiement et limites

1. Autoriser séparément inventaire, sauvegarde, maintenance, migration et déploiement sur la cible réelle ; **aucune de ces opérations n’est effectuée ici**. Anciens écrivains arrêtés, références historiques validées sans effacement silencieux, migration/reprise complètes avant code actif.
2. Confirmer types/signatures SQL, noms/index/FK, moteur InnoDB et contrôles effectifs, version compatible et éventuels triggers ; tester isolation, verrous, attentes et deadlocks sur moteur autorisé. SQLite ignore les verrous de ligne et le harnais :memory: ne constitue pas un test concurrent partagé.
3. Valider le dialogue dans un navigateur séparément autorisé : clavier, focus, mobile et affichage. Les contrôles DOM ne remplacent pas cette recette.
4. Assumer l’absence de journal : pas de preuve durable d’auteur/commande, pas de replay attribuable après réponse perdue. Surveiller la configuration de logs pour ne pas enregistrer les jetons ou contenus. Aucun mécanisme de conservation/purge de reçus ajouté.
5. Les médias, copies statiques/donnees.js/JSON, exports, caches et sauvegardes restent hors transaction SQL ; une restauration ancienne doit éviter la republication involontaire. La purge d’une Story n’est pas un parcours RGPD d’une personne ; lot 6E non commencé.

**GO pour revue du code et des preuves locales ; aucune autorisation de purge réelle ou de déploiement implicite.** Les commentaires français importants sont dans les véritables fichiers de modèle, migration, service, API et panneau.

## 9. Documentation et conservation finale

README principal/frontend, contrat Swagger, documentation admin/tests/sécurité/démonstration/oral, matrice des 22 remarques, index et fiches sont actualisés. Les 76 questions/réponses courtes historiques sont conservées et contextualisées ; la représentation ER de Report est actualisée sans prétendre à un nouveau rendu navigateur. C-05 peut être considéré livré pour ce périmètre local autorisé, avec réserves de déploiement et recette réelles explicites.

<!-- CONTROLES_IMPLEMENTATION_6C2_START -->

**PASS statique final.** 11 sources Python analysées/compilées en mémoire et 4 JavaScript/CJS vérifiés par node --check. **9 modèles, 11 FK dont les dix originales préservées, 32 opérations API** cohérentes avec Swagger ; aucune table/route de reçus. **191 repères** (172 conservés/recalculés et 19 ajouts), **22 remarques**, C-05 terminé pour ce périmètre local. **900 liens internes dans 25 Markdown**, dont 309 liens de lignes. **76 questions/réponses courtes historiques conservées** ; six sources Mermaid, dont deux ER actualisées, aucun rendu navigateur revendiqué. Branche, HEAD, index, sauvegardes et fichiers hors périmètre conservés ; diff --check passe avec les fins de ligne Windows. Les **65 sources du manifeste final** correspondent aux **657 PASS**, compteurs interdits à zéro et FK ON sur toutes les connexions de test. Reçus : final-validation.json, file-inventory.json et documentation-updates.json hors dépôt.

<!-- CONTROLES_IMPLEMENTATION_6C2_END -->

**Arrêt après lot 6C.2 autorisé : aucune donnée réelle supprimée, aucune migration MySQL/Aiven, aucun accès au `.env` privé, navigateur réel, configuration Windows, changement de branche, commit, push ou développement 6E.**

## 10. Inventaire exact de cette intervention

24 fichiers préexistants modifiés :

```text
README.md
backend/api/v1/swagger.json
backend/api/v1/views/admin_stories.py
backend/api/v1/views/comments.py
backend/api/v1/views/index.py
backend/models.py
backend/tests/test_api_errors_stats_login.py
backend/tests/test_story_archiving.py
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
frontend/admin-dashboard.js
frontend/admin-stories.js
frontend/api.js
```

6 fichiers créés :

```text
backend/api/v1/views/story_deletion_support.py
backend/tests/test_report_migration.py
backend/tests/test_story_deletion.py
docs/soutenance/BILAN_LOT6C2_IMPLEMENTATION.md
frontend/tests/admin-deletion.test.cjs
migrations/versions/c6c200000001_comment_reports_and_story_revision.py
```
