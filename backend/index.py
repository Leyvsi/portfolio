from flask import Flask, jsonify
from flask_cors import CORS
from api.v1.views import app_views
from models import db

app = Flask(__name__)

# Enable CORS so your frontend can communicate with this backend
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Configure SQLite database path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database with the Flask app
db.init_app(app)

# Automatically create the site.db file and its tables on startup
with app.app_context():
    db.create_all()

# Register your API blueprint routes
app.register_blueprint(app_views)

@app_views.route('/stats', methods=['GET'])
def get_stats():
    # Simple English comment: static statistics placeholder
    return jsonify({"visits": 142}), 200

if __name__ == "__main__":
    # Run the server on port 5000
    app.run(host="0.0.0.0", port=5000, debug=True)

