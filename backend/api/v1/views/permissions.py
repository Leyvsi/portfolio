from functools import wraps

from flask import jsonify, session

from models import db, User


def admin_required(view_function):
    """Allow access only to authenticated administrators."""
    @wraps(view_function)
    def wrapped_view(*args, **kwargs):
        user_id = session.get("user_id")

        if user_id is None:
            return jsonify({
                "status": "error",
                "message": "Authentification requise."
            }), 401

        user = db.session.get(User, user_id)

        if not user:
            session.clear()

            return jsonify({
                "status": "error",
                "message": "Utilisateur introuvable."
            }), 401

        if not user.is_admin:
            return jsonify({
                "status": "error",
                "message": "Acces administrateur requis."
            }), 403

        return view_function(*args, **kwargs)

    return wrapped_view
