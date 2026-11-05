# Installation isolée et reproduction — lot 6H.2

> Copie publique de référence : les chemins personnels et liens de travail internes sont retirés. Les preuves et commandes historiques gardent leur date et leur périmètre ; utiliser le README actuel pour le lancement.

Vérification du 2 novembre 2026 : copie sélectionnée neuve, environnement Python neuf, installation réussie et lancement complet de l'application par le kit existant. Il s'agit du même PC Windows, avec Python 3.13.0 AMD64 préexistant. Un autre PC, Linux, une migration d'une base existante et la production ne sont pas testés.

## Résultat et preuves

Les neuf dépendances directes de `backend/requirements.txt` et les dépendances transitives sont installées dans un nouveau venv sans accès aux paquets du système. Les 25 versions sont figées dans [les contraintes](CONTRAINTES_INSTALLATION_LOT6H2.txt). Le téléchargement PyPI a été autorisé séparément ; l'installation a ensuite utilisé les roues locales avec `--no-index`. `pip check` réussit. Aucun logiciel global ni paquet JavaScript n'est installé. Le frontend utilise les fichiers HTML/CSS/JS existants, sans étape npm ou build.

Les reçus installation (pièce interne non diffusée), roues et SHA-256 (pièce interne non diffusée), parcours HTTP (pièce interne non diffusée), échanges sans corps ni cookies (pièce interne non diffusée), parcours WSGI (pièce interne non diffusée) et service des images (pièce interne non diffusée) séparent les contrôles. `installation.json` décrit seulement les dépendances : son indicateur de lancement encore faux est complété par le reçu HTTP PASS, et ne doit pas être interprété isolément.

La copie initiale contient 153 fichiers : les 145 revalidés de 6H.1, le manifeste 6H.1, les quatre WebP nouvellement examinés et trois utilitaires/contraintes 6H.2. Seul le contrôleur de vérification, hors application, a ensuite reçu une correction de synchronisation de son observation SQL. Le site, les tests existants, les images et les 40 sources figées du kit restent identiques. Les documents finaux ajoutés après cette recette ne modifient pas les sources exécutées.

## Parcours effectivement exécuté

Inspection du kit, puis **43 requêtes WSGI**, puis **71 requêtes HTTP réelles sur 127.0.0.1:5064** : inscription/connexion, deux catégories, théorie, proposition pending, commentaire, refus CSRF, signalement contextualisé, likes ajout/unicité/retrait/relecture, refus des lectures admin au membre, administration et sept agrégats égaux à SQL, bannissement de la session ouverte, archivage/restauration sans perte des contributions, déconnexion et refus des données privées. Les 20 ressources du kit et l'accueil sont servis avec `Cache-Control: no-store` et leurs octets correspondent à la copie.

Les sept valeurs sont **2, 1, 1, 4, 1, 1, 1** dans ce nouveau scénario : un quatrième utilisateur est inscrit et une proposition est créée. Cela ne contredit pas les **2, 1, 1, 3, 1, 1, 0** de la recette Edge 6G.5, qui utilisait d'autres données synthétiques. Dix tables, FK actives, vérification FK vide, aucun fichier SQLite, aucun accès MySQL/Aiven. Les sept gardes comptent zéro violation. Serveur arrêté, connexion au port refusée après arrêt.

Le premier essai n'a pas abouti au reçu final : le client pouvait lire l'instantané SQL de la requête précédente. Le contrôleur a été corrigé pour terminer l'observation avant d'envoyer le corps HTTP. Le second essai complet réussit ; aucune route applicative ni garde du kit n'a été modifiée. Les cinq images sont également vérifiées en WSGI statique séparé, sans importer le backend.

Les **854 PASS du 1er novembre restent historiques** ; ils ne sont ni relancés intégralement ni additionnés aux requêtes ci-dessus. Aucun nouveau parcours humain Edge n'a été demandé ou simulé dans ce lot.

## Configuration et lancement sûr

Le point d'entrée habituel `run_local.py` charge le `.env` et ne crée pas le schéma. Il n'est donc pas lancé directement pour cette recette. Le kit [recette_lot6g4.py](../../tools/recette_lot6g4.py) importe réellement les vues et modèles, neutralise dotenv avant l'import, vide les six variables `AIVEN_DB_*`/`AIVEN_CA_CERT`, configure exactement SQLite `:memory:`, crée un schéma synthétique et démarre le même middleware local. Sa liste de 40 empreintes n'est pas renouvelée. Les migrations restent sept révisions en une chaîne ; elles sont inspectées dans l'audit 6H.1, sans application. `create_all` dans une base mémoire neuve ne valide pas une migration MySQL.

L'outil INSTALLER_LOT6H2.py (pièce interne non diffusée) documente l'installation avec Internet autorisé. Il refuse une destination existante et vérifie les empreintes des deux listes : requirements `932bc4952dbef5b0158696a66d34671899c0e70aee1171451de30401fd1b6af8`, contraintes `ffde23b77effbf629a44aa3613296db6e363b4da69ba039d075dbfa8187e5dc1`. La sauvegarde privée conserve également les 25 roues, sans copier le venv. Ces roues sont destinées à Windows/Python 3.13 AMD64 et aux paquets universels présents ; elles ne constituent pas un installateur Python ou Node.

Pour reproduire hors réseau sur une machine compatible, depuis la source récupérée, créer un nouveau venv avec un Python déjà installé, puis installer exclusivement depuis le wheelhouse de la sauvegarde :

```powershell
python -I -B -m venv C:\chemin\temp\nouveau-venv
C:\chemin\temp\nouveau-venv\Scripts\python.exe -I -B -m pip --isolated install --no-index --find-links C:\chemin\sauvegarde\annexes\wheelhouse --requirement backend\requirements.txt --constraint docs\soutenance\CONTRAINTES_INSTALLATION_LOT6H2.txt
C:\chemin\temp\nouveau-venv\Scripts\python.exe -I -B -m pip --isolated check
```

Les chemins sont des exemples à adapter, pas des dossiers créés par ce document. Vérifier d'abord les SHA des roues et des sources à l'aide des manifestes sauvegardés. La création du venv dépend d'un Python préinstallé ; les commandes ci-dessus ne téléchargent rien.

Pour la vérification automatique complète, copier la sélection de sources dans un dossier neuf `portfolio-lot6h2-*` sous Temp, par exemple un sous-dossier `worktree`, puis exécuter avec ce nouveau Python :

```powershell
C:\chemin\temp\nouveau-venv\Scripts\python.exe -I -B C:\chemin\Temp\portfolio-lot6h2-exemple\worktree\docs\soutenance\VERIFIER_INSTALLATION_LOT6H2.py --project C:\chemin\Temp\portfolio-lot6h2-exemple\worktree --python C:\chemin\temp\nouveau-venv\Scripts\python.exe --evidence-root C:\chemin\Temp\portfolio-lot6h2-exemple\preuves-neuves
```

Cet outil crée le répertoire de preuves, démarre temporairement l'écoute loopback et l'arrête automatiquement. Le port 5064 doit être libre. Il ne doit pas être lancé sur le dépôt original. Pour une démonstration humaine distincte, les commandes du [guide 6H.1](LANCEMENT_AUTRE_PC_LOT6H1.md) restent applicables avec l'autorisation d'écoute déjà donnée ; les identifiants synthétiques affichés sont éphémères et ne doivent pas être archivés.
