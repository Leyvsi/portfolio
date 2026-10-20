import os
from flask import jsonify, request, render_template_string
from api.v1.views import app_views
from api.v1.views.permissions import admin_required
from models import db, Report, User


@app_views.route('/reports', methods=['POST'])
def post_report():
    req_data = request.get_json(silent=True)

    if not isinstance(req_data, dict):
        return jsonify({
            "status": "error",
            "message": "Corps JSON invalide."
        }), 400

    report_type = req_data.get("type")
    target_id = req_data.get("target_id")
    reason = req_data.get("reason")

    if (
        not isinstance(report_type, str)
        or not report_type.strip()
        or not isinstance(target_id, str)
        or not target_id.strip()
        or not isinstance(reason, str)
        or not reason.strip()
    ):
        return jsonify({
            "status": "error",
            "message": "type, target_id et reason sont obligatoires."
        }), 400

    report = Report(
        type=report_type.strip(),
        target_id=target_id.strip(),
        reason=reason.strip()
    )

    db.session.add(report)
    db.session.commit()

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

    user.is_banned = True
    db.session.commit()

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
