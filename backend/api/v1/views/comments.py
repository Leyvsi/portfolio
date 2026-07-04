from flask import jsonify, request
from api.v1.views import app_views
from api.v1.views.index import data_store

@app_views.route('/histoires/<string:story_id>/commentaires', methods=['GET'])
def get_story_comments(story_id):
    return jsonify(data_store["commentaires_resolus"].get(story_id, [])), 200

@app_views.route('/histoires/<string:story_id>/commentaires', methods=['POST'])
def post_story_comment(story_id):
    req_data = request.get_json() or {}
    nouveau_commentaire = {
        "author": req_data.get('author', 'Anonyme'),
        "text": req_data.get('text', '').strip(),
        "date": req_data.get('date', '')
    }
    if story_id not in data_store["commentaires_resolus"]:
        data_store["commentaires_resolus"][story_id] = []
    data_store["commentaires_resolus"][story_id].append(nouveau_commentaire)
    return jsonify({"status": "success", "comment": nouveau_commentaire}), 201

@app_views.route('/theories/<string:theory_id>/commentaires', methods=['GET'])
def get_theory_comments(theory_id):
    return jsonify(data_store["commentaires_theories"].get(theory_id, [])), 200

@app_views.route('/theories/<string:theory_id>/commentaires', methods=['POST'])
def post_theory_comment(theory_id):
    req_data = request.get_json() or {}
    nouveau_comm = {
        "author": req_data.get('author', 'Anonyme'),
        "text": req_data.get('text', '').strip()
    }
    if theory_id not in data_store["commentaires_theories"]:
        data_store["commentaires_theories"][theory_id] = []
    data_store["commentaires_theories"][theory_id].append(nouveau_comm)
    return jsonify({"status": "success", "comment": nouveau_comm}), 201
