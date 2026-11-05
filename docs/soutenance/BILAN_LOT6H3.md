# Lot 6H.3 — finalisation des six remarques du jury

> Archive pédagogique datée : les résultats et descriptions ci-dessous concernent le lot indiqué. Les anciens repères de ligne ne décrivent pas la version candidate. Pour préparer la soutenance actuelle, consulter les quatre fiches et le référentiel reliés au sommaire.

> Copie publique de référence : les chemins personnels et liens de travail internes sont retirés. Les preuves et commandes historiques gardent leur date et leur périmètre ; utiliser le README actuel pour le lancement.

2 novembre 2026. Audit documentaire autorisé après validation de 6H.2. **16 remarques TERMINÉ sur 22 ; six PARTIEL ; aucune nouvelle clôture suffisamment prouvée.** Le décompte exact est **16/22 × 100 = 800/11 % = 72,727272… %, soit 72,73 % arrondi à deux décimales**. Aucun crédit intermédiaire n'est attribué aux lignes partielles.

**GO pour la soutenance scolaire locale dans le périmètre isolé déjà recetté. NO-GO pour les commits de livraison de l'ensemble actuel.** Le premier verdict maintient le résultat fonctionnel de la contre-recette 6G.5 et de l'installation 6H.2 ; il ne certifie ni les droits des images ni une conformité RGPD, et ne signifie pas que les 22 remarques sont terminées. Aucun nouveau lancement n'est effectué ou autorisé par ce rapport.

Références intégralement reprises : [6H.2](BILAN_LOT6H2.md), [6H.1](BILAN_LOT6H1.md), plan de livraison (pièce interne non diffusée), [matrice des 22 remarques](SUIVI_REMARQUES_JURY.md), [6G.4](BILAN_LOT6G4.md), [recette initiale 6G.5](BILAN_LOT6G5.md) et [correctifs/contre-recette 6G.5](BILAN_CORRECTIFS_LOT6G5.md). Les bilans historiques et les manifestes figés sont conservés. La matrice intégrale de 6H.1 reste dans son bilan ; le présent audit ne réécrit pas ce résultat historique.

## 1. Périmètre, Git et sauvegarde vérifiés

Instructions : demande 6H.3, README et procédures de soutenance du dépôt. Aucun `AGENTS.md` trouvé par la recherche dans le dépôt, y compris les fichiers cachés hors `.git` et `.venv`, ni dans les parents accessibles contrôlés. L'énumération de `[chemin local privé retiré]` a été refusée ; aucune absence de consigne dans un emplacement inaccessible n'est certifiée. Aucune élévation n'est nécessaire pour l'audit du projet.

| Élément | État au début de 6H.3 |
|---|---|
| Branche | `feature/frontend-api-integration` |
| HEAD | `07a9f03ea0a3bdad4a07066fdd7bab1997cc158b` |
| Fichiers suivis / suivis modifiés | 66 / 51 |
| Fichiers non suivis, recensés individuellement | 107 |
| Indexés / conflits / suivis malgré une règle d'ignore | 0 / 0 / 0 |
| SHA-256 de l'index | `cc33bbdc5993495735a8c63e85f22f321b05323716ff29b4af3d0fd8df6c5ec3` |

Les modifications et fichiers non suivis préexistants sont conservés, notamment `revision_code/mahamadou/backend/models.py`, distinct du modèle actif. Aucune attribution automatique des changements locaux aux trois étudiants n'est déduite de Git.

La sauvegarde `[chemin local privé retiré]` et la récupération séparée `[chemin local privé retiré]` sont revérifiées en lecture seule :

- **197 fichiers exactement dans chaque dossier**, sans fichier manquant ni supplémentaire : 169 sources, 25 roues Python et trois métadonnées.
- Les **196 entrées hachées** du reçu final correspondent à leur taille et SHA-256 dans les deux copies ; les deux exemplaires du reçu final sont identiques. Le reçu ne prétend pas contenir sa propre empreinte.
- SHA-256 du reçu final relu : `9e1c04fb1f5d9c47bd992631b9aaf6815b3531798f3724e649de2e0e511b8fc7`.
- **169/169 sources courantes identiques à la sauvegarde avant les corrections documentaires 6H.3.** Les cinq images sont comprises dans ce contrôle.

Le script de sauvegarde n'a pas été réexécuté. Aucune nouvelle copie durable, restauration écrasant le projet, écriture dans les sauvegardes ou modification d'ACL. Le contrôle de récupération compare la copie séparée existante ; il ne réinstalle pas le logiciel. Les 115 fichiers de l'ancienne sauvegarde 6E.1 restent la vérification historique de 6H.2, sans nouvelle campagne sur cette archive.

**La réserve de sauvegarde obsolète de 6H.1 est levée pour les sources 6H.2.** Cette archive privée ne sauvegarde ni une base réelle ni l'ensemble de l'historique Git. Elle ne devient pas une sélection publique. Les trois retouches et deux nouveaux livrables documentaires de 6H.3 n'y sont pas ajoutés ; prévoir leur conservation dans une future sauvegarde autorisée, sans écraser 6H.2.

## 2. Les six remarques : état et critères de clôture

Les identifiants et libellés sont exactement ceux de la matrice autorisée. Aucun verbatim supplémentaire du jury n'est inventé. État d'entrée retenu : celui de 6H.2, donc six PARTIEL ; la matrice restée datée 6H.1 affichait encore I-02 NON TRAITÉ.

### H-03 — Houssem : améliorer l'architecture

- **État : PARTIEL → PARTIEL. Nature : documentation et preuve visuelle.** Aucun défaut applicatif supplémentaire établi.
- Déjà réalisé : navigateur/DOM, répartiteur WSGI, middleware statique, Flask, ORM, fichiers et cible SQL sont distingués. Le connecteur est devenu `STATIC → FRONT`, avec « lit les fichiers publics » en 5.1.
- Preuves : [bilan 5.1](BILAN_ETAPE51.md), [support oral](SUPPORT_JURY_LOT6H1.md), code de `run_local.py` ; deux sources d'architecture identiques et connecteur corrigé revérifiés statiquement en 6H.3. Les recettes attestent le service des fichiers, pas la géométrie du diagramme.
- Manque réel : un rendu courant inspecté montrant que le connecteur et son libellé ne se chevauchent plus. Une syntaxe valide ou une capture antérieure à la correction ne suffit pas.
- Correction minimale : rendre la source existante ; ne retoucher que la disposition documentaire si un défaut est effectivement visible. Préciser oralement que le dessin décrit le lanceur normal et ses cibles possibles ; le kit jury utilise SQLite mémoire et le port 5064.
- Fichiers : `README.md`, `docs/soutenance/fiche-commune.md` ; `run_local.py` comme référence de lecture uniquement.
- Clôture vérifiable : archiver rendu et source exacte avec date/empreinte et outil utilisé, inspecter flèches/libellés/responsabilités à la taille de présentation, conserver les deux copies synchronisées. Un futur lancement Edge reste soumis à autorisation distincte.

### H-06 — Houssem : rendre le relationnel lisible

- **État : PARTIEL → PARTIEL. Nature : documentation et preuve visuelle.** Aucune modification de modèle nécessaire démontrée.
- Déjà réalisé : diagramme actualisé en 6H.1 à dix tables et treize relations, incluant `CommentLike`, les deux couples uniques et `management_revision`.
- Preuves : deux blocs ER identiques, dix modèles et treize `ForeignKey` trouvés par AST en 6H.3 ; cohérence des cibles et règles déclarées à la lecture de `backend/models.py`. Le rendu historique à neuf tables ne couvre pas ce modèle actuel.
- Manque réel : preuve de lisibilité des dix entités, des noms/cardinalités et des deux liens `CommentLike → Comment/User`, sans confusion entre unicité d'une colonne et unicité d'un couple.
- Correction minimale : rendre le bloc ER actuel et ajuster uniquement sa présentation en cas de besoin. Garder les modèles comme référence, sans les modifier pour faciliter le dessin.
- Fichiers : `README.md`, `docs/soutenance/fiche-mahamadou.md` ; `backend/models.py` et `migrations/versions/` en lecture seule.
- Clôture vérifiable : comparer le rendu aux dix entités/treize FK et contraintes du code, inspecter la projection à une taille lisible et conserver source/empreinte/rendu datés. Cela ne valide pas le schéma physique MySQL.

### P-01 — Pauline : expliquer le flux de données

- **État : PARTIEL → PARTIEL. Nature : documentation et preuve visuelle.** Le parcours métier n'est pas à redévelopper.
- Déjà réalisé : formulaire → session/CSRF → requête HTTP → contrôles Flask → SQLAlchemy/commit ou rollback → JSON → DOM ; lecture des théories explicitement manuelle. La note finale est scindée en trois lignes avec `<br/>`.
- Preuves : [bilan 5.1](BILAN_ETAPE51.md), copies du diagramme identiques en 6H.3 ; vrais échanges WSGI/HTTP et observations SQL historiques en 6G.5/6H.2. Le contrôle statique retrouve la note corrigée, sans mesurer son cadre.
- Manque réel : rendre la séquence actuelle et vérifier le débordement de la note, les flèches et les branches de refus/transaction.
- Correction minimale : inspecter le rendu existant, ne retoucher la largeur ou le texte documentaire que si nécessaire ; conserver l'absence de répétition automatique du POST et l'actualisation manuelle.
- Fichiers : `README.md`, `docs/soutenance/fiche-commune.md` ; `frontend/api.js`, `frontend/app.js` et `backend/api/v1/views/theories.py` comme références.
- Clôture vérifiable : rendu daté rattaché à l'empreinte de sa source, note entièrement dans son cadre, texte lisible à la taille de présentation, explication orale conforme aux contrôleurs. Aucun test d'API ne remplace cette preuve visuelle.

### C-02 — Fichier privé de comptes de démonstration

- **État : PARTIEL → PARTIEL. Nature : organisation humaine et preuve de disponibilité.** Ce n'est pas un manque d'authentification.
- Déjà réalisé : procédure et modèle de comptes fictifs ; kit générant des mots de passe éphémères à chaque lancement pour les rôles prévus. Connexions membre/admin réellement éprouvées dans les campagnes historiques.
- Preuves : [démonstration](DEMONSTRATION.md), [protocole 6G.4](RECETTE_MANUELLE_LOT6G4.md), [contre-recette 6G.5](BILAN_CORRECTIFS_LOT6G5.md), [installation 6H.2](INSTALLATION_LOT6H2.md) ; génération constatée à la lecture de `seed()` et de l'affichage du kit. Le CSV n'est pas ouvert.
- Manque réel : confirmation d'un détenteur, d'un emplacement privé disponible le jour J et d'une paire d'accès membre/admin correspondant au processus effectivement utilisé. Les mots de passe d'un processus arrêté ne prouvent pas des accès réutilisables.
- Correction minimale : désigner qui lance le kit et relève les accès du nouveau processus, conserver la fiche uniquement dans un support privé, prévoir son renouvellement après redémarrage. Aucun compte permanent ou stockage de mot de passe dans le dépôt à ajouter.
- Fichiers : `docs/soutenance/COMPTES_DEMO.exemple.csv` (contenu non examiné), `docs/soutenance/DEMONSTRATION.md`, `tools/recette_lot6g4.py` ; future fiche privée hors Git.
- Clôture vérifiable : confirmation humaine sans valeur secrète (« fiche privée disponible, détenteur désigné, accès membre/admin correspondant au lancement »), plus preuve de connexion des deux rôles lors d'une recette autorisée. Conserver uniquement date, rôle et réussite. Ne transmettre ni mot de passe ni capture de credentials dans Git ou ce rapport.

### C-07 — Informations RGPD et consentement

- **État : PARTIEL → PARTIEL. Nature : décisions humaines, documentation puis vérification technique ciblée.** Les notices provisoires ne suffisent pas.
- Déjà réalisé : notices sur inscription/théorie/proposition, information sur commentaire/signalement, politique et procédures préparées hors site ; conception de l'effacement distincte de la purge d'un dossier.
- Preuves : [6E.2](BILAN_LOT6E2.md), tests historiques de contrats HTML, douze décisions (pièce interne non diffusée), projet de confidentialité (pièce interne non diffusée), procédure des droits (archive interne non diffusée). La revue actuelle ne trouve pas de validation des décisions indispensables.
- Manque réel : responsable/contact, finalités et bases, durées, hébergement/transferts et organisation effective des droits/copies ; détail en section 5. L'information finale devra aussi couvrir `CommentLike`, ajouté après ces brouillons.
- Correction minimale : faire valider D01 à D12 et compléter les documents ; autoriser ensuite uniquement l'intégration des mentions/liens effectivement finalisés. Ne pas ajouter un consentement général obligatoire ou un outil d'effacement de compte par défaut.
- Fichiers : `frontend/inscription.html`, `theories.html`, `proposer-histoire.html`, `dossier.html`, `comments.js` ; documents `LOT6E1_*`, `document interne non publié` et `PROCEDURE_DROITS_LOT6E2.md`.
- Clôture vérifiable : décisions approuvées, politique sans marqueur indispensable manquant, notices cohérentes et contact accessible hors connexion, puis vérification isolée des pages intégrées sous autorisation ultérieure. La clôture de cette remarque d'information ne certifierait pas tout le site conforme au RGPD.

### I-02 — Provenance et droits des illustrations

- **État : PARTIEL → PARTIEL** après la progression NON TRAITÉ → PARTIEL de 6H.2. **Nature : provenance, justificatifs et décision d'usage.** Aucun problème de service d'image à corriger.
- Déjà réalisé : déclaration de création des quatre WebP par l'équipe avec ChatGPT, registre par fichier, associations de slugs et empreintes ; usage local conservé et fonctionnement statique prouvé.
- Preuves : [registre 6H.2](REGISTRE_IMAGES_LOT6H2.md), [README images](../../frontend/images/README.md), preuve WSGI historique (pièce interne non diffusée) ; cinq fichiers identiques aux copies de sauvegarde revérifiées. Une empreinte garantit l'identité des octets, pas leurs droits.
- Manque réel : opérateur/source et références éventuelles par WebP, conditions applicables à la génération et accord de diffusion ; origine du SVG à établir séparément. L'autorisation de modifier donnée en 6H.2 ne prouve pas l'autorisation publique.
- Correction minimale : attestation écrite de l'équipe reliant chaque nom de fichier à sa provenance et à l'usage prévu, complétée des justificatifs des références éventuelles ; détail en section 4. Aucun remplacement nécessaire démontré tant que cette piste n'est pas instruite.
- Fichiers : les quatre `frontend/images/*.webp`, `frontend/images/default-story.svg`, `frontend/images/README.md`, `docs/soutenance/REGISTRE_IMAGES_LOT6H2.md`.
- Clôture vérifiable : revue par fichier des attestations, entrées/références et conditions ; autorisation explicite pour la destination retenue. Une attestation ne remplace pas une autorisation de tiers qui serait nécessaire. À défaut, un remplacement documenté demanderait une nouvelle autorisation ; aucun original ne doit être supprimé.

## 3. Corrections documentaires effectuées

| Fichier | Correction justifiée |
|---|---|
| `docs/soutenance/SUIVI_REMARQUES_JURY.md` | État courant 6H.3, I-02 PARTIEL déjà acquis en 6H.2, six restes et preuves précisées ; identifiants/libellés et seize lignes TERMINÉ conservés. |
| `README.md` | Installation 6H.2 distinguée d'un autre PC ; 36 opérations/27 chemins au lieu de 32 ; quatre lectures/retraits de likes documentés ; chaîne complétée par `c6g200000001` ; deux unicités manquantes ajoutées. Aucune source Mermaid changée. |
| `docs/soutenance/README.md` | Navigation vers ce bilan, matrice et preuve statique ; deux verdicts et décompte courant. Les sections historiques restent contextualisées. |
| `docs/soutenance/BILAN_LOT6H3.md` | Présent audit, critères de clôture et proposition minimale 6H.4. |
| `docs/soutenance/preuves-lot6h3/verification-statique.json` | Reçu documentaire : sauvegarde, état Git, contrôles statiques et préservation du périmètre. |

Aucun bilan historique, image, modèle, route, migration, code frontend, test, kit ou manifeste figé n'est modifié. Les brouillons RGPD ne sont ni finalisés fictivement ni déplacés vers le frontend. Aucune décision humaine n'est enregistrée comme acquise par ces corrections.

## 4. Images : justificatifs locaux et diffusion publique

Les déclarations antérieures sont conservées dans le registre : création par l'équipe, avec IA puis précision « chat gpt ». L'opérateur individuel, la date et les références fournies ne sont pas identifiés. Ni les métadonnées absentes des WebP ni leur ancien ajout Git ne résolvent ces points.

Le SVG est relu séparément : rectangle, trait et texte « Image à venir », sans mention d'auteur, de source ou de licence. Son ajout Git apparaît dans `e8f8e4c` du 24 octobre 2026 ; cette trace atteste l'introduction du fichier dans le dépôt, pas son auteur créatif ni son autorisation. Sa simplicité visuelle ne suffit pas à inventer un statut juridique.

| Fichier | Provenance disponible | Soutenance scolaire locale | Future diffusion publique |
|---|---|---|---|
| `tableau-salle-bleue.webp` | Équipe via ChatGPT, déclaration 6H.2 | Présentation locale conservée ; provenance IA à annoncer ; justification par fichier incomplète | Accord d'usage public et entrées/références à confirmer |
| `medaille-pavillon-ferme.webp` | Même déclaration | Même réserve | Même réserve |
| `malle-quai-silencieux.webp` | Même déclaration | Même réserve | Même réserve |
| `carnet-tour-nord.webp` | Même déclaration | Même réserve | Même réserve |
| `default-story.svg` | Auteur, outil ou source non confirmés séparément | Repli effectivement utilisé par le kit local ; origine encore à justifier | Obtenir origine et autorisation propres au SVG ; ne pas lui attribuer ChatGPT par déduction |

Pour documenter le dossier scolaire et clore I-02, demander une attestation datée identifiant chaque fichier, le membre/opérateur, l'outil/source, l'usage scolaire et les références éventuelles ou leur absence déclarée. Un extrait de génération/export sans information privée peut corroborer la déclaration ; aucun accès au compte, export complet de conversation ou mot de passe n'est requis. Pour le SVG : préciser création originale ou source tierce, avec justificatif correspondant. Une présentation scolaire n'est pas ici déclarée juridiquement autorisée sur la seule présence des fichiers.

Pour une diffusion publique, compléter l'accord de l'équipe/opérateur pour cette diffusion et identifier les conditions du service réellement applicables au compte, au territoire et à la date de création. Si une entrée ou ressource tierce a été utilisée, conserver sa source, licence/autorisation et obligations éventuelles ; si aucune référence n'a été fournie, le faire attester sans inventer une pièce inexistante. Examiner tout élément identifiable nécessitant des droits supplémentaires selon les images et l'usage prévus.

Les [conditions européennes OpenAI, version du 16 janvier 2026](https://openai.com/policies/eu-terms-of-use/) ont été relues pour cet audit : elles attribuent les droits éventuels d'OpenAI sur les sorties à l'utilisateur dans les limites légales, placent les droits des entrées sous sa responsabilité et ne garantissent pas l'unicité des sorties. Elles distinguent les services individuels des services professionnels. Elles ne constituent donc ni une licence libre ni un justificatif propre à ces fichiers ; leur applicabilité précise reste à établir. Aucune licence CC0/Creative Commons, exclusivité ou autorisation de tiers n'est créée dans ce rapport.

**Statut : cinq originaux conservés, zéro image modifiée ou supprimée ; I-02 PARTIEL ; diffusion publique non validée.** Le GO fonctionnel local n'est pas un certificat de droits, notamment pour le SVG.

## 5. RGPD : décisions humaines encore indispensables

La politique Markdown et la page HTML (pièce interne non diffusée) restent **BROUILLONS INTERNES NON VALIDÉS, NON PUBLIÉS**. L'autorisation du lot 6H.3 ne renseigne aucune identité, durée ou base légale.

| Sujet | Décision/justificatif réellement manquant |
|---|---|
| Responsable — D01 | Identité et coordonnées de la personne/organisation qui décide des traitements ; rôle confirmé de l'école et DPO éventuel. Ne pas désigner automatiquement un étudiant ou Holberton. |
| Contact — D02/D10 | Canal effectivement suivi, opérateurs habilités et réponse sécurisée, accessible sans compte, y compris aux personnes bannies et aux tiers. Ne pas inventer une adresse. |
| Finalités et bases — D03/D04 | Justification par traitement : compte/authentification, contributions, propositions, likes/votes, modération, sécurité et droits. Justifier l'email obligatoire alors que le login utilise le pseudo. Aucun consentement général ni contrat présumé. |
| Conservation — D05/D12 | Durées ou critères précis, point de départ, réexamen/action et responsable pour comptes, textes, archives, Vote/CommentLike, signalements, demandes, logs, sauvegardes et copies. Aucune durée par défaut, aucun délai d'inactivité inventé. |
| Hébergement — D06 | Prestataires réellement retenus, localisation, accès, sous-traitants et garanties contractuelles. Une configuration Aiven dans le code ne prouve pas un hébergement effectif. |
| Transferts — D06/D11 | Inventaire des flux réels, ressources externes et garanties si nécessaire. Ne déclarer ni transfert hors EEE ni absence de transfert sans preuve ; distinguer le kit local bloquant le réseau de la future exploitation. |

D07 reste à valider pour public/mineurs/contenus fictifs ou réels et personnes citées ; D08 pour le devenir des contributions et des pseudonymes copiés ; D09 pour identité proportionnée et anciennes sessions ; D10 pour l'organisation des demandes ; D11 pour configuration effective cookies/HTTPS/caches/journaux/incidents ; D12 pour copies/restauration. Les douze décisions restent non validées dans les pièces examinées.

La future information doit intégrer `CommentLike` et ses deux liens compte/commentaire : les documents 6E antérieurs à cet ajout ne décrivent pas seuls le schéma actuel. Il faut distinguer bannissement, archivage, suppression de dossier et effacement de données d'une personne. Un `user_id=NULL` ne retire ni le pseudonyme copié ni les mentions libres. Aucun portail, bannière de consentement ou effacement automatique n'est requis par défaut pour corriger cette remarque.

La [CNIL — information des personnes](https://www.cnil.fr/fr/informer-les-personnes) rappelle les informations à fournir, notamment identité, finalités, bases, destinataires, conservation et exercice des droits. Ces exigences expliquent le maintien du brouillon ; elles ne déterminent pas les réponses propres au projet. La [CNIL — conservation](https://www.cnil.fr/fr/passer-laction/les-durees-de-conservation-des-donnees), page du 2 avril 2026, rattache les durées à la finalité et au choix justifié du responsable : aucune durée sectorielle n'est transposée automatiquement au portfolio.

**C-07 reste PARTIEL. Le site n'est pas déclaré entièrement conforme au RGPD.** Pour la soutenance retenue, rester sur les comptes et récits synthétiques du dispositif isolé, sans inscription de vraies personnes ni collecte publique improvisée.

## 6. Base de données : risques résiduels examinés sans connexion

La revue utilise uniquement texte et AST ; aucun import de Flask, SQLAlchemy applicatif ou Alembic, aucun moteur SQL, aucune base existante et aucun DDL ne sont exécutés.

| Sujet | Acquis et risque résiduel | Suite minimale si la cible doit être déployée ultérieurement |
|---|---|---|
| Migrations MySQL | Sept révisions, tête unique `c6g200000001`. Quatre anciennes révisions diffèrent du HEAD ; trois candidates sont non suivies. La révision réellement appliquée et le schéma physique sont inconnus. | Revue de l'historique appliqué et du diff, moteurs/types/FK/indices et sauvegarde-restauration de données sous autorisation distincte ; ne pas réécrire une révision déjà appliquée pour forcer une reprise. |
| DDL partiel | Candidate likes : création de table puis d'index. Un échec du second peut laisser `comment_likes` présente ; le précontrôle refuse alors la relance. Le rollback applicatif ne prouve pas le retour du schéma MySQL. | Préparer une procédure de diagnostic/reprise fondée sur l'état constaté ; ne pas supprimer la table, désactiver les FK ou estampiller une révision pour contourner le refus. |
| Anciens compteurs | `Comment.likes` reste physique ; seul `type(value) is int` et `value == 0` est compatible. Valeur positive, négative, NULL ou invalide bloque la candidate et l'API concernée ; aucune attribution possible déduite d'un compteur. | Décision humaine sur tout historique incompatible, sans remise à zéro ni répartition fictive. `Theory.likes` reste un mécanisme historique distinct ; Vote conserve son couple unique. |
| Relations SQLAlchemy | Dix modèles/treize FK déclarés. `Story` utilise `delete-orphan` ; `Comment.moderation_reports` et `Comment.comment_likes` ont CASCADE SQL et cascade ORM/passive_deletes ; `User.comment_likes` possède aussi sa cascade. Les autres collections de User ne sont pas toutes équivalentes. | Ne pas généraliser « toutes les relations User sont sans cascade ». Un simple `Session.delete(User)` demeure insuffisant, notamment avec `Story.author_id` obligatoire ; l'effacement de compte est hors périmètre. |
| Suppression de dossiers | Archive préalable, administrateur actif, CSRF, titre exact, confirmation de cinq minutes, empreinte, révision et `If-Match` ; suppression ciblée et contrôles de nombres. Les likes de commentaires sont inclus dans le graphe interne. | Garder C-05 TERMINÉ dans la portée locale prouvée ; concurrence, verrous et moteur MySQL restent à valider sur une cible de test séparément autorisée. Ne pas ajouter un reçu persistant ou refaire la purge sans défaut établi. |
| Commentaires et signalements | `Report.comment_id` entier obligatoire, FK CASCADE ; type/target_id dérivés, pas de déclarant stocké. La candidate refuse cible non canonique, orpheline ou autre type avant DDL. La purge vérifie FK, moteurs et orphelins Report/CommentLike, puis supprime ces enfants avant les commentaires. | Avant reprise réelle, établir l'état des anciennes cibles et l'intégrité physique ; arrêter les anciens écrivains. Ne jamais réattribuer ou effacer silencieusement les signalements incompatibles. |
| Résultat incertain et intégrité | Commit sans accusé peut laisser un résultat inconnu ; relire sans répéter le DELETE. Absence du dossier sans reçu ne prouve pas l'auteur de la suppression. Schémas neufs SQLite et FK actives attestés historiquement, pas sur MySQL. | Préserver ces limites dans l'oral et la procédure ; aucune suppression réelle pour produire une preuve de soutenance. |

Références : `backend/models.py`, `backend/api/v1/views/likes.py`, `story_deletion_support.py`, migrations `c6c200000001_comment_reports_and_story_revision.py` et `c6g200000001_add_comment_likes.py`, [6C.2](BILAN_LOT6C2_IMPLEMENTATION.md), [6G.2](BILAN_LOT6G2.md), [6G.3](BILAN_LOT6G3.md), [6H.1](BILAN_LOT6H1.md). Les risques de DDL et de concurrence sont ceux documentés et déduits des sources, pas un incident observé sur Aiven pendant ce lot.

## 7. Livraison Git : réserves exactes et exclusions

**Aucun blocage de Git lui-même n'est constaté** : index vide, pas de conflit. Le NO-GO concerne la sélection de livraison de l'ensemble actuel, pas une impossibilité technique de créer un commit local.

| Groupe | État constaté et décision nécessaire |
|---|---|
| Sources/tests/contrats courants | Candidats utiles après revue par liste fermée ; conserver ensemble leurs dépendances. Les 40 sources du kit correspondent encore à son manifeste LF, sans régénération. |
| Quatre WebP et SVG | Tous déjà suivis et inchangés ; la provenance publique n'est pas finalisée. Ne pas les omettre seulement d'un futur ajout en pensant les retirer de l'arbre hérité. Décider attestation ou traitement ultérieur autorisé en conservant les originaux. |
| `frontend/donnees.js` | Déjà suivi, plus chargé par les pages, exclu du kit. Le service normal peut encore servir un JS racine. Revue de contenu/diffusion ou décision sur le suivi encore nécessaire ; aucun contenu relu ici, aucune suppression. |
| `frontend/histoires-originales.json` et CSV de comptes | Non suivis mais **non ignorés** par les règles actuelles ; un ajout global pourrait les inclure. Contenus non ouverts : ne pas les présumer publiables. Décider exclusions explicites ; préserver localement. |
| Sept documents RGPD internes | Brouillons et procédures à conserver en privé ; une inclusion dans une sauvegarde privée n'autorise pas leur diffusion. La politique reste hors site. |
| Rapports, inventaires et preuves | Chemins Windows, noms d'équipe et contexte à revoir pour le destinataire public/privé. Les nouveaux livrables 6H.2/6H.3 ne reçoivent pas automatiquement le lot de commit de l'inventaire 6H.1. Préparer une sélection mise à jour, sans altérer les originaux de preuve. |
| Archives | Ancien kit 6F.2 et copie `revision_code/mahamadou/backend/models.py` à conserver distinctement, sans fusion dans le code actif. Décider leur place dans le livrable. |
| Secrets et fichiers locaux | `.env`, cookies, `certs/`, `.venv/` ignorés ; aucun fichier suivi malgré une règle d'ignore. Bases/dumps, caches et journaux privés restent exclus. Aucun contenu privé lu et aucune certification de tout l'historique Git. |

Le CSV 6H.1 comporte 153 chemins après ses huit ajouts, dont 135 « conserver après revue », sept internes, cinq images à arbitrer, trois archives, deux jeux historiques et un CSV à exclure avant relecture. Il ne couvre pas automatiquement les **173 chemins suivis/non suivis présents au début de 6H.3**, ni les deux nouveaux livrables de ce lot. Le CSV 6H.2 décrit une sélection de sauvegarde, pas une liste Git publiable.

Les anciennes réserves de sauvegarde et d'installation sont levées dans la portée 6H.2 : copie neuve et venv neuf, même PC Windows/Python 3.13 AMD64 ; pas un autre PC, pas une migration existante. Elles ne doivent plus être présentées comme des travaux jamais effectués. Le harnais complet des 854 tests et certaines preuves historiques restent liés à Temp ; ne pas promettre une reproduction sûre par découverte globale depuis le seul HEAD.

La finalisation RGPD et les essais MySQL ne sont pas en eux-mêmes des prérequis à un commit de sources candidates correctement délimité et documenté. Ils conditionnent les usages concernés. Les réserves qui maintiennent le NO-GO de livraison actuel sont **le choix des fichiers hérités, les droits/destinations des images et la revue de diffusion des documents/données**, puis l'autorisation distincte des opérations Git. Aucun commit, push, merge, reset, ajout à l'index, retrait du suivi ou changement de branche n'a été exécuté.

## 8. Contrôles exécutés et limites

Avant exécution, le contrôle a été limité à PowerShell et à un script Python standard exécuté avec `python -I -B` : lecture de chemins déterminés, analyse AST/texte, SHA-256, JSON et commandes Git en lecture seule. Aucun module applicatif importé, aucune découverte automatique de tests, aucune lecture de `.env`/comptes/bases. Les seules écritures auxiliaires sont des reçus/scripts sous Temp et les cinq livrables documentaires listés en section 3. La consultation web des trois sources officielles juridiques est distincte de l'application, sans accès Aiven/MySQL.

| Contrôle 6H.3 | Résultat / portée |
|---|---|
| Sauvegarde et récupération | 197 fichiers chacune ; ensembles, tailles et empreintes conformes, reçus finaux identiques |
| Sources avant édition | 169/169 identiques aux sources sauvegardées |
| Sources après édition | 166/169 identiques ; seules les trois retouches documentaires de la section 3 diffèrent ; deux nouveaux livrables documentaires |
| Kit figé | 40/40 SHA-256 normalisés LF conformes ; aucun import/exécution du kit |
| Modèles, migrations et OpenAPI | Dix modèles, treize FK ; sept révisions, tête unique `c6g200000001` ; 27 chemins/36 opérations |
| Diagrammes | Trois sources canoniques et trois copies identiques ; ER dix tables/treize relations ; connecteur corrigé et note en trois lignes présents ; **aucun nouveau rendu** |
| Matrice | 22 identifiants/libellés conservés, 16 TERMINÉ, six PARTIEL, zéro NON TRAITÉ |
| Liens ajoutés et préservation | Cibles locales des documents modifiés vérifiées ; code, tests, migrations, images et manifestes conservés |
| `git diff --check` par défaut | Code 2, 164 signalements CRLF préexistants dans `backend/api/v1/views/index.py` et `frontend/styles.css` |
| Même contrôle avec `-c core.whitespace=cr-at-eol` pour cette seule commande | Code 0 ; aucune configuration Git ou fin de ligne applicative modifiée |
| État Git final | 51 suivis modifiés, 109 non suivis, zéro indexé/conflit ; branche, HEAD et SHA de l'index inchangés ; aucun fichier préexistant supprimé |

La preuve statique (pièce interne non diffusée) contient les constats, empreintes et limites, sans secret. Les fichiers auxiliaires sont `portfolio-lot6h3-audit-20261102.json` et `portfolio-lot6h3-static-20261102.py/.json` sous Temp ; leur disponibilité future n'est pas garantie. Le contrôle final du périmètre est résumé dans la preuve durable sans lui attribuer sa propre empreinte.

**854 PASS = 311 backend + 513 frontend + 30 contrats/lanceur, référence historique du 1er novembre 2026, non réexécutée.** Aucun contrôle statique n'est ajouté à ce nombre. Les sept anciens tests de migration restent exclus ; les six essais historiques de candidate likes en mémoire ne deviennent pas une validation MySQL. Aucun serveur Flask, écoute locale, Edge ou autre navigateur, nouvelle recette HTTP/WSGI, migration ou installation n'est lancé dans ce lot. Les trois pages officielles consultées ne prouvent aucun rendu du portfolio.

## 9. Proposition minimale pour 6H.4, à autoriser séparément

| Priorité / cible | Action minimale proposée | Condition de réussite |
|---|---|---|
| 1 — H-03/H-06/P-01 | Produire et inspecter les trois rendus des sources actuelles ; ajuster uniquement la documentation si un chevauchement est constaté. Autorisation distincte si Edge doit être lancé. | Trois preuves visuelles datées avec source/empreinte, critères de section 2 satisfaits ; permettrait trois clôtures, donc **19/22 = 950/11 % = 86,363636… %**, seulement après preuve. |
| 2 — C-02 | Confirmer l'organisation du lancement et la fiche privée des accès éphémères membre/admin ; contre-vérifier les deux rôles dans une recette autorisée. | Confirmation sans secret et connexion des rôles correspondant au processus du jour J. Aucun développement de compte supplémentaire. |
| 3 — I-02 / sélection Git | Obtenir les attestations des quatre WebP et l'origine distincte du SVG ; arbitrer les anciens jeux, documents internes, archives et destinataires ; établir une liste Git revue. | Justification par fichier et liste approuvée, originaux conservés. Un remplacement d'image ou retrait du suivi resterait une opération séparée à autoriser. |
| 4 — C-07 | Faire valider D01 à D12 ; intégrer `CommentLike` dans l'inventaire d'information ; finaliser textes/contact puis envisager leur intégration autorisée. | Information cohérente et vérifiée, sans promesse de conformité totale. Aucun ajout automatique de fonctionnalité RGPD. |
| Conditionnel — BDD | Préparer un plan de reprise/test MySQL isolé si une diffusion avec base existante est ensuite demandée, notamment DDL partiel et historiques. | Aucune intervention réelle déduite de cette proposition ; cible, données et autorisations à définir séparément. Pas nécessaire à la soutenance SQLite locale. |

**Aucune correction technique applicative n'est démontrée indispensable à ce stade pour les six lignes.** Ne pas programmer une modification des modèles, routes, likes ou purge « par précaution ». Si les rendus ou une recette ciblée révèlent un défaut réel, le décrire et obtenir l'autorisation correspondante avant correction. Pagination, récupération de mot de passe, nouvelles fonctions de modération et nouveaux compteurs ne sont pas ajoutés au lot proposé.

## 10. Verdicts et arrêt

**GO — soutenance scolaire locale**, sur les parcours synthétiques isolés déjà recettés, avec présentation honnête des trois preuves visuelles restantes, de la fiche privée non confirmée, du brouillon RGPD et des droits incomplets. Préparer les rendus et les accès améliore la préparation du jour J ; aucune validation locale ne doit être présentée comme un GO public, MySQL ou juridique. Le serveur reste non lancé par 6H.3 ; sa prochaine ouverture avec Edge nécessite l'autorisation distincte demandée.

**NO-GO — commits de livraison de l'ensemble actuel**, tant que la sélection et les droits/destinations des ressources et documents ne sont pas arbitrés. Sauvegarde privée et installation locale vérifiées ; blocages restants explicités en section 7. Le manque d'autorisation de commit s'ajoute à ces réserves de préparation, sans être présenté comme un conflit Git.

**Bilan : 16/22 terminées, 72,73 %, six PARTIEL.** Aucune clôture inventée, aucune correction applicative, migration, publication ou opération de livraison Git. **Arrêt après 6H.3 ; attente de la validation de l'utilisateur avant tout lot 6H.4.**
