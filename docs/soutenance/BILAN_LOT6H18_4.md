# Bilan local — lot 6H.18.4

> Archive pédagogique datée : les résultats et descriptions ci-dessous concernent le lot indiqué. Les anciens repères de ligne ne décrivent pas la version candidate. Pour préparer la soutenance actuelle, consulter les quatre fiches et le référentiel reliés au sommaire.

> Copie publique de référence : les chemins personnels et liens de travail internes sont retirés. Les preuves et commandes historiques gardent leur date et leur périmètre ; utiliser le README actuel pour le lancement.

Date : 4 novembre 2026, Europe/Paris.
Projet : `[chemin local privé retiré]`.

## Verdict

**Protection CSRF conforme sur les neuf variantes de routes/méthodes testées.**
Les 27 requêtes authentifiées sans jeton valide renvoient HTTP 403, sans exécuter
de modification SQL et sans changer les données ou les octets du fichier SQLite.
Les neuf requêtes avec le jeton valide réussissent avec les effets SQL attendus.
Aucune protection défaillante identifiée ; aucun correctif backend proposé ou appliqué.

Ce résultat lève la réserve du lot 6H.18.3 concernant le comportement du backend
testé. Il ne reconstitue pas l'en-tête envoyé lors de l'ancien essai Edge et ne
prétend pas identifier la cause de l'interruption de cet ancien contrôleur.

## Environnement exclusivement isolé

- Nouvelle SQLite fichier, créée dans un répertoire temporaire neuf sous
  `[chemin local privé retiré]` puis supprimée après les contrôles.
- Deux comptes temporaires classiques, actifs, avec mots de passe générés uniquement
  en mémoire et hachés par `User.set_password()`. Deux authentifications réelles
  réussies via `/api/v1/login` et clients à cookies indépendants ; aucune session forgée.
- Deux supports narratifs synthétiques très courts servent uniquement de cibles de
  test. Les six histoires originales ne sont ni importées dans cette base ni modifiées.
- Véritable application Flask de `backend/index.py`, véritables vues, modèles et
  transactions SQLAlchemy. Requêtes WSGI locales : aucune réponse HTTP simulée.
- Le filtre réel `protect_session_requests_from_csrf` est enregistré et exécuté.
  Aucun remplacement de cette fonction ni désactivation de protection.
- Dotenv neutralisé avant import ; paramètres Aiven neutralisés dans le seul processus
  de test ; configuration SQLAlchemy vérifiée avant création du moteur.
- Garde-fous sur le moteur et les connexions SQLite : seul le nouveau fichier temporaire
  est autorisé. Les ouvertures d'autres SQLite ainsi que ATTACH/DETACH sont bloquées.
- Connexions réseau, écoute réseau et MySQL bloquées. **Zéro tentative réseau,
  zéro tentative MySQL, zéro ouverture d'une autre SQLite, zéro ATTACH/DETACH.**
- Aucune ouverture de `instance/demo-persistante/portfolio.sqlite3`, aucun appel aux
  serveurs 5064/5066, aucun lancement, redémarrage ou arrêt de serveur ou de navigateur.

Les mots de passe, cookies, jetons, clés et réponses d'authentification ne sont pas
enregistrés dans les journaux, les fichiers de résultats ou ce rapport. Les paramètres
SQL et les lignes complètes restent en mémoire pour les comparaisons ; seules leurs
égalités, les comptages et les résultats utiles sont exportés.

## Méthode et preuve d'absence d'écriture

Pour chacune des neuf variantes :

1. Confirmer par `/me` que le client est réellement authentifié comme le compte de test.
2. Relever directement toutes les lignes des dix tables SQLite, triées par identifiant,
   à travers une connexion séparée en lecture seule ; prendre l'empreinte du fichier
   et les compteurs d'exécution DML/DDL, sans exporter leurs données privées.
3. Envoyer successivement la requête avec jeton absent, jeton aléatoire invalide,
   jeton de l'autre session authentifiée, puis jeton valide de la session courante.
4. Observer à l'entrée WSGI seulement la présence du cookie, la présence de l'en-tête
   CSRF et sa correspondance booléenne avec le jeton attendu. Aucune valeur n'est stockée.
   Le cas « absent » est réellement absent ; les cas invalides sont réellement différents.
5. Vérifier le code HTTP, le corps d'erreur CSRF attendu et la nouvelle lecture SQL.
   Après chaque refus : toutes les lignes sont identiques, fichier identique,
   **zéro INSERT/UPDATE/DELETE/REPLACE et zéro CREATE/ALTER/DROP exécuté**.
6. Confirmer que la session est encore authentifiée après la requête.
7. Avec le bon jeton, exiger le statut prévu au contrat Swagger, une seule modification
   SQL et la différence exacte attendue dans la seule table concernée.

La comparaison porte sur les valeurs de toutes les colonnes, pas seulement sur les
comptages : une mise à jour silencieuse ou une suppression compensée serait détectée.
Les DELETE sont testés alors que le like du compte existe déjà, puis doivent retourner
`changed: true` et retirer réellement ce seul like ; un DELETE sans effet ne vaut pas succès.

## Routes et codes HTTP observés

Les identifiants 1 et 2 ci-dessous appartiennent uniquement aux données temporaires.
Les refus 403 et les succès 200/201 ont été confrontés au contrat Swagger existant.

| Route et méthode | Jeton absent | Jeton invalide | Jeton autre session | Jeton valide | SQL |
| --- | ---: | ---: | ---: | ---: | --- |
| `POST /api/v1/votes/1` | 403 | 403 | 403 | 201 | Conforme |
| `DELETE /api/v1/votes/1` | 403 | 403 | 403 | 200 | Conforme |
| `POST /api/v1/comments/1/like` | 403 | 403 | 403 | 200 | Conforme |
| `DELETE /api/v1/comments/1/like` | 403 | 403 | 403 | 200 | Conforme |
| `POST /api/v1/stories/1/comments` | 403 | 403 | 403 | 201 | Conforme |
| `POST /api/v1/comments/1/report` | 403 | 403 | 403 | 201 | Conforme |
| `POST /api/v1/reports` | 403 | 403 | 403 | 201 | Conforme |
| `POST /api/v1/stories/2/theories` | 403 | 403 | 403 | 201 | Conforme |
| `POST /api/v1/theories/1/like` | 403 | 403 | 403 | 200 | Conforme |

Le périmètre inclut les likes de dossiers et commentaires, le like incrémental de
théorie, et les deux entrées de signalement applicables. Aucune route de retrait
de like de théorie n'est inventée : cette fonction n'existe pas dans le contrat testé.

Pour les 27 refus, le corps renvoie le message CSRF existant, ce qui distingue le
refus de protection d'une erreur de rôle, d'une ressource absente ou d'un corps invalide.

## Effets SQL des neuf requêtes valides

| Opération | Différence SQL contrôlée |
| --- | --- |
| POST like dossier | Une ligne `votes` ajoutée pour le compte courant et le dossier ciblé |
| DELETE like dossier | Cette ligne `votes` retirée, aucune autre table modifiée |
| POST like commentaire | Une ligne `comment_likes` ajoutée, compteur historique du commentaire inchangé |
| DELETE like commentaire | Cette ligne `comment_likes` retirée |
| POST commentaire | Une ligne `comments` ajoutée |
| POST signalement ciblé | Une ligne `reports` ajoutée pour le commentaire ciblé |
| POST signalement générique | Une autre ligne `reports` ajoutée pour la cible validée |
| POST théorie | Une ligne `theories` ajoutée dans le dossier ciblé |
| POST like théorie | Une seule théorie mise à jour, `likes` passe de 0 à 1, nombre de théories inchangé |

À chaque succès : une seule instruction DML, aucune instruction DDL, aucune autre
table modifiée. Les articles supports et les deux comptes restent identiques.

| Table temporaire | Au départ | Après les requêtes valides |
| --- | ---: | ---: |
| users | 2 | 2 |
| categories | 2 | 2 |
| stories | 2 | 2 |
| comments | 1 | 2 |
| theories | 1 | 2 |
| votes | 0 | 0 |
| comment_likes | 0 | 0 |
| reports | 0 | 2 |
| proposals | 0 | 0 |
| cold_case_updates | 0 | 0 |

L'intégrité SQLite et les clés étrangères sont conformes à la fin du scénario.
La base temporaire et ses comptes ont ensuite été supprimés, sans toucher à une
base préexistante. Une première tentative avait déjà réussi les 36 contrôles mais
avait conservé une connexion de lecture ouverte pendant le nettoyage Windows.
Le harnais, conservé hors du projet, a été corrigé pour fermer explicitement ces
connexions ; la campagne complète et le nettoyage ont ensuite réussi.

## Conservation et limites du verdict

**425 fichiers préexistants du projet sont inchangés**, dont tout le backend,
le frontend, les modèles, les images, le catalogue original et les anciens bilans.
Seul `docs/soutenance/BILAN_LOT6H18_4.md` est ajouté au projet et reste local, non indexé.
Aucun compte permanent, mot de passe permanent ou donnée persistante n'est touché.

Le contrôle est ciblé sur les routes et cas listés. Il valide le backend Flask avec
une configuration SQLite isolée ; il ne constitue ni une nouvelle validation Edge,
ni un audit de sécurité exhaustif, ni une vérification de déploiement public.
Les 567 tests frontend précédents ne sont pas relancés.

Résultats détaillés expurgés et harnais reproductible conservés exclusivement sous
`[chemin local privé retiré]`.

Gabarit de la commande historique ; le script interne n’est pas distribué :

```powershell
# Gabarit historique ; fournir les deux chemins autorisés avant usage.
$pythonValidation = '<INTERPRETE_PYTHON_AUTORISE>'
$scriptValidation = '<SCRIPT_INTERNE_NON_DISTRIBUE>'
& $pythonValidation -I -B $scriptValidation
```

Index Git vide et HEAD inchangé. Aucun commit, push ou merge. Aucun correctif
applicatif nécessaire pour les cas contrôlés. Lot arrêté après ces vérifications.
