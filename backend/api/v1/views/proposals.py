from flask import jsonify

from api.v1.views import app_views
from api.v1.views.permissions import (
    admin_required,
    get_authenticated_user
)
from models import db, Proposal
from sqlalchemy.exc import SQLAlchemyError
from api.v1.views.write_support import api_error, json_object, required_text


def proposal_to_dict(proposal):
    return {
        "id": proposal.id,
        "user_id": proposal.user_id,
        "title": proposal.title,
        "content": proposal.content,
        "status": proposal.status,
        "created_at": (
            proposal.created_at.isoformat()
            if proposal.created_at else None
        ),
        "updated_at": (
            proposal.updated_at.isoformat()
            if proposal.updated_at else None
        )
    }


@app_views.route("/proposals", methods=["GET"])
@admin_required
def get_proposals():
    proposals = (
        Proposal.query
        .order_by(Proposal.created_at.desc())
        .all()
    )

    return jsonify([
        proposal_to_dict(proposal)
        for proposal in proposals
    ]), 200


@app_views.route("/proposals", methods=["POST"])
def create_proposal():
    user, error_response = get_authenticated_user()

    if error_response:
        return error_response

    req_data, error_response = json_object()
    if error_response:
        return error_response

    title, error_response = required_text(
        req_data, "title", max_length=Proposal.title.type.length
    )
    if error_response:
        return error_response

    content, error_response = required_text(req_data, "content", text_column=True)
    if error_response:
        return error_response

    new_proposal = Proposal(
        user_id=user.id,
        title=title,
        content=content,
        status="pending"
    )

    try:
        db.session.add(new_proposal)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return api_error("Impossible de creer la proposition.", 500)

    return jsonify({
        "status": "success",
        "proposal": proposal_to_dict(new_proposal)
    }), 201
