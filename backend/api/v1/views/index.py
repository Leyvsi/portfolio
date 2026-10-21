import os
from flask import jsonify, request, render_template_string
from api.v1.views import app_views
from api.v1.views.permissions import admin_required, get_authenticated_user
from models import db, Report, User, Comment
from sqlalchemy.exc import SQLAlchemyError
from api.v1.views.write_support import api_error


@app_views.route('/reports', methods=['POST'])
def post_report():
    user, error_response = get_authenticated_user()

    if error_response:
        return error_response

    req_data = request.get_json(silent=True)

    if not isinstance(req_data, dict):
        return jsonify({
            "status": "error",
            "message": "Corps JSON invalide."
        }), 400

    values = {}
    for field in ("type", "target_id", "reason"):
        value = req_data.get(field)
        if not isinstance(value, str) or not value.strip():
            return jsonify({
                "status": "error",
                "message": "type, target_id et reason doivent etre des chaines non vides."
            }), 400
        values[field] = value.strip()

    target_models = {"comment": Comment}
    target_model = target_models.get(values["type"])
    if target_model is None:
        return jsonify({
            "status": "error",
            "message": "Type de signalement non pris en charge."
        }), 400

    target_id = values["target_id"]
    target_digits = target_id.lstrip("0")
    if (
        not target_id.isascii()
        or not target_id.isdecimal()
        or not target_digits
        or len(target_digits) > 10
    ):
        return jsonify({
            "status": "error",
            "message": "target_id doit etre un entier positif valide."
        }), 400

    target_value = int(target_digits)
    if target_value > 2147483647:
        return jsonify({
            "status": "error",
            "message": "target_id doit etre un entier positif valide."
        }), 400

    if db.session.get(target_model, target_value) is None:
        return jsonify({
            "status": "error",
            "message": "Cible du signalement introuvable."
        }), 404

    report = Report(
        type=values["type"],
        target_id=str(target_value),
        reason=values["reason"]
    )

    try:
        db.session.add(report)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": "Impossible d'enregistrer le signalement."
        }), 500

    return jsonify({
        "status": "success",
        "report": report.to_dict()
    }), 201


@app_views.route('/admin/reports', methods=['GET'])
@admin_required
def get_admin_reports():
    reports = Report.query.order_by(
        Report.created_at.desc()
    ).all()

    return jsonify([
        report.to_dict()
        for report in reports
    ]), 200


@app_views.route('/admin/users/<string:username>/ban', methods=['DELETE'])
@admin_required
def ban_user(username):
    user = User.query.filter_by(
        username=username
    ).first()

    if not user:
        return jsonify({
            "error": "User not found"
        }), 404

    try:
        user.is_banned = True
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return api_error("Impossible de bannir l'utilisateur.", 500)

    return jsonify({
        "status": "success",
        "message": f"L'utilisateur {username} a été banni"
    }), 200

@app_views.route('/swagger.json', methods=['GET'])
def get_swagger_json():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    swagger_path = os.path.join(current_dir, '../swagger.json')
    try:
        with open(swagger_path, 'r', encoding='utf-8') as f:
            import json
            return jsonify(json.load(f)), 200
    except FileNotFoundError:
        return jsonify({"error": "Swagger file not found"}), 404

@app_views.route('/swagger', methods=['GET'])
def oauth_swagger():
    swagger_ui_html = """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <title>Swagger UI - Les Petits Enquêteurs</title>
        <link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/4.15.5/swagger-ui.min.css">
        <style>html { box-sizing: border-box; overflow-y: scroll; } *, *:before, *:after { box-sizing: inherit; } body { margin:0; background: #fafafa; }</style>
    </head>
    <body>
        <div id="swagger-ui"></div>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/4.15.5/swagger-ui-bundle.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/4.15.5/swagger-ui-standalone-preset.min.js"></script>
        <script>
        window.onload = function() {
            window.ui = SwaggerUIBundle({
                url: "/api/v1/swagger.json",
                dom_id: '#swagger-ui',
                deepLinking: true,
                presets: [SwaggerUIBundle.presets.apis],
                plugins: [SwaggerUIBundle.plugins.DownloadUrl],
                layout: "BaseLayout"
            });
        };
        </script>
    </body>
    </html>
    """
    return render_template_string(swagger_ui_html)
