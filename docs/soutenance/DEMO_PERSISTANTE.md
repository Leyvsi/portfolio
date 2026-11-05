# Démonstration locale persistante

Ce mode conserve sur disque les comptes et les contributions. Il est distinct du kit scolaire SQLite mémoire et reste destiné à une utilisation locale. Aucun accès MySQL/Aiven ni migration d'une ancienne base n'est nécessaire.

Le lanceur est [tools/demo_persistante.py](../../tools/demo_persistante.py). Python 3.13 et les dépendances de [backend/requirements.txt](../../backend/requirements.txt) sont requis, avec SQLAlchemy 2.0.53 conformément au manifeste existant. Le contrôle des sources refuse une différence ; ne pas renouveler les empreintes pour contourner ce refus.

L'ajout du lanceur ne crée aucune base ni aucun compte. La création réelle et le lancement sont deux actions explicites séparées. Ne pas interrompre une démonstration existante sur 5064 pour utiliser ce mode.

## Données et séparation des modes

| Élément | Mode persistant | Kit scolaire existant |
|---|---|---|
| Base | `instance/demo-persistante/portfolio.sqlite3` | SQLite `:memory:` |
| Comptes | Créés une seule fois, mots de passe choisis en console privée | Accès éphémères générés par le kit |
| Histoires initiales | Six originaux du catalogue approuvé | Deux dossiers scolaires, ou six originaux avec `--histoires-originales` |
| Redémarrage | Ouvre uniquement la base existante | Recrée une mémoire de démonstration |
| Adresse | `http://127.0.0.1:5066/` | `http://127.0.0.1:5064/` |

Les comptes initiaux ont pour pseudonymes **`admin`, `Alice`, `Bob`**, avec respect de la casse. La connexion utilise le pseudonyme, pas l'e-mail. Seul `admin` est administrateur. Les trois e-mails, obligatoires et uniques, sont saisis dans la console privée ; aucune adresse personnelle n'est fournie par la documentation.

Les six titres, résumés et contenus proviennent sans correction du [catalogue historique](../../tools/fixtures/dossiers_historiques.json), versions B pour Anthonioz et Noirval. Catégories 1/2, id 101–103 et 201–203 et slugs sont conservés. Aucun compte ou contenu de la mémoire 5064 n'est transféré automatiquement.

## Préparer la console

Depuis la racine du projet, dans une console privée sans projection, transcription, redirection ou capture :

```powershell
.\.venv\Scripts\python.exe -I -B tools/demo_persistante.py --help
```

Cette commande d'aide n'ouvre pas de base. Ne pas transmettre de mot de passe à une commande, une variable d'environnement, un fichier, un pipe ou un message. Ne pas capturer les réponses d'authentification, cookies ou jetons de session.

## Créer les trois comptes et les six histoires

Lorsque la création effective est autorisée :

```powershell
.\.venv\Scripts\python.exe -I -B tools/demo_persistante.py init
```

Pour chaque pseudonyme affiché, saisir son e-mail, puis deux fois le mot de passe sans écho. La politique existante est conservée : 8–50 caractères avec majuscule, minuscule, chiffre et caractère spécial reconnu. Les espaces du mot de passe ne sont pas retirés. Une console sans saisie confidentielle provoque un refus.

Le hachage utilise `User.set_password()` et Werkzeug. Aucune valeur brute ni aucun hachage n'est affiché. La clé de session est générée automatiquement sans affichage. Le dossier privé Windows reçoit une DACL réservée au compte qui exécute la commande ; les fichiers et journaux héritent de cette protection.

L'initialisation prépare un dossier neuf, contrôle les textes et les contraintes, puis publie le jeu complet sans remplacer une destination existante. Son état initial comporte **3 comptes, 6 dossiers, 2 catégories et aucune contribution artificielle**. Si `instance/demo-persistante/` existe déjà, même incomplet, l'initialisation refuse ; elle ne réinitialise ni accès ni contenu.

## Contrôler puis démarrer

```powershell
.\.venv\Scripts\python.exe -I -B tools/demo_persistante.py check
```

Le contrôle vérifie le schéma, l'intégrité, les rôles initiaux et les six textes, sans réparation. Il signale les originaux manquants, modifiés ou archivés. Un écart de contenu ou de rôle donne un code de sortie non nul. Un archivage seul est rapporté et ne réactive pas le dossier.

Pour une nouvelle séance autorisée :

```powershell
.\.venv\Scripts\python.exe -I -B tools/demo_persistante.py serve
```

Ouvrir ensuite manuellement `http://127.0.0.1:5066/`. Le lanceur n'ouvre pas de navigateur. Il ne crée ni table ni compte au démarrage et refuse une base absente ou un schéma inconnu. Aucun remplacement de processus si le port est occupé. Il n'utilise ni debug ni reloader.

Fermer uniquement cette instance avec Ctrl+C dans sa propre console, puis relancer la même commande pour retrouver ses données. Cela ne donne aucune autorisation d'arrêter le serveur 5064.

La clé et le cookie `lpe_persistante` sont propres à ce mode. Les protections CSRF, `HttpOnly`, `SameSite=Lax` et les permissions existantes restent actives. `Secure` est adapté au HTTP de boucle locale. Pour utiliser simultanément les trois identités, prendre trois profils ou contextes de navigateur indépendants ; des onglets d'un même profil partagent une session. Le changement de port seul n'isole pas les cookies du même hôte.

Un compte conservé sur disque n'est pas une session infinie. Si la clé change, une reconnexion peut être nécessaire. L'inscription publique existante peut créer d'autres utilisateurs classiques après l'initialisation ; elle ne peut pas créer un administrateur via un champ envoyé par le client.

## Sauvegarder hors service

Après fermeture du seul serveur persistant :

```powershell
.\.venv\Scripts\python.exe -I -B tools/demo_persistante.py backup
```

La commande utilise l'API de sauvegarde SQLite et retourne un identifiant local. Le dossier correspondant sous `backups/demo-persistante/` contient la base complète et un manifeste d'intégrité, sans clé de session. Chaque sauvegarde est nouvelle ; aucune sauvegarde précédente n'est remplacée. Un verrou empêche cette commande pendant que le serveur persistant fonctionne.

La base complète conserve comptes, hachages, histoires, commentaires, théories, votes, likes de commentaires, signalements, propositions et mises à jour. Les fichiers SQLite contiennent des données privées et ne sont pas chiffrés par SQLite standard : ne pas les publier ou partager sans protection adaptée.

## Restaurer explicitement

Arrêter uniquement le mode persistant dont on a la charge. Utiliser l'identifiant local retourné par `backup`, jamais un chemin vers une autre base. Exemple de procédure sans valeur d'accès :

```powershell
$sauvegardeLocale = Read-Host 'Identifiant local de sauvegarde'
.\.venv\Scripts\python.exe -I -B tools/demo_persistante.py restore $sauvegardeLocale --remplacer-base-locale --renouveler-cle-session
```

`--remplacer-base-locale` est obligatoire si un jeu existe. Avant remplacement, le lanceur crée une sauvegarde de sécurité de l'état actuel. Il valide le manifeste et le schéma de la source, restaure dans un fichier de travail, puis remplace uniquement le fichier canonique. Il refuse une annexe SQLite présente plutôt que de la supprimer. Dans une destination sans jeu existant, le dossier neuf est publié sans écrasement.

`--renouveler-cle-session` invalide les anciennes sessions sans changer les mots de passe. Les trois comptes se reconnectent avec les accès choisis initialement. La clé est remplacée avant le fichier de base : si le remplacement de la base échoue ensuite, la base actuelle reste présente mais une reconnexion peut déjà être nécessaire.

Une restauration revient à la date de la sauvegarde : contributions, rôles et bannissements postérieurs peuvent être perdus. Vérifier cette conséquence avant d'exécuter la commande. Refaire `check` avant de lancer `serve`. Le contrôle ne recrée pas un dossier supprimé intentionnellement et ne lève pas un archivage.

La procédure conserve les sauvegardes sous le même projet. Pour un transfert vers un autre ordinateur, transporter les fichiers privés de manière protégée et vérifier les ACL sous le nouveau compte Windows ; ce transfert n'est pas automatique.

## Tests et limites

```powershell
.\.venv\Scripts\python.exe -I -B tests/test_demo_persistante.py
```

Ces tests créent uniquement des bases jetables dans des répertoires temporaires et des mots de passe générés en mémoire, jamais codés en dur, enregistrés ou affichés. Le scénario interprocessus ferme complètement un premier processus puis authentifie de nouveau les trois comptes et relit les contributions dans un second. Les essais de compte supplémentaire, archivage et restauration restent dans ces copies.

Le contrôle du dashboard porte sur ses ressources et les réponses API des sept indicateurs ; ce n'est pas une nouvelle validation visuelle Edge du mode persistant. Les validations visuelles antérieures restent distinctes.

Le lanceur neutralise dotenv/Aiven dans son processus, impose la SQLite locale, bloque les connexions réseau sortantes et les ouvertures SQLite alternatives pendant l'exécution de Flask, et active les clés étrangères. Il ne constitue pas un confinement contre un utilisateur capable de modifier les fichiers Python ou les données du compte Windows. Les modèles sont créés à neuf uniquement dans `init` ; aucune migration d'une ancienne base n'est disponible ici.

Le mode utilise le journal SQLite `DELETE` et refuse un autre mode. Les annexes et sauvegardes restent ignorées par Git. Les droits du compte Windows courant doivent correspondre à ceux qui ont initialisé le dossier.

Aucune récupération automatique de mot de passe, vérification d'e-mail, limitation de tentatives ou validation de sécurité en production n'est ajoutée. Aucune conformité RGPD complète n'est revendiquée. Le kit mémoire et son manifeste restent inchangés et indépendants de ce stockage.
