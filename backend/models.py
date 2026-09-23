from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()


class User(db.Model):
    """User and administrator account."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    stories = db.relationship("Story", back_populates="author")
    comments = db.relationship("Comment", back_populates="user")
    votes = db.relationship("Vote", back_populates="user")
    proposals = db.relationship("Proposal", back_populates="user")
    theories = db.relationship("Theory", back_populates="author")

    def set_password(self, password):
        """Hash the password before storing it."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check a password against its hash."""
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "is_admin": self.is_admin,
            "created_at": self.created_at.isoformat()
            if self.created_at else None
        }


class Category(db.Model):
    """Story category."""

    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)

    stories = db.relationship("Story", back_populates="category")


class Story(db.Model):
    """Criminal story."""

    __tablename__ = "stories"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    summary = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(500))

    category_id = db.Column(
        db.Integer,
        db.ForeignKey("categories.id"),
        nullable=False
    )

    author_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    category = db.relationship("Category", back_populates="stories")
    author = db.relationship("User", back_populates="stories")

    comments = db.relationship(
        "Comment",
        back_populates="story",
        cascade="all, delete-orphan"
    )

    votes = db.relationship(
        "Vote",
        back_populates="story",
        cascade="all, delete-orphan"
    )

    theories = db.relationship(
        "Theory",
        back_populates="story",
        cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "summary": self.summary,
            "content": self.content,
            "image_url": self.image_url,
            "category_id": self.category_id,
            "author_id": self.author_id,
            "created_at": self.created_at.isoformat()
            if self.created_at else None,
            "updated_at": self.updated_at.isoformat()
            if self.updated_at else None
        }


class Theory(db.Model):
    """Theory submitted for a story."""

    __tablename__ = "theories"

    id = db.Column(db.Integer, primary_key=True)

    story_id = db.Column(
        db.Integer,
        db.ForeignKey("stories.id"),
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=True
    )

    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    likes = db.Column(db.Integer, default=0, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    story = db.relationship("Story", back_populates="theories")
    author = db.relationship("User", back_populates="theories")


class Comment(db.Model):
    """Comment posted on a story."""

    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)

    story_id = db.Column(
        db.Integer,
        db.ForeignKey("stories.id"),
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=True
    )

    username = db.Column(db.String(100), default="Anonyme")
    text = db.Column(db.Text, nullable=False)

    likes = db.Column(db.Integer, default=0, nullable=False)
    reports = db.Column(db.Integer, default=0, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    story = db.relationship("Story", back_populates="comments")
    user = db.relationship("User", back_populates="comments")

    def to_dict(self):
        return {
            "id": self.id,
            "story_id": self.story_id,
            "user_id": self.user_id,
            "username": self.username,
            "text": self.text,
            "likes": self.likes,
            "reports": self.reports,
            "created_at": self.created_at.isoformat()
            if self.created_at else None
        }


class Vote(db.Model):
    """Vote submitted by a user for a story."""

    __tablename__ = "votes"

    id = db.Column(db.Integer, primary_key=True)

    story_id = db.Column(
        db.Integer,
        db.ForeignKey("stories.id"),
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    story = db.relationship("Story", back_populates="votes")
    user = db.relationship("User", back_populates="votes")

    __table_args__ = (
        db.UniqueConstraint(
            "user_id",
            "story_id",
            name="unique_user_story_vote"
        ),
    )


class Proposal(db.Model):
    """Story proposal submitted by a user."""

    __tablename__ = "proposals"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)

    status = db.Column(
        db.String(20),
        default="pending",
        nullable=False
    )

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    user = db.relationship("User", back_populates="proposals")