from flask import jsonify, request
import re
from api.v1.views import app_views
from api.v1.views.index import data_store

def is_valid_password(password):
    if not (8 <= len(password) <= 50):
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>_\-+=\[\]~/\\\';`~]", password):
        return False
    return True

@app_views.route('/users', methods=['GET'])
def get_users():
    return jsonify(data_store["utilisateurs"]), 200

@app_views.route('/users', methods=['POST'])
def register_user():
    req_data = request.get_json() or {}
    username = req_data.get('username', '').strip()
    email = req_data.get('email', '').strip()
    password = req_data.get('password', '')

    if not username or not email or not password:
        return jsonify({"error": "Champs manquants"}), 400

    if not is_valid_password(password):
        return jsonify({"error": "Le mot de passe ne respecte pas les critères de sécurité"}), 400

    if username in data_store["utilisateurs"]:
        return jsonify({"error": "Cet utilisateur existe déjà"}), 400

    data_store["utilisateurs"].append(username)
    return jsonify({"status": "success", "username": username}), 201
