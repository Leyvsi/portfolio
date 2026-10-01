from flask import jsonify, request

from api.v1.views import app_views
from models import db, Theory, Story, User


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
    story = db.session.get(Story, story_id)

    if not story:
        return jsonify({
            "error": "Story not found"
        }), 404

    req_data = request.get_json() or {}

    title = req_data.get("title", "").strip()
    content = req_data.get("content", "").strip()
    user_id = req_data.get("user_id")

    if not title:
        return jsonify({
            "error": "Theory title is required"
        }), 400

    if not content:
        return jsonify({
            "error": "Theory content is required"
        }), 400

    if user_id is not None:
        user = db.session.get(User, user_id)

        if not user:
            return jsonify({
                "error": "User not found"
            }), 404

    new_theory = Theory(
        story_id=story_id,
        user_id=user_id,
        title=title,
        content=content
    )

    db.session.add(new_theory)
    db.session.commit()

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
    theory = db.session.get(Theory, theory_id)

    if not theory:
        return jsonify({
            "error": "Theory not found"
        }), 404

    theory.likes += 1
    db.session.commit()

    return jsonify({
        "status": "success",
        "theory": theory_to_dict(theory)
    }), 200