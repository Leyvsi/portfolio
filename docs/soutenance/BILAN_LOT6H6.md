# Lot 6H.6 — commits Git locaux sécurisés

> Archive pédagogique datée : les résultats et descriptions ci-dessous concernent le lot indiqué. Les anciens repères de ligne ne décrivent pas la version candidate. Pour préparer la soutenance actuelle, consulter les quatre fiches et le référentiel reliés au sommaire.

> Copie publique de référence : les chemins personnels et liens de travail internes sont retirés. Les preuves et commandes historiques gardent leur date et leur périmètre ; utiliser le README actuel pour le lancement.

2 novembre 2026. **Les trois commits locaux autorisés sont créés : 79 chemins au total, 36 ajouts et 43 modifications, aucune suppression.** Branche conservée, aucun push, merge, reset, changement de branche ou déploiement. Le code et les images du dossier de travail n'ont pas été modifiés pendant ce lot.

**GO pour la conservation des trois commits locaux. NO-GO pour déclarer la préparation du push achevée. NO-GO pour l'ouverture publique.** Les prochaines étapes de préparation du push sont identifiées ci-dessous, mais aucun transfert n'est autorisé. Les remarques restent **19/22 TERMINÉES : 950/11 % = 86,363636… %, soit 86,36 % arrondi** ; C-02, C-07 et I-02 restent PARTIELLES.

## 1. État initial et autorisation appliquée

Les [bilan 6H.5](BILAN_LOT6H5.md), plan de commits 6H.5 (pièce interne non diffusée), [bilan 6H.4](BILAN_LOT6H4.md) et les instructions du dépôt ont été repris. Les listes fermées et le manifeste validés en 6H.5 sont conservés sans modification. L'autorisation 6H.6 permet ces trois commits locaux et les vérifications nécessaires ; elle ne permet ni push, ni modification applicative, ni base réelle.

| Élément | Avant | Après |
|---|---|---|
| Branche | `feature/frontend-api-integration` | Identique |
| HEAD | `07a9f03ea0a3bdad4a07066fdd7bab1997cc158b` | `3fe35965d5dd88151a7e1cab5bc645e2ddfbfca2` |
| Fichiers suivis | 66 | 102 |
| Suivis modifiés restant dans le dossier de travail | 51 | 8 |
| Fichiers non suivis, comptés individuellement | 133 | 114, dont 17 livrables 6H.6 |
| Indexés / conflits | 0 / 0 | 0 / 0 |
| Index SHA-256 | `cc33bbdc5993495735a8c63e85f22f321b05323716ff29b4af3d0fd8df6c5ec3` | Empreinte finale dans le reçu ; index modifié uniquement par les opérations autorisées |

Les **196 fichiers initiaux examinables** sont hachés avant et après : tous conservent leurs octets. Les trois fichiers exclus des lectures (`frontend/donnees.js`, `frontend/histoires-originales.json`, `docs/soutenance/COMPTES_DEMO.exemple.csv`) conservent présence, taille et date de modification ; aucune identité de contenu n'est prétendue à partir de seules métadonnées. Aucun fichier initial supprimé.

Les autorisations techniques d'écriture hors espace inscriptible ont servi uniquement aux nouveaux dossiers de sauvegarde et aux opérations Git locales. Aucune permission Windows, identité Git ou configuration Git persistante modifiée. Aucun hook actif ou chemin de hooks personnalisé trouvé ; aucun filtre Git externe ni signature configurée à exécuter. L'identité déjà configurée est conservée, sans attribution artificielle des changements à Mélissa, Sylvie ou Mahamadou.

## 2. Sauvegardes vérifiées avant les commits

### Sauvegarde 6H.2 conservée

Sous `[chemin local privé retiré]` :

- `portfolio-lot6h2-20261102-55c80c78` ;
- `recuperation-lot6h2-20261102-55c80c78`.

**197 fichiers par dossier**, ensembles, tailles et empreintes conformes. Reçu final SHA-256 : `9e1c04fb1f5d9c47bd992631b9aaf6815b3531798f3724e649de2e0e511b8fc7`. Sur 169 sources, 166 correspondent encore au projet ; les trois écarts documentaires sont `README.md`, `docs/soutenance/README.md`, `docs/soutenance/SUIVI_REMARQUES_JURY.md`.

### Complément 6H.6 créé et récupéré

- Sauvegarde : `[chemin local privé retiré]`.
- Récupération distincte : `[chemin local privé retiré]`.
- **30 sources documentaires** : les trois versions modifiées et 27 chemins absents de la partie `sources/` de 6H.2. Ces 27 comprennent les 26 livrables des lots 6H.3 à 6H.5 et la sélection 6H.2 déjà présente comme métadonnée dans l'ancienne sauvegarde.
- **32 fichiers par nouvelle copie**, avec sélection et reçu ; récupération faite depuis la nouvelle sauvegarde, puis comparaison de toutes les tailles et empreintes.
- SHA-256 du reçu : `df9624a3b09ebf68b6b95e5b87e0658a81dcfd6b0f8885d8b965cc66d718bc47`.

Preuves : sélection complémentaire (pièce interne non diffusée), reçu de validation (pièce interne non diffusée). Créations exclusives, aucun écrasement ni suppression. Les anciennes copies ont été revérifiées après les opérations.

Ce complément, associé à 6H.2, couvre les 196 sources/documents initiaux examinables. Il ne sauvegarde ni base réelle, ni secrets, ni tout l'historique Git. Les 17 livrables 6H.6 produits au cours du lot restent dans le dossier de travail et ne sont pas annoncés comme inclus dans la copie faite avant les commits.

## 3. Commits créés et contenu exact

| Lot | Commit | Parent | Fichiers | Message |
|---|---|---|---:|---|
| 01 | `4bbb75df2b7860e8373890634f6f39935cdde01c` | `07a9f03ea0a3bdad4a07066fdd7bab1997cc158b` | 46 : 12 A, 34 M | Intégrer les contributions, les likes et l'administration sécurisée |
| 02 | `0d776703219c63951823d3e4f06d015165ddeae8` | `4bbb75df2b7860e8373890634f6f39935cdde01c` | 30 : 21 A, 9 M | Conserver les tests métier et leurs contrats internes |
| 03 | `3fe35965d5dd88151a7e1cab5bc645e2ddfbfca2` | `0d776703219c63951823d3e4f06d015165ddeae8` | 3 : 3 A | Préparer la recette scolaire isolée et son manifeste figé |

Les listes complètes figurent en annexe de ce rapport et dans les reçus 01 (pièce interne non diffusée), 02 (pièce interne non diffusée), 03 (pièce interne non diffusée). Les 79 chemins sont disjoints et égaux aux trois listes autorisées ; aucun ajout destiné seulement à atteindre ce nombre.

Le premier groupe conserve ensemble les dépendances backend/frontend/modèles : administration, permissions, commentaires/signalements, likes, archivage/purge et contrat API. Les migrations sont des **sources candidates enregistrées**, jamais exécutées. Les tests suivent au deuxième commit ; le troisième conserve ensemble le kit, son manifeste et son contrat. La répartition des relectures frontend/Flask/BDD suit les rôles de l'équipe, sans forger une attribution d'auteur Git.

Le brouillon HTML `document interne non publié` est volontairement inclus dans le deuxième commit : le test RGPD en dépend. Il reste interne, non finalisé, hors `frontend/`, sans publication de politique. Les autres documents de soutenance ne sont pas ajoutés par ces commits.

## 4. Contrôles avant et après chaque commit

Les contrôles ont porté sur les modifications, les noms/statuts, les empreintes et les dépendances du manifeste. Les **88 fichiers de sélection et de dépendance** étaient conformes aux empreintes 6H.5 ; seuls les 79 changements prévus nécessitaient une indexation. Les neuf autres étaient déjà suivis et inchangés.

À chaque groupe : branche et parent attendus, absence de conflit, index vide avant indexation, liste fermée explicite, égalité des chemins indexés, statuts A/M uniquement, contrôle des octets indexés, revue du diff et formatage ; après commit : nouveau HEAD, parent, chemins réellement inclus, objets Git, index vide et préservation de tous les fichiers initiaux. Aucun `git add .`, `git add -A`, reset ou nettoyage.

### Incident de contrôle CRLF, sans échec de commit

La première indexation de 46 fichiers a réussi, puis le contrôle auxiliaire utilisant `hash-object --path` a signalé une différence sur `backend/api/v1/views/index.py`. Le diagnostic en lecture seule a établi que Git conservait les CRLF de deux fichiers déjà versionnés : celui-ci et `frontend/styles.css`. Les 46 contenus indexés correspondaient exactement aux sources approuvées, soit en octets bruts, soit après la conversion CRLF vers LF normalement effectuée par Git.

Le **contrôle auxiliaire** a été corrigé pour comparer les octets réellement indexés aux sources, avec seulement cette conversion autorisée. Aucun fichier applicatif, attribut, réglage Git ou élément indexé n'a été retouché ; aucune nouvelle indexation du premier lot. L'index existant a été revérifié avant le commit. Diagnostic conservé (pièce interne non diffusée). **Aucun commit n'a échoué.**

| Contrôle indexé | Lot 01 | Lot 02 | Lot 03 |
|---|---:|---:|---:|
| Chemins exacts | 46 | 30 | 3 |
| Suppressions / chemins imprévus | 0 / 0 | 0 / 0 | 0 / 0 |
| `git diff --cached --check` par défaut | Code 2, 164 alertes CRLF historiques | Code 0 | Code 0 |
| Contrôle avec `-c core.whitespace=cr-at-eol` limité à la commande | Code 0 | Code 0 | Code 0 |
| Index vide après commit | Oui | Oui | Oui |

Le contrôle final du diff **restant dans le dossier de travail** retourne 0 par défaut : les deux fichiers aux CRLF historiques sont maintenant committés. Cela ne signifie pas que leurs fins de ligne ont été réécrites.

### Secrets, données et ressources

Les nouveaux changements excluent `.env`, clés, certificats, bases/dumps réels, cookies/sessions, journaux privés, environnements, profils navigateur et dossier téléchargé. Les listes et extensions sont contrôlées ; aucune illustration n'est ajoutée ou modifiée dans les nouveaux diffs.

Recherche ciblée de marqueurs de clés privées, jetons de fournisseurs, JWT, URL SQL authentifiées et affectations littérales de credentials dans les fichiers sélectionnés puis dans les nouveaux blobs. Le seul signalement est la constante de mot de passe synthétique de `backend/tests/test_api_errors_stats_login.py:13`, utilisée dans les fixtures SQLite mémoire ; sa valeur n'est pas reproduite dans les reçus. Aucun autre signalement des règles contrôlées. Les sources et fixtures correspondent à celles déjà examinées ; aucun secret réel identifié dans ces nouveaux changements. **Ce résultat n'est pas un audit exhaustif de tout l'historique Git ou une garantie absolue de détection de toute information privée.**

## 5. Vérification fonctionnelle réellement exécutée

Après le troisième commit, **41 fichiers ont été exportés par lecture des objets Git de `3fe3596`**, sans checkout, changement de branche ou lecture de fichiers exclus : les 40 sources du manifeste du kit, plus le manifeste lui-même. Les 40 empreintes LF correspondent au manifeste figé. Aucun fichier non committé n'a été injecté dans cette copie de recette.

Commande exécutée dans la copie temporaire avec le Python du venv déjà présent : `python -I -B tools/recette_lot6g4.py --check-journey`. Le kit a été inspecté avant exécution : neutralisation de dotenv, paramètres Aiven vidés, connexions SQL limitées à SQLite mémoire, FK activées, réseau/sous-processus/migrations/écritures hors preuves interdits. Aucun `--serve`, navigateur ou écoute réseau.

**PASS : 43 requêtes WSGI, sept groupes de contrôles**, avec les vrais contrôleurs Flask/SQLAlchemy et données synthétiques :

1. Inscription et connexion via les routes.
2. Deux catégories et création d'un commentaire.
3. Likes ajout/retrait/réajout, unicité et refus CSRF.
4. Signalement et préservation/refus d'un compteur historique incompatible.
5. Erreur simulée après flush et rollback sans fuite de changement.
6. Administration et sept valeurs API égales aux SELECT.
7. Archivage/restauration, bannissement et conservation des likes.

Garde-fous : **sept compteurs à zéro** ; aucune base fichier ; FK actives et contrôle FK vide ; sources exportées inchangées. Les compteurs finaux de ce scénario sont **2 histoires / 1 résolue / 1 Cold Case / 4 utilisateurs / 2 commentaires / 1 signalement / 0 proposition en attente**. Ils diffèrent des anciennes recettes parce que leurs actions diffèrent ; ne pas mélanger les jeux de données.

Preuves : export et exécution depuis Git (pièce interne non diffusée), isolation (pièce interne non diffusée), 43 échanges et assertions (pièce interne non diffusée). La copie temporaire et ses preuves sont conservées, sans suppression.

**Les 854 PASS du lot 6G.5 ne sont pas réexécutés.** Leurs 76 empreintes brutes restent conformes dans le dossier de travail ; ce rapprochement historique et les 43 échanges nouveaux sont deux preuves distinctes. Aucune nouvelle installation de dépendances, aucun venv neuf, autre PC, recette humaine Edge, campagne frontend exhaustive ou validation MySQL. Les sept anciens tests de migration restent des exclusions historiques ; les six essais de candidate likes en mémoire ne deviennent pas un déploiement réel.

## 6. Fichiers exclus et travail local restant

Huit fichiers suivis restent modifiés, volontairement hors des trois commits :

```text
README.md
docs/soutenance/README.md
docs/soutenance/fiche-commune.md
docs/soutenance/fiche-mahamadou.md
docs/soutenance/fiche-melissa.md
docs/soutenance/fiche-sylvie.md
frontend/README.md
frontend/images/README.md
```

Sur les 133 fichiers initialement non suivis, 36 sont maintenant enregistrés. Les **97 autres restent non suivis**, dont documents/preuves de soutenance, fichiers privés exclus et archives. Les 17 livrables nouveaux 6H.6 portent le total final à **114 non suivis**. Leur liste exacte est dans le reçu final (pièce interne non diffusée). Aucun de ces chemins n'a été indexé par extension de périmètre.

Exclusions à retenir :

- `frontend/histoires-originales.json` et `docs/soutenance/COMPTES_DEMO.exemple.csv` : non suivis, non ouverts ; pas d'ajout global.
- `frontend/donnees.js` : déjà suivi mais inchangé et hors nouveaux diffs ; reste hérité dans les commits.
- Quatre WebP et `default-story.svg` : déjà suivis, inchangés, origine/droits de diffusion non finalisés ; ne disparaissent pas de l'arbre par omission de l'indexation.
- `frontend/images/Reprendre projet portfolio_files` : ignoré, aucun enfant suivi, hors sélection et kit. Aucun contenu lu ou modifié. La réserve du lanceur normal qui accepte des images imbriquées reste documentée en 6H.5.
- Archives `revision_code/mahamadou/backend/models.py`, `tools/recette_lot6f2.py`, `tools/recette_lot6f2_sources.json` : conservées hors nouveaux commits, sans fusion dans le code actif.
- Documents RGPD internes, rapports et chemins privés : hors nouveaux commits, sauf la dépendance HTML de test explicitement validée ; politique toujours non publiée sur le site.

## 7. Installation et dépendances à ne pas masquer

Le dernier commit, avec son histoire héritée, contient les sources nécessaires au kit mémoire : la recette depuis Git le démontre dans l'environnement déjà installé. Les fichiers backend/frontend et tests sélectionnés sont effectivement enregistrés ; aucune fonctionnalité du kit testé ne dépend d'un fichier de travail non committé. Le SVG de repli est une dépendance **héritée**, pas un nouvel ajout aux droits résolus.

Une installation indépendante nécessite encore un interpréteur et les dépendances de `backend/requirements.txt`, déjà suivi. La présente campagne ne réinstalle pas ces dépendances ; la copie/installation neuve 6H.2 reste une preuve historique sur le même PC. Le harnais intégral des 854 tests et les utilitaires de préparation 6H.2 restent hors des trois commits : aucune reproduction automatique de cette campagne depuis le seul HEAD n'est promise. Les README suivis dans HEAD ne comprennent pas les dernières actualisations documentaires encore locales ; des liens historiques peuvent pointer vers des supports non livrés.

Le lanceur normal exige une configuration locale appropriée, volontairement absente de Git. Une base persistante existante nécessite un schéma compatible ; les sept révisions committées sont des candidates dont l'état réellement appliqué n'a pas été examiné. DDL partiel, anciens compteurs de likes incompatibles, intégrité des signalements/commentaires, verrous et concurrence MySQL restent à traiter dans une intervention distincte. **Aucun accès Aiven/MySQL ni migration réelle n'a servi à produire ces commits.**

## 8. Réserves du jury et conditions avant push

| Remarque | État inchangé et prochain élément utile |
|---|---|
| C-02 — Fichier privé de comptes de démonstration | PARTIEL. Mahamadou est désigné ; support privé, renouvellement et deux connexions du lancement du jour J restent à confirmer. Les comptes synthétiques de cette recette WSGI, jetés à l'arrêt, ne constituent pas cette fiche. |
| C-07 — Informations RGPD et consentement | PARTIEL. Cadre scolaire local confirmé ; groupe responsable du projet sans désignation juridique automatique du responsable du traitement. Contact, bases, durées et autres décisions indispensables non validés ; brouillons conservés. |
| I-02 — Provenance et droits des illustrations | PARTIEL. Mélissa/ChatGPT et usage local déclarés pour les WebP, dates/références non confirmées ; origine créative du SVG inconnue. Un auteur d'ajout Git ne prouve pas l'auteur créatif. |

Avant d'autoriser un push :

1. Confirmer dépôt cible, visibilité, destinataires et portée exacte du partage ; GitHub privé reste un partage avec un service et des personnes.
2. Revoir l'arbre **et l'historique réellement transmis**, notamment anciens jeux déjà suivis, images, éventuelles données/identifiants et documents internes. Le contrôle des 79 changements ne remplace pas cette revue.
3. Obtenir les justificatifs/accords des ressources pour la destination choisie ; tout remplacement ou retrait du suivi exigerait une autorisation adaptée, en préservant les originaux.
4. Préparer le lot documentaire cohérent, ses liens, instructions d'installation et preuves partageables ; décider du traitement du brouillon de test et des archives, sans publier une politique incomplète comme définitive.
5. Présenter la sélection de push et ses réserves, puis obtenir l'autorisation explicite. Aucune action distante n'est engagée par ce rapport.

La finalisation du RGPD d'un futur site public et la migration d'une base réelle ne sont pas artificiellement exigées pour conserver ces commits locaux. Elles conditionnent leurs usages respectifs. Pour une ouverture publique, droits, information/organisation RGPD, configuration/hébergement et exploitation réelle restent non validés.

## 9. Verdicts et arrêt

- **GO — conservation des commits locaux** : trois commits linéaires, 79 chemins exacts, aucune suppression, contenus vérifiés et parcours mémoire depuis Git réussi. Les autres travaux sont conservés.
- **NO-GO — préparation du push considérée comme achevée** : la conservation locale est prête, mais la sélection documentaire, les ressources héritées, l'historique à transmettre et la destination restent à arbitrer. Aucun push effectué ou autorisé.
- **NO-GO — ouverture publique** : réserves juridiques, organisationnelles et techniques inchangées.

**Arrêt après 6H.6. Aucun push sans nouvelle autorisation utilisateur.** Ce rapport et les preuves 6H.6 restent non committés, hors sélection des 79 fichiers.

## Annexe — chemins réellement inclus dans chaque commit

Les listes suivantes sont reproduites des reçus contrôlés après chaque commit ; elles n'incluent pas les fichiers simplement hérités d'anciens commits.

### Commit 01 — 4bbb75df2b7860e8373890634f6f39935cdde01c

```text
M	backend/api/v1/app.py
M	backend/api/v1/swagger.json
M	backend/api/v1/views/__init__.py
A	backend/api/v1/views/admin_stories.py
A	backend/api/v1/views/admin_users_support.py
M	backend/api/v1/views/comments.py
M	backend/api/v1/views/histoires.py
M	backend/api/v1/views/index.py
A	backend/api/v1/views/likes.py
M	backend/api/v1/views/permissions.py
M	backend/api/v1/views/proposals.py
A	backend/api/v1/views/story_deletion_support.py
A	backend/api/v1/views/story_visibility.py
M	backend/api/v1/views/theories.py
M	backend/api/v1/views/users.py
M	backend/api/v1/views/write_support.py
M	backend/index.py
M	backend/models.py
M	frontend/admin-connexion.html
M	frontend/admin-dashboard.html
M	frontend/admin-dashboard.js
A	frontend/admin-stories.js
A	frontend/admin-users.js
M	frontend/api.js
M	frontend/app.js
M	frontend/coldcases.html
A	frontend/comments.js
M	frontend/connexion.html
M	frontend/dossier.html
M	frontend/histoires.html
M	frontend/index.html
M	frontend/inscription.html
A	frontend/likes.js
M	frontend/proposer-histoire.html
M	frontend/styles.css
M	frontend/theories-list.js
M	frontend/theories.html
M	migrations/env.py
M	migrations/versions/3111f5767fc6_ajoute_les_regles_on_delete.py
M	migrations/versions/82deda84bc35_remove_legacy_comment_reports_counter.py
M	migrations/versions/921687c1bd7c_baseline_schema.py
M	migrations/versions/a590c8aac613_add_reports_bans_and_cold_case_updates.py
A	migrations/versions/c6c100000001_add_story_archive_date.py
A	migrations/versions/c6c200000001_comment_reports_and_story_revision.py
A	migrations/versions/c6g200000001_add_comment_likes.py
M	run_local.py
```

### Commit 02 — 0d776703219c63951823d3e4f06d015165ddeae8

```text
A	backend/tests/test_admin_pending_stats.py
A	backend/tests/test_admin_report_context.py
A	backend/tests/test_admin_stories_read.py
A	backend/tests/test_admin_users.py
M	backend/tests/test_api_errors_stats_login.py
A	backend/tests/test_comment_likes_migration.py
M	backend/tests/test_comments_theories.py
A	backend/tests/test_likes.py
A	backend/tests/test_moderation_journey.py
M	backend/tests/test_proposals_ban.py
A	backend/tests/test_report_migration.py
A	backend/tests/test_story_archiving.py
A	backend/tests/test_story_deletion.py
M	backend/tests/test_swagger.py
A	projet de texte de confidentialité (pièce interne non diffusée)
A	frontend/tests/admin-archives.test.cjs
M	frontend/tests/admin-dashboard.test.cjs
A	frontend/tests/admin-deletion.test.cjs
A	frontend/tests/admin-stories.test.cjs
A	frontend/tests/admin-users.test.cjs
A	frontend/tests/comments.test.cjs
A	frontend/tests/fixtures/admin-proposals.json
A	frontend/tests/fixtures/admin-stories.json
A	frontend/tests/likes.test.cjs
M	frontend/tests/proposals.test.cjs
A	frontend/tests/session.test.cjs
M	frontend/tests/theories-list.test.cjs
M	frontend/tests/theories.test.cjs
A	tests/test_rgpd_information.py
M	tests/test_run_local.py
```

### Commit 03 — 3fe35965d5dd88151a7e1cab5bc645e2ddfbfca2

```text
A	tests/test_recette_lot6g4.py
A	tools/recette_lot6g4.py
A	tools/recette_lot6g4_sources.json
```
