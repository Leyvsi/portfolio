# Complément aux repères de migrations — lot 6H.22.4

4 novembre 2026. Les quatre fiches, leurs 76 questions et les trois ressources
pédagogiques du lot 6H.21.1 restent conservées dans leur état daté. Les empreintes
et coordonnées de cet inventaire figé désignent ses sources de référence.

La correction de compatibilité SQLite modifie `migrations/env.py` et deux
révisions. Le nouveau module `migrations/sqlite_safety.py` ajoute une enveloppe
transactionnelle. Les anciens numéros de ligne de ces trois fichiers doivent
donc être lus avec le présent complément ; ils ne constituent pas des coordonnées
actualisées de la candidate.

| Source | Repère à rechercher dans la candidate | Évolution |
|---|---|---|
| [Environnement Alembic](../../migrations/env.py) | `run_migrations_online` | Sur SQLite seulement, appelle l’enveloppe avant les révisions. Le chemin MySQL conserve son fonctionnement. |
| [Enveloppe SQLite](../../migrations/sqlite_safety.py) | `sqlite_migration_scope` | Refuse une transaction déjà active ou une intégrité initiale invalide ; suspend les FK hors transaction, ouvre une transaction explicite, contrôle les relations avant commit, puis réactive les FK même après rollback. |
| [Révision a590c8aac613](../../migrations/versions/a590c8aac613_add_reports_bans_and_cold_case_updates.py) | `upgrade` | Conserve le remplissage des comptes existants avec `False`, puis retire le défaut SQL par batch sur SQLite. Refuse les FK actives avant tout DDL pour éviter des cascades pendant la reconstruction de `users`. L’opération MySQL initiale est conservée. |
| [Révision c6g200000001](../../migrations/versions/c6g200000001_add_comment_likes.py) | `inspect_legacy` | Conserve le refus des FK inactives hors de l’enveloppe dédiée ; dans cette enveloppe, exige aussi un contrôle relationnel valide. Les autres préconditions demeurent. |

Une nouvelle révision placée après a590c8aac613 ne pourrait pas réparer un rejeu
qui échoue avant de l’atteindre. La modification historique proposée corrige ici
une incompatibilité de dialecte sans changer l’intention du schéma ; elle exige
une revue avant intégration. Aucun identifiant ni parent de révision ne change.
Ce travail ne prétend pas avoir migré une base réellement déployée.

Les essais passent par les véritables commandes Alembic, `env.py` et la table
`alembic_version`, sur SQLite mémoire vide puis peuplée. Ils vérifient les sept
révisions, la conservation de témoins, les treize FK, `SET NULL`, `CASCADE`, les
défauts et le rollback. [Tests reproductibles](../../tests/test_migrations_sqlite_chain.py).
Les tests MySQL réels et la rétrogradation complète ne sont pas exécutés.

L’enveloppe requiert une maintenance exclusive : aucun écrivain concurrent
pendant une reconstruction. Les modes de démonstration fondés sur `create_all`
restent distincts d’un parcours Alembic. Les lots pédagogiques 6H.21.4 à 6H.21.6
restent à réaliser.

Sources techniques : [batch Alembic](https://alembic.sqlalchemy.org/en/latest/batch.html),
[PRAGMA SQLite](https://www.sqlite.org/pragma.html#pragma_foreign_keys).
