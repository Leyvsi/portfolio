import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from flask import Flask, jsonify, make_response
from flask_cors import CORS
from api.v1.views import app_views
from api.storage import storage

app = Flask(__name__)
# registration of blueprints
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

@app.teardown_appcontext
def close_db(error):
    """
    No-op for file storage but respects HBnB architecture
    """
    pass

@app.errorhandler(404)
def not_found(error):
    """
    Handle 404 errors RESTfully
    """
    return make_response(jsonify({"error": "Not found"}), 404)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)

