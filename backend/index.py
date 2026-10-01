import os

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_migrate import Migrate

from api.v1.views import app_views
from models import db, User, Comment


load_dotenv()

app = Flask(__name__)

# Allow cross-origin requests during development
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

# Initialize database migrations
migrate = Migrate(app, db)


# Create tables on startup
with app.app_context():
    os.makedirs(os.path.dirname(SQLITE_PATH), exist_ok=True)
    db.create_all()


# Application statistics
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


# User login
@app.route("/api/v1/login", methods=["POST"])
def login_user():
    req_data = request.get_json() or {}

    username = req_data.get("username", "").strip()
    password = req_data.get("password", "")

    if not username or not password:
        return jsonify({
            "status": "error",
            "message": "Identifiant et mot de passe obligatoires."
        }), 400

    user = User.query.filter_by(username=username).first()

    if not user or not user.check_password(password):
        return jsonify({
            "status": "error",
            "message": "Identifiants incorrects."
        }), 401

    return jsonify({
        "status": "success",
        "message": "Connexion réussie !",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_admin": user.is_admin
        }
    }), 200


# Register all API blueprint routes
app.register_blueprint(app_views)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )