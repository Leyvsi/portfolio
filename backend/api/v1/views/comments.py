from flask import jsonify, request
from api.v1.views import app_views
from models import db, Comment

# --- GET COMMENTS ---

@app_views.route('/stories/<string:story_id>/comments', methods=['GET'])
def get_story_comments(story_id):
    # Simple English comment: query database for this story's comments
    comments = Comment.query.filter_by(item_id=story_id, category='story').all()
    return jsonify([c.to_dict() for c in comments]), 200

@app_views.route('/theories/<string:theory_id>/comments', methods=['GET'])
def get_theory_comments(theory_id):
    # Simple English comment: query database for this theory's comments
    comments = Comment.query.filter_by(item_id=theory_id, category='theory').all()
    return jsonify([c.to_dict() for c in comments]), 200


# --- POST COMMENTS ---

@app_views.route('/stories/<string:story_id>/comments', methods=['POST'])
def post_story_comment(story_id):
    req_data = request.get_json() or {}
    
    # Simple English comment: create new story comment record
    new_comment = Comment(
        item_id=story_id,
        category='story',
        username=req_data.get('username', 'Anonyme'),
        text=req_data.get('text', '').strip()
    )
    
    db.session.add(new_comment)
    db.session.commit()
    
    return jsonify(new_comment.to_dict()), 201

@app_views.route('/theories/<string:theory_id>/comments', methods=['POST'])
def post_theory_comment(theory_id):
    req_data = request.get_json() or {}
    
    # Simple English comment: create new theory comment record
    new_comment = Comment(
        item_id=theory_id,
        category='theory',
        username=req_data.get('username', 'Anonyme'),
        text=req_data.get('text', '').strip()
    )
    
    db.session.add(new_comment)
    db.session.commit()
    
    return jsonify(new_comment.to_dict()), 201


# --- LIKES & REPORTS ---

@app_views.route('/comments/<int:comment_id>/like', methods=['POST'])
def like_comment(comment_id):
    # Simple English comment: increment comment likes by 1
    comment = Comment.query.get_or_404(comment_id)
    comment.likes += 1
    db.session.commit()
    return jsonify({"status": "success", "likes": comment.likes}), 200

@app_views.route('/comments/<int:comment_id>/report', methods=['POST'])
def report_comment(comment_id):
    # Simple English comment: increment comment safety reports by 1
    comment = Comment.query.get_or_404(comment_id)
    comment.reports += 1
    db.session.commit()
    return jsonify({"status": "success", "reports": comment.reports}), 200
