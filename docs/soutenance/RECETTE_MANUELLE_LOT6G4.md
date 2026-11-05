# Recette manuelle locale — kit 6G.4

> Copie publique de référence : les chemins personnels et liens de travail internes sont retirés. Les preuves et commandes historiques gardent leur date et leur périmètre ; utiliser le README actuel pour le lancement.

[Bilan 6G.4](BILAN_LOT6G4.md) · [Audit 6G.3](BILAN_LOT6G3.md) · [Kit](../../tools/recette_lot6g4.py)

**Préparation et vérifications sans serveur réalisées le 1er novembre 2026. L’écoute locale et Microsoft Edge ne sont pas lancés dans ce lot. Leur exécution demande une autorisation distincte.** Le marqueur de ligne de commande constate cet accord ; il ne le remplace pas.

## Avant de commencer

Utiliser les sources locales incluant les modifications non committées, Python 3.13 et les dépendances déjà installées de `backend/requirements.txt` ; le kit vérifie SQLAlchemy 2.0.53. Aucun téléchargement automatique. Sur une autre machine, transférer seulement une copie autorisée des sources figées ; exclure configuration privée, bases, certificats, cookies, CSV et anciennes données. Faire réinspecter toute variante de plateforme.

Le kit crée un **schéma neuf de dix tables dans SQLite `:memory:`**, avec FK actives. Aucune migration Alembic n’est jouée. Il fournit trois comptes fictifs et deux dossiers actifs : un par catégorie 1/2. Aucun commentaire, signalement ou like de remplissage au lancement manuel. Les comptes et leurs mots de passe temporaires apparaîtront uniquement dans la console du lancement autorisé ; ne pas les capturer ou les réutiliser.

Les anciens compteurs incompatibles ne sont pas convertis. Pour une base existante, cette recette ne remplace ni l’inventaire, ni la sauvegarde, ni la migration et sa procédure de reprise. Le risque DDL table créée/index absent reste décrit dans le bilan. Aucune compatibilité MySQL n’est déduite de cette mémoire SQLite.

## Vérifications disponibles sans écoute

Depuis `[chemin local privé retiré]`, dans PowerShell :

```powershell
& .\.venv\Scripts\python.exe -I -B .\tools\recette_lot6g4.py --probe-isolation
& .\.venv\Scripts\python.exe -I -B .\tools\recette_lot6g4.py
& .\.venv\Scripts\python.exe -I -B .\tools\recette_lot6g4.py --check-journey
```

Chaque commande utilise son propre dossier de preuves et sa propre mémoire. La première vérifie les refus avant entrée/sortie, sans importer l’application ; ses compteurs positifs sont attendus. La deuxième vérifie ressources, schéma, FK et valeurs SQL ; résultat attendu `READY`, `server_started=false`, `browser_started=false`, sept compteurs de garde à zéro. La troisième réalise un parcours API WSGI complet et des cas d’erreur dans une autre mémoire jetable ; elle n’exécute pas les contrôleurs JavaScript. Les preuves DOM/API complémentaires du bilan sont distinctes.

Le kit ne renouvelle jamais son [manifeste de 40 sources](../../tools/recette_lot6g4_sources.json). Une source différente ou une ressource manquante provoque un arrêt : faire revoir la modification et reconstruire un manifeste après inspection. Ne pas forcer l’ancien kit 6F.2 et ne pas employer `run_local.py` pour cette recette : il peut charger `.env` et privilégier Aiven.

## Lancement proposé seulement après nouvelle autorisation

Obtenir l’accord pour l’écoute **`127.0.0.1:5064`**, avec le kit figé inspecté, puis pour une navigation Edge manuelle. Aucune commande de lancement n’est exécutée pendant 6G.4.

```powershell
& .\.venv\Scripts\python.exe -I -B .\tools\recette_lot6g4.py --serve --autorisation-execution-confirmee
```

Le serveur prévu est mono-thread, sans debug ni reloader. Il ne démarre pas Edge. Après son démarrage autorisé, ouvrir manuellement une fenêtre InPrivate Edge et saisir `http://127.0.0.1:5064/`. Ne pas utiliser CDP ou modifier pare-feu, paramètres Windows ou profil personnel. Si le port est occupé ou qu’une protection refuse l’écoute, arrêter et consigner le message ; aucune désactivation de protection.

Conserver le processus pendant tout le parcours : ses trois comptes sont `jury6g4_admin`, `jury6g4_alice` et `jury6g4_bob`. Les mots de passe sont générés à chaque lancement. L’inscription permet aussi de créer un membre fictif avec un pseudo unique et un e-mail `@example.invalid`.

## Parcours jury

| Étape | Action | Résultat attendu |
|---|---|---|
| 1 — Alice | Ouvrir Connexion et utiliser son compte temporaire | Connexion via la vraie API, puis retour à l’accueil |
| 2 — Histoire | Ouvrir `dossier.html?slug=recette-6g4` | Vrai dossier SQL ; nombre de likes et état personnel lus depuis le serveur |
| 3 — Commentaire | Publier un court texte fictif unique | Confirmation puis commentaire visible avec le bon auteur |
| 4 — Like d’histoire | Cliquer J’aime, puis actualiser | Une ligne Vote ; état « Retirer mon J’aime » et compteur relus |
| 5 — Like de commentaire | Aimer le commentaire créé, puis actualiser | Une ligne CommentLike, compteur historique physique conservé à zéro |
| 6 — Retraits | Retirer les deux likes, puis recharger | Leurs lignes personnelles sont retirées ; les autres contributions restent présentes |
| 7 — Signalement | Depuis l’accueil, déconnecter Alice ; connecter Bob et signaler ce commentaire avec un motif fictif | Confirmation et bonne cible ; le commentaire reste visible |
| 8 — Administration | Déconnecter Bob depuis l’accueil ; connecter l’admin et actualiser le dashboard | Signalement correspondant au commentaire et sept indicateurs issus des requêtes SQL |

Mélissa présente le bouton et son état, Sylvie les routes/session/CSRF, Mahamadou les lignes, le couple unique et COUNT. Aucun export de cookies, CSRF, mots de passe ou capture HAR complète.

Compléments : consulter le Cold Case `dossier.html?slug=recette-coldcase-6g4` ; vérifier l’inscription ; tester Tab/Entrée/Espace, focus visible et lecture des messages ; avec deux comptes successifs, vérifier que chacun retire seulement son like. À partir du dashboard, archiver puis restaurer un dossier fictif et vérifier que ses contributions sont conservées. Bannir Bob seulement après sa participation : le bannissement garde ses données et interdit sa reconnexion ; aucun débannissement n’est prévu dans les routes actuelles. Pour recommencer, une nouvelle mémoire de recette sera nécessaire.

Les sept valeurs doivent être celles des données créées et des états actifs au moment de la lecture. Les likes ne créent aucun nouvel indicateur. Après archivage, les nombres de dossiers actifs peuvent changer ; restauration les rétablit. Ne pas imposer les nombres d’un autre passage ou du rapport dans le dashboard.

## Erreurs, arrêt et preuve à conserver

Après erreur réseau, timeout ou 5xx suivant un envoi, lire le message d’incertitude et vérifier le serveur ; ne pas renvoyer automatiquement. « Action enregistrée, état indisponible » signifie que la confirmation a précédé l’échec de relecture. Après déconnexion, vérifier le refus d’écriture. Les refus CSRF et erreurs serveur sont couverts par les essais isolés ; ne pas prétendre les avoir reproduits manuellement sans les observer.

Noter pour chaque étape : date, version du manifeste, statut réussi/échoué/non exécuté, cible fictive et éventuel défaut visuel. Les noms de fichiers de preuves imprimés par le kit ne contiennent pas de réponse brute d’authentification. Le reçu de lancement indiquera l’écoute ; l’état du navigateur reste à constater manuellement.

Arrêter le serveur par `Ctrl+C`, puis fermer la fenêtre InPrivate. **Toutes les données SQLite de ce processus disparaissent à l’arrêt.** Ce comportement ne prouve aucune persistance après redémarrage. Ne pas supprimer de fichiers du projet et ne pas utiliser une base réelle pour rendre la démonstration persistante.
