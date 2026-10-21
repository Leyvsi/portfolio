from flask import jsonify

from api.v1.views import app_views
from api.v1.views.permissions import get_authenticated_user
from models import db, Theory, Story
from sqlalchemy import update
from sqlalchemy.exc import SQLAlchemyError
from api.v1.views.write_support import api_error, get_resource, json_object, required_text


def theory_to_dict(theory):
    """Convert a Theory object to a dictionary."""
    return {
        "id": theory.id,
        "story_id": theory.story_id,
        "user_id": theory.user_id,
        "title": theory.title,
        "content": theory.content,
        "likes": theory.likes,
        "created_at": (
            theory.created_at.isoformat()
            if theory.created_at else None
        )
    }


@app_views.route(
    "/stories/<int:story_id>/theories",
    methods=["GET"]
)
def get_theories(story_id):
    """Return theories for one story."""
    story = db.session.get(Story, story_id)

    if not story:
        return jsonify({
            "error": "Story not found"
        }), 404

    theories = (
        Theory.query
        .filter_by(story_id=story_id)
        .order_by(Theory.created_at.asc())
        .all()
    )

    return jsonify([
        theory_to_dict(theory)
        for theory in theories
    ]), 200


@app_views.route(
    "/stories/<int:story_id>/theories",
    methods=["POST"]
)
def post_theory(story_id):
    """Create a theory for one story."""
    user, error_response = get_authenticated_user()

    if error_response:
        return error_response

    story = get_resource(Story, story_id)

    if not story:
        return jsonify({
            "error": "Story not found"
        }), 404

    req_data, error_response = json_object()
    if error_response:
        return error_response

    title, error_response = required_text(
        req_data, "title", max_length=Theory.title.type.length
    )
    if error_response:
        return error_response

    content, error_response = required_text(req_data, "content", text_column=True)
    if error_response:
        return error_response

    new_theory = Theory(
        story_id=story_id,
        user_id=user.id,
        title=title,
        content=content
    )

    try:
        db.session.add(new_theory)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return api_error("Impossible de creer la theorie.", 500)

    return jsonify({
        "status": "success",
        "theory": theory_to_dict(new_theory)
    }), 201


@app_views.route(
    "/theories/<int:theory_id>/like",
    methods=["POST"]
)
def like_theory(theory_id):
    """Add one like to a theory."""
    user, error_response = get_authenticated_user()

    if error_response:
        return error_response

    theory = get_resource(Theory, theory_id)

    if not theory:
        return jsonify({
            "error": "Theory not found"
        }), 404

    try:
        # Increment in SQL to avoid overwriting concurrent likes.
        result = db.session.execute(
            update(Theory)
            .where(Theory.id == theory.id)
            .values(likes=Theory.likes + 1)
            .execution_options(synchronize_session=False)
        )
        if result.rowcount == 0:
            db.session.rollback()
            return jsonify({"error": "Theory not found"}), 404
        db.session.refresh(theory)
        payload = theory_to_dict(theory)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return api_error("Impossible d'enregistrer le like.", 500)

    return jsonify({
        "status": "success",
        "theory": payload
    }), 200
