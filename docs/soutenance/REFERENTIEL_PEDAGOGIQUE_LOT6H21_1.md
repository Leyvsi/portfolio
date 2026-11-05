# Référentiel pédagogique — lot 6H.21.1

4 novembre 2026, Europe/Paris. Branche `feature/frontend-api-integration`.

Ce référentiel décrit les sources lues statiquement. Il ne modifie ni les sources, ni les quatre fiches, ni les liens vers le README. La refonte approfondie 6H.19.3 reste un préalable à leur actualisation. Aucune copie commentée n’est créée ici.

La répartition des rôles provient des consignes de l’équipe ; elle ne constitue pas une attribution de chaque ligne ou fichier à une personne. Les effets décrits ci-dessous sont ceux d’un futur appel de la fonction, pas des opérations exécutées pour produire ce document.

[Inventaire structuré](INVENTAIRE_PEDAGOGIQUE_LOT6H21_1.json) · [Conventions des futures copies](CONVENTIONS_COPIES_PEDAGOGIQUES_LOT6H21_1.md)

## Périmètre et responsabilités

| Groupe | Modules | Attendu à l’oral |
|---|---:|---|
| BDD principalement Mahamadou | 9 | Dix modèles, treize FK, unicités, ORM, métadonnées et sept migrations. |
| Intégration partagée | 4 | Configuration et sélection du moteur, WSGI, modes mémoire/persistant, transactions et confinement. |
| API partagée avec Sylvie | 14 | Requêtes, permissions, validations, sérialisation et effets transactionnels. |

Le noyau BDD/intégration compte 13 fichiers, 3 172 lignes physiques, 118 définitions de fonctions ou méthodes et 22 lambda. Avec les vues partagées : 27 modules Python, 20 classes, 189 définitions et 23 lambda, soit 212 entrées de fonctions. Les fonctions imbriquées et propriétés sont comptées ; les méthodes générées par dataclass et celles héritées ne sont pas inventées comme lignes sources.

Ces nombres décrivent un inventaire de code, pas un résultat de tests applicatifs. Les fonctions JavaScript sont hors de cette indexation détaillée Python ; leurs huit modules principaux sont repérés parmi les références de lecture collective.

## Conservation des fiches

| Fiche | Identifiants | Total | Vérification |
|---|---|---:|---|
| Mahamadou | MAH-01 à MAH-18 | 18 | Question et réponse courte identiques à HEAD. |
| Mélissa | MEL-01 à MEL-18 | 18 | Question et réponse courte identiques à HEAD. |
| Sylvie | SYL-01 à SYL-18 | 18 | Question et réponse courte identiques à HEAD. |
| Commune | COM-01 à COM-22 | 22 | Question et réponse courte identiques à HEAD. |

Les 76 identifiants sont complets, sans doublon ni trou. Les empreintes des quatre fichiers et des paires question/réponse figurent dans le JSON. Cette conservation ne valide pas les affirmations anciennes comme état courant. Les actualisations des réponses et la réparation des liens appartiennent à d’autres lots ; aucun lien existant n’est changé ici.

## Lecture commune de l’architecture

Mahamadou explique les modèles, les contraintes, les métadonnées, les requêtes et la persistance. Sylvie explique l’API, les permissions et les contrôles serveur ; les transactions se révisent ensemble. Mélissa explique les pages, le DOM et les contrôleurs navigateur. Tous doivent relier une action à la chaîne navigateur → WSGI/Flask → permissions/CSRF → requête SQLAlchemy → transaction → JSON → DOM.

Les fichiers PNG résident sur disque. Le navigateur reçoit une ressource HTTP ; la base conserve éventuellement une référence, pas les octets de ces fichiers. Les quatre modes doivent rester distincts : kit SQLite mémoire, démonstration persistante, lanceur général configuré et processus de validation isolé.

Un archivage conserve les données ; un bannissement restreint les accès ; une purge éditoriale supprime un graphe déterminé. Aucun de ces gestes ne prouve un effacement complet des données d’une personne ou une conformité RGPD définitive.

## Inventaire des modules

| ID | Source | Responsabilité | Classes | Entrées de fonctions |
|---|---|---|---:|---:|
| MAH-M001 | [backend/models.py](../../backend/models.py) | BDD — Mahamadou | 10 | 12 |
| MAH-M002 | [migrations/env.py](../../migrations/env.py) | BDD — Mahamadou | 0 | 6 |
| MAH-M003 | [migrations/versions/3111f5767fc6_ajoute_les_regles_on_delete.py](../../migrations/versions/3111f5767fc6_ajoute_les_regles_on_delete.py) | BDD — Mahamadou | 0 | 2 |
| MAH-M004 | [migrations/versions/82deda84bc35_remove_legacy_comment_reports_counter.py](../../migrations/versions/82deda84bc35_remove_legacy_comment_reports_counter.py) | BDD — Mahamadou | 0 | 2 |
| MAH-M005 | [migrations/versions/921687c1bd7c_baseline_schema.py](../../migrations/versions/921687c1bd7c_baseline_schema.py) | BDD — Mahamadou | 0 | 2 |
| MAH-M006 | [migrations/versions/a590c8aac613_add_reports_bans_and_cold_case_updates.py](../../migrations/versions/a590c8aac613_add_reports_bans_and_cold_case_updates.py) | BDD — Mahamadou | 0 | 2 |
| MAH-M007 | [migrations/versions/c6c100000001_add_story_archive_date.py](../../migrations/versions/c6c100000001_add_story_archive_date.py) | BDD — Mahamadou | 0 | 2 |
| MAH-M008 | [migrations/versions/c6c200000001_comment_reports_and_story_revision.py](../../migrations/versions/c6c200000001_comment_reports_and_story_revision.py) | BDD — Mahamadou | 0 | 3 |
| MAH-M009 | [migrations/versions/c6g200000001_add_comment_likes.py](../../migrations/versions/c6g200000001_add_comment_likes.py) | BDD — Mahamadou | 0 | 3 |
| MAH-M010 | [backend/index.py](../../backend/index.py) | Intégration — partagée | 0 | 9 |
| MAH-M011 | [run_local.py](../../run_local.py) | Intégration — partagée | 0 | 5 |
| MAH-M012 | [tools/demo_persistante.py](../../tools/demo_persistante.py) | Intégration — partagée | 5 | 42 |
| MAH-M013 | [tools/recette_lot6g4.py](../../tools/recette_lot6g4.py) | Intégration — partagée | 4 | 50 |
| MAH-M014 | [backend/api/v1/views/__init__.py](../../backend/api/v1/views/__init__.py) | API — partagée avec Sylvie | 0 | 0 |
| MAH-M015 | [backend/api/v1/views/admin_stories.py](../../backend/api/v1/views/admin_stories.py) | API — partagée avec Sylvie | 0 | 12 |
| MAH-M016 | [backend/api/v1/views/admin_users_support.py](../../backend/api/v1/views/admin_users_support.py) | API — partagée avec Sylvie | 0 | 2 |
| MAH-M017 | [backend/api/v1/views/comments.py](../../backend/api/v1/views/comments.py) | API — partagée avec Sylvie | 0 | 5 |
| MAH-M018 | [backend/api/v1/views/histoires.py](../../backend/api/v1/views/histoires.py) | API — partagée avec Sylvie | 0 | 4 |
| MAH-M019 | [backend/api/v1/views/index.py](../../backend/api/v1/views/index.py) | API — partagée avec Sylvie | 0 | 7 |
| MAH-M020 | [backend/api/v1/views/likes.py](../../backend/api/v1/views/likes.py) | API — partagée avec Sylvie | 0 | 6 |
| MAH-M021 | [backend/api/v1/views/permissions.py](../../backend/api/v1/views/permissions.py) | API — partagée avec Sylvie | 0 | 3 |
| MAH-M022 | [backend/api/v1/views/proposals.py](../../backend/api/v1/views/proposals.py) | API — partagée avec Sylvie | 0 | 3 |
| MAH-M023 | [backend/api/v1/views/story_deletion_support.py](../../backend/api/v1/views/story_deletion_support.py) | API — partagée avec Sylvie | 1 | 17 |
| MAH-M024 | [backend/api/v1/views/story_visibility.py](../../backend/api/v1/views/story_visibility.py) | API — partagée avec Sylvie | 0 | 1 |
| MAH-M025 | [backend/api/v1/views/theories.py](../../backend/api/v1/views/theories.py) | API — partagée avec Sylvie | 0 | 4 |
| MAH-M026 | [backend/api/v1/views/users.py](../../backend/api/v1/views/users.py) | API — partagée avec Sylvie | 0 | 3 |
| MAH-M027 | [backend/api/v1/views/write_support.py](../../backend/api/v1/views/write_support.py) | API — partagée avec Sylvie | 0 | 5 |

## Catalogue expliqué

Les paramètres ci-dessous décrivent les entrées sans reproduire de valeur privée. Une annotation absente n’est pas remplacée par un type supposé. Les retours et effets sont expliqués par lecture du code ; aucune route, migration, commande ou connexion n’a été exécutée. Les emplacements correspondent aux empreintes figées dans le JSON.

### MAH-M001 — `backend/models.py`

Décrire les dix modèles et leurs contraintes sans ouvrir de base.

- **MAH-C001 — `User`**, lignes 18–63 : Compte, unicités, hachage et états de permissions ; le JSON prévu exclut le hachage.
- **MAH-C002 — `Category`**, lignes 68–77 : Catégorie de classement, nom unique et relation aux dossiers.
- **MAH-C003 — `Story`**, lignes 83–210 : Dossier, slug, auteur et catégorie, archivage et révision de gestion ; enfants ORM et référence d’image.
- **MAH-C004 — `Theory`**, lignes 215–275 : Analyse rattachée à un dossier ; auteur nullable et compteur historique de likes.
- **MAH-C005 — `Comment`**, lignes 281–371 : Commentaire, copie du pseudonyme, auteur nullable et relations de modération et de likes.
- **MAH-C006 — `Vote`**, lignes 376–430 : Lien unique entre un compte et un dossier pour son like personnel.
- **MAH-C007 — `CommentLike`**, lignes 433–450 : Lien unique entre un compte et un commentaire, avec cascades SQL et relations ORM.
- **MAH-C008 — `Proposal`**, lignes 455–507 : Proposition liée au compte, statut pending et dates ; aucune transformation automatique en Story.
- **MAH-C009 — `Report`**, lignes 512–581 : Signalement d’un commentaire par FK entière ; propriétés de compatibilité type et target_id.
- **MAH-C010 — `ColdCaseUpdate`**, lignes 586–633 : Mise à jour rattachée à un dossier ; la FK ne vérifie pas sa catégorie métier.


#### MAH-F0001 — `User.set_password`

**Rôle :** Préparer le hachage du mot de passe du compte.

**Repère :** [backend/models.py:43](../../backend/models.py#L43) ; methode. Signature : `set_password(self, password)`.

**Paramètres :**

- `self` (positionnel_ou_nomme) : Instance sur laquelle la méthode ou la propriété travaille.
- `password` (positionnel_ou_nomme) : Saisie du mot de passe, réservée à la mémoire et jamais aux journaux.

**Fonctionnement :**

- Appeler generate_password_hash sur la saisie
- affecter le résultat à password_hash sans valider de transaction.

**Retour :** None.

**Effets :** Modifie un attribut de l’objet User ; aucun commit dans cette méthode.

**Numérotation prévue :** DÉBUT `MAH-F0001:L0001` à la ligne source 43 ; FIN `MAH-F0001:L0003` à la ligne 45. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0002 — `User.check_password`

**Rôle :** Vérifier une saisie sans déchiffrer le hachage.

**Repère :** [backend/models.py:48](../../backend/models.py#L48) ; methode. Signature : `check_password(self, password)`.

**Paramètres :**

- `self` (positionnel_ou_nomme) : Instance sur laquelle la méthode ou la propriété travaille.
- `password` (positionnel_ou_nomme) : Saisie du mot de passe, réservée à la mémoire et jamais aux journaux.

**Fonctionnement :**

- Transmettre password_hash et la saisie à check_password_hash
- renvoyer le verdict de Werkzeug.

**Retour :** Booléen.

**Effets :** Lit le hachage en mémoire ; ne pas journaliser les paramètres.

**Numérotation prévue :** DÉBUT `MAH-F0002:L0001` à la ligne source 48 ; FIN `MAH-F0002:L0003` à la ligne 50. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0003 — `User.to_dict`

**Rôle :** Sérialiser les champs prévus du modèle User.

**Repère :** [backend/models.py:53](../../backend/models.py#L53) ; methode. Signature : `to_dict(self)`.

**Paramètres :**

- `self` (positionnel_ou_nomme) : Instance sur laquelle la méthode ou la propriété travaille.

**Fonctionnement :**

- Lire les attributs sélectionnés dans le dictionnaire de la méthode.
- Convertir les dates présentes par isoformat ; conserver les références ou propriétés prévues.
- Renvoyer le dictionnaire ; User.to_dict exclut expressément password_hash.

**Retour :** Dictionnaire JSON sérialisable du modèle, selon les clés du code source.

**Effets :** Lecture d’attributs ORM ; aucun add, delete ou commit dans la méthode. ; Une sérialisation ne constitue pas une anonymisation ou une autorisation de diffusion.

**Numérotation prévue :** DÉBUT `MAH-F0003:L0001` à la ligne source 53 ; FIN `MAH-F0003:L0011` à la ligne 63. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0004 — `Story.<lambda>#01`

**Rôle :** Produire une révision aléatoire au moment du défaut ORM.

**Repère :** [backend/models.py:100](../../backend/models.py#L100) ; lambda. Signature : `lambda `.

**Paramètres explicites :** aucun. La fonction peut utiliser son contexte Flask, des variables du module ou une fermeture ; ses effets et le déroulement le précisent.

**Fonctionnement :**

- Appeler uuid4 lorsque SQLAlchemy évalue ce défaut.
- Renvoyer sa représentation hexadécimale.

**Retour :** Chaîne hexadécimale de révision.

**Effets :** Génération aléatoire ; pas de commit dans le callback.

**Numérotation prévue :** DÉBUT `MAH-F0004:L0001` à la ligne source 100 ; FIN `MAH-F0004:L0001` à la ligne 100. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0005 — `Story.to_dict`

**Rôle :** Sérialiser les champs prévus du modèle Story.

**Repère :** [backend/models.py:192](../../backend/models.py#L192) ; methode. Signature : `to_dict(self)`.

**Paramètres :**

- `self` (positionnel_ou_nomme) : Instance sur laquelle la méthode ou la propriété travaille.

**Fonctionnement :**

- Lire les attributs sélectionnés dans le dictionnaire de la méthode.
- Convertir les dates présentes par isoformat ; conserver les références ou propriétés prévues.
- Renvoyer le dictionnaire ; User.to_dict exclut expressément password_hash.

**Retour :** Dictionnaire JSON sérialisable du modèle, selon les clés du code source.

**Effets :** Lecture d’attributs ORM ; aucun add, delete ou commit dans la méthode. ; Une sérialisation ne constitue pas une anonymisation ou une autorisation de diffusion.

**Numérotation prévue :** DÉBUT `MAH-F0005:L0001` à la ligne source 192 ; FIN `MAH-F0005:L0019` à la ligne 210. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0006 — `Comment.to_dict`

**Rôle :** Sérialiser les champs prévus du modèle Comment.

**Repère :** [backend/models.py:359](../../backend/models.py#L359) ; methode. Signature : `to_dict(self)`.

**Paramètres :**

- `self` (positionnel_ou_nomme) : Instance sur laquelle la méthode ou la propriété travaille.

**Fonctionnement :**

- Lire les attributs sélectionnés dans le dictionnaire de la méthode.
- Convertir les dates présentes par isoformat ; conserver les références ou propriétés prévues.
- Renvoyer le dictionnaire ; User.to_dict exclut expressément password_hash.

**Retour :** Dictionnaire JSON sérialisable du modèle, selon les clés du code source.

**Effets :** Lecture d’attributs ORM ; aucun add, delete ou commit dans la méthode. ; Une sérialisation ne constitue pas une anonymisation ou une autorisation de diffusion.

**Numérotation prévue :** DÉBUT `MAH-F0006:L0001` à la ligne source 359 ; FIN `MAH-F0006:L0013` à la ligne 371. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0007 — `Report.type[lecture]`

**Rôle :** Exposer le type historique du signalement.

**Repère :** [backend/models.py:530](../../backend/models.py#L530) ; propriete_lecture. Signature : `type(self)`.

**Paramètres :**

- `self` (positionnel_ou_nomme) : Instance sur laquelle la méthode ou la propriété travaille.

**Fonctionnement :**

- Renvoyer la valeur constante correspondant au seul type de cible pris en charge.

**Retour :** Chaîne comment.

**Effets :** Aucune colonne type stockée ni écriture SQL.

**Numérotation prévue :** DÉBUT `MAH-F0007:L0001` à la ligne source 529 ; FIN `MAH-F0007:L0003` à la ligne 531. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0008 — `Report.type[ecriture]`

**Rôle :** Refuser les anciens types de signalement non compatibles.

**Repère :** [backend/models.py:534](../../backend/models.py#L534) ; propriete_ecriture. Signature : `type(self, value)`.

**Paramètres :**

- `self` (positionnel_ou_nomme) : Instance sur laquelle la méthode ou la propriété travaille.
- `value` (positionnel_ou_nomme) : Valeur à convertir ou valider selon le contrat de cette fonction.

**Fonctionnement :**

- Comparer la valeur reçue au seul type autorisé
- lever ValueError si elle diffère.

**Retour :** None si la valeur est acceptée.

**Effets :** Validation seulement ; aucune colonne type créée.

**Erreurs explicitement levées dans ce corps :** `ValueError`. Les appels délégués peuvent aussi échouer.

**Numérotation prévue :** DÉBUT `MAH-F0008:L0001` à la ligne source 533 ; FIN `MAH-F0008:L0004` à la ligne 536. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0009 — `Report.target_id[lecture]`

**Rôle :** Présenter l’identifiant cible dans le format JSON historique.

**Repère :** [backend/models.py:539](../../backend/models.py#L539) ; propriete_lecture. Signature : `target_id(self)`.

**Paramètres :**

- `self` (positionnel_ou_nomme) : Instance sur laquelle la méthode ou la propriété travaille.

**Fonctionnement :**

- Lire comment_id
- convertir cet entier en chaîne.

**Retour :** Chaîne représentant comment_id.

**Effets :** Pas de lecture d’une ancienne colonne target_id.

**Numérotation prévue :** DÉBUT `MAH-F0009:L0001` à la ligne source 538 ; FIN `MAH-F0009:L0003` à la ligne 540. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0010 — `Report.target_id[ecriture]`

**Rôle :** Convertir une cible textuelle canonique vers la FK entière.

**Repère :** [backend/models.py:543](../../backend/models.py#L543) ; propriete_ecriture. Signature : `target_id(self, value)`.

**Paramètres :**

- `self` (positionnel_ou_nomme) : Instance sur laquelle la méthode ou la propriété travaille.
- `value` (positionnel_ou_nomme) : Valeur à convertir ou valider selon le contrat de cette fonction.

**Fonctionnement :**

- Exiger une chaîne ASCII décimale sans zéro initial et dans le domaine prévu
- affecter sa conversion entière à comment_id.

**Retour :** None, ou exception ValueError.

**Effets :** Modifie la FK en mémoire ; aucune validation de transaction ici.

**Erreurs explicitement levées dans ce corps :** `ValueError`. Les appels délégués peuvent aussi échouer.

**Numérotation prévue :** DÉBUT `MAH-F0010:L0001` à la ligne source 542 ; FIN `MAH-F0010:L0009` à la ligne 550. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0011 — `Report.to_dict`

**Rôle :** Sérialiser les champs prévus du modèle Report.

**Repère :** [backend/models.py:570](../../backend/models.py#L570) ; methode. Signature : `to_dict(self)`.

**Paramètres :**

- `self` (positionnel_ou_nomme) : Instance sur laquelle la méthode ou la propriété travaille.

**Fonctionnement :**

- Lire les attributs sélectionnés dans le dictionnaire de la méthode.
- Convertir les dates présentes par isoformat ; conserver les références ou propriétés prévues.
- Renvoyer le dictionnaire ; User.to_dict exclut expressément password_hash.

**Retour :** Dictionnaire JSON sérialisable du modèle, selon les clés du code source.

**Effets :** Lecture d’attributs ORM ; aucun add, delete ou commit dans la méthode. ; Une sérialisation ne constitue pas une anonymisation ou une autorisation de diffusion.

**Numérotation prévue :** DÉBUT `MAH-F0011:L0001` à la ligne source 570 ; FIN `MAH-F0011:L0012` à la ligne 581. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0012 — `ColdCaseUpdate.to_dict`

**Rôle :** Sérialiser les champs prévus du modèle ColdCaseUpdate.

**Repère :** [backend/models.py:624](../../backend/models.py#L624) ; methode. Signature : `to_dict(self)`.

**Paramètres :**

- `self` (positionnel_ou_nomme) : Instance sur laquelle la méthode ou la propriété travaille.

**Fonctionnement :**

- Lire les attributs sélectionnés dans le dictionnaire de la méthode.
- Convertir les dates présentes par isoformat ; conserver les références ou propriétés prévues.
- Renvoyer le dictionnaire ; User.to_dict exclut expressément password_hash.

**Retour :** Dictionnaire JSON sérialisable du modèle, selon les clés du code source.

**Effets :** Lecture d’attributs ORM ; aucun add, delete ou commit dans la méthode. ; Une sérialisation ne constitue pas une anonymisation ou une autorisation de diffusion.

**Numérotation prévue :** DÉBUT `MAH-F0012:L0001` à la ligne source 624 ; FIN `MAH-F0012:L0010` à la ligne 633. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

### MAH-M002 — `migrations/env.py`

Relier Alembic au moteur et aux métadonnées Flask-Migrate ; ne pas importer pour documenter.


#### MAH-F0013 — `get_engine`

**Rôle :** Retrouver le moteur enregistré par Flask-Migrate.

**Repère :** [migrations/env.py:20](../../migrations/env.py#L20) ; fonction. Signature : `get_engine()`.

**Paramètres explicites :** aucun. La fonction peut utiliser son contexte Flask, des variables du module ou une fermeture ; ses effets et le déroulement le précisent.

**Fonctionnement :**

- Utiliser current_app
- essayer l’accès compatible ancien
- reprendre l’attribut engine si nécessaire.

**Retour :** Moteur SQLAlchemy.

**Effets :** Nécessite un contexte Flask ; ne pas importer ce module pour l’audit documentaire.

**Numérotation prévue :** DÉBUT `MAH-F0013:L0001` à la ligne source 20 ; FIN `MAH-F0013:L0007` à la ligne 26. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0014 — `get_engine_url`

**Rôle :** Préparer l’URL du moteur pour Alembic.

**Repère :** [migrations/env.py:31](../../migrations/env.py#L31) ; fonction. Signature : `get_engine_url()`.

**Paramètres explicites :** aucun. La fonction peut utiliser son contexte Flask, des variables du module ou une fermeture ; ses effets et le déroulement le précisent.

**Fonctionnement :**

- Récupérer le moteur
- rendre son URL et échapper les pourcentages
- employer le repli prévu si la méthode manque.

**Retour :** Chaîne d’URL pour Alembic.

**Effets :** La chaîne peut contenir des informations privées ; ne pas l’afficher.

**Numérotation prévue :** DÉBUT `MAH-F0014:L0001` à la ligne source 31 ; FIN `MAH-F0014:L0006` à la ligne 36. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0015 — `get_metadata`

**Rôle :** Sélectionner les métadonnées du modèle.

**Repère :** [migrations/env.py:54](../../migrations/env.py#L54) ; fonction. Signature : `get_metadata()`.

**Paramètres explicites :** aucun. La fonction peut utiliser son contexte Flask, des variables du module ou une fermeture ; ses effets et le déroulement le précisent.

**Fonctionnement :**

- Distinguer l’accès metadatas de l’accès metadata
- renvoyer les métadonnées de la liaison attendue.

**Retour :** Objet MetaData.

**Effets :** Lecture des extensions déjà configurées.

**Numérotation prévue :** DÉBUT `MAH-F0015:L0001` à la ligne source 54 ; FIN `MAH-F0015:L0004` à la ligne 57. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0016 — `run_migrations_offline`

**Rôle :** Configurer la production SQL hors connexion Alembic.

**Repère :** [migrations/env.py:62](../../migrations/env.py#L62) ; fonction. Signature : `run_migrations_offline()`.

**Paramètres explicites :** aucun. La fonction peut utiliser son contexte Flask, des variables du module ou une fermeture ; ses effets et le déroulement le précisent.

**Fonctionnement :**

- Fournir URL et métadonnées au contexte
- ouvrir la transaction Alembic
- exécuter les révisions dans ce contexte.

**Retour :** None.

**Effets :** Peut produire des instructions de migration ; le mode hors ligne n’est pas un test applicatif.

**Numérotation prévue :** DÉBUT `MAH-F0016:L0001` à la ligne source 62 ; FIN `MAH-F0016:L0019` à la ligne 80. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0017 — `run_migrations_online`

**Rôle :** Appliquer des migrations avec une connexion cible.

**Repère :** [migrations/env.py:85](../../migrations/env.py#L85) ; fonction. Signature : `run_migrations_online()`.

**Paramètres explicites :** aucun. La fonction peut utiliser son contexte Flask, des variables du module ou une fermeture ; ses effets et le déroulement le précisent.

**Fonctionnement :**

- Préparer les arguments et le callback d’autogénération
- ouvrir une connexion moteur
- configurer le contexte et sa transaction
- exécuter les migrations.

**Retour :** None.

**Effets :** Connexion et éventuels DDL/DML sur la cible ; ne jamais appeler pendant ce lot.

**Numérotation prévue :** DÉBUT `MAH-F0017:L0001` à la ligne source 85 ; FIN `MAH-F0017:L0034` à la ligne 118. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0018 — `run_migrations_online.process_revision_directives`

**Rôle :** Éviter une révision autogénérée vide.

**Repère :** [migrations/env.py:97](../../migrations/env.py#L97) ; fonction_imbriquee. Signature : `process_revision_directives(context, revision, directives)`.

**Paramètres :**

- `context` (positionnel_ou_nomme) : Contexte Alembic transmis au callback d’autogénération.
- `revision` (positionnel_ou_nomme) : Révision Alembic transmise au callback d’autogénération.
- `directives` (positionnel_ou_nomme) : Liste mutable des révisions proposées par Alembic.

**Fonctionnement :**

- Détecter le mode autogenerate
- examiner les opérations proposées
- vider directives si la révision ne change rien.

**Retour :** None.

**Effets :** Modifie la liste directives ; n’insère pas de données de démonstration.

**Numérotation prévue :** DÉBUT `MAH-F0018:L0001` à la ligne source 97 ; FIN `MAH-F0018:L0006` à la ligne 102. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

### MAH-M003 — `migrations/versions/3111f5767fc6_ajoute_les_regles_on_delete.py`

Ajouter les règles de suppression des clés étrangères.


#### MAH-F0019 — `upgrade`

**Rôle :** Ajouter les règles de suppression des clés étrangères.

**Repère :** [migrations/versions/3111f5767fc6_ajoute_les_regles_on_delete.py:21](../../migrations/versions/3111f5767fc6_ajoute_les_regles_on_delete.py#L21) ; fonction. Signature : `upgrade()`.

**Paramètres explicites :** aucun. La fonction peut utiliser son contexte Flask, des variables du module ou une fermeture ; ses effets et le déroulement le précisent.

**Fonctionnement :**

- Recréer les contraintes visées avec CASCADE ou SET NULL selon les relations.

**Retour :** None.

**Effets :** Peut modifier le schéma et les données de la connexion Alembic ; aucune exécution autorisée ici.

**Numérotation prévue :** DÉBUT `MAH-F0019:L0001` à la ligne source 21 ; FIN `MAH-F0019:L0105` à la ligne 125. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0020 — `downgrade`

**Rôle :** Revenir à la révision précédente.

**Repère :** [migrations/versions/3111f5767fc6_ajoute_les_regles_on_delete.py:130](../../migrations/versions/3111f5767fc6_ajoute_les_regles_on_delete.py#L130) ; fonction. Signature : `downgrade()`.

**Paramètres explicites :** aucun. La fonction peut utiliser son contexte Flask, des variables du module ou une fermeture ; ses effets et le déroulement le précisent.

**Fonctionnement :**

- Revenir aux contraintes précédentes
- les données déjà supprimées ne sont pas recréées.

**Retour :** None.

**Effets :** Retour de schéma distinct d’une restauration de sauvegarde ; aucune exécution autorisée ici.

**Numérotation prévue :** DÉBUT `MAH-F0020:L0001` à la ligne source 130 ; FIN `MAH-F0020:L0092` à la ligne 221. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

### MAH-M004 — `migrations/versions/82deda84bc35_remove_legacy_comment_reports_counter.py`

Retirer le compteur redondant de signalements des commentaires.


#### MAH-F0021 — `upgrade`

**Rôle :** Retirer le compteur redondant de signalements des commentaires.

**Repère :** [migrations/versions/82deda84bc35_remove_legacy_comment_reports_counter.py:21](../../migrations/versions/82deda84bc35_remove_legacy_comment_reports_counter.py#L21) ; fonction. Signature : `upgrade()`.

**Paramètres explicites :** aucun. La fonction peut utiliser son contexte Flask, des variables du module ou une fermeture ; ses effets et le déroulement le précisent.

**Fonctionnement :**

- Supprimer comments.reports avec batch_alter_table.

**Retour :** None.

**Effets :** Peut modifier le schéma et les données de la connexion Alembic ; aucune exécution autorisée ici.

**Numérotation prévue :** DÉBUT `MAH-F0021:L0001` à la ligne source 21 ; FIN `MAH-F0021:L0003` à la ligne 23. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0022 — `downgrade`

**Rôle :** Revenir à la révision précédente.

**Repère :** [migrations/versions/82deda84bc35_remove_legacy_comment_reports_counter.py:28](../../migrations/versions/82deda84bc35_remove_legacy_comment_reports_counter.py#L28) ; fonction. Signature : `downgrade()`.

**Paramètres explicites :** aucun. La fonction peut utiliser son contexte Flask, des variables du module ou une fermeture ; ses effets et le déroulement le précisent.

**Fonctionnement :**

- Recréer et recalculer le compteur selon les lignes encore présentes
- ne pas promettre de restaurer les anciennes valeurs exactes.

**Retour :** None.

**Effets :** Retour de schéma distinct d’une restauration de sauvegarde ; aucune exécution autorisée ici.

**Numérotation prévue :** DÉBUT `MAH-F0022:L0001` à la ligne source 28 ; FIN `MAH-F0022:L0016` à la ligne 43. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

### MAH-M005 — `migrations/versions/921687c1bd7c_baseline_schema.py`

Créer le schéma initial de sept tables.


#### MAH-F0023 — `upgrade`

**Rôle :** Créer le schéma initial de sept tables.

**Repère :** [migrations/versions/921687c1bd7c_baseline_schema.py:22](../../migrations/versions/921687c1bd7c_baseline_schema.py#L22) ; fonction. Signature : `upgrade()`.

**Paramètres explicites :** aucun. La fonction peut utiliser son contexte Flask, des variables du module ou une fermeture ; ses effets et le déroulement le précisent.

**Fonctionnement :**

- Déclarer les tables et colonnes de la révision initiale, avec les contraintes prévues.

**Retour :** None.

**Effets :** Peut modifier le schéma et les données de la connexion Alembic ; aucune exécution autorisée ici.

**Numérotation prévue :** DÉBUT `MAH-F0023:L0001` à la ligne source 22 ; FIN `MAH-F0023:L0149` à la ligne 170. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0024 — `downgrade`

**Rôle :** Revenir à la révision précédente.

**Repère :** [migrations/versions/921687c1bd7c_baseline_schema.py:175](../../migrations/versions/921687c1bd7c_baseline_schema.py#L175) ; fonction. Signature : `downgrade()`.

**Paramètres explicites :** aucun. La fonction peut utiliser son contexte Flask, des variables du module ou une fermeture ; ses effets et le déroulement le précisent.

**Fonctionnement :**

- Supprimer les tables de ce schéma initial dans l’ordre prévu.

**Retour :** None.

**Effets :** Retour de schéma distinct d’une restauration de sauvegarde ; aucune exécution autorisée ici.

**Numérotation prévue :** DÉBUT `MAH-F0024:L0001` à la ligne source 175 ; FIN `MAH-F0024:L0008` à la ligne 182. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

### MAH-M006 — `migrations/versions/a590c8aac613_add_reports_bans_and_cold_case_updates.py`

Ajouter modération, bannissement et mises à jour au schéma historique.


#### MAH-F0025 — `upgrade`

**Rôle :** Ajouter modération, bannissement et mises à jour au schéma historique.

**Repère :** [migrations/versions/a590c8aac613_add_reports_bans_and_cold_case_updates.py:21](../../migrations/versions/a590c8aac613_add_reports_bans_and_cold_case_updates.py#L21) ; fonction. Signature : `upgrade()`.

**Paramètres explicites :** aucun. La fonction peut utiliser son contexte Flask, des variables du module ou une fermeture ; ses effets et le déroulement le précisent.

**Fonctionnement :**

- Créer les tables historiques de signalements et de mises à jour et ajouter is_banned.

**Retour :** None.

**Effets :** Peut modifier le schéma et les données de la connexion Alembic ; aucune exécution autorisée ici.

**Numérotation prévue :** DÉBUT `MAH-F0025:L0001` à la ligne source 21 ; FIN `MAH-F0025:L0042` à la ligne 62. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0026 — `downgrade`

**Rôle :** Revenir à la révision précédente.

**Repère :** [migrations/versions/a590c8aac613_add_reports_bans_and_cold_case_updates.py:67](../../migrations/versions/a590c8aac613_add_reports_bans_and_cold_case_updates.py#L67) ; fonction. Signature : `downgrade()`.

**Paramètres explicites :** aucun. La fonction peut utiliser son contexte Flask, des variables du module ou une fermeture ; ses effets et le déroulement le précisent.

**Fonctionnement :**

- Retirer les éléments ajoutés par cette révision
- toute donnée correspondante peut être perdue.

**Retour :** None.

**Effets :** Retour de schéma distinct d’une restauration de sauvegarde ; aucune exécution autorisée ici.

**Numérotation prévue :** DÉBUT `MAH-F0026:L0001` à la ligne source 67 ; FIN `MAH-F0026:L0008` à la ligne 74. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

### MAH-M007 — `migrations/versions/c6c100000001_add_story_archive_date.py`

Ajouter l’archivage réversible des dossiers.


#### MAH-F0027 — `upgrade`

**Rôle :** Ajouter l’archivage réversible des dossiers.

**Repère :** [migrations/versions/c6c100000001_add_story_archive_date.py:16](../../migrations/versions/c6c100000001_add_story_archive_date.py#L16) ; fonction. Signature : `upgrade()`.

**Paramètres explicites :** aucun. La fonction peut utiliser son contexte Flask, des variables du module ou une fermeture ; ses effets et le déroulement le précisent.

**Fonctionnement :**

- Ajouter archived_at nullable
- NULL représente un dossier actif.

**Retour :** None.

**Effets :** Peut modifier le schéma et les données de la connexion Alembic ; aucune exécution autorisée ici.

**Numérotation prévue :** DÉBUT `MAH-F0027:L0001` à la ligne source 16 ; FIN `MAH-F0027:L0004` à la ligne 19. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0028 — `downgrade`

**Rôle :** Revenir à la révision précédente.

**Repère :** [migrations/versions/c6c100000001_add_story_archive_date.py:22](../../migrations/versions/c6c100000001_add_story_archive_date.py#L22) ; fonction. Signature : `downgrade()`.

**Paramètres explicites :** aucun. La fonction peut utiliser son contexte Flask, des variables du module ou une fermeture ; ses effets et le déroulement le précisent.

**Fonctionnement :**

- Supprimer archived_at
- l’information d’archivage est alors perdue.

**Retour :** None.

**Effets :** Retour de schéma distinct d’une restauration de sauvegarde ; aucune exécution autorisée ici.

**Numérotation prévue :** DÉBUT `MAH-F0028:L0001` à la ligne source 22 ; FIN `MAH-F0028:L0004` à la ligne 25. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

### MAH-M008 — `migrations/versions/c6c200000001_comment_reports_and_story_revision.py`

Rattacher les signalements aux commentaires et ajouter une révision de dossier.


#### MAH-F0029 — `inspect_legacy`

**Rôle :** Vérifier les anciennes cibles de signalements avant toute transformation.

**Repère :** [migrations/versions/c6c200000001_comment_reports_and_story_revision.py:19](../../migrations/versions/c6c200000001_comment_reports_and_story_revision.py#L19) ; fonction. Signature : `inspect_legacy(bind)`.

**Paramètres :**

- `bind` (positionnel_ou_nomme) : Connexion Alembic utilisée pour inspecter le schéma avant transformation.

**Fonctionnement :**

- Inspecter le schéma et les types
- rechercher les cibles non conformes ou orphelines
- refuser une reprise ambiguë.

**Retour :** Type SQL utile à la création de la nouvelle référence, selon le schéma inspecté.

**Effets :** Lectures de schéma et données ; exception si la reprise ne peut pas préserver les références.

**Erreurs explicitement levées dans ce corps :** `RuntimeError`. Les appels délégués peuvent aussi échouer.

**Numérotation prévue :** DÉBUT `MAH-F0029:L0001` à la ligne source 19 ; FIN `MAH-F0029:L0021` à la ligne 39. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0030 — `upgrade`

**Rôle :** Rattacher les signalements aux commentaires et ajouter une révision de dossier.

**Repère :** [migrations/versions/c6c200000001_comment_reports_and_story_revision.py:42](../../migrations/versions/c6c200000001_comment_reports_and_story_revision.py#L42) ; fonction. Signature : `upgrade()`.

**Paramètres explicites :** aucun. La fonction peut utiliser son contexte Flask, des variables du module ou une fermeture ; ses effets et le déroulement le précisent.

**Fonctionnement :**

- Inspecter les anciennes cibles avant DDL
- créer la FK entière et migrer les références compatibles
- ajouter les révisions de gestion.

**Retour :** None.

**Effets :** Peut modifier le schéma et les données de la connexion Alembic ; aucune exécution autorisée ici.

**Numérotation prévue :** DÉBUT `MAH-F0030:L0001` à la ligne source 42 ; FIN `MAH-F0030:L0021` à la ligne 62. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0031 — `downgrade`

**Rôle :** Revenir à la révision précédente.

**Repère :** [migrations/versions/c6c200000001_comment_reports_and_story_revision.py:65](../../migrations/versions/c6c200000001_comment_reports_and_story_revision.py#L65) ; fonction. Signature : `downgrade()`.

**Paramètres explicites :** aucun. La fonction peut utiliser son contexte Flask, des variables du module ou une fermeture ; ses effets et le déroulement le précisent.

**Fonctionnement :**

- Rétablir la représentation historique prévue sans recréer de contenu purgé.

**Retour :** None.

**Effets :** Retour de schéma distinct d’une restauration de sauvegarde ; aucune exécution autorisée ici.

**Numérotation prévue :** DÉBUT `MAH-F0031:L0001` à la ligne source 65 ; FIN `MAH-F0031:L0016` à la ligne 80. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

### MAH-M009 — `migrations/versions/c6g200000001_add_comment_likes.py`

Créer les likes individuels de commentaires.


#### MAH-F0032 — `inspect_legacy`

**Rôle :** Vérifier que les likes historiques peuvent être repris sans attribution inventée.

**Repère :** [migrations/versions/c6g200000001_add_comment_likes.py:15](../../migrations/versions/c6g200000001_add_comment_likes.py#L15) ; fonction. Signature : `inspect_legacy(bind)`.

**Paramètres :**

- `bind` (positionnel_ou_nomme) : Connexion Alembic utilisée pour inspecter le schéma avant transformation.

**Fonctionnement :**

- Lire les types de clés et l’état des anciens compteurs
- refuser les valeurs incompatibles
- transmettre les types nécessaires.

**Retour :** Couple de types SQL du commentaire et du compte.

**Effets :** Lectures de schéma et compteurs ; aucune remise à zéro silencieuse.

**Erreurs explicitement levées dans ce corps :** `RuntimeError`. Les appels délégués peuvent aussi échouer.

**Numérotation prévue :** DÉBUT `MAH-F0032:L0001` à la ligne source 15 ; FIN `MAH-F0032:L0025` à la ligne 39. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0033 — `upgrade`

**Rôle :** Créer les likes individuels de commentaires.

**Repère :** [migrations/versions/c6g200000001_add_comment_likes.py:42](../../migrations/versions/c6g200000001_add_comment_likes.py#L42) ; fonction. Signature : `upgrade()`.

**Paramètres explicites :** aucun. La fonction peut utiliser son contexte Flask, des variables du module ou une fermeture ; ses effets et le déroulement le précisent.

**Fonctionnement :**

- Refuser les anciens compteurs incompatibles avant DDL
- créer la table, ses FK et son unicité composite.

**Retour :** None.

**Effets :** Peut modifier le schéma et les données de la connexion Alembic ; aucune exécution autorisée ici.

**Numérotation prévue :** DÉBUT `MAH-F0033:L0001` à la ligne source 42 ; FIN `MAH-F0033:L0014` à la ligne 55. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0034 — `downgrade`

**Rôle :** Revenir à la révision précédente.

**Repère :** [migrations/versions/c6g200000001_add_comment_likes.py:59](../../migrations/versions/c6g200000001_add_comment_likes.py#L59) ; fonction. Signature : `downgrade()`.

**Paramètres explicites :** aucun. La fonction peut utiliser son contexte Flask, des variables du module ou une fermeture ; ses effets et le déroulement le précisent.

**Fonctionnement :**

- Refuser un retrait qui perdrait les likes existants
- retirer la table et l’index seulement si les conditions sont réunies.

**Retour :** None.

**Effets :** Retour de schéma distinct d’une restauration de sauvegarde ; aucune exécution autorisée ici.

**Erreurs explicitement levées dans ce corps :** `RuntimeError`. Les appels délégués peuvent aussi échouer.

**Numérotation prévue :** DÉBUT `MAH-F0034:L0001` à la ligne source 59 ; FIN `MAH-F0034:L0006` à la ligne 64. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

### MAH-M010 — `backend/index.py`

Configurer Flask et le moteur ; authentification, sessions et CSRF partagés avec Sylvie.


#### MAH-F0035 — `env_to_bool`

**Rôle :** Lire une option booléenne de configuration.

**Repère :** [backend/index.py:33](../../backend/index.py#L33) ; fonction. Signature : `env_to_bool(name, default=False)`.

**Paramètres :**

- `name` (positionnel_ou_nomme) : Nom de variable de configuration ou repère du compte fictif, selon la fonction.
- `default` (positionnel_ou_nomme ; défaut source : `False`) : Valeur de repli si la configuration demandée est absente.

**Fonctionnement :**

- Chercher la variable d’environnement
- utiliser default si elle manque
- comparer la chaîne normalisée aux valeurs vraies prévues.

**Retour :** Booléen.

**Effets :** Lit l’environnement du processus, sans le modifier.

**Numérotation prévue :** DÉBUT `MAH-F0035:L0001` à la ligne source 33 ; FIN `MAH-F0035:L0013` à la ligne 45. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0036 — `get_csrf_token`

**Rôle :** Obtenir le jeton CSRF associé à la session.

**Repère :** [backend/index.py:156](../../backend/index.py#L156) ; fonction. Signature : `get_csrf_token()`.

**Paramètres explicites :** aucun. La fonction peut utiliser son contexte Flask, des variables du module ou une fermeture ; ses effets et le déroulement le précisent.

**Fonctionnement :**

- Lire le jeton existant
- en générer un aléatoire s’il manque
- le conserver dans session.

**Retour :** Chaîne contenant le jeton de la session.

**Effets :** Peut modifier la session et faire émettre un cookie ; valeur à garder privée.

**Numérotation prévue :** DÉBUT `MAH-F0036:L0001` à la ligne source 156 ; FIN `MAH-F0036:L0009` à la ligne 164. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0037 — `protect_session_requests_from_csrf`

**Rôle :** Contrôler les écritures utilisant une session authentifiée.

**Repère :** [backend/index.py:171](../../backend/index.py#L171) ; fonction. Signature : `protect_session_requests_from_csrf()`.

**Paramètres explicites :** aucun. La fonction peut utiliser son contexte Flask, des variables du module ou une fermeture ; ses effets et le déroulement le précisent.

**Fonctionnement :**

- Laisser passer les méthodes sûres, login et les anonymes
- vérifier deux jetons ASCII non vides
- les comparer avec compare_digest.

**Retour :** None pour poursuivre, ou réponse JSON et statut 403.

**Effets :** Peut interrompre la requête avant la vue ; ne remplace pas les permissions métier.

**Numérotation prévue :** DÉBUT `MAH-F0037:L0001` à la ligne source 167 ; FIN `MAH-F0037:L0047` à la ligne 213. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0038 — `not_found`

**Rôle :** Produire la réponse de ressource absente.

**Repère :** [backend/index.py:217](../../backend/index.py#L217) ; fonction. Signature : `not_found(error)`.

**Paramètres :**

- `error` (positionnel_ou_nomme) : Erreur transmise par Flask ou SQLAlchemy, à traiter sans exposer ses détails privés.

**Fonctionnement :**

- Construire le message JSON prévu
- associer le statut HTTP 404.

**Retour :** Couple réponse JSON, 404.

**Effets :** Aucune modification de données.

**Numérotation prévue :** DÉBUT `MAH-F0038:L0001` à la ligne source 216 ; FIN `MAH-F0038:L0006` à la ligne 221. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0039 — `handle_api_http_error`

**Rôle :** Uniformiser les erreurs HTTP de l’API.

**Repère :** [backend/index.py:227](../../backend/index.py#L227) ; fonction. Signature : `handle_api_http_error(error)`.

**Paramètres :**

- `error` (positionnel_ou_nomme) : Erreur transmise par Flask ou SQLAlchemy, à traiter sans exposer ses détails privés.

**Fonctionnement :**

- Conserver les erreurs hors API
- reprendre la réponse du framework
- remplacer le corps par le JSON prévu en conservant statut et en-têtes.

**Retour :** Exception HTTP hors API ou objet Response adapté.

**Effets :** Modifie la réponse, sans confirmer une opération SQL.

**Numérotation prévue :** DÉBUT `MAH-F0039:L0001` à la ligne source 224 ; FIN `MAH-F0039:L0015` à la ligne 238. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0040 — `get_stats`

**Rôle :** Retourner trois agrégats publics.

**Repère :** [backend/index.py:245](../../backend/index.py#L245) ; fonction. Signature : `get_stats()`.

**Paramètres explicites :** aucun. La fonction peut utiliser son contexte Flask, des variables du module ou une fermeture ; ses effets et le déroulement le précisent.

**Fonctionnement :**

- Compter les comptes, commentaires et signalements
- préparer la réponse
- effectuer rollback en cas d’erreur SQL.

**Retour :** Réponse JSON et statut 200 ou 500.

**Effets :** Lectures SQL ; rollback possible ; ces trois nombres ne sont pas les sept indicateurs complets.

**Numérotation prévue :** DÉBUT `MAH-F0040:L0001` à la ligne source 242 ; FIN `MAH-F0040:L0021` à la ligne 262. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0041 — `login_user`

**Rôle :** Authentifier un compte et renouveler sa session.

**Repère :** [backend/index.py:269](../../backend/index.py#L269) ; fonction. Signature : `login_user()`.

**Paramètres explicites :** aucun. La fonction peut utiliser son contexte Flask, des variables du module ou une fermeture ; ses effets et le déroulement le précisent.

**Fonctionnement :**

- Valider le JSON et les chaînes
- rechercher le compte et vérifier le hachage et le bannissement
- vider l’ancien état et préparer user_id, rôle et CSRF.

**Retour :** Réponse JSON et statut 200, 400, 401 ou 403.

**Effets :** Lecture SQL et modification de session ; aucun mot de passe dans le cookie.

**Numérotation prévue :** DÉBUT `MAH-F0041:L0001` à la ligne source 266 ; FIN `MAH-F0041:L0070` à la ligne 335. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0042 — `get_current_user`

**Rôle :** Renvoyer l’état actuel du compte connecté.

**Repère :** [backend/index.py:342](../../backend/index.py#L342) ; fonction. Signature : `get_current_user()`.

**Paramètres explicites :** aucun. La fonction peut utiliser son contexte Flask, des variables du module ou une fermeture ; ses effets et le déroulement le précisent.

**Fonctionnement :**

- Relire le compte par le helper de permissions
- propager un refus
- obtenir le CSRF et sérialiser les champs prévus.

**Retour :** Réponse JSON et statut 200 ou refus 401/403.

**Effets :** Lecture SQL ; peut renouveler le jeton ou nettoyer une session invalide.

**Numérotation prévue :** DÉBUT `MAH-F0042:L0001` à la ligne source 339 ; FIN `MAH-F0042:L0021` à la ligne 359. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0043 — `logout_user`

**Rôle :** Fermer la session courante du navigateur.

**Repère :** [backend/index.py:366](../../backend/index.py#L366) ; fonction. Signature : `logout_user()`.

**Paramètres explicites :** aucun. La fonction peut utiliser son contexte Flask, des variables du module ou une fermeture ; ses effets et le déroulement le précisent.

**Fonctionnement :**

- Vider session
- renvoyer la confirmation JSON.

**Retour :** Couple réponse JSON, 200.

**Effets :** Émission possible du cookie de suppression ; aucune révocation centrale de toutes ses copies.

**Numérotation prévue :** DÉBUT `MAH-F0043:L0001` à la ligne source 363 ; FIN `MAH-F0043:L0010` à la ligne 372. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

### MAH-M011 — `run_local.py`

Composer les ressources statiques et l’API sur la même origine ; lanceur général distinct du kit.


#### MAH-F0044 — `create_local_app`

**Rôle :** Composer le service du frontend et l’application API.

**Repère :** [run_local.py:17](../../run_local.py#L17) ; fonction. Signature : `create_local_app(api_app, frontend_root=FRONTEND_ROOT)`.

**Paramètres :**

- `api_app` (positionnel_ou_nomme) : Application WSGI de l’API à envelopper ou déléguer.
- `frontend_root` (positionnel_ou_nomme ; défaut source : `FRONTEND_ROOT`) : Répertoire des ressources frontend que le middleware peut distribuer.

**Fonctionnement :**

- Préparer SharedDataMiddleware pour frontend_root
- définir les fermetures de cache et de routage
- renvoyer la fonction WSGI composée.

**Retour :** Fonction WSGI application.

**Effets :** Ne lance pas de serveur et ne choisit pas de base.

**Numérotation prévue :** DÉBUT `MAH-F0044:L0001` à la ligne source 17 ; FIN `MAH-F0044:L0047` à la ligne 63. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0045 — `create_local_app.serve_frontend`

**Rôle :** Distribuer une ressource statique avec contrôle du cache.

**Repère :** [run_local.py:26](../../run_local.py#L26) ; fonction_imbriquee. Signature : `serve_frontend(environ, start_response)`.

**Paramètres :**

- `environ` (positionnel_ou_nomme) : Dictionnaire de la requête WSGI : méthode, chemin et contexte serveur.
- `start_response` (positionnel_ou_nomme) : Callback WSGI recevant le statut et les en-têtes de réponse.

**Fonctionnement :**

- Appeler le middleware statique
- remplacer start_response par la fermeture prevent_storage.

**Retour :** Itérable WSGI d’octets.

**Effets :** Lecture de fichiers publics lors de l’appel ; en-tête no-store.

**Numérotation prévue :** DÉBUT `MAH-F0045:L0001` à la ligne source 26 ; FIN `MAH-F0045:L0008` à la ligne 33. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0046 — `create_local_app.serve_frontend.prevent_storage`

**Rôle :** Empêcher le stockage des réponses statiques.

**Repère :** [run_local.py:27](../../run_local.py#L27) ; fonction_imbriquee. Signature : `prevent_storage(status, headers, exc_info=None)`.

**Paramètres :**

- `status` (positionnel_ou_nomme) : Statut HTTP attendu ou à renvoyer ; forme WSGI textuelle pour prevent_storage.
- `headers` (positionnel_ou_nomme) : Liste des couples d’en-têtes HTTP de la réponse WSGI.
- `exc_info` (positionnel_ou_nomme ; défaut source : `None`) : Informations d’exception optionnelles transmises au callback WSGI.

**Fonctionnement :**

- Retirer Cache-Control existant
- ajouter no-store
- transmettre statut, en-têtes et exc_info au start_response capturé.

**Retour :** Retour du start_response d’origine.

**Effets :** Modifie les en-têtes HTTP seulement.

**Numérotation prévue :** DÉBUT `MAH-F0046:L0001` à la ligne source 27 ; FIN `MAH-F0046:L0005` à la ligne 31. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0047 — `create_local_app.application`

**Rôle :** Aiguiller une requête vers l’API ou le frontend.

**Repère :** [run_local.py:38](../../run_local.py#L38) ; fonction_imbriquee. Signature : `application(environ, start_response)`.

**Paramètres :**

- `environ` (positionnel_ou_nomme) : Dictionnaire de la requête WSGI : méthode, chemin et contexte serveur.
- `start_response` (positionnel_ou_nomme) : Callback WSGI recevant le statut et les en-têtes de réponse.

**Fonctionnement :**

- Transmettre les écritures et chemins API à api_app
- traduire la racine vers index.html
- ne servir que les extensions et emplacements prévus.

**Retour :** Itérable WSGI d’octets de l’application sélectionnée.

**Effets :** Peut lire un fichier public ou appeler Flask ; aucun lancement de processus ici.

**Numérotation prévue :** DÉBUT `MAH-F0047:L0001` à la ligne source 38 ; FIN `MAH-F0047:L0024` à la ligne 61. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0048 — `main`

**Rôle :** Démarrer le lanceur général sur la boucle locale.

**Repère :** [run_local.py:68](../../run_local.py#L68) ; fonction. Signature : `main()`.

**Paramètres explicites :** aucun. La fonction peut utiliser son contexte Flask, des variables du module ou une fermeture ; ses effets et le déroulement le précisent.

**Fonctionnement :**

- Se placer à la racine
- charger dotenv
- importer l’application configurée et composer son WSGI
- lancer Flask sans debug ni reloader.

**Retour :** None après arrêt normal du serveur.

**Effets :** Change le répertoire courant et sys.path ; lit la configuration privée ; ouvre une écoute locale et peut accéder à la base configurée.

**Numérotation prévue :** DÉBUT `MAH-F0048:L0001` à la ligne source 68 ; FIN `MAH-F0048:L0011` à la ligne 78. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

### MAH-M012 — `tools/demo_persistante.py`

Séparer création, contrôle, service, sauvegarde et restauration du jeu SQLite persistant.

- **MAH-C011 — `LocalError`**, lignes 41–42 : Erreur locale à message contrôlé, sans détail d’accès privé.
- **MAH-C012 — `Person`**, lignes 46–49 : Dataclass figée de saisie des comptes ; e-mail et mot de passe exclus de repr.
- **MAH-C013 — `Paths`**, lignes 53–96 : Dataclass figée des chemins privés ; propriétés de composition et validation des destinations.
- **MAH-C014 — `_windows_security.Attributes`**, lignes 137–138 : Structure ctypes d’attributs de sécurité transmise aux API Windows ; aucun modèle SQL.
- **MAH-C015 — `serve.QuietHandler`**, lignes 563–565 : Gestionnaire WSGI spécialisé pour ne pas journaliser les requêtes de démonstration.


#### MAH-F0049 — `Paths.__post_init__`

**Rôle :** Normaliser la racine du jeu local.

**Repère :** [tools/demo_persistante.py:56](../../tools/demo_persistante.py#L56) ; methode. Signature : `__post_init__(self)`.

**Paramètres :**

- `self` (positionnel_ou_nomme) : Instance sur laquelle la méthode ou la propriété travaille.

**Fonctionnement :**

- Résoudre root dans la dataclass figée
- refuser un chemin réseau UNC.

**Retour :** None.

**Effets :** Modifie l’attribut root pendant l’initialisation ; ne crée pas de dossier.

**Erreurs explicitement levées dans ce corps :** `LocalError`. Les appels délégués peuvent aussi échouer.

**Numérotation prévue :** DÉBUT `MAH-F0049:L0001` à la ligne source 56 ; FIN `MAH-F0049:L0004` à la ligne 59. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0050 — `Paths.instance[lecture]`

**Rôle :** Désigner le répertoire instance sous root.

**Repère :** [tools/demo_persistante.py:62](../../tools/demo_persistante.py#L62) ; propriete_lecture. Signature : `instance(self)`.

**Paramètres :**

- `self` (positionnel_ou_nomme) : Instance sur laquelle la méthode ou la propriété travaille.

**Fonctionnement :**

- Composer le chemin à partir de la racine normalisée
- ne pas ouvrir la destination.

**Retour :** Objet Path.

**Effets :** Aucun fichier créé ni aucune valeur privée lue.

**Numérotation prévue :** DÉBUT `MAH-F0050:L0001` à la ligne source 61 ; FIN `MAH-F0050:L0003` à la ligne 63. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0051 — `Paths.data[lecture]`

**Rôle :** Désigner le dossier privé de démonstration sous instance.

**Repère :** [tools/demo_persistante.py:66](../../tools/demo_persistante.py#L66) ; propriete_lecture. Signature : `data(self)`.

**Paramètres :**

- `self` (positionnel_ou_nomme) : Instance sur laquelle la méthode ou la propriété travaille.

**Fonctionnement :**

- Composer le chemin à partir de la racine normalisée
- ne pas ouvrir la destination.

**Retour :** Objet Path.

**Effets :** Aucun fichier créé ni aucune valeur privée lue.

**Numérotation prévue :** DÉBUT `MAH-F0051:L0001` à la ligne source 65 ; FIN `MAH-F0051:L0003` à la ligne 67. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0052 — `Paths.database[lecture]`

**Rôle :** Désigner le fichier SQLite canonique du jeu.

**Repère :** [tools/demo_persistante.py:70](../../tools/demo_persistante.py#L70) ; propriete_lecture. Signature : `database(self)`.

**Paramètres :**

- `self` (positionnel_ou_nomme) : Instance sur laquelle la méthode ou la propriété travaille.

**Fonctionnement :**

- Composer le chemin à partir de la racine normalisée
- ne pas ouvrir la destination.

**Retour :** Objet Path.

**Effets :** Aucun fichier créé ni aucune valeur privée lue.

**Numérotation prévue :** DÉBUT `MAH-F0052:L0001` à la ligne source 69 ; FIN `MAH-F0052:L0003` à la ligne 71. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0053 — `Paths.key[lecture]`

**Rôle :** Désigner le fichier privé de clé de session.

**Repère :** [tools/demo_persistante.py:74](../../tools/demo_persistante.py#L74) ; propriete_lecture. Signature : `key(self)`.

**Paramètres :**

- `self` (positionnel_ou_nomme) : Instance sur laquelle la méthode ou la propriété travaille.

**Fonctionnement :**

- Composer le chemin à partir de la racine normalisée
- ne pas ouvrir la destination.

**Retour :** Objet Path.

**Effets :** Aucun fichier créé ni aucune valeur privée lue.

**Numérotation prévue :** DÉBUT `MAH-F0053:L0001` à la ligne source 73 ; FIN `MAH-F0053:L0003` à la ligne 75. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0054 — `Paths.lock[lecture]`

**Rôle :** Désigner le fichier du verrou des opérations.

**Repère :** [tools/demo_persistante.py:78](../../tools/demo_persistante.py#L78) ; propriete_lecture. Signature : `lock(self)`.

**Paramètres :**

- `self` (positionnel_ou_nomme) : Instance sur laquelle la méthode ou la propriété travaille.

**Fonctionnement :**

- Composer le chemin à partir de la racine normalisée
- ne pas ouvrir la destination.

**Retour :** Objet Path.

**Effets :** Aucun fichier créé ni aucune valeur privée lue.

**Numérotation prévue :** DÉBUT `MAH-F0054:L0001` à la ligne source 77 ; FIN `MAH-F0054:L0003` à la ligne 79. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0055 — `Paths.backups[lecture]`

**Rôle :** Désigner le dossier des sauvegardes locales.

**Repère :** [tools/demo_persistante.py:82](../../tools/demo_persistante.py#L82) ; propriete_lecture. Signature : `backups(self)`.

**Paramètres :**

- `self` (positionnel_ou_nomme) : Instance sur laquelle la méthode ou la propriété travaille.

**Fonctionnement :**

- Composer le chemin à partir de la racine normalisée
- ne pas ouvrir la destination.

**Retour :** Objet Path.

**Effets :** Aucun fichier créé ni aucune valeur privée lue.

**Numérotation prévue :** DÉBUT `MAH-F0055:L0001` à la ligne source 81 ; FIN `MAH-F0055:L0003` à la ligne 83. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0056 — `Paths.checked`

**Rôle :** Refuser un chemin extérieur ou redirigé.

**Repère :** [tools/demo_persistante.py:85](../../tools/demo_persistante.py#L85) ; methode. Signature : `checked(self, path)`.

**Paramètres :**

- `self` (positionnel_ou_nomme) : Instance sur laquelle la méthode ou la propriété travaille.
- `path` (positionnel_ou_nomme) : Chemin de fichier sous garde, ou chemin HTTP pour les clients WSGI du kit.

**Fonctionnement :**

- Normaliser le chemin
- vérifier qu’il reste sous root
- refuser liens symboliques, jonctions et fichiers à plusieurs liens physiques.

**Retour :** Objet Path validé.

**Effets :** Lectures de métadonnées du système de fichiers ; exception LocalError si le chemin est dangereux.

**Erreurs explicitement levées dans ce corps :** `LocalError`. Les appels délégués peuvent aussi échouer.

**Numérotation prévue :** DÉBUT `MAH-F0056:L0001` à la ligne source 85 ; FIN `MAH-F0056:L0012` à la ligne 96. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0057 — `_windows_security`

**Rôle :** Créer ou vérifier une protection Windows du dossier privé.

**Repère :** [tools/demo_persistante.py:99](../../tools/demo_persistante.py#L99) ; fonction. Signature : `_windows_security(action, path=None)`.

**Paramètres :**

- `action` (positionnel_ou_nomme) : Action demandée ; sa signification dépend du contrat : sécurité, SQL ou garde du kit.
- `path` (positionnel_ou_nomme ; défaut source : `None`) : Chemin de fichier sous garde, ou chemin HTTP pour les clients WSGI du kit.

**Fonctionnement :**

- Déterminer le SID du compte courant
- construire les attributs de sécurité
- créer ou inspecter le dossier selon action
- libérer les ressources Windows.

**Retour :** None en cas de succès.

**Effets :** Appels à l’API Windows et éventuelle création de dossier privé ; ne pas imprimer d’informations d’accès.

**Erreurs explicitement levées dans ce corps :** `LocalError`. Les appels délégués peuvent aussi échouer.

**Numérotation prévue :** DÉBUT `MAH-F0057:L0001` à la ligne source 99 ; FIN `MAH-F0057:L0063` à la ligne 161. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0058 — `private_directory`

**Rôle :** Obtenir un dossier privé validé.

**Repère :** [tools/demo_persistante.py:164](../../tools/demo_persistante.py#L164) ; fonction. Signature : `private_directory(paths, path, *, create=False)`.

**Paramètres :**

- `paths` (positionnel_ou_nomme) : Objet Paths regroupant les chemins privés du jeu local.
- `path` (positionnel_ou_nomme) : Chemin de fichier sous garde, ou chemin HTTP pour les clients WSGI du kit.
- `create` (nomme_seul ; défaut source : `False`) : Autorise explicitement la création de la ressource prévue, sinon vérification seule.

**Fonctionnement :**

- Valider le chemin
- utiliser les contrôles Windows ou les droits du système selon la plateforme
- créer seulement si demandé.

**Retour :** Objet Path du dossier.

**Effets :** Peut créer le dossier et vérifier ses autorisations.

**Erreurs explicitement levées dans ce corps :** `LocalError`. Les appels délégués peuvent aussi échouer.

**Numérotation prévue :** DÉBUT `MAH-F0058:L0001` à la ligne source 164 ; FIN `MAH-F0058:L0009` à la ligne 172. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0059 — `exclusive_file`

**Rôle :** Créer un fichier sans remplacer un fichier existant.

**Repère :** [tools/demo_persistante.py:175](../../tools/demo_persistante.py#L175) ; fonction. Signature : `exclusive_file(path, content=b'')`.

**Paramètres :**

- `path` (positionnel_ou_nomme) : Chemin de fichier sous garde, ou chemin HTTP pour les clients WSGI du kit.
- `content` (positionnel_ou_nomme ; défaut source : `b''`) : Octets à écrire dans le nouveau fichier, sans remplacement d’un fichier existant.

**Fonctionnement :**

- Ouvrir avec création exclusive
- écrire content
- conserver les protections prévues.

**Retour :** None.

**Effets :** Écrit un nouveau fichier ; refuse une destination existante.

**Numérotation prévue :** DÉBUT `MAH-F0059:L0001` à la ligne source 175 ; FIN `MAH-F0059:L0006` à la ligne 180. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0060 — `operation_lock`

**Rôle :** Empêcher deux opérations persistantes concurrentes.

**Repère :** [tools/demo_persistante.py:184](../../tools/demo_persistante.py#L184) ; fonction. Signature : `operation_lock(paths, *, create=False)`.

**Paramètres :**

- `paths` (positionnel_ou_nomme) : Objet Paths regroupant les chemins privés du jeu local.
- `create` (nomme_seul ; défaut source : `False`) : Autorise explicitement la création de la ressource prévue, sinon vérification seule.

**Fonctionnement :**

- Valider le chemin du verrou
- le créer seulement lorsque permis
- obtenir un verrou non bloquant
- le libérer dans finally.

**Retour :** Gestionnaire de contexte sans valeur métier fournie au bloc.

**Effets :** Ouvre un fichier de verrou et maintient son verrou pendant le contexte.

**Erreurs explicitement levées dans ce corps :** `LocalError`. Les appels délégués peuvent aussi échouer.

**Numérotation prévue :** DÉBUT `MAH-F0060:L0001` à la ligne source 183 ; FIN `MAH-F0060:L0036` à la ligne 218. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0061 — `_backend`

**Rôle :** Charger les modèles et le validateur de mot de passe attendus.

**Repère :** [tools/demo_persistante.py:221](../../tools/demo_persistante.py#L221) ; fonction. Signature : `_backend()`.

**Paramètres explicites :** aucun. La fonction peut utiliser son contexte Flask, des variables du module ou une fermeture ; ses effets et le déroulement le précisent.

**Fonctionnement :**

- Préparer le chemin d’import
- charger models et vérifier son fichier d’origine
- importer is_valid_password.

**Retour :** Couple module models, fonction is_valid_password.

**Effets :** Modifie l’environnement d’import du processus ; refuse un autre module models déjà chargé ; ne démarre pas le serveur à lui seul.

**Erreurs explicitement levées dans ce corps :** `LocalError`. Les appels délégués peuvent aussi échouer.

**Numérotation prévue :** DÉBUT `MAH-F0061:L0001` à la ligne source 221 ; FIN `MAH-F0061:L0009` à la ligne 229. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0062 — `catalogue`

**Rôle :** Lire le catalogue à travers le validateur du kit.

**Repère :** [tools/demo_persistante.py:232](../../tools/demo_persistante.py#L232) ; fonction. Signature : `catalogue()`.

**Paramètres explicites :** aucun. La fonction peut utiliser son contexte Flask, des variables du module ou une fermeture ; ses effets et le déroulement le précisent.

**Fonctionnement :**

- Charger le module du kit par son chemin
- vérifier ses sources
- appeler son chargeur des six textes.

**Retour :** Liste des six dossiers validés.

**Effets :** Lit des sources et le catalogue ; aucun peuplement de base ici.

**Numérotation prévue :** DÉBUT `MAH-F0062:L0001` à la ligne source 232 ; FIN `MAH-F0062:L0006` à la ligne 237. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0063 — `database_uri`

**Rôle :** Construire une URI SQLite explicite.

**Repère :** [tools/demo_persistante.py:240](../../tools/demo_persistante.py#L240) ; fonction. Signature : `database_uri(path, mode)`.

**Paramètres :**

- `path` (positionnel_ou_nomme) : Chemin de fichier sous garde, ou chemin HTTP pour les clients WSGI du kit.
- `mode` (positionnel_ou_nomme) : Mode d’ouverture SQLite à encoder dans l’URI, par exemple lecture seule ou lecture-écriture selon l’appel.

**Fonctionnement :**

- Transformer path en URI
- ajouter les paramètres de mode demandés.

**Retour :** Chaîne d’URI SQLite.

**Effets :** Aucune connexion ; le mode fourni détermine ensuite les permissions d’ouverture.

**Numérotation prévue :** DÉBUT `MAH-F0063:L0001` à la ligne source 240 ; FIN `MAH-F0063:L0002` à la ligne 241. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0064 — `opened`

**Rôle :** Encadrer une connexion SQLite au fichier choisi.

**Repère :** [tools/demo_persistante.py:245](../../tools/demo_persistante.py#L245) ; fonction. Signature : `opened(path, *, readonly=True)`.

**Paramètres :**

- `path` (positionnel_ou_nomme) : Chemin de fichier sous garde, ou chemin HTTP pour les clients WSGI du kit.
- `readonly` (nomme_seul ; défaut source : `True`) : Sélectionne la lecture seule de la connexion SQLite lorsqu’il est vrai.

**Fonctionnement :**

- Ouvrir l’URI en lecture seule par défaut ou en lecture-écriture sur demande
- activer les FK
- fournir la connexion
- la fermer à la sortie.

**Retour :** Gestionnaire de contexte fournissant une connexion SQLite.

**Effets :** Ouvre le fichier autorisé ; toute écriture dépend de readonly et du code appelant.

**Erreurs explicitement levées dans ce corps :** `LocalError`. Les appels délégués peuvent aussi échouer.

**Numérotation prévue :** DÉBUT `MAH-F0064:L0001` à la ligne source 244 ; FIN `MAH-F0064:L0010` à la ligne 253. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0065 — `inspect_database`

**Rôle :** Vérifier le format et l’intégrité du jeu persistant.

**Repère :** [tools/demo_persistante.py:256](../../tools/demo_persistante.py#L256) ; fonction. Signature : `inspect_database(connection, *, initial=False)`.

**Paramètres :**

- `connection` (positionnel_ou_nomme) : Connexion SQLite déjà ouverte par l’appelant pour l’inspection.
- `initial` (nomme_seul ; défaut source : `False`) : Active les exigences propres à un jeu nouvellement initialisé.

**Fonctionnement :**

- Comparer marqueurs et schéma aux modèles
- contrôler FK et journal
- compter les tables et comparer les six originaux et rôles initiaux
- appliquer les contraintes initiales si demandé.

**Retour :** Dictionnaire de comptages et d’alertes.

**Effets :** Lectures SQL et du catalogue ; refuse un schéma inconnu sans réparation.

**Erreurs explicitement levées dans ce corps :** `LocalError`. Les appels délégués peuvent aussi échouer.

**Numérotation prévue :** DÉBUT `MAH-F0065:L0001` à la ligne source 256 ; FIN `MAH-F0065:L0034` à la ligne 289. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0066 — `inspect_database.<lambda>#01`

**Rôle :** Normaliser les espaces du SQL pour comparer le schéma.

**Repère :** [tools/demo_persistante.py:265](../../tools/demo_persistante.py#L265) ; lambda. Signature : `lambda text`.

**Paramètres :**

- `text` (positionnel_ou_nomme) : Texte de schéma à normaliser pour une comparaison en mémoire.

**Fonctionnement :**

- Découper sur les espaces.
- Rejoindre les fragments avec un espace unique.

**Retour :** Chaîne SQL normalisée.

**Effets :** Aucune réécriture du schéma.

**Numérotation prévue :** DÉBUT `MAH-F0066:L0001` à la ligne source 265 ; FIN `MAH-F0066:L0001` à la ligne 265. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0067 — `initialized`

**Rôle :** Vérifier qu’un jeu reconnu et sa clé existent.

**Repère :** [tools/demo_persistante.py:292](../../tools/demo_persistante.py#L292) ; fonction. Signature : `initialized(paths)`.

**Paramètres :**

- `paths` (positionnel_ou_nomme) : Objet Paths regroupant les chemins privés du jeu local.

**Fonctionnement :**

- Valider le dossier et les chemins
- lire et vérifier le format de la clé
- inspecter la base existante.

**Retour :** Octets de la clé privée de session.

**Effets :** Lit un fichier privé et la base ; aucune création implicite ; retour à ne jamais exporter.

**Erreurs explicitement levées dans ce corps :** `LocalError`. Les appels délégués peuvent aussi échouer.

**Numérotation prévue :** DÉBUT `MAH-F0067:L0001` à la ligne source 292 ; FIN `MAH-F0067:L0012` à la ligne 303. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0068 — `application`

**Rôle :** Configurer Flask avec un accès borné à une SQLite précise.

**Repère :** [tools/demo_persistante.py:307](../../tools/demo_persistante.py#L307) ; fonction. Signature : `application(paths, *, database=None, key=None)`.

**Paramètres :**

- `paths` (positionnel_ou_nomme) : Objet Paths regroupant les chemins privés du jeu local.
- `database` (nomme_seul ; défaut source : `None`) : Chemin SQLite optionnel du contexte persistant, ou nom mémoire dans le connect du kit.
- `key` (nomme_seul ; défaut source : `None`) : Clé de session fournie en mémoire ; privée, non reproduite dans le référentiel.

**Fonctionnement :**

- Valider la destination
- neutraliser dotenv/Aiven et les connexions alternatives
- charger une application sous un nom dédié
- fournir application, db et modèles
- libérer les gardes et ressources.

**Retour :** Gestionnaire de contexte fournissant le triplet application Flask, db, modèles.

**Effets :** Modifie temporairement l’environnement et les points d’accès du processus ; peut lire/écrire la seule base choisie pendant le contexte.

**Erreurs explicitement levées dans ce corps :** `LocalError`. Les appels délégués peuvent aussi échouer.

**Numérotation prévue :** DÉBUT `MAH-F0068:L0001` à la ligne source 306 ; FIN `MAH-F0068:L0075` à la ligne 380. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0069 — `application.deny`

**Rôle :** Refuser une connexion hors du périmètre autorisé.

**Repère :** [tools/demo_persistante.py:327](../../tools/demo_persistante.py#L327) ; fonction_imbriquee. Signature : `deny(*args, **kwargs)`.

**Paramètres :**

- `args` (positionnels_supplementaires) : Arguments positionnels complémentaires reçus par un adaptateur ; transmis ou ignorés selon son contrat.
- `kwargs` (nommes_supplementaires) : Arguments nommés complémentaires reçus par un adaptateur ; transmis ou ignorés selon son contrat.

**Fonctionnement :**

- Interrompre immédiatement l’appel avec une erreur constante.

**Retour :** Aucun retour normal : exception LocalError.

**Effets :** Ne transmet pas les détails privés de la connexion refusée.

**Erreurs explicitement levées dans ce corps :** `LocalError`. Les appels délégués peuvent aussi échouer.

**Numérotation prévue :** DÉBUT `MAH-F0069:L0001` à la ligne source 327 ; FIN `MAH-F0069:L0002` à la ligne 328. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0070 — `application.guard`

**Rôle :** Contrôler le moteur avant une connexion SQLAlchemy.

**Repère :** [tools/demo_persistante.py:329](../../tools/demo_persistante.py#L329) ; fonction_imbriquee. Signature : `guard(engine)`.

**Paramètres :**

- `engine` (positionnel_ou_nomme) : Moteur SQLAlchemy dont le pilote, l’URL ou la destination doivent être contrôlés.

**Fonctionnement :**

- Comparer l’URL attendue
- vérifier l’existence et le chemin du fichier
- déléguer tout écart au refus.

**Retour :** None si le moteur est conforme.

**Effets :** Lit les métadonnées du fichier ; peut interrompre la connexion.

**Numérotation prévue :** DÉBUT `MAH-F0070:L0001` à la ligne source 329 ; FIN `MAH-F0070:L0003` à la ligne 331. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0071 — `application.connect`

**Rôle :** Ouvrir uniquement la connexion SQLite explicitement autorisée.

**Repère :** [tools/demo_persistante.py:332](../../tools/demo_persistante.py#L332) ; fonction_imbriquee. Signature : `connect(database_name, *args, **kwargs)`.

**Paramètres :**

- `database_name` (positionnel_ou_nomme) : URI SQLite exacte à comparer aux destinations autorisées.
- `args` (positionnels_supplementaires) : Arguments positionnels complémentaires reçus par un adaptateur ; transmis ou ignorés selon son contrat.
- `kwargs` (nommes_supplementaires) : Arguments nommés complémentaires reçus par un adaptateur ; transmis ou ignorés selon son contrat.

**Fonctionnement :**

- Contrôler URI et option uri
- vérifier le fichier
- ouvrir la connexion
- activer les FK et interdire ATTACH/DETACH.

**Retour :** Connexion sqlite3 validée.

**Effets :** Ouverture du seul fichier prévu ; installation d’un callback d’autorisation.

**Numérotation prévue :** DÉBUT `MAH-F0071:L0001` à la ligne source 332 ; FIN `MAH-F0071:L0012` à la ligne 343. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0072 — `application.connect.<lambda>#01`

**Rôle :** Autoriser ou refuser une action de la connexion SQLite.

**Repère :** [tools/demo_persistante.py:342](../../tools/demo_persistante.py#L342) ; lambda. Signature : `lambda action, *rest`.

**Paramètres :**

- `action` (positionnel_ou_nomme) : Action demandée ; sa signification dépend du contrat : sécurité, SQL ou garde du kit.
- `rest` (positionnels_supplementaires) : Arguments additionnels du callback, non utilisés par le contrôle décrit.

**Fonctionnement :**

- Refuser ATTACH et DETACH.
- Autoriser les autres actions via les constantes SQLite.

**Retour :** Constante SQLITE_DENY ou SQLITE_OK.

**Effets :** Callback de protection de la connexion.

**Numérotation prévue :** DÉBUT `MAH-F0072:L0001` à la ligne source 342 ; FIN `MAH-F0072:L0001` à la ligne 342. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0073 — `application.configure`

**Rôle :** Configurer les options privées avant init_app.

**Repère :** [tools/demo_persistante.py:344](../../tools/demo_persistante.py#L344) ; fonction_imbriquee. Signature : `configure(app)`.

**Paramètres :**

- `app` (positionnel_ou_nomme) : Application Flask existante à configurer ou à utiliser dans un contexte isolé.

**Fonctionnement :**

- Vérifier l’URI
- imposer cookie propre, options moteur et absence de debug
- appeler le init_app capturé.

**Retour :** None.

**Effets :** Modifie la configuration de l’application puis initialise l’extension SQLAlchemy.

**Numérotation prévue :** DÉBUT `MAH-F0073:L0001` à la ligne source 344 ; FIN `MAH-F0073:L0007` à la ligne 350. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0074 — `application.<lambda>#01`

**Rôle :** Neutraliser le chargement dotenv dans le contexte persistant.

**Repère :** [tools/demo_persistante.py:356](../../tools/demo_persistante.py#L356) ; lambda. Signature : `lambda *a, **k`.

**Paramètres :**

- `a` (positionnels_supplementaires) : Arguments positionnels complémentaires reçus par un adaptateur ; transmis ou ignorés selon son contrat.
- `k` (nommes_supplementaires) : Arguments nommés complémentaires reçus par un adaptateur ; transmis ou ignorés selon son contrat.

**Fonctionnement :**

- Accepter la signature compatible.
- Renvoyer faux sans lire la configuration privée.

**Retour :** Booléen False.

**Effets :** Empêche le chargement dotenv pendant le patch ; aucun fichier lu ici.

**Numérotation prévue :** DÉBUT `MAH-F0074:L0001` à la ligne source 356 ; FIN `MAH-F0074:L0001` à la ligne 356. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0075 — `application.<lambda>#02`

**Rôle :** Neutraliser le chargement dotenv dans le contexte persistant.

**Repère :** [tools/demo_persistante.py:356](../../tools/demo_persistante.py#L356) ; lambda. Signature : `lambda *a, **k`.

**Paramètres :**

- `a` (positionnels_supplementaires) : Arguments positionnels complémentaires reçus par un adaptateur ; transmis ou ignorés selon son contrat.
- `k` (nommes_supplementaires) : Arguments nommés complémentaires reçus par un adaptateur ; transmis ou ignorés selon son contrat.

**Fonctionnement :**

- Accepter la signature compatible.
- Renvoyer faux sans lire la configuration privée.

**Retour :** Booléen False.

**Effets :** Empêche le chargement dotenv pendant le patch ; aucun fichier lu ici.

**Numérotation prévue :** DÉBUT `MAH-F0075:L0001` à la ligne source 356 ; FIN `MAH-F0075:L0001` à la ligne 356. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0076 — `application.<lambda>#03`

**Rôle :** Contrôler le moteur puis appeler sa connexion originale.

**Repère :** [tools/demo_persistante.py:360](../../tools/demo_persistante.py#L360) ; lambda. Signature : `lambda engine, *a, **k`.

**Paramètres :**

- `engine` (positionnel_ou_nomme) : Moteur SQLAlchemy dont le pilote, l’URL ou la destination doivent être contrôlés.
- `a` (positionnels_supplementaires) : Arguments positionnels complémentaires reçus par un adaptateur ; transmis ou ignorés selon son contrat.
- `k` (nommes_supplementaires) : Arguments nommés complémentaires reçus par un adaptateur ; transmis ou ignorés selon son contrat.

**Fonctionnement :**

- Exécuter guard sur le moteur.
- Transmettre les arguments au connect ou raw_connection capturé et renvoyer son résultat.

**Retour :** Retour de la méthode de connexion originale.

**Effets :** Peut ouvrir uniquement la SQLite autorisée.

**Numérotation prévue :** DÉBUT `MAH-F0076:L0001` à la ligne source 360 ; FIN `MAH-F0076:L0001` à la ligne 360. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0077 — `application.<lambda>#04`

**Rôle :** Contrôler le moteur puis appeler sa connexion originale.

**Repère :** [tools/demo_persistante.py:361](../../tools/demo_persistante.py#L361) ; lambda. Signature : `lambda engine, *a, **k`.

**Paramètres :**

- `engine` (positionnel_ou_nomme) : Moteur SQLAlchemy dont le pilote, l’URL ou la destination doivent être contrôlés.
- `a` (positionnels_supplementaires) : Arguments positionnels complémentaires reçus par un adaptateur ; transmis ou ignorés selon son contrat.
- `k` (nommes_supplementaires) : Arguments nommés complémentaires reçus par un adaptateur ; transmis ou ignorés selon son contrat.

**Fonctionnement :**

- Exécuter guard sur le moteur.
- Transmettre les arguments au connect ou raw_connection capturé et renvoyer son résultat.

**Retour :** Retour de la méthode de connexion originale.

**Effets :** Peut ouvrir uniquement la SQLite autorisée.

**Numérotation prévue :** DÉBUT `MAH-F0077:L0001` à la ligne source 361 ; FIN `MAH-F0077:L0001` à la ligne 361. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0078 — `_valid_people`

**Rôle :** Contrôler les trois comptes fournis à l’initialisation.

**Repère :** [tools/demo_persistante.py:383](../../tools/demo_persistante.py#L383) ; fonction. Signature : `_valid_people(people)`.

**Paramètres :**

- `people` (positionnel_ou_nomme) : Liste des objets Person pour l’initialisation ; valeurs sensibles exclues des sorties.

**Fonctionnement :**

- Vérifier les structures et identités attendues
- appliquer la validation existante des mots de passe et adresses
- refuser les doublons ou valeurs invalides.

**Retour :** None si les données sont conformes.

**Effets :** Validation en mémoire ; aucune création de compte ; données à ne pas journaliser.

**Erreurs explicitement levées dans ce corps :** `LocalError`. Les appels délégués peuvent aussi échouer.

**Numérotation prévue :** DÉBUT `MAH-F0078:L0001` à la ligne source 383 ; FIN `MAH-F0078:L0020` à la ligne 402. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0079 — `collect_people`

**Rôle :** Recueillir les informations de création dans une console privée.

**Repère :** [tools/demo_persistante.py:405](../../tools/demo_persistante.py#L405) ; fonction. Signature : `collect_people()`.

**Paramètres explicites :** aucun. La fonction peut utiliser son contexte Flask, des variables du module ou une fermeture ; ses effets et le déroulement le précisent.

**Fonctionnement :**

- Exiger une saisie interactive
- demander les valeurs nécessaires et la double saisie sans écho
- valider la liste obtenue.

**Retour :** Liste d’objets Person.

**Effets :** Lit le terminal ; garde les mots de passe bruts seulement en mémoire.

**Erreurs explicitement levées dans ce corps :** `LocalError`. Les appels délégués peuvent aussi échouer.

**Numérotation prévue :** DÉBUT `MAH-F0079:L0001` à la ligne source 405 ; FIN `MAH-F0079:L0016` à la ligne 420. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0080 — `verify_git_exclusions`

**Rôle :** Vérifier que les fichiers privés ne seront pas suivis par Git.

**Repère :** [tools/demo_persistante.py:423](../../tools/demo_persistante.py#L423) ; fonction. Signature : `verify_git_exclusions(paths)`.

**Paramètres :**

- `paths` (positionnel_ou_nomme) : Objet Paths regroupant les chemins privés du jeu local.

**Fonctionnement :**

- Interroger check-ignore et ls-files avec les chemins privés prévus
- refuser un fichier non exclu ou suivi.

**Retour :** None.

**Effets :** Sous-processus Git de contrôle, sans ajout ni commit.

**Erreurs explicitement levées dans ce corps :** `LocalError`. Les appels délégués peuvent aussi échouer.

**Numérotation prévue :** DÉBUT `MAH-F0080:L0001` à la ligne source 423 ; FIN `MAH-F0080:L0011` à la ligne 433. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0081 — `_work`

**Rôle :** Préparer un dossier de travail privé neuf.

**Repère :** [tools/demo_persistante.py:436](../../tools/demo_persistante.py#L436) ; fonction. Signature : `_work(paths, parent)`.

**Paramètres :**

- `paths` (positionnel_ou_nomme) : Objet Paths regroupant les chemins privés du jeu local.
- `parent` (positionnel_ou_nomme) : Répertoire parent autorisé pour créer le travail temporaire de l’opération.

**Fonctionnement :**

- Valider le parent
- générer un nom propre à l’opération
- créer le dossier privé et renvoyer son chemin.

**Retour :** Objet Path du dossier de travail.

**Effets :** Crée un nouveau dossier réservé à l’opération.

**Numérotation prévue :** DÉBUT `MAH-F0081:L0001` à la ligne source 436 ; FIN `MAH-F0081:L0005` à la ligne 440. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0082 — `_discard`

**Rôle :** Nettoyer uniquement le dossier temporaire reconnu du lanceur.

**Repère :** [tools/demo_persistante.py:443](../../tools/demo_persistante.py#L443) ; fonction. Signature : `_discard(paths, work)`.

**Paramètres :**

- `paths` (positionnel_ou_nomme) : Objet Paths regroupant les chemins privés du jeu local.
- `work` (positionnel_ou_nomme) : Dossier de travail privé à nettoyer après validation de son périmètre.

**Fonctionnement :**

- Valider son chemin et son préfixe
- refuser une autre destination
- supprimer ce dossier de travail s’il existe.

**Retour :** None.

**Effets :** Suppression récursive bornée au travail temporaire ; aucune exécution autorisée pour ce lot documentaire.

**Erreurs explicitement levées dans ce corps :** `LocalError`. Les appels délégués peuvent aussi échouer.

**Numérotation prévue :** DÉBUT `MAH-F0082:L0001` à la ligne source 443 ; FIN `MAH-F0082:L0006` à la ligne 448. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0083 — `initialize`

**Rôle :** Créer un jeu persistant neuf sans remplacer un jeu existant.

**Repère :** [tools/demo_persistante.py:451](../../tools/demo_persistante.py#L451) ; fonction. Signature : `initialize(paths, people)`.

**Paramètres :**

- `paths` (positionnel_ou_nomme) : Objet Paths regroupant les chemins privés du jeu local.
- `people` (positionnel_ou_nomme) : Liste des objets Person pour l’initialisation ; valeurs sensibles exclues des sorties.

**Fonctionnement :**

- Refuser la destination existante
- valider les comptes et le catalogue
- préparer base et clé dans un dossier privé de travail
- créer le schéma et insérer le jeu
- contrôler puis publier le dossier neuf.

**Retour :** Dictionnaire du contrôle initial.

**Effets :** Crée fichiers privés, comptes et données ; nettoie son travail dans finally ; opération distincte du démarrage.

**Erreurs explicitement levées dans ce corps :** `LocalError`. Les appels délégués peuvent aussi échouer.

**Numérotation prévue :** DÉBUT `MAH-F0083:L0001` à la ligne source 451 ; FIN `MAH-F0083:L0034` à la ligne 484. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0084 — `check`

**Rôle :** Contrôler un jeu existant sans le réparer.

**Repère :** [tools/demo_persistante.py:487](../../tools/demo_persistante.py#L487) ; fonction. Signature : `check(paths)`.

**Paramètres :**

- `paths` (positionnel_ou_nomme) : Objet Paths regroupant les chemins privés du jeu local.

**Fonctionnement :**

- Vérifier son initialisation
- ouvrir la base en lecture seule
- renvoyer le résultat d’inspection.

**Retour :** Dictionnaire des comptages et alertes.

**Effets :** Lectures de clé, fichiers et base ; ne réinitialise pas les données.

**Numérotation prévue :** DÉBUT `MAH-F0084:L0001` à la ligne source 487 ; FIN `MAH-F0084:L0004` à la ligne 490. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0085 — `_copy_database`

**Rôle :** Copier une SQLite avec l’API de sauvegarde.

**Repère :** [tools/demo_persistante.py:493](../../tools/demo_persistante.py#L493) ; fonction. Signature : `_copy_database(source, target)`.

**Paramètres :**

- `source` (positionnel_ou_nomme) : Chemin de base source pour la copie, ou texte historique dans historical_blocks.
- `target` (positionnel_ou_nomme) : Chemin de la nouvelle SQLite cible de sauvegarde.

**Fonctionnement :**

- Créer la cible exclusivement
- ouvrir source et cible dans leurs modes
- copier avec backup
- contrôler la copie.

**Retour :** None.

**Effets :** Crée et écrit une nouvelle SQLite cible ; ne remplace pas un fichier existant.

**Numérotation prévue :** DÉBUT `MAH-F0085:L0001` à la ligne source 493 ; FIN `MAH-F0085:L0005` à la ligne 497. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0086 — `backup`

**Rôle :** Créer une sauvegarde privée datée du jeu existant.

**Repère :** [tools/demo_persistante.py:500](../../tools/demo_persistante.py#L500) ; fonction. Signature : `backup(paths)`.

**Paramètres :**

- `paths` (positionnel_ou_nomme) : Objet Paths regroupant les chemins privés du jeu local.

**Fonctionnement :**

- Valider le jeu
- préparer un travail privé
- copier la base et écrire son manifeste
- publier un nouveau dossier de sauvegarde.

**Retour :** Identifiant local de la sauvegarde.

**Effets :** Lit le jeu privé et crée des fichiers de sauvegarde ; nettoyage du travail en finally.

**Numérotation prévue :** DÉBUT `MAH-F0086:L0001` à la ligne source 500 ; FIN `MAH-F0086:L0017` à la ligne 516. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0087 — `restore`

**Rôle :** Restaurer explicitement un état reconnu.

**Repère :** [tools/demo_persistante.py:519](../../tools/demo_persistante.py#L519) ; fonction. Signature : `restore(paths, snapshot, *, replace=False, renew_key=False)`.

**Paramètres :**

- `paths` (positionnel_ou_nomme) : Objet Paths regroupant les chemins privés du jeu local.
- `snapshot` (positionnel_ou_nomme) : Identifiant local d’une sauvegarde reconnue, jamais un chemin arbitraire.
- `replace` (nomme_seul ; défaut source : `False`) : Autorisation explicite de remplacer un jeu persistant déjà présent.
- `renew_key` (nomme_seul ; défaut source : `False`) : Demande de génération d’une nouvelle clé lors de la restauration.

**Fonctionnement :**

- Valider l’identifiant et les empreintes
- exiger le remplacement explicite si un jeu existe
- créer une sauvegarde de sécurité
- préparer et contrôler la copie
- remplacer ou publier selon le cas.

**Retour :** Dictionnaire avec sauvegarde de sécurité et indicateur de renouvellement de clé.

**Effets :** Peut remplacer base et clé et faire perdre les modifications postérieures à la sauvegarde ; un échec après changement de clé peut déjà imposer une reconnexion.

**Erreurs explicitement levées dans ce corps :** `LocalError`. Les appels délégués peuvent aussi échouer.

**Numérotation prévue :** DÉBUT `MAH-F0087:L0001` à la ligne source 519 ; FIN `MAH-F0087:L0035` à la ligne 553. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0088 — `serve`

**Rôle :** Servir le jeu persistant déjà initialisé.

**Repère :** [tools/demo_persistante.py:556](../../tools/demo_persistante.py#L556) ; fonction. Signature : `serve(paths)`.

**Paramètres :**

- `paths` (positionnel_ou_nomme) : Objet Paths regroupant les chemins privés du jeu local.

**Fonctionnement :**

- Vérifier le jeu
- ouvrir l’application bornée
- composer le WSGI
- ouvrir l’écoute locale prévue
- servir jusqu’à arrêt du processus.

**Retour :** None après sortie normale de la boucle.

**Effets :** Écoute réseau locale ; utilise la base existante ; refuse un port occupé sans arrêter l’autre processus.

**Erreurs explicitement levées dans ce corps :** `LocalError`. Les appels délégués peuvent aussi échouer.

**Numérotation prévue :** DÉBUT `MAH-F0088:L0001` à la ligne source 556 ; FIN `MAH-F0088:L0017` à la ligne 572. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0089 — `serve.QuietHandler.log`

**Rôle :** Éviter la journalisation des requêtes de cette démonstration.

**Repère :** [tools/demo_persistante.py:564](../../tools/demo_persistante.py#L564) ; methode. Signature : `log(self, *args, **kwargs)`.

**Paramètres :**

- `self` (positionnel_ou_nomme) : Instance sur laquelle la méthode ou la propriété travaille.
- `args` (positionnels_supplementaires) : Arguments positionnels complémentaires reçus par un adaptateur ; transmis ou ignorés selon son contrat.
- `kwargs` (nommes_supplementaires) : Arguments nommés complémentaires reçus par un adaptateur ; transmis ou ignorés selon son contrat.

**Fonctionnement :**

- Accepter la signature du journaliseur
- ne rien émettre.

**Retour :** None.

**Effets :** Supprime le journal habituel de requêtes du gestionnaire créé ici.

**Numérotation prévue :** DÉBUT `MAH-F0089:L0001` à la ligne source 564 ; FIN `MAH-F0089:L0002` à la ligne 565. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0090 — `main`

**Rôle :** Aiguiller les sous-commandes du mode persistant.

**Repère :** [tools/demo_persistante.py:575](../../tools/demo_persistante.py#L575) ; fonction. Signature : `main(argv=None)`.

**Paramètres :**

- `argv` (positionnel_ou_nomme ; défaut source : `None`) : Arguments de ligne de commande fournis au parseur, ou arguments du processus si None.

**Fonctionnement :**

- Lire les arguments
- séparer init, check, serve, backup et restore
- obtenir le verrou
- exécuter seulement la commande choisie
- rendre les erreurs privées génériques.

**Retour :** Code de sortie entier.

**Effets :** Les effets dépendent de la sous-commande : terminal, fichiers, base ou écoute ; aucun appel pendant ce lot.

**Erreurs explicitement levées dans ce corps :** `LocalError`. Les appels délégués peuvent aussi échouer.

**Numérotation prévue :** DÉBUT `MAH-F0090:L0001` à la ligne source 575 ; FIN `MAH-F0090:L0045` à la ligne 619. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

### MAH-M013 — `tools/recette_lot6g4.py`

Préparer les jeux mémoire et vérifier le parcours sous gardes, sans base persistante.

- **MAH-C016 — `Isolation`**, lignes 68–129 : Gardes, compteurs et hook d’audit propres au processus du kit.
- **MAH-C017 — `HistoricalText`**, lignes 145–181 : Parseur HTML limité aux blocs historiques autorisés, sans exécution ni rendu HTML.
- **MAH-C018 — `inspect_assets.Assets`**, lignes 364–372 : Parseur local qui relève les références aux scripts et feuilles de style des pages du kit.
- **MAH-C019 — `main.QuietHandler`**, lignes 617–619 : Gestionnaire WSGI spécialisé pour ne pas journaliser les requêtes de démonstration.


#### MAH-F0091 — `sensitive`

**Rôle :** Reconnaître un chemin privé interdit au kit.

**Repère :** [tools/recette_lot6g4.py:37](../../tools/recette_lot6g4.py#L37) ; fonction. Signature : `sensitive(path)`.

**Paramètres :**

- `path` (positionnel_ou_nomme) : Chemin de fichier sous garde, ou chemin HTTP pour les clients WSGI du kit.

**Fonctionnement :**

- Examiner le nom, l’extension et l’emplacement sous certs
- renvoyer la classification.

**Retour :** Booléen.

**Effets :** Pas d’ouverture du contenu du fichier.

**Numérotation prévue :** DÉBUT `MAH-F0091:L0001` à la ligne source 37 ; FIN `MAH-F0091:L0004` à la ligne 40. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0092 — `validate_sources`

**Rôle :** Contrôler le manifeste avant tout import applicatif du kit.

**Repère :** [tools/recette_lot6g4.py:43](../../tools/recette_lot6g4.py#L43) ; fonction. Signature : `validate_sources()`.

**Paramètres explicites :** aucun. La fonction peut utiliser son contexte Flask, des variables du module ou une fermeture ; ses effets et le déroulement le précisent.

**Fonctionnement :**

- Lire le manifeste
- refuser chemins et catégories interdits
- comparer les SHA-256 normalisées LF
- vérifier ressources publiques, version SQLAlchemy et catalogue.

**Retour :** Ensemble des chemins approuvés.

**Effets :** Lectures de sources et métadonnées de paquet ; aucun renouvellement automatique d’empreinte.

**Erreurs explicitement levées dans ce corps :** `SystemExit`. Les appels délégués peuvent aussi échouer.

**Numérotation prévue :** DÉBUT `MAH-F0092:L0001` à la ligne source 43 ; FIN `MAH-F0092:L0023` à la ligne 65. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0093 — `Isolation.__init__`

**Rôle :** Préparer les règles et compteurs du confinement du kit.

**Repère :** [tools/recette_lot6g4.py:70](../../tools/recette_lot6g4.py#L70) ; methode. Signature : `__init__(self, evidence, approved)`.

**Paramètres :**

- `self` (positionnel_ou_nomme) : Instance sur laquelle la méthode ou la propriété travaille.
- `evidence` (positionnel_ou_nomme) : Répertoire temporaire autorisé pour les preuves du kit, hors du dépôt.
- `approved` (positionnel_ou_nomme) : Ensemble de chemins dont les empreintes ont été approuvées par le manifeste.

**Fonctionnement :**

- Résoudre evidence et approved
- noter les racines Python
- initialiser les compteurs et l’état d’écoute.

**Retour :** None.

**Effets :** Initialise les attributs de l’objet de garde.

**Numérotation prévue :** DÉBUT `MAH-F0093:L0001` à la ligne source 70 ; FIN `MAH-F0093:L0006` à la ligne 75. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0094 — `Isolation.blocked`

**Rôle :** Tracer un refus et interrompre l’opération.

**Repère :** [tools/recette_lot6g4.py:77](../../tools/recette_lot6g4.py#L77) ; methode. Signature : `blocked(self, kind)`.

**Paramètres :**

- `self` (positionnel_ou_nomme) : Instance sur laquelle la méthode ou la propriété travaille.
- `kind` (positionnel_ou_nomme) : Catégorie du refus du kit, ou famille story/comment du contrôle des likes.

**Fonctionnement :**

- Incrémenter le compteur de la catégorie
- lever PermissionError.

**Retour :** Aucun retour normal.

**Effets :** Modifie un compteur en mémoire ; ne réalise pas l’opération refusée.

**Erreurs explicitement levées dans ce corps :** `PermissionError`. Les appels délégués peuvent aussi échouer.

**Numérotation prévue :** DÉBUT `MAH-F0094:L0001` à la ligne source 77 ; FIN `MAH-F0094:L0003` à la ligne 79. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0095 — `Isolation.read`

**Rôle :** Autoriser uniquement les lectures prévues.

**Repère :** [tools/recette_lot6g4.py:81](../../tools/recette_lot6g4.py#L81) ; methode. Signature : `read(self, path)`.

**Paramètres :**

- `self` (positionnel_ou_nomme) : Instance sur laquelle la méthode ou la propriété travaille.
- `path` (positionnel_ou_nomme) : Chemin de fichier sous garde, ou chemin HTTP pour les clients WSGI du kit.

**Fonctionnement :**

- Résoudre le chemin et son éventuelle source de bytecode
- refuser les chemins sensibles
- vérifier les sources approuvées, preuves et racines Python.

**Retour :** None si la lecture est permise.

**Effets :** Validation de chemin ; appelle blocked en cas d’écart.

**Numérotation prévue :** DÉBUT `MAH-F0095:L0001` à la ligne source 81 ; FIN `MAH-F0095:L0007` à la ligne 87. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0096 — `Isolation.write`

**Rôle :** Interdire les écritures dans le dépôt et hors des preuves.

**Repère :** [tools/recette_lot6g4.py:89](../../tools/recette_lot6g4.py#L89) ; methode. Signature : `write(self, path)`.

**Paramètres :**

- `self` (positionnel_ou_nomme) : Instance sur laquelle la méthode ou la propriété travaille.
- `path` (positionnel_ou_nomme) : Chemin de fichier sous garde, ou chemin HTTP pour les clients WSGI du kit.

**Fonctionnement :**

- Résoudre le chemin
- refuser la racine du dépôt
- exiger un chemin sous evidence.

**Retour :** None si l’écriture est permise.

**Effets :** N’écrit pas lui-même ; bloque les destinations non autorisées.

**Numérotation prévue :** DÉBUT `MAH-F0096:L0001` à la ligne source 89 ; FIN `MAH-F0096:L0006` à la ligne 94. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0097 — `Isolation.database`

**Rôle :** Exiger un moteur SQLite strictement en mémoire.

**Repère :** [tools/recette_lot6g4.py:96](../../tools/recette_lot6g4.py#L96) ; methode. Signature : `database(self, engine)`.

**Paramètres :**

- `self` (positionnel_ou_nomme) : Instance sur laquelle la méthode ou la propriété travaille.
- `engine` (positionnel_ou_nomme) : Moteur SQLAlchemy dont le pilote, l’URL ou la destination doivent être contrôlés.

**Fonctionnement :**

- Comparer le pilote et le nom de base à ceux attendus
- refuser tout autre moteur ou fichier.

**Retour :** None si le moteur convient.

**Effets :** Garde préalable, sans ouverture de connexion dans cette méthode.

**Numérotation prévue :** DÉBUT `MAH-F0097:L0001` à la ligne source 96 ; FIN `MAH-F0097:L0003` à la ligne 98. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0098 — `Isolation.audit`

**Rôle :** Distribuer les événements d’audit aux gardes.

**Repère :** [tools/recette_lot6g4.py:100](../../tools/recette_lot6g4.py#L100) ; methode. Signature : `audit(self, event, values)`.

**Paramètres :**

- `self` (positionnel_ou_nomme) : Instance sur laquelle la méthode ou la propriété travaille.
- `event` (positionnel_ou_nomme) : Nom de l’événement reçu par le hook d’audit Python.
- `values` (positionnel_ou_nomme) : Arguments de l’événement d’audit, sans en exporter les valeurs privées.

**Fonctionnement :**

- Distinguer ouvertures, SQLite, exécution, réseau, sous-processus et opérations de fichiers
- autoriser seulement les exceptions d’écoute prévues
- refuser le reste.

**Retour :** None si l’événement est permis.

**Effets :** Peut empêcher une opération et incrémenter les compteurs ; le hook reste propre au processus.

**Numérotation prévue :** DÉBUT `MAH-F0098:L0001` à la ligne source 100 ; FIN `MAH-F0098:L0030` à la ligne 129. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0099 — `public_application`

**Rôle :** Ajouter la liste publique stricte du kit au WSGI général.

**Repère :** [tools/recette_lot6g4.py:132](../../tools/recette_lot6g4.py#L132) ; fonction. Signature : `public_application(api_app)`.

**Paramètres :**

- `api_app` (positionnel_ou_nomme) : Application WSGI de l’API à envelopper ou déléguer.

**Fonctionnement :**

- Composer create_local_app
- définir un filtre de chemins
- renvoyer cette fermeture.

**Retour :** Fonction WSGI.

**Effets :** Aucun serveur lancé par cette fonction.

**Numérotation prévue :** DÉBUT `MAH-F0099:L0001` à la ligne source 132 ; FIN `MAH-F0099:L0011` à la ligne 142. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0100 — `public_application.application`

**Rôle :** Refuser les ressources hors du périmètre scolaire.

**Repère :** [tools/recette_lot6g4.py:136](../../tools/recette_lot6g4.py#L136) ; fonction_imbriquee. Signature : `application(environ, start_response)`.

**Paramètres :**

- `environ` (positionnel_ou_nomme) : Dictionnaire de la requête WSGI : méthode, chemin et contexte serveur.
- `start_response` (positionnel_ou_nomme) : Callback WSGI recevant le statut et les en-têtes de réponse.

**Fonctionnement :**

- Laisser passer racine, API et chemins PUBLIC
- sinon produire la réponse 403.

**Retour :** Itérable WSGI d’octets.

**Effets :** Peut lire des ressources autorisées ou appeler Flask ; aucune extension de la liste publique.

**Numérotation prévue :** DÉBUT `MAH-F0100:L0001` à la ligne source 136 ; FIN `MAH-F0100:L0006` à la ligne 141. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0101 — `HistoricalText.__init__`

**Rôle :** Préparer l’extraction contrôlée des blocs historiques.

**Repère :** [tools/recette_lot6g4.py:147](../../tools/recette_lot6g4.py#L147) ; methode. Signature : `__init__(self)`.

**Paramètres :**

- `self` (positionnel_ou_nomme) : Instance sur laquelle la méthode ou la propriété travaille.

**Fonctionnement :**

- Initialiser HTMLParser
- créer pile de balises, blocs et fragments de texte.

**Retour :** None.

**Effets :** Initialise l’état du parseur, sans exécuter le HTML.

**Numérotation prévue :** DÉBUT `MAH-F0101:L0001` à la ligne source 147 ; FIN `MAH-F0101:L0003` à la ligne 149. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0102 — `HistoricalText.handle_starttag`

**Rôle :** Valider l’ouverture d’une balise historique.

**Repère :** [tools/recette_lot6g4.py:151](../../tools/recette_lot6g4.py#L151) ; methode. Signature : `handle_starttag(self, tag, attrs)`.

**Paramètres :**

- `self` (positionnel_ou_nomme) : Instance sur laquelle la méthode ou la propriété travaille.
- `tag` (positionnel_ou_nomme) : Nom de la balise rencontrée par HTMLParser.
- `attrs` (positionnel_ou_nomme) : Couples nom/valeur des attributs de la balise analysée.

**Fonctionnement :**

- Limiter balises et attributs
- contrôler l’imbrication
- initialiser le texte d’un bloc et empiler la balise.

**Retour :** None, ou ValueError.

**Effets :** Modifie la pile du parseur ; aucun rendu navigateur.

**Erreurs explicitement levées dans ce corps :** `ValueError`. Les appels délégués peuvent aussi échouer.

**Numérotation prévue :** DÉBUT `MAH-F0102:L0001` à la ligne source 151 ; FIN `MAH-F0102:L0010` à la ligne 160. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0103 — `HistoricalText.handle_endtag`

**Rôle :** Fermer un bloc historique et en conserver le texte.

**Repère :** [tools/recette_lot6g4.py:162](../../tools/recette_lot6g4.py#L162) ; methode. Signature : `handle_endtag(self, tag)`.

**Paramètres :**

- `self` (positionnel_ou_nomme) : Instance sur laquelle la méthode ou la propriété travaille.
- `tag` (positionnel_ou_nomme) : Nom de la balise rencontrée par HTMLParser.

**Fonctionnement :**

- Vérifier la fermeture attendue
- retirer la dernière balise de la pile
- produire le bloc terminé et vérifier son contenu.

**Retour :** None, ou ValueError.

**Effets :** Ajoute des blocs en mémoire sans changer les mots sources.

**Erreurs explicitement levées dans ce corps :** `ValueError`. Les appels délégués peuvent aussi échouer.

**Numérotation prévue :** DÉBUT `MAH-F0103:L0001` à la ligne source 162 ; FIN `MAH-F0103:L0008` à la ligne 169. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0104 — `HistoricalText.handle_data`

**Rôle :** Accumuler le texte autorisé.

**Repère :** [tools/recette_lot6g4.py:171](../../tools/recette_lot6g4.py#L171) ; methode. Signature : `handle_data(self, value)`.

**Paramètres :**

- `self` (positionnel_ou_nomme) : Instance sur laquelle la méthode ou la propriété travaille.
- `value` (positionnel_ou_nomme) : Valeur à convertir ou valider selon le contrat de cette fonction.

**Fonctionnement :**

- Vérifier le contexte de la pile
- conserver le texte utile du bloc ou refuser un texte inattendu.

**Retour :** None.

**Effets :** Modifie les fragments du parseur.

**Erreurs explicitement levées dans ce corps :** `ValueError`. Les appels délégués peuvent aussi échouer.

**Numérotation prévue :** DÉBUT `MAH-F0104:L0001` à la ligne source 171 ; FIN `MAH-F0104:L0005` à la ligne 175. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0105 — `HistoricalText.handle_comment`

**Rôle :** Refuser les commentaires HTML historiques non autorisés.

**Repère :** [tools/recette_lot6g4.py:177](../../tools/recette_lot6g4.py#L177) ; methode. Signature : `handle_comment(self, value)`.

**Paramètres :**

- `self` (positionnel_ou_nomme) : Instance sur laquelle la méthode ou la propriété travaille.
- `value` (positionnel_ou_nomme) : Valeur à convertir ou valider selon le contrat de cette fonction.

**Fonctionnement :**

- Lever ValueError à la rencontre d’un commentaire.

**Retour :** Aucun retour normal.

**Effets :** Interrompt l’analyse ; n’écrit aucun fichier.

**Erreurs explicitement levées dans ce corps :** `ValueError`. Les appels délégués peuvent aussi échouer.

**Numérotation prévue :** DÉBUT `MAH-F0105:L0001` à la ligne source 177 ; FIN `MAH-F0105:L0002` à la ligne 178. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0106 — `HistoricalText.handle_decl`

**Rôle :** Refuser une déclaration HTML non attendue.

**Repère :** [tools/recette_lot6g4.py:180](../../tools/recette_lot6g4.py#L180) ; methode. Signature : `handle_decl(self, value)`.

**Paramètres :**

- `self` (positionnel_ou_nomme) : Instance sur laquelle la méthode ou la propriété travaille.
- `value` (positionnel_ou_nomme) : Valeur à convertir ou valider selon le contrat de cette fonction.

**Fonctionnement :**

- Lever ValueError pour la déclaration reçue.

**Retour :** Aucun retour normal.

**Effets :** Interrompt l’analyse ; aucune exécution HTML.

**Erreurs explicitement levées dans ce corps :** `ValueError`. Les appels délégués peuvent aussi échouer.

**Numérotation prévue :** DÉBUT `MAH-F0106:L0001` à la ligne source 180 ; FIN `MAH-F0106:L0002` à la ligne 181. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0107 — `historical_blocks`

**Rôle :** Extraire les paragraphes et intertitres contrôlés d’un texte.

**Repère :** [tools/recette_lot6g4.py:184](../../tools/recette_lot6g4.py#L184) ; fonction. Signature : `historical_blocks(source)`.

**Paramètres :**

- `source` (positionnel_ou_nomme) : Chemin de base source pour la copie, ou texte historique dans historical_blocks.

**Fonctionnement :**

- Créer le parseur
- lui fournir la source et terminer l’analyse
- refuser une pile non fermée ou l’absence de blocs.

**Retour :** Liste de blocs de texte.

**Effets :** Analyse en mémoire seulement.

**Erreurs explicitement levées dans ce corps :** `ValueError`. Les appels délégués peuvent aussi échouer.

**Numérotation prévue :** DÉBUT `MAH-F0107:L0001` à la ligne source 184 ; FIN `MAH-F0107:L0007` à la ligne 190. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0108 — `load_historical_stories`

**Rôle :** Vérifier intégralement le catalogue approuvé.

**Repère :** [tools/recette_lot6g4.py:193](../../tools/recette_lot6g4.py#L193) ; fonction. Signature : `load_historical_stories()`.

**Paramètres explicites :** aucun. La fonction peut utiliser son contexte Flask, des variables du module ou une fermeture ; ses effets et le déroulement le précisent.

**Fonctionnement :**

- Lire le JSON
- contrôler version, choix éditoriaux, six entrées, identifiants et catégories
- comparer les empreintes et le texte extrait au texte conservé.

**Retour :** Liste des six dictionnaires de dossiers.

**Effets :** Lecture du catalogue ; aucune insertion SQL dans cette fonction.

**Erreurs explicitement levées dans ce corps :** `ValueError`. Les appels délégués peuvent aussi échouer.

**Numérotation prévue :** DÉBUT `MAH-F0108:L0001` à la ligne source 193 ; FIN `MAH-F0108:L0030` à la ligne 222. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0109 — `check_historical_journey`

**Rôle :** Contrôler les six histoires par les vraies vues isolées.

**Repère :** [tools/recette_lot6g4.py:225](../../tools/recette_lot6g4.py#L225) ; fonction. Signature : `check_historical_journey(app, application, db, models, credentials)`.

**Paramètres :**

- `app` (positionnel_ou_nomme) : Application Flask existante à configurer ou à utiliser dans un contexte isolé.
- `application` (positionnel_ou_nomme) : Application WSGI composée utilisée par le client de validation.
- `db` (positionnel_ou_nomme) : Extension SQLAlchemy déjà reliée à l’application de test.
- `models` (positionnel_ou_nomme) : Module des modèles chargé dans le périmètre autorisé.
- `credentials` (positionnel_ou_nomme) : Accès fictifs éphémères déjà générés en mémoire ; ne jamais les exporter.

**Fonctionnement :**

- Créer un client WSGI
- comparer les contenus et comptages
- authentifier les comptes fictifs et exercer contributions, permissions et erreurs
- vérifier que les textes d’origine restent identiques.

**Retour :** Dictionnaire du bilan du parcours historique.

**Effets :** Écrit uniquement dans la base mémoire préparée par le kit ; manipule des accès éphémères en mémoire.

**Numérotation prévue :** DÉBUT `MAH-F0109:L0001` à la ligne source 225 ; FIN `MAH-F0109:L0100` à la ligne 324. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0110 — `check_historical_journey.request`

**Rôle :** Envoyer une requête WSGI du scénario historique.

**Repère :** [tools/recette_lot6g4.py:236](../../tools/recette_lot6g4.py#L236) ; fonction_imbriquee. Signature : `request(method, path, status=200, body=None, token=True)`.

**Paramètres :**

- `method` (positionnel_ou_nomme) : Méthode HTTP que le scénario WSGI doit exercer.
- `path` (positionnel_ou_nomme) : Chemin de fichier sous garde, ou chemin HTTP pour les clients WSGI du kit.
- `status` (positionnel_ou_nomme ; défaut source : `200`) : Statut HTTP attendu ou à renvoyer ; forme WSGI textuelle pour prevent_storage.
- `body` (positionnel_ou_nomme ; défaut source : `None`) : Objet JSON de la requête de test, éventuellement absent.
- `token` (positionnel_ou_nomme ; défaut source : `True`) : Indique si le client doit joindre le jeton CSRF en mémoire.

**Fonctionnement :**

- Composer JSON et CSRF selon les options
- appeler le client local
- exiger le statut attendu et consigner seulement méthode, chemin et statut.

**Retour :** JSON décodé de la réponse.

**Effets :** Peut lire/écrire le jeu mémoire selon la route ; n’exporte pas les jetons.

**Numérotation prévue :** DÉBUT `MAH-F0110:L0001` à la ligne source 236 ; FIN `MAH-F0110:L0006` à la ligne 241. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0111 — `check_historical_journey.login`

**Rôle :** Connecter un compte fictif du parcours historique.

**Repère :** [tools/recette_lot6g4.py:243](../../tools/recette_lot6g4.py#L243) ; fonction_imbriquee. Signature : `login(name)`.

**Paramètres :**

- `name` (positionnel_ou_nomme) : Nom de variable de configuration ou repère du compte fictif, selon la fonction.

**Fonctionnement :**

- Appeler la requête de connexion avec les accès mémoire
- retenir le CSRF dans la fermeture
- renvoyer le compte de test.

**Retour :** Dictionnaire du compte connecté.

**Effets :** Modifie les cookies du client WSGI et le jeton en mémoire.

**Numérotation prévue :** DÉBUT `MAH-F0111:L0001` à la ligne source 243 ; FIN `MAH-F0111:L0005` à la ligne 247. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0112 — `check_historical_journey.sql_state`

**Rôle :** Compter toutes les tables du jeu temporaire.

**Repère :** [tools/recette_lot6g4.py:249](../../tools/recette_lot6g4.py#L249) ; fonction_imbriquee. Signature : `sql_state()`.

**Paramètres explicites :** aucun. La fonction peut utiliser son contexte Flask, des variables du module ou une fermeture ; ses effets et le déroulement le précisent.

**Fonctionnement :**

- Entrer dans le contexte Flask
- effectuer un COUNT par table déclarée
- assembler les nombres.

**Retour :** Dictionnaire table vers nombre de lignes.

**Effets :** Lectures SQL uniquement dans la base mémoire.

**Numérotation prévue :** DÉBUT `MAH-F0112:L0001` à la ligne source 249 ; FIN `MAH-F0112:L0004` à la ligne 252. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0113 — `seed`

**Rôle :** Préparer les comptes et dossiers fictifs du kit.

**Repère :** [tools/recette_lot6g4.py:327](../../tools/recette_lot6g4.py#L327) ; fonction. Signature : `seed(db, models, histoires_originales=False)`.

**Paramètres :**

- `db` (positionnel_ou_nomme) : Extension SQLAlchemy déjà reliée à l’application de test.
- `models` (positionnel_ou_nomme) : Module des modèles chargé dans le périmètre autorisé.
- `histoires_originales` (positionnel_ou_nomme ; défaut source : `False`) : Choisit les six textes approuvés plutôt que les deux supports scolaires.

**Fonctionnement :**

- Choisir le catalogue si demandé
- générer les accès éphémères
- ajouter comptes, catégories et dossiers
- valider la transaction.

**Retour :** Dictionnaire des accès éphémères réservés à la console privée.

**Effets :** INSERT et commit dans SQLite mémoire ; aucun compte permanent créé.

**Numérotation prévue :** DÉBUT `MAH-F0113:L0001` à la ligne source 327 ; FIN `MAH-F0113:L0025` à la ligne 351. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0114 — `seven_counts`

**Rôle :** Calculer les sept indicateurs avec leur périmètre exact.

**Repère :** [tools/recette_lot6g4.py:354](../../tools/recette_lot6g4.py#L354) ; fonction. Signature : `seven_counts(db, models)`.

**Paramètres :**

- `db` (positionnel_ou_nomme) : Extension SQLAlchemy déjà reliée à l’application de test.
- `models` (positionnel_ou_nomme) : Module des modèles chargé dans le périmètre autorisé.

**Fonctionnement :**

- Compter les dossiers actifs et leurs catégories
- compter comptes, commentaires et signalements
- compter les seules propositions pending.

**Retour :** Dictionnaire des sept nombres.

**Effets :** Lectures SQL ; ne compter ni une erreur ni un chargement comme zéro.

**Numérotation prévue :** DÉBUT `MAH-F0114:L0001` à la ligne source 354 ; FIN `MAH-F0114:L0007` à la ligne 360. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0115 — `inspect_assets`

**Rôle :** Contrôler les ressources publiques et les refus du kit.

**Repère :** [tools/recette_lot6g4.py:363](../../tools/recette_lot6g4.py#L363) ; fonction. Signature : `inspect_assets(client)`.

**Paramètres :**

- `client` (positionnel_ou_nomme) : Client WSGI local qui ne nécessite pas d’écoute réseau.

**Fonctionnement :**

- Charger chaque ressource autorisée par le client WSGI
- vérifier les références de scripts et styles
- exiger les refus des chemins privés et historiques.

**Retour :** None si toutes les assertions passent.

**Effets :** Requêtes WSGI GET ; aucune écoute ni navigateur.

**Numérotation prévue :** DÉBUT `MAH-F0115:L0001` à la ligne source 363 ; FIN `MAH-F0115:L0019` à la ligne 381. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0116 — `inspect_assets.Assets.__init__`

**Rôle :** Préparer le relevé des ressources HTML.

**Repère :** [tools/recette_lot6g4.py:365](../../tools/recette_lot6g4.py#L365) ; methode. Signature : `__init__(self)`.

**Paramètres :**

- `self` (positionnel_ou_nomme) : Instance sur laquelle la méthode ou la propriété travaille.

**Fonctionnement :**

- Initialiser HTMLParser et la liste paths.

**Retour :** None.

**Effets :** Initialise l’état du parseur local.

**Numérotation prévue :** DÉBUT `MAH-F0116:L0001` à la ligne source 365 ; FIN `MAH-F0116:L0002` à la ligne 366. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0117 — `inspect_assets.Assets.handle_starttag`

**Rôle :** Relever les scripts et feuilles de style du HTML.

**Repère :** [tools/recette_lot6g4.py:367](../../tools/recette_lot6g4.py#L367) ; methode. Signature : `handle_starttag(self, tag, attrs)`.

**Paramètres :**

- `self` (positionnel_ou_nomme) : Instance sur laquelle la méthode ou la propriété travaille.
- `tag` (positionnel_ou_nomme) : Nom de la balise rencontrée par HTMLParser.
- `attrs` (positionnel_ou_nomme) : Couples nom/valeur des attributs de la balise analysée.

**Fonctionnement :**

- Lire les attributs de la balise
- ajouter src pour script et href pour stylesheet.

**Retour :** None.

**Effets :** Ajoute des chemins à la liste du parseur.

**Numérotation prévue :** DÉBUT `MAH-F0117:L0001` à la ligne source 367 ; FIN `MAH-F0117:L0006` à la ligne 372. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0118 — `check_journey`

**Rôle :** Exercer le jeu scolaire par les routes réelles sous garde.

**Repère :** [tools/recette_lot6g4.py:384](../../tools/recette_lot6g4.py#L384) ; fonction. Signature : `check_journey(app, application, db, models, credentials)`.

**Paramètres :**

- `app` (positionnel_ou_nomme) : Application Flask existante à configurer ou à utiliser dans un contexte isolé.
- `application` (positionnel_ou_nomme) : Application WSGI composée utilisée par le client de validation.
- `db` (positionnel_ou_nomme) : Extension SQLAlchemy déjà reliée à l’application de test.
- `models` (positionnel_ou_nomme) : Module des modèles chargé dans le périmètre autorisé.
- `credentials` (positionnel_ou_nomme) : Accès fictifs éphémères déjà générés en mémoire ; ne jamais les exporter.

**Fonctionnement :**

- Créer le client WSGI
- inscrire un compte fictif supplémentaire
- vérifier connexion, contributions, rôles et effets en base
- produire un bilan sans valeurs d’accès.

**Retour :** Dictionnaire du bilan du parcours scolaire.

**Effets :** Écrit dans la seule SQLite mémoire du scénario ; aucun serveur ou navigateur lancé.

**Numérotation prévue :** DÉBUT `MAH-F0118:L0001` à la ligne source 384 ; FIN `MAH-F0118:L0088` à la ligne 471. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0119 — `check_journey.request`

**Rôle :** Envoyer une requête WSGI du jeu scolaire.

**Repère :** [tools/recette_lot6g4.py:393](../../tools/recette_lot6g4.py#L393) ; fonction_imbriquee. Signature : `request(method, path, status=200, body=None, token=True)`.

**Paramètres :**

- `method` (positionnel_ou_nomme) : Méthode HTTP que le scénario WSGI doit exercer.
- `path` (positionnel_ou_nomme) : Chemin de fichier sous garde, ou chemin HTTP pour les clients WSGI du kit.
- `status` (positionnel_ou_nomme ; défaut source : `200`) : Statut HTTP attendu ou à renvoyer ; forme WSGI textuelle pour prevent_storage.
- `body` (positionnel_ou_nomme ; défaut source : `None`) : Objet JSON de la requête de test, éventuellement absent.
- `token` (positionnel_ou_nomme ; défaut source : `True`) : Indique si le client doit joindre le jeton CSRF en mémoire.

**Fonctionnement :**

- Ajouter le CSRF quand demandé
- exiger le statut attendu
- ne mémoriser que les métadonnées d’échange.

**Retour :** JSON décodé.

**Effets :** Peut modifier le jeu mémoire selon la route appelée.

**Numérotation prévue :** DÉBUT `MAH-F0119:L0001` à la ligne source 393 ; FIN `MAH-F0119:L0006` à la ligne 398. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0120 — `check_journey.login`

**Rôle :** Authentifier un compte du jeu scolaire.

**Repère :** [tools/recette_lot6g4.py:400](../../tools/recette_lot6g4.py#L400) ; fonction_imbriquee. Signature : `login(name)`.

**Paramètres :**

- `name` (positionnel_ou_nomme) : Nom de variable de configuration ou repère du compte fictif, selon la fonction.

**Fonctionnement :**

- Envoyer les accès de test déjà en mémoire
- retenir le jeton de la réponse dans la fermeture.

**Retour :** None.

**Effets :** Modifie la session du client et la variable csrf ; aucune exportation de valeurs.

**Numérotation prévue :** DÉBUT `MAH-F0120:L0001` à la ligne source 400 ; FIN `MAH-F0120:L0003` à la ligne 402. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0121 — `main`

**Rôle :** Préparer et contrôler une démonstration scolaire isolée.

**Repère :** [tools/recette_lot6g4.py:474](../../tools/recette_lot6g4.py#L474) ; fonction. Signature : `main()`.

**Paramètres explicites :** aucun. La fonction peut utiliser son contexte Flask, des variables du module ou une fermeture ; ses effets et le déroulement le précisent.

**Fonctionnement :**

- Valider les combinaisons d’options et sources
- créer les preuves hors dépôt
- neutraliser la configuration et installer les gardes
- créer la mémoire et exécuter les contrôles
- écouter seulement avec les options autorisées.

**Retour :** None après fin normale.

**Effets :** Création de preuves temporaires et de données mémoire ; installation d’un hook d’audit ; écoute et affichage privé des accès seulement en mode serve.

**Erreurs explicitement levées dans ce corps :** `RuntimeError`, `SystemExit`. Les appels délégués peuvent aussi échouer.

**Numérotation prévue :** DÉBUT `MAH-F0121:L0001` à la ligne source 474 ; FIN `MAH-F0121:L0157` à la ligne 630. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0122 — `main.<lambda>#01`

**Rôle :** Sonder le refus de lecture privée.

**Repère :** [tools/recette_lot6g4.py:508](../../tools/recette_lot6g4.py#L508) ; lambda. Signature : `lambda `.

**Paramètres explicites :** aucun. La fonction peut utiliser son contexte Flask, des variables du module ou une fermeture ; ses effets et le déroulement le précisent.

**Fonctionnement :**

- Demander l’opération interdite au garde ou au point d’accès surveillé.
- Le scénario attend le refus ; cette sonde n’est jamais exécutée par le référentiel.

**Retour :** Pas de succès attendu : exception de refus sous les gardes du kit.

**Effets :** Incrémente le compteur de refus prévu ; le confinement doit empêcher l’effet demandé.

**Numérotation prévue :** DÉBUT `MAH-F0122:L0001` à la ligne source 508 ; FIN `MAH-F0122:L0001` à la ligne 508. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0123 — `main.<lambda>#02`

**Rôle :** Sonder le refus de écriture dans le dépôt.

**Repère :** [tools/recette_lot6g4.py:509](../../tools/recette_lot6g4.py#L509) ; lambda. Signature : `lambda `.

**Paramètres explicites :** aucun. La fonction peut utiliser son contexte Flask, des variables du module ou une fermeture ; ses effets et le déroulement le précisent.

**Fonctionnement :**

- Demander l’opération interdite au garde ou au point d’accès surveillé.
- Le scénario attend le refus ; cette sonde n’est jamais exécutée par le référentiel.

**Retour :** Pas de succès attendu : exception de refus sous les gardes du kit.

**Effets :** Incrémente le compteur de refus prévu ; le confinement doit empêcher l’effet demandé.

**Numérotation prévue :** DÉBUT `MAH-F0123:L0001` à la ligne source 509 ; FIN `MAH-F0123:L0001` à la ligne 509. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0124 — `main.<lambda>#03`

**Rôle :** Sonder le refus de écriture hors preuves.

**Repère :** [tools/recette_lot6g4.py:510](../../tools/recette_lot6g4.py#L510) ; lambda. Signature : `lambda `.

**Paramètres explicites :** aucun. La fonction peut utiliser son contexte Flask, des variables du module ou une fermeture ; ses effets et le déroulement le précisent.

**Fonctionnement :**

- Demander l’opération interdite au garde ou au point d’accès surveillé.
- Le scénario attend le refus ; cette sonde n’est jamais exécutée par le référentiel.

**Retour :** Pas de succès attendu : exception de refus sous les gardes du kit.

**Effets :** Incrémente le compteur de refus prévu ; le confinement doit empêcher l’effet demandé.

**Numérotation prévue :** DÉBUT `MAH-F0124:L0001` à la ligne source 510 ; FIN `MAH-F0124:L0001` à la ligne 510. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0125 — `main.<lambda>#04`

**Rôle :** Sonder le refus de ouverture SQLite fichier.

**Repère :** [tools/recette_lot6g4.py:511](../../tools/recette_lot6g4.py#L511) ; lambda. Signature : `lambda `.

**Paramètres explicites :** aucun. La fonction peut utiliser son contexte Flask, des variables du module ou une fermeture ; ses effets et le déroulement le précisent.

**Fonctionnement :**

- Demander l’opération interdite au garde ou au point d’accès surveillé.
- Le scénario attend le refus ; cette sonde n’est jamais exécutée par le référentiel.

**Retour :** Pas de succès attendu : exception de refus sous les gardes du kit.

**Effets :** Incrémente le compteur de refus prévu ; le confinement doit empêcher l’effet demandé.

**Numérotation prévue :** DÉBUT `MAH-F0125:L0001` à la ligne source 511 ; FIN `MAH-F0125:L0001` à la ligne 511. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0126 — `main.<lambda>#05`

**Rôle :** Sonder le refus de connexion réseau.

**Repère :** [tools/recette_lot6g4.py:512](../../tools/recette_lot6g4.py#L512) ; lambda. Signature : `lambda `.

**Paramètres explicites :** aucun. La fonction peut utiliser son contexte Flask, des variables du module ou une fermeture ; ses effets et le déroulement le précisent.

**Fonctionnement :**

- Demander l’opération interdite au garde ou au point d’accès surveillé.
- Le scénario attend le refus ; cette sonde n’est jamais exécutée par le référentiel.

**Retour :** Pas de succès attendu : exception de refus sous les gardes du kit.

**Effets :** Incrémente le compteur de refus prévu ; le confinement doit empêcher l’effet demandé.

**Numérotation prévue :** DÉBUT `MAH-F0126:L0001` à la ligne source 512 ; FIN `MAH-F0126:L0001` à la ligne 512. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0127 — `main.<lambda>#06`

**Rôle :** Sonder le refus de migration.

**Repère :** [tools/recette_lot6g4.py:513](../../tools/recette_lot6g4.py#L513) ; lambda. Signature : `lambda `.

**Paramètres explicites :** aucun. La fonction peut utiliser son contexte Flask, des variables du module ou une fermeture ; ses effets et le déroulement le précisent.

**Fonctionnement :**

- Demander l’opération interdite au garde ou au point d’accès surveillé.
- Le scénario attend le refus ; cette sonde n’est jamais exécutée par le référentiel.

**Retour :** Pas de succès attendu : exception de refus sous les gardes du kit.

**Effets :** Incrémente le compteur de refus prévu ; le confinement doit empêcher l’effet demandé.

**Numérotation prévue :** DÉBUT `MAH-F0127:L0001` à la ligne source 513 ; FIN `MAH-F0127:L0001` à la ligne 513. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0128 — `main.<lambda>#07`

**Rôle :** Sonder le refus de sous-processus.

**Repère :** [tools/recette_lot6g4.py:514](../../tools/recette_lot6g4.py#L514) ; lambda. Signature : `lambda `.

**Paramètres explicites :** aucun. La fonction peut utiliser son contexte Flask, des variables du module ou une fermeture ; ses effets et le déroulement le précisent.

**Fonctionnement :**

- Demander l’opération interdite au garde ou au point d’accès surveillé.
- Le scénario attend le refus ; cette sonde n’est jamais exécutée par le référentiel.

**Retour :** Pas de succès attendu : exception de refus sous les gardes du kit.

**Effets :** Incrémente le compteur de refus prévu ; le confinement doit empêcher l’effet demandé.

**Numérotation prévue :** DÉBUT `MAH-F0128:L0001` à la ligne source 514 ; FIN `MAH-F0128:L0001` à la ligne 514. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0129 — `main.connect`

**Rôle :** Encadrer toute ouverture SQLite du kit.

**Repère :** [tools/recette_lot6g4.py:544](../../tools/recette_lot6g4.py#L544) ; fonction_imbriquee. Signature : `connect(database, *positional, **options)`.

**Paramètres :**

- `database` (positionnel_ou_nomme) : Chemin SQLite optionnel du contexte persistant, ou nom mémoire dans le connect du kit.
- `positional` (positionnels_supplementaires) : Arguments positionnels complémentaires reçus par un adaptateur ; transmis ou ignorés selon son contrat.
- `options` (nommes_supplementaires) : Arguments nommés complémentaires reçus par un adaptateur ; transmis ou ignorés selon son contrat.

**Fonctionnement :**

- Exiger le nom mémoire
- ouvrir la connexion
- activer les FK
- installer l’interdiction d’ATTACH/DETACH.

**Retour :** Connexion SQLite mémoire.

**Effets :** Aucune ouverture de fichier SQLite autorisée.

**Numérotation prévue :** DÉBUT `MAH-F0129:L0001` à la ligne source 544 ; FIN `MAH-F0129:L0012` à la ligne 555. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0130 — `main.connect.authorize`

**Rôle :** Refuser le rattachement d’une autre SQLite.

**Repère :** [tools/recette_lot6g4.py:550](../../tools/recette_lot6g4.py#L550) ; fonction_imbriquee. Signature : `authorize(action, *unused)`.

**Paramètres :**

- `action` (positionnel_ou_nomme) : Action demandée ; sa signification dépend du contrat : sécurité, SQL ou garde du kit.
- `unused` (positionnels_supplementaires) : Arguments additionnels du callback, non utilisés par le contrôle décrit.

**Fonctionnement :**

- Comparer l’action SQLite à ATTACH et DETACH
- refuser ces deux actions et permettre les autres.

**Retour :** Constante SQLITE_OK, ou exception issue de blocked.

**Effets :** Garde de connexion ; peut incrémenter un compteur et interrompre une opération.

**Numérotation prévue :** DÉBUT `MAH-F0130:L0001` à la ligne source 550 ; FIN `MAH-F0130:L0004` à la ligne 553. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0131 — `main.engine_guard`

**Rôle :** Contrôler un moteur puis déléguer sa connexion.

**Repère :** [tools/recette_lot6g4.py:557](../../tools/recette_lot6g4.py#L557) ; fonction_imbriquee. Signature : `engine_guard(original, engine, *positional, **options)`.

**Paramètres :**

- `original` (positionnel_ou_nomme) : Fonction de connexion originale capturée avant remplacement temporaire.
- `engine` (positionnel_ou_nomme) : Moteur SQLAlchemy dont le pilote, l’URL ou la destination doivent être contrôlés.
- `positional` (positionnels_supplementaires) : Arguments positionnels complémentaires reçus par un adaptateur ; transmis ou ignorés selon son contrat.
- `options` (nommes_supplementaires) : Arguments nommés complémentaires reçus par un adaptateur ; transmis ou ignorés selon son contrat.

**Fonctionnement :**

- Appeler isolation.database
- transmettre le moteur et les arguments à la fonction originale capturée.

**Retour :** Retour de la fonction de connexion d’origine.

**Effets :** Peut ouvrir uniquement une connexion mémoire contrôlée.

**Numérotation prévue :** DÉBUT `MAH-F0131:L0001` à la ligne source 557 ; FIN `MAH-F0131:L0003` à la ligne 559. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0132 — `main.<lambda>#08`

**Rôle :** Neutraliser dotenv dans le kit mémoire.

**Repère :** [tools/recette_lot6g4.py:563](../../tools/recette_lot6g4.py#L563) ; lambda. Signature : `lambda *a, **k`.

**Paramètres :**

- `a` (positionnels_supplementaires) : Arguments positionnels complémentaires reçus par un adaptateur ; transmis ou ignorés selon son contrat.
- `k` (nommes_supplementaires) : Arguments nommés complémentaires reçus par un adaptateur ; transmis ou ignorés selon son contrat.

**Fonctionnement :**

- Accepter les arguments compatibles.
- Renvoyer faux sans charger de fichier.

**Retour :** Booléen False.

**Effets :** Remplacement temporaire du chargeur dotenv.

**Numérotation prévue :** DÉBUT `MAH-F0132:L0001` à la ligne source 563 ; FIN `MAH-F0132:L0001` à la ligne 563. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0133 — `main.<lambda>#09`

**Rôle :** Neutraliser dotenv dans le kit mémoire.

**Repère :** [tools/recette_lot6g4.py:564](../../tools/recette_lot6g4.py#L564) ; lambda. Signature : `lambda *a, **k`.

**Paramètres :**

- `a` (positionnels_supplementaires) : Arguments positionnels complémentaires reçus par un adaptateur ; transmis ou ignorés selon son contrat.
- `k` (nommes_supplementaires) : Arguments nommés complémentaires reçus par un adaptateur ; transmis ou ignorés selon son contrat.

**Fonctionnement :**

- Accepter les arguments compatibles.
- Renvoyer faux sans charger de fichier.

**Retour :** Booléen False.

**Effets :** Remplacement temporaire du chargeur dotenv.

**Numérotation prévue :** DÉBUT `MAH-F0133:L0001` à la ligne source 564 ; FIN `MAH-F0133:L0001` à la ligne 564. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0134 — `main.<lambda>#10`

**Rôle :** Refuser une tentative de base alternative.

**Repère :** [tools/recette_lot6g4.py:565](../../tools/recette_lot6g4.py#L565) ; lambda. Signature : `lambda *a, **k`.

**Paramètres :**

- `a` (positionnels_supplementaires) : Arguments positionnels complémentaires reçus par un adaptateur ; transmis ou ignorés selon son contrat.
- `k` (nommes_supplementaires) : Arguments nommés complémentaires reçus par un adaptateur ; transmis ou ignorés selon son contrat.

**Fonctionnement :**

- Appeler isolation.blocked avec la catégorie prévue.
- Laisser remonter PermissionError.

**Retour :** Aucun retour normal.

**Effets :** Incrémente un compteur ; ne délègue pas à la cible interdite.

**Numérotation prévue :** DÉBUT `MAH-F0134:L0001` à la ligne source 565 ; FIN `MAH-F0134:L0001` à la ligne 565. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0135 — `main.<lambda>#11`

**Rôle :** Passer la connexion SQLAlchemy par le garde mémoire.

**Repère :** [tools/recette_lot6g4.py:567](../../tools/recette_lot6g4.py#L567) ; lambda. Signature : `lambda engine, *a, **k`.

**Paramètres :**

- `engine` (positionnel_ou_nomme) : Moteur SQLAlchemy dont le pilote, l’URL ou la destination doivent être contrôlés.
- `a` (positionnels_supplementaires) : Arguments positionnels complémentaires reçus par un adaptateur ; transmis ou ignorés selon son contrat.
- `k` (nommes_supplementaires) : Arguments nommés complémentaires reçus par un adaptateur ; transmis ou ignorés selon son contrat.

**Fonctionnement :**

- Transmettre la méthode originale et le moteur à engine_guard.
- Propager les arguments et son résultat.

**Retour :** Retour de la connexion originale après contrôle.

**Effets :** Ouverture limitée à SQLite mémoire.

**Numérotation prévue :** DÉBUT `MAH-F0135:L0001` à la ligne source 567 ; FIN `MAH-F0135:L0001` à la ligne 567. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0136 — `main.<lambda>#12`

**Rôle :** Passer la connexion SQLAlchemy par le garde mémoire.

**Repère :** [tools/recette_lot6g4.py:568](../../tools/recette_lot6g4.py#L568) ; lambda. Signature : `lambda engine, *a, **k`.

**Paramètres :**

- `engine` (positionnel_ou_nomme) : Moteur SQLAlchemy dont le pilote, l’URL ou la destination doivent être contrôlés.
- `a` (positionnels_supplementaires) : Arguments positionnels complémentaires reçus par un adaptateur ; transmis ou ignorés selon son contrat.
- `k` (nommes_supplementaires) : Arguments nommés complémentaires reçus par un adaptateur ; transmis ou ignorés selon son contrat.

**Fonctionnement :**

- Transmettre la méthode originale et le moteur à engine_guard.
- Propager les arguments et son résultat.

**Retour :** Retour de la connexion originale après contrôle.

**Effets :** Ouverture limitée à SQLite mémoire.

**Numérotation prévue :** DÉBUT `MAH-F0136:L0001` à la ligne source 568 ; FIN `MAH-F0136:L0001` à la ligne 568. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0137 — `main.<lambda>#13`

**Rôle :** Refuser une tentative de migration.

**Repère :** [tools/recette_lot6g4.py:569](../../tools/recette_lot6g4.py#L569) ; lambda. Signature : `lambda *a, **k`.

**Paramètres :**

- `a` (positionnels_supplementaires) : Arguments positionnels complémentaires reçus par un adaptateur ; transmis ou ignorés selon son contrat.
- `k` (nommes_supplementaires) : Arguments nommés complémentaires reçus par un adaptateur ; transmis ou ignorés selon son contrat.

**Fonctionnement :**

- Appeler isolation.blocked avec la catégorie prévue.
- Laisser remonter PermissionError.

**Retour :** Aucun retour normal.

**Effets :** Incrémente un compteur ; ne délègue pas à la cible interdite.

**Numérotation prévue :** DÉBUT `MAH-F0137:L0001` à la ligne source 569 ; FIN `MAH-F0137:L0001` à la ligne 569. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0138 — `main.<lambda>#14`

**Rôle :** Refuser une tentative de migration.

**Repère :** [tools/recette_lot6g4.py:570](../../tools/recette_lot6g4.py#L570) ; lambda. Signature : `lambda *a, **k`.

**Paramètres :**

- `a` (positionnels_supplementaires) : Arguments positionnels complémentaires reçus par un adaptateur ; transmis ou ignorés selon son contrat.
- `k` (nommes_supplementaires) : Arguments nommés complémentaires reçus par un adaptateur ; transmis ou ignorés selon son contrat.

**Fonctionnement :**

- Appeler isolation.blocked avec la catégorie prévue.
- Laisser remonter PermissionError.

**Retour :** Aucun retour normal.

**Effets :** Incrémente un compteur ; ne délègue pas à la cible interdite.

**Numérotation prévue :** DÉBUT `MAH-F0138:L0001` à la ligne source 570 ; FIN `MAH-F0138:L0001` à la ligne 570. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0139 — `main.<lambda>#15`

**Rôle :** Refuser une tentative de migration.

**Repère :** [tools/recette_lot6g4.py:574](../../tools/recette_lot6g4.py#L574) ; lambda. Signature : `lambda *a, **k`.

**Paramètres :**

- `a` (positionnels_supplementaires) : Arguments positionnels complémentaires reçus par un adaptateur ; transmis ou ignorés selon son contrat.
- `k` (nommes_supplementaires) : Arguments nommés complémentaires reçus par un adaptateur ; transmis ou ignorés selon son contrat.

**Fonctionnement :**

- Appeler isolation.blocked avec la catégorie prévue.
- Laisser remonter PermissionError.

**Retour :** Aucun retour normal.

**Effets :** Incrémente un compteur ; ne délègue pas à la cible interdite.

**Numérotation prévue :** DÉBUT `MAH-F0139:L0001` à la ligne source 574 ; FIN `MAH-F0139:L0001` à la ligne 574. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0140 — `main.QuietHandler.log_request`

**Rôle :** Ne pas journaliser les requêtes du serveur de démonstration.

**Repère :** [tools/recette_lot6g4.py:618](../../tools/recette_lot6g4.py#L618) ; methode. Signature : `log_request(self, *unused)`.

**Paramètres :**

- `self` (positionnel_ou_nomme) : Instance sur laquelle la méthode ou la propriété travaille.
- `unused` (positionnels_supplementaires) : Arguments additionnels du callback, non utilisés par le contrôle décrit.

**Fonctionnement :**

- Accepter les arguments du gestionnaire
- ne rien écrire.

**Retour :** None.

**Effets :** Supprime ce journal de requêtes, sans exporter de cookie.

**Numérotation prévue :** DÉBUT `MAH-F0140:L0001` à la ligne source 618 ; FIN `MAH-F0140:L0002` à la ligne 619. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

### MAH-M014 — `backend/api/v1/views/__init__.py`

Déclarer le Blueprint et enregistrer les vues sous /api/v1.

Aucune définition de fonction ni classe : ce module enregistre le Blueprint et importe ses vues.

### MAH-M015 — `backend/api/v1/views/admin_stories.py`

Routes administratives de lecture, archivage, restauration et orchestration de la purge.


#### MAH-F0141 — `archive_admin_required`

**Rôle :** Protéger une vue de gestion et encadrer les erreurs SQL de permission.

**Repère :** [backend/api/v1/views/admin_stories.py:16](../../backend/api/v1/views/admin_stories.py#L16) ; fonction. Signature : `archive_admin_required(view)`.

**Paramètres :**

- `view` (positionnel_ou_nomme) : Vue Flask à protéger avant délégation.

**Fonctionnement :**

- Appliquer admin_required à la vue
- définir un wrapper qui intercepte aussi les erreurs SQL survenues pendant la relecture du rôle.

**Retour :** Fonction décorée wrapped.

**Effets :** Ne donne aucun rôle au client ; ajoute une réponse d’erreur administrative homogène.

**Numérotation prévue :** DÉBUT `MAH-F0141:L0001` à la ligne source 16 ; FIN `MAH-F0141:L0013` à la ligne 28. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0142 — `archive_admin_required.wrapped`

**Rôle :** Déléguer à la vue sécurisée sans exposer une erreur SQL du contrôle.

**Repère :** [backend/api/v1/views/admin_stories.py:20](../../backend/api/v1/views/admin_stories.py#L20) ; fonction_imbriquee. Signature : `wrapped(*args, **kwargs)`.

**Paramètres :**

- `args` (positionnels_supplementaires) : Arguments positionnels complémentaires reçus par un adaptateur ; transmis ou ignorés selon son contrat.
- `kwargs` (nommes_supplementaires) : Arguments nommés complémentaires reçus par un adaptateur ; transmis ou ignorés selon son contrat.

**Fonctionnement :**

- Appeler secured dans un bloc try
- intercepter SQLAlchemyError
- effectuer rollback et retourner l’erreur générique 500.

**Retour :** Réponse de la vue sécurisée, refus de permission ou réponse JSON 500.

**Effets :** Lectures de permission et effets éventuels de la vue ; rollback si la relecture ou la vue échoue.

**Numérotation prévue :** DÉBUT `MAH-F0142:L0001` à la ligne source 19 ; FIN `MAH-F0142:L0009` à la ligne 27. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0143 — `admin_story_data`

**Rôle :** Préparer la représentation administrative d’un dossier.

**Repère :** [backend/api/v1/views/admin_stories.py:31](../../backend/api/v1/views/admin_stories.py#L31) ; fonction. Signature : `admin_story_data(story)`.

**Paramètres :**

- `story` (positionnel_ou_nomme) : Objet ou dictionnaire du dossier relu, selon le contrat.

**Fonctionnement :**

- Reprendre la sérialisation du dossier
- ajouter ses informations de gestion et archivage prévues.

**Retour :** Dictionnaire JSON sérialisable.

**Effets :** Lecture des attributs ; aucune suppression.

**Numérotation prévue :** DÉBUT `MAH-F0143:L0001` à la ligne source 31 ; FIN `MAH-F0143:L0009` à la ligne 39. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0144 — `protect_admin_story_cache`

**Rôle :** Interdire le stockage des réponses de gestion.

**Repère :** [backend/api/v1/views/admin_stories.py:43](../../backend/api/v1/views/admin_stories.py#L43) ; fonction. Signature : `protect_admin_story_cache(response)`.

**Paramètres :**

- `response` (positionnel_ou_nomme) : Réponse Flask dont les en-têtes peuvent être adaptés.

**Fonctionnement :**

- Reconnaître les chemins administratifs visés
- ajouter Cache-Control no-store
- renvoyer la réponse.

**Retour :** Objet Response.

**Effets :** Modifie seulement les en-têtes des réponses concernées.

**Numérotation prévue :** DÉBUT `MAH-F0144:L0001` à la ligne source 42 ; FIN `MAH-F0144:L0006` à la ligne 47. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0145 — `get_admin_stories`

**Rôle :** Lister les dossiers pour leur gestion.

**Repère :** [backend/api/v1/views/admin_stories.py:52](../../backend/api/v1/views/admin_stories.py#L52) ; fonction. Signature : `get_admin_stories()`.

**Paramètres explicites :** aucun. La fonction peut utiliser son contexte Flask, des variables du module ou une fermeture ; ses effets et le déroulement le précisent.

**Fonctionnement :**

- Vérifier les paramètres de lecture prévus
- rechercher et ordonner les dossiers selon le contrat
- sérialiser les résultats et gérer une erreur SQL.

**Retour :** Réponse JSON avec statut 200 ou erreur.

**Effets :** Lectures SQL sous permission administrateur.

**Numérotation prévue :** DÉBUT `MAH-F0145:L0001` à la ligne source 50 ; FIN `MAH-F0145:L0017` à la ligne 66. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0146 — `get_admin_story`

**Rôle :** Lire un dossier administratif par identifiant.

**Repère :** [backend/api/v1/views/admin_stories.py:71](../../backend/api/v1/views/admin_stories.py#L71) ; fonction. Signature : `get_admin_story(story_id)`.

**Paramètres :**

- `story_id` (positionnel_ou_nomme) : Identifiant entier du dossier visé, borné avant requête selon le parcours.

**Fonctionnement :**

- Valider l’identifiant
- rechercher le dossier même archivé selon ce parcours
- sérialiser ou refuser l’absence.

**Retour :** Réponse JSON, ou erreur 404/500.

**Effets :** Lectures SQL ; pas de changement d’archivage.

**Numérotation prévue :** DÉBUT `MAH-F0146:L0001` à la ligne source 69 ; FIN `MAH-F0146:L0021` à la ligne 89. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0147 — `set_story_archive`

**Rôle :** Réaliser la transition archive/restauration.

**Repère :** [backend/api/v1/views/admin_stories.py:92](../../backend/api/v1/views/admin_stories.py#L92) ; fonction. Signature : `set_story_archive(story_id, *, archived)`.

**Paramètres :**

- `story_id` (positionnel_ou_nomme) : Identifiant entier du dossier visé, borné avant requête selon le parcours.
- `archived` (nomme_seul) : État d’archivage demandé ; vrai pour retirer, faux pour restaurer.

**Fonctionnement :**

- Valider et verrouiller le dossier
- comparer son état
- modifier archived_at et la révision si nécessaire
- confirmer la transaction et traiter les erreurs.

**Retour :** Réponse JSON avec état et indicateur de changement, ou erreur.

**Effets :** UPDATE et commit possibles ; ne supprime aucune contribution.

**Numérotation prévue :** DÉBUT `MAH-F0147:L0001` à la ligne source 92 ; FIN `MAH-F0147:L0021` à la ligne 112. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0148 — `archive_story`

**Rôle :** Demander l’archivage du dossier.

**Repère :** [backend/api/v1/views/admin_stories.py:117](../../backend/api/v1/views/admin_stories.py#L117) ; fonction. Signature : `archive_story(story_id)`.

**Paramètres :**

- `story_id` (positionnel_ou_nomme) : Identifiant entier du dossier visé, borné avant requête selon le parcours.

**Fonctionnement :**

- Déléguer à set_story_archive avec archived vrai.

**Retour :** Réponse du helper.

**Effets :** Peut archiver après les contrôles serveur ; aucun effacement.

**Numérotation prévue :** DÉBUT `MAH-F0148:L0001` à la ligne source 115 ; FIN `MAH-F0148:L0004` à la ligne 118. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0149 — `restore_story`

**Rôle :** Demander le retour public d’un dossier archivé.

**Repère :** [backend/api/v1/views/admin_stories.py:123](../../backend/api/v1/views/admin_stories.py#L123) ; fonction. Signature : `restore_story(story_id)`.

**Paramètres :**

- `story_id` (positionnel_ou_nomme) : Identifiant entier du dossier visé, borné avant requête selon le parcours.

**Fonctionnement :**

- Déléguer à set_story_archive avec archived faux.

**Retour :** Réponse du helper.

**Effets :** Peut mettre archived_at à NULL ; ne recrée pas un dossier supprimé.

**Numérotation prévue :** DÉBUT `MAH-F0149:L0001` à la ligne source 121 ; FIN `MAH-F0149:L0004` à la ligne 124. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0150 — `get_story_deletion_preview`

**Rôle :** Fournir un aperçu contrôlé avant suppression.

**Repère :** [backend/api/v1/views/admin_stories.py:129](../../backend/api/v1/views/admin_stories.py#L129) ; fonction. Signature : `get_story_deletion_preview(story_id)`.

**Paramètres :**

- `story_id` (positionnel_ou_nomme) : Identifiant entier du dossier visé, borné avant requête selon le parcours.

**Fonctionnement :**

- Déléguer l’action deletion_preview au gestionnaire commun d’erreurs.

**Retour :** Réponse HTTP de l’aperçu ou du refus.

**Effets :** Lectures et verrous temporaires ; aucun effacement.

**Numérotation prévue :** DÉBUT `MAH-F0150:L0001` à la ligne source 127 ; FIN `MAH-F0150:L0005` à la ligne 131. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0151 — `confirm_story_deletion`

**Rôle :** Valider les confirmations explicites d’une suppression.

**Repère :** [backend/api/v1/views/admin_stories.py:136](../../backend/api/v1/views/admin_stories.py#L136) ; fonction. Signature : `confirm_story_deletion(story_id)`.

**Paramètres :**

- `story_id` (positionnel_ou_nomme) : Identifiant entier du dossier visé, borné avant requête selon le parcours.

**Fonctionnement :**

- Déléguer confirm_deletion au gestionnaire commun.

**Retour :** Réponse HTTP avec confirmation ou erreur.

**Effets :** Contrôle de l’état et signature d’une confirmation ; aucune purge à ce stade.

**Numérotation prévue :** DÉBUT `MAH-F0151:L0001` à la ligne source 134 ; FIN `MAH-F0151:L0005` à la ligne 138. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0152 — `delete_story_permanently`

**Rôle :** Exécuter la purge conditionnelle demandée.

**Repère :** [backend/api/v1/views/admin_stories.py:143](../../backend/api/v1/views/admin_stories.py#L143) ; fonction. Signature : `delete_story_permanently(story_id)`.

**Paramètres :**

- `story_id` (positionnel_ou_nomme) : Identifiant entier du dossier visé, borné avant requête selon le parcours.

**Fonctionnement :**

- Déléguer delete_story au gestionnaire commun après les protections de la route.

**Retour :** Réponse HTTP du résultat ou du refus.

**Effets :** Peut supprimer le graphe d’un dossier archivé ; opération irréversible distincte des lectures.

**Numérotation prévue :** DÉBUT `MAH-F0152:L0001` à la ligne source 141 ; FIN `MAH-F0152:L0005` à la ligne 145. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

### MAH-M016 — `backend/api/v1/views/admin_users_support.py`

Sérialisation administrative et bannissement transactionnel des comptes ordinaires.


#### MAH-F0153 — `admin_user_to_dict`

**Rôle :** Ajouter les informations administratives au compte sérialisé.

**Repère :** [backend/api/v1/views/admin_users_support.py:12](../../backend/api/v1/views/admin_users_support.py#L12) ; fonction. Signature : `admin_user_to_dict(user)`.

**Paramètres :**

- `user` (positionnel_ou_nomme) : Compte ORM déjà sélectionné pour la sérialisation administrative.

**Fonctionnement :**

- Reprendre User.to_dict
- ajouter is_banned sous forme booléenne.

**Retour :** Dictionnaire de compte sans hachage.

**Effets :** Lit des attributs ; ne change pas le compte.

**Numérotation prévue :** DÉBUT `MAH-F0153:L0001` à la ligne source 12 ; FIN `MAH-F0153:L0002` à la ligne 13. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0154 — `ban_user_account`

**Rôle :** Suspendre un membre sans supprimer ses données.

**Repère :** [backend/api/v1/views/admin_users_support.py:19](../../backend/api/v1/views/admin_users_support.py#L19) ; fonction. Signature : `ban_user_account(*, user_id=None, username=None)`.

**Paramètres :**

- `user_id` (nomme_seul ; défaut source : `None`) : Identifiant du compte ciblé ou du titulaire du like personnel.
- `username` (nomme_seul ; défaut source : `None`) : Pseudonyme ciblé par le parcours de bannissement ; aucune valeur réelle fournie ici.

**Fonctionnement :**

- Choisir le compte par identifiant ou pseudonyme
- le relire sous verrou
- protéger les administrateurs
- modifier le bannissement et valider ou annuler la transaction.

**Retour :** Réponse JSON et statut du résultat ou du refus.

**Effets :** UPDATE/commit possibles ; aucun effacement ni débannissement.

**Numérotation prévue :** DÉBUT `MAH-F0154:L0001` à la ligne source 19 ; FIN `MAH-F0154:L0034` à la ligne 52. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

### MAH-M017 — `backend/api/v1/views/comments.py`

Lecture et publication de commentaires ; délégation des likes et signalement ciblé.


#### MAH-F0155 — `comment_to_dict`

**Rôle :** Sérialiser un commentaire avec ses likes individuels.

**Repère :** [backend/api/v1/views/comments.py:13](../../backend/api/v1/views/comments.py#L13) ; fonction. Signature : `comment_to_dict(comment)`.

**Paramètres :**

- `comment` (positionnel_ou_nomme) : Commentaire ORM dont les champs ou compteurs doivent être lus.

**Fonctionnement :**

- Reprendre la représentation du commentaire
- déterminer la compatibilité du compteur historique
- fournir le nombre individuel selon le contrat.

**Retour :** Dictionnaire du commentaire.

**Effets :** Peut effectuer un comptage SQL ; n’attribue pas les anciens likes aux comptes.

**Numérotation prévue :** DÉBUT `MAH-F0155:L0001` à la ligne source 13 ; FIN `MAH-F0155:L0014` à la ligne 26. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0156 — `get_story_comments`

**Rôle :** Lire les commentaires d’un dossier actif.

**Repère :** [backend/api/v1/views/comments.py:32](../../backend/api/v1/views/comments.py#L32) ; fonction. Signature : `get_story_comments(story_id)`.

**Paramètres :**

- `story_id` (positionnel_ou_nomme) : Identifiant entier du dossier visé, borné avant requête selon le parcours.

**Fonctionnement :**

- Vérifier l’existence et la visibilité du dossier
- trier les commentaires
- sérialiser la liste et gérer les erreurs.

**Retour :** Réponse JSON et statut 200 ou erreur.

**Effets :** Lectures SQL publiques des contributions du dossier actif.

**Numérotation prévue :** DÉBUT `MAH-F0156:L0001` à la ligne source 29 ; FIN `MAH-F0156:L0022` à la ligne 50. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0157 — `post_story_comment`

**Rôle :** Publier un commentaire sous le compte de session.

**Repère :** [backend/api/v1/views/comments.py:56](../../backend/api/v1/views/comments.py#L56) ; fonction. Signature : `post_story_comment(story_id)`.

**Paramètres :**

- `story_id` (positionnel_ou_nomme) : Identifiant entier du dossier visé, borné avant requête selon le parcours.

**Fonctionnement :**

- Exiger un compte actif et un dossier actif
- valider le texte UTF-8
- utiliser l’identité serveur
- ajouter et valider la contribution.

**Retour :** Réponse JSON et statut 201 ou refus/erreur.

**Effets :** INSERT et commit ; rollback si échec ; le pseudonyme peut être copié dans le commentaire.

**Numérotation prévue :** DÉBUT `MAH-F0157:L0001` à la ligne source 53 ; FIN `MAH-F0157:L0045` à la ligne 97. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0158 — `like_comment`

**Rôle :** Ajouter un like personnel de commentaire.

**Repère :** [backend/api/v1/views/comments.py:103](../../backend/api/v1/views/comments.py#L103) ; fonction. Signature : `like_comment(comment_id)`.

**Paramètres :**

- `comment_id` (positionnel_ou_nomme) : Identifiant entier du commentaire ciblé.

**Fonctionnement :**

- Appeler handle_like avec le type commentaire et l’action add.

**Retour :** Réponse du helper de likes.

**Effets :** Peut créer un lien unique au compte ; aucun simple incrément anonyme.

**Numérotation prévue :** DÉBUT `MAH-F0158:L0001` à la ligne source 100 ; FIN `MAH-F0158:L0006` à la ligne 105. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0159 — `report_comment`

**Rôle :** Signaler le commentaire ciblé.

**Repère :** [backend/api/v1/views/comments.py:111](../../backend/api/v1/views/comments.py#L111) ; fonction. Signature : `report_comment(comment_id)`.

**Paramètres :**

- `comment_id` (positionnel_ou_nomme) : Identifiant entier du commentaire ciblé.

**Fonctionnement :**

- Contrôler compte, cible et dossier actif
- valider le motif
- insérer le signalement et confirmer.

**Retour :** Réponse JSON et statut 201 ou erreur.

**Effets :** INSERT/commit ; ne masque pas automatiquement le commentaire.

**Numérotation prévue :** DÉBUT `MAH-F0159:L0001` à la ligne source 108 ; FIN `MAH-F0159:L0042` à la ligne 149. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

### MAH-M018 — `backend/api/v1/views/histoires.py`

Lecture des dossiers, vote individuel et mises à jour ; contrôles de visibilité.


#### MAH-F0160 — `get_stories`

**Rôle :** Lire les dossiers actifs.

**Repère :** [backend/api/v1/views/histoires.py:14](../../backend/api/v1/views/histoires.py#L14) ; fonction. Signature : `get_stories()`.

**Paramètres explicites :** aucun. La fonction peut utiliser son contexte Flask, des variables du module ou une fermeture ; ses effets et le déroulement le précisent.

**Fonctionnement :**

- Sélectionner les dossiers non archivés
- les trier et sérialiser
- traiter l’erreur SQL prévue.

**Retour :** Réponse JSON de liste et statut 200, ou 500.

**Effets :** Lecture SQL publique ; aucun dossier archivé dans cette liste.

**Numérotation prévue :** DÉBUT `MAH-F0160:L0001` à la ligne source 11 ; FIN `MAH-F0160:L0029` à la ligne 39. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0161 — `get_story_by_slug`

**Rôle :** Retrouver un dossier actif par son slug.

**Repère :** [backend/api/v1/views/histoires.py:44](../../backend/api/v1/views/histoires.py#L44) ; fonction. Signature : `get_story_by_slug(slug)`.

**Paramètres :**

- `slug` (positionnel_ou_nomme) : Identifiant lisible du dossier utilisé dans les URL.

**Fonctionnement :**

- Filtrer sur slug et état actif
- sérialiser le dossier ou signaler l’absence.

**Retour :** Réponse JSON avec statut 200, 404 ou 500.

**Effets :** Lecture SQL ; le slug n’est pas le chemin d’un fichier image.

**Numérotation prévue :** DÉBUT `MAH-F0161:L0001` à la ligne source 42 ; FIN `MAH-F0161:L0019` à la ligne 60. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0162 — `post_story_vote`

**Rôle :** Enregistrer un like unique de dossier.

**Repère :** [backend/api/v1/views/histoires.py:66](../../backend/api/v1/views/histoires.py#L66) ; fonction. Signature : `post_story_vote(story_id)`.

**Paramètres :**

- `story_id` (positionnel_ou_nomme) : Identifiant entier du dossier visé, borné avant requête selon le parcours.

**Fonctionnement :**

- Exiger un compte actif
- verrouiller le dossier actif
- refuser un vote déjà présent
- insérer, compter et valider la transaction.

**Retour :** Réponse JSON, 201 si création, 409 si doublon reconnu, autres refus/erreurs.

**Effets :** INSERT/commit ; rollback après erreur ; contrainte unique protège aussi la concurrence.

**Numérotation prévue :** DÉBUT `MAH-F0162:L0001` à la ligne source 63 ; FIN `MAH-F0162:L0056` à la ligne 118. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0163 — `get_case_updates`

**Rôle :** Lire les mises à jour d’un dossier.

**Repère :** [backend/api/v1/views/histoires.py:124](../../backend/api/v1/views/histoires.py#L124) ; fonction. Signature : `get_case_updates(case_id)`.

**Paramètres :**

- `case_id` (positionnel_ou_nomme) : Identifiant du dossier dont les mises à jour sont demandées.

**Fonctionnement :**

- Vérifier le dossier actif
- chercher et trier les mises à jour rattachées
- sérialiser la réponse.

**Retour :** Réponse JSON et statut 200 ou erreur.

**Effets :** Lectures SQL ; la FK seule ne vérifie pas la catégorie Cold Case.

**Numérotation prévue :** DÉBUT `MAH-F0163:L0001` à la ligne source 121 ; FIN `MAH-F0163:L0022` à la ligne 142. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

### MAH-M019 — `backend/api/v1/views/index.py`

Signalement compatible, lecture administrative, bannissement et distribution de Swagger.


#### MAH-F0164 — `post_report`

**Rôle :** Enregistrer un signalement via l’entrée générique compatible.

**Repère :** [backend/api/v1/views/index.py:17](../../backend/api/v1/views/index.py#L17) ; fonction. Signature : `post_report()`.

**Paramètres explicites :** aucun. La fonction peut utiliser son contexte Flask, des variables du module ou une fermeture ; ses effets et le déroulement le précisent.

**Fonctionnement :**

- Exiger le compte actif
- valider type, cible et motif
- résoudre un commentaire d’un dossier actif
- créer et valider Report.

**Retour :** Réponse JSON et statut 201 ou erreur.

**Effets :** INSERT/commit ; aucune identité de déclarant stockée dans ce modèle.

**Numérotation prévue :** DÉBUT `MAH-F0164:L0001` à la ligne source 13 ; FIN `MAH-F0164:L0085` à la ligne 97. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0165 — `protect_admin_reports_cache`

**Rôle :** Empêcher le stockage des réponses de signalements privés.

**Repère :** [backend/api/v1/views/index.py:101](../../backend/api/v1/views/index.py#L101) ; fonction. Signature : `protect_admin_reports_cache(response)`.

**Paramètres :**

- `response` (positionnel_ou_nomme) : Réponse Flask dont les en-têtes peuvent être adaptés.

**Fonctionnement :**

- Reconnaître le chemin administratif concerné
- fixer no-store
- renvoyer la réponse.

**Retour :** Objet Response.

**Effets :** Modifie les en-têtes, pas les signalements.

**Numérotation prévue :** DÉBUT `MAH-F0165:L0001` à la ligne source 100 ; FIN `MAH-F0165:L0005` à la ligne 104. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0166 — `get_admin_reports`

**Rôle :** Présenter les signalements et leur contexte aux administrateurs.

**Repère :** [backend/api/v1/views/index.py:110](../../backend/api/v1/views/index.py#L110) ; fonction. Signature : `get_admin_reports()`.

**Paramètres explicites :** aucun. La fonction peut utiliser son contexte Flask, des variables du module ou une fermeture ; ses effets et le déroulement le précisent.

**Fonctionnement :**

- Lire les signalements et les informations de commentaire/dossier nécessaires
- produire la représentation contextualisée.

**Retour :** Réponse JSON administrative et statut 200 ou erreur.

**Effets :** Lectures SQL protégées ; motifs non publiés dans la liste publique.

**Numérotation prévue :** DÉBUT `MAH-F0166:L0001` à la ligne source 107 ; FIN `MAH-F0166:L0026` à la ligne 132. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0167 — `ban_user`

**Rôle :** Conserver l’entrée historique de bannissement par pseudonyme.

**Repère :** [backend/api/v1/views/index.py:139](../../backend/api/v1/views/index.py#L139) ; fonction. Signature : `ban_user(username)`.

**Paramètres :**

- `username` (positionnel_ou_nomme) : Pseudonyme ciblé par le parcours de bannissement ; aucune valeur réelle fournie ici.

**Fonctionnement :**

- Transmettre username au helper de suspension du compte.

**Retour :** Réponse du helper.

**Effets :** Le verbe DELETE de cette route ne supprime pas le compte.

**Numérotation prévue :** DÉBUT `MAH-F0167:L0001` à la ligne source 135 ; FIN `MAH-F0167:L0006` à la ligne 140. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0168 — `ban_user_by_id`

**Rôle :** Bannir un membre par son identifiant.

**Repère :** [backend/api/v1/views/index.py:147](../../backend/api/v1/views/index.py#L147) ; fonction. Signature : `ban_user_by_id(user_id)`.

**Paramètres :**

- `user_id` (positionnel_ou_nomme) : Identifiant du compte ciblé ou du titulaire du like personnel.

**Fonctionnement :**

- Transmettre user_id au helper de suspension.

**Retour :** Réponse du helper.

**Effets :** Peut modifier is_banned après les contrôles du helper.

**Numérotation prévue :** DÉBUT `MAH-F0168:L0001` à la ligne source 143 ; FIN `MAH-F0168:L0006` à la ligne 148. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0169 — `get_swagger_json`

**Rôle :** Distribuer le contrat OpenAPI conservé sur disque.

**Repère :** [backend/api/v1/views/index.py:153](../../backend/api/v1/views/index.py#L153) ; fonction. Signature : `get_swagger_json()`.

**Paramètres explicites :** aucun. La fonction peut utiliser son contexte Flask, des variables du module ou une fermeture ; ses effets et le déroulement le précisent.

**Fonctionnement :**

- Construire le chemin relatif au module
- lire et décoder le JSON
- gérer l’absence du fichier.

**Retour :** Réponse JSON et statut 200 ou 404.

**Effets :** Lecture du fichier de contrat ; n’exécute pas ses opérations.

**Numérotation prévue :** DÉBUT `MAH-F0169:L0001` à la ligne source 150 ; FIN `MAH-F0169:L0012` à la ligne 161. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0170 — `oauth_swagger`

**Rôle :** Afficher la documentation interactive historique.

**Repère :** [backend/api/v1/views/index.py:167](../../backend/api/v1/views/index.py#L167) ; fonction. Signature : `oauth_swagger()`.

**Paramètres explicites :** aucun. La fonction peut utiliser son contexte Flask, des variables du module ou une fermeture ; ses effets et le déroulement le précisent.

**Fonctionnement :**

- Préparer le HTML de Swagger UI
- le rendre avec le contrat local et les ressources CDN déclarées.

**Retour :** HTML rendu.

**Effets :** Le navigateur peut charger cdnjs ; aucune authentification OAuth réalisée malgré le nom de la fonction.

**Numérotation prévue :** DÉBUT `MAH-F0170:L0001` à la ligne source 163 ; FIN `MAH-F0170:L0034` à la ligne 196. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

### MAH-M020 — `backend/api/v1/views/likes.py`

État personnel et retrait des likes ; compatibilité des anciens compteurs et transactions.


#### MAH-F0171 — `legacy_likes_compatible`

**Rôle :** Décider si les likes de commentaire sont attribuables au modèle individuel.

**Repère :** [backend/api/v1/views/likes.py:13](../../backend/api/v1/views/likes.py#L13) ; fonction. Signature : `legacy_likes_compatible(comment)`.

**Paramètres :**

- `comment` (positionnel_ou_nomme) : Commentaire ORM dont les champs ou compteurs doivent être lus.

**Fonctionnement :**

- Exiger un entier de valeur zéro pour le compteur historique.

**Retour :** Booléen.

**Effets :** Aucune remise à zéro ni attribution artificielle.

**Numérotation prévue :** DÉBUT `MAH-F0171:L0001` à la ligne source 13 ; FIN `MAH-F0171:L0004` à la ligne 16. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0172 — `like_state`

**Rôle :** Calculer l’état personnel et le total d’une cible.

**Repère :** [backend/api/v1/views/likes.py:19](../../backend/api/v1/views/likes.py#L19) ; fonction. Signature : `like_state(kind, identifier, user_id)`.

**Paramètres :**

- `kind` (positionnel_ou_nomme) : Catégorie du refus du kit, ou famille story/comment du contrôle des likes.
- `identifier` (positionnel_ou_nomme) : Identifiant de ressource à borner ou résoudre.
- `user_id` (positionnel_ou_nomme) : Identifiant du compte ciblé ou du titulaire du like personnel.

**Fonctionnement :**

- Choisir Vote ou CommentLike
- filtrer par cible
- compter les liens et rechercher celui du compte.

**Retour :** Dictionnaire avec total et liked_by_me.

**Effets :** Lectures SQL uniquement.

**Numérotation prévue :** DÉBUT `MAH-F0172:L0001` à la ligne source 19 ; FIN `MAH-F0172:L0006` à la ligne 24. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0173 — `handle_like`

**Rôle :** Centraliser lecture, ajout et retrait des likes individuels.

**Repère :** [backend/api/v1/views/likes.py:27](../../backend/api/v1/views/likes.py#L27) ; fonction. Signature : `handle_like(kind, identifier, action='read')`.

**Paramètres :**

- `kind` (positionnel_ou_nomme) : Catégorie du refus du kit, ou famille story/comment du contrôle des likes.
- `identifier` (positionnel_ou_nomme) : Identifiant de ressource à borner ou résoudre.
- `action` (positionnel_ou_nomme ; défaut source : `'read'`) : Action demandée ; sa signification dépend du contrat : sécurité, SQL ou garde du kit.

**Fonctionnement :**

- Vérifier compte et cible active
- contrôler la compatibilité historique
- lire ou modifier le lien personnel
- préparer le JSON puis confirmer ou annuler la transaction.

**Retour :** Réponse JSON avec état personnel et statut, ou refus/erreur.

**Effets :** SELECT, INSERT ou DELETE selon l’action ; commit/rollback possibles ; ne répète pas une écriture réseau.

**Erreurs explicitement levées dans ce corps :** `SQLAlchemyError`. Les appels délégués peuvent aussi échouer.

**Numérotation prévue :** DÉBUT `MAH-F0173:L0001` à la ligne source 27 ; FIN `MAH-F0173:L0055` à la ligne 81. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0174 — `personal_story_like`

**Rôle :** Lire ou retirer le like personnel d’un dossier.

**Repère :** [backend/api/v1/views/likes.py:85](../../backend/api/v1/views/likes.py#L85) ; fonction. Signature : `personal_story_like(story_id)`.

**Paramètres :**

- `story_id` (positionnel_ou_nomme) : Identifiant entier du dossier visé, borné avant requête selon le parcours.

**Fonctionnement :**

- Déduire l’action de la méthode HTTP
- déléguer à handle_like pour une cible story.

**Retour :** Réponse du helper.

**Effets :** Lecture ou retrait d’un seul lien au compte selon GET/DELETE.

**Numérotation prévue :** DÉBUT `MAH-F0174:L0001` à la ligne source 84 ; FIN `MAH-F0174:L0003` à la ligne 86. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0175 — `personal_comment_like`

**Rôle :** Lire ou retirer le like personnel d’un commentaire.

**Repère :** [backend/api/v1/views/likes.py:90](../../backend/api/v1/views/likes.py#L90) ; fonction. Signature : `personal_comment_like(comment_id)`.

**Paramètres :**

- `comment_id` (positionnel_ou_nomme) : Identifiant entier du commentaire ciblé.

**Fonctionnement :**

- Déduire l’action de la méthode HTTP
- déléguer à handle_like pour une cible comment.

**Retour :** Réponse du helper.

**Effets :** Lecture ou retrait d’un lien personnel, avec contrôle du dossier actif.

**Numérotation prévue :** DÉBUT `MAH-F0175:L0001` à la ligne source 89 ; FIN `MAH-F0175:L0003` à la ligne 91. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0176 — `protect_personal_likes_cache`

**Rôle :** Protéger le cache des états personnels de likes.

**Repère :** [backend/api/v1/views/likes.py:95](../../backend/api/v1/views/likes.py#L95) ; fonction. Signature : `protect_personal_likes_cache(response)`.

**Paramètres :**

- `response` (positionnel_ou_nomme) : Réponse Flask dont les en-têtes peuvent être adaptés.

**Fonctionnement :**

- Reconnaître les réponses des routes concernées
- ajouter no-store
- renvoyer response.

**Retour :** Objet Response.

**Effets :** Modifie les en-têtes privés seulement.

**Numérotation prévue :** DÉBUT `MAH-F0176:L0001` à la ligne source 94 ; FIN `MAH-F0176:L0006` à la ligne 99. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

### MAH-M021 — `backend/api/v1/views/permissions.py`

Relire le compte, refuser les états interdits et protéger les vues administratives.


#### MAH-F0177 — `get_authenticated_user`

**Rôle :** Relire le compte de la session et refuser les états interdits.

**Repère :** [backend/api/v1/views/permissions.py:10](../../backend/api/v1/views/permissions.py#L10) ; fonction. Signature : `get_authenticated_user()`.

**Paramètres explicites :** aucun. La fonction peut utiliser son contexte Flask, des variables du module ou une fermeture ; ses effets et le déroulement le précisent.

**Fonctionnement :**

- Lire user_id
- rechercher le compte en base
- nettoyer la session si le compte manque ou est banni
- renvoyer compte ou refus.

**Retour :** Couple User et None, ou None et réponse HTTP 401/403.

**Effets :** Lecture SQL ; nettoyage possible de session ; aucun rôle choisi par le client.

**Numérotation prévue :** DÉBUT `MAH-F0177:L0001` à la ligne source 10 ; FIN `MAH-F0177:L0038` à la ligne 47. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0178 — `admin_required`

**Rôle :** Construire un décorateur de permission administrateur.

**Repère :** [backend/api/v1/views/permissions.py:52](../../backend/api/v1/views/permissions.py#L52) ; fonction. Signature : `admin_required(view_function)`.

**Paramètres :**

- `view_function` (positionnel_ou_nomme) : Vue Flask capturée par le décorateur administrateur.

**Fonctionnement :**

- Définir un wrapper conservant les métadonnées de la vue
- renvoyer ce wrapper.

**Retour :** Fonction wrapped_view.

**Effets :** Pas d’appel de la vue lors de la construction du décorateur.

**Numérotation prévue :** DÉBUT `MAH-F0178:L0001` à la ligne source 52 ; FIN `MAH-F0178:L0018` à la ligne 69. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0179 — `admin_required.wrapped_view`

**Rôle :** Contrôler le rôle avant une vue administrative.

**Repère :** [backend/api/v1/views/permissions.py:55](../../backend/api/v1/views/permissions.py#L55) ; fonction_imbriquee. Signature : `wrapped_view(*args, **kwargs)`.

**Paramètres :**

- `args` (positionnels_supplementaires) : Arguments positionnels complémentaires reçus par un adaptateur ; transmis ou ignorés selon son contrat.
- `kwargs` (nommes_supplementaires) : Arguments nommés complémentaires reçus par un adaptateur ; transmis ou ignorés selon son contrat.

**Fonctionnement :**

- Appeler get_authenticated_user
- propager les refus
- exiger is_admin puis déléguer à la vue capturée.

**Retour :** Réponse de refus ou valeur retournée par la vue.

**Effets :** Lecture de compte ; les effets de la vue déléguée dépendent de sa fonction.

**Numérotation prévue :** DÉBUT `MAH-F0179:L0001` à la ligne source 54 ; FIN `MAH-F0179:L0014` à la ligne 67. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

### MAH-M022 — `backend/api/v1/views/proposals.py`

Réception des propositions en attente et lecture réservée aux administrateurs.


#### MAH-F0180 — `proposal_to_dict`

**Rôle :** Préparer les champs JSON d’une proposition.

**Repère :** [backend/api/v1/views/proposals.py:15](../../backend/api/v1/views/proposals.py#L15) ; fonction. Signature : `proposal_to_dict(proposal)`.

**Paramètres :**

- `proposal` (positionnel_ou_nomme) : Objet Proposal à convertir en données JSON.

**Fonctionnement :**

- Lire identifiant, auteur, titre, contenu et statut
- convertir les dates présentes en ISO.

**Retour :** Dictionnaire sérialisable.

**Effets :** Aucun changement de statut ni publication.

**Numérotation prévue :** DÉBUT `MAH-F0180:L0001` à la ligne source 15 ; FIN `MAH-F0180:L0016` à la ligne 30. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0181 — `get_proposals`

**Rôle :** Lire les propositions pour l’administration.

**Repère :** [backend/api/v1/views/proposals.py:36](../../backend/api/v1/views/proposals.py#L36) ; fonction. Signature : `get_proposals()`.

**Paramètres explicites :** aucun. La fonction peut utiliser son contexte Flask, des variables du module ou une fermeture ; ses effets et le déroulement le précisent.

**Fonctionnement :**

- Sélectionner et trier les propositions
- les convertir avec proposal_to_dict.

**Retour :** Réponse JSON et statut 200.

**Effets :** Lecture SQL protégée par admin_required.

**Numérotation prévue :** DÉBUT `MAH-F0181:L0001` à la ligne source 33 ; FIN `MAH-F0181:L0014` à la ligne 46. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0182 — `create_proposal`

**Rôle :** Recevoir une proposition liée au compte connecté.

**Repère :** [backend/api/v1/views/proposals.py:52](../../backend/api/v1/views/proposals.py#L52) ; fonction. Signature : `create_proposal()`.

**Paramètres explicites :** aucun. La fonction peut utiliser son contexte Flask, des variables du module ou une fermeture ; ses effets et le déroulement le précisent.

**Fonctionnement :**

- Exiger le compte actif
- valider le JSON et les textes
- créer Proposal en attente
- valider ou annuler la transaction.

**Retour :** Réponse JSON et statut 201 ou erreur.

**Effets :** INSERT/commit ; ne crée pas de Story et ne publie pas de dossier.

**Numérotation prévue :** DÉBUT `MAH-F0182:L0001` à la ligne source 49 ; FIN `MAH-F0182:L0044` à la ligne 92. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

### MAH-M023 — `backend/api/v1/views/story_deletion_support.py`

Contrôler et purger le graphe d’une archive avec confirmations signées et état relu.

- **MAH-C020 — `PurgeError`**, lignes 27–29 : Exception métier portant message, statut HTTP et code de refus de purge.


#### MAH-F0183 — `PurgeError.__init__`

**Rôle :** Porter une erreur métier de suppression.

**Repère :** [backend/api/v1/views/story_deletion_support.py:28](../../backend/api/v1/views/story_deletion_support.py#L28) ; methode. Signature : `__init__(self, message, status, code)`.

**Paramètres :**

- `self` (positionnel_ou_nomme) : Instance sur laquelle la méthode ou la propriété travaille.
- `message` (positionnel_ou_nomme) : Message constant ou contrôlé destiné à la réponse d’erreur.
- `status` (positionnel_ou_nomme) : Statut HTTP attendu ou à renvoyer ; forme WSGI textuelle pour prevent_storage.
- `code` (positionnel_ou_nomme) : Code métier stable de l’erreur de purge.

**Fonctionnement :**

- Conserver message, statut HTTP et code métier sur l’exception.

**Retour :** None.

**Effets :** Initialise les attributs d’exception sans opération SQL.

**Numérotation prévue :** DÉBUT `MAH-F0183:L0001` à la ligne source 28 ; FIN `MAH-F0183:L0002` à la ligne 29. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0184 — `fail`

**Rôle :** Interrompre une purge avec une erreur métier déterminée.

**Repère :** [backend/api/v1/views/story_deletion_support.py:32](../../backend/api/v1/views/story_deletion_support.py#L32) ; fonction. Signature : `fail(message, status=409, code='DELETE_CONDITIONS_NOT_MET')`.

**Paramètres :**

- `message` (positionnel_ou_nomme) : Message constant ou contrôlé destiné à la réponse d’erreur.
- `status` (positionnel_ou_nomme ; défaut source : `409`) : Statut HTTP attendu ou à renvoyer ; forme WSGI textuelle pour prevent_storage.
- `code` (positionnel_ou_nomme ; défaut source : `'DELETE_CONDITIONS_NOT_MET'`) : Code métier stable de l’erreur de purge.

**Fonctionnement :**

- Construire PurgeError avec les paramètres
- lever cette exception.

**Retour :** Aucun retour normal.

**Effets :** Interrompt le contrôle ; l’appelant doit effectuer le rollback prévu.

**Erreurs explicitement levées dans ce corps :** `PurgeError`. Les appels délégués peuvent aussi échouer.

**Numérotation prévue :** DÉBUT `MAH-F0184:L0001` à la ligne source 32 ; FIN `MAH-F0184:L0002` à la ligne 33. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0185 — `signer`

**Rôle :** Créer le sérialiseur des confirmations de suppression.

**Repère :** [backend/api/v1/views/story_deletion_support.py:36](../../backend/api/v1/views/story_deletion_support.py#L36) ; fonction. Signature : `signer()`.

**Paramètres explicites :** aucun. La fonction peut utiliser son contexte Flask, des variables du module ou une fermeture ; ses effets et le déroulement le précisent.

**Fonctionnement :**

- Utiliser la clé de l’application avec le sel dédié et SHA-256.

**Retour :** Sérialiseur URLSafeTimedSerializer.

**Effets :** Lit la clé en contexte Flask ; ne pas exporter sa valeur.

**Numérotation prévue :** DÉBUT `MAH-F0185:L0001` à la ligne source 36 ; FIN `MAH-F0185:L0003` à la ligne 38. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0186 — `session_binding`

**Rôle :** Lier une confirmation à la session courante.

**Repère :** [backend/api/v1/views/story_deletion_support.py:41](../../backend/api/v1/views/story_deletion_support.py#L41) ; fonction. Signature : `session_binding()`.

**Paramètres explicites :** aucun. La fonction peut utiliser son contexte Flask, des variables du module ou une fermeture ; ses effets et le déroulement le précisent.

**Fonctionnement :**

- Lire le jeton CSRF
- en calculer une empreinte SHA-256.

**Retour :** Chaîne d’empreinte.

**Effets :** Aucun jeton brut ajouté aux confirmations ou journaux.

**Numérotation prévue :** DÉBUT `MAH-F0186:L0001` à la ligne source 41 ; FIN `MAH-F0186:L0003` à la ligne 43. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0187 — `load_token`

**Rôle :** Vérifier une confirmation signée et sa validité.

**Repère :** [backend/api/v1/views/story_deletion_support.py:46](../../backend/api/v1/views/story_deletion_support.py#L46) ; fonction. Signature : `load_token(value, purpose)`.

**Paramètres :**

- `value` (positionnel_ou_nomme) : Valeur à convertir ou valider selon le contrat de cette fonction.
- `purpose` (positionnel_ou_nomme) : Usage attendu de la confirmation signée, aperçu ou suppression.

**Fonctionnement :**

- Contrôler présence, type et longueur
- vérifier signature et âge
- comparer usage, compte, session et expiration.

**Retour :** Dictionnaire de revendications validé.

**Effets :** Peut lever PurgeError ; aucune suppression à ce stade.

**Numérotation prévue :** DÉBUT `MAH-F0187:L0001` à la ligne source 46 ; FIN `MAH-F0187:L0017` à la ligne 62. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0188 — `lock_actor`

**Rôle :** Exiger et verrouiller l’administrateur de la purge.

**Repère :** [backend/api/v1/views/story_deletion_support.py:65](../../backend/api/v1/views/story_deletion_support.py#L65) ; fonction. Signature : `lock_actor()`.

**Paramètres explicites :** aucun. La fonction peut utiliser son contexte Flask, des variables du module ou une fermeture ; ses effets et le déroulement le précisent.

**Fonctionnement :**

- Relire le compte courant avec demande de verrou
- refuser absence, bannissement ou rôle non administrateur.

**Retour :** Objet User autorisé.

**Effets :** Lecture SQL avec verrou selon le moteur ; aucune élévation de privilège.

**Numérotation prévue :** DÉBUT `MAH-F0188:L0001` à la ligne source 65 ; FIN `MAH-F0188:L0007` à la ligne 71. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0189 — `require_integrity`

**Rôle :** Refuser une purge sur un moteur ou schéma non vérifié.

**Repère :** [backend/api/v1/views/story_deletion_support.py:74](../../backend/api/v1/views/story_deletion_support.py#L74) ; fonction. Signature : `require_integrity()`.

**Paramètres explicites :** aucun. La fonction peut utiliser son contexte Flask, des variables du module ou une fermeture ; ses effets et le déroulement le précisent.

**Fonctionnement :**

- Contrôler FK actives et moteur pris en charge
- inspecter colonnes et cascades
- chercher les références orphelines.

**Retour :** None si les conditions sont réunies.

**Effets :** Lectures SQL et métadonnées ; refus sans réparation automatique.

**Numérotation prévue :** DÉBUT `MAH-F0189:L0001` à la ligne source 74 ; FIN `MAH-F0189:L0042` à la ligne 115. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0190 — `snapshot`

**Rôle :** Relever le dossier et son graphe pour les confirmations.

**Repère :** [backend/api/v1/views/story_deletion_support.py:118](../../backend/api/v1/views/story_deletion_support.py#L118) ; fonction. Signature : `snapshot(story_id, *, lock=True)`.

**Paramètres :**

- `story_id` (positionnel_ou_nomme) : Identifiant entier du dossier visé, borné avant requête selon le parcours.
- `lock` (nomme_seul ; défaut source : `True`) : Demande un verrou de lecture/écriture approprié à la requête lorsque vrai.

**Fonctionnement :**

- Valider l’identifiant
- lire dossier et révision avec verrous optionnels
- charger les familles dépendantes dans les limites
- calculer l’empreinte canonique du graphe.

**Retour :** Triplet dossier, graphe, empreinte.

**Effets :** Lectures SQL et verrous éventuels ; textes conservés en mémoire, jamais dans un reçu persistant.

**Numérotation prévue :** DÉBUT `MAH-F0190:L0001` à la ligne source 118 ; FIN `MAH-F0190:L0034` à la ligne 151. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0191 — `snapshot.<lambda>#01`

**Rôle :** Sérialiser une date du graphe pour son empreinte canonique.

**Repère :** [backend/api/v1/views/story_deletion_support.py:150](../../backend/api/v1/views/story_deletion_support.py#L150) ; lambda. Signature : `lambda value`.

**Paramètres :**

- `value` (positionnel_ou_nomme) : Valeur à convertir ou valider selon le contrat de cette fonction.

**Fonctionnement :**

- Recevoir une valeur non directement sérialisable par json.dumps.
- Appeler sa méthode isoformat.

**Retour :** Chaîne ISO de la valeur date.

**Effets :** Conversion en mémoire ; ne rend pas public le graphe.

**Numérotation prévue :** DÉBUT `MAH-F0191:L0001` à la ligne source 150 ; FIN `MAH-F0191:L0001` à la ligne 150. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0192 — `ensure_archive`

**Rôle :** Exiger un dossier déjà archivé avant purge.

**Repère :** [backend/api/v1/views/story_deletion_support.py:154](../../backend/api/v1/views/story_deletion_support.py#L154) ; fonction. Signature : `ensure_archive(story)`.

**Paramètres :**

- `story` (positionnel_ou_nomme) : Objet ou dictionnaire du dossier relu, selon le contrat.

**Fonctionnement :**

- Vérifier archived_at
- refuser NULL.

**Retour :** None ou PurgeError.

**Effets :** Aucune modification de dossier.

**Numérotation prévue :** DÉBUT `MAH-F0192:L0001` à la ligne source 154 ; FIN `MAH-F0192:L0003` à la ligne 156. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0193 — `check_state`

**Rôle :** Comparer une confirmation à l’état relu.

**Repère :** [backend/api/v1/views/story_deletion_support.py:159](../../backend/api/v1/views/story_deletion_support.py#L159) ; fonction. Signature : `check_state(data, story_id, story, digest)`.

**Paramètres :**

- `data` (positionnel_ou_nomme) : Dictionnaire décodé ou revendications déjà chargées, selon la validation.
- `story_id` (positionnel_ou_nomme) : Identifiant entier du dossier visé, borné avant requête selon le parcours.
- `story` (positionnel_ou_nomme) : Objet ou dictionnaire du dossier relu, selon le contrat.
- `digest` (positionnel_ou_nomme) : Empreinte calculée de l’état courant à comparer à une confirmation.

**Fonctionnement :**

- Comparer identifiant, révision et empreinte attendus aux valeurs courantes
- refuser une confirmation périmée.

**Retour :** None ou PurgeError.

**Effets :** Validation en mémoire des éléments relus.

**Numérotation prévue :** DÉBUT `MAH-F0193:L0001` à la ligne source 159 ; FIN `MAH-F0193:L0004` à la ligne 162. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0194 — `strict_confirmation_json`

**Rôle :** Valider strictement le corps de confirmation.

**Repère :** [backend/api/v1/views/story_deletion_support.py:165](../../backend/api/v1/views/story_deletion_support.py#L165) ; fonction. Signature : `strict_confirmation_json()`.

**Paramètres explicites :** aucun. La fonction peut utiliser son contexte Flask, des variables du module ou une fermeture ; ses effets et le déroulement le précisent.

**Fonctionnement :**

- Borner le corps JSON
- refuser les clés dupliquées
- exiger exactement les champs attendus et l’accord explicite.

**Retour :** Dictionnaire de confirmation validé.

**Effets :** Lit le corps de requête ; aucune modification SQL.

**Numérotation prévue :** DÉBUT `MAH-F0194:L0001` à la ligne source 165 ; FIN `MAH-F0194:L0021` à la ligne 185. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0195 — `strict_confirmation_json.unique`

**Rôle :** Détecter les clés JSON dupliquées.

**Repère :** [backend/api/v1/views/story_deletion_support.py:166](../../backend/api/v1/views/story_deletion_support.py#L166) ; fonction_imbriquee. Signature : `unique(pairs)`.

**Paramètres :**

- `pairs` (positionnel_ou_nomme) : Liste des couples JSON avant construction d’un dictionnaire sans doublon.

**Fonctionnement :**

- Parcourir les couples décodés
- refuser une clé déjà rencontrée
- construire le dictionnaire.

**Retour :** Dictionnaire des couples, ou ValueError.

**Effets :** Transformation en mémoire utilisée par json.loads.

**Erreurs explicitement levées dans ce corps :** `ValueError`. Les appels délégués peuvent aussi échouer.

**Numérotation prévue :** DÉBUT `MAH-F0195:L0001` à la ligne source 166 ; FIN `MAH-F0195:L0007` à la ligne 172. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0196 — `deletion_preview`

**Rôle :** Préparer un aperçu signé de l’impact d’une purge.

**Repère :** [backend/api/v1/views/story_deletion_support.py:188](../../backend/api/v1/views/story_deletion_support.py#L188) ; fonction. Signature : `deletion_preview(story_id)`.

**Paramètres :**

- `story_id` (positionnel_ou_nomme) : Identifiant entier du dossier visé, borné avant requête selon le parcours.

**Fonctionnement :**

- Contrôler acteur et intégrité
- relever le graphe archivé
- signer les éléments d’état et produire l’impact
- libérer les verrous par rollback.

**Retour :** Réponse JSON et statut 200.

**Effets :** Lectures SQL et signature ; rollback de fin de lecture ; aucune suppression.

**Numérotation prévue :** DÉBUT `MAH-F0196:L0001` à la ligne source 188 ; FIN `MAH-F0196:L0013` à la ligne 200. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0197 — `confirm_deletion`

**Rôle :** Transformer un aperçu valide en confirmation de suppression.

**Repère :** [backend/api/v1/views/story_deletion_support.py:203](../../backend/api/v1/views/story_deletion_support.py#L203) ; fonction. Signature : `confirm_deletion(story_id)`.

**Paramètres :**

- `story_id` (positionnel_ou_nomme) : Identifiant entier du dossier visé, borné avant requête selon le parcours.

**Fonctionnement :**

- Valider le JSON et l’aperçu signé
- relire l’état protégé
- comparer le titre exact
- signer l’usage delete avec l’expiration initiale
- libérer les verrous.

**Retour :** Réponse JSON et statut 200.

**Effets :** Lectures, signature et rollback ; aucun renouvellement implicite de la durée de confirmation.

**Numérotation prévue :** DÉBUT `MAH-F0197:L0001` à la ligne source 203 ; FIN `MAH-F0197:L0015` à la ligne 217. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0198 — `delete_story`

**Rôle :** Supprimer atomiquement le graphe d’un dossier archivé confirmé.

**Repère :** [backend/api/v1/views/story_deletion_support.py:220](../../backend/api/v1/views/story_deletion_support.py#L220) ; fonction. Signature : `delete_story(story_id)`.

**Paramètres :**

- `story_id` (positionnel_ou_nomme) : Identifiant entier du dossier visé, borné avant requête selon le parcours.

**Fonctionnement :**

- Exiger les en-têtes et l’absence de corps
- revalider acteur, schéma, signature et empreinte
- réserver la révision
- supprimer les familles dans l’ordre et vérifier les comptes
- confirmer la transaction.

**Retour :** Réponse JSON de succès 200, ou état de commit incertain 503 ; autres refus remontent au gestionnaire.

**Effets :** UPDATE et DELETE transactionnels ; ne supprime pas les comptes ; un accusé de commit perdu ne justifie pas de réémettre DELETE.

**Numérotation prévue :** DÉBUT `MAH-F0198:L0001` à la ligne source 220 ; FIN `MAH-F0198:L0058` à la ligne 277. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0199 — `run_deletion_action`

**Rôle :** Normaliser les erreurs des trois actions de purge.

**Repère :** [backend/api/v1/views/story_deletion_support.py:280](../../backend/api/v1/views/story_deletion_support.py#L280) ; fonction. Signature : `run_deletion_action(action, story_id)`.

**Paramètres :**

- `action` (positionnel_ou_nomme) : Action demandée ; sa signification dépend du contrat : sécurité, SQL ou garde du kit.
- `story_id` (positionnel_ou_nomme) : Identifiant entier du dossier visé, borné avant requête selon le parcours.

**Fonctionnement :**

- Exécuter action
- intercepter erreurs métier et SQL
- effectuer rollback
- distinguer verrou/concurrence et erreur générique.

**Retour :** Réponse de l’action ou réponse JSON d’erreur avec statut adapté.

**Effets :** Rollback possible ; aucun reçu persistant ni relance automatique ajouté.

**Numérotation prévue :** DÉBUT `MAH-F0199:L0001` à la ligne source 280 ; FIN `MAH-F0199:L0015` à la ligne 294. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

### MAH-M024 — `backend/api/v1/views/story_visibility.py`

Résoudre uniquement les dossiers actifs et demander un verrou si nécessaire.


#### MAH-F0200 — `get_active_story`

**Rôle :** Résoudre un dossier accessible aux parcours publics.

**Repère :** [backend/api/v1/views/story_visibility.py:10](../../backend/api/v1/views/story_visibility.py#L10) ; fonction. Signature : `get_active_story(identifier, *, lock=False)`.

**Paramètres :**

- `identifier` (positionnel_ou_nomme) : Identifiant de ressource à borner ou résoudre.
- `lock` (nomme_seul ; défaut source : `False`) : Demande un verrou de lecture/écriture approprié à la requête lorsque vrai.

**Fonctionnement :**

- Borner l’identifiant
- filtrer sur dossier non archivé
- demander un verrou si lock est vrai.

**Retour :** Objet Story actif ou None.

**Effets :** Lecture SQL et verrou optionnel ; aucune restauration de dossier.

**Numérotation prévue :** DÉBUT `MAH-F0200:L0001` à la ligne source 10 ; FIN `MAH-F0200:L0015` à la ligne 24. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

### MAH-M025 — `backend/api/v1/views/theories.py`

Lecture, publication et compteur historique des théories.


#### MAH-F0201 — `theory_to_dict`

**Rôle :** Sérialiser une théorie sans exposer l’objet ORM.

**Repère :** [backend/api/v1/views/theories.py:14](../../backend/api/v1/views/theories.py#L14) ; fonction. Signature : `theory_to_dict(theory)`.

**Paramètres :**

- `theory` (positionnel_ou_nomme) : Objet Theory à sérialiser.

**Fonctionnement :**

- Sélectionner ses champs et références d’auteur
- convertir la date présente.

**Retour :** Dictionnaire JSON sérialisable.

**Effets :** Lecture des attributs seulement.

**Numérotation prévue :** DÉBUT `MAH-F0201:L0001` à la ligne source 14 ; FIN `MAH-F0201:L0014` à la ligne 27. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0202 — `get_theories`

**Rôle :** Lire les théories d’un dossier actif.

**Repère :** [backend/api/v1/views/theories.py:36](../../backend/api/v1/views/theories.py#L36) ; fonction. Signature : `get_theories(story_id)`.

**Paramètres :**

- `story_id` (positionnel_ou_nomme) : Identifiant entier du dossier visé, borné avant requête selon le parcours.

**Fonctionnement :**

- Vérifier le parent
- sélectionner et ordonner les théories
- sérialiser la liste.

**Retour :** Réponse JSON avec statut 200, ou 404 si dossier absent/archivé.

**Effets :** Lectures SQL publiques ; pas de modération préalable par statut.

**Numérotation prévue :** DÉBUT `MAH-F0202:L0001` à la ligne source 30 ; FIN `MAH-F0202:L0026` à la ligne 55. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0203 — `post_theory`

**Rôle :** Publier une théorie sous le compte courant.

**Repère :** [backend/api/v1/views/theories.py:64](../../backend/api/v1/views/theories.py#L64) ; fonction. Signature : `post_theory(story_id)`.

**Paramètres :**

- `story_id` (positionnel_ou_nomme) : Identifiant entier du dossier visé, borné avant requête selon le parcours.

**Fonctionnement :**

- Contrôler session et dossier actif
- valider titre et contenu
- insérer puis confirmer, avec rollback en cas d’erreur.

**Retour :** Réponse JSON avec statut 201 ou refus/erreur.

**Effets :** INSERT/commit ; aucune publication différée ajoutée.

**Numérotation prévue :** DÉBUT `MAH-F0203:L0001` à la ligne source 58 ; FIN `MAH-F0203:L0055` à la ligne 112. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0204 — `like_theory`

**Rôle :** Conserver le compteur historique de likes de théorie.

**Repère :** [backend/api/v1/views/theories.py:121](../../backend/api/v1/views/theories.py#L121) ; fonction. Signature : `like_theory(theory_id)`.

**Paramètres :**

- `theory_id` (positionnel_ou_nomme) : Identifiant de la théorie dont le compteur historique est modifié.

**Fonctionnement :**

- Exiger le compte actif et le dossier visible
- incrémenter le compteur par la requête prévue
- confirmer ou annuler la transaction.

**Retour :** Réponse JSON et statut du résultat.

**Effets :** UPDATE/commit ; pas d’unicité individuelle comparable à Vote ou CommentLike.

**Numérotation prévue :** DÉBUT `MAH-F0204:L0001` à la ligne source 115 ; FIN `MAH-F0204:L0042` à la ligne 156. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

### MAH-M026 — `backend/api/v1/views/users.py`

Validation du mot de passe, inscription membre et liste administrative des utilisateurs.


#### MAH-F0205 — `is_valid_password`

**Rôle :** Vérifier la politique actuelle des mots de passe.

**Repère :** [backend/api/v1/views/users.py:14](../../backend/api/v1/views/users.py#L14) ; fonction. Signature : `is_valid_password(password)`.

**Paramètres :**

- `password` (positionnel_ou_nomme) : Saisie du mot de passe, réservée à la mémoire et jamais aux journaux.

**Fonctionnement :**

- Tester longueur et présence des familles de caractères prévues
- renvoyer la conformité.

**Retour :** Booléen.

**Effets :** Validation en mémoire ; ne pas enregistrer ni afficher la saisie.

**Numérotation prévue :** DÉBUT `MAH-F0205:L0001` à la ligne source 14 ; FIN `MAH-F0205:L0018` à la ligne 31. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0206 — `get_users`

**Rôle :** Lister les comptes pour l’administration.

**Repère :** [backend/api/v1/views/users.py:37](../../backend/api/v1/views/users.py#L37) ; fonction. Signature : `get_users()`.

**Paramètres explicites :** aucun. La fonction peut utiliser son contexte Flask, des variables du module ou une fermeture ; ses effets et le déroulement le précisent.

**Fonctionnement :**

- Sélectionner les comptes dans l’ordre prévu
- les sérialiser avec leur état de bannissement
- gérer une erreur SQL.

**Retour :** Réponse JSON et statut 200 ou 500.

**Effets :** Lecture SQL privée sous permission administrateur.

**Numérotation prévue :** DÉBUT `MAH-F0206:L0001` à la ligne source 34 ; FIN `MAH-F0206:L0011` à la ligne 44. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0207 — `register_user`

**Rôle :** Créer un membre à partir d’une inscription valide.

**Repère :** [backend/api/v1/views/users.py:50](../../backend/api/v1/views/users.py#L50) ; fonction. Signature : `register_user()`.

**Paramètres explicites :** aucun. La fonction peut utiliser son contexte Flask, des variables du module ou une fermeture ; ses effets et le déroulement le précisent.

**Fonctionnement :**

- Valider JSON, pseudonyme, e-mail et mot de passe
- contrôler unicités
- hacher et créer un membre sans rôle client
- confirmer ou annuler.

**Retour :** Réponse JSON avec statut 201 ou refus/erreur.

**Effets :** INSERT/commit et calcul du hachage ; aucun administrateur créé par le JSON public.

**Numérotation prévue :** DÉBUT `MAH-F0207:L0001` à la ligne source 47 ; FIN `MAH-F0207:L0070` à la ligne 116. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

### MAH-M027 — `backend/api/v1/views/write_support.py`

Validation commune des entrées et reconnaissance limitée des conflits d’unicité.


#### MAH-F0208 — `api_error`

**Rôle :** Construire une erreur API homogène.

**Repère :** [backend/api/v1/views/write_support.py:14](../../backend/api/v1/views/write_support.py#L14) ; fonction. Signature : `api_error(message, status=400)`.

**Paramètres :**

- `message` (positionnel_ou_nomme) : Message constant ou contrôlé destiné à la réponse d’erreur.
- `status` (positionnel_ou_nomme ; défaut source : `400`) : Statut HTTP attendu ou à renvoyer ; forme WSGI textuelle pour prevent_storage.

**Fonctionnement :**

- Assembler statut logique et message
- associer le statut HTTP demandé.

**Retour :** Couple réponse JSON, statut HTTP.

**Effets :** Aucune opération SQL.

**Numérotation prévue :** DÉBUT `MAH-F0208:L0001` à la ligne source 14 ; FIN `MAH-F0208:L0002` à la ligne 15. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0209 — `json_object`

**Rôle :** Exiger un objet JSON de requête.

**Repère :** [backend/api/v1/views/write_support.py:20](../../backend/api/v1/views/write_support.py#L20) ; fonction. Signature : `json_object(optional=False)`.

**Paramètres :**

- `optional` (positionnel_ou_nomme ; défaut source : `False`) : Permet explicitement un corps vide dans json_object lorsque vrai.

**Fonctionnement :**

- Accepter un corps vide seulement si optional
- décoder sans exception de parse exposée
- refuser les autres types.

**Retour :** Couple dictionnaire et None, ou None et erreur HTTP.

**Effets :** Lecture du corps HTTP, sans écriture.

**Numérotation prévue :** DÉBUT `MAH-F0209:L0001` à la ligne source 20 ; FIN `MAH-F0209:L0007` à la ligne 26. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0210 — `required_text`

**Rôle :** Valider et normaliser un texte obligatoire.

**Repère :** [backend/api/v1/views/write_support.py:32](../../backend/api/v1/views/write_support.py#L32) ; fonction. Signature : `required_text(data, field, *, max_length=None, text_column=False, trim=True)`.

**Paramètres :**

- `data` (positionnel_ou_nomme) : Dictionnaire décodé ou revendications déjà chargées, selon la validation.
- `field` (positionnel_ou_nomme) : Nom du champ texte obligatoire dans le dictionnaire reçu.
- `max_length` (nomme_seul ; défaut source : `None`) : Borne optionnelle du nombre de caractères.
- `text_column` (nomme_seul ; défaut source : `False`) : Active la limite du champ TEXT en octets UTF-8.
- `trim` (nomme_seul ; défaut source : `True`) : Autorise le retrait des espaces aux extrémités ; faux conserve la saisie exacte.

**Fonctionnement :**

- Exiger une chaîne non vide
- retirer les espaces seulement si trim
- contrôler longueur en caractères et encodage UTF-8
- borner les octets TEXT si demandé.

**Retour :** Couple texte validé et None, ou None et erreur HTTP.

**Effets :** Transformation en mémoire ; trim faux conserve notamment les espaces significatifs.

**Numérotation prévue :** DÉBUT `MAH-F0210:L0001` à la ligne source 32 ; FIN `MAH-F0210:L0014` à la ligne 45. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0211 — `get_resource`

**Rôle :** Rechercher une ressource après contrôle de son identifiant.

**Repère :** [backend/api/v1/views/write_support.py:50](../../backend/api/v1/views/write_support.py#L50) ; fonction. Signature : `get_resource(model, identifier)`.

**Paramètres :**

- `model` (positionnel_ou_nomme) : Classe du modèle SQLAlchemy à interroger.
- `identifier` (positionnel_ou_nomme) : Identifiant de ressource à borner ou résoudre.

**Fonctionnement :**

- Refuser un entier hors domaine
- appeler db.session.get sur le modèle demandé.

**Retour :** Instance du modèle ou None.

**Effets :** Lecture SQL seulement si l’identifiant est dans le domaine.

**Numérotation prévue :** DÉBUT `MAH-F0211:L0001` à la ligne source 50 ; FIN `MAH-F0211:L0004` à la ligne 53. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

#### MAH-F0212 — `is_unique_conflict`

**Rôle :** Reconnaître un doublon métier sans masquer une autre erreur SQL.

**Repère :** [backend/api/v1/views/write_support.py:59](../../backend/api/v1/views/write_support.py#L59) ; fonction. Signature : `is_unique_conflict(error, *, mysql_keys, sqlite_columns)`.

**Paramètres :**

- `error` (positionnel_ou_nomme) : Erreur transmise par Flask ou SQLAlchemy, à traiter sans exposer ses détails privés.
- `mysql_keys` (nomme_seul) : Noms des seules contraintes MySQL autorisées à être reconnues comme doublons métier.
- `sqlite_columns` (nomme_seul) : Ensembles des seules colonnes SQLite autorisées pour reconnaître les doublons.

**Fonctionnement :**

- Examiner l’erreur d’origine
- distinguer formats MySQL et SQLite
- comparer seulement les clés ou ensembles de colonnes autorisés.

**Retour :** Booléen.

**Effets :** Analyse de l’erreur en mémoire ; aucun accès MySQL nécessaire pour cette reconnaissance.

**Numérotation prévue :** DÉBUT `MAH-F0212:L0001` à la ligne source 59 ; FIN `MAH-F0212:L0030` à la ligne 88. Les conventions traitent les décorateurs, imbrications et exceptions de syntaxe.

## Références complémentaires, sans copie ni exécution

| Fichier | Usage |
|---|---|
| [tools/fixtures/dossiers_historiques.json](../../tools/fixtures/dossiers_historiques.json) | Catalogue approuvé ; ne pas annoter ni modifier les six textes dans ce lot. |
| [tools/recette_lot6g4_sources.json](../../tools/recette_lot6g4_sources.json) | 41 empreintes du kit ; aucune modification ou régénération. |
| [backend/api/v1/swagger.json](../../backend/api/v1/swagger.json) | Contrat OpenAPI à rapprocher des routes, sans exécution des opérations. |
| [migrations/alembic.ini](../../migrations/alembic.ini) | Configuration Alembic ; explications adjacentes, aucune valeur privée ajoutée. |
| [migrations/script.py.mako](../../migrations/script.py.mako) | Gabarit Mako de révision ; ne pas le traiter comme un module Python directement exécutable. |
| [backend/requirements.txt](../../backend/requirements.txt) | Dépendances Python fixées ; aucune installation effectuée. |
| [backend/api/v1/app.py](../../backend/api/v1/app.py) | Réexport de l’application existante ; ne crée pas une deuxième application indépendante. |
| [frontend/api.js](../../frontend/api.js) | Module partagé avec Mélissa ; lecture collective du parcours navigateur, indexation détaillée JavaScript hors du présent périmètre Python. |
| [frontend/app.js](../../frontend/app.js) | Module partagé avec Mélissa ; lecture collective du parcours navigateur, indexation détaillée JavaScript hors du présent périmètre Python. |
| [frontend/comments.js](../../frontend/comments.js) | Module partagé avec Mélissa ; lecture collective du parcours navigateur, indexation détaillée JavaScript hors du présent périmètre Python. |
| [frontend/likes.js](../../frontend/likes.js) | Module partagé avec Mélissa ; lecture collective du parcours navigateur, indexation détaillée JavaScript hors du présent périmètre Python. |
| [frontend/theories-list.js](../../frontend/theories-list.js) | Module partagé avec Mélissa ; lecture collective du parcours navigateur, indexation détaillée JavaScript hors du présent périmètre Python. |
| [frontend/admin-dashboard.js](../../frontend/admin-dashboard.js) | Module partagé avec Mélissa ; lecture collective du parcours navigateur, indexation détaillée JavaScript hors du présent périmètre Python. |
| [frontend/admin-users.js](../../frontend/admin-users.js) | Module partagé avec Mélissa ; lecture collective du parcours navigateur, indexation détaillée JavaScript hors du présent périmètre Python. |
| [frontend/admin-stories.js](../../frontend/admin-stories.js) | Module partagé avec Mélissa ; lecture collective du parcours navigateur, indexation détaillée JavaScript hors du présent périmètre Python. |
| [backend/tests/test_report_migration.py](../../backend/tests/test_report_migration.py) | Tests à lire pour les contraintes et transactions ; aucune nouvelle exécution. |
| [backend/tests/test_comment_likes_migration.py](../../backend/tests/test_comment_likes_migration.py) | Tests à lire pour les contraintes et transactions ; aucune nouvelle exécution. |
| [backend/tests/test_story_archiving.py](../../backend/tests/test_story_archiving.py) | Tests à lire pour les contraintes et transactions ; aucune nouvelle exécution. |
| [backend/tests/test_story_deletion.py](../../backend/tests/test_story_deletion.py) | Tests à lire pour les contraintes et transactions ; aucune nouvelle exécution. |
| [backend/tests/test_likes.py](../../backend/tests/test_likes.py) | Tests à lire pour les contraintes et transactions ; aucune nouvelle exécution. |
| [backend/tests/test_users_votes.py](../../backend/tests/test_users_votes.py) | Tests à lire pour les contraintes et transactions ; aucune nouvelle exécution. |
| [tests/test_demo_persistante.py](../../tests/test_demo_persistante.py) | Tests à lire pour la persistance et l’intégration isolée ; aucune nouvelle exécution. |
| [tests/test_histoires_originales.py](../../tests/test_histoires_originales.py) | Tests à lire pour la persistance et l’intégration isolée ; aucune nouvelle exécution. |
| [tests/test_recette_lot6g4.py](../../tests/test_recette_lot6g4.py) | Tests à lire pour la persistance et l’intégration isolée ; aucune nouvelle exécution. |
| [tests/test_run_local.py](../../tests/test_run_local.py) | Tests à lire pour la persistance et l’intégration isolée ; aucune nouvelle exécution. |

## Périmètre de la suite

Le présent lot fige les identifiants et les responsabilités. Les fiches, index historiques et leurs liens seront traités seulement après les autorisations propres à ces travaux ; les liens vers le README attendent en outre la fin de 6H.19.3. La copie ancienne de `revision_code/mahamadou/backend/models.py` reste conservée comme archive et ne sert pas de modèle courant.

Les copies du futur dossier `docs/soutenance/code-commente-mahamadou/` constituent un lot final distinct. Les JSON, gabarits et fichiers de configuration auront un guide adjacent lorsque des commentaires intégrés ne sont pas permis. Aucun original ne doit être remplacé ou importé depuis les copies pédagogiques.

## Contrôles et limites

La préparation vérifie la couverture des 212 entrées et des 20 classes, les paramètres et emplacements par AST, les 76 paires historiques, les 41 empreintes du kit et les chemins documentaires. Elle n’importe pas l’application et ne teste pas le comportement en production. Les secrets, bases, certificats, clés, sauvegardes et profils de navigateur ne sont pas ouverts.

Le référentiel ne remplace pas une revue pédagogique de chaque explication avant une future copie ligne par ligne. Les numéros de ligne dépendent de l’empreinte source : si le code change, signaler la divergence et réviser le repérage explicitement. Aucun identifiant existant ne doit être silencieusement réattribué.
