from flask import jsonify, request
import uuid
from api.v1.views import app_views
from api.v1.views.index import data_store

@app_views.route('/coldcases/<string:case_id>/theories', methods=['GET'])
def get_case_theories(case_id):
    return jsonify(data_store["theories"].get(case_id, [])), 200

@app_views.route('/coldcases/<string:case_id>/theories', methods=['POST'])
def post_case_theory(case_id):
    req_data = request.get_json() or {}
    nouvelle_theorie = {
        "id": "t_" + str(uuid.uuid4())[:8],
        "author": req_data.get('author', 'Anonyme'),
        "text": req_data.get('text', '').strip()
    }
    if case_id not in data_store["theories"]:
        data_store["theories"][case_id] = []
    data_store["theories"][case_id].append(nouvelle_theorie)
    return jsonify({"status": "success", "theory": nouvelle_theorie}), 201
