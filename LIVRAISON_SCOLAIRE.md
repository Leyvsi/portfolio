# Installation et démonstration scolaire

Projet Les Petits Enquêteurs, pour une soutenance locale Holberton. Le code livré ne déploie aucun site public. Le kit [recette_lot6g4.py](tools/recette_lot6g4.py) prépare les données fictives, neutralise dotenv et impose SQLite en mémoire.

## Prérequis

La reproduction a été vérifiée sur Windows AMD64 avec Python 3.13.0. Python doit être installé séparément. Le frontend n'a pas d'étape de compilation ; Node.js est nécessaire uniquement pour les tests JavaScript.

Depuis une copie neuve du dépôt, créer un environnement sans paquets système :

```powershell
python -I -B -m venv .venv
```

Installer les versions directes et transitives fixées. Avec un accès réseau autorisé sur la machine de destination :

```powershell
.\.venv\Scripts\python.exe -I -B -m pip --isolated install --requirement backend/requirements.txt --constraint docs/soutenance/CONTRAINTES_INSTALLATION_LOT6H2.txt
.\.venv\Scripts\python.exe -I -B -m pip --isolated check
```

Pour une installation hors ligne, fournir séparément les roues compatibles et leurs empreintes vérifiées. Elles ne font pas partie du dépôt. Remplacer le chemin ci-dessous ; aucune roue n'est téléchargée par cette variante :

```powershell
$rouesPortfolio = 'C:\chemin\vers\wheelhouse-verifie'
.\.venv\Scripts\python.exe -I -B -m pip --isolated install --no-index --no-cache-dir --only-binary=:all: --find-links $rouesPortfolio --requirement backend/requirements.txt --constraint docs/soutenance/CONTRAINTES_INSTALLATION_LOT6H2.txt
.\.venv\Scripts\python.exe -I -B -m pip --isolated check
```

Arrêter si une commande échoue. Un venv, Python, Node et les roues restent des prérequis externes ; le dépôt ne fournit pas un système complet.

## Vérification automatique sans serveur

```powershell
.\.venv\Scripts\python.exe -I -B tools/recette_lot6g4.py --check-journey
```

Le kit vérifie son manifeste de sources, les dix pages et vingt ressources publiques, puis 43 requêtes WSGI réparties en sept groupes. Il contrôle inscription/connexion, histoires et Cold Cases, commentaire, signalement, likes et CSRF, rollback, administration, sept valeurs rapprochées de SQL, archivage/restauration et bannissement. Le SVG fourni est le repli local des dossiers.

Résultat attendu : `journey: PASS`, sept gardes à zéro, `server_started: false`, `browser_started: false`. Les reçus sont créés sous Temp. La base synthétique disparaît à la fin du processus. Cette commande ne lance ni navigateur, ni écoute réseau, ni migration.

Le manifeste a été adapté pour la livraison aux deux ressources effectivement changées : sélection d'image dans `frontend/app.js` et nouveau SVG. Les autres sources figées et les protections du kit sont conservées. Ne pas renouveler les empreintes pour contourner un échec.

## Démonstration devant le jury

Le kit propose un mode `--serve --autorisation-execution-confirmee` sur `127.0.0.1:5064`, à utiliser dans une séance de démonstration autorisée. Il crée des accès fictifs éphémères à chaque processus. Mahamadou organise leur conservation privée pour le jour J. Ne pas conserver ces valeurs dans Git ou une capture. Arrêter avec Ctrl+C ; ne pas combiner `--serve` et `--check-journey`.

Ne pas remplacer ce kit par `run_local.py` pour la reproduction : le lanceur normal lit la configuration locale et peut viser une base persistante. Les migrations candidates ne doivent être appliquées à une cible réelle que dans une intervention distincte approuvée.

Voir les [supports de soutenance](docs/soutenance/README.md), la [validation](docs/soutenance/VALIDATION_SCOLAIRE.md) et la [provenance des ressources](docs/soutenance/PROVENANCE_RESSOURCES.md). Les tests historiques, la recette actuelle et la validation visuelle sont des preuves distinctes. Le projet n'est pas présenté comme entièrement conforme au RGPD.
