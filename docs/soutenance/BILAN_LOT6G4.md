# Lot 6G.4 — préparation finale de la recette navigateur

> Archive pédagogique datée : les résultats et descriptions ci-dessous concernent le lot indiqué. Les anciens repères de ligne ne décrivent pas la version candidate. Pour préparer la soutenance actuelle, consulter les quatre fiches et le référentiel reliés au sommaire.

> Copie publique de référence : les chemins personnels et liens de travail internes sont retirés. Les preuves et commandes historiques gardent leur date et leur périmètre ; utiliser le README actuel pour le lancement.

[Audit 6G.3](BILAN_LOT6G3.md) · [Développement 6G.2](BILAN_LOT6G2.md) · [Recette historique 6F.2](BILAN_LOT6F2.md) · [Nouveau protocole manuel](RECETTE_MANUELLE_LOT6G4.md)

**1er novembre 2026. GO pour une recette manuelle locale sur le nouveau kit isolé, sous autorisation distincte de lancement.** Les deux blocages techniques de préparation sont levés : kit actuel figé et inspecté, chargements historiques inutilisés retirés. **815 tests réussis : 303 backend, 484 frontend, 28 lanceur/contrats**, soit la référence de 803 et 12 nouveaux tests. Deux parcours supplémentaires réussissent sans navigateur : 43 requêtes API du kit et 79 requêtes depuis les contrôleurs frontend réels avec DOM simulé.

**Aucun Edge ou serveur en écoute lancé. Aucun accès MySQL/Aiven, configuration privée, migration réelle ou changement Windows.** Les modèles, routes backend, migrations, dashboard et `donnees.js` sont conservés. Arrêt après 6G.4 ; le GO ne vaut pas autorisation d’exécuter le serveur ou Edge.

## 1. Audit initial et préservation

Les bilans 6G.3, 6G.2 et 6F.2, les consignes et scripts précédents ont été repris. Leurs empreintes confirment la continuité avec les sources examinées au lot précédent. Aucun `AGENTS.md` trouvé dans le dépôt ou les parents contrôlés. Sources concernées : cinq HTML de chargement, `api.js`, `app.js`, `likes.js`, `comments.js`, `theories-list.js`, styles et contrôleurs administratifs ; kit/manifeste 6F.2, harnais Python/Node et tests de contrats HTML.

Départ : branche `feature/frontend-api-integration`, HEAD `07a9f03ea0a3bdad4a07066fdd7bab1997cc158b`, **46 fichiers suivis modifiés, 70 non suivis, aucun indexé**. Un manifeste de 130 fichiers préexistants et une copie ciblée des cinq HTML/tests à modifier sont enregistrés hors dépôt. Le contenu de `donnees.js` n’est pas copié dans cette sauvegarde : seules son empreinte et ses métadonnées sont conservées.

La nouvelle autorisation permet sa lecture locale après contrôle de type/taille. Les autres anciennes exclusions — `histoires-originales.json`, CSV et quatre images WebP — ainsi que `.env`, secrets, cookies, certificats et bases privées restent non lus.

## 2. Cause exacte de l’obsolescence du kit 6F.2

L’ancien kit n’est pas défectueux parce qu’il refuse les sources actuelles : son refus protège son instantané inspecté. Trois écarts étaient à traiter :

1. **16 sources ne correspondaient plus à ses empreintes**, notamment modèles/sérialiseurs/purge, contrat API, contrôleurs et fiche après l’ajout des likes.
2. **`likes.js` manquait dans son manifeste et dans `PUBLIC`**. Mettre seulement les anciennes empreintes à jour aurait encore empêché de lire/servir le module.
3. Cinq HTML chargeaient le script historique exclu. L’ancien parcours omettait ce chargement sur les pages de compte et ne validait donc pas tous leurs scripts.

`tools/recette_lot6f2.py`, son manifeste et ses anciens protocoles restent inchangés. Le nouveau kit porte un nom distinct et ne renouvelle aucune empreinte à l’exécution.

## 3. `donnees.js` : type, dépendances et retrait des balises

Contrôle préalable : fichier régulier `.js`, **1 701 octets**, sans lien symbolique. Analyse locale textuelle uniquement, sans évaluation JavaScript : une déclaration de tableau `histoiresOriginales`, six entrées de données littérales, pas d’interpolation de template. Aucun appel DOM/réseau/stockage ou instruction exécutable supplémentaire n’est nécessaire à cette déclaration. L’identifiant n’est référencé par aucun autre source JS/HTML/CSS frontend examiné.

Les valeurs littérales n’ont été ni affichées ni exportées. Les sondes locales n’ont trouvé ni motif d’e-mail ni clé apparente de secret ; cela ne constitue pas une certification d’absence de données personnelles. Aucune valeur historique n’est nécessaire pour établir l’absence de dépendance. Le reçu d’inspection contient seulement structure, identifiant, taille et empreinte.

Les trois pages de compte demandées sont **`inscription.html`, `connexion.html`, `admin-connexion.html`**. Le bilan 6G.3 avait également identifié deux autres pages. L’autorisation de retirer les balises inutiles est appliquée aux **cinq références réellement présentes** :

| Fichier | Correction |
|---|---|
| `frontend/inscription.html` | Retrait de la seule balise `script src="donnees.js"` |
| `frontend/connexion.html` | Même retrait |
| `frontend/admin-connexion.html` | Même retrait |
| `frontend/proposer-histoire.html` | Même retrait ; formulaire/API conservés |
| `frontend/theories.html` | Même retrait ; `api.js`, `app.js`, `theories-list.js` conservent leur ordre |

Les comptes dépendent de `api.js`/`app.js`, les propositions du POST réel, les sélecteurs de théories de `getStories`, leur lecture de l’API des théories. La fiche utilise déjà l’API, `likes.js` et `comments.js` sans charger l’ancien tableau. Le fichier historique est donc inutile aux parcours actifs ; le garder chargé entretiendrait une source de démonstration ambiguë sans fonction actuelle. Aucun conflit de données n’a été reproduit : les contrôleurs actifs ne consomment pas ce tableau.

**`donnees.js` reste intact, non exécuté et non servi par le kit.** Son SHA-256 reste `3896cf4b9b96f6dcc61441709bfd2ec96116340d2519c894a9e1b6e21c35a177`. La comparaison avec les copies initiales confirme que les cinq HTML ont uniquement perdu cette balise, avec fins de ligne et fin de fichier préservées. Un contrôle de préservation a détecté l’ajout d’une fin de ligne finale sur deux fichiers par l’outil d’édition ; elle a été rétablie avant le passage final des suites.

## 4. Nouveau kit et isolation

Fichiers créés : [recette_lot6g4.py](../../tools/recette_lot6g4.py), [manifeste](../../tools/recette_lot6g4_sources.json), [tests du kit](../../tests/test_recette_lot6g4.py), [protocole manuel](RECETTE_MANUELLE_LOT6G4.md) et ce bilan.

Le manifeste épingle **40 sources** par SHA-256 normalisé CRLF/LF, dont le kit lui-même et les vingt ressources publiques prévues. Il refuse une source différente, une ressource absente ou une entrée privée/historique/migration. Il n’inclut pas les anciens jeux de données. Les vingt ressources sont effectivement servies en WSGI, et toutes les références JS/CSS des dix pages publiques sont couvertes. `likes.js` répond normalement, sans omission ni 403 de dépendance nécessaire.

| Protection | Vérification effectuée |
|---|---|
| Configuration | Environnement réduit avant import applicatif ; nouveau secret éphémère ; dotenv neutralisé ; six paramètres Aiven vides |
| Base | Driver SQLite et URL exactement `:memory:` imposés ; PyMySQL bloqué ; bases fichier et ATTACH/DETACH interdits |
| Intégrité | FK activées à chaque connexion ; `foreign_key_check` vide ; `database_list` sans fichier |
| Schéma | Dix tables neuves depuis les modèles dans la mémoire fictive ; aucune mise à niveau de base existante |
| Fichiers | Lectures limitées aux sources approuvées/runtime/preuves ; écritures interdites dans le dépôt et hors dossier de preuves |
| Réseau | Toutes les opérations réseau bloquées pendant l’inspection ; même les connexions sortantes locales restent interdites dans le mode futur d’écoute |
| Migrations | Code sous `migrations/`, commandes Alembic, `run_migrations` et opérations de migration bloqués par le kit |
| Processus | Sous-processus applicatifs bloqués ; aucun Edge/CDP ou script d’automatisation navigateur |
| Ressources | Liste publique explicite ; ancien script, données JSON historiques, README, secrets et chemins de documents refusés avant lecture |
| Écoute future | `--serve` sans marqueur refusé avant préparation ; adresse prévue uniquement `127.0.0.1:5064`, mono-thread, sans debug/reloader |

L’inspection a aussi été exécutée avec un environnement enfant contenant un groupe Aiven complet **strictement fictif** et une URL MySQL fictive : le kit les neutralise et confirme SQLite mémoire. Aucun hôte n’est résolu, aucun certificat lu et aucune connexion MySQL tentée.

Sept sondes séparées vérifient les refus avant entrée/sortie : lecture privée, écriture dépôt, écriture hors preuves, base fichier, réseau, migration et sous-processus. Leurs compteurs positifs sont attendus. Les inspections et parcours applicatifs réussis ont tous leurs compteurs interdits à zéro. Ces gardes sont propres aux processus de test ; ils ne changent aucune protection Windows.

## 5. Configuration fictive et routes utilisées

Le lancement manuel préparera trois comptes actifs (`jury6g4_admin`, `jury6g4_alice`, `jury6g4_bob`), mots de passe générés pour ce seul processus, catégories 1/2 et deux dossiers synthétiques d’id 17/42, slugs `recette-6g4` et `recette-coldcase-6g4`. Leurs images pointent vers le SVG local autorisé. Aucun commentaire, vote, like ou signalement de remplissage au démarrage.

Les routes sont celles du dépôt sous **`/api/v1`** : `/users`, `/login`, `/me`, `/logout`, `/stories`, `/stories/slug/{slug}`, `/stories/{id}/comments`, `/comments/{id}/report`, `/votes/{id}` et `/comments/{id}/like` en GET/POST/DELETE, `/stats`, `/proposals`, `/admin/reports`, `/admin/stories/{id}`, `/admin/users/{id}/ban`, `/admin/stories/{id}/archive` et `/restore`. Les listes administratives existantes restent utilisées par les contrôleurs du dashboard. Aucune route ou modèle ajouté/modifié.

Les sept nombres initiaux observés sont **2 dossiers actifs, 1 résolu, 1 Cold Case, 3 utilisateurs, 0 commentaire, 0 signalement, 0 proposition pending**. Ils sont calculés depuis les lignes de cette mémoire. Ce ne sont pas des valeurs injectées dans le dashboard.

## 6. Tests et intégration

Le harnais de régression est réinspecté : environnement minimal, dotenv neutralisé avant import, Aiven vide, SQLite mémoire uniquement, FK actives, réseau/privé/écritures dépôt/bases fichier/sous-processus bloqués. Son manifeste est préparé explicitement après revue, avec **74 sources**. Les sept tests de migration historiques restent exclus. Les six tests de la seule candidate likes, déjà isolés et autorisés lors des lots précédents, sont réexécutés uniquement dans des mémoires synthétiques ; ils ne sont pas exécutés par le nouveau kit de recette.

| Vérification finale | Résultat | Échecs / erreurs / ignorés |
|---|---:|---|
| Backend de référence | **303 PASS** | 0 / 0 / 0 |
| Frontend de référence | **484 PASS** | 0 / 0 / 0 ; aucun annulé |
| Lanceur/HTML existants et nouveaux contrats | **28 PASS** | 0 / 0 / 0 |
| **Total actuel** | **815 PASS** | 803 de référence + 12 nouveaux, sans cumul entre passages |
| Kit : contrôle des ressources et isolation, sans écoute | **READY** | Tous les compteurs interdits à zéro |
| Kit : parcours API WSGI | **43 requêtes, 7 groupes réussis** | Hors total des méthodes unitaires |
| HTML/contrôleurs réels → WSGI du nouveau wrapper → SQL → DOM simulé | **79 requêtes, 14 groupes réussis** | Aucun script omis, hors total unitaire |

Les douze nouveaux tests vérifient les formulaires/scripts des trois pages de compte et des deux autres pages, les ressources réellement servies, le manifeste complet, le refus d’une source likes altérée, le refus d’une entrée privée avant lecture, le driver/base autorisés, les lectures/écritures refusées, la politique d’écoute et les connexions sortantes, le blocage migrations/processus et les deux refus CLI avant préparation. Le test HTML historique de protection des données est adapté pour attendre `api.js`/`app.js` sans l’ancien script ; ses autres contrôles sont conservés.

Le parcours propre au kit réalise inscription/connexion, lecture des deux catégories, publication d’un commentaire, ajout/doublon/retrait/retrait répété/réajout sur chaque type de like, refus CSRF, signalement, vrai flush suivi d’erreur de commit et rollback, déconnexion, lecture administrative, archivage/restauration et bannissement. Un commentaire témoin distinct est créé avec un historique synthétique de 7 : GET/POST/DELETE de like sont refusés et **7 reste conservé**. Aucun reset de cet historique.

Les sept agrégats API sont comparés aux SELECT dans cette mémoire : **2, 1, 1, 4, 2, 1, 0** après ses actions et fixtures de contrôle. Le membre inscrit ajoute réellement une ligne User ; le second commentaire est le témoin historique du test. Cette mémoire est jetée, distincte du lancement manuel initial.

Le parcours DOM/API supplémentaire exerce les vrais gestionnaires d’inscription/connexion, commentaires, signalements, likes ajoutés/retirés/réajoutés, refus CSRF, réponses perdues après commit et accès/déconnexion administrateur. Il passe par le wrapper public du nouveau kit. Les sept valeurs du **DOM administratif** sont comparées à SQL : **2, 1, 1, 2, 2, 2, 0** dans sa propre fixture. Un Vote et un CommentLike restent présents, le compteur physique du commentaire reste zéro. Les trois anciennes omissions de scripts des pages de compte ont disparu : le reçu d’omissions est vide.

Les suites de bannissement, listes utilisateurs, commentaires/signalements, archives/restaurations, purge, propositions et théories passent. **Le dashboard n’est pas modifié.** Ses quatre fichiers et le CSS sont identiques par empreinte ; les likes ne créent aucun huitième indicateur.

Deux passages complets ont réussi, `attempt-1` puis **`attempt-2` sur les octets finaux** après préservation de fins de fichier. Ils ne sont pas additionnés. Les 43 requêtes et les 79 requêtes ne sont pas converties en nouvelles méthodes unitaires. Le refus `--serve` donne volontairement le code 2 attendu, sans démarrage. Aucun test applicatif échoué.

## 7. Contrôles statiques et limites

Contrôles statiques : analyse textuelle sans exécution du script historique ; recherche de dépendances ; comparaison des HTML avant/après ; fermeture du graphe de ressources publiques ; AST Python ; empreintes des sources, index/branche/HEAD ; liens documentaires ; contrôle Git des espaces avec prise en charge CRLF. Ces contrôles ne prouvent pas un rendu navigateur.

**NON RÉALISÉS :** écoute HTTP réelle du nouveau kit, Microsoft Edge, clavier/lecteur d’écran/mobile/rendu réels, cookies dans Edge, installation sur une autre machine, courses multi-connexions, durabilité après redémarrage, MySQL/Aiven, sept anciens tests de migration et chaîne Alembic complète. Les anciens neuf contrôles supplémentaires de 6G.3 ne sont pas additionnés aux 815. Le parcours DOM simule document/transport ; le parcours API du kit n’exécute aucun JS.

La SQLite de démonstration disparaît à l’arrêt. Son schéma neuf ne valide aucune migration. Le risque 6G.3 de table `comment_likes` créée sans index après échec DDL reste documenté : un rollback ne garantit pas le retour au schéma antérieur, une relance peut être refusée car la table existe. Aucun correctif ou nettoyage automatique de migration n’est introduit. Avant intervention future sur une base existante : inventaire autorisé, arrêt des anciens écrivains, sauvegarde contrôlée et procédure de reprise ; tout compteur non nul/invalide impose un arrêt et une décision humaine.

SQLite ne prouve ni les types/FK/moteurs de MySQL déployé, ni ses verrous, instantanés de lecture ou DDL avec commits implicites. Aucun GO de déploiement ou de migration réelle n’est déduit de ce lot. Les limites existantes d’incertitude après réponse perdue et de synchronisation entre onglets restent celles de 6G.3.

## 8. Livraison et preuves

**Neuf fichiers préexistants modifiés :** les cinq HTML listés en section 3 ; `tests/test_rgpd_information.py` (attente de scripts) ; `README.md`, `frontend/README.md`, `docs/soutenance/README.md` (références au nouveau kit et statut des anciennes données). **Cinq fichiers créés :** kit Python, manifeste JSON, douze tests, protocole manuel et présent bilan.

Les **121 autres fichiers du manifeste initial sont identiques**, dont tout le backend, les migrations, les contrôleurs JS/CSS, le dashboard, le kit 6F.2 et `donnees.js`. Branche, HEAD et index sont préservés. État final : **48 fichiers suivis modifiés, 75 non suivis, aucun indexé**, incluant tout le travail antérieur. Aucun commit/push, changement de branche ou suppression de fichiers.

Preuves temporaires :

```text
[chemin local privé retiré]
```

`baseline.json`, sauvegardes ciblées `before/`, `legacy-inspection.json`, `content-preservation.json`, manifeste de tests `preflight.json`, `attempt-1/` et `attempt-2/` avec commandes/journaux, gardes Python/Node, `kit-commands.json` et premier reçu conservé, sous-dossiers `portfolio-recette6g4-*` contenant reçus et `journey.json`, preuves d’intégration SQL/DOM/échanges/omissions et `final-validation.json`. Aucune valeur littérale de `donnees.js`, réponse brute avec cookie/CSRF ou mot de passe de recette dans ces preuves. Les scripts de préparation/coordination restent hors dépôt ; le kit et les protocoles sont les artefacts permanents.

## 9. Conditions de lancement Edge et verdict

Le [protocole manuel](RECETTE_MANUELLE_LOT6G4.md) donne inspection, comptes, huit étapes du parcours jury, vérifications complémentaires, erreurs et arrêt. Pour la suite : valider ce lot, puis autoriser explicitement l’écoute `127.0.0.1:5064` avec le kit courant et l’ouverture **manuelle** d’une fenêtre InPrivate Edge. Vérifier les empreintes avant lancement ; aucun profil personnel, CDP, pare-feu ou paramètre Windows à modifier. La commande proposée n’a pas été exécutée.

**Verdict final : GO pour une recette manuelle locale avec le kit 6G.4 et sa SQLite mémoire, sous autorisation distincte.** Le kit passe ses inspections et les parcours isolés ; serveur et navigateur réels restent à tester après cet accord. Aucun accès réel, déploiement ou migration n’est autorisé par ce verdict. Arrêt après 6G.4, en attente de validation.
