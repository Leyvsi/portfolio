import os

from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_cors import CORS

from api.v1.views import app_views
from models import db, User, Comment

load_dotenv()

app = Flask(__name__)

# CORS
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Database configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SQLITE_PATH = os.path.join(BASE_DIR, "instance", "site.db")

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL",
    f"sqlite:///{SQLITE_PATH.replace(os.sep, '/')}"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize database
db.init_app(app)


# Create database tables
with app.app_context():
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
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )