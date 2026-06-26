from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

USERS_DATABASE = []

ADMIN_CREDENTIALS = {
    "votre_identifiant_secret_leyvsi": "votre_mot_de_passe_leyvsi",
    "votre_identifiant_secret_melissa": "votre_mot_de_passe_melissa"
}

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if username in ADMIN_CREDENTIALS and ADMIN_CREDENTIALS[username] == password:
        return jsonify({"status": "success", "role": "admin", "message": "Bienvenue Admin !"}), 200
        
    for user in USERS_DATABASE:
        if (user['username'] == username or user['email'] == username) and user['password'] == password:
            return jsonify({"status": "success", "role": "user", "message": f"Bonjour {user['username']} !"}), 200

    return jsonify({"status": "error", "message": "Identifiants incorrects."}), 401

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if not username or not email or not password:
        return jsonify({"status": "error", "message": "Tous les champs sont obligatoires."}), 400
        
    for user in USERS_DATABASE:
        if user['username'] == username or user['email'] == email:
            return jsonify({"status": "error", "message": "Ce pseudo ou cet email est déjà utilisé."}), 400
            
    USERS_DATABASE.append({
        "username": username,
        "email": email,
        "password": password
    })
    
    return jsonify({"status": "success", "message": "Utilisateur enregistré avec succès !"}), 201

if __name__ == '__main__':
    app.run(debug=True, port=5000)

