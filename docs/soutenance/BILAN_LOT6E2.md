# Lot 6E.2 — intégration des informations RGPD

> Archive pédagogique datée : les résultats et descriptions ci-dessous concernent le lot indiqué. Les anciens repères de ligne ne décrivent pas la version candidate. Pour préparer la soutenance actuelle, consulter les quatre fiches et le référentiel reliés au sommaire.

> Copie publique de référence : les chemins personnels et liens de travail internes sont retirés. Les preuves et commandes historiques gardent leur date et leur périmètre ; utiliser le README actuel pour le lancement.

[Sommaire](README.md) · [Matrice du jury](SUIVI_REMARQUES_JURY.md) · Décisions non confirmées (pièce interne non diffusée) · Procédure interne (archive interne non diffusée)

**Préparation le 31 octobre 2026, clôture le 1er novembre 2026 — périmètre autorisé : information et accessibilité, sans développement d'effacement de compte.** Trois notices provisoires sont intégrées aux formulaires. La page HTML de confidentialité est préparée hors du site servi : les mentions essentielles ne sont pas validées. Aucune conformité complète ni ouverture publique générale n'est annoncée.

## État initial, sauvegarde et conservation du travail

Branche conservée : `feature/frontend-api-integration`. HEAD : `07a9f03ea0a3bdad4a07066fdd7bab1997cc158b`. Avant édition : **37 fichiers suivis modifiés, 47 non suivis, aucun fichier indexé**. Les bilans 6A/6B/6C.1/6C.2/6D/6E.1, les décisions, brouillons et 22 remarques ont été examinés.

La sauvegarde durable existe :

```text
[chemin local privé retiré]
```

Ses 115 fichiers sont inventoriés par SHA-256 en lecture seule avant les modifications ; aucune copie, modification, suppression ou correction de permissions n'y est faite. La réserve antérieure sur la comparaison exhaustive des ACL n'est pas levée dans ce lot. C'est une sauvegarde de sources sélectionnées, sans base réelle ni les sept fichiers précédemment exclus.

Un état de référence de **106 fichiers examinés** et de l'index Git est enregistré avant édition. Les 18 fichiers préexistants concernés sont copiés avant leur modification dans un répertoire de préparation hors dépôt :

```text
[chemin local privé retiré]
```

Ce répertoire temporaire contient `baseline.json`, `avant-edition/`, les gardes inspectées, les manifestes et reçus de tests. Les jeux statiques, CSV de comptes, images non examinées, secrets et bases restent exclus de ces lectures/sauvegardes ciblées. Aucun reset, changement de branche, commit ou push.

## Fichiers créés et modifiés

**Quatre fichiers créés :**

```text
projet de texte de confidentialité (pièce interne non diffusée)
docs/soutenance/PROCEDURE_DROITS_LOT6E2.md
docs/soutenance/BILAN_LOT6E2.md
tests/test_rgpd_information.py
```

**Dix-huit fichiers préexistants modifiés :**

```text
frontend/inscription.html
frontend/theories.html
frontend/proposer-histoire.html
frontend/styles.css
frontend/README.md
frontend/tests/proposals.test.cjs
frontend/tests/theories.test.cjs
frontend/tests/theories-list.test.cjs
docs/soutenance/ARCHITECTURE_SECURITE_RGPD.md
docs/soutenance/SUIVI_REMARQUES_JURY.md
docs/soutenance/INDEX_CODE_JURY.md
docs/soutenance/fiche-melissa.md
docs/soutenance/fiche-sylvie.md
docs/soutenance/fiche-mahamadou.md
docs/soutenance/ORAL_JURY.md
docs/soutenance/DEMONSTRATION.md
docs/soutenance/README.md
docs/soutenance/TESTS_ET_VALIDATION.md
```

Aucun JavaScript applicatif, fichier du dashboard, backend, Swagger, modèle, migration ou lanceur modifié. Les trois fichiers JavaScript adaptés sont des tests HTML, pas des scripts du produit. Les commentaires français existants sont conservés ; les commentaires ajoutés expliquent les styles et les contrôles nouveaux.

## Informations intégrées et statut de publication

| Élément | Réalisation | Statut et limite |
|---|---|---|
| Inscription | Pourquoi les champs sont demandés, pseudonyme de connexion, hachage, visibilité possible des contributions, politique en préparation | Notice provisoire dans la page existante ; aucun nouveau champ, consentement ou faux lien |
| Théorie | Publication sur un dossier actif, prudence avec les données de tiers | Notice avant les champs ; sélecteur et bouton restent désactivés pendant le chargement prévu |
| Proposition | Envoi aux administrateurs, lien au compte et absence de publication automatique | Notice avant les champs ; titre/catégorie/contenu et requête existants conservés |
| Page de confidentialité (pièce interne non diffusée) | Design commun, compte/hachage, sessions, contributions, modération, archivage/purge, droits et réclamation CNIL | **Brouillon interne hors de frontend/, non publié et absent de la navigation du site** |
| Procédure des droits (archive interne non diffusée) | Accès, copie, rectification, effacement et contestation de contenu avec identité, tiers et réponse sûre | Document interne structuré ; activation après validation des opérateurs, canaux et décisions |
| Commentaires et signalements | Courts textes ci-dessous et références de placement | Préparés uniquement : aucun formulaire public nouveau |

Le formulaire et le bouton d'envoi référencent la notice par `aria-describedby`. Aucun contrôle nouveau ne bloque l'envoi et aucune donnée supplémentaire n'est collectée. Les classes CSS ajoutées sont limitées aux notices et au brouillon ; les règles préexistantes ne sont pas remplacées. Les liens natifs du brouillon ont un focus visible, des libellés et des cibles existantes.

Les six catégories du brouillon portent exactement « À confirmer avant publication » : responsable/coordonnées, contact, bases légales, conservation, hébergement/destinataires et transferts. Aucun nom de responsable, adresse électronique, base, durée ou infrastructure de production n'est inventé. Aucun lien public n'annonce une politique achevée. La balise noindex n'est pas une protection d'accès : le brouillon est hors des fichiers servis, ce qui est vérifié en WSGI. Un autre hébergement devra préserver cette séparation.

### Notices pour les formulaires non existants

**Commentaire — texte prêt à relire avant une future intégration autorisée :**

> Votre commentaire et votre pseudonyme peuvent être consultés publiquement sur le dossier actif. Évitez les coordonnées privées et les informations personnelles sur des tiers sans justification. L'information complète sur les traitements est en cours de préparation.

**Signalement — texte prêt à relire avant une future intégration autorisée :**

> Votre motif est transmis aux administrateurs pour examiner le commentaire signalé. N'ajoutez pas de coordonnées ou de justificatifs inutiles. L'information complète sur les traitements est en cours de préparation.

Les API existent, mais le site n'a pas ces formulaires publics. Leur création n'est pas ajoutée à ce lot. Le modèle ne stocke pas l'id du déclarant ; aucun anonymat général n'est promis.

## Décisions humaines encore nécessaires

Les décisions D01 à D12 ne sont pas réputées validées par cette intégration. Le contexte jury est confirmé ; public effectivement accessible, participants et contenus restent à préciser. Responsable/contact, finalités détaillées dont nécessité de l'email, bases, conservation, prestataires/localisation/transferts, organisation des droits et copies doivent être arrêtés avant publication finale.

Le contact est indispensable à une procédure effective, y compris pour une personne bannie ou sans compte : une adresse fictive ou un formulaire absent ne résout pas ce point. Une suppression de compte exigerait aussi les décisions sur les contributions partagées, la transaction, les anciennes sessions et la réutilisation possible d'un id. Aucun tel outil n'est créé. Les récits visant des personnes réelles demandent l'examen humain du cadre applicable ; aucun contenu réel n'est lu ici.

## Protections conservées et explications techniques

Hachage Werkzeug, relecture du compte et des rôles, bannissement, CSRF, CORS et gestion des erreurs sont inchangés. HttpOnly=True et SameSite=Lax sont constatés dans le code ; Secure dépend de la configuration, avec défaut False. Ni HTTPS effectif ni durée de session ne sont déduits d'une lecture du code. Aucun réglage n'est modifié, aucun secret lu.

Le cookie nécessaire à l'authentification se distingue des traceurs facultatifs ; aucune bannière automatique n'est ajoutée. L'absence de mécanisme identifié dans les sources examinées ne certifie pas l'absence de traceur sur le déploiement réel. Swagger/cdnjs et les URL d'images restent à vérifier séparément, sans accès réseau ici.

La documentation explique User, Story, Theory, Comment, Vote, Proposal et Report, les pseudonymes copiés, FK et cascades ORM, et les copies de cookies. **Bannissement, archivage, purge du dossier et effacement personnel restent distincts.** Neuf modèles et onze FK conservés, aucune migration exécutée, y compris par les tests de cette campagne.

Les sept compteurs, utilisateurs/bannissement, listes, recherche/filtres, archivage/restauration et purge sécurisée restent identiques par empreintes et couverts côté frontend par la suite existante. Aucun faux enregistrement n'est créé dans la base du site ; les simulations de tests restent isolées. Le fonctionnement réel persistant demandé pour le jury n'est pas démontré par ces simulations.

## Tests exécutés et preuves

| Campagne retenue | Résultat exact | Preuves hors dépôt |
|---|---|---|
| Frontend | **364 PASS, 0 FAIL**, aucun annulé/ignoré | `attempt-3/frontend.stdout.txt`, `attempt-3/frontend.node-guard.json` |
| Lanceur et nouveaux contrats HTML/WSGI | **16 PASS, 0 FAIL**, aucune erreur/ignoré : huit tests existants et huit nouveaux | `attempt-4/launcher.stdout.txt`, `launcher.guard.json` |
| Total actuel exécuté | **380 PASS** | Deux suites distinctes, pas addition des tentatives |
| Backend | **NON RÉEXÉCUTÉ** ; sources conservées par empreintes | Les 285 PASS backend et le total 657 de 6C.2 restent historiques |

Le backend n'est pas modifié et ses tests de migration ne sont pas lancés. Les **657 historiques ne sont ni rejoués ni ajoutés aux 380 actuels** ; aucun total de 665 nouvelles réussites n'est revendiqué.

Premiers passages frontend : attempt-1 **361 PASS / 3 FAIL**, attempt-2 **362 PASS / 2 FAIL**. Ces échecs concernent trois comparaisons HTML figées devenues incompatibles avec la notice et ses attributs. Les tests gardent désormais les contraintes d'id/classe/méthode, champs, titre, chargement/bouton désactivé et scripts. Le snapshot du formulaire historique reste comparé après retrait des seuls ajouts de notice autorisés ; il n'est pas remplacé par le nouveau HTML. Les huit nouveaux tests vérifient séparément le nouveau contrat et l'absence de collecte supplémentaire. Aucune assertion de comportement applicatif n'est retirée pour obtenir PASS.

Les huit nouveaux tests couvrent les trois contrats de champs, les notices visibles/reliées et non bloquantes, les scripts/contrôles inchangés, le brouillon absent des fichiers et liens publics, les refus GET/HEAD de ses chemins et le service des trois pages par le vrai middleware local. Ils n'utilisent ni serveur réseau ni données de la base.

Les gardes Python/Node sont lues avant copie dans ce dossier neuf. Node reste identique ; Python adapte seulement la découverte et le nombre des tests du lanceur, sans assouplir les protections. Le contrôleur n'exécute que frontend/lanceur. Manifestes et SHA-256 portent sur 65 sources examinées ; les deux anciennes entrées inutilisées `donnees.js` et `ancien_app.py` sont exclues sans lecture. L'environnement enfant est minimal, dotenv neutralisé, paramètres Aiven vides, réseau/DNS et sous-processus applicatifs bloqués, lectures privées et écritures du dépôt interdites ; seules les bases SQLite mémoire seraient autorisées. Les sondes valident les refus avant entrée/sortie et leurs compteurs sont séparés. **Tous les compteurs interdits des suites retenues sont à zéro.**

```powershell
# Commandes du harnais inspecté, hors dépôt ; aucun Flask/Edge/Alembic réel.
$preuves6e2 = Join-Path $env:LOCALAPPDATA 'Temp\portfolio-lot6e2-20261031-e641e2aa'
& .\.venv\Scripts\python.exe -I -B (Join-Path $preuves6e2 'run-checks.py') --inspect
& .\.venv\Scripts\python.exe -I -B (Join-Path $preuves6e2 'run-checks.py')
```

**PASS statique et documentaire :** quatre documents HTML analysés pour structure, identifiants, labels et descriptions ARIA ; 46 références HTML locales et 901 références Markdown locales existantes sur 34 documents, ainsi que les deux nouvelles cibles de sections. L'index conserve ses 191 cibles historiques et ajoute six repères réels, soit 197. Les 22 remarques sont conservées ; seule C-07 est actualisée et reste PARTIEL. Les préfixes des fiches et réponses orales historiques sont préservés, ainsi que les six sources Mermaid de référence et le diagramme historique distinct de l'audit 6C. Aucun rendu nouveau.

Les contraintes des formulaires et leurs liens/scripts sont comparés à l'avant-édition ; le snapshot historique du formulaire est inchangé. Le CSS préexistant reste le préfixe du fichier et les blocs ajoutés sont équilibrés ; les trois fichiers de tests JavaScript sont analysés/exécutés par Node. Il ne s'agit pas d'une validation normative exhaustive HTML5/CSS ni d'une recette visuelle. `git diff --check` passe avec reconnaissance des fins de ligne CRLF, sans changement de configuration Git persistante ou Windows.

Les 88 fichiers examinés hors périmètre et les 115 fichiers de la sauvegarde durable sont inchangés par empreintes ; branche, HEAD et index sont conservés. État final : **44 fichiers suivis modifiés, 51 non suivis, aucun fichier indexé**, incluant le travail antérieur. Reçu : `static-validation.json` dans le dossier de preuves. Les liens externes ne sont pas ouverts. Une lecture locale, des assertions ARIA et un DOM simulé ne valident pas le rendu ni l'accessibilité exhaustive.

## Documentation et responsabilités

Frontend README, sécurité/RGPD, matrice des 22 remarques, index des lignes, fiches des trois membres, réponses orales, démonstration, sommaire et document des tests sont actualisés. Une formulation périmée de Report sans FK dans l'index est corrigée pour correspondre au modèle déjà livré en 6C.2, sans changement de schéma.

- **Mélissa** : notices, brouillon HTML, structure et liens accessibles, distinction public/proposition interne et information/consentement.
- **Sylvie** : cookies et protections inchangées, identité proportionnée, accès/copie/rectification/effacement/contestation, protection des tiers et réponse sûre.
- **Mahamadou** : compte et relations, pseudo copié, signalements, limites des cascades et sessions, conservation/copies ; aucune modification de base.

Sept réponses RGPD simples sont ajoutées aux supports oraux, hors des questions historiques. Les six sources Mermaid et les réponses historiques restent à conserver ; aucun nouveau rendu n'est annoncé.

## Limites et dernières validations

Non exécutés : Edge/navigateur/lecteur d'écran, navigation clavier réelle, rendu mobile, contrôle d'hébergement/HTTPS/cookies, réseau externe, traitement d'une vraie demande, lecture de données personnelles réelles, persistance après redémarrage, MySQL/Aiven, migrations et déploiement. Aucune nouvelle preuve backend ou de courses concurrentes.

Avant présentation : confirmer les informations indispensables, le contact et le périmètre de démonstration ; autoriser séparément la recette et les interactions réelles. Avant ouverture générale : compléter l'information validée, l'organisation des droits et la vérification de la cible réelle, puis autoriser la publication. Le statut scolaire ou un dashboard fonctionnel ne prouve pas la conformité.

**GO pour revue des notices intégrées et du brouillon interne. NO-GO pour publier la politique en l'état ou déclarer une conformité complète.** Aucun autre lot commencé ; aucune suppression de compte, modification de bannissement/purge, migration, donnée artificielle ajoutée au site, secret lu, changement Windows/branche, commit, push ou suppression de fichier existant.
