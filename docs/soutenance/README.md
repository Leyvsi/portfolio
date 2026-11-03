# Soutenance — Les Petits Enquêteurs

> Etat de diffusion scolaire du 3 novembre 2026 : suivre le [guide actuel](../../LIVRAISON_SCOLAIRE.md) et la [validation scolaire](VALIDATION_SCOLAIRE.md). Les sections de campagnes anterieures et leurs commandes sont historiques ; elles ne remplacent pas la procedure actuelle. Les chemins sous `C:\chemin\utilisateur` sont des exemples anonymises. Les archives internes signalees sont conservees localement.

Ces quatre fiches conservent les questions historiques de l’équipe. Les supports actualisés du 29 octobre 2026 ci-dessous complètent leur préparation pour une première année Holberton. Le présent README reste un index de navigation.

## Sommaire

Lot courant du 2 novembre 2026 : bilan 6H.5 (archive interne non livree), [matrice](SUIVI_REMARQUES_JURY.md), [procédure d'accès](PROCEDURE_ACCES_LOT6H5.md), propositions RGPD internes (archive interne non livree), [fiche de provenance](PROVENANCE_RESSOURCES.md), plan de commits locaux (archive interne non livree), inventaire (archive interne non livree) et preuves (archive interne non livree). **19/22 terminées (86,36 %), C-02/C-07/I-02 PARTIELLES. GO scolaire local ; GO pour les trois commits locaux ciblés préparés, à autoriser séparément ; NO-GO push GitHub et ouverture publique.** Aucun commit, lancement ou publication pendant ce lot ; ajout global toujours exclu. Les rendus et clôtures 6H.4 (archive interne non livree), l'audit 6H.3 (archive interne non livree) et la sauvegarde 6H.2 (archive interne non livree) restent des preuves historiques conservées.

- [Choisir sa fiche](#choisir-sa-fiche)
- [Origine et intégrité](#origine-et-intégrité)
- [Comment réviser](#comment-réviser)
- [Portée des validations](#portée-des-validations)
- [Limites à connaître](#limites-à-connaître)
- [Petit glossaire Git](#petit-glossaire-git)
- [Documentation technique](#documentation-technique)

## Supports actualisés du 29 octobre 2026

| Support | Usage |
|---|---|
| [Tests et validation](TESTS_ET_VALIDATION.md) | Types, fichiers, assertions, outils/versions, commandes et preuves séparées des étapes 2/3/4. |
| [Architecture, sécurité et RGPD](ARCHITECTURE_SECURITE_RGPD.md) | DOM, WSGI, flux, données, exceptions CSRF et fonctions manquantes. |
| Index du code pour le jury (archive interne non livree) | Noms exacts, lignes après commentaires, liens GitHub et explications courtes. |
| [Fiche de démonstration](DEMONSTRATION.md) | Démarrage, adresses, parcours, limites et modèle de comptes fictifs. |
| [Réponses orales](ORAL_JURY.md) | Vingt et une questions ciblées, répartition par membre et réponse de Mahamadou sur la persistance. |
| Bilan de l'étape 5 (archive interne non livree) | Fichiers modifiés, contrôles statiques et réserves. |
| [Suivi des remarques du jury](SUIVI_REMARQUES_JURY.md) | Matrice exhaustive : membres, fichiers, acquis, corrections restantes et contrôles futurs. |
| Bilan de l'étape 5.1 (archive interne non livree) | Commentaires complétés, sources Mermaid ajustées et contrôles statiques locaux. |
| Lot 6A : utilisateurs et bannissement (archive interne non livree) | Parcours livré, deux routes centralisées, comptes protégés et 487 tests isolés réussis. |
| Lot 6B : consultation des dossiers (archive interne non livree) | Liste, recherche, filtres et fiches ; API réutilisées et 533 tests isolés réussis. |
| Lot 6D : statistiques administrateur (archive interne non livree) | Sept compteurs, API privée réutilisée, 561 tests isolés réussis ; recette navigateur reportée. |
| Lot 6C : audit et conception (archive interne non livree) | Relations, signalements, trois stratégies, contrats envisagés et tests à prévoir ; aucun développement ni suppression. |
| Lot 6C phase 1 : archivage réversible (archive interne non livree) | Archivage/restauration développés et testés hors ligne ; migration non déployée, suppression définitive restante. |
| Lot 6C.2 : conception finale de la suppression (archive interne non livree) | Audit documentaire uniquement ; algorithme, reports relationnels, confirmation, reçu et plan de tests proposés ; NO-GO actuel avant décisions et autorisation de développement. |
| Lot 6C.2 : proposition de décisions finales (archive interne non livree) | Dix règles validées ; vérifications ciblées, contrat et reprise précisés, reçu minimal proposé à 30 jours ; deux arbitrages et autorisation d’implémentation encore attendus. |
| Lot 6C.2 : condition S1 et solution S2 simplifiée (archive interne non livree) | S1 non confirmée au niveau du modèle ; option de restriction aux commentaires à approuver. S2 accepté : aucun reçu persistant. Implémentation arrêtée avant modification applicative. |
| Lot 6C.2 : implémentation autorisée (archive interne non livree) | S1 désormais validée : Report limité aux commentaires ; purge conditionnelle des archives, sans reçu persistant. 657 tests isolés réussis ; migration réelle et validation MySQL restent non exécutées. |

**État historique 5.1, remplacé pour les rendus par le bilan 6H.4 :** les sources de l'architecture et du flux ont été ajustées, sans nouveau rendu. Les deux défauts visuels restent à confirmer comme corrigés. Le diagramme BDD reste identique à son rendu historique validé. Les repères actualisés complètent les fiches historiques.

## Choisir sa fiche

| Fiche | Responsabilité déclarée par l’équipe | Identifiants | Questions |
|---|---|---|---:|
| [Mahamadou — Base de données et intégration](fiche-mahamadou.md) | MySQL, SQLAlchemy, base de données et intégration | MAH-01 à MAH-18 | 18 |
| [Mélissa — Frontend](fiche-melissa.md) | HTML, CSS, JavaScript et expérience utilisateur | MEL-01 à MEL-18 | 18 |
| [Sylvie — Backend Flask et API](fiche-sylvie.md) | Routes, sécurité, authentification et permissions | SYL-01 à SYL-18 | 18 |
| [Fiche commune](fiche-commune.md) | Architecture, démonstration, limites et organisation | COM-01 à COM-22 | 22 |
| **Total** | **Quatre fiches historiques** | | **76** |

La répartition reprend les déclarations de l’équipe. Elle n’attribue pas chaque fichier ou correction à une personne : chacun doit confirmer ses contributions personnelles.

## Origine et intégrité

Questions-réponses historiques récupérées de la réponse Codex de l’étape 15.1 du **25 octobre 2026**, fondée sur le commit `dec5c7ef4c753970bd94014b37b59b035e1877f1`. Audit de référence : étape 15.8.1 ; préparation documentaire : étape 15.8.2, au commit `857190654457b15d7324adde8c920d9fdd3db0c8`.

Les formulations des questions et des réponses courtes originales sont conservées. Les explications, exemples, identifiants de repérage et références facilitent la révision. **VALIDÉE** signifie conforme aux sources ; ce statut ne constitue pas une validation en production.

Empreinte SHA-256 du texte historique complet : `218cf13b814a1f20a4258f1f6b24ab600b296bc62baab1c23610a36905ace4cd`.

**Portée historique :** cette indication concernait la préparation initiale des fiches. Les résultats plus récents sont dans les supports actualisés ci-dessus. L’étape 5 reste documentaire : aucune campagne fonctionnelle, base, migration ni connexion Aiven ; le contrôle des diagrammes est local. Les droits des illustrations restent à confirmer.

La réponse historique est conservée dans le journal local de la conversation Codex. Ce journal privé n’est pas publié avec les fiches. Son texte comporte les quatre fiches ; les deux représentations identiques du même message ont été comptées une seule fois lors de la récupération.

Les séries historiques conservent **18 + 18 + 18 + 22 questions**, sans ajout ni doublon exact. Les identifiants de repérage MAH, MEL, SYL et COM correspondent à la numérotation retrouvée lors de l’audit 15.8.1.

Les passages d’accompagnement ont été actualisés : les trois diagrammes viennent du README approuvé et les 14 liens Windows absolus d’origine sont devenus des liens relatifs. Les explications et exemples complètent les réponses courtes ; ils ne les remplacent pas.

## Comment réviser

1. Lire les repères de sa fiche, puis les questions communes.
2. Dire la réponse courte à voix haute, sans apprendre uniquement une formule.
3. Utiliser l’explication simple pour comprendre le raisonnement.
4. Montrer l’exemple et retrouver le fichier cité.
5. Préciser ce qui est vérifié dans les sources, historique, partiel ou non vérifié.

Chaque question utilise les mêmes rubriques : **Question du jury**, **Réponse courte à dire**, **Explication simple**, **Exemple concret**, **Référence technique** et **Statut de validation**.

Les liens techniques pointent vers les sources du dépôt. Les numéros de ligne correspondent au commit de référence et peuvent évoluer ensuite.

## Portée des validations

| Mention | Ce qu’elle signifie |
|---|---|
| **VALIDÉE** | La formulation est conforme au code ou à la documentation examinés. Elle ne prouve pas une exécution en production. |
| **Preuve historique** | Le résultat vient d’une campagne antérieure, sans nouvelle exécution pendant cette préparation. |
| **Partiellement implémenté** | Une partie du parcours existe, mais pas l’ensemble des fonctions envisagées. |
| **NON CONFIRMÉE** | Une preuve ou une décision de l’équipe manque. |
| **Non vérifié** | Le contrôle réel n’a pas été effectué dans ce périmètre. |

**75 réponses sont validées.** [COM-21](fiche-commune.md#com-21) conserve une **priorité proposée, à confirmer par l’équipe**. Ce classement ne signale pas une erreur technique ; il distingue une suggestion d’une décision confirmée.

Les **439 tests réussis** — 205 backend, 226 frontend et 8 lanceur — ont été réexécutés le 29 octobre 2026, après la préparation historique des fiches. La recette Edge (28/2/0/7) et la persistance SQLite (dix BDD PASS ; bilan consolidé 15/1/0/1) restent des campagnes distinctes. Voir [les preuves et commandes](TESTS_ET_VALIDATION.md). Aucun accès Aiven ni migration exécutée ; aucun test fonctionnel relancé pendant l’étape documentaire 5.

Les diagrammes ont été simplifiés et synchronisés avec le README le 29 octobre ; le bilan (archive interne non livree) distingue leur contrôle local actuel de la preuve historique du 25 octobre. Le rendu sur GitHub reste non attesté.

La [PR #16](https://github.com/Leyvsi/portfolio/pull/16) était ouverte en Draft et non fusionnée lors de la lecture autorisée de l’étape 15.8.1, le 25 octobre 2026. Son état n’est pas relu pendant la création locale de ces documents.

## Limites à connaître

**Liste historique de l’étape 5 : plusieurs fonctions et l’installation ont été livrées ensuite. Pour les limites actuelles, consulter le bilan 6H.4 (archive interne non livree) ; les sections chronologiques ci-dessous conservent les étapes intermédiaires.**

- Administration : consultation, bannissement et archivage/restauration ; publication, suppression définitive et traitement des propositions restent absents.
- Propositions enregistrées en `pending`, sans transformation automatique en histoire.
- Pas d’interface pour commenter, voter, liker, signaler ou bannir, même si des routes existent.
- Actualisation manuelle du lecteur après création d’une théorie.
- Catégories dépendantes des identifiants `1` et `2`.
- Listes sans pagination, aucune récupération de mot de passe et aucun téléchargement d’image dans les propositions.
- Installation et données de démonstration non validées de bout en bout sur une base vierge.
- MySQL/Aiven, TLS réel et révision Alembic déployée non vérifiés dans cet audit.
- Droits et provenance des illustrations non confirmés.
- Les 332 alertes historiques de `git diff --check` sur `frontend/styles.css` sont liées aux CRLF enregistrés ; aucune correction CSS n’est comprise ici.

La démonstration nécessite un environnement préparé et explicitement autorisé, avec des données fictives et des comptes adaptés. Elle ne doit pas improviser une migration ou une écriture sur une base distante.

## Petit glossaire Git

Cet encadré complète les fiches et **ne fait pas partie des 76 questions historiques**.

| Terme | Explication simple |
|---|---|
| **Branche** | Une ligne de travail qui permet de préparer des changements avant leur intégration à la branche principale. |
| **Commit** | Un enregistrement versionné d’un état du projet, identifié par une empreinte et accompagné d’un message. |
| **Pull Request** | Une proposition d’intégration d’une branche dans une autre, avec un espace pour examiner le diff et discuter des changements. |
| **Draft** | Une Pull Request encore en préparation. Elle permet de partager le travail et les réserves avant de demander son passage en revue finale. |

Créer une PR ne fusionne pas les branches. Ajouter un commit à sa branche source publiée peut compléter le contenu de cette PR ; toute publication reste soumise aux autorisations prévues.

## Documentation technique

- [README principal](../../README.md)
- [README frontend](../../frontend/README.md)
- [Images et droits](../../frontend/images/README.md)
- [Modèles SQLAlchemy](../../backend/models.py)
- [Routes API](../../backend/api/v1/views/)
- [Lanceur local](../../run_local.py)

L’archive narrative locale `frontend/histoires-originales.json` reste non suivie et exclue de la sélection proposée ; elle n’est pas ignorée par les règles actuelles. Aucun contenu n’a été ouvert pour ce lot.

## Préparation RGPD — lot 6E.1

**Brouillons internes non publiés sur le site ; aucune conformité déclarée et aucune fonction d'effacement de compte développée.**

- Bilan, sauvegarde vérifiée et limites (archive interne non livree)
- Décisions à valider avec l'équipe (archive interne non livree)
- Brouillon de politique de confidentialité (archive interne non livree)
- Brouillons des notices de collecte et publication (archive interne non livree)
- Procédures manuelles : identité, accès, rectification, effacement (archive interne non livree)
- Conséquences d'un éventuel effacement de compte (archive interne non livree)

## Information RGPD — lot 6E.2

Trois notices provisoires sont intégrées aux formulaires existants ; aucun lien public vers la politique inachevée, aucune nouvelle API, bannière, migration ou fonction RGPD du dashboard.

## Vérification technique — lot 6E.3

Bilan 6E.3 : tests, douze décisions et scénario complet (archive interne non livree).

**659 PASS exécutés : 279 backend, 364 frontend, 16 lanceur.** Sept cas de migration volontairement non exécutés, sans changement des tests historiques. Parcours commentaire/signalement/administration prouvé via API et SQLite mémoire ; formulaires publics de commentaire/signalement absents. Aucun code applicatif, donnée réelle ou politique publiée modifié.

## Commentaires et signalements publics — lot 6F.1

Bilan 6F.1 : interface, contrats, protections, tests et limites (archive interne non livree).

**723 PASS exécutés : 279 backend, 428 frontend, 16 lanceur.** Les 659 de 6E.3 restent historiques. Formulaires publics maintenant intégrés dans la fiche commune aux histoires et Cold Cases, avec session, CSRF, cible vérifiée, notices, doubles clics bloqués et résultats incertains explicites. Backend et dashboard inchangés ; aucune migration, donnée réelle ou publication de politique incomplète. Recette navigateur et MySQL/Aiven non exécutées.

## Recette fonctionnelle et soutenance — lot 6F.2

- Bilan : audit, preuves intégrées, limites et autorisations restantes (archive interne non livree).
- Protocole manuel Edge et kit isolé — lancement soumis à autorisation distincte (archive interne non livree).
- Scénario de 14 minutes : Mélissa, Sylvie et Mahamadou (archive interne non livree).

**723 PASS réexécutés**, plus une vérification intégrée de 42 requêtes réelles vers Flask/SQLite mémoire depuis les contrôleurs frontend et un DOM simulé. Les sept compteurs affichés correspondent aux requêtes SQL. Kit inspecté READY sans écoute réseau. Aucun code applicatif modifié, serveur ou navigateur lancé. Le script historique donnees.js reste exclu ; aucune couverture de tous les scripts des pages de compte ou recette Edge n'est revendiquée.

## Conception des likes — lot 6G.1

Bilan 6G.1 : routes existantes, modèles, historique et plan 6G.2 (archive interne non livree). Vote convient aux histoires/Cold Cases ; état personnel et retrait à ajouter. Les commentaires nécessitent une relation individuelle et un arbitrage des anciens compteurs non attribuables. Conception uniquement ; **723 PASS de 6F.2 restent historiques**, sans réexécution. Implémentation en attente d'autorisation.

## Likes individuels — lot 6G.2

Bilan 6G.2 : développement, migration candidate, protections et résultats (archive interne non livree). Histoires/Cold Cases via Vote conservé ; commentaires via CommentLike sur compteurs historiques compatibles. Ajout/retrait personnel, unicité, CSRF, état et compteurs serveur, protection des données historiques et purge interne adaptée. **803 PASS exécutés : 303 backend, 484 frontend, 16 lanceur**, plus un parcours intégré sans réseau de 79 requêtes. Aucun navigateur ou MySQL validé, aucune migration réelle ; sept tests de migration historiques toujours exclus.

## Préparation finale de recette — lot 6G.4

Audit 6G.3 (archive interne non livree), bilan des corrections 6G.4 (archive interne non livree) et [nouveau protocole manuel](RECETTE_MANUELLE_LOT6G4.md). Kit isolé actualisé, `likes.js` servi, cinq chargements historiques inutilisés retirés. Le fichier `donnees.js` et le kit 6F.2 sont conservés. Serveur et Edge restent arrêtés ; leur lancement exige une autorisation distincte.

## Recette Edge et corrections autorisées — lot 6G.5

Bilan historique de la recette partielle (archive interne non livree) : vrais échanges Edge/Flask/SQLite temporaire, avec NO-GO initial conservé. Correctifs autorisés et contre-recette finale (archive interne non livree) : affichage partagé du compte, contexte des signalements et cache local explicite. **854 PASS réexécutés**, plus 17 groupes intégrés sans navigateur. Affichages, likes après actualisation, sept compteurs et déconnexion confirmés dans Edge puis rapprochés de SQL. **GO pour la démonstration locale isolée des parcours recettés** ; serveur arrêté, preuves conservées. Les limites de migration et de déploiement restent distinctes.

## Audit final et préparation Git — lot 6H.1

Rapport 6H.1 (archive interne non livree) · [22 remarques et pourcentage](SUIVI_REMARQUES_JURY.md) · [Présentation par étudiant](SUPPORT_JURY_LOT6H1.md) · [Index courant](INDEX_CODE_LOT6H1.md) · [Procédure autre PC](../../LIVRAISON_SCOLAIRE.md) · Plan de commits et sauvegarde (archive interne non livree) · Inventaire CSV (archive interne non livree). Aucun code applicatif ni test fonctionnel modifié ou exécuté.
