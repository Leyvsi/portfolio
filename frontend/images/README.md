# Ressource visuelle livrée

Une seule image locale est requise : [default-story.svg](default-story.svg), composition géométrique 1200 × 675 représentant un dossier et une loupe. Le fichier contient uniquement des formes vectorielles, sans script, image incorporée, police téléchargée ou URL externe.

Il a été écrit pour cette livraison avec l'assistance de Codex, sans image d'entrée ni reprise d'une ressource externe. Voir la [provenance](../../docs/soutenance/PROVENANCE_RESSOURCES.md).

Les cartes utilisent `loading="lazy"`, la fiche `loading="eager"`, le ratio 16:9 et un texte alternatif incluant le titre du dossier. L'image HTTP(S) éventuelle de l'API est prioritaire ; en cas d'absence ou d'échec, le SVG est affiché. Si le SVG échoue aussi, un message lisible remplace l'image.
