from flask import jsonify, session
import re

from api.v1.views import app_views
from api.v1.views.permissions import admin_required, get_authenticated_user
from models import db, User
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from api.v1.views.write_support import api_error, json_object, required_text, is_unique_conflict


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
@admin_required
def get_users():
    """Return all users."""
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200


@app_views.route('/users', methods=['POST'])
def register_user():
    """Create a new user; passwords are preserved exactly as supplied."""
    if session.get("user_id") is not None:
        user, error_response = get_authenticated_user()
        if error_response:
            return error_response

    req_data, error_response = json_object()
    if error_response:
        return error_response

    username, error_response = required_text(req_data, "username", max_length=100)
    if error_response:
        return error_response
    email, error_response = required_text(req_data, "email", max_length=150)
    if error_response:
        return error_response
    password, error_response = required_text(
        req_data, "password", max_length=50, trim=False
    )
    if error_response:
        return error_response

    email_pattern = r"[A-Za-z0-9.!#$%&'*+/=?^_\x60{|}~-]+@[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?)+"
    local_part = email.partition("@")[0]
    if (
        not re.fullmatch(email_pattern, email)
        or len(local_part) > 64
        or local_part.startswith(".")
        or local_part.endswith(".")
        or ".." in local_part
        or any(len(label) > 63 for label in email.partition("@")[2].split("."))
    ):
        return api_error("Adresse email invalide.")

    if not is_valid_password(password):
        return api_error("Le mot de passe ne respecte pas les criteres de securite.")

    if User.query.filter_by(username=username).first():
        return api_error("Cet utilisateur existe deja.")
    if User.query.filter_by(email=email).first():
        return api_error("Cette adresse email est deja utilisee.")

    new_user = User(username=username, email=email)
    new_user.set_password(password)

    try:
        db.session.add(new_user)
        db.session.commit()
    except IntegrityError as error:
        db.session.rollback()
        if is_unique_conflict(
            error, mysql_keys={"username", "email"},
            sqlite_columns={frozenset({"users.username"}), frozenset({"users.email"})}
        ):
            return api_error("Cet utilisateur ou cette adresse email existe deja.")
        return api_error("Impossible de creer l'utilisateur.", 500)
    except SQLAlchemyError:
        db.session.rollback()
        return api_error("Impossible de creer l'utilisateur.", 500)

    return jsonify({"status": "success", "user": new_user.to_dict()}), 201
