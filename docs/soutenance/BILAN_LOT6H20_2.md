# Bilan local — lot 6H.20.2

> Archive pédagogique datée : les résultats et descriptions ci-dessous concernent le lot indiqué. Les anciens repères de ligne ne décrivent pas la version candidate. Pour préparer la soutenance actuelle, consulter les quatre fiches et le référentiel reliés au sommaire.

> Copie publique de référence : les chemins personnels et liens de travail internes sont retirés. Les preuves et commandes historiques gardent leur date et leur périmètre ; utiliser le README actuel pour le lancement.

4 novembre 2026, Europe/Paris. Projet cible : `[chemin local privé retiré]`, branche `feature/frontend-api-integration`.

## Périmètre autorisé

Après l’audit en lecture seule, l’utilisateur a autorisé la première phase proposée : notices factuelles sur six pages, brouillon interne non publié, contrôles ciblés et actualisation du README. La publication de `frontend/confidentialite.html`, les liens publics et toute modification fonctionnelle demeurent hors de cette phase. Aucun rapport identifié 6H.20.1 n’a été retrouvé ; les conclusions ont été réexaminées dans les sources actuelles et les documents disponibles jusqu’à 6H.18.4.

## Changements

- Notices ajoutées aux connexions membre et administrateur, avant les champs, avec description du cookie de session et du rôle administrateur.
- Notices d’inscription, théorie, proposition, commentaire et signalement précisées. Publication sans connexion et destination administrative sont distinguées ; aucune base juridique, durée, identité ou adresse de contact n’est inventée.
- Information visible près des zones de likes de dossier et commentaires : lien au compte, ajout/retrait et visibilité des totaux. Les conteneurs et boutons de formulaire sont associés aux notices par `aria-describedby`.
- Brouillon interne à quinze sections, clairement incomplet, hors du répertoire servi. Les anciens brouillons restent conservés. Aucune page `frontend/confidentialite.html` ni aucun lien public de confidentialité ajouté.
- Tests HTML/WSGI étendus aux six pages et sept formulaires, aux likes, aux différences de visibilité des formulaires dynamiques et au refus des deux brouillons par les deux lanceurs.
- README actualisé : sources locales et livraison historique distinguées ; six PNG et slugs, distribution WSGI/Flask, modes 5064/5066/5000, commandes, cookies, résultats historiques et limites RGPD. Aucune nouvelle livraison GitHub annoncée.
- Protocole manuel Edge préparé, avec tests sur données isolées et critères futurs de publication ; cases laissées non cochées.

## Fichiers concernés

| Action | Chemin |
|---|---|
| Modifier | `frontend/inscription.html` |
| Modifier | `frontend/connexion.html` |
| Modifier | `frontend/admin-connexion.html` |
| Modifier | `frontend/dossier.html` |
| Modifier | `frontend/theories.html` |
| Modifier | `frontend/proposer-histoire.html` |
| Modifier | `tests/test_rgpd_information.py` |
| Modifier | `tests/test_run_local.py` |
| Modifier | `tools/recette_lot6g4_sources.json` |
| Modifier | `README.md` |
| Créer | projet de texte de confidentialité (pièce interne non diffusée) |
| Créer | `docs/soutenance/RECETTE_MANUELLE_LOT6H20_2.md` |
| Créer | `docs/soutenance/BILAN_LOT6H20_2.md` |

Le manifeste conserve ses 41 entrées et ses autres métadonnées. Seules les six empreintes des pages HTML modifiées sont actualisées après revue. Aucune ressource publique supplémentaire n’est autorisée par le kit ; ses protections restent inchangées.

## Validations réellement exécutées

Sources candidates testées dans une copie isolée sous `[chemin local privé retiré]`. Interpréteur du venv existant utilisé avec `-B`, sans installation et sans génération de bytecode.

| Suite | Résultat |
|---|---|
| `tests/test_rgpd_information.py` | 13 tests réussis |
| `tests/test_run_local.py` | 10 tests réussis |
| `tests/test_recette_lot6g4.py` | 13 tests réussis |
| `tests/test_histoires_originales.py` | 13 tests réussis |
| `backend/tests/test_csrf.py` | 29 tests réussis |
| `backend/tests/test_api_errors_stats_login.py` | 14 tests réussis |
| Ensemble `frontend/tests/*.test.cjs` | Réussite de la suite complète, code de sortie 0, avec DOM/API simulés |

Soit 92 tests Python ciblés. Les résultats historiques 6H.18.x ne sont pas additionnés à cette campagne.

Les commandes `unittest discover` et Node sont précisées dans le README. Les tests HTML/WSGI utilisent des applications sans serveur ; les gardes réseau/SQL interdisent les connexions et écoutes. Les deux suites backend utilisent le harnais mémoire existant, neutralisent dotenv/Aiven avant import et vérifient les connexions SQLAlchemy. Aucune SQLite existante n’est ouverte.

Un contrôle complémentaire réel du cycle de compte, conservé hors du projet dans `[chemin local privé retiré]`, a également réussi : inscription avec mot de passe généré uniquement en mémoire, vérification de son hachage, connexion, attributs et contenu minimal du cookie signé, permissions membre, refus CSRF sans modification des dix tables, rotation du jeton à la reconnexion et suppression du cookie à la déconnexion. SQLite mémoire uniquement ; connexions aux autres SQLite et ATTACH/DETACH interdits, aucune écoute réseau. Aucune donnée d’authentification n’est exportée.

Gabarit de la commande historique exécutée ; le script interne n’est pas distribué :

```powershell
# Gabarit historique ; fournir les deux chemins autorisés avant usage.
$pythonValidation = '<INTERPRETE_PYTHON_AUTORISE>'
$scriptValidation = '<SCRIPT_INTERNE_NON_DISTRIBUE>'
& $pythonValidation -I -B $scriptValidation
```

Les tests existants du kit ont émis des `ResourceWarning` sur la fermeture de flux statiques et SQLAlchemy une dépréciation `datetime.utcnow`. Ils n’ont entraîné aucun échec ; leur correction n’est pas incluse dans ce lot d’information.

## Préservation et limites

Les empreintes de 457 fichiers sources/documentaires/ressources non privés ont été relevées avant préparation ; les changements admis sont limités aux dix modifications et trois créations listées. Le transfert doit refuser toute source cible changée entre-temps et tout remplacement d’un nouveau document déjà présent. Le contrôle après transfert compare les fichiers livrés à la copie testée et les autres fichiers au relevé initial.

Aucun accès à une base persistante, aucune création ou modification de compte permanent, aucune modification de clé, d’image, d’histoire ou de contribution. Aucun lancement, arrêt ou redémarrage de serveur, aucun commit, indexation, push ou merge. Les préparations et copies de revue restent hors du dépôt cible.

Pas de nouvelle recette Edge, de mesure visuelle mobile, de validation par lecteur d’écran, d’inspection réseau navigateur, de vérification de durée effective des cookies, ni de validation MySQL/production. Le protocole manuel demeure à exécuter sur une instance isolée autorisée. Les tests statiques ne prouvent pas la lisibilité réelle ni l’absence générale de traceurs.

## Décisions et publication restantes

Le registre D01–D12 reste à finaliser : responsable et responsabilité conjointe éventuelle, contact suivi, finalités/minimisation, bases légales, conservation, hébergement/destinataires/transferts, public et récits de personnes réelles, sort des contributions et copies, identité/sessions, organisation des droits, configuration/incidents, sauvegardes/restauration.

La page finale et les liens des dix pieds de page nécessiteront ces décisions puis une autorisation de publication. Le lanceur général servirait automatiquement un HTML placé à la racine de `frontend/` ; la protection actuelle est donc son absence de ce répertoire, pas la balise `noindex`. Une future diffusion exposant tout le dépôt demanderait une revue propre. Aucune conformité RGPD définitive annoncée.
