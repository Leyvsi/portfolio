import os

from flask import Flask, jsonify
from flask_cors import CORS

from api.v1.views import app_views
from models import db, User, Comment

app = Flask(__name__)

# Allow CORS for all domains
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Use SQLite: Zero configuration, no passwords needed for the team
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INSTANCE_DIR = os.path.join(BASE_DIR, "instance")
SQLITE_PATH = os.path.join(INSTANCE_DIR, "site.db")

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{SQLITE_PATH.replace(os.sep, '/')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize database
db.init_app(app)

# Create all database tables automatically on startup
with app.app_context():
    # Ensure the instance folder exists before creating the database
    os.makedirs(INSTANCE_DIR, exist_ok=True)
    db.create_all()

# API stats
@app.route("/api/v1/stats", methods=["GET"])
def get_stats():
    try:
        user_count = User.query.count()
        comment_count = Comment.query.count()
        reported_count = Comment.query.filter(
            Comment.reports > 0
        ).count()

        return jsonify({
            "users": user_count,
            "comments": comment_count,
            "reports": reported_count
        }), 200

    except Exception as error:
        print(f"[ERROR] Stats: {error}")

        return jsonify({
            "users": 0,
            "comments": 0,
            "reports": 0
        }), 500

# Register API routes
app.register_blueprint(app_views)

if __name__ == "__main__":
    # Start the Flask server
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
