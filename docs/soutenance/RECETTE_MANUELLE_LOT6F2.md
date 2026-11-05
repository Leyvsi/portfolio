# Recette manuelle Edge — lot 6F.2

[Bilan](BILAN_LOT6F2.md) · [Scénario oral de 14 minutes](SCENARIO_SOUTENANCE_LOT6F2.md)

**Préparée le 1er novembre 2026 ; NON EXÉCUTÉE dans Edge.** Aucun serveur ou navigateur lancé pendant 6F.2. La section 5 de l'autorisation exige une autorisation spécifique d'exécution, après confirmation de l'isolation. Le résultat READY ci-dessous ne donne pas cette autorisation. Ne pas utiliser CDP, un profil personnel automatisé, le pare-feu ou des changements Windows.

## 1. Préparation sûre et reproductible

Le [kit dédié](../../tools/recette_lot6f2.py) réutilise les vrais modèles, vues et middleware statique. Il neutralise dotenv avant import, vide les six paramètres Aiven, génère une clé de session éphémère et impose SQLite `:memory:`. Les connexions fichier/MySQL, ATTACH/DETACH, migrations, lectures privées, écritures du dépôt et connexions réseau sortantes sont bloquées. Les FK sont activées et vérifiées. Aucun fichier de base n'est créé ; arrêter détruit les données de cette recette.

Le [manifeste figé](../../tools/recette_lot6f2_sources.json) épingle 65 sources relues. Les empreintes normalisent uniquement CRLF/LF pour le transfert vers une autre machine. Une source différente provoque un arrêt : ne pas régénérer automatiquement le manifeste ni désactiver la vérification.

Sur une machine de l'école : utiliser une copie autorisée des sources effectives incluant les fichiers non committés 6F.1/6F.2 et ce kit. Un simple clone du HEAD historique ne suffit pas. Exclure `.env`, certificats, cookies, bases, secrets, sept anciennes exclusions et données privées. Disposer de Python 3.13, des neuf versions fixées dans `backend/requirements.txt` et d'un environnement virtuel séparé. Aucun téléchargement/installation n'est effectué par le kit ; faire inspecter toute variante de plateforme non prise en charge.

Depuis la racine de cette copie, inspection sans serveur :

```powershell
& .\.venv\Scripts\python.exe -I -B tools/recette_lot6f2.py
```

Cette commande a réellement été exécutée ici avec **READY**, FK actives, aucun fichier de base, aucun serveur/navigateur et compteurs interdits à zéro. Elle crée uniquement un dossier neuf de preuves sous Temp et le schéma courant dans une mémoire vide. `create_all()` dans cette mémoire n'est ni une migration ni une vérification du schéma MySQL existant. Les sessions, comptes et écritures de recette n'atteignent jamais la base du site.

**Périmètre des ressources :** trois pages de compte référencent encore `donnees.js` (inscription, connexion, connexion administrateur). Ce fichier reste non examiné et exclu. Le kit refuse sa requête en 403 sans lire son contenu ; les contrôleurs `api.js`/`app.js` relus continuent séparément leur parcours. Le test intégré a vérifié ces contrôleurs avec cette omission explicite. **Ne pas annoncer une recette de tous les scripts de ces pages.** Le 403 de cette ressource est une limite connue, pas une réussite. Pour une recette complète sans cette exclusion, faire autoriser sa revue ou la suppression des trois balises historiques ; aucune de ces modifications n'est effectuée ici.

## 2. Lancement proposé, uniquement après autorisation distincte

```powershell
# NON EXÉCUTÉ pendant 6F.2. Le marqueur atteste l'accord reçu ; il ne le remplace pas.
& .\.venv\Scripts\python.exe -I -B tools/recette_lot6f2.py --serve --autorisation-execution-confirmee
```

Le kit prévoit une écoute unique sur **127.0.0.1:5062**, sans debug, reloader ou ouverture automatique du navigateur. Aucun repli vers un autre hôte/port ou une autre base. Si le port est occupé, arrêter et diagnostiquer ; ne tuer aucun processus inconnu. La branche d'écoute n'a pas été exécutée ici : ses conditions de démarrage restent à confirmer pendant la recette autorisée.

Les gardes protègent le processus Python ; ils ne confinent pas Edge et ne changent aucun de ses réglages. Rester sur les pages locales du protocole, sans Swagger dépendant d'assets CDN ni ressource distante. Aucune preuve de confinement d'un navigateur réel n'est revendiquée.

Ouvrir Edge **manuellement**, dans une fenêtre InPrivate distincte, et saisir `http://127.0.0.1:5062/`. Ne pas utiliser `file://`, `localhost:5000`, le site réel ou une session administrateur personnelle. Le kit prépare deux dossiers fictifs dans les catégories 1/2 et un administrateur `jury6f2_admin`. Son mot de passe éphémère apparaît seulement lors du démarrage autorisé, dans la console locale ; ne pas le capturer ni le copier dans un rapport. L'inscription publique n'accorde jamais le rôle administrateur.

Avant de poursuivre : contrôler l'adresse, READY, la mémoire/FK et l'absence d'URL MySQL dans les preuves ; ne jamais ouvrir une configuration privée pour le vérifier. Noter le dossier de preuves, date et opérateur, sans identifiant personnel inutile. Une actualisation de page conserve la base mémoire tant que le processus reste actif ; un arrêt/redémarrage la recrée vide.

## 3. Feuille de recette à renseigner

Inscrire **PASS / FAIL / NON EXÉCUTÉ**, le résultat observé et une preuve expurgée pour chaque ligne. Les attentes ci-dessous ne sont pas des résultats déjà obtenus dans Edge. Les valeurs initiales viennent des vraies lignes fictives du kit : deux dossiers dont un par catégorie, un compte administrateur, zéro commentaire, signalement ou proposition. Aucun nombre n'est écrit dans le code du dashboard pour simuler ce résultat.

| ID | Action manuelle | Résultat attendu et moyen de vérifier |
|---|---|---|
| M01 | Ouvrir accueil, Histoires, Cold Cases et un dossier | Deux dossiers disponibles ; titre, slug et catégorie corrects ; illustration SVG de repli ; aucune donnée de la base réelle |
| M02 | Parcourir au clavier, tester une fenêtre étroite | Labels et focus utilisables, notices lisibles, retours de ligne ; contrôler réellement les éléments masqués |
| M03 | Ouvrir inscription ; saisir un pseudo unique et une adresse `@example.invalid`, mot de passe fictif conforme | Notice avant les champs ; compte créé après 201, mot de passe effacé ; le 403 connu de donnees.js est consigné séparément |
| M04 | Connexion classique, retour à l'accueil | Connexion réelle ; pseudo et Déconnexion affichés ; ne pas afficher cookies/jetons ni exporter un HAR sensible |
| M05 | Ouvrir `dossier.html?slug=recette-6f2` | Dossier réel id 17 ; commentaires vides, formulaire et notice présents |
| M06 | Publier un texte distinct, un seul envoi puis double clic volontaire sur un deuxième texte | Chaque intention confirmée crée une ligne ; un double clic en cours n'en crée pas deux. Attendre le 201 avant de conclure ; compter les intentions réellement effectuées |
| M07 | Actualiser les commentaires puis quitter/revenir à la fiche | Textes sauvegardés présents ; succès non fabriqué depuis une fixture navigateur |
| M08 | Publier un texte littéral tel que `<b>test isolé</b>` | Balises visibles en texte, aucune mise en forme HTML injectée. Ne pas tester un code externe ou des données d'un tiers |
| M09 | Signaler le premier commentaire, vérifier sa cible, Annuler | Numéro et auteur corrects ; aucune écriture à l'annulation ; motif non réattribué à un autre commentaire |
| M10 | Rouvrir le bon signalement, saisir un motif distinct, Confirmer une fois | 201 puis confirmation réelle ; commentaire toujours public, motif absent de la liste publique ; le statut ne devient pas automatiquement Traité |
| M11 | Depuis l'accueil, Déconnexion ; revenir à la fiche et envoyer un nouveau brouillon | Demande de connexion, texte conservé, aucun faux succès ni nouvelle ligne ; lectures publiques toujours possibles |
| M12 | Ouvrir dashboard sans connexion puis avec un membre | Données privées masquées et refus ; HTML accessible ne signifie pas autorisation des API privées |
| M13 | Déconnecter le membre ; connecter l'administrateur via sa page ; ouvrir dashboard | Le motif et l'id du commentaire de M10 sont retrouvés dans Signalements, avec statut En attente. Aucune résolution de statut n'est ajoutée |
| M14 | Comparer les sept compteurs, les listes puis Actualiser | Dossiers et catégories depuis les actifs ; utilisateurs/commentaires/reports depuis `/stats` ; pending depuis `/proposals`. Comparer aux actions effectuées et aux lectures API autorisées, jamais imposer des chiffres arbitraires |
| M15 | Déconnecter l'administrateur depuis l'accueil ; actualiser une ancienne page admin | `/me` refuse ; cartes privées masquées et sept valeurs `—`. Sans requête, un autre onglet n'est pas nettoyé instantanément : limite existante |
| M16 | Ouvrir un slug absent ; tenter un texte vide ; simuler une panne uniquement selon une procédure locale approuvée | 404 distinct d'une liste vide ; validations visibles ; aucun succès si refus. Après résultat incertain, ne pas renvoyer : relire ou faire vérifier par l'administration |

La conformité des cookies dans Edge, la lisibilité responsive, le clavier et le fonctionnement continu navigateur/API restent à observer réellement. Un refus CSRF, timeout ou perte après commit n'est pas déclaré reproduit manuellement si seul le harnais l'a exercé. Ne pas interrompre le processus pour prétendre vérifier un commit incertain : cela détruit cette base mémoire.

Les actions de bannissement/archivage/restauration/purge restent conservées par non-régression. La démonstration prioritaire ne nécessite pas leur exécution ; les expliquer à partir des preuves. N'improviser aucune suppression définitive ou opération sur la base du site.

## 4. Arrêt et replis

Arrêter le seul processus de recette au clavier avec **Ctrl+C**, fermer la fenêtre InPrivate et ne conserver que des preuves expurgées. Ne supprimer aucun fichier du dépôt ou des campagnes précédentes. Aucune persistance après redémarrage n'est revendiquée ; la sauvegarde de sources 6E.1 n'est pas une sauvegarde des interactions.

Si Edge, les dépendances, le port ou l'isolation échouent : noter FAIL ou NON EXÉCUTÉ, conserver le diagnostic et utiliser les preuves WSGI/SQLite/DOM de 6F.2 comme repli explicitement identifié. Sur une autre machine, reprendre l'inspection du kit avant de demander l'autorisation de lancement. Ne pas modifier le pare-feu, les permissions, les navigateurs, le manifeste ou les protections pour contourner un échec.
