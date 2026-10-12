from flask import jsonify, request, session

from api.v1.views import app_views
from api.v1.views.permissions import admin_required
from models import db, Proposal, User


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
    req_data = request.get_json(silent=True) or {}

    user_id = session.get("user_id")
    title = req_data.get("title", "").strip()
    content = req_data.get("content", "").strip()

    if user_id is None:
        return jsonify({
            "status": "error",
            "message": "Authentification requise pour proposer une histoire."
        }), 401

    user = db.session.get(User, user_id)

    if not user:
        session.clear()

        return jsonify({
            "status": "error",
            "message": "Utilisateur introuvable."
        }), 401

    if not title:
        return jsonify({
            "error": "Le titre est obligatoire"
        }), 400

    if not content:
        return jsonify({
            "error": "Le contenu est obligatoire"
        }), 400

    new_proposal = Proposal(
        user_id=user.id,
        title=title,
        content=content,
        status="pending"
    )

    db.session.add(new_proposal)
    db.session.commit()

    return jsonify({
        "status": "success",
        "proposal": proposal_to_dict(new_proposal)
    }), 201
