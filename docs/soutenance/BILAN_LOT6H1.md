# Lot 6H.1 — audit final et préparation de la livraison Git

> Archive pédagogique datée : les résultats et descriptions ci-dessous concernent le lot indiqué. Les anciens repères de ligne ne décrivent pas la version candidate. Pour préparer la soutenance actuelle, consulter les quatre fiches et le référentiel reliés au sommaire.

> Copie publique de référence : les chemins personnels et liens de travail internes sont retirés. Les preuves et commandes historiques gardent leur date et leur périmètre ; utiliser le README actuel pour le lancement.

**2 novembre 2026 — audit documentaire terminé. NO-GO pour considérer la livraison Git prête en l’état.** Le GO de démonstration locale 6G.5 reste acquis. Les freins de livraison sont la sauvegarde devenue ancienne, les ressources et données historiques à arbitrer avant diffusion et la reproductibilité complète encore non démontrée sur un ordinateur vierge.

L’utilisateur a validé 6G.5 et autorisé cet audit. Il a également confirmé l’emploi des **22 libellés de la matrice existante**. Aucun code applicatif, dashboard, test, modèle, migration, kit ou manifeste de recette n’est modifié. Aucun test applicatif, serveur, Edge, accès MySQL/Aiven, migration réelle, commit, push, indexation, fusion ou changement Windows n’est exécuté.

## 1. État Git exact et conservation

Projet : `[chemin local privé retiré]`.

| Élément au début de l’audit | Constat |
|---|---|
| Branche | `feature/frontend-api-integration` |
| HEAD | `07a9f03ea0a3bdad4a07066fdd7bab1997cc158b` |
| Fichiers suivis | 66 |
| Suivis modifiés | 51 |
| Non suivis | 79 |
| Indexés | 0 |
| Entrées non fusionnées | 0 |
| Fichiers suivis malgré une règle d’ignore | 0 |
| Chemins suivis ou non suivis inventoriés | 145 |

L’état initial, l’empreinte de l’index, les numstat des différences et les SHA-256 des fichiers examinables sont conservés hors dépôt. Les 138 fichiers texte/sources retenus sont contrôlés ; les sept anciennes exclusions n’ont pas été ouvertes. Les douze tests `.cjs` sont couverts par un reçu complémentaire à l’état initial, avant toute édition documentaire.

Les différences Git ont été examinées par chemins, volumes et cohérence des sources/contrats ; aucun patch brut contenant des valeurs privées n’est exporté. Aucun marqueur de conflit n’est relevé dans les sources examinées. L’absence de conflit Git ne suffit pas à attribuer les modifications non commitées à un étudiant : la répartition de présentation reste celle fournie par l’équipe.

La copie `revision_code/mahamadou/backend/models.py` est une archive distincte des modèles actifs. Elle est conservée, pas fusionnée ni substituée à `backend/models.py`. Le code courant importe les modèles actifs ; les preuves d’intégration antérieures concernent cet ensemble. Les originaux documentaires modifiés en 6H.1 sont également conservés avant édition.

État final documentaire attendu et contrôlé : **51 suivis modifiés, 87 non suivis, aucun indexé**, branche et HEAD identiques. Huit nouveaux documents/listes 6H.1 ; treize documents préexistants actualisés. L’index reste identique à son SHA-256 initial `cc33bbdc5993495735a8c63e85f22f321b05323716ff29b4af3d0fd8df6c5ec3`. Aucun fichier préexistant supprimé.

## 2. Fichiers nécessaires et inventaire de livraison

L’inventaire CSV (pièce interne non diffusée) donne **chaque chemin suivi/non suivi**, sa famille, son état initial, son rôle pour le kit, la décision de diffusion proposée et le lot de commit. Il ne s’agit pas d’une autorisation d’indexer ces fichiers.

| Famille avant 6H.1 | Chemins | Traitement |
|---|---:|---|
| Backend hors tests | 19 | Vues, application partagée, sérialisation, permissions, modèles et dépendances à conserver |
| Frontend hors ressources/tests | 22 | Dix pages et scripts/styles actifs ; README ; deux anciens jeux à distinguer |
| Tests et fixtures | 34 | Conserver sources et cas historiques, y compris candidats de migration avec exclusions d’exécution explicites |
| Migrations et configuration Alembic | 11 | Sept révisions, configuration et environnement ; candidats non appliqués |
| Documentation sous `docs/` | 45 | Supports, bilans et brouillons à distinguer ; pas de publication automatique des documents internes |
| Ressources | 6 | Quatre WebP, SVG et README ; nécessité technique et droits sont deux questions différentes |
| Kits | 4 | Kit 6G.4/manifeste courant et ancienne paire 6F.2 historique |
| Racine/configuration | 3 | README, `.gitignore`, lanceur |
| Copie historique de modèles | 1 | Préserver le travail de Mahamadou sans l’inclure dans le chemin d’exécution |
| Total | **145** | Avant les huit nouveaux livrables documentaires 6H.1 |

Les 40 sources du manifeste 6G.4 correspondent encore à leurs empreintes normalisées LF. Elles constituent un socle fermé pour la démonstration isolée, pas la liste exhaustive de tous les documents/tests à conserver. Le SVG est nécessaire à ce témoin minimal ; les quatre WebP servent des associations historiques de dossiers et ne sont pas chargés par ce kit.

La sélection de sauvegarde proposée comprend les sources examinées et les nouveaux livrables de l’audit, avec leurs SHA-256. Les fichiers privés, bases et anciennes exclusions restent hors sélection. Le manifeste ne se référence pas lui-même.

## 3. Fichiers à exclure, différer ou préserver comme archives

Les 2 731 chemins ignorés sont recensés par métadonnées : 2 664 sous `.venv/`, treize sous `backend/`, quarante-quatre sous `frontend/`, cinq sous `migrations/` et cinq chemins/groupes unitaires (`.DS_Store`, `.env`, `.vscode`, `certs`, `cookies.txt`). Aucun contenu de configuration privée, certificat, cookie ou base n’a été lu.

| Groupe | Décision |
|---|---|
| `.env`, secrets, certificats/clés, cookies, bases/dumps, logs privés | Exclure de toute livraison ; contrôler les chemins par liste fermée, pas par copie globale |
| `.venv`, caches, `.DS_Store`, `.vscode/settings.json` | Éléments locaux à ne pas livrer |
| `backend/ancien_app.py` et téléchargements `Reprendre projet portfolio_files/` | Obsolètes/locaux, ignorés ; signalés sans ouverture ni suppression |
| `frontend/donnees.js` et `frontend/histoires-originales.json` | Non utilisés par les pages actives ; littéraux non inspectés en 6H.1, absence de données personnelles non attestée ; à exclure de la sélection publique proposée |
| `COMPTES_DEMO.exemple.csv` et fichier privé de comptes | Contenu non ouvert ; ne pas supposer qu’un fichier de comptes est publiable |
| Quatre WebP et SVG | Conserver localement ; aucun justificatif de droits confirmé, diffusion à arbitrer |
| Politique HTML et décisions RGPD en brouillon | Conserver comme documents internes, ne pas publier la politique incomplète |
| Kit 6F.2 et copie historique des modèles | Préserver en archive, clairement hors parcours courant |
| Harnais et bases des recettes dans Temp | Preuves hors dépôt ; ne pas copier les bases, credentials ou outils propres à la machine dans Git |

Les quatre WebP et `donnees.js` sont déjà suivis. Les ignorer au moment d’un futur ajout ne les retirerait pas de l’arbre Git hérité. Tout retrait du suivi ou remplacement nécessitera une décision distincte, en conservant les originaux. Rien n’est supprimé ou désindexé ici.

Le lanceur normal peut servir un fichier JavaScript à la racine de `frontend/`, même s’il n’est plus chargé par une balise HTML. Le kit 6G.4 a une liste publique plus étroite qui exclut les anciens jeux. L’absence de référence HTML ne constitue donc pas une garantie générale de non-exposition par tous les modes de service.

## 4. Sauvegarde durable et proposition nouvelle

La sauvegarde durable **existe** :

`[chemin local privé retiré]`

Le premier rapport de revue 6E.1 décrivait une copie refusée/non réalisée. Le dossier de vérification durable, daté du 31 octobre, et le bilan 6E.3 attestent une opération ultérieure ; l’état actuel ne doit pas être déduit du seul premier échec. Les 115 fichiers de la copie sont relus et conformes aux empreintes du plan : 99 sources, huit documents et huit métadonnées, sans modification de cette sauvegarde.

Au début de 6H.1 : **50 sources sauvegardées encore identiques, 49 modifiées et 39 fichiers sûrs actuels absents de l’ancienne sélection de sources**. La sauvegarde ne couvre donc pas les développements récents de commentaires, likes, contexte des signalements et supports actuels. Elle reste utile comme instantané ancien ; elle n’est ni effacée ni écrasée.

Nouvelle proposition concrète : `portfolio-lot6h1-20261102-sources-01` dans le même parent privé, sous autorisation spécifique d’écriture hors projet. Voir le plan détaillé (pièce interne non diffusée) et la liste fermée avec empreintes (pièce interne non diffusée). **Aucune nouvelle copie durable n’est créée pendant cet audit.**

La récupération contrôlée historique de la copie précédente est une preuve du 31 octobre ; aucune nouvelle restauration ni vérification exhaustive des ACL n’est effectuée ici. Le futur contrôle devra restaurer la nouvelle sélection dans un dossier isolé et comparer ses empreintes. Cette archive sélective de sources ne sauvegardera ni une base réelle ni tout l’historique Git.

## 5. Matrice vérifiée des 22 remarques

Les libellés sont ceux de la matrice existante, conservés à l’identique après confirmation explicite de l’utilisateur. Aucun verbatim original supplémentaire du jury n’a été retrouvé ; les deux lignes images et les neuf lignes communes gardent leur classification antérieure.

| Demande (libellé conservé) | Statut | Correction actuelle | Fichiers concernés | Preuves disponibles | Travail restant / limite |
|---|---|---|---|---|---|
| H-01 — Houssem : expliquer les types de tests | TERMINÉ | Tests unitaires, API/SQLite, DOM simulé, WSGI et humain Edge distingués. | backend/tests/ ; frontend/tests/ ; tests/ | BILAN_CORRECTIFS_LOT6G5.md ; TESTS_ET_VALIDATION.md | Aucun taux de couverture inventé ; résultats 854 historiques, non relancés ici. |
| H-02 — Houssem : scénarios, outils, commandes et méthodes | TERMINÉ | Scénarios, outils et commandes archivés ; procédure de reprise sans Aiven préparée. | tools/recette_lot6g4.py ; backend/requirements.txt | BILAN_LOT6G4.md ; LANCEMENT_AUTRE_PC_LOT6H1.md | Une installation sur un autre PC reste non exécutée ; harnais complet 854 hors dépôt. |
| H-03 — Houssem : améliorer l'architecture | PARTIEL | Architecture et service des fichiers expliqués ; source du connecteur corrigée. | README.md ; fiche-commune.md ; run_local.py | BILAN_ETAPE51.md ; SUPPORT_JURY_LOT6H1.md | Rendre et inspecter le diagramme corrigé ; aucun navigateur lancé en 6H.1. |
| H-04 — Houssem : rôle du système de fichiers serveur | TERMINÉ | Stockage, URL, fichiers autorisés et API sont distingués ; cache local no-store expliqué. | run_local.py ; frontend/images/README.md | 30 tests contrats/lanceur historiques ; BILAN_CORRECTIFS_LOT6G5.md | Production distincte ; aucun hébergeur public annoncé. |
| H-05 — Houssem : présentation de la base | TERMINÉ | Présentation actualisée à dix tables, treize FK, contraintes et transactions. | backend/models.py ; migrations/ ; fiche-mahamadou.md | AST statique 6H.1 ; BILAN_LOT6G2.md ; SUPPORT_JURY_LOT6H1.md | Ne pas assimiler modèles déclarés et migrations appliquées à MySQL. |
| H-06 — Houssem : rendre le relationnel lisible | PARTIEL | Deux sources ER synchronisées avec les dix tables et treize relations actuelles. | README.md ; fiche-mahamadou.md | Comparaison statique 6H.1 ; ancien rendu neuf tables historique | Nouveau rendu visuel dix tables à contrôler sous autorisation distincte. |
| H-07 — Houssem : expliquer le DOM | TERMINÉ | DOM expliqué avec cartes, événements, textContent, session partagée et états des likes. | frontend/app.js ; comments.js ; likes.js ; admin-dashboard.js | 513 tests frontend historiques ; recette Edge 6G.5 ; SUPPORT_JURY_LOT6H1.md | Accessibilité complète et rendu mobile non revendiqués. |
| H-08 — Houssem : expliquer l'API REST | TERMINÉ | Ressources, JSON, méthodes, statuts et autorisations expliqués ; 36 opérations OpenAPI. | backend/api/v1/swagger.json ; frontend/api.js ; vues Flask | Contrat statique 27 chemins/36 opérations ; 311 tests backend historiques | POST Swagger complet et déploiement ne sont pas validés. |
| H-09 — Houssem : expliquer précisément le CSRF | TERMINÉ | CSRF de session, comparaison serveur, exceptions login/anonymes et rôle distinct de CORS expliqués. | backend/index.py ; frontend/api.js ; backend/tests/test_csrf.py | Tests CSRF inclus dans la campagne 311 backend ; lecture statique 6H.1 | Aucune publication de jeton/cookie ni promesse de révocation centralisée. |
| P-01 — Pauline : expliquer le flux de données | PARTIEL | Flux formulaire → HTTP → contrôles → SQL → DOM expliqué et note reformulée. | README.md ; fiche-commune.md ; frontend/api.js | BILAN_ETAPE51.md ; preuves WSGI et SQL historiques | Contrôler le débordement de la note dans un nouveau rendu visuel. |
| P-02 — Pauline : améliorer l'explication REST | TERMINÉ | Explication REST commune avec exemple de contribution et statuts concrets. | ORAL_JURY.md ; SUPPORT_JURY_LOT6H1.md ; swagger.json | Contrat actuel et tests API historiques | Réutiliser les preuves sans annoncer une recette Swagger non exécutée. |
| C-01 — Actualiser la documentation | TERMINÉ | Entrées de documentation actualisées ; anciens supports contextualisés et guides 6H.1 ajoutés. | README.md ; frontend/README.md ; docs/soutenance/ | Liens, repères et cohérence documentaire vérifiés statiquement en 6H.1 | Les réserves de rendu, de sauvegarde et de déploiement restent explicites. |
| C-02 — Fichier privé de comptes de démonstration | PARTIEL | Modèle et procédure de comptes fictifs ; accès temporaires lecteur/admin observés en recette. | COMPTES_DEMO.exemple.csv ; DEMONSTRATION.md ; tools/recette_lot6g4.py | Recette 6G.5 ; fichier privé non ouvert conformément au périmètre | Disponibilité et conservation d’une copie privée de comptes à confirmer sans communiquer de secrets. |
| C-03 — Bannissement dans l’interface administrateur | TERMINÉ | Liste, statuts, confirmation et bannissement ; administrateurs protégés. | frontend/admin-users.js ; admin_users_support.py ; index.py | Tests 6A puis régressions ; POST de bannissement 200 observé dans Edge initial | Reconnexion du compte banni non recettée dans Edge ; débannissement hors demande. |
| C-04 — Consultation admin des histoires et Cold Cases | TERMINÉ | Consultation des dossiers, recherche, filtres et accès aux fiches dans le tableau. | frontend/admin-stories.js ; admin_stories.py ; admin-dashboard.html | Tests 6B et régressions ; navigation humaine 6G.5 | Clavier/responsive exhaustifs non attestés. |
| C-05 — Suppression sécurisée de dossiers | TERMINÉ | Suppression transactionnelle des seuls dossiers archivés, titre et confirmation fraîche exigés. | story_deletion_support.py ; admin_stories.py ; frontend/admin-stories.js ; migration c6c200000001 | Tests backend SQLite/FK et DOM, rollback et conservation ; BILAN_LOT6C2_IMPLEMENTATION.md | Aucune suppression Edge ni migration réelle ; maintenance MySQL et concurrence réelles à valider avant déploiement. |
| C-06 — Statistiques commentaires et signalements | TERMINÉ | Sept indicateurs SQL/API conservés, pending exact ; contexte des signalements enrichi. | backend/index.py ; proposals.py ; frontend/admin-dashboard.js | Contre-recette Edge : sept valeurs confirmées et égales aux SELECT ; tests historiques | Aucune statistique de remplissage ; compteurs indépendants des likes. |
| C-07 — Informations RGPD et consentement | PARTIEL | Notices provisoires, politique en brouillon hors site et procédure interne. | frontend/inscription.html ; theories.html ; proposer-histoire.html ; documents RGPD | BILAN_LOT6E2.md ; tests de contrats HTML historiques | Valider les douze décisions, contact, bases, conservation, hébergement et organisation ; ne pas publier le brouillon. |
| C-08 — Index fichier/fonction/ligne | TERMINÉ | Nouvel index courant : fichiers, définitions et lignes vérifiés sur les sources inchangées. | INDEX_CODE_LOT6H1.md ; INDEX_CODE_JURY.md ; quatre fiches | Contrôle statique automatique des repères 6H.1 | Recalculer après toute édition ultérieure de code ; ancien index conservé comme historique. |
| C-09 — Commentaires français dans le vrai code | TERMINÉ | Commentaires français des vrais contrôleurs et services ; explications mises en rapport avec le code. | frontend/*.js ; backend/models.py ; vues ; migrations/ | BILAN_ETAPE51.md et bilans fonctionnels ; lecture statique 6H.1 | Répéter les explications ; aucune modification applicative dans cet audit. |
| I-01 — Où sont hébergées et servies les images, et pourquoi ? | TERMINÉ | Choix local établi : fichiers dans frontend/images, URL via middleware ; image_url est une référence. | frontend/images/README.md ; frontend/app.js ; run_local.py | WSGI et service HTTP local 6G.5 ; SUPPORT_JURY_LOT6H1.md | Statut terminé pour la démonstration locale ; aucun CDN ou hébergement public inventé. |
| I-02 — Provenance et droits des illustrations | NON TRAITÉ | Réserve documentaire explicite ; aucun justificatif de provenance ou de droits confirmé. | Quatre WebP ; frontend/images/default-story.svg ; frontend/images/README.md | Aucune preuve de licence ou d’attribution disponible | Obtenir auteur/outil/source et conditions d’utilisation avant validation d’une diffusion. |

Les cinq demandes partielles ne reçoivent aucun pourcentage intermédiaire. Les likes et commentaires sont des développements complémentaires ; ils ne gonflent pas le dénominateur.

**16 / 22 × 100 = 800/11 % = 72,727272… %, soit 72,73 % arrondi à deux décimales.** Cinq PARTIEL et un NON TRAITÉ. H-06 est PARTIEL pour le diagramme actuel à dix tables : un ancien rendu à neuf tables ne prouve pas la nouvelle lisibilité. C-01 et C-08 sont évalués sur les supports actuels ; I-01 porte sur le mode local démontré, pas sur un fournisseur public supposé.

## 6. Fonctionnalités et nature des preuves

« Automatisé » et « SQLite » indiquent les campagnes historiques, pas une nouvelle exécution en 6H.1. Le DOM simulé n’est jamais assimilé à Edge.

| Fonctionnalité | Automatisé / SQLite isolé | Véritable essai Edge disponible | Limite ou contrôle statique |
|---|---|---|---|
| Inscription et connexion | Tests backend/frontend et parcours WSGI | Oui, POST users 201 et login 200 dans 6G.5 initial ; nouvel accès admin confirmé en contre-recette | Installation vierge non rejouée |
| Histoires et Cold Cases | Lectures API/SQL, catégories, archives et refus | Oui, dossiers 17/42 initiaux ; navigation et compte sur Histoires/dossier corrigés | Classement frontend dépend encore des catégories 1/2 |
| Théories et propositions | Suites et lectures/écritures isolées | Soumissions historiques de l’étape 4, avec sessions fictives préparées par le harnais ; pas de nouvelle soumission 6G.5 | Pages ouvertes en 6G.5 ne prouvent pas leurs formulaires ; publication des propositions non livrée |
| Commentaires | POST/GET, validation, CSRF, rollback, DOM | Oui, trois créations et textes visibles dans 6G.5 initial | La contre-recette utilise un témoin créé par API de préparation, pas une nouvelle création humaine |
| Signalements | Cible FK, motif, permissions, contexte, affichage texte | Oui, deux créations initiales ; commentaire/dossier/catégorie/motif confirmés après actualisation | Plusieurs signalements d’un commentaire restent autorisés |
| Likes des histoires | Unicité Vote, ajout/retrait, deux comptes/cibles, refus et purge | Oui, opérations sur histoire et Cold Case ; état personnel 1/0 après actualisation confirmé sur dossier 17 | Pas de POST doublon volontaire Edge revendiqué |
| Likes des commentaires | CommentLike, cas historiques, contraintes et retrait | Oui, POST 200, DELETE 200, relectures de fiche 1/0 et confirmations humaines | Compteur historique non nul/invalide bloque ; compatibilité d’une base réelle inconnue |
| Administration des utilisateurs | Rôles, refus, liste, nettoyage et confirmations | Oui, lectures privées 200 et tableau visible | Clavier/mobile complets non attestés |
| Bannissement | Protections des administrateurs, 409, rollback, relecture du compte | POST ban 200 du compte ordinaire id 2 dans la recette initiale | Reconnexion de ce compte banni non recettée dans Edge |
| Dashboard, sept compteurs | Agrégats, pending exact, erreurs et états périmés | Oui, sept valeurs confirmées et égales aux SELECT en contre-recette | `/stats` public expose trois agrégats ; détails administrateur protégés |
| Archivage et restauration | Vraies routes/transactions SQLite, conservation et DOM | Non exercés humainement dans la recette Edge 6G.5 | Migration et verrous MySQL non attestés |
| Suppression de dossiers | Préconditions, FK, dépendances, rollback, confirmations et DOM | Non exercée humainement dans Edge 6G.5 | Aucun effacement automatique de compte ; aucune suppression réelle |
| Déconnexion | Session/CSRF, réponse perdue et nettoyage DOM | Oui, depuis Histoires : logout 200 puis quatre `/me` 401 ; Connexion et données masquées confirmées | Révocation centrale d’une copie de cookie non fournie |

Références : [tests et campagnes historiques](TESTS_ET_VALIDATION.md), [bilan 6G.2](BILAN_LOT6G2.md), [recette initiale](BILAN_LOT6G5.md), [contre-recette finale](BILAN_CORRECTIFS_LOT6G5.md), [suppression 6C.2](BILAN_LOT6C2_IMPLEMENTATION.md).

## 7. Modèles et migrations — revue documentaire

L’analyse AST trouve **dix modèles, treize FK, sept révisions et une tête unique `c6g200000001`**. Le contrat déclare 27 chemins et 36 opérations. Aucun de ces constats n’importe Flask, ne construit un moteur SQL ou n’applique Alembic.

Vote conserve le couple unique compte/dossier. CommentLike ajoute deux FK CASCADE, le couple unique compte/commentaire et un index de cible. La colonne physique `Comment.likes` reste conservée. Seul un entier exactement égal à zéro permet les nouveaux likes ; valeur non nulle, négative, incompatible ou NULL bloque la reprise candidate. Aucune attribution fictive, conversion ou remise à zéro n’est proposée.

Les sept migrations sont livrées comme sources candidates. Quatre anciennes révisions sont modifiées par rapport au HEAD ; trois candidates sont non suivies. Avant une future migration réelle autorisée, identifier les révisions déjà appliquées, examiner le schéma physique, les types et contraintes, contrôler les historiques Vote/Comment, les moteurs InnoDB et les FK, disposer d’une sauvegarde/restauration de données et arrêter les anciens écrivains. `create_all()` d’une base neuve ne met pas à niveau une base existante.

Risque DDL concret de 6G.3 : création de `comment_likes` réussie puis création d’index échouée ; un rollback ne garantit pas l’effacement de la table et une relance est refusée parce qu’elle existe déjà. Ne pas contourner ce refus, supprimer la table ou estampiller une révision pour faire passer la migration. Le traitement d’un état partiel doit faire l’objet d’un plan séparé fondé sur l’état réellement observé. Les six essais de la candidate en mémoire ne valident ni la chaîne réelle ni les DDL MySQL.

Les diagrammes README/fiche Mahamadou ont été actualisés et synchronisés pour les dix tables/treize relations. Leur nouveau rendu n’est pas exécuté. Aucune modification des modèles ou migrations n’est réalisée pour corriger la documentation.

## 8. Sécurité, ressources personnelles et RGPD

Le scan des 138 fichiers sélectionnés ne détecte pas les motifs examinés de clés privées, jetons de fournisseurs ou URL avec credentials. Aucun extrait ni valeur de correspondance n’est journalisé. Les sept exclusions et les fichiers privés n’ont pas été ouverts : leur innocuité n’est pas affirmée. L’historique Git complet n’est pas certifié par ce contrôle.

Les routes administrateur contrôlent le compte et le rôle en base ; le bannissement est relu côté serveur. Les sessions sont signées, cookies HttpOnly/SameSite Lax, Secure configurable. Le CSRF concerne les écritures authentifiées, avec exceptions explicites pour login et requêtes anonymes ; les vues conservent leurs permissions. Les contenus raccordés sont affichés avec `textContent`. Les lectures privées/états personnels et le cache local ont leurs protections documentées ; les sessions ne disposent pas d’un registre central de révocation.

Le lanceur ordinaire lit `.env` et donne priorité à un groupe Aiven complet. Aucune configuration privée n’est examinée. La procédure sur un autre PC privilégie le kit qui neutralise ces entrées avant l’import.

Les notices restent provisoires. Les douze décisions RGPD portent notamment sur responsable/contact, finalités et email, bases, conservation, hébergement/transferts, public/contenus réels, contributions lors d’un effacement, identité/révocation, opérateurs et sauvegardes. Elles ne sont pas réputées validées par une recette technique. La politique HTML reste sous `docs/`, hors site ; aucune publication ni conformité totale annoncée.

La provenance et les conditions d’utilisation des quatre WebP et du SVG ne sont pas confirmées. Les anciennes ressources frontend peuvent également nécessiter une revue de contenu avant diffusion. Les noms des étudiants dans les supports répondent à la répartition demandée ; aucune information de compte ou donnée réelle de contribution n’est ajoutée aux livrables.

## 9. Supports et reprise sur un autre ordinateur

Les [supports courants](SUPPORT_JURY_LOT6H1.md) répartissent les explications : Mélissa — HTML/CSS/JavaScript/DOM ; Sylvie — Flask/API/authentification/CSRF ; Mahamadou — SQLAlchemy/relations/contraintes/intégrité/compteurs. Ils proposent des formulations de première année et un scénario court. Les 76 questions/réponses historiques des fiches sont préservées, avec un avertissement de contexte et un renvoi au nouvel [index de 70 repères](INDEX_CODE_LOT6H1.md).

Le [guide autre PC](LANCEMENT_AUTRE_PC_LOT6H1.md) prépare une copie courante, Python/venv/dépendances et l’inspection du kit SQLite mémoire sans MySQL. Il distingue commandes préparées et opérations effectivement exécutées. Il n’affirme pas qu’un clone du HEAD contient les travaux locaux, ni qu’une installation sur un PC vierge a réussi. Le futur lancement réseau/Edge reste soumis à une autorisation distincte.

## 10. Tests disponibles et contrôles de ce lot

| Preuve disponible | Statut en 6H.1 |
|---|---|
| 311 backend + 513 frontend + 30 contrats/lanceur = 854 PASS | Historique du 1er novembre ; sorties et manifeste retrouvés, pas de réexécution |
| 76 sources du manifeste de cette campagne | Empreintes comparées, aucune différence au début de l’audit |
| 40 sources du kit 6G.4 | Empreintes normalisées LF comparées, aucune différence ; manifeste non renouvelé |
| Sept anciens tests de migration exclus | Non comptés comme PASS ni comme migrations validées |
| Six essais de candidate likes SQLite mémoire | Historiques, pas une application réelle des migrations |
| 17 groupes / 99 échanges du parcours contrôleurs→WSGI→SQL | Historique, DOM simulé, aucun navigateur |
| 200 requêtes Edge / 134 API de la contre-recette finale | Historique humain distinct ; source des confirmations UI, likes, compteurs, logout |
| AST, chaîne de révisions, labels/statuts, liens, repères, diagrammes et hashes | Contrôles statiques documentaires 6H.1 ; ne pas les ajouter aux 854 |
| Sauvegarde durable ancienne | 115 empreintes relues, toutes conformes ; aucune nouvelle sauvegarde créée |

Les preuves antérieures restent dans les dossiers temporaires référencés par leurs bilans. Elles sont retrouvées aujourd’hui mais ne sont pas une archive durable de tous les outils : leur conservation et la portabilité du harnais complet restent à préparer. Les sources de tests seules ne suffisent pas à promettre une reproduction sûre des 854 avec une découverte globale non inspectée.

**Contrôles finaux 6H.1 : PASS documentaire.** 22 libellés conservés et statuts comptés ; 70 repères de définition vérifiés ; deux sources ER identiques (10 entités/13 relations), sans rendu navigateur ; nouveaux liens locaux valides ; questions/réponses historiques des quatre fiches intactes ; 125 fichiers examinables préexistants inchangés et treize documents actualisés uniquement. Les 76 sources des 854 PASS et les 40 sources du kit restent identiques. Ces contrôles ne sont pas de nouveaux tests applicatifs.

## 11. Risques et plan de commits

Le plan détaillé (pièce interne non diffusée) et le CSV attribuent les chemins à cinq messages proposés :

1. `Intégrer les contributions, les likes et l’administration sécurisée`.
2. `Couvrir les parcours métier et les contrôles de sécurité`.
3. `Préparer la recette locale isolée et son manifeste contrôlé`.
4. `Actualiser les supports du jury et la préparation de livraison`.
5. `Conserver les archives techniques des étapes précédentes`.

Les risques à lever sont concrets : sources récentes non couvertes par la copie durable ancienne ; fichiers déjà suivis à arbitrer malgré l’ignore ; droits des images non documentés ; brouillons internes à ne pas publier ; harnais complet dépendant de Temp ; installation vierge non éprouvée ; ancienne chaîne de migrations modifiée et cible réelle inconnue. Aucun secret n’est demandé pour résoudre ces points dans le présent audit.

## 12. Verdict et arrêt

**NO-GO pour finaliser la préparation d’une livraison Git sûre et reproductible en l’état.** L’audit, l’inventaire, la matrice et le plan de commits sont prêts à être examinés. Avant une future indexation : nouvelle sauvegarde sélective avec récupération contrôlée, décisions sur les ressources/anciens jeux/documents internes et validation d’une copie autonome sur un autre PC sous autorisation adaptée.

Ce NO-GO ne retire pas le **GO de démonstration locale isolée 6G.5**. Il distingue une application fonctionnelle recettée d’un arbre Git et d’une procédure de livraison prêts à diffuser. Aucun commit, push, fusion, déploiement, suppression ou nouveau lot engagé. Arrêt après 6H.1 et attente de l’autorisation suivante.

Preuves locales de l’audit, hors dépôt et sans secrets :

`[chemin local privé retiré]`

Les reçus comprennent l’état initial, son complément `.cjs`, les copies documentaires avant édition, l’inventaire, l’audit des sources/migrations/contrat, la comparaison de sauvegarde, les 22 statuts, les repères actuels et les contrôles finaux. Les livrables durables de préparation sont les documents et listes présents dans `docs/soutenance/` ; ils ne constituent pas la nouvelle copie de sauvegarde proposée.
