# Lot 6H.7 — validation finale avant push GitHub

> Archive pédagogique datée : les résultats et descriptions ci-dessous concernent le lot indiqué. Les anciens repères de ligne ne décrivent pas la version candidate. Pour préparer la soutenance actuelle, consulter les quatre fiches et le référentiel reliés au sommaire.

> Copie publique de référence : les chemins personnels et liens de travail internes sont retirés. Les preuves et commandes historiques gardent leur date et leur périmètre ; utiliser le README actuel pour le lancement.

3 novembre 2026. **La version committée fonctionne depuis une copie complète de HEAD et un environnement Python neuf, hors ligne. Aucun fichier applicatif indispensable au parcours testé ne manque. Aucun push ni nouveau commit effectué.**

**GO pour la version Git actuelle dans le périmètre scolaire synthétique testé. NO-GO pour un push ciblé à ce stade. NO-GO pour l'ouverture publique du site.** Le dépôt cible est public, ce que l'utilisateur a confirmé comme destination souhaitée pendant ce lot. Le GO technique ne vaut pas validation des droits, de l'historique ou d'un déploiement.

Les remarques restent **19/22 terminées : 950/11 % = 86,363636… %, soit 86,36 % arrondi**. C-02, C-07 et I-02 restent partielles ; aucun développement supplémentaire n'est justifié pour les clôturer artificiellement.

## 1. Périmètre, lectures et état initial

Lecture intégrale de [6H.6](BILAN_LOT6H6.md), du plan de commits 6H.5 (pièce interne non diffusée), de [6H.5](BILAN_LOT6H5.md), des instructions d'installation et du kit avant exécution. Recherche des instructions du dépôt et des parents accessibles : aucun `AGENTS.md` trouvé. Les README et consignes du kit ont été examinés ; aucun lancement humain n'est déduit de leur présence.

| Élément | État vérifié |
|---|---|
| Branche | `feature/frontend-api-integration`, conservée |
| HEAD | `3fe35965d5dd88151a7e1cab5bc645e2ddfbfca2`, conservé |
| Fichiers suivis | 102 |
| Modifications suivies restantes | 8, toutes documentaires |
| Non suivis à l'entrée du lot | 114, comptés individuellement |
| Index / conflits | Vides : aucun fichier indexé, aucun conflit |
| Travail initial | 216 chemins suivis ou non suivis ; 122 changements restants |

Le reçu initial (pièce interne non diffusée) fixe les chemins et empreintes. Deux fichiers non suivis restent non ouverts : `frontend/histoires-originales.json` et `docs/soutenance/COMPTES_DEMO.exemple.csv`. Leurs métadonnées sont conservées. La nouvelle autorisation d'audit de l'arbre et de l'historique permet cette fois d'examiner **le blob Git** de `frontend/donnees.js`, précédemment exclu des lectures ; aucun contenu n'est exécuté.

La sauvegarde complète et le complément restent ceux vérifiés en 6H.6. Ce lot ne les remplace pas et ne prétend pas avoir revalidé leurs 197/32 fichiers en entier. Le reçu 6H.2 et les 25 roues effectivement réutilisées sont revérifiés par SHA-256. Les nouveaux documents 6H.7 ne sont pas annoncés comme sauvegardés dans ces copies antérieures.

## 2. Contrôle des trois commits

| Commit | Parent | Contenu |
|---|---|---:|
| `4bbb75df2b7860e8373890634f6f39935cdde01c` | `07a9f03ea0a3bdad4a07066fdd7bab1997cc158b` | 46 fichiers : 12 ajouts, 34 modifications |
| `0d776703219c63951823d3e4f06d015165ddeae8` | `4bbb75df2b7860e8373890634f6f39935cdde01c` | 30 fichiers : 21 ajouts, 9 modifications |
| `3fe35965d5dd88151a7e1cab5bc645e2ddfbfca2` | `0d776703219c63951823d3e4f06d015165ddeae8` | 3 ajouts |

Les chemins de chaque commit correspondent exactement aux trois listes fermées 6H.5. **79 chemins, 36 ajouts, 43 modifications, zéro suppression**, chaîne linéaire. Reçu (pièce interne non diffusée). Aucun amend, réindexation, checkout, reset, merge ou changement de branche.

## 3. Classement exhaustif des 122 fichiers restants

L'annexe CSV (pièce interne non diffusée) donne **une ligne par fichier**, son statut M/??, une catégorie exclusive et le motif. Le reçu JSON (pièce interne non diffusée) conserve la même sélection. Les nouveaux livrables 6H.7 sont comptés séparément : ils ne sont pas ajoutés rétroactivement aux 122.

| Catégorie | Nombre | Sens de la décision |
|---|---:|---|
| Nécessaires à la livraison | 7 | Informations d'installation, d'usage et de provenance à consolider ; pas sept dépendances applicatives ni une sélection de commit automatique |
| Documentation interne | 59 | Fiches, bilans, matrice, plans et décisions à sélectionner selon le destinataire |
| Fichiers temporaires ou preuves locales | 54 | Reçus, inventaires, rendus, listes, utilitaires et archives ; conservation locale |
| Ressources exclues pour sécurité ou droits | 2 | Fichiers non ouverts cités ci-dessus, hors sélection |
| **Total** | **122** | **8 modifiés + 114 non suivis** |

Les sept documents du premier groupe sont exactement :

```text
README.md
frontend/README.md
frontend/images/README.md
docs/soutenance/CONTRAINTES_INSTALLATION_LOT6H2.txt
docs/soutenance/INSTALLATION_LOT6H2.md
docs/soutenance/LANCEMENT_AUTRE_PC_LOT6H1.md
docs/soutenance/RECETTE_MANUELLE_LOT6G4.md
```

Leurs informations utiles peuvent être livrées sous forme d'un **guide autonome**, sans ajouter les sept versions locales et toutes leurs dépendances documentaires. Les contraintes transitives restent une aide de reproduction, pas un fichier indispensable à l'installation réussie ici : seuls les requirements de HEAD et le répertoire de roues vérifié ont été utilisés.

Les cinq autres fichiers suivis modifiés sont `docs/soutenance/README.md` et les quatre `fiche-*.md` ; ils sont classés documentation interne. Les trois archives `revision_code/mahamadou/backend/models.py`, `tools/recette_lot6f2.py` et `tools/recette_lot6f2_sources.json` sont conservées comme preuves/outillage historique, sans dépendance avec le kit actuel.

**Manquant indispensable au fonctionnement testé : aucun.** Les 122 fichiers ne doivent pas être ajoutés globalement. `.env`, cookies, certificats, environnements, bases locales et dossier téléchargé restent hors suivi ; ne pas les confondre avec ces 122 chemins non ignorés.

## 4. Copie réellement committée et installation indépendante

Les **102 fichiers de l'arbre HEAD** ont été exportés depuis les blobs Git dans un dossier Temp neuf. Chaque mode, chemin, taille et SHA-256 est enregistré dans reçu de validation (pièce interne non diffusée). Aucune copie d'un fichier applicatif non committé, aucun `.env`, aucun ancien venv, aucun historique `.git` injecté. Le venv neuf est placé à côté de cette copie, hors de son arbre source.

Installation avec **Python 3.13.0 AMD64 préexistant**, sans paquets du système. Les **25 roues** de la sauvegarde 6H.2 ont toutes été contrôlées contre le reçu approuvé. Installation limitée à ce répertoire : `pip --isolated install --no-index --no-cache-dir --only-binary=:all: --find-links … --requirement backend/requirements.txt`. Aucun téléchargement, aucune contrainte non committée ajoutée, aucune installation globale. **24 distributions de dépendances installées, plus pip ; `pip check` PASS.** Les 25 roues disponibles ne correspondent pas toutes à une dépendance installée sur cette plateforme.

La recette utilise exclusivement le Python du nouveau venv et le code exporté. Le kit fige 40 sources, désactive dotenv avant import, remplace l'environnement par la configuration synthétique et interdit réseau, sous-processus, migrations, bases persistantes et lectures/écritures hors périmètre. **Aucun `--serve`, serveur en écoute ou navigateur lancé.** L'import applicatif et les appels WSGI sont nécessaires au test, sans accès à un Flask déjà lancé.

Cette preuve est indépendante du dossier de travail applicatif et de son venv. Elle utilise le même PC, un Python installé et les roues privées vérifiées : elle ne prouve ni un autre PC/système, ni la disponibilité Internet des versions, ni une installation depuis le seul Git sans dépendances externes.

## 5. Résultats effectivement exécutés

| Contrôle | Résultat et limite |
|---|---|
| Sources exportées | 102/102 ; mêmes octets avant/après ; aucun fichier supplémentaire dans l'arbre source |
| Installation et cohérence | Venv neuf, installation hors ligne et `pip check` réussis |
| Pages et ressources | 10 pages HTML et 20 ressources du kit servies en WSGI ; leurs références script/style sont acceptées ; 6 chemins privés/hors liste refusés |
| Références statiques | 36 références script/style des 10 pages présentes ; zéro référence externe de ce type, zéro manquante |
| Connexion et contributions | Inscription, connexion, deux catégories, commentaire et signalement réussis |
| Likes | Ajout/retrait/réajout, doublon, CSRF, conservation ; ancien compteur incompatible refusé sans remise à zéro |
| Transactions | Erreur synthétique après flush et rollback sans changement résiduel |
| Administration | Rapport contextualisé, détail administratif, archivage/restauration, bannissement et refus de connexion du compte banni |
| Sept compteurs | API comparée aux SELECT : 2 dossiers, 1 résolu, 1 Cold Case, 4 utilisateurs, 2 commentaires, 1 signalement, 0 proposition pending |
| Intégrité | Dix tables synthétiques, FK actives, contrôle FK vide, aucune base fichier |
| Gardes | Sept compteurs à zéro ; serveur/navigateur non lancés |

**43 requêtes API, sept groupes de vérification, PASS.** Le service des ressources et les refus statiques sont des vérifications supplémentaires du kit, pas des tests à additionner aux 854 historiques. Preuves : installation (pièce interne non diffusée), isolation (pièce interne non diffusée), parcours (pièce interne non diffusée), références (pièce interne non diffusée).

Les **854 tests restent une référence historique**, non relancée. Les 43 appels actuels ne vérifient pas un navigateur, le responsive, tous les scénarios frontend ou la suppression définitive. Les migrations MySQL, anciennes données, verrous et reprise après DDL partiel ne sont ni exercés ni certifiés. Aucun besoin de rejouer les développements déjà validés pour prouver l'installation ciblée.

Le kit ne sert que le SVG de repli parmi les cinq images. Les quatre WebP sont bien présents dans l'export ; leur service visuel complet n'est pas retesté ici. La preuve 6H.2 des cinq images reste historique, distincte des contrôles présents.

## 6. Audit de sécurité de l'arbre et de l'histoire

Audit local de **127 commits**, **1 142 blobs**, **928 chemins historiques distincts**, soit 12 860 696 octets de blobs non compressés. Les règles recherchent clés privées, jetons fournisseurs, JWT, URL authentifiées, affectations littérales de credentials, cookies de session, certaines adresses personnelles et inserts de données SQL. Noms de fichiers sensibles et messages des commits sont aussi contrôlés. Les reçus ne contiennent **aucune valeur de secret**, seulement chemins, objets, lignes, règles et classifications.

Les 1 114 blobs textuels sont recherchés par motifs ; les 28 binaires sont inventoriés, sans décodage sémantique/OCR. L'audit n'est pas une garantie absolue d'absence de secret ou de données personnelles. Recherche (pièce interne non diffusée), qualification (pièce interne non diffusée).

### Nouveaux contenus

Le périmètre `07a9f03..3fe3596` représente **3 commits, 20 arbres et 79 blobs**, 790 489 octets de nouveaux blobs avant compression. Ce n'est pas la taille réseau exacte négociée par Git.

**Neuf signalements dans les nouveaux blobs : tous des constantes de fixtures de tests synthétiques**, dans `test_admin_users.py`, `test_api_errors_stats_login.py`, `test_moderation_journey.py` et `test_swagger.py`. Ce nombre diffère du contrôle plus étroit 6H.6 parce que les règles présentes couvrent aussi les valeurs de dictionnaires. Aucun secret réel identifié dans les nouveaux contenus avec ces règles ; aucun fichier `.env`, base/dump réel, cookie/session, certificat privé ou illustration nouvellement ajouté par les trois commits.

Le brouillon HTML RGPD est bien un nouveau contenu, explicitement marqué brouillon et dépendance de test ; un push le rendrait consultable comme source sur GitHub, bien qu'il ne soit pas servi comme politique du site. Cette distinction doit rester visible.

### Anciens accès administrateur : réserve concrète

**Deux couples administrateur/mot de passe codés en dur**, présents dans deux anciennes versions de `backend/index.py` (quatre occurrences signalées), alimentaient une création automatique de comptes au démarrage. Ils ne sont pas de simples exemples de documentation. Les objets concernés : `33af638e271bddaff73fce2732a8ca0a6fe300eb` et `9f343f3922864d397d074bdf10377031a7f754a3`, lignes 24–25. Les changements sont repérés par les commits `e933825`, `63934be` et `66ffe4b` ; détails sans valeurs dans le reçu.

Ils sont absents de HEAD, mais déjà accessibles depuis le parent distant confirmé. **Réponse utilisateur : utilisation et invalidation inconnues.** Aucun essai de connexion, accès à une base ou révocation effectué. Avant de considérer le risque traité, faire établir par les détenteurs si ces valeurs ont été utilisées ou réutilisées ; le cas échéant faire remplacer/désactiver les accès concernés dans une intervention autorisée. Un retrait futur d'un fichier ou un commit documentaire ne révoque pas ces accès et ne retire pas les copies historiques. Aucune réécriture d'historique prescrite comme opération automatique.

Ce constat ne signifie pas que le nouveau code introduit ces secrets ; c'est un risque préexistant à traiter, indépendamment de la recette locale synthétique.

### Autres contenus hérités

- **792 chemins de l'ancien `backend/venv/`**, caches Python, `.DS_Store` et configuration éditeur restent dans l'histoire, absents de l'arbre courant. Aucun fichier historique ne dépasse 273 394 octets. Cela représente du bruit et des dépendances embarquées anciennes, pas des fichiers à restaurer ou committer aujourd'hui.
- Le `.pem` historique repéré est le bundle d'autorités publiques de certifi ; le chemin `requests/cookies.py` est du code de bibliothèque, pas un fichier de cookies utilisateur. Aucun nom de `.env`, base réelle ou dump SQL trouvé dans les arbres parcourus. Aucun en-tête SQLite dans les fichiers signalés. Cela ne prouve pas qu'un fichier arbitrairement nommé ne contient jamais de données.
- Les autres signalements historiques se répartissent en **8 occurrences de fixtures**, **9 attributions d'auteurs tiers** et **3 exemples/masques dans des bibliothèques**. Avec les 4 occurrences d'accès administrateur, cela fait 24 signalements hérités ; avec les 9 nouveaux, 33 au total.
- Les métadonnées Git contiennent cinq adresses d'auteur/committer distinctes dans l'histoire. Les trois nouveaux commits en utilisent une, déjà présente dans l'ascendance distante ; aucune adresse reproduite dans ce bilan. Aucun auteur ni email réécrit.
- `frontend/donnees.js` contient six petits enregistrements titre/résumé/catégorie, dont des affaires nommant des personnes réelles et des victimes. Aucun compte utilisateur ou credential trouvé ; aucune URL externe. **Ce n'est pas un jeu entièrement synthétique certifié.** Il n'est chargé par aucune des dix pages actuelles, reste hérité dans HEAD et demande une décision éditoriale de diffusion. Les faits narratifs et leurs sources n'ont pas été vérifiés.
- Les cinq images actuelles sont déjà dans l'ascendance distante, avec les mêmes objets. Leurs droits ne sont pas établis par cette antériorité. Les ressources visuelles historiques des bibliothèques tierces ne sont pas de nouvelles illustrations du projet ; aucune licence globale n'est inventée pour l'ensemble.

Le dossier téléchargé signalé en 6H.5 reste non suivi/ignoré, hors copie HEAD et hors histoire parcourue. Aucun contenu ouvert ou modifié. Son risque conditionnel de service direct par le lanceur normal reste celui documenté en 6H.5 ; le kit à liste fermée ne l'expose pas.

## 7. Destination distante et portée réelle du push

Consultation **GitHub en GET uniquement**, via le connecteur ; aucune authentification ou URL de remote contenant un secret imprimée. `origin` en lecture et en push désigne `https://github.com/Leyvsi/portfolio.git`, sans credentials incorporés. Métadonnées et références (pièce interne non diffusée), branche ciblée (pièce interne non diffusée).

| Élément | Constat |
|---|---|
| Dépôt | [Leyvsi/portfolio](https://github.com/Leyvsi/portfolio), **public**, non archivé |
| Choix utilisateur | Dépôt public confirmé comme cible souhaitée, sous réserve des points identifiés ; aucun push autorisé |
| Branche à viser | `refs/heads/feature/frontend-api-integration` |
| HEAD distant observé | `07a9f03ea0a3bdad4a07066fdd7bab1997cc158b` |
| Relation locale/distant ciblé | **3 commits en avance, 0 en retard** ; le distant est l'ancêtre direct de la série |
| Protection déclarée | Branche non protégée, aucun contrôle obligatoire retourné par cet endpoint |
| Permission du connecteur | Lecture/push déclarés, pas administration ; cela ne prouve pas l'authentification du client Git local |
| Branche par défaut | `main`, distante `45170b7d5530c834c561afc1a19f39abf288cb74` |
| Référence locale de main | `origin/main` encore `5f488f8…` : obsolète ; aucune fusion vers main évaluée ou proposée |
| Déploiement | `has_pages: false`, aucun workflow dans HEAD ; aucun hébergement externe ou hook distant certifié absent |

La lecture de la branche avec le slash encodé a été refusée par le connecteur ; la lecture du chemin non encodé et des références Git a ensuite réussi. Aucun `fetch` n'a modifié les références locales pour contourner cet échec.

**Un push ciblé n'enverrait pas 127 nouveaux commits : seuls les trois commits locaux sont absents de cette branche distante.** Les 124 ancêtres, dont les anciens accès et images, sont déjà accessibles depuis sa tête. Ils resteraient accessibles dans l'histoire ; vers un nouveau dépôt vide, la même branche rendrait aussi accessible cette ascendance complète. Ne pas confondre objets nouvellement transférés et historique accessible. Périmètre chiffré (pièce interne non diffusée).

Pas de divergence à résoudre sur la branche ciblée à l'instant observé ; aucun merge ni test de conflit vers `main`. Une nouvelle observation distante est nécessaire juste avant l'opération future.

## 8. Trois remarques partielles et décisions réellement nécessaires

| Remarque | État et décision | Effet sur un push de sources |
|---|---|---|
| C-02 — Fichier privé de comptes de démonstration | Mahamadou désigné. Support privé, renouvellement et deux connexions du processus du jour J non confirmés. | Ne manque pas au code et ne doit pas être committé. N'empêche pas en soi le partage du code. Les anciens accès historiques constituent une réserve distincte. |
| C-07 — Informations RGPD et consentement | Groupe responsable du projet scolaire, sans identité juridique du responsable de traitement établie ; contact absent, bases/durées/hébergement/transferts non validés. | Ne pas exiger la mise en production RGPD d'un site non ouvert pour partager du code synthétique. Conserver le brouillon comme tel ; vérifier les contenus/personnes effectivement diffusés. Bloque une prétention de conformité ou une ouverture publique. |
| I-02 — Provenance et droits des illustrations | Mélissa/ChatGPT et usage local déclarés pour quatre WebP ; dates et références inconnues ; origine du SVG non confirmée. | La destination publique souhaitée ne fournit pas les justificatifs manquants. Décision et preuves pour la diffusion des ressources encore nécessaires, même déjà distantes. Aucun remplacement/retrait autorisé ici. |

La publication du code sur GitHub n'est pas l'ouverture du site. L'absence de contact RGPD n'est pas transformée en impossibilité technique de push. Inversement, un dépôt public ne doit pas être décrit comme une livraison privée au jury. **19/22 inchangé.**

## 9. Correction documentaire préparée et sélection supplémentaire

Les README présents dans HEAD ne présentent aucun lien local cassé parmi les liens Markdown contrôlés, mais leurs descriptions sont **périmées** : commentaires/likes prétendument réservés à l'API, administration prétendument en lecture seule, ancienne procédure exigeant configuration et migrations, ancien décompte de tests et absence annoncée de peuplement reproductible. Les versions locales actualisées renvoient à de nombreux documents internes non committés ; les ajouter seules ne constitue pas une sélection cohérente.

Correction minimale préparée : [LIVRAISON_SCOLAIRE.md](../../LIVRAISON_SCOLAIRE.md), **nouveau guide autonome à la racine**, avec installation hors ligne, recette du kit committé, fonctions actuelles, limites de preuve, organisation du jour J et réserves de diffusion. Tous ses liens locaux ciblent des fichiers déjà suivis ; il n'exige aucun bilan, compte privé ou contrainte non committée. Ses deux blocs PowerShell sont analysés syntaxiquement sans exécution.

**Liste exacte du commit documentaire supplémentaire proposé : un seul fichier, `LIVRAISON_SCOLAIRE.md` (ajout).** Message proposé : `Documenter la livraison scolaire isolée et ses réserves`. Aucun autre fichier, aucune version locale des README, aucun rapport/preuve/inventaire/compte. Ce guide est l'entrée actuelle à indiquer au jury ; les README historiques restent à lire comme tels. Une refonte ultérieure de leur navigation peut être décidée séparément, sans forcer l'ajout de tous les bilans.

**Autorisation requise avant ce commit**, conformément à la section 6 de l'autorisation utilisateur 6H.7 : « Si un commit supplémentaire est nécessaire, présenter sa liste exacte de fichiers et demander mon autorisation. » Le contenu est préparé et contrôlé ; aucune indexation n'est faite. Ce commit améliorerait la livraison documentaire, mais ne résoudrait pas les réserves d'accès historiques, de droits et de contenus hérités.

Autres livrables locaux du lot : présent bilan, classement CSV et reçus sous `preuves-lot6h7/`. Aucun document antérieur ni fichier applicatif modifié.

## 10. Procédure de livraison préparée, non exécutée

1. Faire traiter ou qualifier explicitement les anciens accès par les personnes compétentes, sans transmettre leurs valeurs ; confirmer les décisions de diffusion pour les cinq images et l'ancien jeu narratif. Tout retrait/remplacement ou travail sur l'historique demanderait une autorisation distincte et une sélection concrète préservant les originaux.
2. Valider le guide et autoriser séparément son éventuel commit local. Si effectué, le HEAD et la liste de commits à livrer changent : refaire le contrôle ciblé et préparer la commande avec le nouveau SHA. **La commande ci-dessous ne livrerait pas ce futur guide.**
3. Avant tout push autorisé, vérifier `origin`, visibilité, branche/HEAD attendus, index, hooks et état de travail. Aucun hook local actif trouvé pendant ce lot. Vérifier en lecture seule que la branche distante n'a pas avancé. Conserver les sauvegardes et tous les travaux locaux ; aucun besoin de les stasher, nettoyer ou réinitialiser pour pousser une révision précise.
4. Obtenir l'autorisation explicite de push visant le dépôt public, la branche et les SHA effectivement retenus. La validation de 6H.6 ou l'intention GitHub n'est pas cette autorisation.
5. Exécuter seulement le push ciblé autorisé, sans force, sans `--all`, `--mirror` ou tags implicites. Après succès, lire la référence distante et vérifier le SHA ; contrôler que l'index et les travaux locaux sont préservés. Un refus non-fast-forward impose un nouvel examen, pas un push forcé.

Commande préparée pour **les trois commits actuels seulement**, à ne pas exécuter avant levée des réserves et autorisation :

```powershell
# PREPARATION UNIQUEMENT : aucune commande de ce bloc executee en 6H.7.
if ((git branch --show-current) -ne 'feature/frontend-api-integration') {
    throw 'Branche inattendue : arreter.'
}
if ((git rev-parse HEAD) -ne '3fe35965d5dd88151a7e1cab5bc645e2ddfbfca2') {
    throw 'HEAD modifie : revoir la selection et la commande.'
}
git diff --cached --quiet
if ($LASTEXITCODE -ne 0) { throw 'Index a reexaminer sans reset.' }
$ref6h7 = @(git ls-remote --heads origin refs/heads/feature/frontend-api-integration)
if ($LASTEXITCODE -ne 0 -or $ref6h7.Count -ne 1) {
    throw 'Reference distante non verifiee.'
}
if (($ref6h7[0] -split '\s+')[0] -ne '07a9f03ea0a3bdad4a07066fdd7bab1997cc158b') {
    throw 'Distant modifie : reexaminer avant livraison.'
}
# Seulement apres autorisation explicite de cette operation :
git -c push.followTags=false push origin 3fe35965d5dd88151a7e1cab5bc645e2ddfbfca2:refs/heads/feature/frontend-api-integration
if ($LASTEXITCODE -ne 0) { throw 'Push non confirme : ne pas forcer.' }
```

Aucune liaison upstream n'est configurée pour la branche actuelle ; le refspec explicite évite de supposer celle de `main` ou une valeur de `push.default`. L'opération proposée ne touche qu'une branche distante. Un push n'ajoute pas les huit modifications ni les fichiers non suivis ; ceux-ci resteront locaux. Les réglages côté serveur et l'authentification Git effective peuvent encore refuser l'opération ; aucune réussite distante n'est promise.

## 11. Préservation et verdicts

Le contrôle final (pièce interne non diffusée) rapproche HEAD, branche, index, 214 empreintes et les métadonnées des deux fichiers non ouverts. Les 216 chemins initiaux sont conservés ; seuls les nouveaux documents du lot augmentent les non-suivis. Le dossier téléchargé est contrôlé par métadonnées, sans lecture de contenu. `git diff --check` vérifie les modifications documentaires restantes ; les originaux et la copie de test sont conservés, sans suppression.

- **GO — version Git actuelle**, pour son fonctionnement scolaire local synthétique : copie HEAD complète, installation neuve hors ligne et parcours WSGI réussis. Ce verdict ne vaut ni documentation de livraison déjà actualisée dans Git, ni validation MySQL, visuelle ou publique.
- **NO-GO — push GitHub ciblé maintenant** : cible publique confirmée et absence de divergence établies ; statut des accès historiques, décisions/preuves de diffusion et guide de livraison restent à traiter. Les seuls nouveaux contenus examinés ne révèlent pas de secret réel ; ne pas présenter les réserves héritées comme de nouveaux transferts. Aucun push autorisé ou tenté.
- **NO-GO — ouverture publique du site** : droits, organisation/information RGPD, hébergement, sécurité d'exploitation et éventuel schéma réel non validés. Aucun déploiement.

**Arrêt après 6H.7, en attente de validation.** Aucune correction applicative, migration, connexion MySQL/Aiven, suppression, modification des permissions Windows ou opération distante d'écriture.
