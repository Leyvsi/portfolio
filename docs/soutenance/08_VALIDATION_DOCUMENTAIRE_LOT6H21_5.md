# Validation documentaire — lot 6H.21.5

Les Petits Enquêteurs — préparation pour Mahamadou — **5 novembre 2026, Europe/Paris**.

**Proposition documentaire externe, sans installation autorisée.** Référence : 203 fichiers de la copie intégrée, vérifiés par empreintes. Aucun module applicatif importé, aucun accès SQL, aucune migration, aucun test applicatif ni intervention sur le serveur 5066. Les exemples sont des illustrations non exécutées, pas des commandes à lancer sur une base réelle. Les responsabilités BDD de Mahamadou sont distinguées des composants partagés avec Sylvie et du frontend de Mélissa.

[Sommaire des huit guides](01_GUIDE_REQUETES_SQLALCHEMY_LOT6H21_5.md#sommaire) · [Références exactes et soutenance](07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md) · [Contrôles et limites](08_VALIDATION_DOCUMENTAIRE_LOT6H21_5.md)

## Verdict et objet de cette validation

**Proposition documentaire validée statiquement ; aucune installation dans un dépôt.** Huit documents sont prêts à examiner. Les contrôles attestent des correspondances et de la préservation décrites ici, pas d’une exécution de l’application ou d’une certification de production.

## Contrôles nouveaux réellement exécutés

| Contrôle | Résultat | Portée technique |
|---|---|---|
| Huit livrables présents | PASS | Sommaire intégré dans le guide 01 ; aucun neuvième Markdown nécessaire |
| Dix-huit familles complètes | PASS | Objectif, Python, mécanisme, SQL pédagogique, colonnes, résultat, erreurs, effets, exemple, réponse orale |
| Douze parcours complets | PASS | Inscription, session, dossier, commentaire, théorie, like, proposition, signalement, bannissement, archive, purge, statistiques |
| Inventaire des opérations couvert | PASS | {"sites_appel": 480, "modules_python": 29, "trace_sql_executee": false} |
| Appels et positions rapprochés | PASS | Chaque expression du catalogue correspond à un ast.Call réel au chemin et aux lignes indiqués |
| Routes et méthodes sans doublon | PASS | {"declarations": 34, "couples_methode_route": 36, "HEAD_OPTIONS_automatiques_non_comptes": true} |
| HTTP des douze parcours | PASS | Toutes les routes de parcours sont déclarées dans les sources ; aucun endpoint de publication inventé |
| Références au code exactes | PASS | {"references": 115, "noms_lignes_empreintes": "conformes", "renumerotation_historique": false} |
| Index de références complet | PASS | Chaque lien vers du code a une entrée de source dans le guide 07 |
| 76 questions originales conservées | PASS | {"mahamadou": 18, "melissa": 18, "sylvie": 18, "commune": 22} |
| 40 correspondances MAH et communes | PASS | 18 MAH + 22 COM ; formulations originales inchangées |
| Modèles actuels vérifiés | PASS | {"classes": 10, "colonnes": 60, "fk": 13, "relationships": 26} |
| Sept migrations rapprochées | PASS | {"ordre": ["921687c1bd7c", "3111f5767fc6", "a590c8aac613", "82deda84bc35", "c6c100000001", "c6c200000001", "c6g200000001"], "aucune_migration_executee": true} |
| Sept guides 6H.21.4 référencés | PASS | Noms et empreintes conservés ; documents préexistants non réécrits |
| Syntaxe des exemples Python | PASS | {"blocs_python": 19, "execution": false} |
| Exemples SQL et diagrammes qualifiés | PASS | {"SQL_pedagogiques_non_compiles_non_executes": 18, "diagrammes_non_rendus": 2, "blocs_de_commandes_shell": 0} |
| Liens Markdown locaux et ancres | PASS | {"liens_valides": 291, "URL_officielles_distinctes": 9, "reseau_durant_controle": false} |
| Absence de secrets reconnaissables | PASS | Recherche de marqueurs de clés privées, jetons et URI avec identifiants ; pas de garantie d’analyse de toutes les données sensibles |
| Livraison documentaire sans base ni certificat | PASS | Aucune source privée consultée ni fichier de base/certificat ajouté aux documents |
| Preuves historiques distinguées | PASS | {"backend_historique": 318, "date_utc_origine": "2026-11-04T21:55:02.370831+00:00", "tests_applicatifs_nouveaux": 0} |
| Intégrité des 203 fichiers de référence | PASS | Tous les SHA-256 initiaux identiques ; aucun ajout ni retrait dans le dépôt |
| Git préservé | PASS | HEAD, branche, refs, index et statut inchangés ; aucune commande Git d’écriture |
| Noms des huit ajouts futurs libres | PASS | Aucune installation réalisée ; total futur 211 seulement après une autorisation distincte |

Les preuves structurées sont conservées dans VALIDATION_DOCUMENTAIRE_LOT6H21_5.json, INVENTAIRE_STATIQUE.json, ROUTES_DECLAREES.json, REFERENCES_CODE_UTILISEES.json, PARCOURS_DOCUMENTES.json et CORRESPONDANCE_QUESTIONS.json. Le contrôle de référence couvre les 203 chemins publics attendus avant de lire leurs octets ; aucun fichier nouveau inattendu n’est ouvert pour enrichir ce manifeste.

Les sept guides de contenu totalisent 40825 mots selon un comptage par espaces ; cela inclut le catalogue détaillé des appels. Le volume n’est pas un indicateur de couverture applicative ou de qualité à lui seul. Les dix-huit familles possèdent chacune les rubriques A à J ; les douze parcours explicitent leurs étapes absentes et leurs limites de résultat.

## Références et interprétation des opérations

Le relevé final repère 480 sites d’appel dans 29 modules Python. Il distingue construction, exécution, consommation, contexte, schéma et DBAPI. Les homonymes dict.get, mises à jour de dictionnaires et jointures de chemins sont exclus. Les agrégats func.count et textes SQL sont des constructions ; op.get_bind récupère un contexte, pas un DDL. Les appels chaînés sont plusieurs entrées ; ce n’est pas un nombre de requêtes exécutées.

Les 115 références utilisées sont vérifiées par symbole, ligne et SHA-256. Les routes sont rapprochées des décorateurs et du préfixe effectif du Blueprint, sans importer Flask. Les règles implicites de HEAD/OPTIONS ne sont pas comptées comme des parcours métier distincts.

## Exemples et commandes

Les 19 blocs Python ont été parsés avec ast.parse, sans import applicatif ni appel. Certains sont des réductions d’expression avec objets/paramètres supposés déjà fournis dans une fixture ; leur validité syntaxique ne les rend pas autonomes, exécutables sans contexte ou sûrs sur une base réelle.

Les 18 blocs SQL sont des équivalents pédagogiques relus : aucun moteur, compilateur SQL ou parseur SQL spécialisé ne les a validés. Leurs placeholders sont symboliques et la syntaxe de verrou est explicitement qualifiée pour le dialecte. Aucune commande de lancement, de migration ou de restauration n’est exécutée ou fournie comme test documentaire. Aucun bloc shell n’est nécessaire dans cette proposition.

Deux diagrammes sont inclus dans le guide 04 : un trajet général nouvellement décrit et le diagramme-3.mmd validé du projet, repris sans modification. Le contrôle vérifie la présence des blocs et la provenance du diagramme réutilisé ; aucun rendu graphique nouveau n’est revendiqué.

## Ce qui reste historique

Le rapport de campagne 6H.22.8 a été lu comme un fichier de preuve : backend-complet y rapporte 318 tests réussis à sa date d’origine, avec mysql_tested=False, base_originale_utilisee=False et serveur_5066_utilise=False. La synthèse PREUVE_HISTORIQUE_CONSULTEE.json conserve son chemin, son empreinte et cette portée. Les anciens nombres de tests des README/fiches gardent leurs dates et unités ; COM-16 conserve sa formulation historique de 439.

Le code des tests CSRF, uniques, contributions et administration a été examiné statiquement. La présence d’une méthode test_* ne prouve pas son exécution ; les injections d’erreur MySQL ne sont pas des accès Aiven. Aucune campagne backend, frontend ou navigateur n’a été relancée dans ce lot.

## Préservation vérifiée et limites d’observation

Les 203 SHA-256 sont identiques avant et après : sources, sept migrations, README, quatre fiches, trois référentiels, sept guides 6H.21.4, catalogue, six PNG et autres ressources publiques de référence. HEAD, branche, références, statut et empreinte de l’index Git restent également identiques. Les quatre fiches conservent ainsi leurs textes entiers, réponses historiques comprises, au-delà du comptage des 76 questions.

Le dépôt original Documents/portfolio n’a pas été ciblé par une opération de ce lot. Ses bases et secrets ne sont pas ouverts pour établir une preuve de préservation ; on ne prétend pas avoir calculé l’empreinte exhaustive de ses fichiers privés. La SQLite persistante et le serveur 5066 ne sont pas contactés.

Les écritures de travail et de livraison restent hors des dépôts. Le dossier durable est C:\Users\diarr\pedagogie-requetes-integration-lot6h21-5 ; les scripts de fabrication utilisent aussi un espace temporaire de préparation, qui n’est pas l’unique conservation des livrables. Aucune copie commentée ligne par ligne du lot 6H.21.6 n’est créée.

## Confidentialité et sécurité de la production documentaire

Les exemples utilisent des paramètres et données fictives ; les adresses synthétiques éventuelles des expressions de seed proviennent du code public de fixture. Aucun mot de passe, jeton CSRF, cookie, motif réel, clé ou URI privée n’est prélevé dans une exécution. Les marqueurs de clés privées, jetons usuels et URI MySQL avec identifiants ont été recherchés dans les guides.

Cette recherche de motifs ne prouve pas l’absence de toute information sensible possible. La garantie opérationnelle de cette rédaction est le choix de sources publiques attendues et l’absence d’ouverture de secrets/bases, pas la prétendue capacité d’un regex à certifier une confidentialité totale. Les gardes Python du projet ne sont jamais traités comme une frontière de confinement de code arbitraire.

## Points de précision conservés pour la revue

1. /stats est public et fournit trois agrégats ; les sept indicateurs du dashboard ne viennent pas d’un unique endpoint ou instantané transactionnel.
2. La publication d’une proposition et son acceptation ne sont pas implémentées ; le formulaire enregistre pending et sa catégorie dans le texte.
3. Les likes individuels de dossier/commentaire sont des couples uniques ; Theory.likes reste un compteur historique.
4. Le parseur /reports et le setter Report.target_id n’acceptent pas exactement les mêmes formats ; la route générique n’utilise pas required_text pour sa borne UTF-8.
5. Les traitements d’incertitude varient selon les formulaires ; apiRequest n’ajoute pas une idempotence serveur universelle.
6. Plusieurs sérialiseurs et requêtes sont après commit ou hors try local ; une panne n’implique pas automatiquement absence de donnée ni JSON métier uniforme.
7. Les demandes de verrous et contrôles MySQL ne constituent pas une preuve d’exécution de concurrence sur Aiven.
8. Les chemins du README et des fiches ont un contexte historique ; ils ne sont pas réécrits pour annoncer une nouvelle publication ou une autre branche.

Ces constats sont des explications de code, pas des correctifs appliqués ni de nouveaux blocages d’un audit global. Les fonctionnalités et documents existants restent intacts.

## Huit fichiers exacts proposés pour une installation future

Seuls les Markdown ci-dessous seraient candidats à un ajout dans docs/soutenance après une autorisation explicite. Les huit noms sont libres au contrôle et leurs liens restent internes à ce groupe. Le sommaire est inclus dans le premier ; aucun README ou fiche existant n’aurait à être remplacé pour conserver ces liens. Une navigation entrante depuis le sommaire existant demanderait une décision distincte.

1. `01_GUIDE_REQUETES_SQLALCHEMY_LOT6H21_5.md`
2. `02_GUIDE_TRANSACTIONS_INTEGRITE_LOT6H21_5.md`
3. `03_GUIDE_PARCOURS_FONCTIONNELS_LOT6H21_5.md`
4. `04_GUIDE_INTEGRATION_FLASK_API_LOT6H21_5.md`
5. `05_GUIDE_PERMISSIONS_SECURITE_LOT6H21_5.md`
6. `06_GUIDE_PERSISTANCE_ENVIRONNEMENTS_LOT6H21_5.md`
7. `07_CORRESPONDANCE_SOUTENANCE_LOT6H21_5.md`
8. `08_VALIDATION_DOCUMENTAIRE_LOT6H21_5.md`

Les JSON de preuve, instantanés, manifeste de référence et archive demeurent hors du dépôt. Le total de 203 fichiers n’est pas modifié par cette préparation ; une éventuelle autorisation d’ajouter ces huit fichiers porterait le total à 211, sous réserve de revérifier la base au moment du transfert.

## Archive et conservation durable

LOT6H21_5_DOCUMENTS_PROPOSES.zip regroupe les huit Markdown et les annexes documentaires explicitement listées, sans fichier de base, secret ni source applicative complète copiée. LIVRABLES_SHA256.json fixe les membres et leurs empreintes. CONTROLE_ARCHIVE.json, à côté du ZIP, consigne l’empreinte de l’archive, son contrôle CRC et la comparaison des contenus archivés.

Les chemins, les résultats de copie durable et la comparaison finale de l’arbre source sont consignés dans RAPPORT_LIVRAISON_DURABLE.json. Ces deux contrôles sont produits après la fabrication du ZIP ; leur réussite doit être lue dans leurs fichiers, sans s’appuyer sur une promesse de contrôle futur du présent paragraphe.

**Décision : proposition prête pour revue et autorisation éventuelle ; aucun transfert, commit ou publication réalisé.**
