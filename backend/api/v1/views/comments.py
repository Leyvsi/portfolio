from flask import jsonify, request
from api.v1.views import app_views
from models import db, Comment, Story


@app_views.route("/stories/<int:story_id>/comments", methods=["GET"])
def get_story_comments(story_id):
    story = Story.query.get(story_id)

    if not story:
        return jsonify({"error": "Story not found"}), 404

    comments = (
        Comment.query
        .filter_by(story_id=story_id)
        .order_by(Comment.created_at.asc())
        .all()
    )

    return jsonify([comment.to_dict() for comment in comments]), 200


@app_views.route("/stories/<int:story_id>/comments", methods=["POST"])
def post_story_comment(story_id):
    story = Story.query.get(story_id)

    if not story:
        return jsonify({"error": "Story not found"}), 404

    req_data = request.get_json() or {}

    text = req_data.get("text", "").strip()

    if not text:
        return jsonify({"error": "Comment text is required"}), 400

    new_comment = Comment(
        story_id=story_id,
        user_id=req_data.get("user_id"),
        username=req_data.get("username", "Anonyme"),
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
    comment = Comment.query.get(comment_id)

    if not comment:
        return jsonify({"error": "Comment not found"}), 404

    comment.likes += 1
    db.session.commit()

    return jsonify({
        "status": "success",
        "comment": comment.to_dict()
    }), 200


@app_views.route("/comments/<int:comment_id>/report", methods=["POST"])
def report_comment(comment_id):
    comment = Comment.query.get(comment_id)

    if not comment:
        return jsonify({"error": "Comment not found"}), 404

    comment.reports += 1
    db.session.commit()

    return jsonify({
        "status": "success",
        "comment": comment.to_dict()
    }), 200