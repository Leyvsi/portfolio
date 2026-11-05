# Lot 6H.8 — livraison complète : publication bloquée

> Archive pédagogique datée : les résultats et descriptions ci-dessous concernent le lot indiqué. Les anciens repères de ligne ne décrivent pas la version candidate. Pour préparer la soutenance actuelle, consulter les quatre fiches et le référentiel reliés au sommaire.

> Copie publique de référence : les chemins personnels et liens de travail internes sont retirés. Les preuves et commandes historiques gardent leur date et leur périmètre ; utiliser le README actuel pour le lancement.

3 novembre 2026. **Aucun push effectué, aucun fichier nouvellement livré sur GitHub, aucun commit complémentaire créé pendant 6H.8.** La livraison complète n'est pas annoncée comme réalisée.

La condition de sécurité imposée par l'utilisateur reste non satisfaite. Les deux anciens accès administrateur alimentaient réellement du code de création de comptes dans une base SQLite persistante ; leur utilisation effective et leur invalidation ne sont pas établies. Réponse reçue pendant ce lot : **« Toujours inconnus : maintenir le blocage du push ».** La publication est donc arrêtée, y compris celle des quatre commits locaux seuls. Aucune réécriture d'historique, révocation ou connexion de contrôle n'a été tentée.

## 1. État Git et dépôt distant

| Élément | Résultat |
|---|---|
| Dépôt cible | [Leyvsi/portfolio](https://github.com/Leyvsi/portfolio), public |
| Branche locale et cible | `feature/frontend-api-integration` |
| HEAD local | `0d77a9ab0859f1aa6488405a4f524a399a402f30` |
| Tête distante revérifiée par GET | `07a9f03ea0a3bdad4a07066fdd7bab1997cc158b` |
| Relation | **4 commits en avance, 0 en retard**, pas de divergence sur cette branche à l'instant du contrôle |
| Suivis | 103 fichiers |
| Changements à l'entrée de 6H.8 | **8 suivis modifiés + 130 non suivis = 138** |
| Inventaire initial complet | **233 fichiers** suivis ou non suivis non ignorés |
| Index / conflits | Vides |

Les 114 non suivis étaient le point de départ de 6H.7. Ses livrables ont porté ce nombre à 131, puis le commit du guide a ramené le total à **130**. Les nouveaux livrables de 6H.8 sont comptés séparément dans le reçu final, sans réécrire l'inventaire initial.

La branche distante est non protégée selon la réponse GitHub ; cela ne lève aucune condition de sécurité ou d'autorisation. Consultation distante en lecture seule, sans `fetch` modifiant les références locales. Aucun contrôle de fusion vers `main`, aucun changement de branche. Aucun `AGENTS.md` trouvé lors de la recherche dans le dépôt ; les règles et constats antérieurs sont conservés.

Preuves : état initial (pièce interne non diffusée), état distant (pièce interne non diffusée).

## 2. Quatre commits locaux contrôlés

| Commit | Objet | Chemins modifiés dans le commit |
|---|---|---:|
| `4bbb75d` | Fonctionnalités, sécurité, modèles et migrations candidates | 46 |
| `0d77670` | Tests et brouillon HTML nécessaire au contrat de test | 30 |
| `3fe3596` | Kit scolaire, manifeste figé et test du kit | 3 |
| `0d77a9a` | Guide autonome `LIVRAISON_SCOLAIRE.md` | 1 |

Les trois premières listes correspondent exactement aux sélections 6H.5 ; le quatrième commit ajoute uniquement le guide approuvé, dont l'empreinte est inchangée. Les **102 objets de fichiers contrôlés en 6H.7 sont identiques dans le HEAD actuel**. Le seul ajout depuis cette vérification est documentaire.

La série contient donc 80 chemins distincts changés par rapport au parent distant, dont 37 ajouts et 43 modifications, aucune suppression. Les sources frontend/backend, API, authentification, modèles, sept migrations candidates, commentaires, signalements, likes, administration, tests et kit sont déjà conservés dans les commits locaux. Le guide aussi. **Le travail documentaire restant ne doit pas être confondu avec du code absent de HEAD.**

Ces quatre commits n'ont pas été poussés pendant 6H.8. Leur conservation locale ne prouve pas qu'ils existent sur GitHub.

## 3. Fichiers utiles à la livraison complète

L'inventaire CSV (pièce interne non diffusée) couvre les **233 chemins initiaux**, chacun avec statut Git, décision et motif. Le manifeste de préparation (pièce interne non diffusée) conserve les listes exactes et empreintes. Ce manifeste est expressément **bloqué et non validé pour indexation/publication**.

| Classe exclusive | Nombre | Décision |
|---|---:|---|
| Déjà dans HEAD, hors catégories ci-dessous | 89 | Sources, tests, kit, guide et dépendances conservés |
| Candidats documentaires | 31 | 8 fichiers suivis modifiés et 23 ajouts possibles, à consolider |
| Exclus de la sélection publique automatique, conservés localement | 105 | Bilans historiques, reçus bruts, inventaires, scripts ponctuels et archives |
| Exclus privés/non relus | 2 | Aucun ajout, aucune ouverture de contenu |
| Ressource héritée nécessitant une décision éditoriale | 1 | `frontend/donnees.js` |
| Illustrations héritées en attente de droits/provenance | 5 | Quatre WebP et `default-story.svg` |
| **Total** | **233** | Aucune suppression |

La sélection documentaire comprend :

- Les trois README racine/frontend/images, l'index de soutenance et les quatre fiches de l'équipe.
- L'architecture et la sécurité, la démonstration, l'oral, le suivi des 22 remarques, le support de soutenance et l'index courant du code.
- Les tests et limites, l'installation hors ligne, les contraintes de dépendances, le guide autre PC et le protocole de recette actuel.
- La procédure d'accès sans comptes, la fiche de provenance, le document RGPD explicitement marqué brouillon.
- Les **neuf fichiers des trois diagrammes** : source Mermaid, SVG et PNG pour chacun.

Les 31 chemins exacts sont dans le manifeste ; leur regroupement avec HEAD formerait 126 chemins distincts, **avant résolution des six ressources retenues et des liens documentaires**. Ce total est une base de préparation, pas une livraison validée.

### Dépendances documentaires effectivement détectées

Les candidats contiennent **207 occurrences de liens vers 54 cibles locales hors de cette sélection**. Aucune de ces cibles n'est absente du dossier de travail ; elles deviendraient manquantes dans une livraison qui copierait seulement les candidats. Il s'agit notamment de bilans, reçus, utilitaires et archives historiques. Détail (pièce interne non diffusée).

Ne pas ajouter automatiquement les 54 cibles pour fermer les liens. La correction minimale consiste à consolider les documents courants autour du guide committé, du code et d'un résumé des preuves partageable ; conserver les liens vers les archives internes seulement si leurs fichiers sont explicitement retenus et revus. Les informations historiques utiles ne doivent pas être perdues, mais les instructions périmées doivent rester identifiées comme historiques.

**Les 31 versions existantes ne sont donc pas présentées comme prêtes à committer ensemble.** Leur consolidation est différée : l'utilisateur impose des commits complémentaires après validation des contrôles, et maintient ici le blocage de sécurité. Aucun commit partiel n'a été créé pour donner l'impression d'une livraison complète.

## 4. Exclusions et ressources retenues

### Fichiers conservés hors publication automatique

- `docs/soutenance/COMPTES_DEMO.exemple.csv` et `frontend/histoires-originales.json` : contenus non relus, conservés sans ajout ni copie ; métadonnées vérifiées.
- `.env`, cookies, certificats/clés, bases et environnements locaux : exclus par les règles existantes, hors sélection ; aucun fichier privé ignoré ouvert pour cet audit.
- Les reçus avec chemins locaux, les inventaires, les scripts de sauvegarde/commit et les archives 6F.2 : éléments de travail à conserver, pas dépendances applicatives à publier.
- `revision_code/mahamadou/backend/models.py` : copie de travail historique distincte du modèle actif, non fusionnée automatiquement.
- `frontend/images/Reprendre projet portfolio_files` : 44 fichiers, métadonnées inchangées, dossier ignoré et non suivi ; aucun contenu ouvert, modifié ou supprimé.

Les 105 exclusions locales sont une **sélection de diffusion**, pas une déclaration d'inutilité ou une autorisation d'effacement. Le bilan 6H.8 et ses nouveaux reçus restent eux aussi locaux pendant ce lot.

### Ressources déjà suivies : leur omission ne les retire pas

| Ressource | Informations confirmées | Décision restante |
|---|---|---|
| `tableau-salle-bleue.webp` | Mélissa, génération ChatGPT déclarée ; même fichier déjà distant | Dates/contexte et références non confirmés ; justificatifs de diffusion non complets |
| `medaille-pavillon-ferme.webp` | Idem | Idem |
| `malle-quai-silencieux.webp` | Idem | Idem |
| `carnet-tour-nord.webp` | Idem | Idem |
| `default-story.svg` | Repli du kit ; trace d'ajout Git connue | Auteur créatif, outil/source et autorisation non établis |
| `frontend/donnees.js` | Six récits courts dont des affaires nominatives ; aucune page actuelle ne le charge | Décision éditoriale et justification du partage des contenus hérités |

La demande vise les ressources **dont la diffusion est autorisée**. Elle ne fournit pas les justificatifs jusqu'ici inconnus et ne transforme pas une présence antérieure sur GitHub en licence. Aucune licence libre, autorisation de tiers ou auteur du SVG n'est inventé. Aucun fichier image modifié ou supprimé. Si un retrait du suivi ou un remplacement est choisi, préparer cette intervention séparément en conservant les originaux ; cela ne retirerait pas automatiquement l'histoire déjà publique.

Les diagrammes sont distincts de ces illustrations : les trois sources correspondent au README local courant et les neuf fichiers restent conformes aux empreintes du rendu contrôlé en 6H.4. Aucune nouvelle exécution de navigateur ou génération d'image.

## 5. Sécurité : condition bloquante maintenue

### Nature des anciens accès

L'analyse statique renouvelée des deux blobs historiques de `backend/index.py` retrouve une liste de **deux couples username/password littéraux**, puis création de `User(is_admin=True)`, hachage du mot de passe et commit SQL. La configuration désignait `sqlite:///site.db` et exécutait `create_all` au démarrage.

Ces valeurs sont donc **des identifiants codés pour créer des comptes**, et non de simples exemples isolés dans un commentaire. L'analyse du code ne démontre ni qu'un compte a réellement été créé, ni qu'il est encore accessible, ni qu'une valeur a été réutilisée ailleurs. Sans preuve supplémentaire, ils restent potentiellement utilisables. Constat sans valeurs (pièce interne non diffusée).

Repères privés de recherche pour la personne chargée de la vérification : blobs `33af638e271bddaff73fce2732a8ca0a6fe300eb` et `9f343f3922864d397d074bdf10377031a7f754a3`, lignes 24–25 ; changements repérés dans `e933825`, `63934be`, `66ffe4b`. **Aucun identifiant, mot de passe ou empreinte de mot de passe reproduit.**

L'utilisateur confirme pendant 6H.8 : **utilisation et invalidation toujours inconnues ; maintenir le blocage du push**. Il manque une vérification par une personne responsable, portant sur les environnements où l'ancien code a pu être lancé et sur une éventuelle réutilisation de ces valeurs. Pour lever la condition, fournir sans secret soit une confirmation étayée de tests uniquement jetables sans réutilisation, soit une preuve expurgée de révocation/rotation : personne ayant vérifié, date, périmètre, action et résultat. Une simple autorisation générale de publication ne remplace pas cette preuve.

Ni Aiven/MySQL, ni base locale réelle, ni compte externe interrogé ; aucun essai de connexion avec les anciens accès. Aucune rotation, aucun changement d'auteur et aucune réécriture de l'histoire partagée.

### Contenus nouveaux et hérités

L'audit 6H.7 avait parcouru 127 commits et 1 142 blobs, avec qualification des signalements : fixtures synthétiques, attributions/exemples de bibliothèques et les deux accès historiques. Le quatrième commit ajoute seulement le guide revérifié. **Les objets précédemment audités restent inchangés** ; l'histoire accessible compte désormais 128 commits. Le contrôle ne prétend pas être un détecteur exhaustif de données personnelles ou un décodage de tous les binaires.

La nouvelle recherche ciblée sur le guide et les candidats documentaires ne trouve aucun marqueur de clé privée, jeton fournisseur, URL SQL authentifiée, credential littéral ou adresse personnelle correspondant aux règles contrôlées. Elle signale **14 références de chemins locaux et 15 mentions de fichiers sensibles**, à relire avant diffusion documentaire. Les mentions de `.env` ou cookies ne sont pas en elles-mêmes des valeurs de secrets ; aucune valeur n'est imprimée dans les reçus.

Les noms des membres et leurs rôles déclarés appartiennent au support scolaire demandé ; cela ne vaut pas autorisation générale de diffuser d'autres personnes, comptes ou informations internes. L'ancien jeu narratif et les métadonnées d'auteur Git restent à distinguer des données fictives du kit. Le contrôle n'autorise pas à annoncer « aucune donnée personnelle » dans l'ensemble de l'histoire.

Les anciens accès, l'ancien venv, les caches, les cinq images et le jeu narratif sont **déjà dans l'ascendance du distant confirmé**. Le push envisagé ajouterait les quatre commits locaux et les futurs compléments sélectionnés, sans introduire pour la première fois ces ancêtres. Cela ne lève pas la condition de sécurité fixée par l'utilisateur ; un nouveau dépôt vide avec la même histoire exposerait également ces ancêtres. Aucun nettoyage ou push forcé entrepris.

## 6. Sauvegardes revérifiées

Sous `[chemin local privé retiré]`, vérification des ensembles exacts de fichiers, tailles, SHA-256 et reçus :

| Copie | Fichiers | Résultat |
|---|---:|---|
| `portfolio-lot6h2-20261102-55c80c78` | 197 | PASS |
| `recuperation-lot6h2-20261102-55c80c78` | 197 | PASS |
| `portfolio-lot6h6-complement-20261102-166a41ed` | 32 | PASS |
| `recuperation-lot6h6-complement-20261102-166a41ed` | 32 | PASS |

Reçu de vérification (pièce interne non diffusée). Aucun écrasement, aucune restauration sur le projet et aucune nouvelle sauvegarde annoncée. Les documents produits après ces copies, notamment les livrables 6H.6/6H.7/6H.8 et le guide ultérieur, ne sont pas rétroactivement couverts par ces sauvegardes. Les deltas devront être préservés avant une future intervention risquée ; une sauvegarde de sources n'est ni une sauvegarde de base réelle ni une copie exhaustive de l'historique Git.

## 7. Tests et dépendances

**Aucun test applicatif relancé en 6H.8**, car aucun code n'a changé et aucune publication ne peut commencer. Les contrôles présents sont Git en lecture seule, empreintes, AST sans exécution des anciens blobs, liens et inventaires.

La preuve fonctionnelle pertinente reste 6H.7 : export des 102 fichiers depuis Git, venv neuf, installation hors ligne depuis 25 roues vérifiées, `pip check` PASS, dix pages/vingt ressources du kit, **43 requêtes WSGI et sept groupes réussis**, SQLite mémoire, sept gardes à zéro, sans serveur ni navigateur. Le rapprochement des **102 empreintes des objets Git est à nouveau réussi** ; le guide ultérieur n'altère pas cette preuve. Contrôles de rapprochement (pièce interne non diffusée).

Les **854 tests historiques** restent distincts et non relancés. Aucune nouvelle preuve visuelle, aucun nouveau système/PC, aucune migration réelle. Aucun fichier applicatif indispensable au parcours recetté n'est manquant dans HEAD. Le répertoire de roues n'est pas dans Git : les dépendances doivent être disponibles séparément ; publier le dépôt ne livre ni Python, ni un venv, ni une base préparée réelle.

Les sept révisions restent **candidates**. Le schéma d'une base existante, les anciens compteurs de likes, les relations SQL et l'intégrité des suppressions/commentaires/signalements sur MySQL ne sont pas validés par la création d'un schéma synthétique neuf.

## 8. RGPD et soutenance

Le code est destiné à une démonstration scolaire locale ; aucun site accessible au public n'est ouvert par cette demande. Le dépôt GitHub cible reste public. Ne pas confondre ces deux périmètres.

C-07 reste partielle : la responsabilité du projet appartient au groupe, mais l'identité juridique du responsable de traitement n'est pas établie ; aucun contact RGPD désigné, bases/conservation/hébergement/transferts non validés. Les documents proposés comme brouillons conservent cette mention. Le brouillon HTML déjà committé est une dépendance de test, non une politique définitive publiée sur le site. Aucune base de comptes réels incluse ou préparée.

C-02 reste partielle : Mahamadou est désigné pour les accès, mais le support privé, le renouvellement et les deux connexions du processus du jour J restent à confirmer. I-02 reste partielle pour les preuves de provenance/diffusion. **19/22 terminées, 950/11 % = 86,363636… %, soit 86,36 % arrondi.**

Avant la soutenance : finaliser la fiche privée des accès fictifs, utiliser le kit isolé autorisé, présenter les limites des tests et des migrations, disposer des supports et diagrammes à jour. Ne pas afficher les accès du jour J, cookies, tokens ou anciens credentials au jury.

## 9. Résultat réel et reprise nécessaire

- **Fichiers nouvellement livrés sur GitHub : aucun.** Les fichiers existants du distant n'ont pas été modifiés.
- **Commits créés en 6H.8 : aucun.** Les quatre commits locaux récents sont préservés ; le dernier reste `0d77a9a`.
- **Push : non exécuté**, même partiellement ; aucun `--force` ni opération distante d'écriture.
- **Préparation : inventaire complet et sélection candidate établis**, avec exclusions, ressources retenues et dépendances documentaires explicitement recensées.
- **Préservation :** aucun fichier initial supprimé ou modifié ; index, HEAD et branche inchangés. Le reçu final (pièce interne non diffusée) conserve les nombres et empreintes.

Pour reprendre la livraison :

1. Fournir la vérification et, si nécessaire, la preuve de rotation/révocation des anciens accès. C'est la condition bloquante demandée par l'utilisateur, pas une nouvelle demande de permission générale.
2. Résoudre les décisions de diffusion des cinq illustrations et du jeu narratif hérité ; ne pas retirer des fichiers du suivi ou de l'histoire sans une intervention autorisée adaptée.
3. Consolider les 31 candidats et leurs 54 cibles de liens hors sélection ; produire une sélection documentaire cohérente et relue, avec preuves partageables et brouillons clairement identifiés. Revérifier les éventuelles corrections sans rejouer inutilement tout le développement.
4. Après validation des contrôles, créer les commits complémentaires explicitement sélectionnés, puis relire la branche distante, les différences et la portée exacte de l'histoire. L'autorisation conditionnelle 6H.8 couvre le push ciblé seulement lorsque toutes ces conditions sont satisfaites ; aucun nouvel accord générique n'est demandé pour contourner un contrôle manquant.
5. Effectuer alors le push sans force et vérifier réellement le SHA distant, les fichiers, les ressources et les exclusions. Tant que cette étape n'est pas exécutée et vérifiée, ne pas annoncer la livraison.

**Verdict : NO-GO livraison GitHub complète actuellement ; fonctionnement scolaire local déjà recetté conservé ; aucune ouverture publique de l'application validée.** Le lot s'arrête sur le blocage de sécurité confirmé par l'utilisateur, avec les travaux et la préparation préservés.
