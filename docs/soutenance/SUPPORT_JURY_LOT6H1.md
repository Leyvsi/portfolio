# Présentation courante — lot 6H.1

> Etat de diffusion scolaire du 3 novembre 2026 : suivre le [guide actuel](../../LIVRAISON_SCOLAIRE.md) et la [validation scolaire](VALIDATION_SCOLAIRE.md). Les sections de campagnes anterieures et leurs commandes sont historiques ; elles ne remplacent pas la procedure actuelle. Les chemins sous `C:\chemin\utilisateur` sont des exemples anonymises. Les archives internes signalees sont conservees localement.

État du 2 novembre 2026. Audit (archive interne non livree) · [70 repères du code](INDEX_CODE_LOT6H1.md) · [22 remarques](SUIVI_REMARQUES_JURY.md) · [Autre PC](../../LIVRAISON_SCOLAIRE.md).

Les anciens questionnaires des quatre fiches sont conservés. Ce support donne l’état à présenter aujourd’hui ; il ne remplace pas les preuves par une promesse de déploiement.

## Introduction commune — une minute

« Les Petits Enquêteurs permet de lire des dossiers, des Cold Cases et des théories. Un membre peut contribuer, commenter, signaler et ajouter ou retirer ses J’aime. L’administrateur consulte les données, bannit un compte ordinaire, archive ou restaure un dossier et peut supprimer un dossier déjà archivé avec une confirmation renforcée.

L’interface échange du JSON avec Flask. Flask contrôle les permissions, puis SQLAlchemy lit ou écrit dans la base. Pour notre recette, nous avons utilisé des données fictives et SQLite isolé. Les compteurs viennent des enregistrements de cette base.

Nous avons 854 tests réussis dans la campagne du 1er novembre et une recette humaine Edge distincte. La démonstration locale est validée ; cela ne prouve pas une installation MySQL distante ni une conformité RGPD complète. »

## Mélissa — montrer le frontend et expliquer le DOM

Temps indicatif : trois minutes. Fichiers : `frontend/app.js`, `api.js`, `comments.js`, `likes.js`, `admin-dashboard.js`, HTML et CSS. Les liens précis sont dans l’index courant.

« Le DOM est l’arbre des éléments de la page. JavaScript crée une carte avec `createElement`, place le texte avec `textContent` et attache un événement au bouton. Le texte reçu n’est pas interprété comme du HTML.

Les appels passent par `apiRequest`. Pendant une écriture, le bouton est bloqué pour éviter un double envoi. Une erreur conserve la saisie. Une réponse perdue ne déclenche pas automatiquement un second POST.

Le compte affiché vient de `/me`. Il apparaît sur les dix pages et le bouton Déconnexion attend le serveur. Nous avons aussi corrigé un problème de cache : Edge réutilisait d’anciennes pages. Après actualisation complète, l’identité et la catégorie du signalement étaient correctes. Le serveur local utilisera `no-store` au prochain démarrage.

Pour un J’aime, je relis le nombre et mon état personnel sur le serveur. Je n’ajoute pas simplement 1 dans la page. Le contrôle du commentaire est dans sa propre carte ; il est distinct de celui du dossier. »

À montrer : dossier, commentaire, signalement contextualisé, ajout/retrait et actualisation. Les preuves Edge existent pour ces parcours. Le clavier, le mobile et un lecteur d’écran n’ont pas fait l’objet d’une recette exhaustive.

## Sylvie — expliquer Flask, l’API et les protections

Temps indicatif : trois minutes. Fichiers : `backend/index.py`, `api/v1/views/permissions.py`, vues métier et `swagger.json`.

« Une route associe une URL et une méthode HTTP à une fonction Flask. Par exemple, GET lit les commentaires et POST crée un commentaire. Le JSON transporte les données. HTTP 201 confirme une création ; 401 signifie session absente, 403 accès refusé et 409 conflit métier.

Les mots de passe sont hachés avec Werkzeug. Le cookie de session est signé ; il n’est pas chiffré. Les routes protégées relisent le compte en base, son bannissement et son rôle. Un bouton caché ne constitue pas une permission.

Le CSRF est un jeton lié à la session, transmis dans `X-CSRF-Token` pour les écritures authentifiées. La connexion est une exception prévue. Les requêtes anonymes passent ce filtre, mais les vues continuent d’appliquer leurs permissions.

L’auteur vient de la session, pas d’un identifiant libre envoyé par le navigateur. Les erreurs SQL gérées déclenchent un rollback. Si le commit a déjà eu lieu et que la réponse se perd, un rollback ultérieur ne défait pas ce commit ; le client relit sans répéter l’écriture. »

À distinguer : 27 chemins et 36 opérations OpenAPI déclarées ; affichage de Swagger et exécution de ses POST ; session absente et erreur métier. Ne montrer ni cookie, ni jeton, ni mot de passe au jury. La déconnexion a été constatée dans Edge par POST 200 puis `/me` 401 ; elle ne constitue pas une révocation centrale de toutes les copies possibles d’un cookie.

## Mahamadou — expliquer SQLAlchemy et les données

Temps indicatif : trois minutes. Fichiers : `backend/models.py`, migrations candidates, services de likes/suppression et fonction des compteurs.

« Nous déclarons dix tables et treize clés étrangères. La clé primaire identifie une ligne. Une clé étrangère relie deux tables. Une contrainte unique empêche un doublon : un compte ne peut avoir qu’un Vote par dossier et qu’un CommentLike par commentaire.

Le nombre de J’aime provient de COUNT sur ces lignes. Les anciens compteurs de commentaires sont conservés : s’ils ne valent pas exactement zéro, les nouveaux likes individuels sont bloqués. Nous ne pouvons pas inventer les auteurs d’anciens clics.

Le dashboard assemble sept valeurs depuis les lectures serveur. Les catégories 1 et 2 correspondent au classement actuel des dossiers. Les propositions en attente sont celles dont le statut est exactement `pending`. Aucune statistique n’est ajoutée pour remplir le tableau.

Archiver conserve le dossier et ses contributions, en le masquant du public. Restaurer le rend à nouveau visible. Supprimer définitivement un dossier déjà archivé retire ses dépendances dans une transaction contrôlée. Les comptes et les autres dossiers sont conservés. CASCADE est une règle SQL ; la cascade ORM est un mécanisme distinct. »

À préciser : les tests de FK et de suppression utilisent SQLite isolé. Les sept migrations forment une chaîne candidate ; aucune migration Aiven n’a été appliquée par les recettes. Une sauvegarde du code n’est pas une sauvegarde des interactions stockées en base.

## Démonstration proposée — cinq minutes

Ce scénario est préparé, pas exécuté à nouveau en 6H.1. Le lancement futur exige l’autorisation distincte décrite dans le guide.

1. Ouvrir le kit local isolé et annoncer les données fictives. Montrer une histoire et un Cold Case, puis le compte sur les différentes pages.
2. Avec un compte membre fictif, commenter et signaler. Montrer le succès confirmé et la relecture. Les compteurs évoluent uniquement avec ces opérations réelles dans la base de test.
3. Ajouter puis retirer le J’aime du dossier et du commentaire ; actualiser après chaque action. Montrer les deux compteurs distincts.
4. Se connecter comme administrateur, consulter les sept valeurs et le signalement avec commentaire, dossier, catégorie et motif.
5. Se déconnecter depuis Histoires, puis montrer que le tableau ne conserve pas ses données privées après consultation/actualisation.

L’inscription, les créations de commentaires/signalements et le bannissement ont des preuves Edge dans la recette initiale. Les affichages corrigés, les deux cycles de likes, les sept valeurs et la déconnexion ont leurs preuves complémentaires. La suppression, l’archivage et la restauration sont développés et testés automatiquement, mais ne sont pas présentés comme déjà exercés humainement dans Edge. Ne pas improviser une suppression pendant l’oral.

## Questions courtes à répéter

| Question | Réponse simple |
|---|---|
| Le frontend est-il la base ? | Non. Il affiche les réponses ; Flask et SQLAlchemy accèdent à la base. |
| Pourquoi un J’aime n’est-il pas un compteur local ? | Une ligne unique lie le compte à la cible ; le serveur la compte. |
| Pourquoi un administrateur ne choisit-il pas son rôle dans le navigateur ? | Le serveur relit le rôle de son compte en base. |
| Bannir supprime-t-il le compte ? | Non. Le compte est conservé et ses accès authentifiés sont refusés. |
| Archiver signifie-t-il effacer ? | Non. Les données sont conservées pour une restauration. |
| Une FK et une relation ORM sont-elles identiques ? | Non. La FK agit dans SQL ; la relation organise les objets Python. |
| 854 PASS signifie-t-il 854 essais Edge ? | Non. Il s’agit de suites Python/Node ; la recette humaine est comptée séparément. |
| Est-ce conforme au RGPD ? | Nous avons des protections et des notices provisoires ; les décisions de responsabilité, contact, bases, conservation et droits restent à valider. |
| Les illustrations sont-elles libres ? | Leur provenance et leurs droits ne sont pas confirmés ; nous ne les présentons pas comme libres. |
| Le site est-il livré publiquement ? | Non. Le GO porte sur la démonstration locale isolée. L’audit Git ne publie rien. |

La répartition est celle annoncée par l’équipe ; elle ne prétend pas attribuer automatiquement chaque ligne non commitée à un étudiant.
