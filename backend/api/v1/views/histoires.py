from flask import jsonify, request

from api.v1.views import app_views
from models import db, Story, Vote


@app_views.route('/stories', methods=['GET'])
def get_stories():
    """Return all stories."""
    stories = Story.query.order_by(Story.created_at.desc()).all()

    result = []

    for story in stories:
        result.append({
            "id": story.id,
            "title": story.title,
            "summary": story.summary,
            "content": story.content,
            "image_url": story.image_url,
            "category_id": story.category_id,
            "author_id": story.author_id,
            "votes": Vote.query.filter_by(story_id=story.id).count(),
            "created_at": (
                story.created_at.isoformat()
                if story.created_at else None
            )
        })

    return jsonify(result), 200


@app_views.route('/votes/<int:story_id>', methods=['POST'])
def post_story_vote(story_id):
    """Add one vote to a story."""
    req_data = request.get_json() or {}

    user_id = req_data.get("user_id")

    if not user_id:
        return jsonify({
            "error": "user_id est obligatoire pour voter"
        }), 400

    story = Story.query.get(story_id)

    if not story:
        return jsonify({
            "error": "Story not found"
        }), 404

    existing_vote = Vote.query.filter_by(
        story_id=story_id,
        user_id=user_id
    ).first()

    if existing_vote:
        return jsonify({
            "error": "Vous avez déjà voté pour cette histoire"
        }), 409

    new_vote = Vote(
        story_id=story_id,
        user_id=user_id
    )

    db.session.add(new_vote)
    db.session.commit()

    vote_count = Vote.query.filter_by(story_id=story_id).count()

    return jsonify({
        "message": "Vote pris en compte !",
        "votes": vote_count
    }), 201


@app_views.route('/coldcases/<int:case_id>/updates', methods=['GET'])
def get_case_updates(case_id):
    """Return updates for a cold case."""
    # This feature still uses the old data_store.
    # It will be migrated separately.
    from api.v1.views.index import data_store

    return jsonify(
        data_store["updates"].get(str(case_id), [])
    ), 200