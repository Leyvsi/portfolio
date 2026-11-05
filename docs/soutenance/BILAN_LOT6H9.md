# Lot 6H.9 — résolution du blocage GitHub

> Archive pédagogique datée : les résultats et descriptions ci-dessous concernent le lot indiqué. Les anciens repères de ligne ne décrivent pas la version candidate. Pour préparer la soutenance actuelle, consulter les quatre fiches et le référentiel reliés au sommaire.

> Copie publique de référence : les chemins personnels et liens de travail internes sont retirés. Les preuves et commandes historiques gardent leur date et leur périmètre ; utiliser le README actuel pour le lancement.

3 novembre 2026. **NO-GO pour le push.** Le diagnostic et la sélection documentaire ont progressé, mais aucune preuve ne permet d'affirmer que les deux anciens accès sont révoqués ou n'ont jamais été utilisables hors d'un test jetable. Aucun commit, push, changement de branche, réécriture d'historique ou connexion avec ces accès.

Le [bilan 6H.8](BILAN_LOT6H8.md) est repris. Les sources applicatives et les travaux de l'équipe sont conservés. La nouvelle réponse utilisateur confirme l'abandon de l'ancien code et l'intention de ne pas réutiliser les accès ; elle confirme aussi que les ordinateurs d'exécution et l'utilisation éventuelle sur une base réelle restent inconnus. **Une intention de non-réutilisation n'est pas une preuve de désactivation.**

## 1. Diagnostic précis des deux anciens accès

Les deux entrées sont désignées ici **A1 et A2**, simples repères de revue dans l'ordre de l'ancienne liste. Ce ne sont pas leurs identifiants. Aucune valeur, capture, copie de mot de passe ou empreinte individuelle de mot de passe n'est conservée dans ce lot.

| Question | A1 et A2 : constat vérifiable |
|---|---|
| Nature | Deux couples username/password littéraux dans `admins_to_create`, utilisés pour créer des `User` administrateurs si absents |
| Fichier | `backend/index.py`, lignes 24 et 25 des deux versions historiques identifiées |
| Mécanisme | `create_all`, `User(is_admin=True)`, hachage du mot de passe, ajout puis commit SQL |
| Base déclarée | `sqlite:///site.db`, donc un fichier persistant prévu, et non SQLite `:memory:` |
| Exposition réseau prévue | Ancien lancement déclaré sur `0.0.0.0` ; ce code ne prouve ni qu'il a été lancé ni qu'un service était accessible depuis Internet |
| Description fictive | Aucun commentaire de ces sources ne désigne la liste comme comptes fictifs réservés à un environnement de test isolé |
| Utilisation effective | Inconnue ; aucune connexion ni base réelle consultée |
| Révocation/rotation | Aucune preuve disponible |
| Version actuelle | Ces deux valeurs et leur création automatique ont disparu du code actuel ; le kit actuel génère séparément des accès synthétiques éphémères |

Les deux blobs examinés contiennent **les mêmes deux couples**, et non quatre accès différents. L'analyse AST s'effectue sans exécution du code ; les valeurs restent uniquement en mémoire le temps de comparer et d'expurger les métadonnées. Diagnostic sans valeurs (pièce interne non diffusée).

### Chronologie Git et présence publique

Dates ci-dessous : métadonnées Git, sans prétendre identifier une date d'exécution du programme.

| Commit | Date Git | Effet constaté dans `backend/index.py` |
|---|---|---|
| `e933825fb31e632628de388cf7bcfc5eb160f34f` | 15 juillet 2026, 13:46 +02:00 | Introduction ; les couples ne sont pas présents dans la version parente examinée |
| `63934be65c4aab924f2273c5cf4ee85c6938c210` | 15 juillet 2026, 14:38 +02:00 | Modification du fichier ; les deux couples sont conservés |
| `c26b1b1adee4ed0a27041174c6b0d3a632898e34` | 15 juillet 2026, 14:50 +02:00 | Les mêmes accès restent dans l'arbre de ce commit, sans nouvelle modification de leur fichier |
| `66ffe4b14c1e9996914caa74437e2ff665920cbe` | 23 septembre 2026, 12:48 +02:00 | Retrait des valeurs de la source pendant le changement d'intégration ; aucune preuve de suppression des comptes ou de rotation |

Dans les arbres accessibles depuis le HEAD actuel, les **deux blobs connus apparaissent dans un seul chemin et trois commits**, tous ancêtres du HEAD distant revérifié. Le périmètre est celui de cette branche et des objets déjà signalés, pas une nouvelle recherche de tous les secrets possibles dans toutes les branches ou bases externes.

Le dépôt [Leyvsi/portfolio](https://github.com/Leyvsi/portfolio) est **public** ; la branche distante ciblée pointe toujours sur `07a9f03ea0a3bdad4a07066fdd7bab1997cc158b`. Ces trois commits sont donc **déjà dans l'histoire publiée**, pas uniquement dans les quatre commits locaux récents. Leur omission d'un futur ajout Git ne retire pas cette exposition. Consultation GitHub en lecture seule (pièce interne non diffusée).

Les premiers changements portent l'étiquette d'auteur Git `leyvsi`. Le retrait porte `Mahamadou75-19`. Ces étiquettes permettent de demander du contexte aux personnes concernées ; elles ne prouvent pas qui a exécuté le code, détenu les machines ou administré les comptes. L'utilisateur l'a expressément rappelé.

## 2. Vérifications à confier à l'équipe

**Coordination proposée à Mahamadou**, déjà désigné pour les accès et responsable déclaré de l'intégration/BDD ; **relecture proposée à Sylvie** pour les anciens points d'entrée Flask et les modes de lancement. La personne liée à l'auteur Git `leyvsi` constitue une autre piste de contexte. Ces rôles proposés ne sont pas une désignation confirmée du détenteur des anciennes machines.

Seul le détenteur ou administrateur effectivement autorisé de chaque environnement peut attester ce qui s'y est passé. Pour chaque machine ou service pertinent, relever sans secret :

1. Qui possédait l'environnement et qui peut en attester l'utilisation ; période et version du code employée.
2. Si ces versions ont été lancées, quelle configuration de base était réellement utilisée, et si le fichier SQLite ou ses copies ont subsisté. Ne pas supposer qu'un fichier persistant était isolé parce que le projet était scolaire.
3. Si les comptes A1/A2 ont été créés, migrés, restaurés, copiés ou réutilisés sur une autre application. Une migration ultérieure du code vers MySQL ne prouve ni transfert ni absence de transfert des comptes.
4. Si un environnement correspondant existe encore et reste accessible ; si l'ancien lancement pourrait recréer un compte devenu absent.
5. Quelle action documentée empêche désormais l'utilisation des accès, et quelle personne l'a vérifiée par un accès administratif légitime.

Ne pas tenter une connexion avec les anciennes valeurs pour « voir si elles marchent ». Ne pas envoyer de mot de passe, cookie, jeton, dump, identifiant de connexion ou capture contenant ces éléments dans le chat ou Git. Il n'est pas demandé de fournir un export complet d'une machine.

### Critères pour lever la réserve

| Situation établie | Élément recevable pour l'examen final |
|---|---|
| Comptes exclusivement jetables, sans réutilisation | Vérification datée et attribuée, périmètre connu, contexte d'exécution et éléments concordants démontrant l'isolement et l'absence d'accès subsistant ; pas une simple affirmation générale |
| Comptes utilisés ou réutilisation possible | Preuve expurgée de leur désactivation/rotation sur chaque environnement identifié, traitement des sessions concernées et prévention de leur recréation |
| Ancien environnement définitivement hors service | Constat documenté du détenteur sur son inaccessibilité et ses copies/restaurations pertinentes, avec examen de toute réutilisation des valeurs |
| Environnements ou statut toujours inconnus | **NO-GO maintenu** ; ne pas transformer une absence de souvenir ou de journal en preuve de non-utilisation |

Une attestation utile contient : responsable effectif, date, périmètre vérifié, méthode, résultat pour A1/A2, action éventuelle, référence d'une preuve privée expurgée et limites encore inconnues. Ces champs sont à compléter après vérification, pas à préremplir comme acquis. La dernière réponse utilisateur ne désigne pas encore une personne capable d'attester tous les environnements.

## 3. Instructions de sécurisation, à exécuter uniquement par un responsable autorisé

1. **Délimiter l'intervention** avec le détenteur de la machine/base. Préserver les données et sauvegardes utiles ; ne pas effacer `site.db` ou des comptes pour contourner la vérification.
2. **Empêcher la recréation** par les anciens points d'entrée : retirer leur usage opérationnel dans le périmètre approuvé. Laisser des copies historiques hors exploitation n'est pas une autorisation de les relancer.
3. **Désactiver ou renouveler les comptes concernés** via une procédure de maintenance validée, avec des valeurs nouvelles, uniques et privées. Vérifier aussi les éventuelles réutilisations sur d'autres services identifiés. Ne pas improviser une requête SQL sur une cible supposée.
4. **Traiter les sessions séparément.** Changer un mot de passe ne prouve pas l'invalidation de cookies déjà émis. Le bannissement via l'interface actuelle refuse les administrateurs ; cette interface ne constitue donc pas une procédure universelle de révocation de ces anciens comptes. Une éventuelle invalidation globale de sessions doit être préparée avec son impact et autorisée pour la cible réelle.
5. **Vérifier par l'accès administratif légitime et les contrôles disponibles**, sans tester les anciens mots de passe, puis conserver le reçu expurgé. Vérifier qu'une restauration ou un ancien script ne réintroduira pas l'accès.

Ce sont des instructions préparatoires, **aucune intervention réelle n'a été exécutée ou nouvellement autorisée dans 6H.9**. GitHub recommande de commencer par révoquer/renouveler un secret exposé ; cela peut rendre inutile une réécriture d'histoire. Celle-ci présente des risques pour les clones et les travaux des collaborateurs. [Documentation GitHub](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository).

La disparition du secret dans HEAD, un dépôt devenu privé ou un nouveau commit ne remplace pas sa révocation. Aucune commande de réécriture, force push ou suppression n'est préparée comme étape automatique.

## 4. Sélection arrêtée des fichiers livrables

Le périmètre des **233 fichiers de 6H.8** est entièrement repris dans CLASSEMENT_LOT6H9.csv (pièce interne non diffusée). Les onze livrables d'audit 6H.8 apparus ensuite restent locaux. L'état initial 6H.9 comprend ainsi **244 fichiers : 103 suivis et 141 non suivis**, dont huit suivis modifiés.

| Décision sur les 233 fichiers | Nombre |
|---|---:|
| Conserver la version déjà dans HEAD | 89 |
| Retenir une version documentaire préparée | 28 |
| Conserver uniquement en local | 110 |
| Suspendre la décision de diffusion des ressources déjà suivies | 6 |
| **Total** | **233** |

**Les choix de chemins sont arrêtés ; la publication n'est pas autorisée.** La liste contient 117 chemins retenus parmi les 233, plus un nouveau résumé de validation : **118 fichiers retenus hors des six ressources suspendues**. Avec ces six ressources actuellement héritées, l'arbre envisagé comporterait **124 chemins**. On ne peut pas annoncer une sélection intégralement approuvée tant que leurs justificatifs/décisions manquent.

Le manifeste définitif de préparation (pièce interne non diffusée) donne les chemins complets, le HEAD de référence, les décisions, les empreintes des originaux et des copies destinées à la publication. Il ne s'agit pas d'une liste permettant de retirer silencieusement les six ressources de l'histoire : elles restent actuellement suivies.

### Sources et tests

Le code frontend/backend, modèles SQLAlchemy, sept migrations candidates, sécurité, fonctions et kit sont déjà dans les quatre commits locaux. Aucun fichier applicatif indispensable au parcours recetté n'est absent. **34 fichiers de tests/fixtures** restent suivis : 17 sous `backend/tests`, 14 sous `frontend/tests`, trois sous `tests`. Le brouillon HTML RGPD reste conservé parce que le test correspondant en dépend, explicitement hors politique publique.

Le kit, son manifeste et son test sont conservés ensemble. Les scripts ponctuels de sauvegarde, d'installation historique, d'audit, de commit et l'ancien kit 6F.2 restent locaux. Le guide courant permet la reproduction avec les dépendances externes prévues, sans injecter un fichier privé ou une base réelle.

### Examen des 31 candidats et copies préparées

**28 retenus, trois maintenus locaux** :

- `docs/soutenance/INSTALLATION_LOT6H2.md` : historique d'installation et références à des preuves/outils internes ; l'usage actuel est couvert par le guide committé.
- `docs/soutenance/LANCEMENT_AUTRE_PC_LOT6H1.md` : procédure historique redondante ; aucun autre PC n'est certifié par le nouveau guide.
- projet de texte de confidentialité (pièce interne non diffusée) : décisions et politique à compléter conservées en interne. Leur état reste expliqué dans les supports retenus ; aucun brouillon n'est présenté comme final.

Aux 28 retenus s'ajoute **`docs/soutenance/VALIDATION_SCOLAIRE.md`**, un résumé partageable des campagnes, limites et trois remarques partielles. Il ne publie pas les reçus bruts ni leurs chemins privés.

Les **29 versions documentaires** sont préparées dans un dossier Temp distinct, indiqué dans le manifeste. **Aucun original du projet n'est remplacé.** Les trois diagrammes et leurs SVG/PNG sont copiés à l'identique. Dans les supports textuels, une introduction distingue l'état courant des campagnes historiques ; les liens vers les archives exclues deviennent des mentions explicites, et les deux anciennes procédures d'installation renvoient au guide courant.

Résultats : **211 liens adaptés**, **489 références locales de fichiers/répertoires vérifiées, zéro cible manquante dans l'arbre projeté**, quatre préfixes de profils personnels anonymisés. Les 76 identifiants de questions des fiches sont préservés, ainsi que leurs réponses hors adaptation documentaire de liens/chemins. Les ancres Markdown et le rendu GitHub ne sont pas certifiés par cette vérification de chemins. Les 17 blocs PowerShell présents sont analysés syntaxiquement, **sans exécution**, et ne présentent pas d'erreur de syntaxe.

Un contrôle de chemins trop large a aussi rencontré `/admin/users/...`, qui est une route API, pas un chemin personnel ; aucun nom de route n'a été modifié pour masquer ce faux positif. Les copies et leurs empreintes ont été contrôlées ensuite. Reçu des copies (pièce interne non diffusée), contrôle final de préparation (pièce interne non diffusée).

Voici la **liste fermée des 29 versions documentaires préparées** ; les 89 fichiers à reprendre tels quels depuis HEAD et les six ressources suspendues sont détaillés dans le manifeste :

```text
README.md
frontend/README.md
frontend/images/README.md
docs/soutenance/README.md
docs/soutenance/fiche-commune.md
docs/soutenance/fiche-mahamadou.md
docs/soutenance/fiche-melissa.md
docs/soutenance/fiche-sylvie.md
docs/soutenance/ARCHITECTURE_SECURITE_RGPD.md
docs/soutenance/CONTRAINTES_INSTALLATION_LOT6H2.txt
docs/soutenance/DEMONSTRATION.md
docs/soutenance/FICHE_PROVENANCE_IMAGES_LOT6H5.md
docs/soutenance/INDEX_CODE_LOT6H1.md
docs/soutenance/ORAL_JURY.md
docs/soutenance/PROCEDURE_ACCES_LOT6H5.md
docs/soutenance/RECETTE_MANUELLE_LOT6G4.md
docs/soutenance/SUIVI_REMARQUES_JURY.md
docs/soutenance/SUPPORT_JURY_LOT6H1.md
docs/soutenance/TESTS_ET_VALIDATION.md
docs/soutenance/VALIDATION_SCOLAIRE.md
docs/soutenance/preuves-lot6h4/diagrammes/diagram-1.mmd
docs/soutenance/preuves-lot6h4/diagrammes/diagram-1.svg
docs/soutenance/preuves-lot6h4/diagrammes/diagram-1.png
docs/soutenance/preuves-lot6h4/diagrammes/diagram-2.mmd
docs/soutenance/preuves-lot6h4/diagrammes/diagram-2.svg
docs/soutenance/preuves-lot6h4/diagrammes/diagram-2.png
docs/soutenance/preuves-lot6h4/diagrammes/diagram-3.mmd
docs/soutenance/preuves-lot6h4/diagrammes/diagram-3.svg
docs/soutenance/preuves-lot6h4/diagrammes/diagram-3.png
```

Ce serait **huit modifications et 21 ajouts documentaires**, après autorisation d'appliquer ces versions et de les committer. Aucun fichier de cette liste n'est indexé pendant 6H.9. Les 110 fichiers locaux sont classés nominativement, pas effacés ; les preuves brutes, fichiers privés non relus et archives ne sont pas incorporés pour atteindre artificiellement une livraison « complète ».

## 5. Décision de publication des images

Les quatre WebP — `tableau-salle-bleue.webp`, `medaille-pavillon-ferme.webp`, `malle-quai-silencieux.webp`, `carnet-tour-nord.webp` — sont déclarés générés avec ChatGPT par Mélissa. Les dates, le contexte de compte/service et les références éventuellement fournies ne sont pas entièrement documentés. L'usage confirmé jusqu'ici pour les images reste la soutenance scolaire locale ; le souhait de livrer le code sur un dépôt public est une décision distincte.

### Conditions officielles consultées le 3 novembre 2026

Les conditions européennes OpenAI, affichées au 16 janvier 2026, attribuent à l'utilisateur les droits d'OpenAI sur les sorties, dans la mesure permise par la loi, dans la relation entre ces parties. L'utilisateur reste responsable des droits nécessaires sur ses entrées ; les sorties peuvent ne pas être uniques. Ce texte ne prouve ni les droits de tiers propres aux quatre fichiers ni une licence libre. Le régime dépend notamment du lieu de résidence, du service et de la période d'utilisation. [Conditions européennes, sections Using our Services et Content](https://openai.com/policies/eu-terms-of-use/).

Les services pour particuliers hors EEE/Suisse/Royaume-Uni renvoient à d'autres conditions ; les offres d'organisation/API relèvent d'un contrat distinct. Le compte effectivement utilisé n'est pas établi ici. [Conditions générales](https://openai.com/policies/terms-of-use/), [Services Agreement](https://openai.com/policies/services-agreement/).

La politique officielle de partage demande notamment une relecture humaine et une indication claire de la génération par IA. Une attribution proposée doit donc rester factuelle, par exemple « Illustrations générées par Mélissa avec ChatGPT », après confirmation du périmètre de partage. Cela n'attribue aucune création du SVG à Mélissa. [Politique de partage et publication](https://openai.com/policies/sharing-publication-policy/).

### Décisions fondées sur les preuves disponibles

| Ressource | Décision 6H.9 | Ce qui permettrait de statuer |
|---|---|---|
| Quatre WebP | **Diffusion GitHub à justifier ; aucun GO général accordé** | Confirmation par Mélissa des quatre fichiers, service/période approximative, références fournies ou éléments disponibles à leur sujet, relecture des visuels et accord de partage vers le dépôt public désigné |
| `default-story.svg` | **Origine non établie ; suspendu** | Identifier sa création ou sa source, les conditions applicables et la personne en mesure d'autoriser le partage ; le déposant Git n'est pas nécessairement le créateur |
| Trois diagrammes et neuf fichiers associés | **Retenus dans la sélection scolaire** | Sources internes raccordées au README, empreintes et rendus 6H.4 contrôlés ; aucune nouvelle revendication de licence globale |
| Dossier téléchargé | **Local uniquement** | Pas de ressource nécessaire au kit ; provenance non établie, aucun contenu ouvert ou supprimé |

La **date exacte n'est pas à elle seule une exigence universelle de publication** ; une période ou trace fiable peut aider à identifier les conditions applicables. Aucune autorisation spéciale OpenAI par image n'est inventée. Les inconnues sur les références et le contexte restent des lacunes de preuve propres à ce dossier, et non la preuve d'une violation.

Si les justificatifs restent introuvables, l'équipe peut choisir ultérieurement un remplacement dont l'origine est connue, avec autorisation de modification. **Ne pas retirer maintenant le SVG : le kit et son manifeste figé en dépendent.** Toute substitution nécessiterait un lot technique et une validation ciblée. Aucun original modifié, supprimé ou régénéré.

La sixième ressource suspendue est `frontend/donnees.js` : données narratives héritées, dont des personnes réelles, non utilisées par les pages actuelles. Sa décision éditoriale reste à prendre ; ce n'est ni une base de comptes ni un fichier privé nouvellement ajouté. Ces six ressources sont déjà suivies et présentes dans l'histoire distante ; les omettre d'une liste ne les exclut pas d'un push.

## 6. Contrôles Git, sauvegardes et portée du transfert

| Contrôle | Résultat |
|---|---|
| Branche | `feature/frontend-api-integration`, inchangée |
| HEAD | `0d77a9ab0859f1aa6488405a4f524a399a402f30`, inchangé |
| Série locale | `4bbb75d`, `0d77670`, `3fe3596`, `0d77a9a` : quatre commits, 80 chemins changés depuis le parent distant |
| Distant revérifié | `07a9f03ea0a3bdad4a07066fdd7bab1997cc158b` ; quatre commits en avance, zéro en retard |
| Index / autres branches | Index vide ; toutes les références locales conservées |
| Modifications suivies | Les huit modifications documentaires initiales, inchangées |
| Sources testées | 102 objets identiques à l'export contrôlé en 6H.7 ; guide approuvé inchangé |
| Sauvegarde et récupération 6H.2 | 197 fichiers chacune, ensembles/tailles/SHA conformes |
| Complément et récupération 6H.6 | 32 fichiers chacune, ensembles/tailles/SHA conformes |

Les quatre copies de sauvegarde ont été revérifiées sans restauration ni écriture. Elles ne contiennent pas les deltas produits après leur date. Les 29 versions de publication sont préparées sous Temp : **copies de travail inspectables, pas une nouvelle sauvegarde durable**. Leur contenu devra être préservé avec les deltas avant une intervention ultérieure. Reçu des sauvegardes (pièce interne non diffusée).

Le push ciblé actuel ajouterait les **quatre commits locaux**, pas 128 nouveaux commits. Les 124 ancêtres sont déjà accessibles depuis la branche distante. Un futur commit documentaire ajouterait d'autres objets ; son SHA et son contenu devront être contrôlés après création autorisée. Les fichiers non suivis et les huit modifications locales ne partent jamais par simple push d'un HEAD qui ne les contient pas.

Aucun test applicatif relancé : le code n'a pas changé. Les **854 tests historiques** et les **43 requêtes WSGI de 6H.7** restent des preuves distinctes. Aucun Edge, serveur, accès Aiven/MySQL, migration ou déploiement. Les vérifications nouvelles concernent l'histoire ciblée, les empreintes, les copies documentaires et les liens.

## 7. Blocages restants et plan après résolution

1. **Accès historiques : blocage prioritaire.** Obtenir la vérification des responsables effectifs et les preuves de non-utilisabilité ou rotation/révocation. L'abandon déclaré du code ne suffit pas. Les instructions de ce bilan sont prêtes, aucune intervention réelle effectuée.
2. **Images et récit hérité : décision de diffusion.** Compléter les éléments de provenance/partage et décider du sort des ressources pour lesquelles aucun justificatif n'est disponible. Toute modification technique ou d'histoire exige son autorisation adaptée.
3. **Appliquer la sélection documentaire arrêtée après validation.** Utiliser les 29 versions et leurs empreintes, préserver les originaux, vérifier les différences, les dépendances et les liens. Ne pas recopier aveuglément les 31 originaux ou tous les fichiers restants.
4. **Créer les commits uniquement après nouvelle autorisation.** Ce lot interdit explicitement tout commit/push, même si un justificatif arrive avant sa fin. Garder une liste fermée et revoir les nouveaux blobs sans afficher de secret.
5. **Livrer ensuite seulement dans le périmètre autorisé.** Relire la visibilité et la tête distante, confirmer l'absence de divergence, pousser la branche exacte sans force puis vérifier réellement SHA, fichiers, ressources et exclusions. Ne pas annoncer le succès avant cette vérification. Aucune autre branche à modifier.

La finalisation du RGPD d'une application publique n'est pas artificiellement exigée pour partager du code de démonstration. Les brouillons restent désignés comme tels, aucune base réelle n'est sélectionnée, et aucune ouverture publique n'est validée. Les remarques C-02, C-07 et I-02 restent partielles : **19/22, 950/11 % = 86,363636… %, soit 86,36 % arrondi**.

## 8. Verdict et arrêt

**NO-GO PUSH.** L'exposition historique est démontrée et le travail documentaire est désormais borné et préparé. En revanche, le statut réel des anciens comptes et les justificatifs/décisions de six ressources restent insuffisants. Aucun risque n'est déclaré résolu par défaut.

**Aucun commit ni push. Arrêt après 6H.9, en attente de validation et des éléments vérifiables.** Les 244 fichiers initiaux, les huit modifications, l'index et les références sont préservés ; le reçu final (pièce interne non diffusée) enregistre les contrôles et les livrables ajoutés. Aucun fichier applicatif ou original d'image modifié.
