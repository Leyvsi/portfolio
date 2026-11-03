# Index courant des fonctions — lot 6H.1

> Etat de diffusion scolaire du 3 novembre 2026 : suivre le [guide actuel](../../LIVRAISON_SCOLAIRE.md) et la [validation scolaire](VALIDATION_SCOLAIRE.md). Les sections de campagnes anterieures et leurs commandes sont historiques ; elles ne remplacent pas la procedure actuelle. Les chemins sous `C:\chemin\utilisateur` sont des exemples anonymises. Les archives internes signalees sont conservees localement.

Repères statiques du 2 novembre 2026 ; aucun import de l’application ou lancement requis. Les noms ci-dessous existent réellement ; les lignes visent leur définition. Les fonctions JavaScript locales sont repérées dans leur fichier et ne sont pas présentées comme des API globales.

[Supports de présentation](SUPPORT_JURY_LOT6H1.md) · Ancien index conservé (archive interne non livree) · Audit (archive interne non livree)

## Serveur et sécurité

| Fichier et ligne | Nom exact |
|---|---|
| [run_local.py:17](../../run_local.py#L17) | `create_local_app` |
| [run_local.py:68](../../run_local.py#L68) | `main` |
| [backend/index.py:156](../../backend/index.py#L156) | `get_csrf_token` |
| [backend/index.py:171](../../backend/index.py#L171) | `protect_session_requests_from_csrf` |
| [backend/index.py:245](../../backend/index.py#L245) | `get_stats` |
| [backend/index.py:269](../../backend/index.py#L269) | `login_user` |
| [backend/index.py:342](../../backend/index.py#L342) | `get_current_user` |
| [backend/index.py:366](../../backend/index.py#L366) | `logout_user` |
| [backend/api/v1/views/permissions.py:10](../../backend/api/v1/views/permissions.py#L10) | `get_authenticated_user` |
| [backend/api/v1/views/permissions.py:52](../../backend/api/v1/views/permissions.py#L52) | `admin_required` |

## Données, contraintes et modération

| Fichier et ligne | Nom exact |
|---|---|
| [backend/models.py:18](../../backend/models.py#L18) | `User` |
| [backend/models.py:68](../../backend/models.py#L68) | `Category` |
| [backend/models.py:83](../../backend/models.py#L83) | `Story` |
| [backend/models.py:215](../../backend/models.py#L215) | `Theory` |
| [backend/models.py:281](../../backend/models.py#L281) | `Comment` |
| [backend/models.py:433](../../backend/models.py#L433) | `CommentLike` |
| [backend/models.py:376](../../backend/models.py#L376) | `Vote` |
| [backend/models.py:455](../../backend/models.py#L455) | `Proposal` |
| [backend/models.py:512](../../backend/models.py#L512) | `Report` |
| [backend/models.py:586](../../backend/models.py#L586) | `ColdCaseUpdate` |
| [backend/api/v1/views/comments.py:13](../../backend/api/v1/views/comments.py#L13) | `comment_to_dict` |
| [backend/api/v1/views/comments.py:32](../../backend/api/v1/views/comments.py#L32) | `get_story_comments` |
| [backend/api/v1/views/comments.py:56](../../backend/api/v1/views/comments.py#L56) | `post_story_comment` |
| [backend/api/v1/views/comments.py:103](../../backend/api/v1/views/comments.py#L103) | `like_comment` |
| [backend/api/v1/views/comments.py:111](../../backend/api/v1/views/comments.py#L111) | `report_comment` |
| [backend/api/v1/views/index.py:17](../../backend/api/v1/views/index.py#L17) | `post_report` |
| [backend/api/v1/views/index.py:110](../../backend/api/v1/views/index.py#L110) | `get_admin_reports` |
| [backend/api/v1/views/index.py:139](../../backend/api/v1/views/index.py#L139) | `ban_user` |
| [backend/api/v1/views/index.py:147](../../backend/api/v1/views/index.py#L147) | `ban_user_by_id` |
| [backend/api/v1/views/likes.py:13](../../backend/api/v1/views/likes.py#L13) | `legacy_likes_compatible` |
| [backend/api/v1/views/likes.py:19](../../backend/api/v1/views/likes.py#L19) | `like_state` |
| [backend/api/v1/views/likes.py:27](../../backend/api/v1/views/likes.py#L27) | `handle_like` |
| [backend/api/v1/views/likes.py:85](../../backend/api/v1/views/likes.py#L85) | `personal_story_like` |
| [backend/api/v1/views/likes.py:90](../../backend/api/v1/views/likes.py#L90) | `personal_comment_like` |
| [backend/api/v1/views/admin_stories.py:52](../../backend/api/v1/views/admin_stories.py#L52) | `get_admin_stories` |
| [backend/api/v1/views/admin_stories.py:71](../../backend/api/v1/views/admin_stories.py#L71) | `get_admin_story` |
| [backend/api/v1/views/admin_stories.py:92](../../backend/api/v1/views/admin_stories.py#L92) | `set_story_archive` |
| [backend/api/v1/views/admin_stories.py:117](../../backend/api/v1/views/admin_stories.py#L117) | `archive_story` |
| [backend/api/v1/views/admin_stories.py:123](../../backend/api/v1/views/admin_stories.py#L123) | `restore_story` |
| [backend/api/v1/views/admin_stories.py:129](../../backend/api/v1/views/admin_stories.py#L129) | `get_story_deletion_preview` |
| [backend/api/v1/views/admin_stories.py:136](../../backend/api/v1/views/admin_stories.py#L136) | `confirm_story_deletion` |
| [backend/api/v1/views/admin_stories.py:143](../../backend/api/v1/views/admin_stories.py#L143) | `delete_story_permanently` |
| [backend/api/v1/views/story_deletion_support.py:74](../../backend/api/v1/views/story_deletion_support.py#L74) | `require_integrity` |
| [backend/api/v1/views/story_deletion_support.py:118](../../backend/api/v1/views/story_deletion_support.py#L118) | `snapshot` |
| [backend/api/v1/views/story_deletion_support.py:188](../../backend/api/v1/views/story_deletion_support.py#L188) | `deletion_preview` |
| [backend/api/v1/views/story_deletion_support.py:203](../../backend/api/v1/views/story_deletion_support.py#L203) | `confirm_deletion` |
| [backend/api/v1/views/story_deletion_support.py:220](../../backend/api/v1/views/story_deletion_support.py#L220) | `delete_story` |

## Frontend et DOM

| Fichier et ligne | Nom exact |
|---|---|
| [frontend/api.js:8](../../frontend/api.js#L8) | `apiRequest` |
| [frontend/api.js:126](../../frontend/api.js#L126) | `getCurrentUser` |
| [frontend/api.js:133](../../frontend/api.js#L133) | `logout` |
| [frontend/api.js:246](../../frontend/api.js#L246) | `getAdminReports` |
| [frontend/app.js:82](../../frontend/app.js#L82) | `makeCard` |
| [frontend/app.js:121](../../frontend/app.js#L121) | `loadStories` |
| [frontend/app.js:154](../../frontend/app.js#L154) | `loadStory` |
| [frontend/app.js:522](../../frontend/app.js#L522) | `refreshSession` |
| [frontend/app.js:540](../../frontend/app.js#L540) | `disconnect` |
| [frontend/comments.js:2](../../frontend/comments.js#L2) | `mountStoryComments` |
| [frontend/likes.js:2](../../frontend/likes.js#L2) | `createLikeControl` |
| [frontend/likes.js:154](../../frontend/likes.js#L154) | `mountStoryLike` |
| [frontend/admin-dashboard.js:116](../../frontend/admin-dashboard.js#L116) | `reportCard` |
| [frontend/admin-dashboard.js:155](../../frontend/admin-dashboard.js#L155) | `displayData` |
| [frontend/admin-dashboard.js:183](../../frontend/admin-dashboard.js#L183) | `loadDashboard` |
| [frontend/admin-users.js:5](../../frontend/admin-users.js#L5) | `createAdminUsersPanel` |
| [frontend/admin-stories.js:5](../../frontend/admin-stories.js#L5) | `createAdminStoriesPanel` |

## Kit local

| Fichier et ligne | Nom exact |
|---|---|
| [tools/recette_lot6g4.py:42](../../tools/recette_lot6g4.py#L42) | `validate_sources` |
| [tools/recette_lot6g4.py:65](../../tools/recette_lot6g4.py#L65) | `Isolation` |
| [tools/recette_lot6g4.py:142](../../tools/recette_lot6g4.py#L142) | `seed` |
| [tools/recette_lot6g4.py:163](../../tools/recette_lot6g4.py#L163) | `seven_counts` |
| [tools/recette_lot6g4.py:193](../../tools/recette_lot6g4.py#L193) | `check_journey` |
| [tools/recette_lot6g4.py:283](../../tools/recette_lot6g4.py#L283) | `main` |

## Migrations candidates

Ces fichiers sont des sources à examiner ; cliquer un lien ne les applique pas. Leurs sept révisions forment une chaîne unique terminant sur `c6g200000001`.

| Fichier | Révision | Parent |
|---|---|---|
| [migrations/versions/3111f5767fc6_ajoute_les_regles_on_delete.py](../../migrations/versions/3111f5767fc6_ajoute_les_regles_on_delete.py) | `3111f5767fc6` | `921687c1bd7c` |
| [migrations/versions/82deda84bc35_remove_legacy_comment_reports_counter.py](../../migrations/versions/82deda84bc35_remove_legacy_comment_reports_counter.py) | `82deda84bc35` | `a590c8aac613` |
| [migrations/versions/921687c1bd7c_baseline_schema.py](../../migrations/versions/921687c1bd7c_baseline_schema.py) | `921687c1bd7c` | `None` |
| [migrations/versions/a590c8aac613_add_reports_bans_and_cold_case_updates.py](../../migrations/versions/a590c8aac613_add_reports_bans_and_cold_case_updates.py) | `a590c8aac613` | `3111f5767fc6` |
| [migrations/versions/c6c100000001_add_story_archive_date.py](../../migrations/versions/c6c100000001_add_story_archive_date.py) | `c6c100000001` | `82deda84bc35` |
| [migrations/versions/c6c200000001_comment_reports_and_story_revision.py](../../migrations/versions/c6c200000001_comment_reports_and_story_revision.py) | `c6c200000001` | `c6c100000001` |
| [migrations/versions/c6g200000001_add_comment_likes.py](../../migrations/versions/c6g200000001_add_comment_likes.py) | `c6g200000001` | `c6c200000001` |

La migration des likes refuse les compteurs historiques incompatibles ; aucune reprise automatique. Les fonctions Alembic, les types MySQL et les garanties DDL réelles restent hors exécution en 6H.1.
