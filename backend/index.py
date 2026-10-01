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

    return jsonify({
        "status": "success",
        "message": "Connexion réussie !",
        "username": user.username,
        "email": user.email,
        "is_admin": user.is_admin
    }), 200

# Route to fetch all comments (Admin/Global)
@app.route('/api/v1/comments', methods=['GET'])
def get_comments():
    try:
        comments = Comment.query.all()
        comments_list = [{
            "id": c.id,
            "story_id": getattr(c, 'story_id', ''),
            "username": getattr(c, 'username', 'Anonyme'),
            "text": getattr(c, 'text', getattr(c, 'content', '')),
            "likes": getattr(c, 'likes', 0),
            "reports": getattr(c, 'reports', 0)
        } for c in comments]
            
        return jsonify({
            "status": "success", 
            "comments": comments_list
        }), 200
    except Exception as error:
        print(f"[ERROR] Get Comments: {error}")
        return jsonify({"status": "error", "message": "Erreur serveur."}), 500

# Route to create a global comment
@app.route('/api/v1/comments', methods=['POST'])
def add_comment():
    req_data = request.get_json() or {}
    
    username = req_data.get('username', '').strip()
    content = req_data.get('content', req_data.get('text', '')).strip()

    if not username or not content:
        return jsonify({"status": "error", "message": "Le pseudo et le contenu sont obligatoires."}), 400

    try:
        new_comment = Comment(username=username, text=content, story_id='global')
        db.session.add(new_comment)
        db.session.commit()
        return jsonify({"status": "success", "message": "Publié avec succès !"}), 201
    except Exception as error:
        db.session.rollback()
        print(f"[ERROR] Add Comment: {error}")
        return jsonify({"status": "error", "message": "Impossible de publier le commentaire."}), 500

# Route to fetch comments for specific stories
@app.route('/api/v1/stories/<story_id>/comments', methods=['GET'])
def get_story_comments(story_id):
    try:
        comments = Comment.query.filter_by(story_id=story_id).all()
        comments_list = [{
            "id": c.id,
            "username": getattr(c, 'username', 'Anonyme'),
            "text": getattr(c, 'text', getattr(c, 'content', '')),
            "likes": getattr(c, 'likes', 0),
            "reports": getattr(c, 'reports', 0)
        } for c in comments]
        return jsonify(comments_list), 200
    except Exception as e:
        print(f"[ERROR] Get Story Comments: {e}")
        return jsonify([]), 200

# Route to post comment for specific stories
@app.route('/api/v1/stories/<story_id>/comments', methods=['POST'])
def post_story_comment(story_id):
    req_data = request.get_json() or {}
    try:
        new_comment = Comment(
            story_id=story_id,
            username=req_data.get('username', 'Anonyme'),
            text=req_data.get('text', req_data.get('content', ''))
        )
        db.session.add(new_comment)
        db.session.commit()
        return jsonify({"status": "success", "message": "Commentaire publié !"}), 201
    except Exception as e:
        db.session.rollback()
        print(f"[ERROR] Post Story Comment: {e}")
        return jsonify({"status": "error", "message": "Erreur serveur."}), 500

# Route to fetch comments for theories / cold cases
@app.route('/api/v1/theories/<case_id>/comments', methods=['GET'])
def get_theory_comments(case_id):
    try:
        comments = Comment.query.filter_by(story_id=case_id).all()
        comments_list = [{
            "id": c.id,
            "username": getattr(c, 'username', 'Anonyme'),
            "text": getattr(c, 'text', getattr(c, 'content', '')),
            "likes": getattr(c, 'likes', 0),
            "reports": getattr(c, 'reports', 0)
        } for c in comments]
        return jsonify(comments_list), 200
    except Exception as e:
        print(f"[ERROR] Get Theory Comments: {e}")
        return jsonify([]), 200

# Route to post comment for theories / cold cases
@app.route('/api/v1/theories/<case_id>/comments', methods=['POST'])
def post_theory_comment(case_id):
    req_data = request.get_json() or {}
    try:
        new_comment = Comment(
            story_id=case_id,
            username=req_data.get('username', 'Anonyme'),
            text=req_data.get('text', req_data.get('content', ''))
        )
        db.session.add(new_comment)
        db.session.commit()
        return jsonify({"status": "success", "message": "Théorie publiée !"}), 201
    except Exception as e:
        db.session.rollback()
        print(f"[ERROR] Post Theory Comment: {e}")
        return jsonify({"status": "error", "message": "Erreur serveur."}), 500

# Dictionary to track IPs for each comment
ip_likes_tracker = {}

# Route to like a comment
@app.route('/api/v1/comments/<int:comment_id>/like', methods=['POST'])
@app.route('/api/v1/theories/<case_id>/<int:comment_id>/like', methods=['POST'])
def like_comment(comment_id, case_id=None):
    try:
        # Get the user IP address
        user_ip = request.remote_addr
        
        # Initialize the set for this comment if it does not exist
        if comment_id not in ip_likes_tracker:
            ip_likes_tracker[comment_id] = set()
            
        # Check if this IP already liked this comment
        if user_ip in ip_likes_tracker[comment_id]:
            return jsonify({"status": "error", "message": "Already liked by this IP"}), 403

        comment = Comment.query.get(comment_id)
        if comment:
            comment.likes = getattr(comment, 'likes', 0) + 1
            db.session.commit()
            
            # Save the IP to block future likes
            ip_likes_tracker[comment_id].add(user_ip)
            
            return jsonify({"status": "success", "likes": comment.likes}), 200
        
        return jsonify({"status": "error", "message": "Introuvable"}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500

# Route to report a comment
@app.route('/api/v1/comments/<int:comment_id>/report', methods=['POST'])
@app.route('/api/v1/theories/<case_id>/<int:comment_id>/report', methods=['POST'])
def report_comment(comment_id, case_id=None):
    try:
        comment = Comment.query.get(comment_id)
        if comment:
            comment.reports = getattr(comment, 'reports', 0) + 1
            db.session.commit()
            return jsonify({"status": "success", "reports": comment.reports}), 200
        return jsonify({"status": "error", "message": "Introuvable"}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500

# Load all routes from views
app.register_blueprint(app_views)

if __name__ == "__main__":
    # Start the server
    app.run(host="0.0.0.0", port=5000, debug=True)
