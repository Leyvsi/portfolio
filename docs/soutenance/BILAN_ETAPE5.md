# Bilan de l’étape 5 — documentation et commentaires

> Archive pédagogique datée : les résultats et descriptions ci-dessous concernent le lot indiqué. Les anciens repères de ligne ne décrivent pas la version candidate. Pour préparer la soutenance actuelle, consulter les quatre fiches et le référentiel reliés au sommaire.

> Copie publique de référence : les chemins personnels et liens de travail internes sont retirés. Les preuves et commandes historiques gardent leur date et leur périmètre ; utiliser le README actuel pour le lancement.

> **Document historique conservé.** Les corrections et contrôles autorisés de l'étape 5.1 sont présentés dans le [nouveau bilan](BILAN_ETAPE51.md) et le [suivi du jury](SUIVI_REMARQUES_JURY.md). Les verdicts de rendu ci-dessous décrivent les sources antérieures ; aucun nouveau rendu n'est effectué en 5.1.

[Sommaire](README.md) · [Index du code](INDEX_CODE_JURY.md) · [Tests et validation](TESTS_ET_VALIDATION.md)

Travail local du **29 octobre 2026**, branche `feature/frontend-api-integration`, HEAD conservé `07a9f03ea0a3bdad4a07066fdd7bab1997cc158b`. Aucun commit ni push. Cette étape est limitée aux commentaires, documents et supports de soutenance.

## Changements livrés

- **17 fichiers de code**, **212 lignes de commentaires français ajoutées** : serveur, sessions, CSRF, rôles, validations, transactions, neuf modèles, relations, DOM, fetch et tableau admin. Aucune instruction exécutable, signature, route ou donnée changée.
- **7 documents existants actualisés** : les deux README, le sommaire de soutenance et les quatre fiches historiques. Les **76 questions et réponses courtes historiques sont conservées** ; 70 liens de lignes anciennes ont été recalculés.
- **7 nouveaux supports** : tests/preuves, architecture/sécurité/RGPD, index de 93 repères, démonstration, modèle CSV fictif, réponses orales et présent bilan.
- **3 diagrammes Mermaid révisés**, présents dans 6 blocs synchronisés : architecture avec DOM/fichiers/SQLite embarqué, relations et flux de théorie.

## Fichiers concernés

| Fichier | Modification |
|---|---|
| [run_local.py](../../run_local.py) | Commentaires seuls |
| [backend/index.py](../../backend/index.py) | Commentaires seuls |
| [backend/models.py](../../backend/models.py) | Commentaires seuls |
| [backend/api/v1/app.py](../../backend/api/v1/app.py) | Commentaires seuls |
| [backend/api/v1/views/__init__.py](../../backend/api/v1/views/__init__.py) | Commentaires seuls |
| [backend/api/v1/views/permissions.py](../../backend/api/v1/views/permissions.py) | Commentaires seuls |
| [backend/api/v1/views/write_support.py](../../backend/api/v1/views/write_support.py) | Commentaires seuls |
| [backend/api/v1/views/users.py](../../backend/api/v1/views/users.py) | Commentaires seuls |
| [backend/api/v1/views/histoires.py](../../backend/api/v1/views/histoires.py) | Commentaires seuls |
| [backend/api/v1/views/theories.py](../../backend/api/v1/views/theories.py) | Commentaires seuls |
| [backend/api/v1/views/comments.py](../../backend/api/v1/views/comments.py) | Commentaires seuls |
| [backend/api/v1/views/proposals.py](../../backend/api/v1/views/proposals.py) | Commentaires seuls |
| [backend/api/v1/views/index.py](../../backend/api/v1/views/index.py) | Commentaires seuls |
| [frontend/api.js](../../frontend/api.js) | Commentaires seuls |
| [frontend/app.js](../../frontend/app.js) | Commentaires seuls |
| [frontend/theories-list.js](../../frontend/theories-list.js) | Commentaires seuls |
| [frontend/admin-dashboard.js](../../frontend/admin-dashboard.js) | Commentaires seuls |
| [README.md](../../README.md) | Actualisation documentaire |
| [frontend/README.md](../../frontend/README.md) | Actualisation documentaire |
| [docs/soutenance/fiche-commune.md](fiche-commune.md) | Actualisation documentaire |
| [docs/soutenance/fiche-mahamadou.md](fiche-mahamadou.md) | Actualisation documentaire |
| [docs/soutenance/fiche-melissa.md](fiche-melissa.md) | Actualisation documentaire |
| [docs/soutenance/fiche-sylvie.md](fiche-sylvie.md) | Actualisation documentaire |
| [docs/soutenance/README.md](README.md) | Actualisation documentaire |
| [docs/soutenance/TESTS_ET_VALIDATION.md](TESTS_ET_VALIDATION.md) | Nouveau support |
| [docs/soutenance/ARCHITECTURE_SECURITE_RGPD.md](ARCHITECTURE_SECURITE_RGPD.md) | Nouveau support |
| [docs/soutenance/INDEX_CODE_JURY.md](INDEX_CODE_JURY.md) | Nouveau support |
| [docs/soutenance/DEMONSTRATION.md](DEMONSTRATION.md) | Nouveau support |
| [docs/soutenance/COMPTES_DEMO.exemple.csv](COMPTES_DEMO.exemple.csv) | Nouveau support |
| [docs/soutenance/ORAL_JURY.md](ORAL_JURY.md) | Nouveau support |
| [docs/soutenance/BILAN_ETAPE5.md](BILAN_ETAPE5.md) | Nouveau support |

## Vérifications effectuées

| Contrôle | Résultat |
|---|---|
| Code Python | **13 fichiers** analysés par ast.parse et compile en mémoire ; AST avant/après identiques, sans import applicatif ni exécution du site. |
| Code JavaScript | **4 fichiers** : node --check, syntaxe valide ; aucun script applicatif exécuté. |
| Commentaires seulement | Retirer les blocs ajoutés restitue exactement les octets d’origine des **17 fichiers**, BOM et fins de ligne existantes compris. |
| Index | **93 repères** vérifiés contre les définitions/événements réels et les liens relatifs #L. |
| Fiches de l’équipe | 22 + 18 + 18 + 18 questions/réponses courtes identiques aux textes avant modifications. |
| Routes et contrat | Analyse statique : les **24 opérations** Flask correspondent au document OpenAPI. Aucun appel HTTP du site. |
| Mermaid | Parse et rendu hors ligne avec le bundle local **Mermaid 11.16.0**, Playwright **1.58.2** et Microsoft Edge **156.0.4314.42** headless ; trois rendus et SVG XML valides. Neuf entités et dix relations réellement présentes dans le SVG ER. |
| Copies des diagrammes | Six blocs correspondent exactement aux trois diagrammes canoniques. |
| Réseau/rendu | Zéro requête externe dans le contrôle de diagrammes ; contexte hors ligne, ressources locales, profil neuf ensuite fermé et supprimé. Aucun serveur applicatif ni base ouvert. |
| Modèle de comptes | Deux identités fictives @example.invalid ; marqueurs sans mot de passe utilisable ; copie privée à conserver hors dépôt. |
| Intégrité | Branche, HEAD, index Git, fichiers non concernés et deux fichiers non suivis préexistants conservés ; .env contrôlé uniquement par métadonnées. |
| Liens documentaires | Tous les liens internes des 13 Markdown contrôlés localement : cibles, ancres de titres et plages de lignes. Les URL externes/GitHub ne sont pas consultées. |

Commandes des contrôles : Python `.venv\Scripts\python.exe -I -B` avec les scripts de contrôle hors dépôt ; `node --check` sur chacun des quatre scripts modifiés ; `git --no-optional-locks diff --check` puis `git --no-optional-locks -c core.whitespace=cr-at-eol diff --check`. Les argv complets, sorties et empreintes figurent dans les reçus locaux. Les sources Python sont compilées en mémoire via compile(), sans exec ni création de pyc.

Le contrôle Git brut signale **14 fins de ligne CRLF** sur les commentaires ajoutés à backend/api/v1/views/index.py ; les autres octets de ce fichier ont été préservés. Le contrôle tenant compte de CR en fin de ligne termine à **0**, sans blanc final supplémentaire. Git annonce aussi ses conversions LF/CRLF habituelles sur certains fichiers ; aucun réglage Git ni normalisation globale n’a été appliqué. Les anciennes alertes de styles.css ne sont pas des modifications de cette étape.

Le premier relevé du rendu Mermaid utilisait Object.keys sur la collection d’entités et indiquait 0 ; ce nombre ne comptait pas les entités rendues. Le contrôle XML complémentaire compte les **neuf groupes de tables et dix chemins de relation** effectivement dessinés, sans nouvelle exécution du rendu. Les deux reçus restent conservés. Le rendu a été inspecté visuellement par l’assistant ; cela n’est pas une recette humaine du site.

## Résultats antérieurs conservés

| Campagne | Bilan qui reste valable dans son périmètre |
|---|---|
| Étape 2, 29/10 | **439 réussites** : 205 backend, 226 frontend, 8 lanceur ; trois sorties 0. |
| Étape 3, Edge réel automatisé | **28 PASS / 2 FAIL de contrôle Swagger / 0 BLOQUÉ / 7 NON EXÉCUTÉS**. |
| Étape 4 | **Dix BDD PASS** ; bilan consolidé **15 PASS / 1 FAIL initial suivi d’une reprise / 0 BLOQUÉ / 1 NON EXÉCUTÉ** ; huit créations persistées, vingt refus attendus. |

Aucune de ces suites n’a été relancée à l’étape 5. La restitution octet pour octet des instructions et l’égalité des AST prouvent la nature documentaire des changements, pas une nouvelle campagne de 439 tests. Les scénarios Edge/BDD ne sont pas ajoutés à ce nombre. La reprise signée de l’étape 4 ne revalide pas le mot de passe. Aucun test MySQL/Aiven ni migration Alembic attesté ; aucune conformité RGPD déclarée.

## Preuves locales et réserves

Répertoire de cette étape sous `$env:TEMP` : `portfolio-doc-etape5-20261029-d249637e935e4d37a47055aeceb13f87`. Il contient baseline.json et les copies avant modification, comment-only-verification.json, syntax-verification.json, index-entries.json, line-link-updates.json, historical-questions-before.json, mermaid-verification.json, mermaid-structure-verification.json, SVG/PNG, validation.json et le diff complet. Les preuves des étapes 2/3/4 restent hors dépôt et ne sont pas remplacées. Les répertoires temporaires doivent être conservés localement pour une présentation ultérieure ; ils ne sont pas livrés dans un clone GitHub.

Les scripts auxiliaires ont d’abord rencontré un BOM UTF-8 dans le module de compatibilité : la lecture statique a été adaptée, sans modifier ce BOM ni importer l’application. Aucun résultat fonctionnel n’est lié à cet incident.

Rendu Mermaid sur GitHub et liens distants non attestés ; recette humaine, POST Swagger complets, MySQL/Aiven, migrations, cascades/suppressions et fonctions RGPD restent à traiter séparément. Les secrets restent exclusivement dans les emplacements privés ; aucun compte de démonstration n’a été créé par cette étape.

Aucune donnée, migration, configuration privée ou logique métier modifiée. Aucun accès Aiven, commit ou push. **Aucune nouvelle étape engagée : validation utilisateur attendue.**


## Complément — vérification visuelle autorisée

Ce contrôle complémentaire a exécuté **une seule fois**, après inspection, le script `render-mermaid.cjs` autorisé par l’utilisateur. Les résultats techniques et visuels sont distingués : **3 PASS de syntaxe/SVG, mais 1 PASS et 2 FAIL visuels**. Ces verdicts de présentation complètent la ligne Mermaid technique du tableau précédent.

| Diagramme / source canonique | Syntaxe Mermaid | SVG valide | Résultat visuel | Problème restant |
|---|---|---|---|---|
| Architecture générale — [README.md](../../README.md) | PASS, aucune erreur | Oui | **FAIL** | Le connecteur frontend/ → SharedDataMiddleware traverse la zone du bloc Flask, qui en masque une partie. Cela rend son trajet ambigu. |
| Modèle relationnel — [README.md](../../README.md) | PASS, aucune erreur | Oui | **PASS** | Aucun chevauchement important ; neuf tables et dix relations lisibles. |
| Flux frontend/API/base — [README.md](../../README.md) | PASS, aucune erreur | Oui | **FAIL** | La longue note finale déborde de son encadré jaune à gauche et à droite. Son texte reste lisible, mais sa présentation doit être corrigée. |

Exécution UTC : 2026-10-29T18:45:28.600Z à 2026-10-29T18:45:31.637Z, sortie 0. Edge 156.0.4314.42 headless, Playwright 1.58.2, Mermaid 11.16.0 déjà disponibles localement. Les trois PNG ont été examinés visuellement par l’assistant ; aucune recette humaine du site revendiquée.

La liaison des fichiers doit être repositionnée pour ne plus passer derrière Flask. La note finale du flux doit être scindée en plusieurs lignes ou son encadré élargi. Les sources des diagrammes sont conservées : **aucune correction ni relance automatique** pendant ce contrôle. Le mauvais compteur technique d’entités reste diagnostiqué séparément du SVG contenant effectivement neuf tables.

Contexte hors ligne, ressources file:// autorisées uniquement, proxy/DNS bloqués et zéro requête distante enregistrée. Aucun Flask/site/serveur HTTP démarré, aucun accès à une base applicative, aucun .env chargé et aucun téléchargement. Seul le contexte Edge de cette vérification a été fermé ; profil temporaire supprimé et absence confirmée.

Les preuves précédentes sont archivées, et le rapport par diagramme, SVG/PNG, reçus et empreintes sont conservés sous `$env:TEMP` / `portfolio-doc-etape5-20261029-d249637e935e4d37a47055aeceb13f87` / `render-authorized-20261029T184436Z-7cec3abd`. Le rapport détaillé se nomme `rapport-mermaid.md`. Le rendu sur GitHub reste non vérifié.

L’étape 5 est documentée avec ces **deux réserves visuelles à corriger après validation**, sans modification du fonctionnement applicatif. Aucun commit ni push ; validation utilisateur attendue.
