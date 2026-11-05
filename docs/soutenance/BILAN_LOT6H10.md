# Lot 6H.10 — état final de livraison

> Archive pédagogique datée : les résultats et descriptions ci-dessous concernent le lot indiqué. Les anciens repères de ligne ne décrivent pas la version candidate. Pour préparer la soutenance actuelle, consulter les quatre fiches et le référentiel reliés au sommaire.

> Copie publique de référence : les chemins personnels et liens de travail internes sont retirés. Les preuves et commandes historiques gardent leur date et leur périmètre ; utiliser le README actuel pour le lancement.

3 novembre 2026. **PUSH NON EFFECTUÉ — livraison bloquée par la condition de sécurité encore non satisfaite.** Aucun commit complémentaire créé. Aucun nouvel audit général ni test applicatif relancé.

## Contrôle ciblé effectué

- Branche : `feature/frontend-api-integration`.
- HEAD local : `0d77a9ab0859f1aa6488405a4f524a399a402f30`.
- Quatre commits locaux conservés : `4bbb75d`, `0d77670`, `3fe3596`, `0d77a9a`.
- Branche distante de [Leyvsi/portfolio](https://github.com/Leyvsi/portfolio), relue via GitHub en GET : `07a9f03ea0a3bdad4a07066fdd7bab1997cc158b`.
- Relation : quatre commits locaux en avance, zéro en retard ; aucune divergence sur cette branche à l'instant du contrôle.
- Index vide ; huit fichiers documentaires modifiés et 151 non suivis à l'entrée de ce lot. Le présent rapport ajoute un non-suivi.

Les travaux locaux restent en place. Aucun changement de branche, reset, réécriture d'histoire, accès à une base, connexion avec les anciens identifiants ou opération distante d'écriture.

## Action humaine minimale indispensable

Le [diagnostic 6H.9](BILAN_LOT6H9.md) établit que les deux accès servaient à une création automatique de comptes administrateur dans une configuration SQLite persistante. Ils sont déjà dans l'histoire publique et absents du code actuel. Leur utilisation effective, les anciens environnements et leur invalidation restent inconnus. Il n'est donc pas établi qu'ils sont actifs ; leur non-utilisabilité n'est pas davantage établie.

**Mahamadou peut coordonner l'identification du détenteur de l'ancien environnement, avec Sylvie pour le contexte Flask. La personne qui possède effectivement cet environnement doit ensuite :**

1. Désactiver les deux comptes concernés ou renouveler leurs mots de passe par un accès administratif légitime, sur les environnements identifiés où ils peuvent encore donner accès.
2. Invalider les sessions concernées et empêcher l'ancien mécanisme de recréer les comptes avec les valeurs exposées. Une rotation de mot de passe seule ne démontre pas l'invalidation des sessions.
3. Confirmer la date, la personne responsable, le périmètre et le résultat, avec un justificatif expurgé. Aucun identifiant, mot de passe, cookie ou jeton ne doit être envoyé dans le chat ou Git.

Si l'environnement n'existe plus, son détenteur doit établir sa mise hors service et le sort des copies pertinentes, ainsi que l'absence de réutilisation des valeurs. L'abandon du code seul ne suffit pas. Le responsable effectif n'a pas encore été identifié ; cette information ne peut pas être déduite de l'auteur Git.

Ces instructions sont préparatoires. Aucune révocation réelle n'a été exécutée. Conformément à la section 4 de la demande 6H.10, le travail de publication s'arrête sur ce blocage ; aucun push partiel des quatre commits.

## Sélection et reprise après sécurisation

Le manifeste 6H.9 (pièce interne non diffusée) reste la préparation de référence : code et tests déjà suivis, 29 versions documentaires préparées séparément, diagrammes et guide scolaire. Les six ressources en attente de décision de diffusion restent suspendues. Leur présence antérieure dans Git ne vaut pas autorisation.

Une adaptation supplémentaire est nécessaire pour respecter l'exclusion 6H.10 des brouillons RGPD internes : projet de texte de confidentialité (pièce interne non diffusée) est déjà suivi et constitue une dépendance de `tests/test_rgpd_information.py`. Il faut traiter ensemble son exclusion de l'arbre livré et le contrat de test, en préservant l'original local ; il ne suffit pas d'omettre ce chemin lors de l'ajout. Aucun changement de ce type n'est effectué pendant l'arrêt de sécurité. Une exclusion future de l'arbre ne retirerait pas les commits historiques, dont la réécriture reste interdite.

Après justification de la sécurisation : appliquer les versions documentaires retenues, résoudre les exclusions et droits restants, contrôler uniquement les différences et leurs dépendances, effectuer les vérifications ciblées nécessaires puis créer les commits complémentaires. Relire la tête distante avant le push normal autorisé sous conditions. Vérifier ensuite réellement les commits, fichiers et ressources sur GitHub.

La preuve de reproduction reste celle de 6H.7 : installation hors ligne dans un venv neuf et 43 requêtes WSGI réussies ; les 854 tests sont historiques. Aucune nouvelle reproduction ou vérification après livraison ne peut être annoncée ici, puisque la livraison n'a pas eu lieu.

**Verdict : NO-GO PUSH tant que la sécurisation des anciens accès n'est pas établie. Aucun nouveau secret publié ; aucun fichier livré pendant 6H.10.**
