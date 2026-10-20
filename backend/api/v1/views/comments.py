from flask import jsonify, request

from api.v1.views import app_views
from api.v1.views.permissions import get_authenticated_user
from models import db, Comment, Story, Report


def comment_to_dict(comment):
    data = comment.to_dict()

    data["reports"] = Report.query.filter_by(
        type="comment",
        target_id=str(comment.id)
    ).count()

    return data


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
        comment_to_dict(comment)
        for comment in comments
    ]), 200


@app_views.route("/stories/<int:story_id>/comments", methods=["POST"])
def post_story_comment(story_id):
    user, error_response = get_authenticated_user()

    if error_response:
        return error_response

    story = db.session.get(Story, story_id)

    if not story:
        return jsonify({
            "error": "Story not found"
        }), 404

    req_data = request.get_json(silent=True) or {}

    text = req_data.get("text", "").strip()

    if not text:
        return jsonify({
            "error": "Comment text is required"
        }), 400

    new_comment = Comment(
        story_id=story_id,
        user_id=user.id,
        username=user.username,
        text=text
    )

    db.session.add(new_comment)
    db.session.commit()

    return jsonify({
        "status": "success",
        "comment": comment_to_dict(new_comment)
    }), 201


@app_views.route("/comments/<int:comment_id>/like", methods=["POST"])
def like_comment(comment_id):
    user, error_response = get_authenticated_user()

    if error_response:
        return error_response

    comment = db.session.get(Comment, comment_id)

    if not comment:
        return jsonify({
            "error": "Comment not found"
        }), 404

    comment.likes += 1
    db.session.commit()

    return jsonify({
        "status": "success",
        "comment": comment_to_dict(comment)
    }), 200


@app_views.route("/comments/<int:comment_id>/report", methods=["POST"])
def report_comment(comment_id):
    user, error_response = get_authenticated_user()

    if error_response:
        return error_response

    comment = db.session.get(Comment, comment_id)

    if not comment:
        return jsonify({
            "error": "Comment not found"
        }), 404

    req_data = request.get_json(silent=True) or {}
    reason = req_data.get("reason", "")

    if not isinstance(reason, str) or not reason.strip():
        return jsonify({
            "status": "error",
            "message": "La raison du signalement est obligatoire."
        }), 400

    report = Report(
        type="comment",
        target_id=str(comment.id),
        reason=reason.strip()
    )

    db.session.add(report)
    db.session.commit()

    return jsonify({
        "status": "success",
        "report": report.to_dict()
    }), 201
