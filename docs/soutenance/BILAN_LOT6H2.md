# Bilan du lot 6H.2 — sauvegarde, images et installation

> Archive pédagogique datée : les résultats et descriptions ci-dessous concernent le lot indiqué. Les anciens repères de ligne ne décrivent pas la version candidate. Pour préparer la soutenance actuelle, consulter les quatre fiches et le référentiel reliés au sommaire.

> Copie publique de référence : les chemins personnels et liens de travail internes sont retirés. Les preuves et commandes historiques gardent leur date et leur périmètre ; utiliser le README actuel pour le lancement.

2 novembre 2026. Bilan produit après vérification effective du corps de sauvegarde et de sa récupération. Le reçu final contrôle également son annexe et sa copie récupérée.

## Résultat

**Sauvegarde actualisée et récupération vérifiées ; installation propre et lancement isolé vérifiés. Les droits des images sont partiellement clarifiés. Verdict : NO-GO pour déclarer l'ensemble actuel prêt aux commits de livraison.** Aucun commit, push, indexation, changement de branche, fusion, reset, suppression ou déploiement n'a été réalisé.

La provenance ChatGPT des quatre illustrations est déclarée par l'équipe. L'accord pour modifier les images a été reçu, sans modification nécessaire. La diffusion publique et l'origine séparée du SVG restent à confirmer. La préparation technique locale est valide ; elle ne constitue pas l'approbation d'une sélection publique.

## État Git et intégrité

Avant : branche `feature/frontend-api-integration`, HEAD `07a9f03ea0a3bdad4a07066fdd7bab1997cc158b`, **51 fichiers suivis modifiés, 87 non suivis, 0 indexé**, aucun conflit. SHA-256 de l'index : `cc33bbdc5993495735a8c63e85f22f321b05323716ff29b4af3d0fd8df6c5ec3`.

Après : 51 fichiers suivis modifiés, 107 non suivis, 0 indexé, aucun conflit ; branche, HEAD et empreinte de l’index inchangés.

Les 145 fichiers du manifeste 6H.1 étaient identiques à leurs SHA au début du lot. Les 150 empreintes initiales (ces 145, leur manifeste et quatre WebP) ont également été contrôlées avant les retouches documentaires. Seuls `docs/soutenance/README.md` et `frontend/images/README.md` sont ensuite actualisés pour pointer vers les nouveaux résultats. Les autres ajouts 6H.2 sont des documents, preuves et utilitaires hors exécution du site. Backend, frontend applicatif, tests existants, modèles, migrations, images et manifestes figés n'ont pas changé. La copie de travail de Mahamadou et les travaux de Mélissa et Sylvie sont conservés. Aucun contenu privé de comptes, `.env`, clé, certificat, cookie ou base réelle n'a été ouvert.

Le contrôle `git diff --check` par défaut retourne 2 avec 164 signalements liés aux fins CRLF de `backend/api/v1/views/index.py` et `frontend/styles.css`, tous deux identiques à leur empreinte initiale. Avec `core.whitespace=cr-at-eol` limité à cette commande, le contrôle retourne 0. Aucune configuration Git ni fin de ligne du code n'est modifiée. Le reçu d'intégrité conserve ces deux résultats ; aucun succès du contrôle par défaut n'est annoncé.

## Sauvegarde durable et récupération

Nouvelle sauvegarde : `[chemin local privé retiré]`.

Récupération séparée : `[chemin local privé retiré]`.

Le corps principal contient **168 fichiers du projet et 25 roues Python**, soit **193 fichiers / 9455876 octets**. Le bilan final est produit après contrôle du corps principal et ajouté comme un fichier source supplémentaire, avec ses empreintes et copies récupérées ; les métadonnées restent séparées. Les nombres exhaustifs et chaque SHA sont dans `metadata/RESULTAT_FINAL_LOT6H2.json`, dont l'empreinte propre est affichée par l'exécution de l'utilitaire. Le bilan n'est donc pas présenté comme déjà inclus dans le manifeste préparé avant sa rédaction finale.

La sélection fermée (pièce interne non diffusée) et l'inventaire (pièce interne non diffusée) détaillent chaque chemin. SHA du manifeste préparé : `cad6996aa0195a95fb11ccd6b1848e435eb50410fa6a1f42b8c07c8894f67f18`. **Aucun écart SHA-256 ni de récupération pour le corps principal** ; le reçu final vérifie aussi le bilan annexé et l'ensemble des fichiers attendus, sans fichier supplémentaire. Cette copie est une archive privée sélective, pas une sauvegarde de base réelle, de l'environnement installé ou de tout l'historique Git. Elle ne constitue pas une sélection automatique à publier.

L'ancienne sauvegarde `portfolio-lot6e1-20261031-s35x4owh` est conservée, ses **115 fichiers revérifiés avant et après copie**, sans écriture dans ce dossier. Les nouvelles destinations devaient être absentes ; l'utilitaire utilise une création exclusive de chaque fichier et n'effectue aucune suppression, remplacement ou modification des permissions Windows. L'écriture hors sandbox fait l'objet de l'autorisation technique requise au §2.

Les trois anciennes exclusions `frontend/donnees.js`, `frontend/histoires-originales.json` et le CSV de comptes restent exclues et non ouvertes. Les quatre WebP, désormais examinés et autorisés pour ce travail local, sont inclus dans la sauvegarde privée avec leurs octets originaux. Secrets, environnements, cookies/sessions, bases, certificats, clés, journaux sensibles, téléchargements de page et données personnelles non autorisées restent exclus. Les brouillons RGPD sont préservés comme documents internes, sans être publiés dans le site.

## Images et droits

Le [registre par fichier](REGISTRE_IMAGES_LOT6H2.md) distingue déclaration, fournisseur, conditions générales, justificatifs et destination d'usage pour les quatre WebP et le SVG. La déclaration utilisateur identifie **ChatGPT** ; l'opérateur et les références d'entrée ne sont pas précisés. Aucune licence libre n'est inventée. Les conditions consultées ne constituent pas un justificatif propre à chaque image ; le registre donne le lien officiel et les limites. Les cinq ressources sont présentes, leurs octets et le cache sont contrôlés en WSGI statique. Le parcours HTTP du kit expose seulement le SVG, sans élargissement du garde.

**I-02 : NON TRAITÉ → PARTIEL**, preuve nouvelle de provenance déclarée, aucune validation de diffusion publique. Pour clore : attestation couvrant les cinq fichiers, les références éventuelles et l'accord d'usage public ; à défaut, décision ultérieure sur des remplacements documentés. L'autorisation de modifier ne remplace pas cette preuve. L'opération de diffusion reste arrêtée, conformément au §8.

## Installation, lancement et tests

Voir [la méthode détaillée](INSTALLATION_LOT6H2.md) et les preuves conservées (pièce interne non diffusée). Copie source isolée et venv neuf sous Temp ; Python **3.13.0 / Windows AMD64**, 25 roues installées hors réseau après téléchargement PyPI expressément autorisé, neuf dépendances directes conformes, `pip check` réussi, aucune installation globale. Versions transitives figées et roues hachées préservées dans l'annexe privée. Node **v24.16.0** préexistant ; aucun paquet JavaScript, build ou npm requis.

Le lancement complet a été effectué avec les vrais modèles, routes et middleware via le kit 6G.4 inchangé, utilisant exclusivement **SQLite en mémoire**, données synthétiques, FK actives et vérification FK vide. Pas de `.env`, paramètres Aiven vides, aucun accès MySQL/Aiven ni migration exécutée. Le schéma neuf `create_all` ne valide pas une migration d'une base existante. Les sept révisions en chaîne et les 27 chemins/36 opérations OpenAPI restent les constats statiques de 6H.1.

| Contrôle exécuté | Résultat / portée |
|---|---|
| Installation neuve et résolution des dépendances | PASS, 25 roues, venv sans paquets système, installation locale `--no-index`, `pip check` réussi |
| Inspection isolée du kit | PASS, sources figées, ressources et références de scripts disponibles |
| Parcours WSGI existant | PASS, 43 requêtes, vrais contrôleurs et SQL ; sans navigateur |
| Parcours HTTP réel | PASS, 71 requêtes, 13 groupes fonctionnels ; écoute loopback temporaire |
| Inscription, login, histoires et Cold Cases | PASS ; création d'un quatrième membre synthétique |
| Théorie, proposition, commentaire et signalement | PASS ; pending, contexte commentaire/dossier/catégorie, refus CSRF |
| Likes histoire et commentaire | PASS ; ajout, doublon refusé, relecture, retrait, relecture à zéro |
| Administration et sept compteurs | PASS ; **2 / 1 / 1 / 4 / 1 / 1 / 1**, comparaison aux vrais SELECT de cette base mémoire |
| Bannissement, archivage/restauration | PASS ; session bannie refusée, dossier masqué puis retrouvé, contributions conservées |
| Déconnexion et confidentialité | PASS ; `/me` et données admin refusés après logout |
| Pages, scripts, CSS, SVG du kit | PASS ; octets égaux à la copie et `Cache-Control: no-store` |
| Quatre WebP et SVG via middleware statique | PASS en WSGI séparé ; pas d'import backend ni d'écoute supplémentaire |
| Isolation et arrêt | Zéro violation des sept gardes ; serveur arrêté et connexion au port 5064 refusée |

Les nombres diffèrent volontairement de la recette Edge 6G.5 (**2/1/1/3/1/1/0**) car le scénario 6H.2 inscrit un membre et crée une proposition. Aucun défaut du dashboard n'en est déduit. Aucun nouveau navigateur Edge n'a été lancé. **854 PASS reste la référence historique du 1er novembre**, sans relance intégrale ni addition aux requêtes de ce lot.

Le premier essai HTTP est conservé dans Temp comme essai incomplet : un décalage entre la réponse et l'observation SQL de l'outil de contrôle empêchait la preuve finale. Le contrôleur a été corrigé, puis le second essai complet réussit. Aucune correction applicative n'était nécessaire. Le venv neuf charge bien Flask/SQLAlchemy depuis son propre dossier et l'application depuis la copie, comme le reçu d'arrêt l'atteste.

Limites techniques : même PC, aucun autre système ou matériel essayé ; ni migration réelle, ni sauvegarde des interactions en base, ni recette humaine nouvelle, ni nouvelle campagne exhaustive de sécurité/mobile/accessibilité. Ces limites ne sont pas assimilées à un échec du lancement synthétique effectué.

## Six remarques restantes et plan minimal

Les six libellés, priorités, fichiers et preuves de clôture sont reproduits dans pièce de préparation (pièce interne non diffusée). **H-03, H-06, P-01, C-02 et C-07 restent PARTIEL ; I-02 devient PARTIEL.** Aucun nouveau TERMINÉ : **16/22 = 800/11 % = 72,727272… %, soit 72,73 %**, désormais six PARTIEL et zéro NON TRAITÉ. La matrice 6H.1 demeure un état historique conservé.

Plan minimal proposé pour une phase ultérieure, soumise à validation :

1. Confirmer la provenance et l'autorisation publique des cinq images, notamment le SVG ; documenter les références éventuelles ou décider d'un remplacement.
2. Rendre et inspecter les trois diagrammes actuels : connecteur d'architecture, modèle dix tables/treize FK et note du flux.
3. Confirmer la conservation privée des comptes de soutenance ; aucun secret à transmettre dans Git ou cette conversation.
4. Valider les douze décisions RGPD avant une collecte publique, sans publier le brouillon.
5. Revoir la sélection Git : anciens jeux déjà suivis, images, documents internes et chemins privés des rapports ; préparer ensuite des commits ciblés sous autorisation distincte.

Les deux blocages techniques de 6H.1 (sauvegarde obsolète et lancement neuf non vérifié) sont levés dans le périmètre décrit. Le blocage de diffusion des illustrations n'est que partiellement levé. Les trois premiers besoins de rendu restent des demandes du jury ; les validations de production/DDL et les améliorations facultatives ne sont pas transformées en nouvelles lignes de la matrice.

## Décision finale

**NO-GO pour déclarer l'ensemble actuel prêt aux commits de livraison**, en raison de la provenance publique encore incomplète et des arbitrages de sélection des fichiers hérités/documents internes. La sauvegarde privée et la recette locale sont valides. Aucun nettoyage Git ou retrait du suivi n'est exécuté pour contourner ces réserves. Les options sur les images sont une attestation complète de l'équipe ou un remplacement ultérieur autorisé, en conservant les originaux.

Le lot 6H.2 s'arrête à ce bilan. Toute préparation effective de commits, modification applicative, publication ou autre phase attend la validation demandée par l'autorisation.
