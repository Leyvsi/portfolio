# Préparer un lancement sur un autre PC sans MySQL/Aiven

> Copie publique de référence : les chemins personnels et liens de travail internes sont retirés. Les preuves et commandes historiques gardent leur date et leur périmètre ; utiliser le README actuel pour le lancement.

Procédure documentaire du 2 novembre 2026. **Aucune installation vierge, aucun serveur ni navigateur relancé en 6H.1.** Le kit a été inspecté et exécuté dans les campagnes précédentes ; sa portabilité sur un nouveau PC reste à vérifier.

## Ce qu’il faut transmettre

Utiliser une copie sélective validée du futur livrable, en conservant les chemins relatifs : code frontend/backend courant, modèles, `run_local.py`, `backend/requirements.txt`, `tools/recette_lot6g4.py`, son manifeste et `frontend/images/default-story.svg`. Les 40 sources de ce manifeste doivent toutes être présentes et inchangées. L’inventaire (pièce interne non diffusée) et le plan (pièce interne non diffusée) donnent les autres fichiers à conserver.

Un clone du HEAD actuel ne contient pas les 51 fichiers modifiés ni les 79 fichiers non suivis relevés au début de l’audit. Il ne suffit donc pas à reproduire l’état validé. Ne pas transmettre `.env`, certificats, cookies, base ou dump réel, environnement `.venv`, téléchargement de page privée ou ancien fichier de comptes.

Le kit utilise un schéma neuf et fictif en **SQLite mémoire**, qui disparaît à l’arrêt. Il ne restaure pas les bases SQLite fichier conservées dans les preuves 6G.5. Ces dernières et leurs adaptateurs temporaires ne sont pas un installateur portable du produit.

## Préparer Python et les dépendances

Mode documenté : Windows et PowerShell, avec Python 3.13 et son module `venv`. La campagne historique utilisait Python 3.13.0 et Node 24.16.0. Node sert aux tests ; les pages du site ne nécessitent pas de compilation. Aucun environnement macOS ni nouvelle architecture n’est validé par ce guide.

Depuis le dossier de la copie livrable, après validation de son contenu :

```powershell
py -3.13 --version
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt
```

Ces commandes sont des instructions futures, non exécutées pendant l’audit. L’installation exige un accès aux paquets ou un dépôt de wheels préparé ; elle ne suppose aucune base distante. SQLAlchemy est fixé à `2.0.53` et le kit refuse une autre version avant import applicatif. Ne pas copier l’environnement virtuel d’un autre ordinateur.

## Inspecter le kit sans lancer de serveur

```powershell
.\.venv\Scripts\python.exe -I -B tools\recette_lot6g4.py
```

Le résultat attendu est `READY`, SQLite `:memory:`, paramètres Aiven vidés, `dotenv` désactivé avant import, aucun listener et gardes à zéro. Une nouvelle base de test contient deux dossiers et trois comptes fictifs ; les commentaires/signalements viennent ensuite des actions de recette, pas de valeurs ajoutées au dashboard.

Le manifeste compare les SHA-256 des sources après normalisation LF. En cas de différence, arrêter et faire examiner les fichiers ; ne pas renouveler automatiquement les empreintes pour contourner le refus. Le kit 6F.2 conserve son ancien instantané et refuse normalement les sources actuelles : il ne remplace pas le kit 6G.4.

Le lancement ordinaire `run_local.py` charge `.env`. Un groupe Aiven complet a priorité sur `DATABASE_URL` : définir seulement une URL SQLite n’est donc pas une isolation suffisante. Pour cette démonstration sans base distante, utiliser le kit contrôlé ci-dessus.

## Lancer uniquement après une nouvelle autorisation de recette

Le lot 6H.1 ne donne pas cette autorisation. Après inspection réussie et autorisation distincte de lancer le serveur et Edge :

```powershell
.\.venv\Scripts\python.exe -I -B tools\recette_lot6g4.py --serve --autorisation-execution-confirmee
```

Le marqueur de ligne de commande confirme une autorisation déjà obtenue ; il ne la remplace pas. Le serveur écoute seulement sur `127.0.0.1:5064`, sans debug ni reloader. Un port occupé doit être examiné ; ne pas arrêter un processus inconnu.

Ouvrir manuellement `http://127.0.0.1:5064/` dans Edge. Faire une actualisation complète des pages déjà visitées si l’ancienne version y est conservée. Le middleware courant envoie `Cache-Control: no-store` pour les ressources frontend. Utiliser les identifiants fictifs nouvellement affichés dans la console locale ; ils changent à chaque lancement. Ne pas réutiliser les mots de passe d’une recette précédente ni les inscrire dans Git.

La lecture du contrat JSON peut être montrée sans charger Swagger UI et ses ressources CDN. Les ressources publiques du kit sont limitées : les anciennes données statiques et quatre WebP non examinés n’en font pas partie. Le SVG local sert au témoin minimal ; sa provenance reste une question documentaire avant diffusion.

## Vérifier et arrêter

Suivre le [protocole 6G.4](RECETTE_MANUELLE_LOT6G4.md), les observations des [correctifs 6G.5](BILAN_CORRECTIFS_LOT6G5.md) et le scénario des [supports courants](SUPPORT_JURY_LOT6H1.md). Les nombres du dashboard dépendent des actions réalisées dans cette nouvelle mémoire ; ne pas recopier les valeurs finales d’une ancienne base.

Se déconnecter explicitement, puis arrêter le serveur lancé pour cette recette. En cas d’échec de Ctrl+C, identifier et arrêter uniquement son propre processus avec les droits existants, sans élévation ni modification Windows. La mémoire SQLite est perdue à l’arrêt ; conserver seulement les preuves autorisées, sans identifiants, cookies ou jetons. Aucun fichier préexistant ne doit être supprimé.

Les 854 tests historiques ne sont pas reproduits par cette commande. Leur harnais complet est hors dépôt, dépend d’une sélection inspectée et exclut sept tests de migration historiques ; un `unittest discover` global ne constitue pas une commande équivalente. La préparation d’un harnais portable complet est une action distincte du présent audit.
