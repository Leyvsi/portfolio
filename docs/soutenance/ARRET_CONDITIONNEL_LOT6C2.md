# Lot 6C.2 — vérification S1 et arrêt conditionnel

> Archive pédagogique datée : les résultats et descriptions ci-dessous concernent le lot indiqué. Les anciens repères de ligne ne décrivent pas la version candidate. Pour préparer la soutenance actuelle, consulter les quatre fiches et le référentiel reliés au sommaire.

**31 octobre 2026.** Réponse à l’autorisation conditionnelle ; aucun développement applicatif commencé. [Conception](CONCEPTION_LOT6C2_SUPPRESSION.md) · [Proposition précédente](DECISIONS_FINALES_LOT6C2.md) · [Sommaire](README.md).

## 1. Condition essentielle non confirmée

| Élément revérifié | Constat |
|---|---|
| [Modèle Report](../../backend/models.py) | `type` est un String(100) NOT NULL sans enum/CHECK ; `target_id` est une chaîne sans FK. Aucune exclusivité SQL pour les commentaires. |
| [POST /reports](../../backend/api/v1/views/index.py) | Seul le type `comment`, après trim, est accepté par l’API ; un commentaire existant et un dossier actif sont exigés. |
| [POST /comments/{id}/report](../../backend/api/v1/views/comments.py) | Impose le type `comment` et l’identifiant du commentaire. |
| [Tests API](../../backend/tests/test_reports.py) | Refus explicite des types story, theory, user, photo, Comment et commentaire. |
| [Fixture 6C.1](../../backend/tests/test_story_archiving.py) | Une construction ORM directe `Report(type='other', target_id='1', ...)` est permise et sert de témoin de conservation. |

**Conclusion : seuls les commentaires sont pris en charge par les routes actuelles ; plusieurs valeurs de type restent possibles dans le modèle.** Le contenu d’une base réelle est inconnu et n’a pas été consulté. La fixture ne démontre aucun usage réel d’un autre type, mais interdit de confirmer l’exclusivité demandée au niveau du modèle/données.

L’instruction utilisateur applicable est : **« Si plusieurs types de cibles sont possibles, arrêter cette partie et présenter une alternative compatible. Ne pas créer de clé étrangère incorrecte. »** La purge et son intégrité dépendant de ce choix, aucun modèle, migration, route, bouton ou test de suppression n’est modifié. Aucune FK n’est posée sur la chaîne générique target_id.

## 2. Alternative simple recommandée — accord explicite nécessaire

**A — Décider explicitement que le produit ne prend en charge que les signalements de commentaires**, ce qui correspond aux deux routes existantes, puis restreindre le modèle. Ce serait une décision de périmètre nouvelle, pas une affirmation sur les données historiques.

- Cible finale proposée : `Report.comment_id`, même type entier que `Comment.id`, NOT NULL, index non unique, FK vers `comments.id` avec ON DELETE CASCADE. Les doublons de signalement restent permis.
- Supprimer les colonnes physiques génériques seulement après reprise validée ; le JSON HTTP continue de calculer `type="comment"` et `target_id=str(comment_id)`. Motifs, statuts, dates et ids de reports valides conservés pendant la reprise.
- Préparer d’abord un contrôle des références canoniques et de leur correspondance. Type autre/inconnu, cible absente, invalide, non canonique ou historiquement suspecte : **arrêt explicite de la reprise, sans correction ni suppression automatique**. L’existence actuelle d’un numéro ne prouve pas sa provenance historique.
- Ne pas activer la purge sur un schéma transitoire ou une reprise incomplète. Une anomalie non attribuable bloque globalement la bascule, car sa portée est inconnue. Les interventions réelles resteraient séparément autorisées.
- Conserver l’intention du test `other` : en faire un cas de migration refusée ; garder un report d’un autre dossier comme témoin de non-suppression. Ne pas simplement retirer ce test pour faire accepter le nouveau modèle.

**B — Conserver un modèle à plusieurs types**, si l’équipe en a réellement besoin : identifier et valider d’abord chaque type et sa table cible, puis définir des références relationnelles adaptées à ces types. Ne pas relier toutes les valeurs de target_id à comments.id. Aucun schéma polymorphe supplémentaire n’est développé ou supposé nécessaire ici.

L’option A est recommandée pour le périmètre actuel et le niveau du projet. Elle ne sera implémentée qu’après accord explicite, puisque la condition S1 initiale ne permet pas cette restriction automatiquement.

## 3. S2 pris en compte : aucun reçu persistant

Le choix utilisateur **remplace la proposition de reçus sur 30/31 jours**. Il n’y aura ni table de reçus, ni route de consultation de reçus, ni purge programmée, ni durée de conservation de reçus à faire valider. L’absence de journal d’audit persistant sera une limite assumée.

Pour la future implémentation, si S1 est résolue :

- Succès de commit reconnu : HTTP 200 et JSON explicite avec la cible/identité supprimée et les nombres effectivement supprimés, construits à partir de la transaction ; aucune écriture de journal séparée.
- Précondition de fraîcheur, identité immuable/version et verrous transactionnels conservés dans le principe ; confirmation renforcée et CSRF. Une erreur avant validation entraîne rollback intégral. Perte de liaison pendant COMMIT : ne pas promettre qu’un rollback local annule un éventuel succès serveur.
- Après timeout/réponse illisible : relecture administrative de la cible sur le serveur, puis listes et statistiques. Dossier de même identité encore présent : présence constatée, pas preuve qu’une opération en cours ne pourra plus se terminer. Dossier 404 : **absence constatée**, pas preuve que cette requête précise a effectué la suppression.
- Si le même numéro désigne une autre identité, ne jamais agir sur le nouveau dossier. Si la relecture échoue ou les droits sont perdus, afficher une issue inconnue et masquer les anciennes actions.
- Aucun DELETE relancé automatiquement. Une répétition sur une cible disparue pourra donner 404 ; sans reçu, ne pas inventer de replay 200, de compteurs historiques ni d’attribution à un administrateur. Une nouvelle action éventuelle exige un nouvel état éligible et une nouvelle confirmation explicite.

Le contrat envisagé sera donc simplifié à l’aperçu, la confirmation et DELETE, plus la lecture administrative existante pour la vérification d’état. **Aucune de ces nouvelles routes n’est ajoutée maintenant.** Les scénarios de reçu P-16/P-17/P-27/P-29/P-31/P-36 devront vérifier cette limite et cette absence de relance, au lieu d’exiger une preuve persistante de l’opération.

## 4. Bilan de cette intervention et décision attendue

- Branche : `feature/frontend-api-integration`, HEAD `07a9f03ea0a3bdad4a07066fdd7bab1997cc158b`, conservés avec l’index Git et le travail antérieur.
- Fichiers concernés : ce rapport créé et une ligne ajoutée au sommaire. **Aucun fichier applicatif, modèle, migration, Swagger ou test modifié.** Aucune migration préparée ou exécutée pendant cette intervention.
- Tests backend/frontend/lanceur : **NON EXÉCUTÉS ici**, car l’autorisation d’implémentation dépend de S1. Les 604 PASS restent la référence historique ; aucune nouvelle affirmation de non-régression ou de compatibilité MySQL.
- Limites actuelles : référence textuelle générique non contrainte ; données historiques réelles non examinées ; concurrence MySQL non prouvée ; absence future de preuve persistante après réponse perdue conformément à S2.

**NO-GO conditionnel pour l’implémentation de la purge. Accord attendu uniquement sur l’option A ou une autre politique de types explicite ; S2 n’est pas à revalider.** L’autorisation de développement déjà donnée reste conditionnelle à la résolution de S1. Aucun développement 6E.

<!-- CONTROLES_ARRET_6C2_START -->
**PASS statique :** 94 ressources publiques préexistantes sur 95 inventoriées conservées octet pour octet ; seul le sommaire est modifié, un rapport créé. 44 liens locaux contrôlés ; code, modèles, migrations, Swagger, tests, branche, HEAD et index Git inchangés. Zéro test exécuté, zéro opération de base. Sauvegarde et reçu hors dépôt : `$env:TEMP/portfolio-lot6c2-condition-s1-20261031-et0tt2l5/baseline.json` et `final-validation.json`.
<!-- CONTROLES_ARRET_6C2_END -->

**Aucune donnée réelle supprimée, aucun accès MySQL/Aiven ou `.env` privé, aucune base ouverte, aucun test destructif, aucun navigateur/Flask, changement de branche, commit ou push.**
