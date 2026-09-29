import os
from flask import Flask, jsonify, request
from flask_cors import CORS

from api.v1.views import app_views
from models import db, User, Comment

app = Flask(__name__)

# Allow cross-origin requests
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Setup local SQLite database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INSTANCE_DIR = os.path.join(BASE_DIR, "instance")
SQLITE_PATH = os.path.join(INSTANCE_DIR, "site.db")

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{SQLITE_PATH.replace(os.sep, '/')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize the database
db.init_app(app)

# Create tables on startup
with app.app_context():
    os.makedirs(INSTANCE_DIR, exist_ok=True)
    db.create_all()

# Route for application statistics
@app.route("/api/v1/stats", methods=["GET"])
def get_stats():
    try:
        user_count = User.query.count()
        comment_count = Comment.query.count()
        reported_count = Comment.query.filter(Comment.reports > 0).count()

        return jsonify({
            "users": user_count,
            "comments": comment_count,
            "reports": reported_count
        }), 200

    except Exception as error:
        print(f"[ERROR] Stats: {error}")
        return jsonify({"users": 0, "comments": 0, "reports": 0}), 500

# Route for user login
@app.route('/api/v1/login', methods=['POST'])
def login_user():
    req_data = request.get_json() or {}
    
    username = req_data.get('username', '').strip()
    password = req_data.get('password', '')

    user = User.query.filter_by(username=username).first()

    if not user or not user.check_password(password):
        return jsonify({
            "status": "error",
            "message": "Identifiants incorrects."
        }), 401

    # Return user data
    return jsonify({
        "status": "success",
        "message": "Connexion réussie !",
        "username": user.username,
        "email": user.email,
        "is_admin": user.is_admin
    }), 200

# Route to fetch all comments
@app.route('/api/v1/comments', methods=['GET'])
def get_comments():
    try:
        # Fetch comments from database
        comments = Comment.query.all()
        comments_list = []
        
        for c in comments:
            comments_list.append({
                "id": c.id,
                "username": getattr(c, 'username', 'Anonyme'),
                "content": getattr(c, 'content', ''),
                "reports": getattr(c, 'reports', 0)
            })
            
        return jsonify({
            "status": "success", 
            "comments": comments_list
        }), 200
    except Exception as error:
        print(f"[ERROR] Get Comments: {error}")
        return jsonify({"status": "error", "message": "Erreur serveur."}), 500


# Route to create a new comment
@app.route('/api/v1/comments', methods=['POST'])
def add_comment():
    req_data = request.get_json() or {}
    
    username = req_data.get('username', '').strip()
    content = req_data.get('content', '').strip()

    if not username or not content:
        return jsonify({
            "status": "error", 
            "message": "Le pseudo et le contenu sont obligatoires."
        }), 400

    try:
        # Create and save the new comment
        new_comment = Comment(username=username, content=content)
        db.session.add(new_comment)
        db.session.commit()
        
        return jsonify({
            "status": "success", 
            "message": "Théorie publiée avec succès !"
        }), 201
    except Exception as error:
        db.session.rollback()
        print(f"[ERROR] Add Comment: {error}")
        return jsonify({"status": "error", "message": "Impossible de publier le commentaire."}), 500

# Load all routes from views
app.register_blueprint(app_views)

if __name__ == "__main__":
    # Start the server
    app.run(host="0.0.0.0", port=5000, debug=True)
