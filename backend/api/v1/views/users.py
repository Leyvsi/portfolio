from flask import jsonify
from api.v1.views import app_views
from api.v1.views.index import data_store

@app_views.route('/users', methods=['GET'])
def get_users():
    return jsonify(data_store["utilisateurs"]), 200
