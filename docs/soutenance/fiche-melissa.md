# Fiche Mélissa — Frontend

[Retour au sommaire de soutenance](README.md)

Questions-réponses historiques récupérées de la réponse Codex de l’étape 15.1 du **25 octobre 2026**, fondée sur le commit `dec5c7ef4c753970bd94014b37b59b035e1877f1`. Audit de référence : étape 15.8.1 ; préparation documentaire : étape 15.8.2, au commit `857190654457b15d7324adde8c920d9fdd3db0c8`.

Les formulations des questions et des réponses courtes originales sont conservées. Les explications, exemples, identifiants de repérage et références facilitent la révision. **VALIDÉE** signifie conforme aux sources ; ce statut ne constitue pas une validation en production.

Empreinte SHA-256 du texte historique complet : `218cf13b814a1f20a4258f1f6b24ab600b296bc62baab1c23610a36905ace4cd`.

**Portée des preuves :** les résultats de tests et de rendu Mermaid sont historiques. Aucun test fonctionnel, rendu de diagramme, serveur, migration ou accès Aiven n’est exécuté pendant cette préparation. Les droits des illustrations restent à confirmer.

## Sommaire

- [Repères pour comprendre](#repères-pour-comprendre)
- [Questions du jury](#questions-du-jury)

Accès direct aux 18 questions :

[MEL-01](#mel-01) · [MEL-02](#mel-02) · [MEL-03](#mel-03) · [MEL-04](#mel-04) · [MEL-05](#mel-05) · [MEL-06](#mel-06)

[MEL-07](#mel-07) · [MEL-08](#mel-08) · [MEL-09](#mel-09) · [MEL-10](#mel-10) · [MEL-11](#mel-11) · [MEL-12](#mel-12)

[MEL-13](#mel-13) · [MEL-14](#mel-14) · [MEL-15](#mel-15) · [MEL-16](#mel-16) · [MEL-17](#mel-17) · [MEL-18](#mel-18)

## Repères pour comprendre

**Phrase à retenir à l’oral**

> « HTML structure les pages, CSS organise leur présentation, et JavaScript les relie à l’API. Le frontend affiche les données et guide l’utilisateur. Les permissions restent vérifiées par Flask. »

Sources : [README frontend](../../frontend/README.md), [api.js](../../frontend/api.js), [app.js](../../frontend/app.js), [styles.css](../../frontend/styles.css).

### 1. HTML, CSS et JavaScript

**HTML** décrit les éléments de la page : titres, liens, formulaires et zones de résultat.

Exemple : `theories.html` contient le formulaire `theory-form` et une section distincte pour les théories publiées. Cette structure permet à JavaScript de retrouver chaque zone.

**CSS** définit la présentation : couleurs, espacements, grilles et adaptation à la largeur disponible.

Exemple : `.cards` affiche trois colonnes sur les grands écrans, puis deux et une colonne selon les media queries.

**JavaScript** réagit aux actions et met à jour la page.

Exemple : le formulaire de théorie intercepte `submit`, vérifie les champs et appelle l’API.

Le frontend n’utilise pas de compilation. Node.js intervient dans les tests JavaScript.

### 2. Les dix pages

| Page | Fonction réelle |
|---|---|
| `index.html` | Accueil, jusqu’à trois dossiers récents, affichage de session et déconnexion |
| `histoires.html` | Histoires résolues et recherche locale dans les titres et résumés |
| `coldcases.html` | Dossiers classés comme non résolus |
| `dossier.html` | Lecture d’un dossier avec `?slug=…` |
| `connexion.html` | Connexion membre |
| `admin-connexion.html` | Connexion avec vérification du rôle administrateur |
| `inscription.html` | Création d’un compte ; connexion ensuite séparée |
| `proposer-histoire.html` | Proposition d’une nouvelle histoire |
| `theories.html` | Création de théorie et consultation publique |
| `admin-dashboard.html` | Consultation des compteurs, propositions et signalements |

Les catégories sont associées directement aux identifiants `1` et `2` dans `app.js`. C’est une dépendance actuelle à la préparation des données.

### 3. Responsabilités des scripts

| Script | Responsabilité |
|---|---|
| `api.js` | Requêtes HTTP, JSON, cookies, CSRF, délai, erreurs et validation de réponses |
| `app.js` | Cartes, recherche, dossier, images, inscription, connexion, session et contributions |
| `theories-list.js` | Lecture publique des théories, sélection et actualisation |
| `admin-dashboard.js` | Vérification du rôle puis chargement des données administratives |

Les pages chargent `api.js` avant `app.js`, puis leur script spécialisé.

`donnees.js` contient un ancien jeu de données. Les scripts actifs ne consomment plus ce tableau. Il ne remplace pas l’API lorsque celle-ci échoue.

### 4. DOM et événements

Le **DOM** est la représentation de la page manipulable par JavaScript.

Exemples réels :

```javascript
document.getElementById('theory-form')
document.createElement('article')
title.textContent = story.title;
```

Ces opérations permettent de retrouver un formulaire, de créer une carte et d’afficher un titre.

Un **événement** signale une action ou un changement :

- `submit` : envoi d’un formulaire ;
- `input` : modification de la recherche ;
- `change` : changement du dossier sélectionné ;
- `click` : actualisation ou déconnexion ;
- `error` : échec de chargement d’une image.

`event.preventDefault()` empêche l’envoi HTML classique. Le script peut alors gérer la requête et son résultat.

Les contenus externes concernés sont insérés avec `textContent`. Une chaîne reçue est ainsi affichée comme du texte.

### 5. `fetch`, promesses et JSON

**`fetch`** envoie une requête HTTP.

Exemple réel dans `api.js` :

```javascript
fetch(API_BASE + path, {
  ...requestOptions,
  headers,
  credentials: 'include',
  signal: controller.signal
})
```

Une **promesse** représente un résultat disponible plus tard. `await` permet d’attendre ce résultat dans une fonction `async`.

Dans le tableau administrateur, `Promise.all()` attend plusieurs lectures après la vérification du compte.

**JSON** est le format d’échange entre JavaScript et Flask :

```javascript
JSON.stringify({ title, content })
```

Flask lit le corps JSON et renvoie une réponse avec `jsonify()`.

`api.js` vérifie `response.ok`. Une réponse HTTP `400` ou `500` doit être traitée explicitement : elle ne provoque pas automatiquement un rejet de `fetch`.

### 6. Session, cookies et CSRF

Une **session** permet au serveur de reconnaître le compte connecté entre plusieurs requêtes.

Le navigateur reçoit le cookie de session Flask. Les requêtes utilisent `credentials: 'include'`.

Le cookie est configuré avec :

- `HttpOnly` ;
- `SameSite=Lax` ;
- `Secure` configurable selon l’environnement.

`HttpOnly` empêche JavaScript de lire directement ce cookie.

Le **CSRF** protège les écritures utilisant la session. Le navigateur obtient un jeton à la connexion ou via `/api/v1/me`. `api.js` le conserve en mémoire et l’ajoute dans `X-CSRF-Token`.

Aucun stockage d’authentification dans `localStorage` ou `sessionStorage` n’est utilisé.

Pour les propositions et théories, le formulaire appelle `/me` avant l’écriture. Il récupère ainsi une vérification de session et un CSRF à jour.

### 7. Erreurs et conservation des formulaires

`api.js` distingue notamment :

- refus HTTP ;
- réponse JSON illisible ;
- statut inattendu ;
- délai dépassé ;
- erreur réseau.

Le délai par défaut est de **10 secondes**. Les écritures ne sont pas répétées automatiquement.

Les formulaires de proposition et de théorie :

1. vérifient les champs ;
2. bloquent les doubles soumissions pendant l’envoi ;
3. vérifient la session ;
4. envoient le JSON ;
5. se réinitialisent après un succès confirmé.

La création attend **HTTP 201 avec un JSON lisible**.

En cas d’échec, la saisie reste présente dans la page. Il ne s’agit pas d’une sauvegarde durable : une navigation ou un rechargement peut la perdre.

**Exception à préciser :** les champs de mot de passe sont effacés après les tentatives de connexion ou d’inscription.

### 8. Consultation publique des théories

Le lecteur de théories fonctionne sans connexion.

Son sélecteur est indépendant de celui du formulaire de création. Les deux utilisent les identifiants numériques renvoyés par l’API.

`theories-list.js` gère :

- chargement ;
- liste vide ;
- erreur ;
- dossier supprimé ;
- actualisation manuelle ;
- réponses arrivées trop tard.

Un compteur de version et l’annulation des requêtes empêchent une ancienne réponse de remplacer la sélection actuelle.

Après une création, le lecteur ne se recharge pas automatiquement. L’utilisateur doit sélectionner le dossier ou cliquer sur **Actualiser**.

### 9. Images et responsive

La chaîne de remplacement est :

1. `image_url` provenant de l’API ;
2. illustration locale associée au slug ;
3. `images/default-story.svg` ;
4. texte « Image indisponible ».

Les URL d’image acceptées se résolvent en HTTP ou HTTPS. Les schémas comme `javascript:`, `data:` et `file:` sont refusés.

Les sources identiques sont dédupliquées. Le repli s’arrête après le dernier échec.

Le dépôt contient quatre illustrations WebP et un SVG de remplacement. Les cartes utilisent le chargement `lazy`, les fiches utilisent `eager`.

Le **responsive** adapte la présentation à l’espace disponible :

- trois colonnes par défaut ;
- deux colonnes jusqu’à `780px` ;
- une colonne jusqu’à `560px` ;
- navigation et groupes de boutons avec retour à la ligne ;
- images au ratio `16:9`, avec `object-fit: cover`.

Ces règles sont **vérifiées dans les sources**. Leur rendu sur de vrais appareils n’a pas été contrôlé ici.

### 10. Limites actuelles

- Aucun écran pour commenter, voter, liker ou signaler.
- Aucun bouton de bannissement.
- Administration limitée à la consultation.
- Aucune acceptation ou publication des propositions.
- Aucun téléchargement d’image.
- Aucune récupération de mot de passe.
- Listes sans pagination.
- Actualisation manuelle des théories et du tableau administrateur.
- Catégories dépendantes des identifiants `1` et `2`.
- Ancien libellé « maquette » encore présent sur la connexion administrateur.
- Tests frontend avec DOM et API simulés ; navigateur réel non vérifié ici.

## Questions du jury

### MEL-01

**Question du jury**

Quel est le rôle de HTML ?

**Réponse courte à dire**

Il structure les pages. Dans `theories.html`, il définit le formulaire et la zone de lecture des théories.

**Explication simple**

La page déclare les zones et les champs que les scripts vont utiliser.

**Exemple concret**

Le formulaire et le lecteur public sont deux zones distinctes.

**Référence technique**

[frontend/theories.html](../../frontend/theories.html#L31)

**Statut de validation**

**VALIDÉE — conforme aux sources.**

### MEL-02

**Question du jury**

Quel est le rôle de CSS ?

**Réponse courte à dire**

Il organise l’apparence et les adaptations d’écran. Les media queries réduisent le nombre de colonnes des cartes.

**Explication simple**

La présentation change suivant la largeur disponible.

**Exemple concret**

La grille passe de trois à deux, puis une colonne.

**Référence technique**

[frontend/styles.css](../../frontend/styles.css#L318)

**Statut de validation**

**VALIDÉE — conforme aux sources.**

### MEL-03

**Question du jury**

Quel est le rôle de JavaScript ?

**Réponse courte à dire**

Il gère les interactions et les appels API. Par exemple, il soumet une théorie sans recharger toute la page.

**Explication simple**

Les événements du navigateur déclenchent des actions et des requêtes.

**Exemple concret**

submit lance une création de théorie.

**Référence technique**

[frontend/app.js](../../frontend/app.js#L233)

**Statut de validation**

**VALIDÉE — conforme aux sources.**

### MEL-04

**Question du jury**

Pourquoi centraliser les appels dans `api.js` ?

**Réponse courte à dire**

Cela regroupe les règles communes : cookies, CSRF, JSON, délai et erreurs. Chaque page utilise les mêmes fonctions.

**Explication simple**

Une seule fonction applique les mêmes règles de communication aux différents écrans.

**Exemple concret**

apiRequest() gère le délai et les erreurs HTTP.

**Référence technique**

[frontend/api.js](../../frontend/api.js#L6)

**Statut de validation**

**VALIDÉE — conforme aux sources.**

### MEL-05

**Question du jury**

Que fait `app.js` ?

**Réponse courte à dire**

Il gère les parcours communs : affichage des dossiers, recherche, images, session et formulaires.

**Explication simple**

Ce script relie les éléments communs de l’interface aux fonctions API.

**Exemple concret**

loadStories() remplit les cartes depuis getStories().

**Référence technique**

[frontend/app.js](../../frontend/app.js#L108)

**Statut de validation**

**VALIDÉE — conforme aux sources.**

### MEL-06

**Question du jury**

Pourquoi un script séparé pour les théories publiées ?

**Réponse courte à dire**

Le lecteur possède sa propre sélection et ses propres états. Il peut fonctionner publiquement, indépendamment du formulaire connecté.

**Explication simple**

Lire les théories ne nécessite pas de remplir le formulaire de contribution.

**Exemple concret**

Le lecteur possède son propre sélecteur et un bouton Actualiser.

**Référence technique**

[frontend/theories-list.js](../../frontend/theories-list.js#L75)

**Statut de validation**

**VALIDÉE — conforme aux sources.**

### MEL-07

**Question du jury**

Qu’est-ce que le DOM ?

**Réponse courte à dire**

C’est la représentation de la page manipulée par JavaScript. `createElement()` permet par exemple de construire une carte de dossier.

**Explication simple**

JavaScript peut créer et modifier les éléments visibles de la page.

**Exemple concret**

makeCard() crée un article et lui ajoute un titre.

**Référence technique**

[frontend/app.js](../../frontend/app.js#L73)

**Statut de validation**

**VALIDÉE — conforme aux sources.**

### MEL-08

**Question du jury**

Pourquoi utiliser `preventDefault()` ?

**Réponse courte à dire**

Il empêche l’envoi HTML classique du formulaire. Le script peut valider les données et traiter la réponse de Flask.

**Explication simple**

Le navigateur ne doit pas envoyer le formulaire par son mécanisme classique en plus du script.

**Exemple concret**

La validation précède createTheory().

**Référence technique**

[frontend/app.js](../../frontend/app.js#L233)

**Statut de validation**

**VALIDÉE — conforme aux sources.**

### MEL-09

**Question du jury**

Qu’est-ce qu’une promesse ?

**Réponse courte à dire**

Elle représente un résultat futur. Le code utilise `await` pour attendre la réponse d’un appel API.

**Explication simple**

Une requête prend du temps : await attend son résultat sans produire immédiatement une réponse.

**Exemple concret**

Le script attend fetch(), puis la lecture du JSON.

**Référence technique**

[frontend/api.js](../../frontend/api.js#L31)

**Statut de validation**

**VALIDÉE — conforme aux sources.**

### MEL-10

**Question du jury**

Pourquoi vérifier `response.ok` ?

**Réponse courte à dire**

Une réponse HTTP en erreur peut quand même être reçue par `fetch`. Cette vérification évite d’afficher un succès après un refus serveur.

**Explication simple**

Recevoir une réponse ne signifie pas que l’opération a réussi.

**Exemple concret**

Une réponse 403 devient une erreur affichée.

**Référence technique**

[frontend/api.js](../../frontend/api.js#L64)

**Statut de validation**

**VALIDÉE — conforme aux sources.**

### MEL-11

**Question du jury**

Comment le cookie accompagne-t-il les requêtes ?

**Réponse courte à dire**

`api.js` utilise `credentials: 'include'`. Le navigateur gère l’envoi du cookie ; le script ne lit pas sa valeur.

**Explication simple**

Le navigateur transmet les cookies selon ses règles ; le script n’a pas à lire le cookie HttpOnly.

**Exemple concret**

credentials: 'include' accompagne les requêtes.

**Référence technique**

[frontend/api.js](../../frontend/api.js#L36)

**Statut de validation**

**VALIDÉE — conforme aux sources.**

### MEL-12

**Question du jury**

À quoi sert le CSRF ?

**Réponse courte à dire**

Il protège les écritures utilisant la session. Le jeton obtenu auprès du serveur est transmis dans `X-CSRF-Token`.

**Explication simple**

Le jeton permet au serveur de vérifier une écriture utilisant la session ; la connexion est exemptée.

**Exemple concret**

Le client envoie X-CSRF-Token.

**Référence technique**

[backend/index.py](../../backend/index.py#L152)

**Statut de validation**

**VALIDÉE — conforme aux sources.**

### MEL-13

**Question du jury**

La validation frontend suffit-elle ?

**Réponse courte à dire**

Non. Elle aide l’utilisateur, mais Flask doit refaire les contrôles car le client peut être modifié.

**Explication simple**

Une personne peut envoyer une requête directement, en dehors du formulaire officiel.

**Exemple concret**

Le titre et le contenu sont également contrôlés par Flask.

**Référence technique**

[backend/api/v1/views/write_support.py](../../backend/api/v1/views/write_support.py#L27)

**Statut de validation**

**VALIDÉE — conforme aux sources.**

### MEL-14

**Question du jury**

Pourquoi conserver les champs après une erreur ?

**Réponse courte à dire**

Cela évite de perdre une contribution. Les formulaires de proposition et de théorie se réinitialisent seulement après le succès attendu.

**Explication simple**

Un échec ne doit pas obliger à retaper la contribution encore présente dans la page.

**Exemple concret**

reset() n’intervient qu’après la création réussie.

**Référence technique**

[frontend/app.js](../../frontend/app.js#L276)

**Statut de validation**

**VALIDÉE — conforme aux sources.**

### MEL-15

**Question du jury**

Cette conservation survit-elle à un rechargement ?

**Réponse courte à dire**

Aucune sauvegarde durable de brouillon n’est implémentée. La conservation concerne le formulaire encore ouvert.

**Explication simple**

Aucun brouillon n’est enregistré dans un stockage durable par ces formulaires.

**Exemple concret**

Recharger ou quitter la page peut faire perdre la saisie.

**Référence technique**

[frontend/app.js](../../frontend/app.js#L296)

**Statut de validation**

**VALIDÉE — conforme aux sources.**

### MEL-16

**Question du jury**

Comment éviter les doubles envois ?

**Réponse courte à dire**

Le code utilise un indicateur `sending` et désactive les contrôles pendant la requête. Cela bloque les doubles soumissions dans ce parcours.

**Explication simple**

Pendant la requête, un indicateur empêche un nouveau départ de la même soumission.

**Exemple concret**

sending est remis à false à la fin de l’envoi.

**Référence technique**

[frontend/app.js](../../frontend/app.js#L313)

**Statut de validation**

**VALIDÉE — conforme aux sources.**

### MEL-17

**Question du jury**

Que se passe-t-il si une image échoue ?

**Réponse courte à dire**

Le script essaie la source suivante. Après les derniers replis, il masque l’image cassée et affiche un message.

**Explication simple**

Chaque erreur déclenche le prochain repli, jusqu’à épuisement des sources.

**Exemple concret**

API, illustration locale, SVG, puis message texte.

**Référence technique**

[frontend/app.js](../../frontend/app.js#L37)

**Statut de validation**

**VALIDÉE — conforme aux sources.**

### MEL-18

**Question du jury**

La page administrateur est-elle privée ?

**Réponse courte à dire**

Le HTML est accessible, mais les données protégées exigent une autorisation serveur. Le contrôle JavaScript du rôle améliore l’interface sans remplacer Flask.

**Explication simple**

La protection porte sur les données et les routes ; cacher une page ne remplace pas l’autorisation.

**Exemple concret**

Flask exige admin_required pour les propositions et signalements.

**Référence technique**

[frontend/admin-dashboard.js](../../frontend/admin-dashboard.js#L143)

**Statut de validation**

**VALIDÉE — conforme aux sources.**

[Retour au sommaire de soutenance](README.md)
