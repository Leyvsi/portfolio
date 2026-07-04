from flask import jsonify
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
