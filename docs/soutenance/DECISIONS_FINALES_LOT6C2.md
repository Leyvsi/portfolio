# Lot 6C.2 — proposition de décisions finales

**31 octobre 2026 — vérifications ciblées, documentation uniquement.** [Conception détaillée et scénarios P-01 à P-36](CONCEPTION_LOT6C2_SUPPRESSION.md). Cette fiche précise les choix proposés ; elle ne crée aucune fonctionnalité et ne vaut pas autorisation d’implémentation. Les **604 PASS restent historiques**, sans nouvelle exécution.

## 1. Règles désormais validées par l’utilisateur

- Dossier déjà archivé ; administrateur actif, authentifié et autorisé ; confirmation renforcée obligatoire.
- Traitement cohérent des théories, commentaires, votes, mises à jour et signalements ; aucune référence orpheline ; autres dossiers et comptes conservés.
- Dépendance historique non identifiable fiablement : purge bloquée ; aucun effacement automatique des données ambiguës. Erreur avant commit validé : rollback intégral.
- Suppressions concurrentes et confirmations périmées contrôlées ; réponse perdue après commit : aucune seconde suppression automatique ; reçus minimisés et durée explicitement définie.

Un commit dont l’accusé est perdu ne peut pas être réputé annulé par un simple appel à rollback : son issue doit être recherchée par reçu. Cette précision applique les règles validées, sans promettre l’annulation d’un commit déjà réalisé.

## 2. Signalements : faits confirmés et structure proposée

| Source actuelle vérifiée | Conclusion exacte |
|---|---|
| [Report](../../backend/models.py) | `type` et `target_id` : chaînes NOT NULL, sans enum, CHECK de type ou FK. Le modèle ne limite donc pas les cibles aux commentaires. |
| [POST /reports](../../backend/api/v1/views/index.py) | Après trim, seul `type="comment"` est accepté. Identifiant ASCII positif borné, commentaire existant et parent actif exigés ; la cible enregistrée est canonique. |
| [POST /comments/{id}/report](../../backend/api/v1/views/comments.py) | Impose `type="comment"` et la cible issue du commentaire ; parent actif exigé. |
| [Tests des types](../../backend/tests/test_reports.py) et [normalisation](../../backend/tests/test_reports.py) | `story`, `theory`, `user`, `photo`, `Comment`, `commentaire` refusés ; espaces et zéros initiaux acceptés en entrée puis normalisés. |
| [Fixture 6C.1](../../backend/tests/test_story_archiving.py) | Construit directement un report `other`, pour vérifier sa conservation. Cela prouve la permissivité du modèle, **pas un support HTTP de cette cible** ni sa présence dans une base réelle. |

**Proposition S1 : limiter le schéma cible aux signalements de commentaires et supprimer ceux des commentaires purgés.** Structure finale de `reports` : `id` PK, **`comment_id INTEGER NOT NULL`**, `reason`, `status`, `created_at` conservés ; FK nommée `fk_reports_comment` vers `comments.id`, **ON DELETE CASCADE**, index non unique `ix_reports_comment_id`. Même type et signe que la PK référencée ; plusieurs signalements d’un commentaire restent permis. Les deux colonnes physiques `type/target_id` disparaissent après reprise ; le JSON compatible calcule `type="comment"`, `target_id=str(comment_id)`. Aucune seconde référence modifiable indépendante.

Les reports sont identifiés par **Report → Comment → Story**, jamais par égalité entre target_id et l’id du dossier. Conserver les motifs exigerait une autre politique explicite de trace détachée ; les garder avec une cible disparue est exclu. **La suppression des motifs est encore proposée, pas déjà autorisée par la seule règle « aucun orphelin ».**

### Reprise sans effacement automatique

1. Dans une intervention autorisée ultérieure, inventorier les références, sans les modifier. Reprendre seulement `type` exactement `comment`, cible canonique ASCII entre 1 et 2147483647 et commentaire existant identifié sans ambiguïté. Préserver ids, motifs, statuts, dates et doublons.
2. Référence absente, invalide, non canonique (`00042`, espaces, etc.), type inconnu ou provenance suspecte : enregistrer un diagnostic **restreint**, sans copier les textes ; aucune suppression, conversion permissive ou réattribution automatique. Réparation uniquement après décision explicite et preuve de correspondance.
3. Anomalie attribuable : dossier concerné inéligible. Anomalie non attribuable : impossible de garantir quels dossiers elle concerne ; **bascule relationnelle et activation des purges globalement bloquées** jusqu’à résolution. La contrainte NOT NULL/FK finale ne laisse aucune ligne ambiguë « de côté ».

La normalisation actuelle des **nouvelles requêtes** n’autorise pas à corriger automatiquement l’histoire d’une ancienne ligne. Une ancienne réutilisation d’id peut aussi produire une référence apparemment valide mais fausse ; l’existence actuelle ne suffit pas à prouver la provenance. Le cas de fixture `other` devra devenir un test de reprise refusée, avec un report d’un autre dossier comme témoin de conservation ; aucune assertion supprimée sans remplacement justifié.

## 3. Concurrence : combinaison technique retenue pour la proposition

**Identité immuable + version persistée + verrous + précondition conditionnelle**, conformément au § 4 de la conception : `Story.identity` UUID UNIQUE NOT NULL ; `management_version` entier large positif, départ 1. Version incrémentée sous verrou lors des transitions effectives et des sept écritures réussies de contributions. `updated_at` seul est insuffisant.

L’aperçu fournit le validateur fort **de la représentation administrative de Story**, lié au jeton signé, à l’identité, à la version et à l’empreinte des dépendances. DELETE exige `If-Match` exact. Une restauration/réarchive ou une modification d’impact invalide la confirmation. Le POST de confirmation vérifie le validateur **dans son jeton**, sans If-Match d’une autre ressource. [RFC 9110 — If-Match](https://www.rfc-editor.org/rfc/rfc9110.html#section-13.1.1).

Ordre commun : **User acteur partagé → Story exclusif → Comment → Theory → Vote → ColdCaseUpdate → Report → reçu**, ids croissants par famille. Lectures courantes sur primaire d’écriture, pas de cache/réplique. Recalculer les ensembles verrouillés. Avant le premier DELETE, réserver la version par UPDATE conditionnel `(id, identity, version attendue, archivé)` : **version +1 et exactement une ligne exigée** ; DELETE final vise cette version réservée. La réservation fait partie du rollback. Cette précision complète l’algorithme précédent ; aucune réservation n’est persistée hors transaction de purge.

- **MySQL/InnoDB** : `FOR UPDATE`/verrou partagé et FK actifs sérialisent les opérations ; les commentaires sont verrouillés aussi, car Story seule ne verrouille pas les reports. Deadlock/délai : rollback, 503, aucun retry destructif automatique. Version/moteur réels restent à vérifier sur cible autorisée. [MySQL — locking reads](https://dev.mysql.com/doc/refman/8.4/en/innodb-locking-reads.html).
- **SQLite** : pas de preuve des verrous InnoDB ; la réservation conditionnelle et les transactions restent nécessaires. `BUSY`/snapshot en conflit : rollback et 503. FK à activer **avant** transaction sur chaque connexion puis à contrôler. Le harnais `:memory:` actuel ne prouve pas une course multi-connexion ; pas d’élargissement discret à une base fichier. [SQLite — FK](https://www.sqlite.org/foreignkeys.html).

Une seule transaction : réserver la version ; supprimer reports associés, théories, votes, updates, commentaires, puis Story ; contrôler portée/nombres et absence des dépendances capturées ; insérer le reçu ; commit unique. Toute erreur pré-commit annule aussi reçu et réservation. Aucun changement des dix FK actuelles, aucune suppression de compte, catégorie ou proposition.

## 4. Reçu strictement minimal et durée proposée

**Proposition S2 : un reçu de réconciliation, sans journal d’attribution nominative.** Table nouvelle `story_deletion_receipts` :

| Champs nécessaires | Contraintes / finalité |
|---|---|
| `operation_id` | UUID canonique, PK ; retrouver cette intention après timeout |
| `deleted_story_identity` | UUID UNIQUE NOT NULL, valeur historique non navigable ; éviter de confondre deux incarnations d’un numéro |
| `request_fingerprint` | Empreinte HMAC de la commande canonique (action, opération, identité, validateur, impact), NOT NULL ; détecter une réutilisation incompatible de clé ; aucun contenu/CSRF dans la commande enregistrée |
| `recorded_at` | Date UTC NOT NULL, indexée, fixée juste avant commit ; visible seulement si la transaction est validée |
| Cinq compteurs entiers NOT NULL ≥ 0 | Théories, commentaires, votes, updates et reports réellement supprimés ; le reçu implique un dossier supprimé |

**Affinement du § 4.4 précédent : pas d’actor_id ni de numéro numérique historique du dossier**, inutiles à la réconciliation ; pas de titre, slug, texte, motif, mot de passe, cookie ou jeton. Le contrôle d’identité de l’administrateur/session demeure dans les jetons transitoires. Le reçu n’est pas déclaré anonyme et ne permettra pas de répondre « quel administrateur ? ». Le schéma proposé compte donc **10 tables et 11 FK**, au lieu des 12 envisagées avec la FK d’acteur. Pas de FK du reçu vers la Story supprimée : c’est un fait historique, pas une cible active orpheline.

Accès : GET réservé aux administrateurs actifs authentifiés, par operation_id ; aucun accès public ni listing supplémentaire. Réponse `Cache-Control: no-store`. Reçu inséré **dans la transaction de suppression** ; son échec annule toute la purge. GET et replays ne renouvellent jamais sa conservation.

**Durée proposée : 30 jours à compter de recorded_at pour réconciliation/diagnostic**, avec refus de consultation et de replay à échéance ; nettoyage physique quotidien, sous 24 h supplémentaires, soit **31 jours maximum visés en base active**. Alerter si le nettoyage échoue ; ne pas transformer un incident en conservation indéfinie. Ce choix couvre une reprise après absence ou incident différé sans créer un historique permanent : **durée de produit à valider, pas délai légal**. Les finalités déterminent les durées. [CNIL — conservation](https://www.cnil.fr/fr/passer-laction/les-durees-de-conservation-des-donnees).

Les sauvegardes ont une politique distincte, encore à préciser pour le déploiement : un reçu expiré n’est ni un registre permanent de purge ni une protection suffisante contre une ancienne sauvegarde qui republierait le dossier. Aucun développement général du lot 6E n’est impliqué ici.

## 5. Ordre de migration et déploiement proposé

1. **Préparer ultérieurement** migrations et tests fictifs, sans les appliquer à une base réelle : vérifier la chaîne après `c6c100000001`, les index/FK attendus et le plan de reprise. Aucun fichier de migration créé ici.
2. Lors d’une exécution réelle **séparément autorisée** : sauvegarde contrôlée, maintenance des écritures et arrêt/drainage des anciens processus ; inventorier puis résoudre les anomalies. Aucun ancien écrivain ne doit continuer pendant la reprise.
3. Ajouter les colonnes transitoires, remplir chaque UUID Story différemment, initialiser les versions ; établir comment_id seulement depuis les références validées. Contrôler la conservation de chaque report et de ses valeurs. Une anomalie bloque la suite.
4. Rendre comment_id NOT NULL, ajouter FK/index, retirer les anciennes colonnes **après validation**, créer les contraintes d’identité/version et la table de reçus. Déployer de manière coordonnée les deux créations Report, leurs sérialiseurs et les écrivains versionnés.
5. Attester schéma, FK actives et tests appropriés avant activation de DELETE. Sur MySQL, ne pas promettre le rollback global de plusieurs DDL ; conserver la maintenance et reprendre explicitement une étape échouée. Un downgrade ne recrée jamais les données déjà purgées. Les tests de migration SQLite restent distincts des garanties MySQL.

## 6. Contrat final proposé — routes encore inexistantes

Préfixe `/api/v1`. Toutes les routes exigent admin actif ; CSRF sur POST/DELETE ; aucun changement de l’API publique. Identifiant Story : 1..2147483647, UUID canonique 36 caractères ; tokens ASCII ≤ 4096 octets ; JSON de confirmation ≤ 16 Kio, titre ≤ 200 caractères, clés dupliquées/inconnues refusées. Jetons signés liés à l’acteur/session/action/cible/version/impact, **cinq minutes depuis l’aperçu**, sans prolongation.

| Route | Paramètres / préconditions | JSON 200 |
|---|---|---|
| GET `/admin/stories/{id}/deletion-preview` | Dossier archivé ; lecture sans écriture SQL | `story` (id, identity, title, version, état), `impact` (cinq compteurs), `resource_etag`, `preview_token`, `operation_id`, `expires_at` |
| POST `/admin/stories/{id}/deletion-confirmations` | JSON exact : `preview_token`, `typed_title`, `confirm_contributions:true` ; titre exact et état relus | `status`, `confirmation_token`, même `operation_id`, même `expires_at` ; aucune suppression |
| DELETE `/admin/stories/{id}` | Sans corps ; `If-Match` : un tag fort exact, jamais `*`, liste ou tag faible ; `Idempotency-Key` = operation_id et `X-Deletion-Confirmation` = jeton final | `status`, `code:"PURGE_COMMITTED"`, `replayed`, `receipt` |
| GET `/admin/story-deletions/{operation_id}` | Lecture primaire, admin actif ; reçu dans sa période d’accès | `status`, `receipt` validé |

Formes JSON communes (schématiques) :

```json
{"status":"success","code":"PURGE_COMMITTED","replayed":false,"receipt":{"operation_id":"UUID","deleted_story_identity":"UUID","recorded_at":"DATE_UTC","deleted_counts":{"theories":2,"comments":3,"votes":4,"updates":1,"reports":5}}}
```

```json
{"status":"error","code":"STALE_CONFIRMATION","message":"Confirmation périmée : relire l’aperçu."}
```

Codes : **400** corps/format/accord/titre invalide ; **401** session absente ; **403** rôle, bannissement, CSRF ou signature/contexte invalide ; **404** id hors domaine, Story absente sans reçu correspondant ou reçu absent/expiré ; **409** dossier actif, dépendance ambiguë ou clé incompatible ; **412** identité/version/impact/validateur périmé ou jeton expiré ; **428** préconditions de DELETE manquantes ; **500** erreur avec rollback confirmé ; **503** verrou/capacité indisponible ou `DELETE_STATUS_UNKNOWN` pendant/après COMMIT. Erreurs JSON sans détails SQL ni contenu sensible ; operation_id ajouté seulement s’il est connu et autorisé. Le CSRF global peut refuser avant la vue.

Même clé/demande déjà validée et reçu non expiré : 200 replay sans nouvelle suppression, sous contrôles d’accès. Autre demande : 409. Sans preuve correspondante, **404 ou reçu momentanément absent ne prouvent pas la réussite ni l’échec de la requête**. Après timeout : GET du reçu puis relecture des listes ; jamais de DELETE automatique. Un nouveau dossier ayant repris le même numéro doit rester intact grâce à son UUID différent.

## 7. Tests indispensables et risques résiduels

Les **36 scénarios restent des critères avant mise en service**. Priorité de construction du premier passage sécurisé :

| Socle bloquant | Scénarios existants à implémenter |
|---|---|
| Droits, CSRF, validation, archive et confirmation périmée | P-01 à P-08 |
| Portée exacte, témoins, FK, reprise ambiguë et réutilisation d’id | P-09 à P-14 |
| Vraies écritures puis rollback, COMMIT incertain et doubles demandes | P-15 à P-18 |
| Contributions, reports, restauration et rôle concurrents ; contention et volume | P-19 à P-24, avec garanties MySQL testées sur cible autorisée |
| Annulation/double clic, réponse perdue et états de lecture | P-25 à P-30 |
| Expiration/reprise, migration et non-régression des 604 historiques | P-31 à P-34 ; P-31/P-36 adaptés au reçu sans acteur et aux échéances 30/31 jours |
| Affichage sûr, accès privés et minimisation des reçus | P-35 et P-36 ; clavier/mobile réels en recette séparée |

Risques restant annoncés : données historiques numériquement valides mais déjà mal attribuées ; écritures SQL privilégiées contournant les contrôles ; limites de concurrence SQLite ; deadlocks/volume ; perte irréversible des motifs ; copies, médias et sauvegardes hors transaction ; preuve de réconciliation indisponible après expiration. Aucun de ces risques n’autorise un report volontairement orphelin ou un succès inventé.

## 8. Décisions restantes et verdict pour écrire le code

**Les dix règles métier sont validées ; il n’est pas demandé de les revalider.** Deux arbitrages précis restent proposés :

1. **S1 :** approuver la suppression des reports associés et le schéma limité aux commentaires, avec reprise bloquante des anomalies, y compris blocage global lorsque leur portée est inconnue.
2. **S2 :** approuver le reçu de réconciliation **sans attribution d’acteur**, sa fenêtre d’accès de 30 jours et son nettoyage sous 24 h supplémentaires ; s’il faut identifier l’administrateur, justifier ce besoin avant de réintroduire actor_id.

**NO-GO pour écrire le code à ce stade** : S1/S2 doivent être acceptés, puis une autorisation explicite d’implémentation donnée. La combinaison technique et le contrat proposés sont précis ; aucune reprise de l’audit général n’est nécessaire. Le déploiement réel restera une autorisation distincte, conditionnée au schéma, au moteur, aux tests et à la procédure de sauvegarde.

<!-- CONTROLES_DECISIONS_6C2_START -->
**Contrôle statique PASS :** 93 ressources publiques préexistantes inchangées sur 94 inventoriées ; un document créé, une ligne de navigation ajoutée. Code, modèles, Swagger, migrations, tests, branche, HEAD et index conservés. 42 liens locaux et les exemples JSON contrôlés ; aucun test fonctionnel/destructif ni opération de base. Reçu hors dépôt : `$env:TEMP/portfolio-lot6c2-decisions-20261031-4u5okdsg/final-validation.json`.
<!-- CONTROLES_DECISIONS_6C2_END -->

**Intervention arrêtée à la proposition : aucun code applicatif, route, modèle, migration ou test modifié/exécuté ; aucune suppression, connexion MySQL/Aiven, lecture de secrets, exécution Flask/Edge, modification Windows, commit ou push.**
