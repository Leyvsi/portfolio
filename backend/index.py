from flask import Flask, jsonify
from flask_cors import CORS
from api.v1.views import app_views
from models import db, User, Comment # Import the SQLite database and models

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
    
    # Simple English comment: check and seed administrative credentials on startup
    admins_to_create = [
        {"username": "Leyvsi", "password": "sylvie"},
        {"username": "Mel95", "password": "melissa"}
    ]
    
    for admin_data in admins_to_create:
        existing_admin = User.query.filter_by(username=admin_data["username"]).first()
        if not existing_admin:
            admin_user = User(username=admin_data["username"], is_admin=True)
            admin_user.set_password(admin_data["password"])
            db.session.add(admin_user)
            db.session.commit()
            print(f"[*] Admin account {admin_data['username']} verified/created successfully.")

# Register your API blueprint routes
app.register_blueprint(app_views)

@app_views.route('/api/v1/stats', methods=['GET'])
def get_stats():
    # Simple English comment: query active counters directly from SQLite tables
    try:
        user_count = User.query.count()
        comment_count = Comment.query.count()
        reported_count = Comment.query.filter(Comment.reports > 0).count()
        
        return jsonify({
            "users": user_count,
            "comments": comment_count,
            "reports": reported_count
        }), 200
    except Exception:
        return jsonify({"users": 0, "comments": 0, "reports": 0}), 500

if __name__ == "__main__":
    # Run the server on port 5000
    app.run(host="0.0.0.0", port=5000, debug=True)
