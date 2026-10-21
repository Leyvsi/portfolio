from flask import jsonify

from api.v1.views import app_views
from api.v1.views.permissions import get_authenticated_user
from models import db, Comment, Story, Report
from sqlalchemy import update
from sqlalchemy.exc import SQLAlchemyError
from api.v1.views.write_support import api_error, get_resource, json_object, required_text


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

    story = get_resource(Story, story_id)

    if not story:
        return jsonify({
            "error": "Story not found"
        }), 404

    req_data, error_response = json_object()
    if error_response:
        return error_response

    text, error_response = required_text(req_data, "text", text_column=True)
    if error_response:
        return error_response

    new_comment = Comment(
        story_id=story_id,
        user_id=user.id,
        username=user.username,
        text=text
    )

    try:
        db.session.add(new_comment)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return api_error("Impossible de creer le commentaire.", 500)

    return jsonify({
        "status": "success",
        "comment": comment_to_dict(new_comment)
    }), 201


@app_views.route("/comments/<int:comment_id>/like", methods=["POST"])
def like_comment(comment_id):
    user, error_response = get_authenticated_user()

    if error_response:
        return error_response

    comment = get_resource(Comment, comment_id)

    if not comment:
        return jsonify({
            "error": "Comment not found"
        }), 404

    try:
        # Increment in SQL to avoid overwriting concurrent likes.
        result = db.session.execute(
            update(Comment)
            .where(Comment.id == comment.id)
            .values(likes=Comment.likes + 1)
            .execution_options(synchronize_session=False)
        )
        if result.rowcount == 0:
            db.session.rollback()
            return jsonify({"error": "Comment not found"}), 404
        db.session.refresh(comment)
        payload = comment_to_dict(comment)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return api_error("Impossible d'enregistrer le like.", 500)

    return jsonify({
        "status": "success",
        "comment": payload
    }), 200


@app_views.route("/comments/<int:comment_id>/report", methods=["POST"])
def report_comment(comment_id):
    user, error_response = get_authenticated_user()

    if error_response:
        return error_response

    comment = get_resource(Comment, comment_id)

    if not comment:
        return jsonify({
            "error": "Comment not found"
        }), 404

    req_data, error_response = json_object()
    if error_response:
        return error_response

    reason, error_response = required_text(
        req_data, "reason", text_column=True
    )
    if error_response:
        return error_response

    report = Report(
        type="comment",
        target_id=str(comment.id),
        reason=reason
    )

    try:
        db.session.add(report)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return api_error("Impossible de signaler le commentaire.", 500)

    return jsonify({
        "status": "success",
        "report": report.to_dict()
    }), 201
