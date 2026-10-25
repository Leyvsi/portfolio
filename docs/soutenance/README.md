# Soutenance — Les Petits Enquêteurs

Ces quatre fiches permettent de réviser les questions du jury avec des réponses courtes, des explications simples et des exemples tirés du projet. Elles sont destinées à un niveau bac. Le présent README est un index de navigation : **ce n’est pas une cinquième fiche de questions**.

## Sommaire

- [Choisir sa fiche](#choisir-sa-fiche)
- [Origine et intégrité](#origine-et-intégrité)
- [Comment réviser](#comment-réviser)
- [Portée des validations](#portée-des-validations)
- [Limites à connaître](#limites-à-connaître)
- [Petit glossaire Git](#petit-glossaire-git)
- [Documentation technique](#documentation-technique)

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

**Portée des preuves :** les résultats de tests et de rendu Mermaid sont historiques. Aucun test fonctionnel, rendu de diagramme, serveur, migration ou accès Aiven n’est exécuté pendant cette préparation. Les droits des illustrations restent à confirmer.

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

Les **439 tests réussis** — 205 backend, 226 frontend et 8 lanceur — sont une preuve historique rapportée dans le [README principal](../../README.md#tests-et-validation). Ils n’ont pas été relancés. Les tests SQLite et les simulations DOM/API ne valident pas à eux seuls MySQL Aiven, un navigateur réel, les migrations déployées ou une installation vierge complète.

Les diagrammes approuvés ont été validés antérieurement avec Mermaid 11.16.0 : syntaxe, navigateur local et XML des SVG. Leur réutilisation dans les fiches ne constitue pas une nouvelle exécution de ces contrôles. L’affichage Mermaid sur GitHub reste non vérifié.

La [PR #16](https://github.com/Leyvsi/portfolio/pull/16) était ouverte en Draft et non fusionnée lors de la lecture autorisée de l’étape 15.8.1, le 25 octobre 2026. Son état n’est pas relu pendant la création locale de ces documents.

## Limites à connaître

- Administration limitée à la consultation : aucune action de publication, suppression ou modération dans le tableau.
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

L’archive narrative locale `frontend/histoires-originales.json` reste exclue du suivi Git et de ces documents.
