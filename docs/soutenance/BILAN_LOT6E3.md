# Lot 6E.3 — vérification technique et préparation à la soutenance

> Archive pédagogique datée : les résultats et descriptions ci-dessous concernent le lot indiqué. Les anciens repères de ligne ne décrivent pas la version candidate. Pour préparer la soutenance actuelle, consulter les quatre fiches et le référentiel reliés au sommaire.

> Copie publique de référence : les chemins personnels et liens de travail internes sont retirés. Les preuves et commandes historiques gardent leur date et leur périmètre ; utiliser le README actuel pour le lancement.

[Sommaire](README.md) · [Bilan 6E.2](BILAN_LOT6E2.md) · Décisions originales (pièce interne non diffusée) · [Démonstration](DEMONSTRATION.md)

**1er novembre 2026. 659 tests exécutés et réussis : 279 backend, 364 frontend, 16 lanceur.** Sept tests de migration sont volontairement non exécutés. Le nouveau parcours API/SQL passe dans SQLite mémoire ; aucune recette navigateur ou cible MySQL/Aiven n'est revendiquée. Aucun code applicatif modifié et aucune politique incomplète publiée.

## 1. Préservation et fichiers examinés

Branche : `feature/frontend-api-integration`. HEAD : `07a9f03ea0a3bdad4a07066fdd7bab1997cc158b`. Au départ : **44 fichiers suivis modifiés, 51 non suivis, aucun fichier indexé**. Un état des 110 fichiers de sources/documents déjà examinés, de l'index et du statut Git est enregistré avant intervention. Les sept exclusions antérieures, secrets et données réelles ne sont pas lus ou copiés.

La sauvegarde durable reste inchangée :

```text
[chemin local privé retiré]
```

Les 115 empreintes sont conservées pour comparaison finale, sans écriture dans cette sauvegarde ni modification de permissions. La réserve précédente sur son contrôle exhaustif d'ACL n'est pas levée ici. Cette copie de sources ne sauvegarde pas les données de la base de présentation.

**Lectures ciblées :** bilans 6A, 6B, 6C.1, 6C.2, 6D, 6E.1 et 6E.2 ; lecture intégrale des douze décisions ; matrice des 22 remarques ; notices et brouillon HTML ; frontend/app.js, api.js, admin-dashboard.js, dossier.html ; backend/index.py, modèles et vues commentaires, signalements, propositions, utilisateurs et dossiers administratifs ; les treize modules de tests backend existants ; tests frontend/lanceur et gardes. Les inventaires distinguent sources autorisées, empreintes et preuves ; aucun audit de données réelles n'est réalisé.

**Créés :**

- [backend/tests/test_moderation_journey.py](../../backend/tests/test_moderation_journey.py) : un parcours multi-utilisateur API/SQL, pas une fonction du site.
- Présent rapport `docs/soutenance/BILAN_LOT6E3.md`.

**Documents complétés uniquement :** `README.md`, `DEMONSTRATION.md`, `TESTS_ET_VALIDATION.md`, `SUIVI_REMARQUES_JURY.md` et `INDEX_CODE_JURY.md` dans `docs/soutenance/`. Leurs versions antérieures sont copiées avant édition. Frontend, backend applicatif, modèles, migrations, Swagger et tests historiques ne sont pas corrigés ou réécrits.

## 2. Isolation démontrée avant lancement

Répertoire neuf de preuves, hors dépôt :

```text
[chemin local privé retiré]
```

Les gardes de 6E.2 ont été relues avant adaptation. Environnement enfant minimal, paramètres Aiven vidés, dotenv neutralisé avant import applicatif, moteur obligatoirement SQLite `:memory:`. Les connexions fichier et MySQL, ATTACH/DETACH, réseau/DNS, sous-processus applicatifs, lectures privées et écritures du dépôt sont bloqués. Chaque connexion SQLite active et contrôle les FK.

La sélection exclut le module de migration des signalements avant import et le cas de migration d'archivage avant exécution. Les sources de migrations sont retirées du manifeste de lecture ; exécution de code dans `migrations/`, commandes Alembic, `MigrationContext.run_migrations` et `Operations.invoke` sont bloqués. Le contrôleur s'arrête à tout code de sortie non nul. Les sondes vérifient les refus avant entrée/sortie ; leurs compteurs volontairement positifs sont séparés des suites.

**Un seul passage complet, sans échec : `attempt-1`. Tous les compteurs interdits des suites valent zéro**, dont accès réseau, lecture privée, écriture du dépôt, base non mémoire, sous-processus et migration. Les tables des fixtures sont créées par les modèles dans SQLite mémoire ; aucun script de migration n'est exécuté. Le nouveau test exige le marqueur du harnais avant sa préparation.

Preuves : `baseline.json`, `backend-source-review.json`, `harness-inspection.json`, `preflight.json` et les journaux de `attempt-1/`. Le manifeste épingle 63 sources autorisées et leurs SHA-256. `donnees.js`, `ancien_app.py`, CSV de comptes, bases, certificats et journaux privés restent hors périmètre.

## 3. Résultats exacts et campagnes historiques

| Suite | Exécution 6E.3 | Échecs / erreurs / ignorés |
|---|---:|---|
| Backend sélectionné | **279 PASS** : 278 cas historiques et un nouveau parcours | 0 / 0 / 0 |
| Frontend | **364 PASS** | 0 échec, annulé ou ignoré |
| Lanceur et contrats HTML | **16 PASS** | 0 / 0 / 0 |
| **Total actuel** | **659 PASS** | Aucun cumul avec une campagne antérieure |

Répartition backend :

| Module de tests | Cas exécutés |
|---|---:|
| test_admin_pending_stats | 8 |
| test_admin_stories_read | 6 |
| test_admin_users | 16 |
| test_api_errors_stats_login | 14 |
| test_comments_theories | 37 |
| test_csrf | 29 |
| test_moderation_journey — nouveau | 1 |
| test_proposals_ban | 42 |
| test_reports | 22 |
| test_story_archiving | 18 |
| test_story_deletion | 25 |
| test_swagger | 32 |
| test_users_votes | 29 |

Les **657 PASS de 6C.2** et **380 PASS de 6E.2** restent des campagnes historiques distinctes. Les six cas de `test_report_migration.py` ne sont pas réexécutés : reprise valide/type entier, fixture historique other, références invalides, FK/cascade du schéma migré, downgrade/conservation des doublons et type cible non entier. Le cas `StoryArchivingTests.test_prepared_migration_on_fictitious_memory_schema_only` ne l'est pas non plus. **Sept non-sélections explicites, pas sept PASS ni sept skips unittest.** Leurs sources restent intactes ; liste exacte dans `backend.guard.json`.

Les anciennes recettes Edge, persistance sur fichier et autres campagnes ne sont pas relancées. Aucun nouveau résultat sur migrations, reprise historique ou MySQL n'est déduit des 659 PASS.

```powershell
# Harnais inspecté ; ne pas remplacer par un lancement applicatif non isolé.
$preuves6e3 = Join-Path $env:LOCALAPPDATA 'Temp\portfolio-lot6e3-20261101-e9b5fc9c'
& .\.venv\Scripts\python.exe -I -B (Join-Path $preuves6e3 'run-checks.py') --inspect
& .\.venv\Scripts\python.exe -I -B (Join-Path $preuves6e3 'run-checks.py')
```

## 4. Notices, fonctions principales et limites visuelles

Les notices d'inscription, théorie et proposition sont avant les champs, visibles sans attribut hidden, reliées au formulaire et bouton par aria-describedby. Champs, contraintes, scripts et ordre des contrôles restent ceux de 6E.2. Le CSS conserve le design existant, un bloc contrasté et le retour à la ligne ; aucun gestionnaire d'envoi n'est modifié. Les retours de soumission utilisent `.feedback`, distinct de ces paragraphes.

Les contrôles HTML/WSGI et les tests frontend passent : identifiants/labels, descriptions, liens locaux, états de chargement, valeurs conservées en cas d'erreur et absence de collecte supplémentaire. Le projet de confidentialité (pièce interne non diffusée) reste hors de `frontend/`, sans lien public et refusé par les chemins WSGI testés. Ses six mentions essentielles restent à confirmer. Les notices décrivent le fonctionnement sans annoncer de base légale, contact ou conformité inventés.

**Clavier et lisibilité : contrôle structurel uniquement.** Liens/contrôles natifs, ordre du DOM, références ARIA et absence de nouveau tabindex négatif sont vérifiés ; parcours clavier réel, lecteur d'écran, rendu responsive et inspection visuelle dans Edge restent NON EXÉCUTÉS.

| Fonction | Preuve actuelle | Ce qui reste hors preuve |
|---|---|---|
| Inscription, connexion, sessions | Backend et nouveau parcours avec véritables vues et hachages de test ; contrats HTML | Parcours complet dans un navigateur sur la cible de présentation |
| Théories et propositions | Backend/DOM simulé, validation, CSRF, erreurs et doubles envois ; proposition créée dans le nouveau parcours | Recette visuelle et persistance de la base réelle |
| Commentaires et signalements | API/SQL dans SQLite mémoire, consultation et contrôle relationnel | Formulaires publics absents ; pas de parcours de création par boutons du site |
| Utilisateurs, bannissement | Permissions relues en base ; session bannie refusée, autres données conservées | Recette UI réelle et configuration des comptes de présentation |
| Dossiers, filtres, archives/restauration | Backend et frontend simulé ; archives retirées des lectures publiques | Catégories réelles, rendu et concurrence MySQL |
| Purge sécurisée d'une archive | 25 tests backend, suite frontend existante, dépendances et rollback dans le périmètre simulé | Aucune purge réelle, course multi-connexion ou garantie MySQL |

## 5. Parcours commentaire → signalement → administration

Le nouveau test appelle les **vraies routes Flask** avec clients WSGI séparés, puis relit les modèles SQLAlchemy. Les réponses API et la base ne sont pas remplacées par des mocks ; seules les protections d'isolation et les fixtures sont préparées.

| Étape réellement exécutée | Résultat et contrôle |
|---|---|
| Deux membres s'inscrivent et se connectent | POST `/users` → 201 et `/login` → 200 ; identifiants repris des réponses, pas de session fabriquée pour ce parcours |
| Le premier publie et relit un commentaire | POST `/stories/1/comments` → 201 puis GET → 200 ; auteur, dossier et pseudo copié correspondent à la ligne SQL |
| Le second essaie un signalement sans CSRF, puis un type interdit | 403 et 400 ; aucune ligne de report insérée |
| Il signale le commentaire avec session et CSRF valides | 201 ; id de report **1**, cible physique `comment_id=2`, motif égal au JSON ; compteur du commentaire relu et comparé à SQL |
| Un non-administrateur tente les lectures privées | `/admin/reports`, `/proposals` et `/users` → 403 |
| Un administrateur se connecte réellement dans le test | Login et `/me` → 200 ; GET `/admin/reports` → 200, objet JSON égal à la ligne ORM |
| Sources de statistiques et proposition | Trois agrégats, dossiers actifs/catégories et propositions pending relus par API et comparés aux requêtes SQL |
| Bannissement et intégrité | Session du compte banni refusée, autre auteur encore connecté ; données conservées ; insertion ORM orpheline refusée avec rollback du savepoint ; `foreign_key_check` vide et FK commentaire/CASCADE constatée |

Preuve : `moderation-journey.json`, sans mot de passe, hachage, cookie ni jeton. **Valeurs observées exclusivement dans cette base fictive mémoire :** 5 comptes, 2 commentaires, 1 signalement, 2 dossiers actifs dont un dans chaque catégorie 1/2, et 1 proposition pending. Ce sont les résultats des requêtes comparés à SQL, jamais des chiffres injectés dans le dashboard du site. Les enregistrements ne persistent pas après destruction de cette base mémoire.

Report ne stocke pas d'id du déclarant : le test connaît le client ayant envoyé la requête, mais ne démontre pas un journal persistant d'attribution. La preuve porte sur la ligne de signalement et son commentaire cible. La déclaration CASCADE est inspectée ; la résistance à toutes les opérations concurrentes ou variantes de chargement ORM n'est pas établie.

### Sources des sept compteurs

| Compteur du dashboard | Source effective prévue par le code | Vérification |
|---|---|---|
| Dossiers actifs | Taille de GET `/api/v1/stories` | API comparée aux Story dont archived_at est NULL |
| Histoires résolues | Filtrage client via getStoryCategory, catégorie 1 | Source app.js et tests DOM ; partition API/SQL vérifiée avec la fixture correspondante |
| Cold Cases | Même classement, catégorie 2 | Même contrôle ; aucune vérification de catégories MySQL réelles |
| Utilisateurs | GET `/api/v1/stats`, User.count | Égalité API/SQL, comptes bannis inclus |
| Commentaires | GET `/api/v1/stats`, Comment.count | Égalité API/SQL ; agrégat global, pas limité aux dossiers actifs |
| Signalements | GET `/api/v1/stats`, Report.count | Égalité API/SQL ; pas de nombre maintenu séparément |
| Propositions en attente | GET privé `/api/v1/proposals`, puis filtre client exact pending | Liste API comparée à Proposal et au compte SQL pending |

Les sept éléments et leurs branchements sont inchangés. Les 364 tests frontend vérifient le rendu et les erreurs dans un DOM/API simulés ; **ce rendu n'est pas la continuation dans un navigateur du parcours SQL ci-dessus**. Le classement 1/2 est une hypothèse actuelle de l'interface à vérifier sur la cible réelle ; les autres catégories ne doivent pas être classées artificiellement. L'archivage diminue les comptes de dossiers actifs mais conserve commentaires/signalements globaux.

## 6. Revue des douze décisions RGPD

Aucune identité, adresse, base légale, durée ou infrastructure n'est déduite du caractère scolaire du projet. Les rôles techniques ne désignent pas le responsable juridique.

| ID / point à valider | État actuel | Conséquence soutenance | Conséquence ouverture publique | Qui doit décider | Minimum technique recommandé |
|---|---|---|---|---|---|
| D01 — responsable et coordonnées | Non confirmés ; rôle de l'école/DPO éventuel à établir | Expliquer la limite et obtenir une validation avant information finale | Identification et responsabilité effectives indispensables | Équipe et organisme concerné habilité à confirmer | Une fiche validée ; aucun module supplémentaire |
| D02 — contact suivi sans connexion | Procédure préparée, aucun contact inventé | Ne pas montrer une adresse ou un parcours de demande inexistant | Canal effectif, aussi pour personnes bannies/sans compte | Responsable à désigner et équipe pour le suivi | Un moyen existant approuvé et un lien après validation |
| D03 — finalités et nécessité des champs | Pseudo/email/mot de passe obligatoires ; nécessité de l'email à justifier | Présenter ce qui est demandé et la limite connue | Collecte et information justifiées pour chaque usage | Responsable, Mélissa et Sylvie | Documenter ; aucun champ ni schéma modifié par défaut |
| D04 — bases légales par traitement | Aucune base choisie automatiquement | Ne pas présenter inscription/CGU comme consentement général | Bases et conditions adaptées à arrêter avant publication | Responsable confirmé avec l'équipe | Courte matrice finalité/base, pas de plateforme de consentement |
| D05 — conservation et réexamen | Durées/critères, départ et actions non décidés | Prévoir le devenir des comptes/contributions après leur utilité | Règles effectives incluant journaux et copies | Responsable, Mahamadou et Sylvie | Tableau et réexamen manuel à échéance décidée ; pas d'ordonnanceur |
| D06 — hébergement, accès et transferts | Configuration possible en code ; cible/régions/contrats inconnus | Confirmer le mode de présentation et les accès, sans exposer de secret | Prestataires, garanties et transferts à documenter | Équipe et responsable avec les prestataires concernés | Fiche de la cible réellement retenue ; aucune nouvelle infrastructure par principe |
| D07 — public, mineurs, données et récits | Intention jury confirmée ; restriction effective et contenus non vérifiés | Actions autorisées et données réelles pertinentes, sans remplissage fictif du site | Examiner audience, sources et cadre des récits sur des tiers | Équipe, responsable et école selon leurs rôles confirmés | Fixer le périmètre ; données fictives uniquement dans les essais isolés autorisés |
| D08 — sort des contributions | Étude SQL/ORM et procédure, pas d'effacement de compte livré | Distinguer les quatre opérations et préserver les tiers | Règles justifiées de retrait/conservation et outils réellement utilisables | Responsable, Sylvie et Mahamadou ; Mélissa pour l'information | Examen ciblé, pas de cascade globale depuis User |
| D09 — identité et anciennes sessions | Session/bannissement testés ; révocation globale et id réutilisé restent à traiter | Ne jamais demander de secret ; pas de promesse de suppression complète | Garantie adaptée avant effacement de compte et traitement des demandes | Sylvie/Mahamadou avec validation du responsable | Procédure proportionnée ; aucun delete du compte avant protection démontrée |
| D10 — opérateurs et circuit des demandes | Répartition pédagogique connue ; habilitations/canaux non confirmés | Expliquer le circuit prévu sans prétendre qu'il est activé | Réception, réponse sécurisée et suivi minimal effectifs | Responsable et opérateurs expressément habilités | Organisation privée hors dépôt ; pas de portail d'export ou table de reçus |
| D11 — sécurité effective et incidents | Code et tests isolés vérifiés ; HTTPS/cookies/logs/cible non recettés | Recette du mode retenu à autoriser, sans exposer les jetons | Vérifications du déploiement et organisation incident avant ouverture | Sylvie/Mélissa, responsable et exploitant confirmé | Liste de contrôles ciblés ; ne pas confondre cookies nécessaires et traceurs facultatifs |
| D12 — sauvegardes, copies et reprise | Copie durable de sources existante ; conservation/reprise et base réelle hors preuve, réserve ACL antérieure | Préserver travail et preuves ; ne pas dire que le code sauvegarde les interactions | Politique de copies/restauration évitant la republication des données retirées | Mahamadou/équipe et responsable pour la conservation | Copies privées vérifiées et règles manuelles ; aucun cloud/rotation/purge ajouté |

## 7. Scénario de soutenance

**Parcours proposé pour une future répétition autorisée, pas recette réelle déjà exécutée.** Avant toute action réelle : confirmer participants/contenus, compte administrateur autorisé, responsable/contact et mode de présentation ; autoriser séparément navigateur, serveur et cible SQL. Ne pas importer les fixtures ou comptes de tests dans la base de présentation. Les valeurs affichées doivent provenir des actions réelles ; un zéro est valable.

Les routes abrégées ci-dessous sont sous `/api/v1` ; les fichiers HTML du site sont dans `frontend/`. Les étapes qui modifieraient des données réelles restent des propositions soumises à une autorisation distincte.

| Étape / présentateur | Fonction | Fichier ou route | Donnée écrite si l'action est autorisée | Confirmer le résultat | État actuel et limite à annoncer |
|---|---|---|---|---|---|
| 1 — Mélissa | Navigation, listes et fiche d'histoire | index.html, histoires.html, coldcases.html, dossier.html ; GET `/stories`, `/stories/slug/{slug}` | Aucune en lecture | Titre/slug/catégorie et états vide/erreur ; cohérence des listes | API et DOM testés, rendu navigateur à recetter ; catégories 1/2 à confirmer sur la cible |
| 2 — Mélissa | Notices | inscription.html, theories.html, proposer-histoire.html | Aucune | Lire la notice avant champs et vérifier l'ordre clavier lors de la recette | Structure testée ; politique HTML toujours interne et incomplète |
| 3 — Mélissa / Sylvie | Inscription d'un participant autorisé | POST `/users` via formulaire | User, hachage et date ; aucun rôle admin accordé par ce parcours | 201, puis connexion et `/me` ; contrôle SQL seulement s'il est autorisé | Réalisé en SQLite isolée ; aucune inscription réelle créée en 6E.3 |
| 4 — Sylvie | Connexion / déconnexion | connexion.html ; POST `/login`, GET `/me`, POST `/logout` | Session dans le cookie, pas une table de sessions nouvelle | Compte courant et refus après déconnexion ; masquer tous les secrets | API testée ; cookie/TLS réels à recetter, pas de révocation globale annoncée |
| 5 — Mélissa / Mahamadou | Théorie | theories.html ; POST/GET `/stories/{id}/theories` | Theory liée au dossier et au compte, titre/contenu/date | 201 puis relecture, sans double envoi | Backend/DOM testés ; aucune donnée de remplissage, texte approuvé seulement |
| 6 — Mélissa / Sylvie | Proposition | proposer-histoire.html ; POST `/proposals` | Proposal pending liée au compte | 201 ; consultation privée par admin à l'étape 9 | Aucun passage automatique en dossier publié |
| 7 — Sylvie / Mahamadou | Commentaire | POST/GET `/stories/{id}/comments`, test_moderation_journey.py | Comment, auteur et pseudo copié | Relecture API et relation SQL | **API/SQL testé, pas de formulaire public existant** : montrer la preuve isolée, pas un bouton fictif |
| 8 — Sylvie / Mahamadou | Signalement par un autre membre | POST `/comments/{id}/report`, ou `/reports` | Report vers le commentaire, motif/statut/date | 201 et même id/cible/motif dans la base de test | **API/SQL testé, interface publique absente** ; identité du déclarant non conservée dans Report |
| 9 — Sylvie / Mélissa | Accès admin et modération | admin-connexion.html, GET `/me`, `/admin/reports`, `/proposals` | Aucune en lecture | Refus membre simple ; admin voit la ligne correspondante et la proposition | API/SQL et DOM séparément testés ; consultation, pas de résolution automatique de signalement |
| 10 — Mélissa / Mahamadou | Sept compteurs et filtres | admin-dashboard.js, admin-stories.js et sources de la section 5 | Aucune pour lecture/recherche/filtre | Comparer sources, listes et compteurs réellement obtenus | Pas de chiffres imposés ; archives et catégories expliquées ; navigateur non testé ici |
| 11 — Sylvie | Gestion et bannissement | admin-users.js ; POST `/admin/users/{id}/ban` | User.is_banned, pas une suppression | Session refusée, autres données et utilisateurs conservés | Test isolé réussi ; ne pas bannir un compte réel hors action expressément autorisée |
| 12 — Mahamadou / Mélissa | Archivage et restauration | POST `/admin/stories/{id}/archive` et `/admin/stories/{id}/restore` | archived_at et management_revision du dossier | Retrait/retour des lectures publiques ; dépendances conservées | Backend et DOM testés ; choisir un dossier dont l'action est autorisée, jamais effacer pour la démonstration |
| 13 — Sylvie / Mahamadou | Explication de la purge sécurisée | GET `/admin/stories/{id}/deletion-preview`, POST `/admin/stories/{id}/deletion-confirmations`, DELETE `/admin/stories/{id}` | Graphe du dossier supprimé seulement dans les essais autorisés | Montrer tests/conditions/rollback ; ne pas confirmer une purge réelle ici | 25 tests backend et frontend existant ; MySQL/concurrence/timeout réel non attestés |
| 14 — Tous | Droits et bilan | PROCEDURE_DROITS_LOT6E2.md ; décisions et présent bilan | Aucune demande ou suppression réelle | Expliquer identité proportionnée, tiers, contact à confirmer et limites | Procédure préparée, pas de portail ni d'effacement de compte |

### Alternatives si navigateur ou base indisponibles

- **Navigateur indisponible :** montrer code HTML/JS, rapports et parcours WSGI/SQLite du harnais inspecté. Expliquer que les routes et transactions ont été exécutées sans fenêtre, et que les tests DOM utilisent une simulation. Ne pas présenter un rendu non vu comme recetté.
- **Base de présentation indisponible :** annoncer l'indisponibilité ; utiliser la preuve SQLite mémoire explicitement identifiée comme test. Ne pas rediriger silencieusement le site ni remplir le dashboard avec un jeu fictif.
- **Essais impossibles ou preuves Temp absentes :** montrer les sources et le rapport daté, sans prétendre à une exécution en direct. Reconstituer le harnais et ses protections uniquement par une préparation autorisée ; pas de commande Flask/Alembic improvisée.

## 8. Diagnostics et autorisations nécessaires

**Aucune régression fonctionnelle détectée dans les tests exécutés.** Le parcours navigateur commentaire/signalement ne peut néanmoins pas être présenté intégralement avec l'interface actuelle : dossier.html ne propose pas ces formulaires, app.js n'a pas leurs gestionnaires et api.js n'a pas leurs fonctions de création. Les routes Flask existent et passent le nouveau parcours. Développer cette interface minimale nécessite une autorisation ; aucun correctif applicatif n'est entrepris.

La consultation administrative des signalements est présente ; ne pas annoncer un bouton ou une API de résolution de statut non livré. Les actions de bannissement/archivage ne constituent pas automatiquement la résolution d'un signalement ni un effacement personnel.

**Risque de cible réelle non vérifiée :** les essais créent le schéma actuel des modèles dans une base mémoire vierge. Ils ne prouvent pas que la base de présentation possède archived_at, management_revision, Report.comment_id et les contraintes attendues. Aucun état MySQL/Aiven ni historique de migrations déployées n'est connu ici. La vérification de cette cible requiert une autorisation distincte ; aucune migration réelle ne doit être déduite de ce rapport.

Non attestés : navigateur/clavier/lecteur d'écran réels, mobile, TLS et cookies déployés, persistance après arrêt/redémarrage, charge, courses multi-connexions, toutes variantes ORM, traitement d'une vraie demande et conformité complète. Aucun secret, donnée réelle, MySQL/Aiven, migration, serveur ou Edge n'est utilisé ; aucun changement de permissions, branche, commit, push ou suppression de travail.

## 9. Conservation documentaire et verdict

**PASS documentaire et conservation :** cinq documents complétés par ajout, deux fichiers créés, 105 fichiers examinés préexistants inchangés et 115 empreintes de sauvegarde conservées. Les 63 sources du manifeste correspondent toujours au passage retenu. Les 22 lignes de remarques restent identiques, C-07 PARTIEL ; fiches/réponses historiques et diagrammes ne sont pas modifiés. L'index conserve ses 197 repères et ajoute le test à sa vraie ligne, soit 198.

Quatre documents HTML relus structurellement, 46 références HTML locales et 914 références Markdown locales vérifiées dans 35 documents ; 317 références de lignes vérifiées et nouveau lien de scénario résolu. Les douze décisions figurent dans le tableau et les routes explicites du scénario correspondent au contrat Swagger. Ces contrôles n'ouvrent aucun lien externe et ne remplacent pas la recette visuelle/clavier réelle.

Branche, HEAD et index Git conservés. État final : **44 fichiers suivis modifiés, 53 non suivis, aucun fichier indexé**, comprenant le travail antérieur. Reçu : `final-validation.json` dans le dossier de preuves. Les preuves sous Temp sont susceptibles de nettoyage : leur conservation durable future doit être décidée sans modifier l'instantané 6E.1.

**GO pour revue et répétition technique isolée sur le périmètre démontré.** Ne pas annoncer une chaîne navigateur complète, une compatibilité MySQL/Aiven ou une conformité RGPD globale.

**Prochain lot recommandé, à autoriser : recette jury contrôlée.** D'abord confirmer le mode de présentation et les décisions humaines essentielles, puis autoriser une vérification de la cible et une recette navigateur isolée. Si le jury doit voir création de commentaire et signalement par boutons, autoriser séparément leur interface minimale sur les routes existantes ; cela ne justifie ni refonte du dashboard, ni nouvelle architecture, ni effacement de compte. Arrêt après 6E.3, en attente de validation.
