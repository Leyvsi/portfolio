# Portfolio — Les Petits Enquêteurs

Ce projet est une plateforme web interactive dédiée aux passionnés de faits divers, de cold cases et de théories de psychologie criminelle. Il se compose d'une interface utilisateur dynamique (Frontend) et d'une API de gestion en arrière-plan (Backend) intégrant une documentation interactive Swagger.

## 🚀 Fonctionnalités Principales

* **Compteur de Visites Global** : Suivi en temps réel de la fréquentation de la page d'accueil.
* **Espace Membre & Inscription** : Formulaire d'enregistrement et de connexion sécurisé pour la communauté.
* **Système de Vote (Top Dossiers)** : Permet aux utilisateurs de voter pour le prochain sujet majeur parmi une sélection hebdomadaire.
* **Espace Administration Évolué** :
    * Visualisation du nombre total de visites.
    * Suivi en direct des votes de la communauté.
    * Panel de modération complet (édition, acceptation ou refus) des histoires proposées par les utilisateurs.
* **Documentation Swagger** : Interface graphique interactive accessible pour le test et le développement des endpoints de l'API.

---

## 📂 Structure du Projet

```text
portfolio/
│
├── backend/
│   ├── app.py
│   └── venv/
│
└── frontend/
    ├── index.html
    ├── connexion.html
    ├── admin-connexion.html
    ├── admin-dashboard.html
    ├── histoires.html
    ├── coldscases.html
    ├── updates.html
    ├── theories.html
    ├── top-dossiers.html
    ├── proposer-histoire.html
    ├── styles.css
    └── background.mp4

🛠️ Installation et Lancement
1. Préparation du Backend (API & Swagger)
Ouvre un terminal, déplace-toi dans le dossier backend et active l'environnement virtuel (il faut installer venv, Flask,  flask-cors, flask-restx ):

Bash
cd portfolio/backend
python3 -m venv venv
source venv/bin/activate

Ensuite lance le serveur Flask : 

python app.py

Le serveur s'active à l'adresse suivante : http://127.0.0.1:5000

2. Accès à la Documentation Technique (Swagger)
On peut également avoir accèes à une documentation technique plus poussé avec Swagger avec cette adresse : http://127.0.0.1:5000/swagger/

3. Lancement du Frontend (Site Web)
Accède au dossier frontend/.

Ouvre le fichier index.html dans ton navigateur (ou utilise l'extension Live Server sur VS Code).

Route API,Méthode,Format Attendu (JSON),Description
/api/visit,POST,Aucun,Incrémente le compteur de visites global de +1
/api/stats,GET,Aucun,Renvoie la valeur actuelle du compteur de visites
/api/votes,GET,Aucun,Liste les 3 histoires soumises au vote populaire
/api/votes/<id>,POST,Aucun,Enregistre un vote supplémentaire pour l'histoire spécifiée
/api/register,POST,"{""username"", ""email"", ""password""}",Enregistre un nouvel utilisateur
/api/login,POST,"{""username"", ""password""}",Authentifie un utilisateur classique
/api/admin/login,POST,"{""username"", ""password""}",Authentifie un administrateur
/api/admin/proposals,GET,Aucun,Récupère la liste des récits soumis en attente de modération
/api/admin/proposals/<id>,POST,"{""action"", ""title"", ""content""}",Valide (accept) ou rejette (reject) une proposition
