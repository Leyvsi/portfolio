from flask import jsonify, request
import uuid

from api.v1.views import app_views
from api.v1.views.index import data_store


@app_views.route(
    '/theories/<string:case_id>/comments',
    methods=['GET']
)
def get_theory_comments(case_id):
    """Return theories for a cold case."""
    theories = data_store["theories"].get(case_id, [])

    return jsonify(theories), 200


@app_views.route(
    '/theories/<string:case_id>/comments',
    methods=['POST']
)
def post_theory_comment(case_id):
    """Create a theory for a cold case."""
    req_data = request.get_json() or {}

    text = req_data.get("text", "").strip()
    username = req_data.get("username", "Anonyme").strip()

    if not text:
        return jsonify({
            "error": "Theory text is required"
        }), 400

    if not username:
        username = "Anonyme"

    new_theory = {
        "id": "t_" + str(uuid.uuid4())[:8],
        "username": username,
        "text": text,
        "likes": 0,
        "reports": 0
    }

    if case_id not in data_store["theories"]:
        data_store["theories"][case_id] = []

    data_store["theories"][case_id].append(new_theory)

    return jsonify({
        "status": "success",
        "theory": new_theory
    }), 201


@app_views.route(
    '/theories/<string:case_id>/<string:theory_id>/like',
    methods=['POST']
)
def like_theory(case_id, theory_id):
    """Add one like to a theory."""
    theories = data_store["theories"].get(case_id, [])

    for theory in theories:
        if theory["id"] == theory_id:
            theory["likes"] = theory.get("likes", 0) + 1

            return jsonify({
                "status": "success",
                "theory": theory
            }), 200

    return jsonify({
        "error": "Theory not found"
    }), 404


@app_views.route(
    '/theories/<string:case_id>/<string:theory_id>/report',
    methods=['POST']
)
def report_theory(case_id, theory_id):
    """Report a theory."""
    theories = data_store["theories"].get(case_id, [])

    for theory in theories:
        if theory["id"] == theory_id:
            theory["reports"] = theory.get("reports", 0) + 1

            return jsonify({
                "status": "success",
                "theory": theory
            }), 200

    return jsonify({
        "error": "Theory not found"
    }), 404