from flask import jsonify, request
from api.v1.views import app_views
from api.v1.views.index import data_store

@app_views.route('/stories', methods=['GET'])
def get_voting_stories():
    return jsonify(data_store["histoires"]), 200

@app_views.route('/votes/<string:story_id>', methods=['POST'])
def post_story_vote(story_id):
    for histoire in data_store["histoires"]:
        if histoire["id"] == story_id:
            histoire["votes"] += 1
            return jsonify({"message": "Vote pris en compte !", "votes": histoire["votes"]}), 200
    return jsonify({"error": "Story not found"}), 404

@app_views.route('/coldcases/<string:case_id>/updates', methods=['GET'])
def get_case_updates(case_id):
    return jsonify(data_store["updates"].get(case_id, [])), 200
