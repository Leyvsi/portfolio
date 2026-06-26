 from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

USERS_DATABASE = []
VISITS_COUNT = 0

ADMIN_CREDENTIALS = {
    "votre_identifiant_secret_leyvsi": "votre_mot_de_passe_leyvsi",
    "votre_identifiant_secret_melissa": "votre_mot_de_passe_melissa"
}

STORIES_PROPOSALS = [
    {
        "id": 1,
        "type": "coldcase",
        "title": "L'affaire de la montre arrêtée",
        "content": "Un corps retrouvé dans un manoir avec une montre brisée...",
        "status": "pending"
    },
    {
        "id": 2,
        "type": "theorie",
        "title": "Le mystère d'Ithaque",
        "content": "Une hypothèse concernant la disparition du navire...",
        "status": "pending"
    }
]

@app.route('/api/visit', methods=['POST'])
def track_visit():
    global VISITS_COUNT
    VISITS_COUNT += 1
    return jsonify({"status": "success", "visits": VISITS_COUNT}), 200

@app.route('/api/stats', methods=['GET'])
def get_stats():
    return jsonify({"status": "success", "visits": VISITS_COUNT}), 200

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    for user in USERS_DATABASE:
        if (user['username'] == username or user['email'] == username) and user['password'] == password:
            return jsonify({"status": "success", "role": "user", "message": f"Bonjour {user['username']} !"}), 200

    return jsonify({"status": "error", "message": "Identifiants utilisateur incorrects."}), 401

@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if username in ADMIN_CREDENTIALS and ADMIN_CREDENTIALS[username] == password:
        return jsonify({"status": "success", "role": "admin", "message": "Bienvenue Admin !"}), 200
        
    return jsonify({"status": "error", "message": "Accès refusé. Identifiants incorrects."}), 403

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

@app.route('/api/admin/proposals', methods=['GET'])
def get_proposals():
    pending_proposals = [p for p in STORIES_PROPOSALS if p['status'] == 'pending']
    return jsonify({"status": "success", "proposals": pending_proposals}), 200

@app.route('/api/admin/proposals/<int:proposal_id>', methods=['POST'])
def moderate_proposal(proposal_id):
    data = request.get_json()
    action = data.get('action')
    updated_title = data.get('title')
    updated_content = data.get('content')
    
    for p in STORIES_PROPOSALS:
        if p['id'] == proposal_id:
            if action == 'accept':
                p['status'] = 'accepted'
                p['title'] = updated_title
                p['content'] = updated_content
                return jsonify({"status": "success", "message": "Proposition acceptée et mise à jour !"}), 200
            elif action == 'reject':
                p['status'] = 'rejected'
                return jsonify({"status": "success", "message": "Proposition refusée."}), 200
                
    return jsonify({"status": "error", "message": "Proposition introuvable."}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
