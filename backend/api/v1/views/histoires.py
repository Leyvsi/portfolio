from flask import jsonify

from api.v1.views import app_views
from api.v1.views.permissions import get_authenticated_user
from models import db, Story, Vote, ColdCaseUpdate
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from api.v1.views.write_support import api_error, get_resource, is_unique_conflict


@app_views.route('/stories', methods=['GET'])
def get_stories():
    """Return all stories."""
    stories = Story.query.order_by(Story.created_at.desc()).all()

    result = []

    for story in stories:
        result.append({
            "id": story.id,
            "slug": story.slug,
            "title": story.title,
            "summary": story.summary,
            "content": story.content,
            "image_url": story.image_url,
            "category_id": story.category_id,
            "author_id": story.author_id,
            "votes": Vote.query.filter_by(
                story_id=story.id
            ).count(),
            "created_at": (
                story.created_at.isoformat()
                if story.created_at else None
            )
        })

    return jsonify(result), 200


@app_views.route('/stories/slug/<string:slug>', methods=['GET'])
def get_story_by_slug(slug):
    """Return one story using its slug."""
    story = Story.query.filter_by(slug=slug).first()

    if not story:
        return jsonify({
            "error": "Story not found"
        }), 404

    vote_count = Vote.query.filter_by(
        story_id=story.id
    ).count()

    result = story.to_dict()
    result["votes"] = vote_count

    return jsonify(result), 200


@app_views.route('/votes/<int:story_id>', methods=['POST'])
def post_story_vote(story_id):
    """Add one vote to a story for the authenticated user."""
    user, error_response = get_authenticated_user()

    if error_response:
        return error_response

    story = get_resource(Story, story_id)

    if not story:
        return jsonify({
            "error": "Story not found"
        }), 404

    existing_vote = Vote.query.filter_by(
        story_id=story_id,
        user_id=user.id
    ).first()

    if existing_vote:
        return jsonify({
            "error": "Vous avez déjà voté pour cette histoire"
        }), 409

    new_vote = Vote(
        story_id=story_id,
        user_id=user.id
    )

    try:
        db.session.add(new_vote)
        db.session.commit()
    except IntegrityError as error:
        db.session.rollback()
        if is_unique_conflict(
            error, mysql_keys={"unique_user_story_vote"},
            sqlite_columns={frozenset({"votes.user_id", "votes.story_id"})},
        ):
            return jsonify({"error": "Vous avez déjà voté pour cette histoire"}), 409
        return api_error("Impossible d'enregistrer le vote.", 500)
    except SQLAlchemyError:
        db.session.rollback()
        return api_error("Impossible d'enregistrer le vote.", 500)

    vote_count = Vote.query.filter_by(
        story_id=story_id
    ).count()

    return jsonify({
        "message": "Vote pris en compte !",
        "votes": vote_count
    }), 201


@app_views.route('/coldcases/<int:case_id>/updates', methods=['GET'])
def get_case_updates(case_id):
    """Return updates for a cold case."""
    story = db.session.get(Story, case_id)

    if not story:
        return jsonify({
            "error": "Story not found"
        }), 404

    updates = ColdCaseUpdate.query.filter_by(
        story_id=case_id
    ).order_by(
        ColdCaseUpdate.created_at.asc()
    ).all()

    return jsonify([
        update.to_dict()
        for update in updates
    ]), 200
