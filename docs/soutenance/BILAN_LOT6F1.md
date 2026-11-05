# Lot 6F.1 — commentaires et signalements publics

> Archive pédagogique datée : les résultats et descriptions ci-dessous concernent le lot indiqué. Les anciens repères de ligne ne décrivent pas la version candidate. Pour préparer la soutenance actuelle, consulter les quatre fiches et le référentiel reliés au sommaire.

> Copie publique de référence : les chemins personnels et liens de travail internes sont retirés. Les preuves et commandes historiques gardent leur date et leur périmètre ; utiliser le README actuel pour le lancement.

[Sommaire](README.md) · [Bilan précédent](BILAN_LOT6E3.md) · [Démonstration](DEMONSTRATION.md) · [Tests](TESTS_ET_VALIDATION.md)

**1er novembre 2026 : parcours frontend implémentés, 723 tests réussis : 279 backend, 428 frontend, 16 lanceur.** Aucune régression détectée dans les suites exécutées. Sept tests de migration volontairement non exécutés. Aucun navigateur ou serveur lancé ; aucune validation MySQL/Aiven revendiquée.

## 1. Périmètre et fichiers

Branche conservée : `feature/frontend-api-integration`. HEAD conservé : `07a9f03ea0a3bdad4a07066fdd7bab1997cc158b`. Départ : 44 fichiers suivis modifiés, 53 non suivis, aucun fichier indexé. Le travail antérieur est conservé ; aucun commit, push ou changement de branche.

| Fichier | Changement propre à 6F.1 |
|---|---|
| [frontend/dossier.html](../../frontend/dossier.html) | Zone de lecture, formulaire de commentaire, sélection/motif/confirmation d'un signalement, notices et retours accessibles |
| [frontend/comments.js](../../frontend/comments.js) — créé | Contrôleur de lecture/écriture, cible, validations, verrou d'envoi, erreurs et résultats incertains |
| [frontend/api.js](../../frontend/api.js) | Helpers ajoutés en fin de fichier ; routes existantes et validation des réponses |
| [frontend/app.js](../../frontend/app.js) | Démarrage du panneau après résolution effective du dossier par slug |
| [frontend/styles.css](../../frontend/styles.css) | Styles ajoutés limités à `.story-comments`, dont masquage effectif des éléments `hidden` |
| [frontend/tests/comments.test.cjs](../../frontend/tests/comments.test.cjs) — créé | 64 nouveaux tests, vrais scripts frontend dans un DOM et une API simulés |
| [frontend/README.md](../../frontend/README.md) | Contrat et limites des nouveaux parcours |
| [docs/soutenance/BILAN_LOT6F1.md](BILAN_LOT6F1.md) — créé | Présent rapport |
| [docs/soutenance/README.md](README.md) | Sommaire et état courant |
| [docs/soutenance/DEMONSTRATION.md](DEMONSTRATION.md) | Scénario court à trois et recette future |
| [docs/soutenance/TESTS_ET_VALIDATION.md](TESTS_ET_VALIDATION.md) | Résultats actuels séparés des campagnes historiques |
| [docs/soutenance/SUIVI_REMARQUES_JURY.md](SUIVI_REMARQUES_JURY.md) | Actualisation sans modifier les 22 remarques |
| [docs/soutenance/INDEX_CODE_JURY.md](INDEX_CODE_JURY.md) | Six nouveaux repères, lignes existantes actualisées |
| [docs/soutenance/fiche-commune.md](fiche-commune.md), [fiche-melissa.md](fiche-melissa.md) | Références de lignes de `app.js` uniquement, réponses orales conservées |

Backend applicatif, modèles, Swagger, migrations, tests backend/lanceur et tests frontend antérieurs inchangés pendant ce lot. Dashboard HTML/JS et panneaux administratifs inchangés. Les styles préexistants sont conservés ; aucune donnée n'est injectée pour alimenter les compteurs.

Les 112 sources/documents précédemment examinés sont épinglés avant modification dans `baseline.json` ; copies des fichiers à éditer et preuves conservées hors dépôt dans :

```text
[chemin local privé retiré]
```

Les sept exclusions antérieures restent exclues : `frontend/donnees.js`, `frontend/histoires-originales.json`, CSV de comptes et quatre images WebP. Aucune lecture du `.env`, base réelle, cookie ou certificat. La sauvegarde durable 6E.1 n'est pas modifiée ; ces preuves temporaires ne remplacent pas une nouvelle sauvegarde durable.

## 2. Audit ciblé et routes effectivement utilisées

Le bilan 6E.3, les vues commentaires/signalements, les permissions, la protection CSRF de `backend/index.py`, les modèles et les contrôleurs frontend ont été examinés. **Aucun changement backend nécessaire au raccordement.** La page `dossier.html?slug=...` est commune aux histoires résolues et Cold Cases. Le panneau ne démarre qu'après une lecture réussie du dossier réel ; aucun id inventé depuis le rang d'une carte.

| Route | Paramètres et résultat attendu |
|---|---|
| `GET /api/v1/stories/slug/{slug}` | Slug encodé ; 200 avec dossier et id réel, 404 si absent/archivé |
| `GET /api/v1/stories/{story_id}/comments` | Lecture publique ; 200 liste, y compris vide ; 404 dossier indisponible |
| `GET /api/v1/me` | Avant chaque envoi ; 200 avec compte et `csrf_token`, 401 sans session, 403 compte suspendu |
| `POST /api/v1/stories/{story_id}/comments` | JSON `{"text":"..."}` ; 201 avec `{"status":"success","comment":{...}}` après commit |
| `POST /api/v1/comments/{comment_id}/report` | JSON `{"reason":"..."}` ; 201 avec `{"status":"success","report":{...}}` après commit |

Les POST emploient le cookie via `credentials: 'include'` et `X-CSRF-Token` en mémoire. Aucun auteur, rôle, compteur, type ou id d'histoire supplémentaire n'est envoyé dans leurs JSON. Les erreurs 400, 401, 403, 404 sont affichées sans réussite ni effacement du brouillon. Un éventuel 409 reste un refus ; ce code n'établit pas une règle de doublon absente du backend.

La route générique `/reports` existe mais n'est pas utilisée par ces formulaires. **Les signalements concernent exclusivement les commentaires** : `Report.comment_id`, entier correspondant à `Comment.id`, FK `ON DELETE CASCADE`. Le contrat JSON expose `type: "comment"` et `target_id` comme chaîne canonique de cet entier. Aucune migration préparée ou exécutée dans ce lot ; l'état du schéma de la cible reste à vérifier séparément.

## 3. Parcours commentaire

1. Lire le dossier puis charger sa liste de commentaires. Chargement, liste vide, erreur et dossier absent sont distingués ; **Actualiser les commentaires** relit le serveur.
2. Lire la notice : texte et pseudonyme publics, éviter les données personnelles des tiers. Saisir un texte obligatoire ; contrôle du volume UTF-8 de 65 535 octets après retrait des espaces aux extrémités et refus des demi-surrogates invalides. Le serveur conserve l'autorité sur la validation.
3. Cliquer **Publier le commentaire**. Verrouiller immédiatement les envois, vérifier `/me` et son CSRF puis appeler le POST. Un compte absent, banni ou une session sans jeton ne provoque aucune création depuis le formulaire.
4. Attendre 201, un statut `success` et un commentaire cohérent avec le dossier. Afficher cet objet confirmé dans la liste, vider la saisie et annoncer l'enregistrement. La relecture reste disponible pour vérifier le résultat sauvegardé.

Le navigateur ne crée aucune ligne SQL directement. Flask déduit l'auteur de la session et prépare `Comment` ; SQLAlchemy effectue le flush/commit. Le 201 intervient après commit. La présence immédiate dans la liste vient de cette réponse confirmée, sans copie narrative locale de repli.

## 4. Parcours signalement et administration

1. Choisir **Signaler** sur un commentaire reçu par le GET. Le formulaire affiche son id et son pseudonyme ; le motif n'est jamais réattribué silencieusement à une autre cible. Annuler ferme le formulaire sans requête d'écriture.
2. Lire la notice : motif destiné à l'administration, éviter les informations privées inutiles ; aucun masquage automatique du commentaire. Saisir le motif dans les mêmes limites TEXT.
3. Cliquer **Confirmer le signalement**, vérifier `/me` puis envoyer seulement `reason` sur le chemin du commentaire sélectionné.
4. Annoncer l'enregistrement uniquement après 201, `success`, id de signalement positif, `type: "comment"` et `target_id` égal exactement à la cible sélectionnée. Fermer et vider le formulaire après cette confirmation.

Flask vérifie commentaire et dossier actif ; SQLAlchemy insère `Report(comment_id=..., reason=...)` et commit. L'administration existante retrouve cette même ligne via `GET /api/v1/admin/reports`, après contrôle administrateur. **La nouvelle interface publique n'appelle jamais cette route** et n'affiche ni motifs des autres signalements, ni statuts administratifs. Le signalement ne résout ni ne supprime automatiquement le commentaire.

Le modèle n'enregistre pas l'identité de l'émetteur et n'impose pas d'unicité par cible : plusieurs signalements sont autorisés. Le verrou empêche les doubles clics accidentels pendant une opération ; il n'interdit pas un nouvel envoi volontaire après succès. Aucun compteur local de modération n'est fabriqué.

## 5. Sécurité et résultats incertains

- Session relue avant chaque écriture ; permissions et CSRF à nouveau contrôlés côté Flask. Un bouton visible n'accorde aucun droit serveur.
- Ids numériques bornés ; liste refusée si doublons, mauvais dossier ou structure incohérente. Cible de signalement capturée depuis le commentaire reçu.
- Rendu des pseudonymes, contributions, cibles et messages par `textContent`, jamais `innerHTML`. Les retours à la ligne du commentaire restent du texte.
- Verrou commun dès le début de `/me`, champs et contrôles désactivés pendant l'envoi. Aucun retry automatique. Les boutons de changement de cible et d'actualisation sont aussi protégés.
- Timeout, perte de connexion, 5xx, statut inattendu, JSON illisible/incohérent après un POST : **résultat incertain**, brouillon conservé, aucune réussite annoncée, nouveaux envois de ce type bloqués pour cette instance de page. Une telle erreur peut survenir après commit.
- Pour un commentaire incertain, actualiser la liste sans répéter le POST. Une correspondance de texte n'est pas une preuve d'identité de l'opération. Pour un signalement incertain, faire vérifier par l'administration ; aucun accès public à ses données n'est ajouté. Un rechargement complet ne doit intervenir qu'après vérification ; le verrou local ne survit pas à ce rechargement.
- Une disparition du dossier/commentaire vide la liste et bloque l'écriture jusqu'à une nouvelle lecture valide. Quitter la page annule les lectures et ignore leurs réponses tardives. Un retour depuis le cache exige un rechargement avant nouvelle écriture ; il ne relance aucun POST.

Aucun reçu persistant, stockage de jeton, mot de passe ou motif dans `localStorage`/`sessionStorage`, nouveau cookie, ordonnanceur ou journal d'audit n'est ajouté. Le rollback SQL des routes existantes reste inchangé. **L'absence d'idempotence serveur et de reçu persistant limite la résolution d'un résultat incertain**, notamment après rechargement ou entre onglets.

## 6. Tests réellement exécutés

| Suite | Dernière campagne complète 6F.1 | Résultat |
|---|---:|---|
| Backend sélectionné — vues réelles et SQLite mémoire | 279 | PASS, aucun échec/erreur/ignoré |
| Frontend — scripts réels, DOM/API simulés | 428 = 364 existants + 64 nouveaux | PASS, aucun échec/annulé/ignoré |
| Lanceur et contrats HTML/WSGI | 16 | PASS, aucun échec/erreur/ignoré |
| **Total** | **723** | **PASS** |

`attempt-1` : première vérification frontend, 425 PASS. Trois scénarios supplémentaires ont ensuite été ajoutés (POST en attente pour chaque formulaire et archive restaurée). **`attempt-2` est la campagne complète finale, 723 PASS**, sans addition avec `attempt-1` ou les 659 PASS historiques de 6E.3. Aucun ancien test ou assertion n'est modifié pour obtenir ces résultats.

Les 64 nouveaux cas couvrent : HTML/notices/scripts/hidden ; lecture publique/vide/incohérente/en erreur ; XSS ; ancien auteur sans référence ; création confirmée puis relecture ; cible exacte et annulation ; comportement sans règle d'unicité ; validations vides/UTF-8/Unicode pour chaque formulaire ; session, jeton, refus HTTP ; doubles clics pendant `/me` et POST ; réseau, 500, 200 inattendu, JSON invalide, mauvaise cible/dossier, timeout ; lecture tardive/pagehide/retour cache ; intégration réelle de `app.js` dans les deux catégories, dossier absent et absence d'effets sur les autres pages.

Les suites administrateur existantes vérifient encore les sept indicateurs et les autres parcours. Le test backend `test_moderation_journey` réalise de vraies requêtes Flask avec commits SQLite mémoire : commentaire, signalement, consultation administrative, agrégats comparés aux lignes SQL et FK. **Cette preuve et les tests frontend sont complémentaires, sans constituer un test navigateur de bout en bout.**

Les six tests de `test_report_migration.py` et le cas de migration d'archivage restent exclus, avant exécution ; ils ne sont pas comptés comme PASS. Liste exacte conservée dans `backend.guard.json` et le bilan 6E.3.

Harnais inspecté avant lancement : environnement enfant minimal sans configuration privée héritée, dotenv neutralisé, Aiven vide, SQLite exclusivement `:memory:` et FK activées sur chaque connexion, bases fichier/MySQL/ATTACH/DETACH bloqués. Réseau/DNS, sous-processus applicatifs, lectures privées, écritures du dépôt et exécution des migrations bloqués. Les sondes de refus sont séparées. **Tous les compteurs interdits des suites valent zéro.** Les 65 sources autorisées sont épinglées par SHA-256.

Preuves : `preflight.json`, `harness-inspection.json`, `attempt-2/commands.json`, journaux stdout/stderr, `backend.guard.json`, `launcher.guard.json`, `attempt-2/frontend.node-guard.json`, `moderation-journey.json` et `final-validation.json` dans le répertoire ci-dessus.

Contrôle final réussi : 12 fichiers préexistants modifiés et 3 créés, 100 autres fichiers examinés préservés ; backend, modèles, migrations, tests antérieurs, fichiers administratifs et 115 fichiers de la sauvegarde durable identiques par SHA-256. HTML : identifiants, labels, références ARIA et 52 liens locaux contrôlés sur quatre pages. Documentation : 204 repères dans l'index et 22 remarques conservées. État final : 45 fichiers suivis modifiés, 56 non suivis, aucun indexé ; branche, HEAD et empreinte de l'index conservés. Ce constat distingue les changements 6F.1 du travail antérieur non commité.

## 7. Limites et recette navigateur restante

**NON EXÉCUTÉS :** navigateur réel/Edge, serveur Flask, navigation au clavier réelle, lecteur d'écran, rendu mobile, session/cookies effectifs dans le navigateur, recette intégrée frontend/API/base de présentation, persistance après redémarrage, concurrence entre onglets ou connexions MySQL, migrations et cible Aiven.

Après autorisation distincte, vérifier visuellement les deux catégories, connexion/déconnexion, publication et relecture après navigation, ciblage/annulation/confirmation du signalement, refus d'un compte banni, CSRF, lenteur/erreur, doubles clics, focus, masquage du formulaire, notices et responsive. Examiner le signalement dans l'administration avec un compte autorisé et comparer les compteurs réels. Aucun faux enregistrement destiné à remplir le dashboard.

Limites existantes conservées : pas de pagination ou protection anti-spam nouvelle ; chargement intégral de la liste ; pas d'unicité des signalements ni identification SQL de leur émetteur ; pas de résolution de modération ajoutée ; pseudonyme copié dans les commentaires ; politique complète toujours non publiée, décisions humaines RGPD non inventées. L'hypothèse des catégories 1/2 et l'état réel du schéma restent à confirmer avant présentation.

## 8. Démonstration devant le jury

Scénario à effectuer seulement dans une recette autorisée avec contenus et comptes approuvés :

1. **Mélissa** ouvre un dossier depuis Histoires ou Cold Cases, montre la lecture publique, la notice, publie un commentaire et utilise Actualiser pour le relire. Elle sélectionne ce commentaire, indique le motif et confirme le signalement. Elle distingue message confirmé et résultat incertain.
2. **Sylvie** explique les quatre routes utiles après ouverture du dossier : GET commentaires, GET `/me` avant chaque envoi, POST commentaire, POST signalement. Flask vérifie session active, CSRF, textes et dossier actif ; le serveur déduit l'auteur du commentaire. Le CSRF limite les écritures induites depuis une autre origine et ne remplace pas l'authentification.
3. **Mahamadou** explique `Comment.story_id`, l'auteur et le pseudonyme copié, puis la FK entière `Report.comment_id`. `commit` valide l'enregistrement ; un échec SQL entraîne rollback dans les routes existantes. Il retrouve la ligne par la consultation administrative et explique que les compteurs reflètent les données, y compris zéro.

Si la recette n'est pas autorisée/disponible, montrer code, 723 PASS et preuve API/SQL isolée ; ne pas annoncer que le parcours navigateur ou Aiven a été validé.

## 9. Prochaine phase recommandée

**GO pour la revue du lot 6F.1 ; recette navigateur et déploiement restent à valider.** Proposer une courte recette locale autorisée et isolée sur les fonctions développées, sans refonte RGPD, modification du dashboard, migration implicite ni ajout artificiel de données. Les choix de publication RGPD attendent toujours l'équipe.

Le travail s'arrête à 6F.1. Aucune phase suivante engagée sans validation de l'utilisateur.
