# Index courant des fonctions — lot 6H.1

> Archive pédagogique datée : les résultats et descriptions ci-dessous concernent le lot indiqué. Les anciens repères de ligne ne décrivent pas la version candidate. Pour préparer la soutenance actuelle, consulter les quatre fiches et le référentiel reliés au sommaire.

> Copie publique de référence : les chemins personnels et liens de travail internes sont retirés. Les preuves et commandes historiques gardent leur date et leur périmètre ; utiliser le README actuel pour le lancement.

Repères statiques du 2 novembre 2026 ; aucun import de l’application ou lancement requis. Les noms ci-dessous étaient ceux du lot ; utiliser les fiches et le référentiel actuels pour les coordonnées vérifiées. Les fonctions JavaScript locales sont repérées dans leur fichier et ne sont pas présentées comme des API globales.

[Supports de présentation](SUPPORT_JURY_LOT6H1.md) · [Ancien index conservé](INDEX_CODE_JURY.md) · [Audit](BILAN_LOT6H1.md)

## Serveur et sécurité

| Fichier (repère historique) | Nom exact |
|---|---|
| [run_local.py](../../run_local.py) | `create_local_app` |
| [run_local.py](../../run_local.py) | `main` |
| [backend/index.py](../../backend/index.py) | `get_csrf_token` |
| [backend/index.py](../../backend/index.py) | `protect_session_requests_from_csrf` |
| [backend/index.py](../../backend/index.py) | `get_stats` |
| [backend/index.py](../../backend/index.py) | `login_user` |
| [backend/index.py](../../backend/index.py) | `get_current_user` |
| [backend/index.py](../../backend/index.py) | `logout_user` |
| [backend/api/v1/views/permissions.py](../../backend/api/v1/views/permissions.py) | `get_authenticated_user` |
| [backend/api/v1/views/permissions.py](../../backend/api/v1/views/permissions.py) | `admin_required` |

## Données, contraintes et modération

| Fichier (repère historique) | Nom exact |
|---|---|
| [backend/models.py](../../backend/models.py) | `User` |
| [backend/models.py](../../backend/models.py) | `Category` |
| [backend/models.py](../../backend/models.py) | `Story` |
| [backend/models.py](../../backend/models.py) | `Theory` |
| [backend/models.py](../../backend/models.py) | `Comment` |
| [backend/models.py](../../backend/models.py) | `CommentLike` |
| [backend/models.py](../../backend/models.py) | `Vote` |
| [backend/models.py](../../backend/models.py) | `Proposal` |
| [backend/models.py](../../backend/models.py) | `Report` |
| [backend/models.py](../../backend/models.py) | `ColdCaseUpdate` |
| [backend/api/v1/views/comments.py](../../backend/api/v1/views/comments.py) | `comment_to_dict` |
| [backend/api/v1/views/comments.py](../../backend/api/v1/views/comments.py) | `get_story_comments` |
| [backend/api/v1/views/comments.py](../../backend/api/v1/views/comments.py) | `post_story_comment` |
| [backend/api/v1/views/comments.py](../../backend/api/v1/views/comments.py) | `like_comment` |
| [backend/api/v1/views/comments.py](../../backend/api/v1/views/comments.py) | `report_comment` |
| [backend/api/v1/views/index.py](../../backend/api/v1/views/index.py) | `post_report` |
| [backend/api/v1/views/index.py](../../backend/api/v1/views/index.py) | `get_admin_reports` |
| [backend/api/v1/views/index.py](../../backend/api/v1/views/index.py) | `ban_user` |
| [backend/api/v1/views/index.py](../../backend/api/v1/views/index.py) | `ban_user_by_id` |
| [backend/api/v1/views/likes.py](../../backend/api/v1/views/likes.py) | `legacy_likes_compatible` |
| [backend/api/v1/views/likes.py](../../backend/api/v1/views/likes.py) | `like_state` |
| [backend/api/v1/views/likes.py](../../backend/api/v1/views/likes.py) | `handle_like` |
| [backend/api/v1/views/likes.py](../../backend/api/v1/views/likes.py) | `personal_story_like` |
| [backend/api/v1/views/likes.py](../../backend/api/v1/views/likes.py) | `personal_comment_like` |
| [backend/api/v1/views/admin_stories.py](../../backend/api/v1/views/admin_stories.py) | `get_admin_stories` |
| [backend/api/v1/views/admin_stories.py](../../backend/api/v1/views/admin_stories.py) | `get_admin_story` |
| [backend/api/v1/views/admin_stories.py](../../backend/api/v1/views/admin_stories.py) | `set_story_archive` |
| [backend/api/v1/views/admin_stories.py](../../backend/api/v1/views/admin_stories.py) | `archive_story` |
| [backend/api/v1/views/admin_stories.py](../../backend/api/v1/views/admin_stories.py) | `restore_story` |
| [backend/api/v1/views/admin_stories.py](../../backend/api/v1/views/admin_stories.py) | `get_story_deletion_preview` |
| [backend/api/v1/views/admin_stories.py](../../backend/api/v1/views/admin_stories.py) | `confirm_story_deletion` |
| [backend/api/v1/views/admin_stories.py](../../backend/api/v1/views/admin_stories.py) | `delete_story_permanently` |
| [backend/api/v1/views/story_deletion_support.py](../../backend/api/v1/views/story_deletion_support.py) | `require_integrity` |
| [backend/api/v1/views/story_deletion_support.py](../../backend/api/v1/views/story_deletion_support.py) | `snapshot` |
| [backend/api/v1/views/story_deletion_support.py](../../backend/api/v1/views/story_deletion_support.py) | `deletion_preview` |
| [backend/api/v1/views/story_deletion_support.py](../../backend/api/v1/views/story_deletion_support.py) | `confirm_deletion` |
| [backend/api/v1/views/story_deletion_support.py](../../backend/api/v1/views/story_deletion_support.py) | `delete_story` |

## Frontend et DOM

| Fichier (repère historique) | Nom exact |
|---|---|
| [frontend/api.js](../../frontend/api.js) | `apiRequest` |
| [frontend/api.js](../../frontend/api.js) | `getCurrentUser` |
| [frontend/api.js](../../frontend/api.js) | `logout` |
| [frontend/api.js](../../frontend/api.js) | `getAdminReports` |
| [frontend/app.js](../../frontend/app.js) | `makeCard` |
| [frontend/app.js](../../frontend/app.js) | `loadStories` |
| [frontend/app.js](../../frontend/app.js) | `loadStory` |
| [frontend/app.js](../../frontend/app.js) | `refreshSession` |
| [frontend/app.js](../../frontend/app.js) | `disconnect` |
| [frontend/comments.js](../../frontend/comments.js) | `mountStoryComments` |
| [frontend/likes.js](../../frontend/likes.js) | `createLikeControl` |
| [frontend/likes.js](../../frontend/likes.js) | `mountStoryLike` |
| [frontend/admin-dashboard.js](../../frontend/admin-dashboard.js) | `reportCard` |
| [frontend/admin-dashboard.js](../../frontend/admin-dashboard.js) | `displayData` |
| [frontend/admin-dashboard.js](../../frontend/admin-dashboard.js) | `loadDashboard` |
| [frontend/admin-users.js](../../frontend/admin-users.js) | `createAdminUsersPanel` |
| [frontend/admin-stories.js](../../frontend/admin-stories.js) | `createAdminStoriesPanel` |

## Kit local

| Fichier (repère historique) | Nom exact |
|---|---|
| [tools/recette_lot6g4.py](../../tools/recette_lot6g4.py) | `validate_sources` |
| [tools/recette_lot6g4.py](../../tools/recette_lot6g4.py) | `Isolation` |
| [tools/recette_lot6g4.py](../../tools/recette_lot6g4.py) | `seed` |
| [tools/recette_lot6g4.py](../../tools/recette_lot6g4.py) | `seven_counts` |
| [tools/recette_lot6g4.py](../../tools/recette_lot6g4.py) | `check_journey` |
| [tools/recette_lot6g4.py](../../tools/recette_lot6g4.py) | `main` |

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
