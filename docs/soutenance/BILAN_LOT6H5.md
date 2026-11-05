# Lot 6H.5 — trois remarques restantes et préparation des commits

> Archive pédagogique datée : les résultats et descriptions ci-dessous concernent le lot indiqué. Les anciens repères de ligne ne décrivent pas la version candidate. Pour préparer la soutenance actuelle, consulter les quatre fiches et le référentiel reliés au sommaire.

> Copie publique de référence : les chemins personnels et liens de travail internes sont retirés. Les preuves et commandes historiques gardent leur date et leur périmètre ; utiliser le README actuel pour le lancement.

2 novembre 2026. **19/22 remarques TERMINÉES, trois PARTIELLES : C-02, C-07 et I-02.** Aucune nouvelle clôture sans preuve. Calcul exact : **19/22 × 100 = 950/11 % = 86,363636… %, soit 86,36 % arrondi**.

**Soutenance locale : GO dans le périmètre synthétique déjà recetté. Commits Git locaux : GO pour la sélection ciblée préparée de 79 fichiers, à autoriser séparément ; aucun commit effectué. Push GitHub : NO-GO.** L'ouverture publique reste également NO-GO. Le GO local ciblé remplace la réserve globale uniquement pour les trois lots décrits ici ; un ajout global du dossier reste NO-GO.

## 1. Audit initial et préservation

Lecture des [bilans 6H.4](BILAN_LOT6H4.md), [6H.3](BILAN_LOT6H3.md), [6H.2](BILAN_LOT6H2.md), de la [matrice](SUIVI_REMARQUES_JURY.md), du plan Git 6H.1 (pièce interne non diffusée), des instructions et documents pertinents du dépôt. Recherche renouvelée de `AGENTS.md` dans le dépôt et les parents accessibles : aucun trouvé ; aucune absence certifiée dans un emplacement inaccessible. Aucune consigne locale supplémentaire n'est inventée.

| État Git | Initial | Final |
|---|---|---|
| Branche | `feature/frontend-api-integration` | Identique |
| HEAD | `07a9f03ea0a3bdad4a07066fdd7bab1997cc158b` | Identique |
| Suivis / suivis modifiés | 66 / 51 | 66 / 51 |
| Non suivis, comptés individuellement | 122 | 133 |
| Indexés / conflits | 0 / 0 | 0 / 0 |
| SHA-256 index | `cc33bbdc5993495735a8c63e85f22f321b05323716ff29b4af3d0fd8df6c5ec3` | Identique |

Les 188 chemins initiaux sont conservés ; onze fichiers documentaires nouveaux portent l'inventaire à **199 chemins**. Sur les 185 fichiers initiaux hachés, seuls `README.md`, `docs/soutenance/README.md` et `docs/soutenance/SUIVI_REMARQUES_JURY.md` sont retouchés. Trois chemins sensibles restent non ouverts : `frontend/donnees.js`, `frontend/histoires-originales.json`, `docs/soutenance/COMPTES_DEMO.exemple.csv`. Leurs fichiers sont toujours présents.

Aucun code applicatif, modèle, route, test, migration, illustration, manifeste figé ou bilan historique modifié. Aucun compte créé, rôle changé, secret utilisé, serveur/navigateur lancé, opération Git d'écriture, migration ou accès MySQL/Aiven. Les consultations web officielles sont distinctes du site et ne cherchent pas l'auteur du SVG.

## 2. Sauvegarde : état vérifié et delta

Les dossiers privés `portfolio-lot6h2-20261102-55c80c78` et `recuperation-lot6h2-20261102-55c80c78` sous `[chemin local privé retiré]` sont revérifiés en lecture seule : **197 fichiers chacun**, ensembles, tailles et SHA conformes, aucun écart. Reçu final : `9e1c04fb1f5d9c47bd992631b9aaf6815b3531798f3724e649de2e0e511b8fc7`. Les 196 entrées sont vérifiées, ainsi que l'identité des reçus.

Sur les 169 sources sauvegardées, **166 restent identiques** ; les trois écarts sont les trois README/matrice cités ci-dessus. Les 15 nouveaux livrables 6H.3/6H.4 et les onze nouveaux livrables 6H.5 n'appartiennent pas à la source sauvegardée 6H.2. Le fichier de sélection 6H.2 figure dans ses métadonnées ; ne pas le confondre avec une source manquante. Les trois exclusions historiques ne sont pas sauvegardées.

Des copies temporaires vérifiées des trois documents retouchés préservent l'état d'entrée. **Pas de nouvelle sauvegarde durable créée, pas de restauration écrasant le projet.** Prévoir une sauvegarde sélective des deltas avant une future opération à risque, sans remplacer 6H.2. La copie existante ne sauvegarde ni base réelle ni tout l'historique Git ; ce point ne devient pas une obligation de migration ou de publication pour enregistrer des sources localement.

## 3. C-02 — Fichier privé de comptes de démonstration

**PARTIEL → PARTIEL.** Critère exact conservé : détenteur identifié, fiche privée disponible hors Git, accès fictifs membre/admin correspondant au processus utilisé le jour J et vérification de leurs deux connexions. La revue des rôles ne remplace pas l'organisation effective.

La [procédure d'accès 6H.5](PROCEDURE_ACCES_LOT6H5.md) distingue les preuves et les limites :

- Inscription sans élévation de rôle ; hachage du mot de passe ; compte et rôle relus côté serveur.
- CSRF de session pour les écritures concernées ; exemptions login/anonymes distinctes des permissions.
- Bannissement des membres avec refus des sessions ouvertes et des nouvelles connexions ; administrateurs protégés du bannissement.
- Déconnexion du navigateur, sans registre central révoquant toutes les copies du cookie ; Secure dépend de la configuration.
- Kit mémoire : comptes, mots de passe et clé renouvelés à chaque processus ; une ancienne fiche ne prouve pas les accès du prochain lancement.

Preuves : tests historiques `test_admin_users.py`, `test_csrf.py`, `test_proposals_ban.py`, `test_users_votes.py`, HTTP 6H.2 et Edge 6G.5 ; code actuel identique aux empreintes. Aucun nouveau test ne permettrait à lui seul de désigner le détenteur.

La procédure propose un détenteur principal, un support privé, la vérification des deux rôles, le renouvellement après redémarrage et la fin de session. Elle n'invente pas d'interface de promotion/rétrogradation ni de révocation d'un administrateur réel. **Réponse 6H.5 : « Mahamadou ». Le détenteur est désormais désigné.** Le support privé, la règle de renouvellement et les deux connexions du processus retenu ne sont pas encore confirmés ; cette progression ne suffit pas à clore C-02.

**Question simple pour Mahamadou :** sur quel support privé conserve-t-il les accès et comment assure-t-il leur renouvellement ? Puis vérifier les deux connexions dans une recette autorisée, sans publier leurs valeurs. Aucun code à corriger démontré.

## 4. C-07 — Informations RGPD et consentement

**PARTIEL → PARTIEL.** Les notices et leurs contrats existent ; ils ne prouvent pas la validité des informations encore absentes. La réponse 6H.5 confirme le cadre pédagogique, la base isolée et la responsabilité du **projet** portée par Mélissa, Sylvie et Mahamadou ; elle précise expressément que cela ne désigne pas juridiquement le responsable du traitement. Aucun contact RGPD n'est créé ou désigné, aucune ouverture publique prévue. La livraison du code sur GitHub après la soutenance est souhaitée sous réserve de vérifications et autorisations ; dépôt/visibilité restent à préciser.

Le document de propositions et textes 6H.5 (pièce interne non diffusée) propose une voie scolaire simple : rester local et synthétique, sans demander aux visiteurs de vrais comptes. Il prépare les choix de responsable/contact, finalités, bases envisagées par traitement, conservation par événement, hébergement et transferts. Il contient une politique et des notices prêtes à compléter, incluant **Vote et CommentLike**, sans transformer les propositions en faits.

Les décisions incontournables appartiennent à l'équipe et, selon son rôle réel, à l'établissement :

| Question à décider | Repère |
|---|---|
| Qui décide des traitements et accepte d'être identifié ; quel rôle l'école assume-t-elle ? | D01 |
| Quel contact réel sera suivi, par qui, et accessible sans connexion ? | D02/D10 |
| Pourquoi chaque donnée est-elle nécessaire ; quelle base est justifiée pour chaque usage ? | D03/D04 |
| À quelle échéance chaque catégorie est-elle réexaminée/supprimée ; par qui et avec quelle preuve ? | D05/D12 |
| Reste-t-on local ; sinon, quels prestataires, lieux et flux/transferts ? | D06/D11 |
| Quel public, quelles mentions de tiers, quels contenus et devenir des contributions ? | D07/D08 |
| Comment traiter les demandes, l'identité, les anciennes sessions, les incidents et les copies ? | D09 à D12 |

Aucune adresse fictive, identité automatique, durée prétendument légale ou hébergement inventé. Les pistes de bases légales et de conservation sont à valider, pas à appliquer. Les sources officielles sont citées dans le document : [CNIL, bases légales](https://www.cnil.fr/fr/les-bases-legales), [information](https://www.cnil.fr/fr/informer-les-personnes) et [conservation](https://www.cnil.fr/fr/passer-laction/les-durees-de-conservation-des-donnees), consultées le 2 novembre 2026.

**La politique reste un brouillon interne, non publiée sur le site.** Clôture après décisions réelles, textes complets et cohérents puis intégration et contrôles ciblés autorisés. Aucune conformité totale annoncée ; aucune nouvelle fonction RGPD nécessaire démontrée.

## 5. I-02 — Provenance et droits des illustrations

**PARTIEL → PARTIEL.** La [fiche des cinq ressources 6H.5](FICHE_PROVENANCE_IMAGES_LOT6H5.md) rassemble noms, empreintes, origine déclarée, pièces et champs restant à confirmer.

Pour les quatre WebP : Mélissa, ChatGPT et soutenance locale sont déclarés ; dates/contexte de génération et références éventuelles restent inconnus, ce que la réponse détaillée 6H.5 confirme explicitement. Elle confirme aussi l'usage scolaire local uniquement et l'origine du SVG encore à vérifier. Les [conditions européennes OpenAI](https://openai.com/policies/eu-terms-of-use/), affichées au 16 janvier 2026 et relues le 2 novembre, ne constituent pas une preuve des droits de tiers propres aux fichiers. Leur applicabilité au service/compte et à la période doit être établie ; aucune licence libre inventée.

Pour `default-story.svg`, investigation **uniquement locale** : source, documentation et `git log --all --follow` du chemin ; lecture du blob d'introduction. L'ajout est attribué dans Git à `Mahamadou75-19`, commit `e8f8e4c7bd34530cbbb3eb3ec10ec423c8fc0131`, le 24 octobre 2026. Le texte du blob et le fichier actuel sont identiques après normalisation LF. **L'auteur Git de l'ajout n'est pas une preuve de l'auteur créatif.** Ni signature, licence ni origine créative démontrée dans les éléments examinés.

**Questions simples :** Mélissa confirme-t-elle les quatre fichiers et les références fournies ou leur absence ? Quel contexte de génération ? Qui sait comment le SVG a été créé ou obtenu ? L'usage reste-t-il local, ou un partage déterminé est-il souhaité et autorisé ? Une fiche à compléter est fournie sans demander d'accès au compte. Aucun original modifié ou supprimé.

La provenance locale peut être documentée sans inventer une autorisation publique ; une future diffusion nécessite ses propres accords et justificatifs. Aucun remplacement automatique proposé.

Le dossier téléchargé `frontend/images/Reprendre projet portfolio_files`, signalé par l'utilisateur, a été vérifié **par références, règles de service et métadonnées seulement** : présent, 44 fichiers, ignoré, aucun enfant suivi, aucune référence explicite dans les 21 fichiers courants contrôlés, absent du kit et de sa liste publique. Aucun contenu lu ou changé. Une extension image compatible est présente : le lanceur normal autorise les chemins imbriqués `/images/` et pourrait servir ce fichier sur demande directe ; aucune requête n'a été exécutée. Le kit fermé le refuse. Cette réserve conditionnelle doit être examinée avant un usage élargi du lanceur normal ; aucune modification applicative nécessaire au kit scolaire ni suppression proposée. Voir la fiche de provenance pour les limites.

## 6. Fichiers prêts et véritables blocages Git

Le plan 6H.5 et ses commandes non exécutées (pièce interne non diffusée), le manifeste de sélection (pièce interne non diffusée) et l'inventaire complet (pièce interne non diffusée) distinguent les périmètres.

**88 fichiers techniques/de dépendance revus ; 79 changements à indexer, neuf fichiers suivis déjà inchangés.** Trois listes fermées : **46** sources fonctionnelles/candidates de migration ; **30** tests/fixtures et dépendance HTML interne ; **3** fichiers du kit/manifeste/test. Mélissa relit le frontend, Sylvie le backend et Mahamadou les modèles/intégration ; les responsabilités ne permettent pas de forger l'auteur des changements locaux.

Un correctif de préparation est apporté : le brouillon HTML est nécessaire à `tests/test_rgpd_information.py`. Son inclusion **locale interne** est explicite, sans publication de politique. Les autres documents et archives attendent leur sélection propre. Les sept anciennes exclusions de tests de migration et les six essais de candidate likes en mémoire restent documentés ; aucun PASS MySQL annoncé.

| Sujet | Commit local ciblé | Push GitHub / exploitation |
|---|---|---|
| Index/conflits | Index vide, pas de conflit ; aucun blocage Git technique trouvé | À vérifier à nouveau avant opération |
| Secrets/données privées | Listes sans fichiers secrets, base, cookie, session ou temporaire ; trois données non relues exclues des ajouts | Historique complet non audité ; aucun certificat d'absence de secret dans toute l'histoire |
| Images et ancien jeu déjà suivis | Inchangés, restent hérités ; aucun nouvel ajout de ces ressources | Revue des droits/contenus et destination indispensables ; absence de `git add` ne les retire pas du push |
| RGPD | Sources et brouillon de test peuvent être conservés localement, clairement désignés | Pas de politique définitive ni collecte publique autorisée ; diffusion documentaire à revoir |
| Migrations | Sources candidates conservables, sans appliquer ni certifier le déploiement | Schéma réel, historique, reprise DDL et anciens compteurs à traiter avant exploitation MySQL |
| Accès du jury | Ne bloque pas l'enregistrement des sources | Préparation du jour J toujours ouverte |
| Autorisation | Aucune opération Git permise pendant 6H.5 ; sélection concrète désormais soumise à validation suivante | Aucun push autorisé ; destination et visibilité non confirmées |

Le contrôle limité du contenu de la sélection n'a relevé qu'une constante de mot de passe de fixture synthétique, classifiée sans divulguer sa valeur. Aucun autre marqueur de clé privée, jeton fournisseur, JWT, URL SQL authentifiée ou affectation littérale correspondant aux règles contrôlées. Ce contrôle ne garantit pas l'absence absolue de tout secret ou renseignement personnel, ni l'autorisation de diffusion de l'historique. Aucun hook non `.sample` ni chemin de hooks personnalisé trouvé ; aucun hook exécuté.

**Le NO-GO global 6H.4 n'était pas une impossibilité de commettre localement.** Les éléments publics non résolus ne sont plus utilisés pour bloquer artificiellement la sélection locale bornée. Le prochain lot peut autoriser précisément les trois commits locaux, sans push ni publication. Un ajout global demeure exclu.

## 7. Contrôles exécutés et corrections documentaires

Contrôles limités à Git en lecture seule, empreintes, analyse de texte/AST et liens de fichiers déterminés ; bibliothèque standard Python en mode isolé, sans import applicatif ou découverte de tests. Les 854 tests ne sont pas relancés : **76/76 empreintes brutes** de leur manifeste et **40/40 empreintes LF** du kit toujours conformes. Les preuves de rendu 6H.4 restent valides et ne sont pas refaites.

Le reçu 6H.5 (pièce interne non diffusée) conserve sauvegarde, état initial/final, sélection, exclusions, rapprochement des preuves, contrôles de conservation et limites. `git diff --check` : code 2, **164 avertissements CRLF préexistants** dans les deux mêmes fichiers ; contrôle avec `-c core.whitespace=cr-at-eol` pour cette seule commande : code 0. Aucune configuration ou fin de ligne applicative changée.

| Livrable / retouche | Justification |
|---|---|
| Procédure d'accès 6H.5 | Organisation simple, droits, révocation et fiche sans secret ; critère C-02 conservé |
| Propositions RGPD et textes à compléter | Choix discutables séparés des faits, douze décisions et brouillon incluant CommentLike |
| Fiche de provenance | Cinq fichiers, déclaration Mélissa et trace Git du SVG sans attribution abusive |
| Plan, manifeste et trois listes de commits | Sélection locale concrète, dépendance du test RGPD, commandes préparées sans exécution |
| Inventaire 6H.5 | 199 chemins classés ; aucun fichier hérité ou non suivi oublié |
| Bilan et reçu | Résultats, limites, preuves et trois verdicts distincts |
| README principal, index soutenance, matrice | Navigation courante, trois points encore partiels, séparation local/push ; 22 libellés et 19 lignes déjà terminées conservés |

## 8. Prochaines actions minimales et verdicts

1. **Pour C-02** : faire confirmer à Mahamadou le support privé et le renouvellement, puis vérifier les deux accès du lancement retenu lors d'une recette autorisée. Ne pas développer de gestion de rôles supplémentaire pour satisfaire ce critère.
2. **Pour I-02** : compléter les cinq fiches et conserver le dossier téléchargé hors sélection, notamment références des WebP et origine du SVG ; décider séparément d'un partage GitHub ou public.
3. **Pour C-07** : faire valider les propositions par les personnes réellement responsables, compléter les textes puis autoriser leur intégration. Maintenir le brouillon en attendant.
4. **Pour les commits locaux** : valider la sélection 79 chemins et autoriser précisément les trois lots. Revérifier empreintes/index et conserver les autres travaux ; aucun besoin de forcer 22/22 ou de migrer MySQL pour cela.
5. **Pour un push ultérieur** : confirmer destination/visibilité et revoir l'arbre/historique transmis, les ressources héritées et les documents personnels/internes. Aucun push ne découle d'un accord de commit local.

**GO — soutenance locale** avec données synthétiques et parcours déjà recettés ; accès du jour J à organiser, réserves documentées. Aucun nouveau lancement autorisé par ce bilan.

**GO — préparation des trois commits Git locaux ciblés**, 79 chemins et dépendances décrits. Exécution interdite pendant ce lot et soumise à validation suivante ; **NO-GO pour un ajout global**.

**NO-GO — push GitHub**, y compris vers une destination privée non encore approuvée. Ouverture publique également non validée.

**19/22, 86,36 % ; trois PARTIELLES maintenues sans clôture artificielle. Arrêt après 6H.5, en attente de validation.**
