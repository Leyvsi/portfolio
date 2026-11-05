# Lot 6F.2 — recette fonctionnelle et préparation de soutenance

> Archive pédagogique datée : les résultats et descriptions ci-dessous concernent le lot indiqué. Les anciens repères de ligne ne décrivent pas la version candidate. Pour préparer la soutenance actuelle, consulter les quatre fiches et le référentiel reliés au sommaire.

> Copie publique de référence : les chemins personnels et liens de travail internes sont retirés. Les preuves et commandes historiques gardent leur date et leur périmètre ; utiliser le README actuel pour le lancement.

[Sommaire](README.md) · [Lot 6F.1](BILAN_LOT6F1.md) · [Recette Edge](RECETTE_MANUELLE_LOT6F2.md) · [Scénario oral](SCENARIO_SOUTENANCE_LOT6F2.md)

**1er novembre 2026 — 723 tests réexécutés et réussis.** En complément, les contrôleurs frontend relus ont accompli un parcours continu vers Flask/SQLAlchemy/SQLite mémoire puis le DOM administratif : **42 requêtes API, 12 groupes de contrôles réussis**. Le DOM et le transport navigateur sont simulés ; les réponses Flask et les enregistrements SQL sont réels. Aucun serveur HTTP ou navigateur lancé, aucune base réelle consultée. Le kit manuel est inspecté **READY**, sa branche d'écoute reste NON EXÉCUTÉE.

## 1. Fichiers examinés et conservation

Branche `feature/frontend-api-integration`, HEAD `07a9f03ea0a3bdad4a07066fdd7bab1997cc158b`. Départ : **45 fichiers suivis modifiés, 56 non suivis, aucun indexé**. Les empreintes de 115 sources/documents déjà examinés, le statut et l'index Git sont enregistrés avant modification. Le travail antérieur n'est ni supprimé, réinitialisé, écrasé ou committé.

Lectures : bilans 6F.1 et 6E.3 intégralement ; démonstration ; bilans administrateur 6A, 6B, 6D, 6C phase 1 et 6C.2 ; README/instructions de lancement ; dépendances ; `run_local.py`, `backend/index.py`, routes et modèles de comptes/commentaires/signalements, contrôleurs et HTML de compte/dossier/dashboard, harnais et configuration de sélection des tests. Aucune instruction AGENTS.md trouvée dans le dépôt ou ses parents contrôlés.

Les neuf dépendances installées correspondent exactement à `backend/requirements.txt` : Flask 3.1.3, flask-restx 1.3.2, Flask-Cors 6.0.5, Flask-SQLAlchemy 3.1.1, SQLAlchemy 2.0.53, PyMySQL 1.2.0, python-dotenv 1.0.1, Werkzeug 3.1.6, Flask-Migrate 4.1.0 ; Python 3.13.0. Aucun paquet installé ou téléchargé.

**Créés :**

- Ce rapport `docs/soutenance/BILAN_LOT6F2.md`.
- [docs/soutenance/RECETTE_MANUELLE_LOT6F2.md](RECETTE_MANUELLE_LOT6F2.md).
- [docs/soutenance/SCENARIO_SOUTENANCE_LOT6F2.md](SCENARIO_SOUTENANCE_LOT6F2.md).
- [tools/recette_lot6f2.py](../../tools/recette_lot6f2.py) : préparation isolée, sans serveur par défaut ; lancement conditionné à un accord humain distinct.
- [tools/recette_lot6f2_sources.json](../../tools/recette_lot6f2_sources.json) : 65 sources figées et empreintes normalisées CRLF/LF.

**Documents actualisés :** `README.md` principal et, dans `docs/soutenance/`, `README.md`, `DEMONSTRATION.md`, `TESTS_ET_VALIDATION.md`, `INDEX_CODE_JURY.md`, `SUIVI_REMARQUES_JURY.md`. Le README indiquait encore les commentaires/signalements comme API seulement ; cette incohérence documentaire a été signalée puis corrigée. Les démonstrations historiques sont contextualisées et renvoient au protocole courant.

**Aucun code applicatif modifié** : frontend HTML/JS/CSS, backend, modèles, Swagger, migrations et tests existants conservés. Dashboard et fonctionnalités de bannissement/modération/archivage/restauration/purge inchangés. Les sept exclusions antérieures restent non lues ; aucun `.env`, secret, cookie privé, certificat, base réelle ou journal sensible lu ou copié.

## 2. Audit d'intégration

| Point | Constat vérifié |
|---|---|
| Origine et URLs | `/api/v1` relatif ; même middleware pour HTML/JS et Flask ; aucune nouvelle route. La fiche résout le slug avant de transmettre l'id réel aux commentaires |
| Inscription/connexion | Formulaires `app.js` → GET `/me`, POST `/users` avec username/email/password ; POST `/login` ; auteur et rôle décidés par Flask |
| Commentaire | GET/POST `/api/v1/stories/{id}/comments` ; seul `text` dans le POST ; texte requis, limite TEXT UTF-8 65 535 octets, contrôle serveur conservé |
| Signalement | POST `/api/v1/comments/{id}/report`, seul `reason` ; id sélectionné depuis le commentaire reçu ; réponse `type=comment`, `target_id` canonique exactement égal à la cible |
| Session/CSRF | Cookie réel géré par le client WSGI de test, `credentials: include` exigé par le relais JS ; jeton frais par `/me`, transmis dans `X-CSRF-Token` ; jamais persisté dans un reçu |
| Confirmation | Après POST : 201, JSON lisible, statut success et réponse cohérente avant de vider le formulaire et d'annoncer l'enregistrement |
| Refus | 400/401/403/404 sans réussite ; brouillon conservé. Un 403 CSRF réel a été observé sans nouvelle ligne |
| Délai | `apiRequest` : 10 secondes par défaut, AbortController ; les tests existants couvrent le timeout. Aucun délai réel Edge mesuré |
| Résultat incertain | Réponse réseau perdue, 5xx, JSON illisible/incohérent ou statut inattendu après POST : pas de réussite supposée, pas de relance ; blocage local du même type d'envoi |
| Double envoi | Verrou commun dès `/me` jusqu'à la fin du POST ; les deux doubles clics du parcours intégré n'ajoutent pas de doublons |
| XSS | Contenu et pseudonyme par textContent ; les littéraux img/script restent du texte, y compris dans la carte admin du signalement |
| Déconnexion | GET `/me` suivant refusé ; création empêchée. L'actualisation d'une ancienne page admin efface cartes et sept valeurs. Pas de surveillance instantanée inter-onglets |

**Limite détectée avant correction applicative :** inscription.html, connexion.html et admin-connexion.html référencent encore `donnees.js`. Ce fichier historique est exclu des audits précédents et n'est pas lu/exécuté ici. Le premier raccordement s'est arrêté sur cette référence ; la vérification finale exécute explicitement les contrôleurs relus et enregistre les omissions. Aucun contenu ou effet de donnees.js n'est déduit de son seul nom. **Le parcours de tous les scripts des pages de compte n'est donc pas prouvé.** Les trois balises restent intactes ; toute correction exige une autorisation distincte. Le kit manuel bloque cette ressource en 403, sans la lire : limite visible à consigner pendant la recette.

Autres limites existantes : un autre onglet conserve potentiellement une ancienne vue admin jusqu'à requête/pagehide ; le verrou d'incertitude ne survit pas à un rechargement complet ; plusieurs signalements sont permis et Report ne conserve pas l'id de leur émetteur. Aucun reçu persistant, journal d'audit, anti-spam, pagination ou nouvelle règle d'unicité n'est ajouté.

Les différents GET du dashboard ne forment pas un instantané transactionnel global. Leur égalité SQL/DOM a été vérifiée dans ce parcours sans écriture concurrente ; elle ne prouve pas la cohérence de toutes les lectures possibles sous charge.

## 3. Preuve continue exécutée sans navigateur

Les vrais HTML et scripts autorisés sont servis par `create_local_app` en WSGI. Un adaptateur reconstruit leur DOM en mémoire et déclenche les gestionnaires réels. Son fetch de test transfère URL/méthode/en-têtes/JSON à un client WSGI via **stdin/stdout**, puis renvoie la vraie réponse Flask au contrôleur. SQLAlchemy travaille dans une mémoire fictive unique, FK actives. Ni socket, HTTP réseau, Edge, CDP ou base fichier.

| Groupes de contrôles effectivement réussis | Preuve |
|---|---|
| 1–2 : inscription et connexion | Vrais gestionnaires signup/login, 201 et 200, membre ordinaire, mot de passe du formulaire effacé |
| 3 : ouverture, commentaire, XSS et double clic | Slug recette-6f2 → Story 17 ; commentaire confirmé, relu, texte littéral non interprété ; une seule ligne pour cette intention |
| 4 : signalement | Commentaire id 1 sélectionné par le bouton ; Report id 1, FK comment_id=1 ; motif envoyé identique au stockage et à l'administration |
| 5 : refus CSRF | Le relais retire volontairement l'en-tête ; vrai 403, aucune nouvelle ligne, saisie conservée, aucun succès |
| 6–7 : réponses perdues | Le relais jette la réponse de deux vrais POST déjà commités (un commentaire puis un signalement) ; UI Résultat incertain, pas de second POST ; le commentaire est retrouvé par GET |
| 8 : déconnexion et nouvelle tentative | POST logout réel, puis `/me` 401 ; aucun commentaire supplémentaire créé |
| 9–10 : accès admin | Visiteur refusé par `/me`, membre refusé par le contrôle de rôle ; données masquées |
| 11 : administration et SQL | Connexion administrateur réelle ; les deux signalements sont affichés sans exécuter leur texte ; sept valeurs DOM exactement égales aux SELECT |
| 12 : déconnexion admin | Ancien dashboard actualisé : `/me` 401, cartes privées masquées et sept valeurs `—` |

Les **42 requêtes API** comprennent 32 réponses 200, 5 réponses 201, 4 réponses 401 et 1 réponse 403. Les lectures HTML/JS WSGI sont distinctes de ce compte. Le cookie de session est véritablement émis et relu par Flask dans le client WSGI ; cela ne prouve pas sa gestion effective par Edge.

Comparaison finale SQL/DOM, exclusivement dans cette mémoire :

| Indicateur | Valeur observée | Source |
|---|---:|---|
| Dossiers actifs | 2 | Story active / GET stories |
| Histoires résolues | 1 | Catégorie 1 des actifs |
| Cold Cases | 1 | Catégorie 2 des actifs |
| Utilisateurs | 2 | Un admin de fixture + le membre réellement inscrit dans ce parcours |
| Commentaires | 2 | Premier confirmé + second dont la réponse a été volontairement perdue |
| Signalements | 2 | Premier confirmé + second dont la réponse a été volontairement perdue, même commentaire cible |
| Propositions en attente | 0 | Aucune proposition créée dans ce parcours ; le zéro est affiché normalement |

Aucun compteur artificiel, aucune contribution de remplissage, aucune fixture importée dans la base du site. Les deux dossiers et l'admin sont la préparation minimale de ce test ; les autres lignes résultent des formulaires exercés. Les textes, auteur, story_id, comment_id et motifs sont comparés aux enregistrements ORM relus. `PRAGMA database_list` ne donne aucun fichier, foreign_keys=1 et foreign_key_check est vide. Les GET/refus de cette vérification n'ajoutent aucune ligne.

## 4. Non-régression et statut des vérifications

| Type | Exécution 6F.2 | Échecs / erreurs / ignorés |
|---|---:|---|
| Backend sélectionné | **279 PASS** | 0 / 0 / 0 |
| Frontend | **428 PASS** | 0 échec/annulé/ignoré |
| Lanceur/HTML/WSGI | **16 PASS** | 0 / 0 / 0 |
| Total des suites | **723 PASS** | Pas de cumul avec les 723 historiques de 6F.1 |
| Script d'intégration supplémentaire | 1 parcours, 12 groupes réussis, 42 requêtes | Rapport séparé ; pas compté comme 12 nouveaux tests unittest |
| Kit de recette sans serveur | **READY** | Dernière inspection sans tentative interdite |
| Contrôles statiques | Sources/contrats, dépendances, HTML/liens, empreintes et préservation | Ne prouvent pas une recette navigateur |
| Edge réel / branche d'écoute / clavier, responsive, accessibilité réels | **NON EXÉCUTÉS** | Autorisation spécifique d'exécution attendue |
| MySQL/Aiven, sept tests de migration, durabilité après redémarrage | **NON EXÉCUTÉS** | Hors autorisation ; aucun succès déduit de SQLite |

Harnais inspecté avant lancement : 65 sources autorisées épinglées par SHA-256, configuration enfant minimale, dotenv neutralisé avant import, six valeurs Aiven vides, SQLite `:memory:` exclusivement avec FK sur chaque connexion. Blocage MySQL/bases fichier/ATTACH/DETACH, sockets/DNS, sous-processus applicatifs, lectures privées, écritures du dépôt et commandes/exécution de migrations. Les sondes sont séparées des suites. **Tous les compteurs interdits des suites et du parcours intégré retenu valent zéro.**

Un seul passage complet des suites : `attempt-1`. Les six tests de `test_report_migration.py` et le test de migration d'archivage restent exclus, non exécutés et non comptés comme PASS ; liste dans `backend.guard.json`. Les tests existants ne sont pas modifiés. Aucun nouveau test unitaire n'est ajouté faute de défaut applicatif à corriger ; le nouveau script vérifie le raccordement demandé.

**Essais de préparation échoués conservés :** le premier relais a refusé la balise du script exclu ; le second a révélé un décodage stdin Windows différent d'UTF-8 et échoué sur l'accent du motif. La sélection explicite avec omission et le décodage UTF-8 corrigent le harnais, sans changer les contrôleurs ou réduire l'assertion d'égalité du texte. Le troisième passage intégré réussit. La première inspection du kit manuel a échoué sur les compteurs du garde de lecture ; la correspondance des caches Python avec les seules sources approuvées, déjà employée par le harnais historique, a permis READY. Ces essais ne sont ni effacés ni annoncés comme succès applicatifs.

## 5. Preuves et fichiers de vérification

```text
[chemin local privé retiré]
```

`baseline.json`, `dependencies.json`, `preflight.json`, `harness-inspection.json`, `attempt-1/commands.json` et journaux des trois suites, `backend.guard.json`, `launcher.guard.json`, `attempt-1/frontend.node-guard.json`, `integration-frontend.json`, `integration-sql.json`, `integration-exchanges.json`, `integration-omissions.json`, gardes intégrés, deux erreurs initiales et `final-validation.json`. Les corps de messages du relais (mots de passe fictifs, cookie, CSRF) ne sont pas archivés. Les preuves ne contiennent que des statuts, booléens, ids et résultats métier fictifs nécessaires.

Scripts supplémentaires dans ce répertoire : `run-integration.py`, `frontend-worker.cjs`, `wsgi-worker.py`, `python-integration-bootstrap.py`. Le coordinateur lance deux enfants contrôlés ; ceux-ci ne peuvent pas lancer de sous-processus applicatif ou faire de réseau. Ce dispositif de test n'est pas une nouvelle architecture de l'application.

Dernier reçu d'inspection du kit manuel :

```text
[chemin local privé retiré]
```

READY, FK actives, aucun fichier de base, serveur et navigateur non démarrés, sept compteurs de garde à zéro. Le lancement `--serve` sans marqueur d'accord est refusé avant préparation ; **aucune branche d'écoute exécutée**. Les scripts et preuves temporaires sont susceptibles de nettoyage : le kit et les protocoles permanents restent dans le dépôt, sans modifier l'instantané durable 6E.1.

## 6. Recette manuelle et soutenance

La [procédure Edge détaillée](RECETTE_MANUELLE_LOT6F2.md) donne prérequis, transfert vers une machine de l'école, inspection sans serveur, commande proposée après autorisation, fenêtre InPrivate manuelle, adresses, 16 étapes, résultats attendus, preuves et arrêt. **La commande normale run_local.py n'est pas employée**, car elle lit `.env` et un groupe Aiven complet prend priorité sur DATABASE_URL. Définir cette URL seule ne constitue pas une isolation.

Le [scénario de 14 minutes](SCENARIO_SOUTENANCE_LOT6F2.md) répartit actions, résultats, fichiers/routes, données écrites, vérifications et replis : Mélissa présente navigation/formulaires/DOM, Sylvie explique routes/session/CSRF/erreurs, Mahamadou explique SQLAlchemy/FK/transactions et les sept agrégats. Les textes simples à mémoriser accompagnent le tableau. Aucune migration ou purge réelle n'est nécessaire devant le jury.

En cas de navigateur ou machine indisponible : présenter les sources et preuves isolées explicitement identifiées, sans prétendre à un parcours Edge effectué. Une perte de réponse appelle une vérification, jamais un renvoi réflexe. Aucun secret, chiffre imposé ou capture réseau complète dans les diapositives.

## 7. Défauts, limites et autorisations restantes

| Point | État et décision nécessaire |
|---|---|
| Ancienne description commentaires/signalements API seulement | Incohérence documentaire corrigée dans le README principal ; application inchangée |
| Balises donnees.js sur trois pages de compte | Références confirmées ; contenu/effets non examinés. Étendre la revue ou autoriser leur retrait séparément avant de revendiquer la couverture de tous les scripts. Aucun retrait effectué |
| Rendu Edge et réseau local | Protocole/kit prêts ; autorisation spécifique serveur `127.0.0.1:5062` et Edge manuel nécessaire selon section 5 de la demande. Aucun CDP prévu |
| Session entre onglets, résultats incertains après rechargement, absence de journal/unicité/identité du déclarant | Limites existantes documentées ; aucune promesse d'effacement instantané ou d'attribution persistante. Éventuels changements applicatifs à autoriser séparément |
| Cible MySQL, contraintes et migrations réellement déployées | Non consultées. SQLite ignore notamment les verrous de ligne ; tests mémoire sans preuve de durabilité, concurrence MySQL ou migration de la cible |
| RGPD | Notices et brouillon conservés ; aucune politique incomplète publiée, choix humains de responsable/contact/bases/conservation/hébergement toujours non inventés |

**Aucune régression applicative détectée dans les contrôleurs relus et les tests exécutés.** Cela ne signifie pas absence de défaut dans les scripts exclus, le navigateur ou la cible réelle. Aucune correction applicative engagée sans accord.

## 8. Verdict et arrêt

**GO pour la revue des preuves et la préparation de soutenance. Recette navigateur non validée ; déploiement/MySQL non validés.** Prochaine action recommandée : décider du traitement du script historique puis autoriser une courte recette manuelle sur la mémoire isolée avec le kit inspecté. Aucun besoin démontré de framework, refonte RGPD, service supplémentaire, modification de dashboard ou faux peuplement.

**Préservation finale vérifiée :** six documents préexistants actualisés, cinq fichiers créés, 109 autres fichiers examinés identiques ; code applicatif/tests/migrations/dashboard et 115 fichiers de la sauvegarde durable conservés par SHA-256. Les 204 repères de code et 22 remarques sont inchangés ; 435 références Markdown locales contrôlées dans les documents concernés. État final : **45 fichiers suivis modifiés, 61 non suivis, aucun indexé** ; branche, HEAD et empreinte de l'index Git préservés. Ces nombres incluent le travail antérieur.

Arrêt après 6F.2, en attente de validation. Aucun accès au `.env` privé ou à MySQL/Aiven, migration, modification Windows, ouverture de navigateur, lancement HTTP, changement de branche, commit, push, suppression ou publication de politique incomplète.
