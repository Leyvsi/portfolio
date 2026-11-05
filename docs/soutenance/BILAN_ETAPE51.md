# Bilan de l'étape 5.1 — reprise et compléments documentaires

> Archive pédagogique datée : les résultats et descriptions ci-dessous concernent le lot indiqué. Les anciens repères de ligne ne décrivent pas la version candidate. Pour préparer la soutenance actuelle, consulter les quatre fiches et le référentiel reliés au sommaire.

[Sommaire](README.md) · [Suivi du jury](SUIVI_REMARQUES_JURY.md) · [Index du code](INDEX_CODE_JURY.md) · [Réponses orales](ORAL_JURY.md)

Travail local du **29 octobre 2026**, après audit de reprise puis autorisation explicite de l'utilisateur. Branche conservée : `feature/frontend-api-integration` ; HEAD : `07a9f03ea0a3bdad4a07066fdd7bab1997cc158b`. Les changements préexistants de l'étape 5 sont conservés. Les étapes 1 à 5 ne sont pas recommencées.

## Livrables et couverture des commentaires

Douze fichiers de code ont reçu des compléments ciblés dans les sources réellement utilisées : **79 lignes de commentaires ajoutées et deux anciens commentaires anglais remplacés**, soit 77 lignes supplémentaires. Les scripts de migration ont seulement reçu des commentaires ; leurs opérations, révisions et dépendances n'ont pas changé. Aucun import de l'application ni d'Alembic n'est nécessaire à ces contrôles.

| Membres concernés | Vrai fichier | Couverture déjà présente | Complément 5.1 |
|---|---|---|---|
| Mélissa | `frontend/api.js` | fetch, cookies, CSRF, statuts et erreurs | Annulation/délai et limite d'annulation des POST ; nettoyage des écouteurs ; contrôle d'accès avant lecture du corps ; validation des structures et rôles des helpers. |
| Mélissa | `frontend/app.js` | DOM, recherche, dossiers, formulaires, sessions, replis | Progression bornée des sources d'image et rôle du texte alternatif. |
| Mélissa | `frontend/theories-list.js` | Sélection publique, version des requêtes, cartes en texte | Début/fin du chargement, état accessible et convention UTC/Paris ; commentaire de date traduit. |
| Mélissa | `frontend/admin-dashboard.js` | Contrôle de session, effacement, compteurs et chargement | Invalidation des réponses, dates, cartes de consultation et retour depuis le cache de navigation. |
| Sylvie, Mahamadou | `backend/api/v1/views/theories.py` | Lecture/création/like, compte, validation et transaction | Rôle de `theory_to_dict`, champs JSON et date sans écriture SQL. |
| Sylvie, Mahamadou | `backend/api/v1/views/proposals.py` | Consultation privée, création pending et transaction | Rôle de `proposal_to_dict` et distinction entre sérialisation et permissions. |
| Mahamadou, Sylvie | `backend/models.py` | Neuf classes, PK/FK, relations, contraintes et hachage | Sérialisation de Story, Comment, Report et ColdCaseUpdate ; absence de modification des références et collections. |
| Mahamadou | `migrations/env.py` | Gabarit et explications majoritairement anglaises | Moteur, URL privée, métadonnées, modes offline/online et suppression des révisions vides. |
| Mahamadou | `migrations/versions/921687c1bd7c_baseline_schema.py` | Schéma initial | Rôle d'upgrade/downgrade et limite de restauration des données. |
| Mahamadou | `migrations/versions/3111f5767fc6_ajoute_les_regles_on_delete.py` | Règles SQL et commentaires anglais | FK nommées, CASCADE/SET NULL et distinction des cascades ORM. |
| Mahamadou | `migrations/versions/a590c8aac613_add_reports_bans_and_cold_case_updates.py` | Deux tables et colonne is_banned | Rôle du défaut SQL temporaire et conséquences du downgrade. |
| Mahamadou | `migrations/versions/82deda84bc35_remove_legacy_comment_reports_counter.py` | Retrait du compteur ancien | Source du comptage et absence de reconstitution historique au downgrade. |

Les fonctions importantes des parcours audités disposent désormais d'explications ciblées ; aucune prétention à commenter chaque utilitaire évident ou à mesurer une couverture automatisée des commentaires. La copie `revision_code/mahamadou/backend/models.py` reste préservée et n'est pas utilisée comme substitut au vrai code.

La [matrice du jury](SUIVI_REMARQUES_JURY.md) contient **22 lignes** : neuf remarques Houssem, deux Pauline, neuf communes, plus hébergement et provenance des images séparés. Elle donne membres, fichiers, état, correction réalisée, reste, contrôles futurs et statut. Le [support oral](ORAL_JURY.md) passe de 15 à **18 questions**, avec une répartition par membre et une réponse complète sur les images. Les **76 questions et réponses courtes historiques** restent conservées dans les quatre fiches.

L'[index](INDEX_CODE_JURY.md) comporte **124 repères** : les 93 existants et 31 compléments sans doublon de cible. **74 liens de lignes existants** ont été recalculés dans les supports à partir de l'état réel avant 5.1, et non des seules lignes du HEAD.

## Sources Mermaid ajustées, rendu non exécuté

| Diagramme | Modification de source | Portée de la preuve |
|---|---|---|
| Architecture | Remplacement de la liaison remontante `FRONT → STATIC : octets lus` par `STATIC → FRONT : lit les fichiers publics`, pour orienter le lien vers la lecture effectuée par le middleware. | Les composants et leur rôle sont conservés ; la disparition du chevauchement reste à confirmer visuellement. |
| Flux | Note finale scindée en trois lignes explicites avec `<br/>`, sans changer les messages, participants ou branches. | Le texte décrit le même comportement ; son encadrement reste à confirmer dans un nouveau rendu. |
| Relationnel | Aucune modification. | Les deux copies restent identiques à celles du dernier rendu local validé : neuf tables et dix relations. |

Les trois sources canoniques du README et leurs trois copies documentaires sont synchronisées. La réserve visuelle est annoncée dans les supports de navigation, fiches, démonstration et architecture. Les PNG/SVG historiques ne sont ni remplacés ni présentés comme des rendus des nouvelles sources.

**Aucun navigateur ni serveur n'est lancé.** Le contrôle est complété par le parseur Mermaid local : les trois sources canoniques passent la syntaxe, sans appeler le moteur de mise en page ni la fonction de rendu. Une validation visuelle réelle nécessite une autorisation de navigateur distincte. Les demandes H-03 et P-01 restent **À VÉRIFIER** dans la matrice.

## Contrôles statiques locaux

Les résultats détaillés et les commandes locales sont conservés dans les reçus indiqués ci-dessous. Ce sont des vérifications documentaires et syntaxiques ; aucun test fonctionnel n'est relancé.

| Contrôle exécuté | Résultat |
|---|---|
| Différences du code depuis l'instantané avant 5.1 | **PASS : 12 fichiers, commentaires seuls**. Les segments inchangés conservent leurs octets ; BOM et fins de ligne existants sont préservés. |
| Python | **PASS : huit fichiers** ; arbres AST identiques avant/après, analyse et compilation en mémoire sans import applicatif, sans exécution et sans pyc. |
| JavaScript | **PASS : quatre fichiers**, `node --check` ; les différences ne touchent que des lignes de commentaires, les instructions existantes sont conservées. |
| Diagrammes | **PASS statique : six blocs synchronisés** ; seules les deux substitutions prévues sont présentes. Les deux blocs BDD sont identiques à l'instantané : neuf entités et dix relations déclarées. Un contrôle de syntaxe séparé par le parseur Mermaid passe sur les trois sources ; aucun rendu exécuté. |
| Syntaxe Mermaid | **PASS : trois sources canoniques** (`flowchart-v2`, `er`, `sequence`) via le bundle local Mermaid 11.16.0, Node 24.16.0 et jsdom 28.1.0 utilisé pour l'assainissement des textes. Imports limités aux assets locaux, réseau bloqué, zéro tentative réseau enregistrée ; aucun navigateur ni appel à `render`. |
| Questions historiques | **PASS : 76 questions et réponses courtes identiques**, comparées au contenu précédant 5.1. |
| Liens locaux | **PASS : 619 liens internes dans 16 Markdown**, dont 205 liens de lignes ; cibles, ancres de titres, bornes et libellés de lignes vérifiés. Aucune URL externe consultée. |
| Index du code | **PASS : 124 repères**, avec les 93 cibles historiques conservant leur instruction de référence ; les 31 ajouts pointent sur les définitions ou événements réels. |
| Matrice du jury | **PASS : 22 lignes de suivi et neuf colonnes, dont les huit demandées et une colonne de preuves explicites**, sans confondre travaux réalisés et tests futurs. |
| Git | **PASS : branche, HEAD et index inchangés** ; aucun fichier préexistant supprimé. `git --no-optional-locks -c core.whitespace=cr-at-eol diff --check` termine à 0. |

Commande de contrôle : `.venv\Scripts\python.exe -I -B` suivi du chemin local de `validate-static.py` dans le dossier de preuves ci-dessous. Ce script analyse les fichiers autorisés, compare les instantanés, vérifie les liens et lance seulement `node --check` et les commandes Git en lecture seule. Le contrôle final utilise la copie adaptée `completion/validate-static.py` ; les argv, sorties, empreintes et résultats finaux sont enregistrés dans `completion/static-validation.json`. Le reçu initial `static-validation.json` reste conservé. Aucune configuration privée n'est chargée.

Commande de syntaxe Mermaid : `node --experimental-vm-modules` suivi du chemin de `completion/mermaid-parse.cjs` dans le dossier de preuves. Le script appelle uniquement `mermaid.parse()` dans une VM Node avec un DOM jsdom en mémoire ; il ne lance pas de navigateur et ne mesure aucune géométrie. Les trois résultats et empreintes des sources sont dans `completion/mermaid-syntax.json`. Le DOM ne reçoit aucune page applicative et les scripts de page sont désactivés.

Le premier montage du harnais a nécessité deux adaptations locales : utilisation de l'API de ressources de jsdom 28 à la place de ResourceLoader, puis exposition de WebCrypto à la VM. Ces incidents du harnais sont corrigés ; ils ne sont pas des échecs de syntaxe des diagrammes. Le reçu d'échec WebCrypto est conservé dans `completion/mermaid-syntax-attempt1.json`. Le contrôle final des trois diagrammes termine à 0.

## Preuves et réserves conservées

Le dossier local sous `$env:TEMP` se nomme `portfolio-etape51-20261029-9f4a3b680b874395bca4d0f5bfa0e58e`. Il contient `baseline.json` (copies des seuls fichiers de code/documentation concernés avant 5.1, état Git et index), `reference-updates.json` (correspondances de lignes et nouveaux repères), les scripts statiques de maintenance/contrôle et les reçus de validation. Il ne contient aucune copie de `.env`, cookies, certificats ou base. Les preuves des étapes précédentes ne sont ni modifiées ni remplacées ; elles restent référencées dans [Tests et validation](TESTS_ET_VALIDATION.md) et le [bilan 5](BILAN_ETAPE5.md). Ces dossiers temporaires hors Git ne sont pas livrés dans un clone.

Les résultats historiques restent : **439 réussites automatiques** (205 backend, 226 frontend, huit lanceur) ; étape 3 **28 PASS, deux FAIL Swagger, sept NON EXÉCUTÉS** ; dix BDD PASS à l'étape 4, avec bilan consolidé **15 PASS, un FAIL initial suivi d'une reprise et un NON EXÉCUTÉ**. Les campagnes ne s'additionnent pas et ne deviennent pas de nouvelles réussites 5.1.

Les fonctions de bannissement dans l'interface, consultation dédiée admin, suppression, consentement et autres demandes RGPD ne sont pas développées. Le fichier privé des comptes n'est pas lu ou créé. L'hébergement de production, la provenance et les droits des illustrations restent à confirmer. Aucun accès MySQL/Aiven, migration appliquée, secret lu, fichier préexistant supprimé, changement de branche, commit ou push. Le prochain travail de rendu ou de développement reste distinct de cette autorisation documentaire.

## Liste exacte des fichiers de l'étape 5.1

Comparaison avec l'instantané local avant 5.1 : **25 fichiers existants modifiés et deux créés**. Ce périmètre ne confond pas les travaux de cette étape avec toutes les différences déjà présentes par rapport au HEAD. Certains supports modifiés étaient déjà non suivis avant 5.1.

Fichiers existants modifiés :

```text
README.md
backend/api/v1/views/proposals.py
backend/api/v1/views/theories.py
backend/models.py
docs/soutenance/ARCHITECTURE_SECURITE_RGPD.md
docs/soutenance/BILAN_ETAPE5.md
docs/soutenance/DEMONSTRATION.md
docs/soutenance/INDEX_CODE_JURY.md
docs/soutenance/ORAL_JURY.md
docs/soutenance/README.md
docs/soutenance/fiche-commune.md
docs/soutenance/fiche-mahamadou.md
docs/soutenance/fiche-melissa.md
docs/soutenance/fiche-sylvie.md
frontend/README.md
frontend/admin-dashboard.js
frontend/api.js
frontend/app.js
frontend/images/README.md
frontend/theories-list.js
migrations/env.py
migrations/versions/3111f5767fc6_ajoute_les_regles_on_delete.py
migrations/versions/82deda84bc35_remove_legacy_comment_reports_counter.py
migrations/versions/921687c1bd7c_baseline_schema.py
migrations/versions/a590c8aac613_add_reports_bans_and_cold_case_updates.py
```

Fichiers créés dans le dépôt à cette étape :

```text
docs/soutenance/BILAN_ETAPE51.md
docs/soutenance/SUIVI_REMARQUES_JURY.md
```

Les 24 fichiers initialement modifiés et les neuf fichiers initialement non suivis restent présents. Le statut Git total est désormais de 30 fichiers suivis modifiés et 11 fichiers non suivis : les six fichiers suivis supplémentaires sont le README des images et les cinq scripts Alembic seulement commentés ; les deux nouveaux supports expliquent les deux fichiers non suivis supplémentaires. Aucun fichier n'est indexé. Le fichier `revision_code/mahamadou/backend/models.py` et l'archive narrative `frontend/histoires-originales.json` ne sont pas modifiés par 5.1.

Les outils auxiliaires et leurs reçus sont créés uniquement dans le dossier temporaire de preuves, hors dépôt. L'inventaire machine est `completion/file-inventory.json`.
