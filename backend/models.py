from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize SQLAlchemy
# Simple English comment: db instance used to define models and query SQLite
db = SQLAlchemy()

class User(db.Model):
    """
    Database model for user and admin accounts
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        # Simple English comment: hash password securely before saving
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        # Simple English comment: verify hashed password against input
        return check_password_hash(self.password_hash, password)

class Comment(db.Model):
    """
    Database model for user comments
    """
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.String(50), nullable=False) # ID of the story or theory
    category = db.Column(db.String(50), nullable=False) # 'story' or 'theory'
    username = db.Column(db.String(100), default="Anonyme") # Matches frontend key
    text = db.Column(db.Text, nullable=False)
    likes = db.Column(db.Integer, default=0) # Counter for likes
    reports = db.Column(db.Integer, default=0) # Counter for safety reports

    def to_dict(self):
        # Convert the SQL database object to a Python dictionary
        return {
            "id": self.id,
            "item_id": self.item_id,
            "category": self.category,
            "username": self.username,
            "text": self.text,
            "likes": self.likes,
            "reports": self.reports
        }
