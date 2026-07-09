import os
from flask import jsonify, render_template_string
from api.v1.views import app_views

data_store = {
    "visites": 142,
    "histoires": [
        {"id": "1", "title": "L'Affaire du Tueur du Zodiaque", "summary": "Cryptogrammes non résolus et traque infernale.", "votes": 14},
        {"id": "2", "title": "La Colonie de Roanoke", "summary": "115 colons volatilisés en ne laissant qu'un mot gravé.", "votes": 29},
        {"id": "3", "title": "Le Mystère du Col Dyatlov", "summary": "Neuf randonneurs russes meurent de façon inexplicable.", "votes": 42}
    ],
    "commentaires_resolus": {"1": [], "2": [], "3": []},
    "theories": {"cc1": [], "cc2": [], "cc3": []},
    "commentaires_theories": {},
    "updates": {"cc1": [], "cc2": [], "cc3": []},
    "utilisateurs": ["Lupin99", "SherlockParis"]
}

@app_views.route('/stats', methods=['GET'])
def get_stats():
    return jsonify({"visits": data_store["visites"]}), 200

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
