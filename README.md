# Les Petits Enquêteurs

Portfolio scolaire Holberton de Mélissa, Sylvie et Mahamadou. Le site permet de lire des histoires et des Cold Cases, proposer des théories, commenter et signaler des contributions. Le projet est présenté en démonstration locale avec des données fictives.

## Installer et présenter

Commencer par le [guide d'installation scolaire](LIVRAISON_SCOLAIRE.md). Il décrit l'installation des dépendances et la recette SQLite mémoire, reproductible sans base distante. La livraison du code sur GitHub ne déploie pas l'application.

Les [supports de soutenance](docs/soutenance/README.md) regroupent les fiches de l'équipe, le parcours de démonstration, les diagrammes et les [résultats de validation](docs/soutenance/VALIDATION_SCOLAIRE.md).

## Équipe et technologies

| Membre | Responsabilités déclarées |
|---|---|
| Mélissa | Frontend HTML, CSS, JavaScript et DOM |
| Sylvie | Backend Flask, API REST et permissions |
| Mahamadou | Modèles SQLAlchemy, base de données et intégration |

Le navigateur échange du JSON avec Flask. SQLAlchemy gère les requêtes et transactions. Le backend utilise MySQL/PyMySQL lorsqu'il est configuré pour ce moteur ; le kit scolaire impose SQLite en mémoire. Les [dépendances Python](backend/requirements.txt) sont versionnées. Le frontend n'exige aucune compilation ; Node.js sert aux tests.

## Fonctionnalités livrées

- Histoires, Cold Cases, recherche locale et fiche de dossier.
- Inscription, connexion, session commune et déconnexion.
- Théories, propositions en attente, commentaires et signalements contextualisés.
- Likes individuels des dossiers et commentaires compatibles, ajout/retrait et contrôle d'unicité.
- Dashboard avec sept compteurs issus du serveur, consultation des utilisateurs et dossiers.
- Bannissement des membres, archivage/restauration et suppression conditionnelle d'un dossier archivé.
- Contrôles serveur des rôles, mots de passe hachés, sessions signées, CSRF et transactions.

Les propositions ne sont pas publiées automatiquement. Le débannissement, la récupération de mot de passe, les pièces jointes et la pagination ne sont pas fournis. Les compteurs historiques incompatibles restent protégés ; aucune réattribution de likes n'est inventée.

## Code et ressources

Voir le [frontend](frontend/README.md), les [modèles](backend/models.py), les [routes](backend/api/v1/views/) et les [migrations candidates](migrations/versions/). Les migrations sont conservées comme sources : la recette scolaire ne les exécute pas et ne certifie pas la migration d'une base réelle.

Le [SVG de remplacement](frontend/images/default-story.svg) est une composition géométrique créée pour cette livraison, sans ressource externe. Sa [provenance](docs/soutenance/PROVENANCE_RESSOURCES.md) est documentée. Les URL d'images fournies par une autre base relèvent de son propre contenu ; la recette utilise uniquement le SVG local.

Les tests sont conservés dans [backend/tests](backend/tests/), [frontend/tests](frontend/tests/) et [tests](tests/). Les campagnes historiques et la recette actuelle sont distinguées dans la validation ; elles ne constituent pas une validation MySQL ni une ouverture publique.

## Diagrammes

Les rendus [SVG/PNG et sources Mermaid](docs/soutenance/preuves-lot6h4/diagrammes/) sont versionnés. Les schémas suivants décrivent l'architecture et les modèles ; la présence d'un moteur dans un schéma n'affirme pas son déploiement.

```mermaid
flowchart TB
  subgraph NAV["Navigateur"]
    HTML["HTML et CSS"]
    DOM["DOM : page en mémoire"]
    JS["app.js, theories-list.js et admin-dashboard.js"]
    APIJS["api.js : fetch, JSON, cookies et CSRF"]
    HTML --> DOM
    JS -->|"lit et modifie"| DOM
    JS --> APIJS
  end
  subgraph MACHINE["Machine qui héberge le site local"]
    subgraph PROCESSUS["Un processus Python : 127.0.0.1:5000"]
      RUN["run_local.py : répartiteur WSGI"]
      STATIC["SharedDataMiddleware"]
      FLASK["Flask : routes et contrôles selon la requête"]
      ORM["SQLAlchemy : requêtes et transactions"]
      RUN -->|"GET et HEAD de ressources"| STATIC
      RUN -->|"API et autres méthodes"| FLASK
      FLASK --> ORM
    end
    subgraph DISQUE["Système de fichiers"]
      FRONT["frontend/ : HTML, CSS, JS, images"]
      SQLITE[("Fichier SQLite : moteur embarqué")]
    end
    STATIC -->|"lit les fichiers publics"| FRONT
    ORM -->|"si une URL SQLite est choisie"| SQLITE
  end
  APIJS -->|"HTTP : JSON et statuts"| RUN
  STATIC -->|"ressources publiques"| HTML
  ORM -.->|"groupe Aiven complet : PyMySQL et TLS"| MYSQL[("Serveur MySQL Aiven")]
```

```mermaid
erDiagram
  users {
    int id PK
    string username UK
    string email UK
  }
  categories {
    int id PK
    string name UK
  }
  stories {
    int id PK
    string slug UK
    string management_revision UK
    int category_id FK
    int author_id FK
  }
  theories {
    int id PK
    int story_id FK
    int user_id FK "NULL autorisé"
  }
  comments {
    int id PK
    int story_id FK
    int user_id FK "NULL autorisé"
  }
  votes {
    int id PK
    int story_id FK
    int user_id FK "UNIQUE avec story_id"
  }
  comment_likes {
    int id PK
    int comment_id FK
    int user_id FK "UNIQUE avec comment_id"
  }
  proposals {
    int id PK
    int user_id FK
  }
  reports {
    int id PK
    int comment_id FK
  }
  cold_case_updates {
    int id PK
    int story_id FK
  }
  users ||..o{ stories : "auteur obligatoire"
  categories ||..o{ stories : "catégorie obligatoire"
  stories ||..o{ theories : "CASCADE"
  users |o..o{ theories : "SET NULL"
  stories ||..o{ comments : "CASCADE"
  users |o..o{ comments : "SET NULL"
  users ||..o{ votes : "CASCADE"
  stories ||..o{ votes : "CASCADE"
  users ||..o{ proposals : "CASCADE"
  stories ||..o{ cold_case_updates : "CASCADE"
  comments ||..o{ reports : "CASCADE"
  comments ||..o{ comment_likes : "CASCADE"
  users ||..o{ comment_likes : "CASCADE"
```

```mermaid
sequenceDiagram
  participant U as Utilisateur
  participant D as DOM et app.js
  participant C as api.js
  participant F as Flask
  participant O as SQLAlchemy
  participant B as Base configurée
  U->>D: Choisir un dossier et saisir titre/contenu
  D->>D: submit, validation et blocage du double envoi
  D->>C: Vérifier le compte courant
  C->>F: GET /api/v1/me avec cookie
  F->>O: Relire le compte et son état
  O->>B: SELECT utilisateur
  alt Session absente ou compte interdit
    F-->>C: 401 ou 403
    C-->>D: Erreur, saisie conservée
  else Compte autorisé
    F-->>C: 200, compte et CSRF de session
    D->>C: createTheory avec identifiant, titre et contenu
    C->>F: POST JSON, cookie et X-CSRF-Token
    F->>F: CSRF, compte, dossier et validation des champs
    alt Contrôle refusé
      F-->>C: 400, 401, 403 ou 404 selon le refus
      C-->>D: Erreur, saisie conservée
    else Requête valide
      F->>O: add(Theory) puis commit()
      O->>B: INSERT lors du flush, puis COMMIT
      alt Transaction réussie
        B-->>O: Écriture validée
        F-->>C: 201 et théorie créée
        C-->>D: Succès confirmé, formulaire réinitialisé
      else Exception SQL gérée
        F->>O: rollback()
        O->>B: ROLLBACK
        F-->>C: 500
        C-->>D: Erreur, saisie conservée
      end
    end
  end
  opt Lecture publique, même sans session
    U->>D: Choisir le dossier du lecteur ou Actualiser
    D->>C: Demander les théories
    C->>F: GET /api/v1/stories/{id}/theories
    F-->>C: 200 et liste, ou 404
    C-->>D: textContent, état vide ou erreur
  end
  Note over D,C: Pas de répétition automatique du POST.<br/>Après création, actualiser le lecteur.<br/>Aucun rechargement automatique.
```

## Données et confidentialité

La démonstration utilise des données synthétiques. Aucune base réelle, configuration privée ou liste d'accès n'est fournie. Les notices présentes ne constituent pas une politique RGPD définitive ; les décisions d'une éventuelle exploitation réelle restent à valider. Ne pas utiliser le lanceur normal avec une configuration distante pour reproduire la recette scolaire.
