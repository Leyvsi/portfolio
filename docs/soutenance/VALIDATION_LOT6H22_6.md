# Corrections ciblées du harnais et de la sélection publique — lot 6H.22.6

Le harnais public remplace `sqlite3.connect` et `sqlite3.dbapi2.connect` par une
fabrique contrôlée. Un contrôle de création, limité au contexte de cet appel,
refuse aussi les constructeurs directs et alias natifs qui passeraient autrement
à côté de l’installation de l’autoriseur. Les fabriques personnalisées sont
refusées avant leur exécution.

Les connexions remises aux tests utilisent SQLite mémoire, un stockage temporaire
en mémoire et un autoriseur qui refuse `ATTACH`, `DETACH`, `VACUUM INTO`, les
extensions et les changements de répertoire ou de mode de stockage temporaire.
Le remplacement ordinaire de cet autoriseur est refusé. Une sauvegarde entre
deux connexions mémoire reste possible ; aucune connexion fichier n’est admise.

Les [sondes reproductibles](../../tests/test_backend_isolation_guards.py)
reprennent le contre-exemple du constructeur direct et vérifient les chemins
Python et SQLite concernés sur des fixtures synthétiques jetables. Les résultats
réellement exécutés, commandes et limites sont consignés dans le dossier local
de livraison de ce lot, distinct des preuves historiques 6H.22.4.

**Portée de sécurité : tests de confiance uniquement.** Les interceptions Python
et l’autoriseur ne constituent pas une frontière de sécurité contre du code
arbitraire. Aucun confinement propre au harnais imposé par le système
d’exploitation n’est attesté dans ces essais Windows. Une action volontaire sur
les internes Python, un appel explicite à une méthode native de la classe de
base, un code natif ou un descripteur hérité peut sortir de cette garantie.
Exécuter uniquement du code revu, dans des ressources jetables autorisées.

Les quatre documents reconnus internes ne font plus partie de l’arbre public.
Leurs originaux et les références des lots précédents restent conservés à leur
emplacement local ; leur contenu n’est pas repris dans les nouveaux supports ou
diffs publics. Les quelques références publiques nécessaires dirigent vers les
descriptions publiques existantes des [illustrations](../../frontend/images/README.md)
et de l’[interface](../../frontend/README.md). Les [tests documentaires](../../tests/test_publication_documents.py)
vérifient leur absence et les références publiques.

Les six PNG, six histoires, dix modèles, sept migrations, fonctionnalités,
quatre fiches avec leurs 76 questions et trois ressources pédagogiques figées
restent préservés. Les autres observations documentaires de la revue précédente
ne sont pas rouvertes dans ce correctif ciblé.

La candidate est un arbre de fichiers sans historique Git. La future publication
doit partir de main et transférer uniquement les fichiers publics autorisés,
sans reprendre les commits locaux contenant des pièces internes. L’exclusion de
fichiers ne nettoie pas un historique déjà contaminé.

Le GO technique éventuel d’un transfert de sources est distinct d’une
autorisation d’intégration, d’une application de migration et d’un GO de
publication. Aucun serveur existant ou base persistante ne doit intervenir dans
la validation de ce harnais.
