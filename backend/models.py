from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy
# Simple English comment: db instance used to interact with the SQLite database
db = SQLAlchemy()

class Comment(db.Model):
    """
    Database model for user comments (stories and theories)
    """
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.String(50), nullable=False) # ID of the story or theory
    category = db.Column(db.String(50), nullable=False) # 'story' or 'theory'
    username = db.Column(db.String(100), default="Anonyme") # Matches frontend key
    text = db.Column(db.Text, nullable=False)
    likes = db.Column(db.Integer, default=0) # Counter for likes
    reports = db.Column(db.Integer, default=0) # Counter for moderation reports

    def to_dict(self):
        # Convert the SQL database object to a Python dictionary for JSON responses
        return {
            "id": self.id,
            "item_id": self.item_id,
            "category": self.category,
            "username": self.username,
            "text": self.text,
            "likes": self.likes,
            "reports": self.reports
        }

