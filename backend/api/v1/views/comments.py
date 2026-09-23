from flask import jsonify, request

from api.v1.views import app_views
from models import db, Comment, Story, User


@app_views.route("/stories/<int:story_id>/comments", methods=["GET"])
def get_story_comments(story_id):
    story = db.session.get(Story, story_id)

    if not story:
        return jsonify({
            "error": "Story not found"
        }), 404

    comments = (
        Comment.query
        .filter_by(story_id=story_id)
        .order_by(Comment.created_at.asc())
        .all()
    )

    return jsonify([
        comment.to_dict()
        for comment in comments
    ]), 200


@app_views.route("/stories/<int:story_id>/comments", methods=["POST"])
def post_story_comment(story_id):
    story = db.session.get(Story, story_id)

    if not story:
        return jsonify({
            "error": "Story not found"
        }), 404

    req_data = request.get_json() or {}

    text = req_data.get("text", "").strip()
    user_id = req_data.get("user_id")
    username = req_data.get("username", "Anonyme").strip()

    if not text:
        return jsonify({
            "error": "Comment text is required"
        }), 400

    if user_id is not None:
        user = db.session.get(User, user_id)

        if not user:
            return jsonify({
                "error": "User not found"
            }), 404

        # Use the real username stored in the database
        username = user.username

    if not username:
        username = "Anonyme"

    new_comment = Comment(
        story_id=story_id,
        user_id=user_id,
        username=username,
        text=text
    )

    db.session.add(new_comment)
    db.session.commit()

    return jsonify({
        "status": "success",
        "comment": new_comment.to_dict()
    }), 201


@app_views.route("/comments/<int:comment_id>/like", methods=["POST"])
def like_comment(comment_id):
    comment = db.session.get(Comment, comment_id)

    if not comment:
        return jsonify({
            "error": "Comment not found"
        }), 404

    comment.likes += 1
    db.session.commit()

    return jsonify({
        "status": "success",
        "comment": comment.to_dict()
    }), 200


@app_views.route("/comments/<int:comment_id>/report", methods=["POST"])
def report_comment(comment_id):
    comment = db.session.get(Comment, comment_id)

    if not comment:
        return jsonify({
            "error": "Comment not found"
        }), 404

    comment.reports += 1
    db.session.commit()

    return jsonify({
        "status": "success",
        "comment": comment.to_dict()
    }), 200