# Illustrations des dossiers

Les six illustrations ci-dessous sont fournies par l'utilisateur pour les six
dossiers restaurés. Elles sont **générées par IA** : ce sont des illustrations,
sans valeur de photographie ni de preuve authentique des affaires racontées.
L'outil, l'opérateur et la date de génération ne sont pas documentés pour ces six
fichiers ; la provenance des anciennes illustrations ne leur est pas attribuée.

## Correspondance vérifiée par slug

Les identifiants et slugs concordent entre le catalogue historique, la SQLite
persistante et son API. L'ordre des réponses API ne sert pas à choisir les images.

| Story | Slug exact | Fichier | Dimensions réelles |
| ---: | --- | --- | --- |
| 101 | `golden-state-killer` | [golden-state-killer.png](golden-state-killer.png) | 1672 × 941 |
| 102 | `chris-watts` | [chris-watts.png](chris-watts.png) | 1672 × 941 |
| 103 | `michelle-carter` | [michelle-carter.png](michelle-carter.png) | 1672 × 941 |
| 201 | `anthonioz` | [mystere-anthonioz.png](mystere-anthonioz.png) | 1671 × 941 |
| 202 | `noirval` | [inconnue-noirval.png](inconnue-noirval.png) | 1671 × 941 |
| 203 | `manoir-de-l-ombre` | [manoir-ombre.png](manoir-ombre.png) | 1670 × 941 |

La correspondance est définie dans `originalStoryIllustrations` de
[app.js](../app.js). Les six champs `Story.image_url` restent NULL : aucun
peuplement, changement de modèle, route API ou modification de base n'est requis.
Les textes, titres, résumés et chapitres du catalogue restent inchangés.

## Format des fichiers conservés

Les six fichiers sont des **PNG RGB 8 bits, non entrelacés**, nommés avec
l'extension `.png`. Les fichiers initialement fournis sous des noms `.webp` ont
été renommés sans réencodage : leurs octets, leurs dimensions et leurs empreintes
SHA-256 restent identiques. Leur intégrité PNG a été vérifiée par les CRC des
blocs, le flux zlib, la taille des pixels décompressés et les filtres des lignes.

Les URL `.png` correspondent au format réel et sont servies avec
`Content-Type: image/png`. Aucune conversion WebP ni réduction de poids n'est
revendiquée : les six fichiers totalisent 15 836 722 octets, soit environ 15,1 Mio.
Le rendu des illustrations avait été validé dans Microsoft Edge 156.0.4314.58 à
1280, 390 et 320 pixels de large au lot 6H.17.3 ; ce contrôle historique précède
le renommage des URL.

| Fichier | SHA-256 des octets fournis |
| --- | --- |
| `golden-state-killer.png` | `22a4a7ee470467387899b6d219cb4da176c2ccea5161a386c27d06f2fdcb1b19` |
| `chris-watts.png` | `7f9d22a3fab83a7132a681219090c12ea8baa7b454360ac941a1f13dceebf882` |
| `michelle-carter.png` | `1422c6c62f8a7ad1c682c31a69bea1b54a290cbd1f2b583ee3cda857641cbd03` |
| `mystere-anthonioz.png` | `0bb8a5acda51b27eb9851b683c2d54aeb11d9a038e99277d79720cac7e969745` |
| `inconnue-noirval.png` | `a6c804d070f172121ba1f04397bb6acd590b2eedc527375c7cfa8cd2c502c2b1` |
| `manoir-ombre.png` | `5fdb88f47e82844df2d479c0fbb9e9413c98286a9c992fef5238c614a5e675d2` |

## Affichage et repli

La fabrique partagée `createStoryImage` sert les cartes de l'accueil, les trois
Histoires, les trois Cold Cases et les six fiches. L'accueil conserve sa limite
de trois cartes. La sélection essaie, dans cet ordre :

1. L'URL HTTP(S) fournie par l'API, si elle est utilisable.
2. L'illustration locale explicitement associée au slug.
3. [default-story.svg](default-story.svg), le visuel neutre « Image à venir ».
4. Le texte « Image indisponible » si le SVG échoue également.

Les erreurs font avancer dans cette liste bornée et dédupliquée. Les schémas
`javascript:`, `data:` et `file:` restent refusés pour `image_url`. La légende IA
et les dimensions réelles s'appliquent uniquement aux six ressources connues ;
elles ne sont pas attribuées à une autre image API ni au SVG de remplacement.

Les illustrations connues ont une légende visible, un texte alternatif indiquant
leur origine IA et leurs dimensions intrinsèques. Le CSS conserve le fichier entier
avec `object-fit: contain`, un cadre fluide et le ratio réel ; les fiches restent
bornées en hauteur sur ordinateur. Les cartes chargent en `lazy`, les fiches en
`eager`, avec décodage `async`. La légende est placée hors du cadre d'image et du
corps narratif ; elle peut revenir à la ligne sur téléphone.

## Serveur persistant et kit scolaire

Le mode persistant 5066 sert déjà ces fichiers sous `/images/` avec
[run_local.py](../../run_local.py), qui désactive le cache local. Les six URL ont
répondu HTTP 200 avec des octets identiques aux fichiers. Aucun redémarrage du
serveur ou changement de session n'est requis pour actualiser les pages statiques.

Le kit scolaire 5064 conserve sa liste publique stricte : seul `default-story.svg`
y est autorisé parmi les images. Il garde donc le repli quand les six illustrations
ne sont pas accessibles. Les contrôles d'intégrité et les protections réseau/SQLite
du kit ne sont pas élargis. Les deux empreintes textuelles d'app.js et styles.css
sont actualisées dans son manifeste ; aucune image binaire n'y est ajoutée.

## Ressources antérieures et provenance

Le SVG de remplacement, auparavant supprimé localement, est restauré à l'identique
depuis Git sous autorisation distincte. Son origine séparée reste non confirmée
dans le [registre historique 6H.2](../../docs/soutenance/REGISTRE_IMAGES_LOT6H2.md).

Les quatre WebP historiques sont conservés depuis les blobs vérifiés de main, car les anciens slugs et leurs tests les utilisent encore. Ils restent distincts des six PNG du catalogue. Le SVG neutre de remplacement est conservé.

## Vérifications

[images.test.cjs](../tests/images.test.cjs) vérifie les six associations, les octets
et dimensions des fichiers, les légendes, les proportions déclarées et les replis.
[histoires-originales.test.cjs](../tests/histoires-originales.test.cjs) contrôle les
six textes exacts, la recherche, l'ordre des catégories et les liens vers les fiches.
Les tests DOM simulés restent distincts du contrôle de décodage et de rendu réel
dans Edge sur ordinateur et téléphone.

```powershell
node --test frontend/tests/images.test.cjs frontend/tests/histoires-originales.test.cjs
```
