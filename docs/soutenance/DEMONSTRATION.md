# Fiche de démonstration

> Etat de diffusion scolaire du 3 novembre 2026 : suivre le [guide actuel](../../LIVRAISON_SCOLAIRE.md) et la [validation scolaire](VALIDATION_SCOLAIRE.md). Les sections de campagnes anterieures et leurs commandes sont historiques ; elles ne remplacent pas la procedure actuelle. Les chemins sous `C:\chemin\utilisateur` sont des exemples anonymises. Les archives internes signalees sont conservees localement.

## État courant — 2 novembre 2026

Lire d’abord les [supports 6H.1](SUPPORT_JURY_LOT6H1.md), l’[index courant](INDEX_CODE_LOT6H1.md) et la [procédure sur un autre PC](../../LIVRAISON_SCOLAIRE.md). Le bilan actuel distingue **854 tests historiques**, recette Edge réussie en SQLite fictif et contrôles documentaires de ce lot. Le modèle actuel contient dix tables et treize FK ; le compte est partagé sur dix pages, les signalements sont contextualisés, les likes de dossier/commentaire sont individuels.

Les compléments et questions ci-dessous conservent leur contexte historique. Les anciennes mentions de fonctions absentes, de neuf tables ou de recette non exécutée ne constituent pas l’état courant. Les 76 questions/réponses historiques restent conservées. Aucun résultat MySQL ou de déploiement n’est ajouté.


[Sommaire](README.md) · [Résultats attestés](TESTS_ET_VALIDATION.md) · [Réponses orales](ORAL_JURY.md)

**Parcours courant après 6F.2 :** utiliser le scénario de 14 minutes (archive interne non livree) et la recette manuelle isolée (archive interne non livree). Les sections historiques ci-dessous conservent leurs limites de campagne ; leurs mentions de formulaires absents ou d'actions non livrées ne décrivent pas toutes l'état actuel. **Ne pas utiliser le lancement normal ci-dessous pour cette recette : il lit `.env`.** Le kit dédié a passé son inspection sans serveur ; le lancement réseau/Edge exige toujours l'autorisation spécifique prévue en section 5 de la demande 6F.2.

## Préparation avant le jury

**Extension 6G.2 :** likes développés et preuves locales (archive interne non livree). Dans une future recette autorisée, Mélissa montre J’aime puis Retirer mon J’aime sur une fiche et un commentaire, et actualise pour vérifier l'état. Sylvie explique GET personnel, POST/DELETE, session/CSRF et absence de renvoi après réponse perdue. Mahamadou montre le couple unique de Vote/CommentLike et les comptes SQL. Les anciens compteurs non nuls bloquent la reprise ; ne pas les remettre à zéro pour démontrer la fonction. Le scénario navigateur reste NON EXÉCUTÉ.

Le kit 6F.2 et son manifeste restent figés : leurs empreintes refuseront les sources applicatives maintenant modifiées. Préparer/réinspecter un kit 6G.2 après validation avant toute recette réelle ; ne pas régénérer silencieusement l'ancien manifeste ou employer run_local.py avec une configuration privée.

Pour répartir les réponses et connaître les travaux restants, utiliser le [suivi du jury](SUIVI_REMARQUES_JURY.md) et la [préparation orale par membre](ORAL_JURY.md#répartition-de-la-préparation-orale--étape-51). Les sources Mermaid ajustées en 5.1 n'ont pas de nouveau rendu visuel validé ; les captures historiques conservent les défauts décrits dans le bilan 5.

Cette fiche décrit un parcours à préparer ; **elle ne prouve pas une nouvelle exécution**. Aucune base, donnée, migration ou configuration n'est modifiée pendant l'étape 5. Utiliser uniquement une recette isolée déjà préparée et explicitement autorisée, avec comptes et contenus fictifs.

La commande normale ci-dessous lit `.env`. Si les six paramètres Aiven sont présents, ils ont priorité sur `DATABASE_URL` : **définir seulement cette dernière n'isole pas le processus**. Le dispositif des campagnes précédentes neutralisait dotenv et verrouillait aussi les connexions. Le réutiliser suppose une revue adaptée au nouvel état des sources et un dossier neuf ; ne pas lever ses protections ni réinitialiser les anciennes bases.

Les mots de passe des campagnes 3/4 étaient éphémères : leurs bases conservées ne constituent pas un kit de connexion rejouable. La reprise signée de l'étape 4 n'est pas une commande de connexion ordinaire à présenter comme telle.

Prévoir avant la séance : versions Python/Node disponibles, base fictive autorisée avec neuf tables, catégories d'id 1 et 2, dossiers et contributions préparés, un lecteur et un administrateur créés par un processus de confiance. L'inscription publique ne crée pas un administrateur. L'installation complète et le peuplement depuis un clone vierge ne sont pas encore attestés comme procédure produit.

## Démarrage et adresses

Sur l'environnement de démonstration **dont la cible a déjà été vérifiée**, depuis PowerShell à la racine :

```powershell
.\.venv\Scripts\python.exe -B run_local.py
```

Ce lanceur ne prépare pas le schéma ni les données, et ne lance aucune migration. Les campagnes isolées utilisaient leurs propres enveloppes de protection ; voir leurs [commandes archivées](TESTS_ET_VALIDATION.md#3-étape-2--439-tests-automatiques-réussis).

| Écran | Adresse locale |
|---|---|
| Accueil | `http://127.0.0.1:5000/` |
| Histoires | `http://127.0.0.1:5000/histoires.html` |
| Cold Cases | `http://127.0.0.1:5000/coldcases.html` |
| Théories | `http://127.0.0.1:5000/theories.html` |
| Connexion lecteur | `http://127.0.0.1:5000/connexion.html` |
| Proposition | `http://127.0.0.1:5000/proposer-histoire.html` |
| Connexion admin | `http://127.0.0.1:5000/admin-connexion.html` |
| Tableau admin | `http://127.0.0.1:5000/admin-dashboard.html` |
| Swagger / contrat | `http://127.0.0.1:5000/api/v1/swagger` / `http://127.0.0.1:5000/api/v1/swagger.json` |

Arrêter avec **Ctrl+C**. Ne pas démarrer directement l'entrée historique `backend/index.py` avec son debug/écoute large. N'ouvrir aucune base distante pour improviser une démonstration.

## Parcours visiteur — environ deux minutes

1. Accueil : montrer les cartes chargées depuis l'API, au plus trois.
2. Histoires : rechercher un mot du titre ou du résumé ; préciser que le filtre travaille sur les données déjà chargées.
3. Cold Cases puis dossier : montrer slug, récit et images. Expliquer les replis lorsqu'une image manque.
4. Théories : sélectionner un dossier dans le lecteur public et actualiser. Une liste vide n'est pas un dossier absent.
5. Swagger : montrer les opérations et le contrat. Son affichage dépend normalement d'assets CDN ; les recettes ont fourni leurs copies localement. Ne pas annoncer un POST Swagger réussi.

## Parcours lecteur — sur base fictive autorisée

1. Se connecter par le formulaire avec les identifiants fictifs détenus localement. Montrer `/me` par son statut seulement, sans afficher le jeton ni le cookie.
2. Revenir sur l'accueil pour l'affichage du pseudo et le bouton de déconnexion ; ce contrôle de session n'est pas présent de manière identique sur toutes les pages.
3. Si les écritures de cette nouvelle séance sont autorisées : créer une théorie et une proposition fictives, une seule soumission chacune. Sinon, montrer les preuves enregistrées à l'étape 4.
4. Pour la théorie, sélectionner le même dossier dans le lecteur puis cliquer Actualiser. Le formulaire et le lecteur ont des sélections indépendantes.
5. Expliquer la chaîne de preuve : POST 201, GET de l'objet, SELECT des champs métier, puis relecture après redémarrage. Les preuves historiques sont déjà disponibles ; ne pas exécuter de SQL imprévu devant le jury.
6. Déconnecter depuis l'accueil, puis montrer qu'une lecture protégée ne garde pas les droits de la session.

## Parcours administrateur — consultation et utilisateurs

1. Utiliser le compte fictif administrateur sur l'écran prévu.
2. Montrer les sept compteurs et leur répartition, dont Propositions en attente, les propositions et signalements, puis Actualiser.
3. Expliquer que le HTML du tableau est public mais que les routes de données privées vérifient le rôle en base.
4. Démontrer un refus lecteur seulement avec le compte fictif et les requêtes autorisées ; les preuves 401/403/200 existent à l'étape 3.

Le lot 6A ajoute la gestion des utilisateurs : montrer pseudo, rôle, statut et protection des administrateurs. **Le parcours navigateur suivant est à préparer, pas attesté comme exécuté.** Après autorisation distincte d’une recette sur base fictive, annuler d’abord une confirmation puis bannir un compte ordinaire préparé ; relire le statut et vérifier le refus d’une session déjà ouverte. Ne jamais improviser cette action sur un compte réel.

Aucun bouton de publication, traitement des propositions, suppression de dossiers ou débannissement n’est livré. Voir le bilan 6A (archive interne non livree) pour les tests automatisés réellement exécutés.

## Comptes fictifs et valeurs privées

Le modèle CSV (archive interne non livree) contient deux identités inventées et des marqueurs, **aucun mot de passe utilisable**. Il n'est ni un script de création ni une configuration Flask. La colonne rôle sert à l'organisation de la séance, pas à attribuer une permission.

Copier le modèle **hors du dépôt** dans un fichier privé local, puis renseigner seulement cette copie. Ne pas mettre cette copie dans `frontend/` ou dans un autre chemin servi par le site. Les vrais identifiants restent dans ce fichier non suivi et ne doivent apparaître ni dans Git, ni dans les captures, ni dans les sorties console. L'étape 5 ne crée pas cette copie et ne change aucun compte.

## Disponible, partiel et restant

| État | Fonctionnalités |
|---|---|
| Interface disponible | Navigation/dossiers/images, recherche, inscription/connexion, sessions sur l'accueil, propositions, création et lecture de théories, tableau admin avec consultation et bannissement des utilisateurs ordinaires. |
| API seulement | Commentaires, votes, likes, signalements et lecture des mises à jour. Liste utilisateurs et bannissement sont maintenant raccordés au tableau. |
| Partiel | Propositions `pending` sans publication ; catégorie proposée incluse dans le texte ; actualisation manuelle ; catégories 1/2 fixes ; ancien libellé « maquette » à l'entrée admin. |
| Non développé ou non attesté | Gestion de consentement/demandes RGPD, récupération de mot de passe, pièces jointes, pagination, actions de modération dans le tableau ; validation MySQL/migrations et installation vierge complète non attestées. |

Afficher les nombres séparément : **439 tests automatiques**, **28/2/0/7 à l'étape 3**, et **15/1/0/1 à l'étape 4 avec dix BDD PASS**. Ne pas additionner ces campagnes et ne pas confondre Edge automatisé avec une recette humaine.

## Consultation administrative des dossiers — lot 6B

**Extension 6C.2, parcours navigateur proposé NON EXÉCUTÉ :** après préparation et migration séparément autorisées d’une base fictive, ouvrir Archives, demander l’aperçu de suppression, lire les nombres et annuler. Recommencer, saisir exactement le titre et cocher l’accord, puis confirmer. Le dossier et ses contributions disparaissent ; users/pending et les actifs déjà diminués par l’archive restent stables, commentaires/signalements globaux diminuent. Expliquer une réponse perdue : « Je relis le serveur sans répéter la suppression. Sans journal, une absence ne permet pas d’attribuer l’opération. » Ne pas improviser une purge sur données réelles. Voir le bilan (archive interne non livree).

**Extension 6C phase 1 — scénario navigateur proposé, NON EXÉCUTÉ.** Sur une base fictive autorisée et migrée séparément, noter les sept compteurs, ouvrir le filtre Actifs et annuler une confirmation d’archivage. Confirmer ensuite : le dossier quitte le public et ses compteurs actifs, sans changer commentaires/signalements/pending. Vérifier le slug public en 404. Ouvrir Archives, consulter texte et contributions, puis restaurer et retrouver le même slug et les mêmes contenus. Présenter les protections contre double clic et le message de relecture après erreur ; ne pas provoquer d’incident sur une cible réelle. Les preuves actuelles sont WSGI/SQLite mémoire et DOM simulé. Dire : « L'archivage masque un dossier du site public tout en conservant ses données pour une restauration éventuelle. Il ne constitue pas une suppression définitive. » Voir le bilan (archive interne non livree).

Ce parcours navigateur est à préparer après autorisation distincte ; les preuves 6B actuelles sont automatisées sans navigateur réel. Après connexion administrateur sur une base fictive préparée, montrer les dossiers, rechercher un titre, combiner les filtres et ouvrir la fiche par son lien. Montrer un résultat vide distinct d’une base vide. Si une catégorie non configurée est présente, son id est affiché dans Autres sans inventer son nom.

Le bouton global Actualiser recharge les données et remet recherche/filtre à zéro. Les sept compteurs actuels ne sont pas recalculés à partir des seuls résultats filtrés. La section utilisateurs et le bannissement 6A restent disponibles. Ne présenter aucune édition, archive ou suppression de dossier. Le bilan 6B (archive interne non livree) précise sa campagne historique ; le bilan 6D (archive interne non livree) décrit les sept compteurs actuels et leurs 561 tests.

## Scénarios proposés pour le septième compteur — lot 6D

**Préparation uniquement : aucun navigateur ni serveur lancé pendant 6D.** La recette 6A/6B reste reportée après le NO-GO VM. Dans un futur environnement autorisé et isolé, utiliser seulement des propositions fictives : aucune attente donne 0, une attente donne 1, deux attentes et d'autres statuts donnent 2. Vérifier les six autres valeurs et le maintien des filtres et du bannissement. Tester ensuite chargement (`—`), erreur (`—` et données masquées), Actualiser, réponse tardive et refus 401/403 effaçant les sept compteurs. Vérifier clavier et grille à plusieurs largeurs.

Ces scénarios sont couverts automatiquement sur DOM/API simulés et WSGI en mémoire ; leur rendu réel reste **NON EXÉCUTÉ**. Aucun nouveau droit de démarrage ou de préparation d'une base fichier n'est déduit de ce document.

## Complément 6E.2 — démonstration à autoriser séparément

Aucun navigateur, serveur, accès Aiven ni écriture dans la base du site n'est lancé pour ce lot. Les étapes suivantes sont un parcours de recette future, pas une campagne effectuée.

La réserve antérieure sur la comparaison exhaustive des ACL de la sauvegarde n'est ni levée ni corrigée dans 6E.2 : seule son existence et la conservation de ses 115 fichiers sont contrôlées en lecture seule.

## Scénario courant 6E.3 — 1er novembre 2026

Le scénario complet, les rôles, routes, données, confirmations et limites (archive interne non livree) remplace toute interprétation implicite d'un parcours navigateur déjà recetté. Il conserve les étapes ci-dessus comme préparation historique et détaille les alternatives en cas d'indisponibilité du navigateur ou de la base.

Le nouveau test réalise inscriptions, connexions, commentaire, signalement, lectures administratives, comparaison aux lignes SQLite, bannissement et contrôles d'intégrité. Les mots de passe, cookies et jetons ne figurent pas dans sa preuve. Ce parcours API/SQL est exécuté ; son rendu dans le navigateur ne l'est pas.

**Limite historique de 6E.3 :** les formulaires publics étaient absents. Ils sont maintenant développés dans le lot 6F.1 ci-dessous ; leur recette dans un navigateur réel reste à autoriser. Le dashboard consulte les signalements ; aucun bouton de résolution n'est ajouté.

Avant une recette réelle, confirmer l'état du schéma de la cible et les catégories 1/2, après autorisation distincte. Les essais SQLite mémoire créent les tables des modèles courants ; ils ne prouvent aucune migration déjà appliquée sur MySQL/Aiven. Ne pas charger les fixtures dans la base de présentation et ne pas ajuster des données pour embellir les compteurs.

## Parcours public 6F.1 — recette future à autoriser

Le bilan 6F.1 (archive interne non livree) décrit les parcours désormais développés et leurs limites. **723 PASS exécutés ; aucun navigateur ou serveur lancé.**

1. **Mélissa** : ouvrir une histoire ou un Cold Case, lire les commentaires et la notice, publier un texte approuvé puis Actualiser. Choisir ce commentaire avec Signaler, saisir le motif et Confirmer. Montrer qu'Annuler n'envoie rien et qu'un résultat incertain ne vaut pas réussite.
2. **Sylvie** : montrer `comments.js` et les helpers `api.js`. Expliquer GET `/me` avant chaque POST, cookie de session, `X-CSRF-Token`, contrôles Flask et réponse 201 seulement après commit. Le navigateur transmet du JSON ; il ne crée aucune ligne SQL lui-même.
3. **Mahamadou** : montrer les modèles existants `Comment` et `Report`, le lien entier `Report.comment_id`, SQLAlchemy/commit/rollback et la lecture administrative de cette même ligne. Les sept compteurs restent alimentés par les sources réelles ; zéro reste une valeur normale.

Vérifier la cible affichée avant confirmation. Le motif n'est pas publié dans la liste publique ; le signalement ne masque pas le commentaire et n'ajoute pas de résolution automatique. Ne pas démontrer un faux refus de doublon : plusieurs signalements sont permis par le modèle actuel.

Cette recette nécessite une autorisation distincte, des comptes/contenus approuvés et une cible isolée ou explicitement autorisée. Sans cela, présenter le code et les preuves DOM/API/SQLite, sans prétendre à une validation visuelle, une durabilité après redémarrage ou une compatibilité MySQL.
