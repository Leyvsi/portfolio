# Bilan local — lot 6H.18.3

> Archive pédagogique datée : les résultats et descriptions ci-dessous concernent le lot indiqué. Les anciens repères de ligne ne décrivent pas la version candidate. Pour préparer la soutenance actuelle, consulter les quatre fiches et le référentiel reliés au sommaire.

> Copie publique de référence : les chemins personnels et liens de travail internes sont retirés. Les preuves et commandes historiques gardent leur date et leur périmètre ; utiliser le README actuel pour le lancement.

Date : 4 novembre 2026, Europe/Paris.
Projet : `[chemin local privé retiré]`.

**Résultat : les cinq formulations ont été observées dans Microsoft Edge avec
Flask et les comptes permanents.** Quatre confirmations ont été capturées par
le contrôleur ; celle du signalement a été confirmée directement par l'utilisateur
dans la fenêtre Edge de Bob après interruption du contrôleur. Le test complémentaire
de refus CSRF reste non concluant et n'est pas présenté comme réussi.

## Autorisations et périmètre

L'utilisateur a donné deux autorisations distinctes : ouverture d'Edge avec des
sessions temporaires pour les connexions et les lectures, puis création d'un
commentaire, d'une théorie et d'un signalement marqués « Validation 6H.18.3 »,
avec ajout puis retrait d'un nouveau J’aime de test et contrôles des doubles clics.

Le serveur persistant fonctionnait déjà. Aucun lancement, arrêt ou redémarrage
de Flask n'a été nécessaire. Aucune réinitialisation, réparation, migration,
création de compte ou connexion MySQL/Aiven n'a été effectuée.

## État initial réellement contrôlé

- Les connexions TCP directes aux ports 5064 et 5066 sont acceptées. Un premier
  relevé CIM sans correspondance a été corrigé par ces connexions et des GET HTTP
  réels ; il ne permettait pas de conclure à l'arrêt des instances.
- Base existante : `instance/demo-persistante/portfolio.sqlite3`. La clé de session
  est présente ; son contenu n'a pas été lu ou exporté par l'audit.
- Les trois comptes permanents sont présents, actifs et non suspendus : admin,
  Alice et Bob. Admin seul possède le rôle administrateur.
- Les inspections SQLite initiale et finale utilisent `mode=ro`, `query_only=ON`
  et une transaction de lecture. Le schéma correspond aux modèles ; intégrité,
  clés étrangères et journal DELETE sont conformes.
- Le contrôle CLI habituel a refusé la concurrence avec le serveur existant.
  Son verrou a été préservé ; aucune opération exclusive n'a été forcée.
- Le GET Flask `/api/v1/stories` fournit les six originaux complets, conformes au
  catalogue approuvé, sans original manquant, modifié ou archivé.
- Les quatre JavaScript servis correspondent aux fichiers du lot 6H.18.2. Les
  41 empreintes du manifeste sont conformes ; aucune source du kit n'est modifiée.

## Validation réelle dans Edge

Navigateur : **Microsoft Edge 156.0.4314.58**, lancé avec interface visible et
environnement temporaire, distinct des sessions habituelles. Les contextes admin,
Alice, Bob et anonyme sont indépendants. Aucun profil Edge habituel n'est ouvert
par le contrôleur. Aucun mot de passe, cookie, jeton, HAR, trace ou formulaire de
connexion n'est exporté dans les rapports ou les captures.

L'utilisateur a saisi lui-même ses mots de passe dans Edge. Les trois connexions
ont abouti ; `/me` a confirmé les identifiants internes 1/2/3 et les rôles
administrateur/utilisateur/utilisateur, sans recopier de réponse d'authentification.
Les trois sessions ont été relues indépendamment après navigation et actualisation.

Les six fiches ont réellement été ouvertes et comparées au catalogue dans le DOM :

| Identifiant | Slug | Titre, résumé et texte intégral | Intertitres |
| ---: | --- | --- | ---: |
| 101 | golden-state-killer | Identiques mot pour mot | 5 |
| 102 | chris-watts | Identiques mot pour mot | 5 |
| 103 | michelle-carter | Identiques mot pour mot | 4 |
| 201 | anthonioz | Identiques mot pour mot, version B | 5 |
| 202 | noirval | Identiques mot pour mot, version B | 5 |
| 203 | manoir-de-l-ombre | Identiques mot pour mot | 5 |

### Confirmations

| Action | Message réel | Preuve et résultat |
| --- | --- | --- |
| Nouveau J’aime d'Alice sur le dossier 102 | J’aime ajouté. | Capture ciblée et GET personnel ; compteur 0 → 1, conservé après actualisation |
| Retrait de ce seul nouveau J’aime | J’aime retiré. | Capture ciblée et GET personnel ; compteur 1 → 0, conservé après actualisation |
| Commentaire d'Alice sur le dossier 102 | Commentaire publié. | Capture ciblée ; commentaire n° 3 unique, toujours visible après actualisation |
| Théorie d'Alice sur le dossier 201 | Théorie publiée. | Capture ciblée ; théorie n° 2 unique, retrouvée dans la liste après actualisation |
| Signalement de Bob sur le nouveau commentaire | Votre signalement a été pris en compte. | Signalement n° 2 relu dans SQLite ; message exact confirmé par l'utilisateur dans Edge |

Les captures des quatre premières confirmations ne contiennent que le message
concerné et sont conservées hors du dépôt, dans le dossier local
`[chemin local privé retiré]`.
La confirmation du signalement n'a pas de capture automatisée.

Les cinq formulations sont courtes et ne contiennent pas « État actuel relu sur
le serveur ». Les actions de création et retrait de like, commentaire et théorie
ont reçu les statuts réels attendus : 201, 200, 201 et 201.

### Erreurs, doubles clics et compteurs

- Une session anonyme affiche « Connectez-vous pour aimer ou retirer votre J’aime. »
  et son bouton J’aime est désactivé.
- Alice voit le refus d'accès au dashboard administrateur. Le GET réel
  `/api/v1/admin/reports` renvoie HTTP 403 ; les données administrateur sont masquées.
- `/stats` est public par conception et renvoie 200 avec trois agrégats. Une
  première attente erronée de 403 dans le contrôleur a été corrigée hors du projet,
  sans modifier l'application ou réauthentifier les comptes.
- Les doubles clics sur les actions J’aime, commentaire et théorie produisent
  chacun une seule requête d'écriture. Le premier essai du contrôleur s'était
  arrêté avant toute écriture sur un sélecteur trop large ; sa correction hors du
  projet n'a provoqué aucune duplication.
- Le signalement marqué du lot existe une seule fois. La capture réseau finale
  a été interrompue : l'absence de doublon de ce signalement est confirmée par
  la donnée enregistrée, pas par une trace réseau complète.
- Les sept indicateurs du dashboard ont été vérifiés après les trois connexions
  et après actualisation : 6 dossiers, 3 histoires résolues, 3 Cold Cases,
  3 utilisateurs, 2 commentaires, 1 signalement et 0 proposition en attente.
- Les nouveaux commentaire et théorie ont été relus dans les listes d'Edge après
  actualisation. Les données finales ont également été relues directement dans
  SQLite. Le dashboard après toutes les contributions n'a pas été recapturé
  automatiquement après l'interruption du contrôleur.

## Données conservées à la fin

| Table | Avant | Après |
| --- | ---: | ---: |
| categories | 2 | 2 |
| users | 3 | 3 |
| stories | 6 | 6 |
| comments | 2 | 3 |
| theories | 1 | 2 |
| votes | 2 | 2 |
| comment_likes | 2 | 2 |
| reports | 1 | 3 |
| proposals | 0 | 0 |
| cold_case_updates | 0 | 0 |

Les contributions de contrôle conservées sont le commentaire **3**, la théorie
**2** et le signalement **2**. Aucun like préexistant n'a été retiré.

Le second signalement ajouté pendant la séance est distinct du texte de contrôle.
L'utilisateur a confirmé l'avoir envoyé manuellement. Il explique le passage
de 1 à 3 signalements, au lieu de 1 à 2 pour le seul scénario automatisé.
Il est conservé ; aucun contenu de son motif n'est reproduit ici.

## Point non conclu et limites

Le scénario complémentaire visant un refus CSRF n'a pas obtenu le 403 attendu :
la tentative a créé le signalement autorisé. Le contrôleur s'est ensuite interrompu
avant sa capture finale ; sa cause d'interruption n'est pas établie. L'en-tête
effectivement transmis n'a pas été enregistré. Cette tentative ne démontre donc
ni un rejet CSRF réussi, ni une défaillance de la protection Flask.

La protection CSRF n'a été désactivée ou modifiée à aucun moment. Ce contrôle
négatif devra être repris dans un essai distinct et maîtrisé, sans créer un
nouveau signalement sans autorisation. Aucun nouvel envoi automatique n'a suivi
l'interruption ; le résultat a d'abord été vérifié en lecture seule.

Les erreurs de session anonyme et de permission administrateur ont, elles, été
vérifiées réellement. Aucune simulation de panne réseau incertaine n'a été ajoutée
sur la base permanente. Les tests simulés du lot 6H.18.2 restent distincts et les
567 tests ne sont pas relancés ni comptés comme nouvelle validation Edge.

La persistance vérifiée dans ce lot porte sur l'actualisation du navigateur et
les relectures de la base, pas sur un nouveau redémarrage de Flask.

## Préservation et clôture

Seul `docs/soutenance/BILAN_LOT6H18_3.md` est ajouté ou actualisé dans le projet.
Les 424 fichiers de référence préexistants restent identiques, y compris les
JavaScript validés, les modèles, les récits, les images et les bilans antérieurs.
Les contrôleurs sont conservés hors du dépôt dans le dossier local du lot.

Les six originaux et les rôles sont conformes lors du contrôle final. Aucun mot
de passe n'est modifié et aucune route de gestion des comptes n'est appelée.
Les deux serveurs continuent d'accepter les connexions sur 5064 et 5066.
Aucune donnée n'est supprimée, hormis le retrait explicitement autorisé du seul
J’aime créé pour ce test ; aucun nettoyage des contributions n'est effectué.

Aucun commit, push ou merge. Index vide et HEAD inchangé. Ce bilan reste local
et non suivi par Git. Aucun correctif applicatif n'est entrepris. Les opérations
de validation sont arrêtées après rédaction du bilan ; les fenêtres temporaires
peuvent rester ouvertes pour consultation, sans nouvelle automatisation d'écriture.
