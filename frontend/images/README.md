# Images des dossiers

Ce dossier contient quatre illustrations WebP et un SVG de remplacement. Les images servent aux cartes de l'accueil et des listes, ainsi qu'aux fiches de dossier.

## Inventaire et association locale

Dimensions vérifiées dans les en-têtes des fichiers WebP : **1200 × 675 pixels**, soit **16:9**.

| Dossier | Slug utilisé par le mappage local | Illustration | Dimensions |
|---|---|---|---|
| Le tableau de la salle bleue | `demo-f32-20261024-v1-tableau-salle-bleue` | [tableau-salle-bleue.webp](tableau-salle-bleue.webp) | 1200 × 675 |
| La médaille du pavillon fermé | `demo-f32-20261024-v1-medaille-pavillon-ferme` | [medaille-pavillon-ferme.webp](medaille-pavillon-ferme.webp) | 1200 × 675 |
| La malle du quai silencieux | `demo-f32-20261024-v1-malle-quai-silencieux` | [malle-quai-silencieux.webp](malle-quai-silencieux.webp) | 1200 × 675 |
| Le carnet de la tour nord | `demo-f32-20261024-v1-carnet-tour-nord` | [carnet-tour-nord.webp](carnet-tour-nord.webp) | 1200 × 675 |

La correspondance est définie dans `demoStoryImages`, dans [app.js](../app.js). Elle repose sur le **slug**, indépendamment du titre affiché. Le préfixe technique des slugs est conservé pour maintenir ces associations et les liens.

[default-story.svg](default-story.svg) est un visuel neutre portant le texte « Image à venir ». Il déclare une taille de 1200 × 675 et un `viewBox="0 0 1200 675"`. Il sert de remplacement ; ce n'est pas une cinquième illustration d'histoire.

## Choix d'une image et repli

[app.js](../app.js), avec `getStoryImageSources` et `createStoryImage`, essaie dans cet ordre :

1. `image_url` fourni par l'API, s'il est non vide et se résout en URL HTTP(S), y compris un chemin relatif.
2. L'illustration locale associée au slug, si une correspondance existe.
3. `images/default-story.svg`.
4. Le texte « Image indisponible » si toutes les images échouent ; l'élément cassé est alors masqué.

Les sources identiques sont dédupliquées et la chaîne de repli s'arrête sans boucle. Les schémas tels que `javascript:`, `data:` et `file:` sont refusés pour `image_url`.

Les quatre WebP et le SVG référencés sont présents : **aucune ressource locale attendue ne manque**. La disponibilité d'éventuelles images HTTP(S) distantes n'a pas été vérifiée pendant cet audit.

Les chemins utilisés sont des URL du site, par exemple `/images/tableau-salle-bleue.webp`. Aucun changement en base n'est nécessaire pour utiliser une correspondance locale existante lorsque `image_url` est absent.

## Cadrage et affichage

Les règles communes sont définies dans [styles.css](../styles.css) :

- Conteneur `.story-media` au ratio 16:9, largeur disponible, débordement masqué et coins arrondis.
- Image occupant le conteneur avec `object-fit: cover` : un autre ratio serait recadré.
- Attributs HTML `width=1200` et `height=675`.
- Chargement `lazy` sur les cartes, `eager` sur les fiches, décodage `async`.
- Texte alternatif basé sur le titre du dossier ; le SVG est annoncé comme « Image à venir pour le dossier ».

## Provenance et droits

Aucune provenance, attribution ou licence d'utilisation confirmée pour les quatre WebP n'est documentée dans les sources examinées. Les fichiers ne comportent pas de blocs EXIF ou XMP permettant de compléter ces informations.

Le SVG est fourni sous forme de source dans le dépôt ; aucune licence spécifique à cette ressource n'a été identifiée. La présence des fichiers dans Git ne permet pas, à elle seule, de conclure sur leurs droits d'utilisation.

L'équipe doit confirmer l'origine, l'auteur ou l'outil de création et les conditions d'utilisation applicables avant d'ajouter une attribution. Ces images ne sont pas présentées comme libres de droits.

Les téléchargements du dossier `Reprendre projet portfolio_files/` ne font pas partie des ressources officielles documentées ici.

## Vérification et documentation associée

Le test [images.test.cjs](../tests/images.test.cjs) couvre le choix des sources, le repli borné, les attributs d'image et leur intégration aux cartes et fiches, avec un DOM simulé. Il ne décode pas les WebP et ne vérifie ni leur licence ni leur rendu réel.

Depuis la racine :

```powershell
node --test frontend/tests/images.test.cjs
```

Voir le [README frontend](../README.md) pour lancer le site et toute la suite frontend, et le [README principal](../../README.md) pour la configuration du projet.
