# Lot 6H.4 — clôture des remarques partielles

> Archive pédagogique datée : les résultats et descriptions ci-dessous concernent le lot indiqué. Les anciens repères de ligne ne décrivent pas la version candidate. Pour préparer la soutenance actuelle, consulter les quatre fiches et le référentiel reliés au sommaire.

> Copie publique de référence : les chemins personnels et liens de travail internes sont retirés. Les preuves et commandes historiques gardent leur date et leur périmètre ; utiliser le README actuel pour le lancement.

2 novembre 2026. **19 remarques TERMINÉES sur 22, trois PARTIELLES, zéro NON TRAITÉE.** H-03, H-06 et P-01 sont clôturées après rendu des sources actuelles et inspection visuelle. C-02, C-07 et I-02 restent partielles. Calcul exact : **19/22 × 100 = 950/11 % = 86,363636… %, soit 86,36 % arrondi**. Les lignes partielles ne donnent aucun crédit intermédiaire.

**GO pour la soutenance scolaire locale dans le périmètre synthétique déjà recetté ; NO-GO pour les commits de livraison de l'ensemble actuel ; NO-GO pour une ouverture publique.** Le GO local ne constitue ni une certification des droits des images, ni une conformité RGPD, ni une garantie de préparation des accès du jour J.

Références reprises intégralement lors de l'audit : [6H.3](BILAN_LOT6H3.md), [6H.2](BILAN_LOT6H2.md), [6H.1](BILAN_LOT6H1.md), plan de livraison (pièce interne non diffusée), [matrice](SUIVI_REMARQUES_JURY.md), [recette 6G.5](BILAN_LOT6G5.md), [correctifs et contre-recette 6G.5](BILAN_CORRECTIFS_LOT6G5.md), procédures et instructions du dépôt. Les bilans et manifestes historiques restent inchangés.

## 1. Autorisation, état Git et conservation

Le texte d'autorisation 6H.4 permet l'audit, les vérifications isolées et les corrections documentaires ; il interdit les modifications applicatives et les opérations de livraison. Une réponse distincte autorise **« ces trois rendus documentaires uniquement »** : Edge headless hors réseau, profil temporaire neuf, aucun serveur Flask, site ou base. Aucun autre lancement n'en est déduit. La recherche de consignes n'a trouvé aucun `AGENTS.md` dans le dépôt et les parents accessibles contrôlés ; l'absence de consigne dans un emplacement inaccessible n'est pas certifiée.

| Élément | Début 6H.4 | Fin 6H.4 |
|---|---|---|
| Branche | `feature/frontend-api-integration` | Identique |
| HEAD | `07a9f03ea0a3bdad4a07066fdd7bab1997cc158b` | Identique |
| Fichiers suivis / suivis modifiés | 66 / 51 | 66 / 51 |
| Non suivis, comptés individuellement | 109 | 122 |
| Indexés / conflits | 0 / 0 | 0 / 0 |
| SHA-256 de l'index | `cc33bbdc5993495735a8c63e85f22f321b05323716ff29b4af3d0fd8df6c5ec3` | Identique |

Les 175 chemins initiaux sont conservés. Treize nouveaux fichiers documentaires portent l'inventaire final à **188 chemins**, suivis et non suivis. Seuls deux fichiers préexistants changent pendant 6H.4 : la matrice et l'index de soutenance. Le README principal, les fiches, le code, les modèles, les migrations, les tests, les cinq illustrations et les manifestes ne changent pas. Aucun ajout à l'index, commit, push, merge, reset, changement de branche, retrait du suivi ou suppression.

La sauvegarde `[chemin local privé retiré]` et la récupération `recuperation-lot6h2-20261102-55c80c78`, sous le même parent, ont été relues : **197 fichiers chacune**, ensembles, tailles et empreintes identiques aux reçus ; aucun écart. Elles comprennent 169 sources, 25 roues Python et trois métadonnées. Les 196 entrées hachées et les deux exemplaires du reçu sont vérifiés ; SHA-256 du reçu : `9e1c04fb1f5d9c47bd992631b9aaf6815b3531798f3724e649de2e0e511b8fc7`.

Depuis 6H.2, trois sources diffèrent : `README.md`, `docs/soutenance/README.md`, `docs/soutenance/SUIVI_REMARQUES_JURY.md` ; **166/169 restent identiques**. Le bilan et le reçu 6H.3 sont deux ajouts ultérieurs. Ces cinq documents ont été copiés et vérifiés dans le dossier temporaire 6H.4 avant édition. Cette conservation ciblée n'est **pas une sauvegarde durable supplémentaire**. Le travail présent est documentaire et réversible ; avant toute future opération à risque, prévoir une nouvelle sauvegarde sélective vérifiée couvrant les deltas 6H.3/6H.4, sans écraser 6H.2. Aucune sauvegarde de base réelle ou de tout l'historique Git n'est revendiquée.

## 2. Preuves retrouvées et adéquation aux critères

Les détails, chemins et empreintes sont conservés dans le reçu 6H.4 (pièce interne non diffusée). Les pièces temporaires historiques restent des preuves locales dont la disponibilité future n'est pas garantie.

| Preuve | Résultat établi | Ce qu'elle ne prouve pas |
|---|---|---|
| 6G.5, `cache-repair/preflight.json` et `final-validation.json` sous `portfolio-correctifs6g5-20261101-d26bc6c9` dans Temp | **854 PASS historiques : 311 backend + 513 frontend + 30 lanceur/contrats. Les 76 empreintes brutes des sources correspondent encore exactement aux fichiers actuels.** | Aucune réexécution en 6H.4 ; ni droits d'image, ni fiche privée, ni décisions RGPD |
| Garde-fous backend/lanceur historiques | Sept compteurs d'interdiction à zéro ; sept anciens cas de migration exclus ; six exécutions de candidate likes en mémoire seulement | Les exclusions ne sont pas des PASS ; aucune migration MySQL validée |
| `cache-repair/integration-frontend.json` | 17 groupes et 99 échanges intégrés avec DOM simulé | Aucun contrôle visuel de navigateur |
| `access-repair/manual-validation.json`, `like-reconciliation.json`, `shutdown-verification.json` | Confirmation humaine dans Edge des affichages du compte et du signalement, cycles ajout/retrait des deux likes après actualisation, sept compteurs identiques à SQL et déconnexion ; 200 requêtes Edge dont 134 API ; arrêt vérifié | Aucun nouveau parcours Edge du site ici ; ni disponibilité des accès au prochain démarrage, ni purge MySQL |
| Vérification HTTP 6H.2 (pièce interne non diffusée) | 71 requêtes, 13 groupes, copie et venv neufs sur le même PC, SQLite mémoire et FK actives, garde-fous à zéro, serveur arrêté | Pas un autre ordinateur ; pas un navigateur ; pas une migration existante |
| Parcours WSGI 6H.2 (pièce interne non diffusée) | 43 requêtes, sept groupes : protections, likes, conservation et rollback dans le cadre synthétique documenté | Pas une recette publique ni une preuve de droits |
| Manifeste du kit `tools/recette_lot6g4_sources.json` | **40/40 empreintes normalisées LF conformes**, sans régénération | Aucun lancement du kit en 6H.4 |
| Ancien rapport Mermaid du 29 octobre dans Temp | Ancienne architecture et séquence en échec visuel ; ancien ER lisible à neuf tables | Les trois sources ont changé : ces rendus sont écartés comme preuves de clôture actuelle |
| Nouveaux rendus 6H.4 | Trois sources épinglées, SVG valides, PNG inspectés, copies Markdown synchronisées ; dix modèles et treize FK vérifiés statiquement | Aucun rendu GitHub ou vidéoprojecteur réel attesté ; aucune validation du schéma physique MySQL |

Les sept compteurs de la contre-recette Edge sont 2 histoires, 1 résolue, 1 Cold Case, 3 utilisateurs, 1 commentaire, 1 signalement, 0 proposition en attente. La recette distincte 6H.2 crée un membre et une proposition supplémentaires : ses chiffres ne doivent pas être mélangés à ceux de 6G.5. Les reçus existants ont été lus sans ouvrir les bases, les sorties contenant des accès ni les secrets.

## 3. Les six remarques examinées

Les identifiants et libellés ci-dessous sont ceux de la matrice autorisée ; aucune nouvelle formulation du jury n'est inventée.

### H-03 — Houssem : améliorer l'architecture

**PARTIEL → TERMINÉ. Documentation et preuve visuelle.** Le service des fichiers, le navigateur/DOM, WSGI, Flask et SQLAlchemy étaient déjà expliqués et le connecteur corrigé. Les tests historiques de service statique prouvent le comportement, pas la disposition du dessin.

Le [PNG actuel](preuves-lot6h4/diagrammes/diagram-1.png), son [SVG](preuves-lot6h4/diagrammes/diagram-1.svg) et la [source exacte](preuves-lot6h4/diagrammes/diagram-1.mmd) montrent le connecteur « lit les fichiers publics » entre middleware et fichiers, sans traverser le bloc Flask ni masquer son texte. Les responsabilités et flèches sont lisibles. Inspection effectuée sur l'image exportée, pas seulement sur un retour technique PASS. La preuve manquante est acquise ; aucune retouche du diagramme ni du code n'a été nécessaire.

Fichiers de référence : `README.md`, `fiche-commune.md`, `run_local.py`. Les deux copies Mermaid sont identiques. Pour vérifier la clôture, rapprocher leur source LF de l'empreinte du reçu et ouvrir l'export. À l'oral, préciser que le dessin décrit le lanceur normal et ses cibles possibles ; le kit jury utilise SQLite mémoire et son port dédié. Aucun nouveau choix humain ne conditionne cette explication locale ; la validation de MySQL reste une question de déploiement distincte.

### H-06 — Houssem : rendre le relationnel lisible

**PARTIEL → TERMINÉ. Documentation et preuve visuelle.** Les sources décrivaient déjà dix tables et treize relations, les couples uniques de Vote/CommentLike et `management_revision`. L'ancien rendu à neuf tables ne suffisait pas.

Le [PNG actuel](preuves-lot6h4/diagrammes/diagram-2.png), le [SVG](preuves-lot6h4/diagrammes/diagram-2.svg) et la [source](preuves-lot6h4/diagrammes/diagram-2.mmd) ont été rapprochés des dix modèles/treize FK. Noms, champs et cardinalités sont lisibles ; les deux liens de `comment_likes` vers `users` et `comments`, ainsi que le lien `reports → comments`, sont identifiables. Des croisements de traits demeurent au centre sans empêcher de suivre les relations ; ce n'est pas une promesse de dessin sans aucun croisement. Les unicités de couples restent explicitement distinguées des clés uniques individuelles.

Fichiers : `README.md`, `fiche-mahamadou.md`, `backend/models.py` en référence. Vérification de clôture : source/empreinte, copies identiques, comparaison AST et inspection de l'export à une taille lisible ; utiliser le SVG avec zoom pour la présentation. Aucune correction des modèles ni décision humaine nouvelle n'est nécessaire. La lisibilité documentaire ne valide pas les migrations MySQL.

### P-01 — Pauline : expliquer le flux de données

**PARTIEL → TERMINÉ. Documentation et preuve visuelle.** Le parcours formulaire, session/CSRF, HTTP, contrôles, SQL/transaction, réponse et DOM était déjà expliqué et éprouvé dans les recettes isolées. Ces tests ne mesuraient pas la note finale.

Le [PNG actuel](preuves-lot6h4/diagrammes/diagram-3.png), le [SVG](preuves-lot6h4/diagrammes/diagram-3.svg) et la [source](preuves-lot6h4/diagrammes/diagram-3.mmd) montrent la note en trois lignes entièrement contenue dans son cadre. Les flèches et branches refus/succès/rollback sont lisibles. L'actualisation manuelle et l'absence de répétition automatique du POST restent explicites. Le diagramme est haut : le consulter en pleine taille ou avec défilement, sans le réduire à une miniature.

Fichiers : `README.md`, `fiche-commune.md` ; `frontend/api.js`, `frontend/app.js`, `backend/api/v1/views/theories.py` comme références inchangées. Vérification : comparer les copies et l'empreinte, inspecter note/cadres/flèches et expliquer le flux avec les contrôleurs. Aucun développement ni arbitrage humain supplémentaire requis pour ce critère local.

### C-02 — Fichier privé de comptes de démonstration

**PARTIEL → PARTIEL. Organisation humaine et preuve de disponibilité.** Procédure, modèle et génération d'accès fictifs éphémères existent ; les connexions membre/admin sont démontrées historiquement. Elles ne prouvent pas une fiche privée correspondant au prochain processus.

Réponse de l'utilisateur en 6H.4 : **« Pas encore confirmé »** pour le détenteur et l'organisation du jour J. Aucun détenteur n'est donc désigné dans ce bilan. Fichiers : `COMPTES_DEMO.exemple.csv` (contenu non ouvert), `DEMONSTRATION.md`, `tools/recette_lot6g4.py`. La fiche effective devra rester hors Git.

Minimum restant : désigner qui démarre le kit, relève et conserve les accès du processus courant, prévoit leur renouvellement après redémarrage et leur disponibilité privée. Clôture : confirmation sans identifiant/mot de passe, puis connexion des deux rôles dans une recette séparément autorisée, avec seulement date/rôle/réussite consignés. Aucun défaut d'authentification ni correction de code établi. Ce point concerne directement la préparation scolaire, pas uniquement la production.

### C-07 — Informations RGPD et consentement

**PARTIEL → PARTIEL. Décisions humaines, documentation puis vérification d'intégration.** Notices provisoires et brouillons existent ; les contrats HTML historiques prouvent leur présence, pas leur complétude juridique. L'utilisateur confirme : **« Aucune nouvelle décision validée »**.

Les décisions D01 à D12 restent à prendre, détaillées en section 6. La politique demeure en brouillon interne, hors site. Les fichiers concernés sont les documents `LOT6E1_*`, `document interne non publié`, `PROCEDURE_DROITS_LOT6E2.md`, puis les notices des pages d'inscription, théorie, proposition et dossier/commentaires lors d'une intégration autorisée.

Minimum : valider les informations réelles, inclure Vote/CommentLike dans l'information, compléter les textes, puis autoriser les seules retouches nécessaires aux notices/liens/contact. Clôture : décisions tracées, information cohérente sans champ indispensable manquant, contact accessible hors connexion et contrôles ciblés isolés. Aucun développement supplémentaire n'est justifié maintenant. Cela bloque la collecte publique ; la démonstration synthétique reste possible sans annoncer une conformité complète.

### I-02 — Provenance et droits des illustrations

**PARTIEL → PARTIEL. Provenance, justificatifs et destination.** Le registre et les empreintes existaient ; le service local des images est prouvé, leurs droits ne le sont pas par un test.

La réponse utilisateur précise désormais que **Mélissa a généré les quatre WebP avec ChatGPT et que l'usage indiqué est la soutenance locale**. Elle ne répond pas sur les images de référence ni sur l'origine distincte du SVG. Elle n'autorise pas une diffusion publique. Ces faits complètent le registre historique sans le réécrire.

Fichiers : quatre WebP et `default-story.svg` dans `frontend/images/`, README des images, [registre 6H.2](REGISTRE_IMAGES_LOT6H2.md). Minimum : rattacher une confirmation datée à chaque fichier, clarifier les références/entrées et leur droit d'utilisation, identifier les conditions de génération, puis justifier séparément le SVG. Clôture par revue de ces pièces pour la destination retenue. Aucun remplacement d'image nécessaire démontré ; aucun fichier image existant modifié. La provenance reste pertinente pour le dossier scolaire, l'accord public constitue une décision supplémentaire.

## 4. Contrôles nouveaux réellement exécutés

Avant exécution : lecture du script de rendu, vérification de sa liste fermée de trois empreintes, de son profil neuf, du blocage réseau, de l'absence de lancement serveur et de la fermeture de son propre navigateur. Les scripts de rapprochement utilisent uniquement la bibliothèque standard, des chemins déterminés et Git en lecture seule, sans import applicatif, découverte globale de tests ou ouverture de base.

L'essai précédent en contexte élevé avait échoué avant lancement sur `MODULE_NOT_FOUND`. Le helper a ensuite été retrouvé dans le contexte de travail ; le lancement autorisé y a réussi. Ce premier échec n'est ni un défaut du portfolio ni une preuve de rendu. Aucun changement de permissions Windows n'a été effectué.

Le reçu de rendu (pièce interne non diffusée) date l'exécution du **2 novembre, 17:04:59 à 17:05:05 UTC** : Edge headless, Playwright 1.58.2, module Mermaid local identifié par SHA-256. Trois SVG analysés sans erreur XML et avec dimensions non nulles ; aucune requête refusée enregistrée dans ce parcours local, contexte configuré hors ligne avec interception, proxy inutilisable et résolution réseau bloquée. Le navigateur propre au contrôle a été fermé. Le profil temporaire neuf est conservé ; aucun autre navigateur n'a été fermé.

L'inspection des trois PNG par l'assistant a ensuite porté sur les critères décrits en section 3. Les exports ont été copiés dans le dépôt par liste fermée et leurs empreintes comparées aux originaux temporaires. L'outil de visualisation ne pouvant lire directement les PNG sous Temp, il a inspecté ces copies identiques dans le dépôt. Les sources canoniques n'ont pas été retouchées.

| Contrôle | Résultat |
|---|---|
| Sources 854 / kit figé | 76/76 SHA bruts et 40/40 SHA normalisés LF conformes |
| Sources Mermaid | Trois blocs canoniques, trois copies synchronisées, empreintes égales aux sources rendues |
| Modèles et chaîne de migrations | Dix modèles, treize FK ; sept révisions, tête unique `c6g200000001`, analyse statique uniquement |
| Rendus et inspection | Trois PASS techniques ; trois critères visuels satisfaits, avec limites de présentation précisées |
| Matrice finale | 22 identifiants/libellés conservés ; 19 TERMINÉ, trois PARTIEL ; seize lignes antérieurement terminées inchangées |
| Conservation | 172 fichiers initiaux hachés : seules les deux retouches documentaires déclarées diffèrent ; trois chemins sensibles exclus des lectures et conservés |
| Inventaire | 188 chemins uniques, correspondant à tous les fichiers suivis/non suivis ; fichiers ignorés exclus du contenu de livraison |
| Liens locaux des documents retouchés | Cibles vérifiées ; ancres et rendu GitHub non recettés |
| `git diff --check` | Code 2 et 164 signalements CRLF préexistants ; avec `-c core.whitespace=cr-at-eol` pour la seule commande : code 0, sans modifier Git ni les fins de ligne applicatives |

**Aucune campagne applicative réexécutée : les 854 PASS restent historiques.** Les contrôles statiques et les trois rendus ne s'ajoutent pas à ce nombre. Aucun Flask, site, base SQL, migration, installation de dépendance ou nouvelle recette HTTP/WSGI. Les consultations des sources officielles juridiques sont distinctes du navigateur de rendu et du portfolio.

## 5. Images : état et justificatifs encore manquants

| Fichier original | Fait disponible en 6H.4 | Reste à établir |
|---|---|---|
| `tableau-salle-bleue.webp` | Mélissa, ChatGPT, soutenance locale, déclaration utilisateur | Confirmation par fichier, date/contexte de génération, références éventuelles et conditions applicables |
| `medaille-pavillon-ferme.webp` | Même déclaration | Même réserve |
| `malle-quai-silencieux.webp` | Même déclaration | Même réserve |
| `carnet-tour-nord.webp` | Même déclaration | Même réserve |
| `default-story.svg` | Origine distincte inconnue ; repli utilisé par le kit ; entrée Git `e8f8e4c` du 24 octobre | Auteur/source/outil et justification de l'usage ; ne pas lui attribuer ChatGPT par déduction |

Les cinq originaux restent identiques à la sauvegarde. L'absence de métadonnées des WebP, la simplicité du SVG et la date d'ajout Git ne constituent pas des licences. Les nouveaux SVG/PNG sous `preuves-lot6h4/diagrammes/` sont des exports documentaires des diagrammes existants, distincts des illustrations applicatives ; aucune illustration n'a été créée, remplacée ou supprimée.

Pour le dossier scolaire : demander à Mélissa une confirmation datée reliant les quatre noms de fichiers à la génération, aux entrées éventuelles et à l'usage local ; un extrait de génération/export sans information privée peut corroborer cette déclaration. Une absence de référence doit être déclarée, pas supposée. Pour le SVG, obtenir une réponse séparée : création originale ou source tierce, avec justificatif adapté. Aucun accès à un compte ou export intégral de conversation n'est demandé.

Pour une diffusion publique : obtenir un accord explicite pour cette destination et les justificatifs des éventuelles ressources tierces, avec leurs conditions ; examiner les éléments identifiables selon l'usage prévu. La réponse reçue couvre seulement la soutenance locale. Les [conditions européennes OpenAI](https://openai.com/policies/eu-terms-of-use/), version affichée du 16 janvier 2026, consultées à nouveau le 2 novembre, distinguent les droits sur entrées/sorties et ne garantissent pas l'unicité. Elles ne prouvent pas les droits propres à ces fichiers ; compte, territoire et date applicables restent à établir. Aucune licence Creative Commons, exclusivité ou autorisation de tiers n'est inventée.

## 6. RGPD : décisions exactes attendues

**Politique et page HTML : BROUILLONS INTERNES NON VALIDÉS, NON PUBLIÉS.** Aucun responsable, contact, fondement, durée ou hébergeur n'a été renseigné fictivement. Les thèmes ci-dessous reprennent les décisions du projet et la revue 6H.3.

| Décision | Réponse attendue de l'équipe |
|---|---|
| D01 — Responsable | Identité et coordonnées de l'entité qui décide des traitements ; rôle de l'école et DPO éventuel, sans désignation automatique d'un étudiant ou d'Holberton |
| D02 — Contact | Canal réellement suivi, accessible aussi sans connexion, aux personnes bannies et aux tiers |
| D03 — Finalités et minimisation | Utilité de chaque donnée, dont email obligatoire malgré une connexion par pseudo ; distinction compte, contributions, modération, sécurité, demandes de droits |
| D04 — Bases légales | Choix justifié par traitement, incluant votes/likes ; aucun consentement général ni contrat présumé |
| D05 — Conservation | Durée ou critère, point de départ, réexamen, action et responsable pour chaque catégorie : comptes, textes, archives, likes, signalements, demandes et journaux |
| D06 — Hébergement et flux | Prestataires réellement retenus, lieux, destinataires, sous-traitants, contrats et transferts éventuels ; le code Aiven ne prouve ni le déploiement ni sa localisation |
| D07 — Public et contenus | Mineurs, récits fictifs/réels, personnes citées et contenus sensibles : périmètre et règles effectives |
| D08 — Contributions | Devenir des textes, pseudonymes copiés et mentions de tiers ; `user_id=NULL` ne suffit pas à les retirer |
| D09 — Identité et sessions | Vérification proportionnée des demandes, traitement des anciennes sessions et de la réutilisation éventuelle d'identifiants |
| D10 — Organisation des droits | Personnes habilitées, réponse sécurisée, suivi privé minimal et mise en œuvre effective |
| D11 — Exploitation | Configuration réellement déployée de HTTPS/cookies/caches/logs, ressources externes, flux et gestion des incidents |
| D12 — Copies | Conservation des sauvegardes, traitement des copies et restauration évitant la réapparition de données retirées |

La [CNIL sur l'information des personnes](https://www.cnil.fr/fr/informer-les-personnes) demande notamment identité, finalités, bases, destinataires, conservation et modalités d'exercice des droits ; la [CNIL sur la conservation](https://www.cnil.fr/fr/passer-laction/les-durees-de-conservation-des-donnees) lie les durées aux finalités et à leur justification. Ces sources officielles, consultées le 2 novembre, ne fournissent pas les réponses propres au portfolio.

Les futurs textes devront intégrer `CommentLike`, ajouté après les premiers brouillons, et distinguer bannissement, archivage, purge de dossier et effacement d'une personne. Aucune bannière, portail de droits ou suppression automatique n'est préconisée sans besoin établi. **C-07 reste PARTIEL ; aucune conformité RGPD complète annoncée.** Le périmètre scolaire retenu utilise des données synthétiques, sans collecte publique improvisée.

## 7. Base de données : réserves maintenues

La revue s'appuie sur les sources et preuves historiques, sans import applicatif ni connexion. Aucun accès MySQL/Aiven réel, aucun moteur SQL ouvert ni migration exécutée dans ce lot.

| Sujet | Acquis et réserve | Suite minimale éventuelle |
|---|---|---|
| Migrations | Sept révisions en chaîne ; quatre anciennes modifiées et trois candidates non suivies ; état réellement appliqué inconnu | Revoir historique appliqué, schéma, types, moteurs, contraintes et sauvegarde/restauration avant une cible MySQL autorisée ; ne pas réécrire l'historique appliqué |
| DDL partiel | Création de table puis index : un échec intermédiaire peut laisser un état que le précontrôle refuse ; rollback applicatif ne prouve pas retour du schéma | Préparer diagnostic/reprise à partir de l'état observé ; aucune suppression, désactivation de FK ou estampillage pour contourner un refus |
| Anciens compteurs | Candidate/API likes acceptent seulement un ancien compteur entier exactement nul ; valeurs incompatibles bloquent ; aucune attribution individuelle déductible | Décision sur l'historique, sans remise à zéro ou redistribution inventée ; distinguer `Theory.likes` et Vote |
| SQLAlchemy | Dix modèles/treize FK ; cascades de Story et des enfants de Comment ; `User.comment_likes` possède aussi sa cascade, contrairement à d'autres collections User | Ne pas généraliser les cascades ni proposer un simple effacement User ; auteur obligatoire et pseudonymes copiés restent à traiter dans une conception distincte |
| Purge de dossiers | Archive préalable, admin, CSRF, titre, confirmation fraîche, empreinte/révision/If-Match ; enfants ciblés et rollback éprouvés localement | C-05 reste TERMINÉ dans sa portée ; concurrence/verrous/MySQL non éprouvés ; aucune suppression réelle pour enrichir la soutenance |
| Commentaires/signalements | FK obligatoire Report vers Comment, cascades et contrôles d'orphelins ; cibles historiques incompatibles refusées | Examiner l'intégrité physique avant reprise réelle, arrêter les anciens écrivains ; ne pas réattribuer/effacer silencieusement les données |
| Résultat incertain | Pas de répétition automatique d'un DELETE dont le résultat est inconnu ; absence d'un dossier sans reçu ne prouve pas l'auteur de la suppression | Maintenir les limites et la relecture prévues ; aucun reçu persistant ajouté par défaut |

Références : [6C.2](BILAN_LOT6C2_IMPLEMENTATION.md), [6G.2](BILAN_LOT6G2.md), [6H.3](BILAN_LOT6H3.md), modèles, vues et candidates inchangés. Ce sont des risques de déploiement documentés, pas des incidents observés sur Aiven. **Aucun défaut applicatif nouveau ne justifie une correction de code dans ce lot.**

## 8. Livraison Git préparée, non exécutée

L'inventaire 6H.4 (pièce interne non diffusée) couvre les **188 chemins** présents à la clôture, avec état initial, catégorie, preuve, rôle local, correction/decision de diffusion et lot proposé. Il remplace comme outil de sélection courant l'inventaire 6H.1, sans effacer cet historique. Il n'est pas une liste approuvée à ajouter à Git.

| Catégorie | Nombre | Position de livraison |
|---|---:|---|
| Sources techniques | 44 | Candidats après revue des dépendances et de la sélection |
| Tests et contrats | 33 | Garder les exclusions historiques explicites ; ne pas lancer une découverte globale non isolée |
| Kit scolaire isolé | 3 | Script, manifeste figé et contrat ensemble ; dépendances et SVG à prendre en compte |
| Migrations candidates | 7 | Sources candidates documentables, aucune application autorisée |
| Documents/preuves à revoir avant diffusion | 83 | Adapter une copie au destinataire : chemins locaux, informations d'équipe, liens internes ; conserver les originaux |
| Documents RGPD internes | 7 | Conservation privée ; aucune publication de brouillon |
| Ressources aux droits non clarifiés | 5 | Quatre WebP et SVG déjà suivis ; décision par fichier et destination |
| Données à exclure | 3 | `frontend/donnees.js`, `frontend/histoires-originales.json`, `docs/soutenance/COMPTES_DEMO.exemple.csv` ; contenus non ouverts |
| Archives techniques | 3 | Ancien kit 6F.2 et copie de modèle de Mahamadou à conserver distincts ; destination à décider |

**72 fichiers sont repérés comme prêts dans la portée technique locale historique**, ce qui ne signifie pas 72 fichiers librement publiables. Les autres catégories peuvent nécessiter une revue ou une décision sans présenter un défaut de code. Les deux corrections documentaires nécessaires au suivi sont réalisées ; l'adaptation de diffusion reste à préparer une fois le destinataire choisi.

Les cinq images et `frontend/donnees.js` sont **déjà suivis** : omettre un futur `git add` ne les retire pas de l'arbre hérité. Les deux autres fichiers du groupe données sont non suivis mais non ignorés ; aucun ajout global ne convient. `.env`, cookies, certificats, environnements, bases/dumps et journaux privés restent exclus ; aucune lecture de secrets ni certification exhaustive de l'historique Git. Aucune règle `.gitignore` ou permission Windows modifiée.

Une revue des liens a repéré **40 liens directs dans 14 documents préexistants** vers les sept documents internes. Une sélection publique les excluant devra adapter ces liens dans sa copie de diffusion ; les retirer seulement de la liste produirait des références manquantes. Ce constat de préparation n'est pas un défaut applicatif. Le présent bilan et la matrice devront aussi être revus selon cette destination.

Stratégie progressive proposée, sans action Git :

1. Décider le destinataire privé/scolaire/public, les ressources déjà héritées, les données historiques, documents internes et archives ; conserver une sélection explicite et une sauvegarde actualisée vérifiée.
2. **A — Sources et candidates** : réunir les changements fonctionnels interdépendants, contrat API et candidates avec leurs limites MySQL, sans appliquer de migration.
3. **B — Tests** : associer les tests pertinents et leurs conditions d'isolation, en documentant les sept exclusions et le harnais historique actuellement extérieur au dépôt.
4. **C — Kit scolaire** : script, manifeste et test ensemble ; résoudre le traitement du SVG requis avant la destination choisie, sans altérer le manifeste pour masquer une différence.
5. **D — Documentation** : sélectionner une copie cohérente des supports et preuves, contrôler les liens et les renseignements à diffuser ; ne pas présenter une politique incomplète comme définitive.
6. **E — Archives facultatives** : décider leur conservation privée ou leur livraison séparée sans les fusionner avec les sources actives.
7. Revoir la liste finale et obtenir l'autorisation de commit correspondant à cette sélection. Aucun push/publication n'est déduit d'une future autorisation de commit.

**Aucun blocage technique de Git n'est constaté : index vide, pas de conflit.** Le NO-GO concerne la sélection de livraison, les ressources héritées, leurs droits/destinations et la revue des documents/données, auxquels s'ajoute l'absence d'autorisation d'opération Git. La finalisation RGPD et les essais MySQL ne sont pas à eux seuls nécessaires à un commit de sources candidates correctement délimité ; ils conditionnent l'exploitation concernée.

## 9. Livrables et plan minimal suivant

| Document | Travail 6H.4 |
|---|---|
| `SUIVI_REMARQUES_JURY.md` | Trois clôtures prouvées, trois restes actualisés, total exact ; identifiants/libellés et seize lignes déjà terminées conservés |
| `README.md` de soutenance | Index courant et trois verdicts ; anciennes limites explicitement datées pour ne pas les confondre avec l'état présent |
| `BILAN_LOT6H4.md` | Présent rapport et critères de suite |
| `INVENTAIRE_LIVRAISON_LOT6H4.csv` | Sélection préparatoire complète, sans ajout à l'index |
| `preuves-lot6h4/verification.json` | Rapprochements, décisions utilisateur, contrôles finaux et empreintes |
| `preuves-lot6h4/diagrammes/` | Neuf exports source/SVG/PNG et reçu technique ; tous nouveaux, aucun original remplacé |

Phase suivante minimale, **à valider séparément** :

1. **C-02, priorité scolaire** : nommer le détenteur des accès et organiser leur conservation privée ; autoriser ensuite une courte vérification des deux connexions du lancement retenu. Aucun compte permanent à développer.
2. **I-02 et livraison** : obtenir les précisions de Mélissa sur les références/conditions et l'origine du SVG ; décider la destination puis la liste de livraison, y compris les fichiers hérités. Aucun remplacement ou retrait du suivi sans autorisation adaptée.
3. **C-07** : faire valider D01 à D12, finaliser l'information et autoriser seulement ensuite son intégration et ses contrôles ciblés. Garder le brouillon tant que les informations essentielles manquent.
4. **MySQL uniquement si nécessaire pour une exploitation future** : concevoir une recette de migration et reprise sur une cible temporaire synthétique explicitement autorisée, avant tout accès réel. Cela n'est pas requis pour la soutenance SQLite locale.

**Corrections applicatives encore nécessaires démontrées : aucune à ce stade pour ces six remarques.** Les trois défauts de preuve visuelle sont levés ; les trois autres points ne se résolvent pas par de nouvelles fonctionnalités. Si une future vérification révèle un défaut applicatif, le diagnostiquer et obtenir l'autorisation avant de modifier le code.

## 10. Verdicts et arrêt

- **GO — soutenance scolaire locale**, pour les parcours isolés avec données fictives déjà recettés. Les exports actuels permettent les explications d'architecture, BDD et flux. La préparation privée des accès du jour J reste à confirmer ; exposer honnêtement les réserves d'images et de RGPD. Ce verdict n'autorise aucun nouveau serveur ni navigateur du site.
- **NO-GO — commits de livraison de l'ensemble actuel** : inventaire préparé mais sélection/destination et ressources héritées non arbitrées ; aucun commit autorisé ou effectué. La sauvegarde 6H.2 est intacte ; prévoir la conservation durable des deltas avant une opération à risque.
- **NO-GO — ouverture publique** : droits/provenances incomplets, informations et organisation RGPD non validées, exploitation et migrations réelles non recettées. Aucune publication réalisée.

**Bilan final : 19/22, soit 86,36 % arrondi ; C-02, C-07 et I-02 restent PARTIELLES. Arrêt après 6H.4 et attente de la validation utilisateur.**
