# Installation et démonstration scolaire

État documentaire du 3 novembre 2026. Le code du portfolio Les Petits Enquêteurs a été publié en lot 6H.11 dans `Leyvsi/portfolio`, branche `feature/frontend-api-integration`, commit `a85091959f98da020ce83f8acf20936d9ece8fbb`. Le lot 6H.12 a vérifié la démonstration locale dans Edge. **Le site n’est pas déployé publiquement.**

Le [README principal](README.md) décrit les fonctionnalités. La [validation scolaire](docs/soutenance/VALIDATION_SCOLAIRE.md) sépare les campagnes exécutées de leurs limites. Les bilans internes et les accès privés ne sont pas nécessaires à l’installation et ne font pas partie de la documentation publique.

## Choisir une copie de travail

Utiliser une copie neuve de la branche publiée. Un ancien dossier local peut avoir un HEAD ou des modifications différents du code livré : ne pas réinitialiser cet ancien dossier ni réutiliser son environnement par défaut. Ne pas remplacer les sources ou arrêter un processus d’une démonstration en cours.

```powershell
git clone --branch feature/frontend-api-integration --single-branch https://github.com/Leyvsi/portfolio.git
cd portfolio
git log -1 --oneline
```

`a850919` est la livraison de référence, pas une promesse que la tête de branche restera inchangée après de futures livraisons. L’environnement attesté est Windows AMD64 avec Python 3.13.0 ; un autre système ou interpréteur reste à vérifier.

## Installer les dépendances

Depuis la racine de cette copie, avec Python déjà installé et un dossier `.venv` absent :

```powershell
if (Test-Path -LiteralPath '.venv') { throw 'Choisir une copie neuve.' }
python -I -B -m venv .venv
if ($LASTEXITCODE -ne 0) { throw 'Creation du venv echouee.' }
.\.venv\Scripts\python.exe -I -B -m pip --isolated install --disable-pip-version-check --no-cache-dir --requirement backend/requirements.txt
if ($LASTEXITCODE -ne 0) { throw 'Installation incomplete.' }
.\.venv\Scripts\python.exe -I -B -m pip --isolated check
if ($LASTEXITCODE -ne 0) { throw 'Dependances incompatibles.' }
```

Cette variante télécharge les paquets. Les neuf dépendances directes sont fixées dans [requirements.txt](backend/requirements.txt), sans verrou complet des transitives. Le frontend ne nécessite ni npm ni compilation. L’installation neuve vérifiée en 6H.11 utilisait des roues locales contrôlées, selon la variante suivante ; le téléchargement ci-dessus n’a pas été rejoué pour le lot documentaire 6H.13.

### Variante hors ligne

Créer d’abord le venv comme ci-dessus. Disposer séparément d’un répertoire de roues compatible Windows/Python 3.13 AMD64, avec son manifeste de tailles et SHA-256 vérifié. Les roues ne sont pas fournies dans Git ; la campagne 6H.11 utilisait 25 roues locales vérifiées.

```powershell
$rouesPortfolio = 'C:\chemin\vers\wheelhouse-verifie'
if (-not (Test-Path -LiteralPath $rouesPortfolio -PathType Container)) {
    throw 'Repertoire de roues absent.'
}
.\.venv\Scripts\python.exe -I -B -m pip --isolated install --disable-pip-version-check --no-cache-dir --no-index --only-binary=:all: --find-links $rouesPortfolio --requirement backend/requirements.txt
if ($LASTEXITCODE -ne 0) { throw 'Installation incomplete.' }
.\.venv\Scripts\python.exe -I -B -m pip --isolated check
if ($LASTEXITCODE -ne 0) { throw 'Dependances incompatibles.' }
```

## Kit scolaire et isolation

Le [kit](tools/recette_lot6g4.py) et son [manifeste](tools/recette_lot6g4_sources.json) sont livrés ensemble. Le kit préparé en 6H.16.2 vérifie 41 empreintes de sources ; ne pas régénérer le manifeste pour contourner une différence. Il neutralise dotenv avant l’import applicatif, vide les paramètres Aiven, impose SQLite `:memory:` et bloque les accès hors du périmètre prévu. Python `-I -B` ne constitue pas, à lui seul, ce confinement.

Aucun `.env`, certificat distant, migration ou compte réel n’est nécessaire. Le schéma est créé en mémoire pour cette séance ; `create_all()` ne migre pas une base existante. Le dossier temporaire de preuves doit rester hors du dépôt.

## Démonstration humaine

Si une séance fonctionne déjà, utiliser sa console privée et ses accès courants. **Ne pas relancer le kit, recréer les comptes ou libérer le port 5064 en interrompant un autre processus.**

Pour une nouvelle séance, obtenir une autorisation distincte de lancement du serveur. Dans une console privée, hors projection, sans transcription, redirection, capture ou `Tee-Object` :

```powershell
.\.venv\Scripts\python.exe -I -B tools/recette_lot6g4.py --serve --autorisation-execution-confirmee
```

Le marqueur ne remplace pas l’autorisation. Attendre l’état `READY`, puis l’annonce de l’écoute locale. Le kit n’ouvre pas de navigateur. Après accord pour le navigateur, ouvrir manuellement `http://127.0.0.1:5064/`, dans un contexte neuf sans profil personnel. Utiliser un second contexte indépendant pour le deuxième membre ; une simple deuxième fenêtre partageant les cookies ne suffit pas.

### Création des comptes fictifs

Le kit génère automatiquement **trois comptes** : un administrateur et deux membres. Ils sont stockés dans SQLite en mémoire, avec des mots de passe hachés côté base. Les accès générés sont affichés uniquement dans la console privée du processus qui vient de démarrer ; aucun accès prédéfini n’est fourni par la documentation.

À chaque redémarrage, de nouveaux mots de passe et une nouvelle clé de session sont générés. Un bloc d’accès d’une ancienne séance ne convient pas à une nouvelle séance. Ne pas copier les valeurs dans Git, un chat, un rapport, une capture, un fichier de comptes ou un journal. Ne pas utiliser l’inscription pour compléter les trois comptes de cette démonstration.

### Contrôles avant présentation

1. Vérifier une connexion de chacun des trois comptes depuis les formulaires réels : `/connexion.html` pour les membres, `/admin-connexion.html` pour l’administrateur. Se déconnecter entre comptes partageant un contexte.
2. Vérifier le rôle affiché et les sept valeurs initiales : **2 dossiers / 1 résolu / 1 Cold Case / 3 utilisateurs / 0 commentaire / 0 signalement / 0 proposition en attente**.
3. Ne noter que les résultats et rôles, jamais les saisies ni les cookies. Si le jeu a déjà servi, ses compteurs et le bannissement peuvent avoir changé ; le reçu de démarrage ne décrit pas son état actuel.
4. Montrer lecture d’un dossier, commentaire, ajout/retrait des likes et signalement ; consulter leur résultat dans l’administration. Le bannissement d’un membre est une action de démonstration à annoncer avant confirmation.

Le lot 6H.12 a exécuté ce parcours dans Edge, puis préparé une session neuve dont les trois connexions ont été vérifiées. Cela atteste ces séances, pas les accès de tout processus futur.

Pour terminer une séance dont on a la charge, utiliser Ctrl+C dans sa console de lancement. Les données mémoire disparaissent à l’arrêt. Ne pas arrêter une séance pour renouveler les accès sans accord de son responsable.

### Six histoires originales — mode distinct 6H.16.2

Les versions B d’Anthonioz et de Noirval et les quatre autres textes retrouvés sont disponibles dans un catalogue contrôlé. Titres, résumés et HTML source sont conservés sans correction ; le texte visible reprend tous les intertitres et paragraphes, sans injection HTML. Les témoignages, sources et références de galerie restent conservés dans le catalogue ; leur présentation dédiée et les images relèvent d’un lot ultérieur. Le repli SVG existant reste utilisé.

Pour vérifier le parcours dans une nouvelle SQLite mémoire, sans serveur ni navigateur :

```powershell
.\.venv\Scripts\python.exe -I -B tools/recette_lot6g4.py --histoires-originales --check-histoires
```

Le mode initial contient **6 dossiers / 3 résolus / 3 Cold Cases / 3 utilisateurs / 0 commentaire / 0 signalement / 0 proposition en attente**. Le contrôle ajoute des contributions séparées puis vérifie que les articles demeurent inchangés. Les id SQL sont 101–103 et 201–203 ; les chaînes `h1` à `cc3` restent des identifiants de provenance. Les slugs sont `golden-state-killer`, `chris-watts`, `michelle-carter`, `anthonioz`, `noirval` et `manoir-de-l-ombre`.

Pour une **nouvelle séance autorisée**, utiliser `--histoires-originales --serve --autorisation-execution-confirmee`. Ce mode utilise aussi `127.0.0.1:5064` : ne pas l’exécuter lorsqu’une séance occupe déjà ce port et ne pas arrêter cette séance sans accord. L’ajout de fichiers ne modifie pas la mémoire d’un serveur déjà lancé. Les comptes restent éphémères et leurs accès restent dans sa console privée.

Sans `--histoires-originales`, le jeu scolaire de deux dossiers et son `--check-journey` restent inchangés. Ne pas combiner ce dernier avec le mode historique. Le manifeste de cette version contrôle **41 sources**, dont le nouveau catalogue ; ses protections restent actives. Aucun accès MySQL/Aiven ni migration n’est nécessaire.

## Mode persistant facultatif, séparé de la recette

Le [guide persistant](docs/soutenance/DEMO_PERSISTANTE.md) décrit une autre procédure : six histoires originales et exactement trois comptes lors d'une initialisation explicite, conservés dans `instance/demo-persistante/portfolio.sqlite3`. Le responsable choisit les mots de passe dans sa console privée ; ne pas utiliser ou recopier ceux d'une ancienne séance mémoire.

Le lanceur `tools/demo_persistante.py` sépare création, contrôle, service sur `127.0.0.1:5066`, sauvegarde et restauration. Rien n'est créé par sa simple présence ou son aide. Le démarrage ouvre uniquement la base existante, avec sa clé et son cookie propres. Il ne lit pas dotenv et ne se connecte pas à Aiven. La base et ses sauvegardes sont privées et ignorées par Git.

Ce mode ne transfère aucune donnée de 5064 et ne remplace pas la recette scolaire, ses accès éphémères ou ses protections. Conserver le serveur actuel. Les tests dédiés portent sur des bases temporaires et une réouverture interprocessus ; le détail des opérations et de leurs limites figure dans le guide.

## Recette automatique distincte

Cette commande est facultative pour une vérification ultérieure ; elle n’est pas nécessaire pour répéter des contrôles déjà réussis :

```powershell
.\.venv\Scripts\python.exe -I -B tools/recette_lot6g4.py --check-journey
if ($LASTEXITCODE -ne 0) { throw 'Recette non validee.' }
```

Ce mode utilise un processus séparé, sans serveur ni navigateur. Il exécute 43 requêtes WSGI en sept groupes, avec un quatrième compte synthétique créé par le scénario d’inscription. Son jeu n’est pas celui de la séance humaine. Attendus : `journey: PASS`, sept gardes à zéro, `server_started: false` et `browser_started: false`.

Ne pas combiner `--check-journey` et `--serve`. Ne pas lancer `run_local.py`, Flask directement ou une commande Alembic pour reproduire cette recette : ces autres procédures ne garantissent pas la même cible de données.

## Limites de la livraison

Le code est publié, mais l’application reste une démonstration locale. Les migrations sur base existante, MySQL/Aiven en production, la durabilité et la concurrence réelle ne sont pas validés par SQLite mémoire. Les notices ne constituent pas une politique RGPD finalisée. Les fonctions partielles sont détaillées dans le [README](README.md).

La [provenance des ressources livrées](docs/soutenance/PROVENANCE_RESSOURCES.md) distingue le SVG géométrique fourni des ressources externes éventuelles. Les anciens visuels et jeux narratifs non livrés ne doivent pas être ajoutés pour faire fonctionner la recette synthétique.
