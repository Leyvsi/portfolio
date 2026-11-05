# Lot 6E.1 — sauvegarde et préparation RGPD

> Archive pédagogique datée : les résultats et descriptions ci-dessous concernent le lot indiqué. Les anciens repères de ligne ne décrivent pas la version candidate. Pour préparer la soutenance actuelle, consulter les quatre fiches et le référentiel reliés au sommaire.

> Copie publique de référence : les chemins personnels et liens de travail internes sont retirés. Les preuves et commandes historiques gardent leur date et leur périmètre ; utiliser le README actuel pour le lancement.

[Sommaire](README.md) · [Matrice des 22 remarques](SUIVI_REMARQUES_JURY.md) · [Dernier bilan applicatif](BILAN_LOT6C2_IMPLEMENTATION.md)

**31 octobre 2026 — phase documentaire autorisée, sans changement applicatif.** Sauvegarde sélective vérifiée avant toute édition. Brouillons internes uniquement ; aucune publication sur le site. La conformité RGPD n'est pas établie.

## 1. État initial et sauvegarde

Branche : `feature/frontend-api-integration`. HEAD : `07a9f03ea0a3bdad4a07066fdd7bab1997cc158b`. Avant édition : **37 fichiers suivis modifiés, 40 fichiers non suivis, aucun fichier indexé**. Les fichiers de l'équipe sont conservés ; aucun reset, changement de branche, commit ou push.

La sauvegarde a été créée le **31 octobre 2026 à 16:32:24 UTC**, avant les brouillons et les ajouts documentaires :

```text
[chemin local privé retiré]
├── sources-avant-6e1/     fichiers sélectionnés avec chemins relatifs conservés
└── metadata/
    ├── git-state.json
    ├── git-status.txt
    ├── git-tracked-paths.txt
    ├── inventory.json
    ├── SHA256SUMS.txt
    └── verification.json
```

**99 fichiers, 1 291 780 octets : 61 suivis et 38 non suivis**, comprenant les 37 fichiers suivis modifiés. Le dossier est hors du dépôt et des ressources servies. Les permissions héritées du dossier temporaire utilisateur ont été examinées en lecture seule : propriétaire utilisateur, système, administrateurs et identités du sandbox ; aucune autorisation générale Everyone/Users observée. Aucun changement d'ACL ou de configuration Windows.

**Limite : cette copie est sélective et située dans Temp.** Elle peut être supprimée par un nettoyage du système ; ce n'est ni un clone Git complet, ni une sauvegarde de données, ni une preuve de restauration applicative. Son déplacement ou sa duplication durable dans un emplacement privé choisi reste à décider en D12 ; aucune copie vers un cloud n'a été faite.

## 2. Sélection, inclusions et exclusions

Les candidats proviennent des chemins Git suivis/non suivis non ignorés, pas d'une copie récursive du dépôt. Les textes admis ont été décodés et examinés par type et motifs de secrets ; les fichiers Python ont été analysés sans import. Les configurations publiques, la copie de modèles de Mahamadou, les fixtures et les occurrences de valeurs de test ont fait l'objet d'un contrôle ciblé. Les adresses et jetons repérés dans les tests sont fictifs. Aucun secret effectif n'a été identifié dans la sélection ; ce contrôle par motifs n'est pas une garantie universelle d'absence de secret.

| Inclus | Nombre | Périmètre |
|---|---:|---|
| Backend | 31 | Modèles, configuration sous forme de code, vues, contrat Swagger, dépendances et tests |
| Documentation de soutenance | 22 | Markdown existants, bilans, fiches et matrice |
| Frontend | 31 | HTML/CSS/JS examinés, tests, deux fixtures JSON fictives, README et SVG de repli |
| Migrations | 10 | Sources et configuration publique, copiées sans exécution |
| Copie de révision de Mahamadou | 1 | `revision_code/mahamadou/backend/models.py`, distinct du modèle exécuté |
| Racine et lanceur | 4 | `.gitignore`, `README.md`, `run_local.py`, `tests/test_run_local.py` |
| **Total** | **99** | Liste exacte et empreintes dans l'inventaire |

Sept fichiers Git candidats ont été **exclus et non copiés** :

```text
docs/soutenance/COMPTES_DEMO.exemple.csv
frontend/donnees.js
frontend/histoires-originales.json
frontend/images/carnet-tour-nord.webp
frontend/images/malle-quai-silencieux.webp
frontend/images/medaille-pavillon-ferme.webp
frontend/images/tableau-salle-bleue.webp
```

Le CSV de comptes est exclu par précaution ; les deux jeux statiques et les quatre images binaires n'ont pas été examinés. Leurs contenus n'ont pas été lus ni hachés. Les deux fichiers non suivis exclus sont le CSV et le JSON historique. Leur exclusion de la sauvegarde ne les supprime ni du disque ni du suivi éventuel.

Sont également exclus par la sélection : `.env` et variantes privées, clés/certificats, fichiers de cookies/sessions, bases et dumps, journaux sensibles, environnements virtuels, objets Git et tout autre fichier ignoré/non examiné. Le contenu du `.env` privé et des données réelles n'a pas été lu. Aucune exception nécessitant la copie d'un fichier potentiellement privé n'a été rencontrée pour cette sélection ; un tel ajout requerrait un accord préalable.

Inventaire exact : Preuve locale conservée hors publication. Empreinte SHA-256 de cet inventaire au moment de sa création :

```text
69e9e9ed4960dc3ad34039b147585e92af391e1a5b386407a6d21a8ef94d4993
```

## 3. Vérification de la sauvegarde

**PASS avant toute édition** : relecture des 99 copies, vérification des tailles et correspondance SHA-256 avec l'inventaire et les 99 sources encore inchangées. État Git, branche, HEAD et empreinte de l'index inchangés à ce stade. Preuve locale conservée hors publication.

Les chemins relatifs permettent de retrouver un fichier dans `sources-avant-6e1/`. Une restauration ultérieure devra viser un emplacement isolé et comparer les empreintes avant tout remplacement autorisé. Aucun fichier du projet n'a été écrasé pour tester la restauration, aucune application n'a été lancée depuis la copie.

Les huit fichiers documentaires dans leur état final sont copiés séparément dans `documents-6e1/`, avec `metadata/documents-final.json` pour leurs tailles et SHA-256. Cette copie complémentaire ne remplace aucun fichier de `sources-avant-6e1/` ; l'état antérieur et les nouveaux brouillons restent distincts. Les huit copies sont relues et comparées aux documents finaux.

## 4. Brouillons et fichiers documentaires

| Fichier créé | Contenu |
|---|---|
| Politique de confidentialité (pièce interne non diffusée) | Préparation de la future page ; tous les choix manquants restent signalés |
| Notices des formulaires (pièce interne non diffusée) | Inscription, publication des contributions, propositions et signalements |
| Procédures manuelles (pièce interne non diffusée) | Vérification d'identité, accès/copie, rectification et demande d'effacement |
| Conséquences de l'effacement (pièce interne non diffusée) | Dépendances SQLAlchemy, pseudonymes copiés, tiers, copies et sessions |
| Décisions à valider (pièce interne non diffusée) | D01 à D12 et tableau de conservation sans durée inventée |
| Présent bilan | Sauvegarde, périmètre, risques, plan, contrôles et oral |

Deux fichiers existants reçoivent uniquement un ajout documentaire : le [sommaire](README.md) et la [matrice](SUIVI_REMARQUES_JURY.md). Les 22 remarques et leurs lignes historiques sont conservées ; C-07 reste PARTIEL. Tous ces fichiers restent dans `docs/soutenance/`. Aucun ajout de lien dans la navigation publique et aucun changement du frontend, backend, Swagger, modèles, migrations ou tests.

## 5. Informations à confirmer et risques

Les décisions D01 à D12 restent ouvertes : responsable/contact, finalités et nécessité de l'email, bases légales, conservation, hébergement/transferts, public et données réelles, sort des contributions, identité/sessions, organisation des demandes, configuration et copies. Aucune identité, adresse, base légale, durée ou infrastructure de production n'est inventée. Liste détaillée (pièce interne non diffusée).

Risques persistants : information utilisateur encore absente du site ; absence de parcours complet de rectification/effacement ; association historique parfois ambiguë ; texte identifiant malgré `SET NULL` ; conservation indéfinie non justifiée ; copies hors SQL ; cookies à invalider et id SQLite potentiellement réutilisable ; configuration réelle et prestataires inconnus. Les ressources externes Swagger/images et les éventuels journaux nécessitent une vérification sur la cible autorisée.

L'archivage conserve les données ; la purge d'un dossier détruit aussi ses contributions. Ni l'un ni l'autre ne traite automatiquement les droits d'une personne. Les règles proposées protègent les autres comptes et dossiers, bloquent les associations ambiguës et évitent les cascades globales depuis `User`. Le responsable devra aussi examiner le cadre des récits visant des personnes réelles avant publication ; l'absence de lecture de ces contenus empêche de les qualifier ici.

## 6. Fonctions nécessaires et progression

**INDISPENSABLE :** décisions confirmées, information claire, contact suivi accessible sans connexion, procédure manuelle sécurisée et traitement réellement possible des demandes. Si l'effacement d'un compte est retenu, son unité de travail et ses protections de session doivent être conçues puis testées avant usage.

**UTILE :** affichage des informations déjà fournies par `/me`, réponses administratives minimisées, contrôles de cache privé et ressources externes limitées. À apprécier après décisions, sans création automatique de routes.

**À REPORTER :** plateforme de consentement, ordonnanceur de suppression, portail d'export, nouvelle architecture de services. Une procédure manuelle et les fonctions Flask/SQLAlchemy existantes sont privilégiées. Aucun reçu de suppression persistant ni purge programmée n'est ajouté, conformément à S2.

Suite proposée : valider les décisions et brouillons → autoriser l'intégration de l'information → autoriser les seuls outils de droits nécessaires → tests fictifs → autorisations distinctes pour recette réelle et déploiement. Aucune de ces étapes suivantes n'est exécutée ici.

## 7. Tests futurs, non exécutés

| Groupe | Vérifications à prévoir |
|---|---|
| Information | Mentions exactes, absence de placeholders, liens accessibles sans connexion, cohérence notices/politique et absence de case générale de consentement |
| Identité | Session, personne bannie ou sans compte, demande pour un tiers, doute raisonnable, email non vérifié, preuve proportionnée, absence de collecte de mot de passe/jeton |
| Accès/copie | Données du bon compte, archives, mentions libres, signalements sans déclarant stocké, données de tiers masquées, absence de secrets/dump global et transmission au destinataire vérifié |
| Rectification | Contraintes uniques, pseudonymes copiés, liens fiables, ambiguïté bloquée et autres comptes conservés |
| Effacement | Dossier partagé, votes/propositions, commentaires et signalements, aucune cascade injustifiée, FK actives, rollback complet et témoins inchangés |
| Sessions et incertitude | Ancien cookie, bannissement puis état courant, compte effacé, id réutilisé, préconditions et absence de relance automatique après timeout |
| Copies et reprise | Exports, fichiers statiques, sauvegardes, accès et prévention d'une republication après restauration |
| Non-régression | Backend/frontend/lanceur sous harnais inspecté, SQLite fictive isolée et FK activées ; navigateur et MySQL séparément autorisés |

Ces tests ne sont ni implémentés ni exécutés en 6E.1. Les **657 PASS historiques** restent la référence applicative, sans nouvelle campagne ni garantie de compatibilité MySQL/Aiven, concurrence réelle ou déploiement.

## 8. Explications pour la soutenance

| Étudiant | Ce qu'il doit pouvoir montrer et expliquer |
|---|---|
| Mélissa | Les notices avant collecte, la future politique et ses liens ; distinguer information, conditions d'utilisation et consentement ; expliquer ce qui est public et ce qui reste une proposition privée à l'administration |
| Sylvie | La relecture du compte et des permissions ; vérifier une demande sans demander le mot de passe ; protéger les tiers dans une copie ; expliquer pourquoi une procédure manuelle peut suffire |
| Mahamadou | Montrer User/Story et les FK ; expliquer `CASCADE`, `SET NULL`, pseudo copié et transaction ; préserver les contributions des autres ; retrouver un fichier sauvegardé et son SHA-256 |
| Tous | Distinguer fonctionnalités testées, preuves historiques, décisions manquantes et conformité ; expliquer les limites Temp, copies, sessions et déploiement |

## 9. Contrôles de cette phase

**PASS documentaire :** les 99 fichiers de la sauvegarde initiale sont relus et conformes aux empreintes ; les 97 fichiers sélectionnés hors sommaire/matrice restent identiques dans le projet. Les deux documents existants ne reçoivent que des ajouts et leurs 22 lignes de remarques sont conservées à l'identique. Six nouveaux fichiers, tous dans `docs/soutenance/`, et deux documents existants complétés : huit fichiers concernés par 6E.1. Les cibles des liens locaux des huit documents existent ; les douze identifiants de décision sont définis. Preuve locale conservée hors publication.

Branche, HEAD et empreinte de l'index conservés. État final attendu et contrôlé : **37 fichiers suivis modifiés, 46 fichiers non suivis, aucun fichier indexé**. Les six ajouts expliquent la différence avec les 40 fichiers non suivis initiaux. Aucun fichier de l'interface ou du backend ne fait partie des changements de cette phase.

Aucune suite applicative n'est lancée pour ces seules modifications documentaires. Les **657 PASS restent historiques**. Aucune restauration complète, recette réelle ou preuve MySQL n'est revendiquée.

## 10. Verdict

**GO pour revue des brouillons et décisions d'équipe. NO-GO pour publication en l'état, effacement de compte ou déclaration de conformité.** Phase limitée à la sauvegarde et à la préparation documentaire ; attendre une autorisation avant toute modification de l'interface ou du backend.

Aucune suppression, migration, lecture du `.env` privé, connexion MySQL/Aiven, lecture de données réelles, navigateur, serveur, modification Windows, commit ou push.
