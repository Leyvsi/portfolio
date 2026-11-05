# Lot 6C — phase 1 : archivage réversible

> Archive pédagogique datée : les résultats et descriptions ci-dessous concernent le lot indiqué. Les anciens repères de ligne ne décrivent pas la version candidate. Pour préparer la soutenance actuelle, consulter les quatre fiches et le référentiel reliés au sommaire.

[Sommaire](README.md) · [Audit préalable](BILAN_LOT6C_AUDIT.md) · [Tests](TESTS_ET_VALIDATION.md) · [Matrice du jury](SUIVI_REMARQUES_JURY.md) · [Index du code](INDEX_CODE_JURY.md)

**Développement commencé le 30 octobre et clôturé le 31 octobre 2026.** Phase 1 uniquement : archivage et restauration. **604 PASS**, aucune suppression définitive, aucun développement 6E. Le code est livré localement ; aucune base réelle n’est migrée et aucun déploiement n’est effectué. La demande de suppression définitive du jury **n’est pas complètement terminée**.

> L'archivage masque un dossier du site public tout en conservant ses données pour une restauration éventuelle. Il ne constitue pas une suppression définitive.

## 1. État initial et conservation du travail

Branche `feature/frontend-api-integration`, HEAD `07a9f03ea0a3bdad4a07066fdd7bab1997cc158b`. Avant modification : **37 fichiers suivis modifiés et 25 fichiers non suivis** (24 entrées groupées dans le premier statut court), aucun changement indexé. Le rapport d’audit 6C a été lu avant développement.

Sauvegarde locale contrôlée : `$env:TEMP/portfolio-lot6c-phase1-20261030-673diw95`. `baseline.json` conserve statut, index, inventaire prévisionnel et SHA-256 de 82 sources publiques. `backup/` contient les copies ciblées avant édition ; l’assertion historique de nombre de routes a été ajoutée à cet inventaire et sauvegardée avant sa modification. Aucun `.env`, cookie, certificat, secret ou fichier de base n’est copié. Les fichiers préexistants hors périmètre sont contrôlés par empreinte. Aucun reset, checkout, stash, commit ou push.

## 2. Modèle et migration

Un seul champ : `Story.archived_at`, `DateTime` nullable, date UTC selon la convention existante du projet.

| Valeur | État |
|---|---|
| NULL | Dossier actif, publiquement visible |
| Date UTC | Archive, visible seulement par les lectures administratives |

Un booléen ferait double emploi. La date fournit la trace minimale du retrait courant ; il n’y a ni table de journal, ni historique complet, ni acteur persistant. Restaurer remet NULL. `updated_at` évolue lors d’une transition effective ; le contenu, la date de création, le slug et l’id restent conservés. Une opération répétée ne change pas la date d’archivage.

Migration préparée : [c6c100000001_add_story_archive_date.py](../../migrations/versions/c6c100000001_add_story_archive_date.py), après `82deda84bc35`. L’ajout nullable sans défaut laisse les anciennes lignes actives, sans nouvelle table, FK, contrainte ou règle CASCADE. **Non appliquée à une base réelle.** Seule sa fonction `upgrade` a été exercée sur un schéma fictif minimal SQLite mémoire, sans charger `migrations/env.py`. La chaîne complète historique et `downgrade` ne sont pas validés par ce test.

Un schéma existant doit recevoir cette migration dans une intervention séparément autorisée **avant déploiement du code**. `create_all()` ne transforme pas les tables déjà présentes. Retirer la colonne en downgrade perdrait les états d’archive et permettrait leur republication avec l’ancien code : cette conséquence est commentée dans la migration. Aucun ordre Alembic n’a été exécuté sur une base réelle, même pour lire sa révision.

## 3. Contrat et protections

Les quatre opérations sont sous `/api/v1` et décrites dans [Swagger](../../backend/api/v1/swagger.json), désormais **29 opérations** au total, **30 règles Flask** avec `static`.

| Méthode / chemin | Résultat |
|---|---|
| GET `/admin/stories` | Actifs par défaut ; `state=archived` ou `state=all` acceptés ; autre valeur : 400 |
| GET `/admin/stories/{story_id}` | Dossier actif ou archivé, ses théories, commentaires, mises à jour et nombre de votes ; reports toujours lisibles par `/admin/reports` |
| POST `/admin/stories/{story_id}/archive` | 200 `{status: "success", changed, story}` ; `changed=false` si déjà archivé |
| POST `/admin/stories/{story_id}/restore` | Même contrat ; `changed=false` si déjà actif |

Toutes exigent une session, un compte existant non banni et `is_admin` relu en base. Un visiteur reçoit 401, un compte ordinaire/banni 403 ; un rôle falsifié dans la session n’accorde aucun droit. Les POST exigent le CSRF global. Aucun corps JSON requis : l’id vient uniquement du chemin et l’action de la route ; aucun champ envoyé ne permet de modifier le contenu ou une autre cible. Domaine d’id : 1 à 2147483647 ; cible inexistante, hors domaine ou chemin mal formé : JSON 404. Les réponses privées portent `Cache-Control: no-store`.

L’opération demande un verrou Story, relit l’état, affecte seulement la date si nécessaire, effectue un flush puis un commit. Une exception SQL entraîne rollback et JSON 500 sans détails sensibles ; le contrôle du rôle est inclus dans cette gestion. Le test injecte une erreur au commit **après un vrai flush** et vérifie les neuf tables après relecture, pour archive et restauration. Aucun appel à `Session.delete`, retrait d’enfant d’une collection ou DELETE de dossier.

## 4. Lectures et contributions

| Entrée publique | Dossier archivé |
|---|---|
| GET `/stories` | Exclu de la liste, donc aussi des sélecteurs et cartes utilisant cette source |
| GET `/stories/slug/{slug}` | 404, y compris avec une session administrateur |
| GET `/stories/{id}/theories`, `/comments` | 404 |
| GET `/coldcases/{id}/updates` | 404 |
| POST théorie, commentaire, vote | 404, aucune création |
| POST like par id de théorie/commentaire | Parent vérifié, 404, aucun incrément |
| POST `/comments/{id}/report` et `/reports` | Parent du commentaire vérifié, 404, aucun nouveau signalement |

Le helper [story_visibility.py](../../backend/api/v1/views/story_visibility.py) centralise le filtre et demande le même verrou parent pour tous les écrivains. La restauration republie le même id/slug et les contributions existantes ; l’unicité du vote utilisateur/dossier reste applicable.

Les quatre collections enfants et les dix FK restent inchangées. Théories avec auteur NULL, commentaires avec pseudo copié, likes, votes, mises à jour et reports multiples sont conservés. Les reports restent des cibles textuelles sans FK : cette phase ne les convertit ni ne les nettoie. Users, categories, proposals et les données du dossier témoin restent conservés.

Les ressources statiques, médias, éventuelles copies dans `donnees.js`/JSON, caches externes et contenus déjà reçus ne sont pas rappelés ni purgés par l’archivage SQL. Les parcours actifs n’utilisent pas ces jeux statiques en repli. Il ne s’agit ni d’effacement complet de toutes copies ni d’un traitement RGPD.

## 5. Tableau et statistiques

Actions Archiver/Restaurer avec confirmation native explicite, statuts Actif/Archivé, filtre Actifs / Archives / Tous, recherche/catégorie conservées. La consultation privée montre le récit, les contributions et les votes conservés ; une archive n’a pas de lien vers la fiche publique. Les textes non fiables passent par `textContent`.

Une seule soumission peut rester en cours ; le verrou couvre aussi la relecture globale. Un timeout, JSON illisible, réponse incohérente ou erreur réseau ne prouve pas une réussite : aucune relance automatique du POST, relecture du serveur et affichage de l’état constaté. Si la relecture échoue, listes/actions masquées et compteurs `—`, avec invitation à Actualiser. Réponses anciennes succès/401/403 écartées par version ; départ/retour et perte d’accès nettoient les archives. Le focus revient sur Actualiser après la relecture, même échouée ; annuler préserve le bouton original. Boutons/select natifs et grille responsive existante réutilisés.

| Compteur | Définition conservée ou précisée |
|---|---|
| Dossiers | Nombre de lignes de GET public `/stories`, **actifs seulement** |
| Résolues / Cold Cases | Classement frontend existant 1/2 sur ces actifs ; catégories inconnues conservées dans le total |
| Utilisateurs | Global, inchangé |
| Commentaires | Toutes les lignes, **archives incluses**, pour compatibilité 6D |
| Signalements | Toutes les lignes et tous statuts, **archives incluses**, inchangé |
| Propositions en attente | Statut exact `pending` dans la liste privée, aucun lien à Story |
| Archives | Nombre de lignes de la lecture privée, affiché séparément des sept cartes |

Les GET séparés ne constituent pas un instantané transactionnel global. Si le même id apparaît simultanément dans les lectures active/archives, le tableau refuse l’ensemble plutôt que d’afficher un doublon ou des actions ambiguës. Un changement après les lectures reste possible : Actualiser est manuel et aucune surveillance continue n’est ajoutée.

## 6. Scénarios obligatoires et preuves

| Exigence utilisateur | Preuve automatique |
|---|---|
| 1. Administrateur autorisé | Archive persistée, un commit, date et réponse explicites |
| 2–3. Lecteur/visiteur refusés | Deux actions, banni, utilisateur absent et rôle de session falsifié |
| 4. CSRF absent/invalide | Deux actions ; manquant, vide, faux et non ASCII |
| 5–6. Cible absente/répétition | Ids invalides et manquants 404 ; répétition `changed=false`, date stable |
| 7–8. Public liste/slug | Liste sans archive ; accès direct 404 pour visiteur, membre et admin |
| 9. Contributions refusées | Les sept points d’entrée, plus les trois lectures de contributions |
| 10–11. Conservation | Comparaison réelle des neuf tables, reports multiples et autre type préservés |
| 12. Consultation admin | Filtres privés, contenus et enfants, accès privé et erreurs testés |
| 13–14. Restauration/réapparition | Mêmes id/slug/contenus ; vote existant reste unique ; nouvelle contribution possible |
| 15. Statistiques | Deux catégories archivées/restaurées, agrégats globaux et pending stables ; sept compteurs DOM |
| 16. Annulation | Aucune écriture, action originale conservée |
| 17. Double soumission | Un POST pendant écriture puis relecture ; deux clients admin répètent une transition sans second effet |
| 18. API/timeout | Erreurs avant/après commit simulé, JSON/DTO incohérents, timeout et relecture échouée |
| 19. Rollback SQL | Erreur après vrai flush archive/restauration ; neuf tables identiques après rollback ; erreur de lecture du rôle gérée |
| 20. Non-régression 6A/6B/6D | Suites existantes réexécutées, utilisateurs/bannissement, recherche/filtres et sept compteurs conservés |

Tests : [19 tests backend 6C](../../backend/tests/test_story_archiving.py), [20 cas frontend archives](../../frontend/tests/admin-archives.test.cjs), plus quatre cas supplémentaires des boucles historiques du tableau exercés sur la nouvelle lecture privée. **43 tests de plus que les 561 historiques**, sans addition de campagnes.

| Suite finale | Résultat |
|---|---|
| Backend | **254 PASS**, 0 échec/erreur/ignoré |
| Frontend | **342 PASS**, 0 échec/annulé/ignoré |
| Lanceur | **8 PASS**, 0 échec/erreur/ignoré |
| Total | **604 PASS** |

Premier passage : 251/253 backend, 342 frontend et 8 lanceur réussis. Deux assertions de tests ajustées : 26 règles historiques deviennent 30 ; le compte banni vide sa session, donc sa session fictive doit être recréée avant chaque route vérifiée séparément. Une gestion JSON des erreurs SQL pendant la relecture du rôle et un rétablissement du focus/annulation de lecture ont ensuite été ajoutés et testés au deuxième passage. Les premières sorties et le reçu de revue du manifeste restent conservés. Aucun garde n’est assoupli. **Aucune régression fonctionnelle restante constatée dans les suites exécutées.**

## 7. Isolation et limites de concurrence

Le harnais 6D est lu avant usage puis copié dans un dossier de preuves neuf. Ses gardes Python/Node sont inchangés. Les cinq nouveaux fichiers de code/tests/migration sont autorisés explicitement, avec SHA-256 et reçu de revue. Environnement minimal, paramètres Aiven vides et dotenv neutralisé **avant import applicatif** ; MySQL et bases fichier, ATTACH/DETACH, sockets/DNS, sous-processus applicatifs, lectures privées et écritures du dépôt bloqués. Les sondes vérifient les refus avant entrée/sortie, leurs compteurs attendus étant séparés. **Tous les compteurs interdits des suites sont à zéro.**

La suite 6C active `PRAGMA foreign_keys=ON` hors transaction puis vérifie son état et `foreign_key_check`. Les anciens tests gardent leur configuration ; ils ne prouvent pas les cascades de purge. Flask est exercé par client WSGI, sans serveur ni port. Node exécute les vrais scripts avec DOM et fetch simulés. Le lanceur est simulé.

Les simulations couvrent double clic, maintien du verrou pendant relecture, réponse tardive après départ/retour, refus tardif, état actif/archive chevauchant et deux clients admin séquentiels. **Ce n’est pas une preuve de concurrence SQL multi-connexion** : `:memory:` et les gardes ne sont pas élargis à une base fichier/URI partagée. Les appels `FOR UPDATE` sont conçus pour sérialiser transitions et contributions sur le parent sous InnoDB ; SQLite les ignore. Deux transitions opposées autorisées suivent l’ordre des verrous, le dernier état validé l’emporte ; aucun ETag ou journal d’opération n’est ajouté pour cette phase réversible.

MySQL/Aiven, isolation InnoDB, deadlocks, collations, schéma/FK déployés, migration réelle et charge restent à valider séparément. Edge réel, accessibilité exhaustive, rendu responsive/clavier, déploiement et durabilité après redémarrage sont **NON EXÉCUTÉS**. Les 604 PASS ne démontrent pas ces propriétés.

## 8. Documents et vérifications finales

README principal/frontend, contrat OpenAPI, documentation admin/sécurité/démonstration/tests, matrice à 22 remarques, index fichier/fonction/ligne et les quatre fiches sont actualisés. Les 76 questions et réponses courtes historiques et les sources Mermaid sont conservées. L’audit 6C et les bilans 6A/6B/6D restent historiques, sans réécriture de leurs résultats.

<!-- CONTROLES_6C_PHASE1_START -->

**PASS statique final.** 12 sources Python analysées/compilées en mémoire, 7 JavaScript/CJS vérifiés par `node --check`. **29 opérations API** cohérentes avec Swagger ; **172 repères** (155 conservés/recalculés et 17 ajouts), **22 remarques**, C-05 PARTIEL. **826 liens internes dans 21 Markdown**, dont 271 liens de lignes ; **76 réponses historiques et six sources Mermaid préservées**. Branche, HEAD, index et fichiers préexistants hors périmètre conservés ; `git diff --check` passe avec les fins de ligne Windows. Les 60 sources du manifeste correspondent au passage final de **604 PASS** ; gardes de 6D inchangés, compteurs interdits à zéro. Reçus : `final-validation.json`, `file-inventory.json`, `documentation-updates.json`.

<!-- CONTROLES_6C_PHASE1_END -->

## 9. Ce qui reste nécessaire à la suppression définitive

C-05 reste **PARTIEL**, et non terminé. Une phase ultérieure exigera une autorisation propre, la politique de traitement des reports sans FK, un aperçu et des préconditions contre confirmations périmées, la trace et les durées retenues, la transaction de suppression et ses cascades SQL/ORM réellement vérifiées, ainsi que les scénarios concurrents sur le moteur cible. Il faudra examiner séparément médias partagés, copies statiques, exports, caches et sauvegardes/restaurations. Aucun de ces travaux de purge ni le lot 6E n’est commencé.

**Arrêt en fin de phase 1.** Aucune donnée réelle ni configuration Windows modifiée, aucun `.env` privé lu, aucun accès MySQL/Aiven, aucune migration réelle, aucun navigateur Edge réel, aucun commit ni push.

## 10. Inventaire exact de cette phase

30 fichiers préexistants modifiés :

```text
README.md
backend/api/v1/swagger.json
backend/api/v1/views/__init__.py
backend/api/v1/views/comments.py
backend/api/v1/views/histoires.py
backend/api/v1/views/index.py
backend/api/v1/views/theories.py
backend/models.py
backend/tests/test_api_errors_stats_login.py
backend/tests/test_swagger.py
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
frontend/admin-stories.js
frontend/api.js
frontend/tests/admin-dashboard.test.cjs
frontend/tests/admin-stories.test.cjs
frontend/tests/admin-users.test.cjs
```

6 fichiers créés :

```text
backend/api/v1/views/admin_stories.py
backend/api/v1/views/story_visibility.py
backend/tests/test_story_archiving.py
docs/soutenance/BILAN_LOT6C_PHASE1.md
frontend/tests/admin-archives.test.cjs
migrations/versions/c6c100000001_add_story_archive_date.py
```
