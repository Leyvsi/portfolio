# Provenance des cinq ressources — 6H.5

2 novembre 2026. Complément au [registre historique 6H.2](REGISTRE_IMAGES_LOT6H2.md), conservé à l'identique. **I-02 — Provenance et droits des illustrations : PARTIEL.** Aucune image modifiée, supprimée, remplacée ou générée.

## Faits et pièces disponibles

La déclaration utilisateur 6H.4 identifie **Mélissa, génération avec ChatGPT, soutenance locale** pour les quatre WebP. Elle ne précise ni date de génération, ni images de référence, ni conditions du compte utilisé. Le périmètre local n'autorise pas par déduction un push GitHub, même privé, ni une publication publique.

| Ressource sous `frontend/images/` | Provenance actuellement déclarée | Preuve propre au fichier | À compléter sans secret |
|---|---|---|---|
| `tableau-salle-bleue.webp` | Mélissa / ChatGPT / usage scolaire local | 1200 × 675 ; 62 266 octets ; SHA `18b61b1df61d53de3fee09f85b0e86ba6c307909423800881b6a4067424c1e6b` | Date approximative, confirmation du fichier, références utilisées ou absence déclarée, contexte des conditions applicables |
| `medaille-pavillon-ferme.webp` | Même déclaration | 1200 × 675 ; 82 094 octets ; SHA `8e40ffca976e191fdcaa529181d3f9ff167137e4ff346532a3d3d1d963d49eff` | Même complément par fichier |
| `malle-quai-silencieux.webp` | Même déclaration | 1200 × 675 ; 83 718 octets ; SHA `e4d07971f31325ce9952f179901a60f049d5e2ec777fd98bee905cb81355317c` | Même complément par fichier |
| `carnet-tour-nord.webp` | Même déclaration | 1200 × 675 ; 102 746 octets ; SHA `51330e678fd2aebb671f57dfba72f00b6e839e54ca4768fb96aba280f34bc266` | Même complément par fichier |
| `default-story.svg` | Auteur créatif, outil et source **non établis** | Source locale 1200 × 675, rectangle/trait/texte « Image à venir » ; SHA `ccc3eb24c2afbbf61ccbee1e7aecb268eeb45961a97f4c842104375b5ebc7086` | Création originale ou source tierce ? Qui l'a créé, comment, et quelles autorisations correspondent ? |

Les cinq empreintes correspondent encore aux copies vérifiées 6H.2. Cela établit l'identité des octets, pas leurs droits. Les métadonnées WebP ne donnent pas d'auteur ; aucune absence de référence ou de droit de tiers n'en est déduite.

La réponse détaillée 6H.5 confirme ChatGPT et la destination exclusivement scolaire locale devant le jury Holberton. L'utilisateur indique ne pas connaître les dates exactes et ne pas pouvoir confirmer l'emploi de références ; créateur et outil du SVG restent à vérifier. Ce sont des inconnues expressément déclarées, pas une absence de références prouvée. Le souhait ultérieur de livrer le code sur GitHub ne vaut pas autorisation de diffuser ces ressources.

## Investigation locale distincte du SVG

Le contenu ne contient ni signature, ni licence, ni référence externe. La documentation des images explique son rôle de repli mais ne précise pas sa création. `git log --all --follow` sur ce seul chemin trouve l'ajout dans **`e8f8e4c7bd34530cbbb3eb3ec10ec423c8fc0131`**, daté du **24 octobre 2026 à 16:03:35 +02:00**, auteur Git déclaré **`Mahamadou75-19`**, message « feat(frontend): finaliser F3.2 avec Flask, images et lancement local ».

Le blob de ce commit a été relu : son texte est identique à la source actuelle après normalisation CRLF/LF. Cette trace permet de demander au déposant s'il connaît l'origine ; **elle ne prouve pas que Mahamadou a créé le dessin**, ni une génération par IA ou une licence. La recherche reste limitée au contenu, à la documentation et à l'historique local accessible ; aucun compte, journal privé ou service distant utilisé pour chercher l'auteur.

## Conditions ChatGPT : portée limitée

Les [conditions européennes OpenAI](https://openai.com/policies/eu-terms-of-use/), version affichée du 16 janvier 2026 consultée le 2 novembre, prévoient entre l'utilisateur et OpenAI la propriété des sorties dans les limites légales, imposent les droits nécessaires sur les entrées et n'assurent pas l'unicité. Les conditions des services professionnels sont distinctes. Elles n'établissent pas à elles seules les droits des tiers ni le statut de ces quatre fichiers.

À confirmer : période de génération, service/type de compte et territoire pertinents, sans communiquer d'identifiant de compte ; source et autorisation de toute image de référence éventuelle. Ne pas attribuer CC0, Creative Commons, exclusivité ou absence de droits de tiers. La mention honnête « illustration générée avec ChatGPT par Mélissa, selon déclaration de l'équipe » ne remplace pas les justificatifs.

## Fiche d'attestation à compléter par ressource

« Je confirme que `[NOM DU FICHIER ET EMPREINTE]` a été `[GÉNÉRÉ/CRÉÉ/OBTENU]` par `[PERSONNE]`, vers `[DATE]`, avec `[OUTIL OU SOURCE]`. Les références fournies étaient `[AUCUNE, SI CONFIRMÉ / LISTE ET PROVENANCES]`. Les pièces permettant leur utilisation sont `[JUSTIFICATIFS OU SANS OBJET JUSTIFIÉ]`. Le contexte de conditions applicable est `[SERVICE/TYPE DE COMPTE/TERRITOIRE/PÉRIODE, SANS ACCÈS PRIVÉ]`. L'usage approuvé est `[SOUTENANCE LOCALE / PARTAGE PRIVÉ DÉTERMINÉ / DIFFUSION PUBLIQUE]`. Confirmation le `[DATE]` par `[PERSONNE HABILITÉE]`. »

Un extrait de génération/export sans données privées peut corroborer la déclaration ; un accès au compte ou une conversation intégrale n'est pas nécessaire. Si une référence tierce a été utilisée, son autorisation doit correspondre à l'usage envisagé. Pour le SVG, ne pas remplir les champs par analogie avec les WebP.

Pour clore la provenance locale, obtenir les informations manquantes des cinq ressources et examiner leur cohérence. Une future diffusion impose en plus l'accord pour cette destination et les obligations applicables. L'autorisation de travailler sur le portfolio ne remplace pas ces pièces. **Aucun remplacement n'est proposé par défaut ; tout remplacement ou retrait du suivi exige une décision distincte et la conservation des originaux.**

## Dossier téléchargé : références et utilité uniquement

À la demande explicite de l'utilisateur, `frontend/images/Reprendre projet portfolio_files` a été contrôlé sans ouverture des contenus, modification ou suppression. Le dossier est présent, ignoré par Git, sans enfant suivi. Son inventaire de métadonnées recense 44 fichiers, dont un à extension image acceptée par le lanceur normal ; aucun fichier n'a été lu pour en déduire une provenance ou une licence.

Aucune référence explicite au nom du dossier n'a été trouvée dans les 21 fichiers courants examinés : pages/scripts/CSS racine du frontend (hors `donnees.js` exclu), lanceur et kit. Le dossier n'appartient ni aux 40 sources figées du kit ni à sa liste de ressources publiques. **Aucune utilité identifiée pour la soutenance avec ce kit**. Cela ne certifie pas l'absence d'une URL stockée dans une base réelle non consultée ou dans les fichiers exclus.

Réserve distincte : `run_local.py` accepte les chemins imbriqués sous `/images/` avec une extension de `IMAGE_SUFFIXES`. Un fichier compatible du dossier pourrait donc être servi sur demande directe par le lanceur normal, même sans référence dans les pages ; `.gitignore` n'est pas une protection HTTP. C'est un constat statique de possibilité, pas une requête exécutée ni une exposition publique observée. Le kit isolé applique sa liste fermée `PUBLIC` et refuse ce dossier.

Conserver le dossier intact et hors sélection Git. Avant tout usage élargi du lanceur normal ou déploiement, décider d'un répertoire public explicitement maîtrisé ou d'une restriction de service ; toute correction applicative attend une autorisation distincte. Aucun besoin de supprimer ce dossier ou de modifier le kit scolaire n'est établi.
