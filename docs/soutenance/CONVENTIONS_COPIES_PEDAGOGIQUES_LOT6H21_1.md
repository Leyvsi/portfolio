# Conventions des futures copies pédagogiques — lot 6H.21.1

4 novembre 2026, Europe/Paris. **Conventions uniquement : aucune copie commentée n’est produite dans ce lot.**

[Référentiel expliqué](REFERENTIEL_PEDAGOGIQUE_LOT6H21_1.md) · [Inventaire figé](INVENTAIRE_PEDAGOGIQUE_LOT6H21_1.json)

## 1. Autorité du code et périmètre

Les sources du projet restent les seuls fichiers utilisés par l’application. Une copie pédagogique ne doit jamais remplacer un original, être ajoutée aux imports applicatifs ou servir de lanceur. Le futur emplacement est `docs/soutenance/code-commente-mahamadou/`, avec reproduction des chemins relatifs, par exemple `backend/models.py` sous ce dossier.

L’inventaire distingue neuf modules principalement BDD, quatre modules d’intégration et quatorze modules API partagés avec Sylvie. Il ne prouve pas une propriété ou une contribution individuelle exclusive. Les références frontend sont des supports de lecture partagée avec Mélissa ; l’indexation complète des fonctions JavaScript ne fait pas partie de ce périmètre Python.

La production des copies demande une autorisation distincte, après les lots de préparation prévus. L’ancienne copie `revision_code/mahamadou/backend/models.py` demeure conservée comme archive. Elle ne représente pas le modèle actuel et ne doit pas être utilisée pour restaurer une source.

Les quatre fiches et leurs 76 questions-réponses restent inchangées. Aucun lien vers le README n’est créé ou corrigé ici ; la fin de la refonte approfondie 6H.19.3 est un préalable à ce travail de liens.

## 2. Identifiants uniques et stables

| Objet | Forme | Règle |
|---|---|---|
| Module | `MAH-M001` | Un identifiant par fichier source du périmètre Python. |
| Classe | `MAH-C001` | Un identifiant par déclaration, même pour une classe imbriquée. |
| Fonction ou méthode | `MAH-F0001` | Numérotation globale commune aux fonctions, méthodes, propriétés, fonctions imbriquées et lambda. |
| Ligne locale de fonction | `MAH-F0001:L0001` | Compteur propre à la fonction, rattaché à une ligne physique source. |

Le préfixe MAH désigne ce référentiel pédagogique, pas l’auteur du fichier. La première attribution suit l’ordre des modules du JSON, puis les positions ligne/colonne des déclarations. Les identifiants attribués sont ensuite figés : ne pas renuméroter les entrées existantes pour insérer une nouvelle fonction ; ajouter une nouvelle entrée à la fin et conserver la trace des retraits. Un renommage ou déplacement doit être rapproché explicitement de l’entrée précédente.

Le nom qualifié conserve la portée : classe, fonction externe et méthode locale si nécessaire. Les accesseurs de propriété portent les qualificatifs `[lecture]` et `[ecriture]`. Les lambda ont un ordinal dans leur portée et une position ligne/colonne ; deux lambda sur une même ligne restent deux entrées distinctes. Les méthodes générées par dataclass ou héritées ne sont pas numérotées comme des définitions sources inexistantes.

## 3. Début, fin et numérotation des lignes

Pour une fonction, la première ligne source retenue est le premier décorateur, ou la ligne `def`/`async def` en l’absence de décorateur. La dernière ligne est celle du dernier élément syntaxique appartenant à la fonction, donnée par l’AST. La signature multiligne fait entièrement partie de ce domaine.

La relation est : **numéro local = numéro source − première ligne de déclaration + 1**. Les blancs comptent dans la progression ; ils restent blancs dans la copie et figurent comme tels dans le guide adjacent. Une explication ne doit pas créer artificiellement une instruction sur une ligne vide.

Le premier repère porte **DÉBUT**, le dernier **FIN**. Une lambda sur une seule ligne porte les deux marqueurs. Si le début ou la fin se situe dans une chaîne multiligne non annotable, placer le marqueur dans le guide et un repère sur une ligne de commentaire dédiée hors de la chaîne.

Les fonctions imbriquées ont leur propre compteur. Les lignes appartenant à plusieurs portées sont associées à tous leurs repères dans le guide ; lorsque c’est lisible et syntaxiquement sûr, le commentaire de code peut contenir les repères parent et enfant. Deux lambda sur une même ligne ne doivent jamais recevoir le même identifiant.

Les en-têtes explicatifs ajoutés pour la pédagogie ne changent pas les numéros locaux associés aux lignes sources. Le guide distingue toujours **ligne source**, **repère local** et **ligne de copie** : ne pas confondre ces trois nombres.

## 4. Contrat pédagogique obligatoire

Chaque fonction, méthode, propriété ou lambda doit avoir les éléments suivants :

1. Identifiant, nom qualifié, fichier et empreinte source.
2. Objectif concret dans le parcours applicatif et responsabilité pédagogique.
3. Signature exacte, paramètres positionnels/nommés, valeurs par défaut statiques et sens de chaque paramètre ; expliquer `self`, `*args` et `**kwargs` quand présents.
4. Contexte implicite : variables du module, fermeture, contexte Flask, session, extension SQLAlchemy ou connexion déjà fournie.
5. Fonctionnement détaillé, dans l’ordre : contrôles, branches, appels délégués et traitement des erreurs.
6. Valeur de retour réelle et variantes ; distinguer `None`, booléen, dictionnaire, réponse HTTP, application WSGI et gestionnaire de contexte.
7. Effets : attributs modifiés, session/cookie, requêtes, `flush`, `commit`, `rollback`, fichiers, verrous, environnement, sous-processus et écoute réseau.
8. Exceptions et refus connus, avec la limite des exceptions propagées par d’autres appels.
9. Marqueurs DÉBUT/FIN et correspondance de toutes les lignes de la fonction.

Ne pas inventer de type absent des annotations. Une fonction décorée par `contextmanager` fournit un gestionnaire de contexte ; son `yield` décrit la valeur fournie au bloc, pas un retour ordinaire équivalent. Une route peut retourner un objet Response ou un couple avec statut ; l’expliquer selon les branches du code.

Une fonction qui prépare ou modifie un objet ORM ne valide pas forcément une transaction. Une demande de verrou ne prouve pas son comportement concurrent sur tous les moteurs. Une migration `downgrade` ne doit jamais être présentée comme une restauration des données supprimées.

## 5. Commentaire en français à côté du code

Chaque ligne non vide portant du code doit recevoir une explication française sur la même ligne **lorsque cela conserve exactement la syntaxe et les valeurs de l’instruction**. L’explication décrit l’action de cette ligne et son rôle, pas seulement une paraphrase du mot-clé Python.

Conserver indentation, noms, ordre des instructions, décorateurs, opérateurs, limites, valeurs par défaut et messages. Un commentaire existant peut être complété sans retirer son information ; ne pas ajouter de code exécutable pour expliquer une instruction. Une ligne uniquement composée d’un commentaire n’est pas une instruction à réécrire.

À l’extérieur d’une fonction, utiliser le repère du module et la ligne source. Les classes et attributs SQLAlchemy doivent aussi être expliqués : type, nullabilité, unicité, défaut, relation et règle SQL/ORM, sans assimiler une déclaration de classe à une création immédiate de table.

Le français est porté par les commentaires et guides. Les docstrings et chaînes originales sont conservées pour préserver leurs valeurs et l’introspection : traduire une chaîne dans le code constituerait une modification de cette valeur. Ne pas ajouter une docstring à une fonction pour prétendre conserver un AST strictement identique.

## 6. Exceptions syntaxiques et guide adjacent

| Cas | Traitement |
|---|---|
| Intérieur ou ouverture d’une chaîne multiligne | Ne jamais insérer l’explication dans la chaîne ; fournir la ligne et son explication dans le guide. |
| Ligne se terminant par une continuation explicite `\` | Ne pas ajouter de texte après la continuation ; expliquer la ligne dans le guide. |
| F-string multiligne ou expression imbriquée sensible | Examiner le token et la syntaxe avant annotation ; utiliser le guide en cas de doute. |
| Commentaire dans une continuation implicite avec parenthèses | L’annotation est souvent possible, mais doit être confirmée par le contrôle syntaxique et la conservation des tokens. |
| En-tête spécial d’encodage ou shebang | Conserver sa place et sa syntaxe ; expliquer séparément si nécessaire. |
| Fichier JSON | Aucun commentaire intégré ; guide adjacent uniquement. |
| Gabarit Mako | Examiner le langage du gabarit ; ne pas appliquer aveuglément des commentaires Python. |

Le guide adjacent contiendra au minimum : chemin et empreinte source, identifiant de fonction, ligne source, numéro local, ligne de copie, nature de la ligne, explication française et motif de l’exception. Les lignes vides et les chevauchements de portées y sont repérés. La future liste d’exceptions doit être exhaustive ; une ligne oubliée ne doit pas être présentée comme une exception syntaxique.

## 7. Validation avant livraison des copies

- Vérifier les empreintes avant préparation et refuser une source différente sans revue explicite.
- Vérifier que chaque définition et chaque lambda du périmètre possède un identifiant unique ; ne pas oublier les accesseurs, décorateurs ou fonctions imbriquées.
- Contrôler les paramètres, retours, effets et explications contre la source, avec une revue humaine des contrats.
- Vérifier la couverture des lignes non vides de code : commentaire adjacent ou explication numérotée et justifiée dans le guide.
- Parser les copies avec `ast.parse`, sans import applicatif, migration ou connexion SQL.
- Comparer les AST sans attributs de position et les tokens significatifs ; conserver les chaînes et docstrings, en excluant uniquement les commentaires et positions de comparaison.
- Vérifier la correspondance des lignes source/copie, les marqueurs DÉBUT/FIN et la conservation des blancs.
- Vérifier par empreintes que les originaux, les 76 paires historiques, les PNG, le catalogue et le manifeste du kit restent inchangés.

Une égalité AST ne rend pas la copie exécutable sans risque : `__file__`, le nom de module, les chemins relatifs et les numéros de ligne peuvent changer par déplacement. Les copies restent des documents de lecture, hors du parcours d’exécution. Aucun `py_compile` écrivant du bytecode, lancement serveur ou test sur la SQLite persistante n’est nécessaire pour leur validation documentaire.

## 8. Confidentialité et limites de ce lot

Décrire les paramètres sensibles sans valeurs : mots de passe, cookies, jetons, clés et URI privées ne doivent pas être copiés depuis une exécution. Les modèles peuvent porter des noms de colonnes sensibles ; cela ne justifie pas d’ouvrir une base réelle pour les expliquer.

Le lot 6H.21.1 crée uniquement les trois documents du référentiel. Il ne crée pas le dossier des copies commentées, ne modifie aucune fiche ou source et ne répare aucun lien vers le README. L’actualisation pédagogique complète et la production ligne par ligne demeurent des étapes distinctes.
