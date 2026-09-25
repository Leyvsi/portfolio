from flask import jsonify, request
import re

from api.v1.views import app_views
from models import db, User


def is_valid_password(password):
    """Check password security requirements."""
    if not (8 <= len(password) <= 50):
        return False

    if not re.search(r"[A-Z]", password):
        return False

    if not re.search(r"[a-z]", password):
        return False

    if not re.search(r"[0-9]", password):
        return False

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>_\-+=\[\]~/\\';`~]", password):
        return False

    return True


@app_views.route('/users', methods=['GET'])
def get_users():
    """Return all users."""
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200


@app_views.route('/users', methods=['POST'])
def register_user():
    """Create a new user."""
    req_data = request.get_json() or {}

    username = req_data.get('username', '').strip()
    email = req_data.get('email', '').strip()
    password = req_data.get('password', '')

    if not username or not email or not password:
        return jsonify({"error": "Champs manquants"}), 400

    if not is_valid_password(password):
        return jsonify({
            "error": "Le mot de passe ne respecte pas les critères de sécurité"
        }), 400

    existing_username = User.query.filter_by(username=username).first()

    if existing_username:
        return jsonify({
            "error": "Cet utilisateur existe déjà"
        }), 400

    existing_email = User.query.filter_by(email=email).first()

    if existing_email:
        return jsonify({
            "error": "Cette adresse email est déjà utilisée"
        }), 400

    new_user = User(
        username=username,
        email=email
    )

    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "status": "success",
        "user": new_user.to_dict()
    }), 201