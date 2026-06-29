from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_restx import Api, Resource, fields

app = Flask(__name__)
CORS(app)

# Initialize Swagger documentation
api = Api(
    app, 
    version='1.0', 
    title='API Les Petits Enquêteurs',
    description='Documentation interactive (Swagger) pour le portfolio',
    doc='/swagger/'
)

USERS_DATABASE = []
VISITS_COUNT = 0

ADMIN_CREDENTIALS = {
    "votre_identifiant_secret_leyvsi": "votre_mot_de_passe_leyvsi",
    "votre_identifiant_secret_melissa": "votre_mot_de_passe_melissa"
}

STORIES_PROPOSALS = []

VOTE_STORIES = [
    {"id": 1, "title": "Le Mystère de la Chambre 104", "summary": "Un dossier complexe impliquant des indices contradictoires laissés dans un hôtel abandonné.", "votes": 0},
    {"id": 2, "title": "Le Secret des Chuchotements", "summary": "Une série d'enregistrements audio anonymes reçus par une radio locale en 1994.", "votes": 0},
    {"id": 3, "title": "L'Ombre du Viaduc", "summary": "Une disparition inexpliquée survenue au cours d'une nuit de brouillard intense.", "votes": 0}
]

COMMENTS_DATABASE = {}

RESOLVED_STORIES = [
    {
        "id": 1,
        "title": "L'Affaire Kouri Richins (Résolue en 2025/2026)",
        "summary": "Une autrice de livres pour enfants sur le deuil est démasquée pour le meurtre par empoisonnement de son propre mari.",
        "content": "En 2022, Eric Richins meurt soudainement d'une overdose de fentanyl administrée à son insu. Son épouse, Kouri Richins, écrit peu après un livre à succès pour aider leurs enfants à surmonter la perte de leur père. L'enquête minutieuse de la police américaine menée sur ses appareils numériques révèle des recherches suspectes et des achats dissimulés de drogues dures. En mars 2026, un jury la déclare officiellement coupable de meurtre au premier degré.",
        "image_summary": "https://images.unsplash.com/photo-1506880018603-83d5b814b5a6?w=500&q=80",
        "image_full": "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?w=800&q=80"
    },
    {
        "id": 2,
        "title": "Le Tueur des Tueuses en Série (L'affaire Bruce Lindahl - Résolue fin 2024)",
        "summary": "Le meurtre non élucidé de Kathy Halle en 1979 trouve sa réponse grâce aux avancées spectaculaires de la généalogie génétique.",
        "content": "Pendant 45 ans, la disparition et la mort de Kathy Halle en Illinois sont restées un cold case frustrant. Fin 2024, le laboratoire DNA Labs International parvient à extraire une micro-trace d'ADN sur les vêtements conservés de la victime. Les résultats croisés établissent avec une certitude absolue la culpabilité de Bruce Lindahl, un tueur en série décédé depuis longtemps, apportant enfin des réponses et une clôture définitive à la famille.",
        "image_summary": "https://images.unsplash.com/photo-1530210124550-912dc1381cb8?w=500&q=80",
        "image_full": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=800&q=80"
    },
    {
        "id": 3,
        "title": "Le Mystère des Meurtres du Yogurt Shop (Résolu fin 2025/2026)",
        "summary": "Une tragédie texane datant de 1991 élucidée après l'identification ADN d'un suspect mort et l'exonération des accusés.",
        "content": "L'assassinat de quatre adolescentes dans une boutique de yaourts à Austin avait mené à l'incarcération injuste de quatre hommes. En septembre 2025, de nouvelles analyses d'empreintes génétiques avancées lient formellement le crime à Robert Brashers, un criminel décédé. En février 2026, un juge boucle définitivement l'affaire en déclarant l'innocence absolue des quatre hommes injustement poursuivis.",
        "image_summary": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=500&q=80",
        "image_full": "https://images.unsplash.com/photo-1509248961158-e54f6934749c?w=800&q=80"
    }
]

comment_model = api.model('Comment', {
    'username': fields.String(required=True),
    'text': fields.String(required=True)
})

@api.route('/api/visit')
class Visit(Resource):
    def post(self):
        global VISITS_COUNT
        VISITS_COUNT += 1
        return {"status": "success", "visits": VISITS_COUNT}, 200

@api.route('/api/stats')
class Stats(Resource):
    def get(self):
        return {"status": "success", "visits": VISITS_COUNT}, 200

@api.route('/api/stories')
class StoriesList(Resource):
    def get(self):
        return {"status": "success", "stories": RESOLVED_STORIES}, 200

@api.route('/api/comments/<string:item_id>')
class CommentsHandler(Resource):
    def get(self, item_id):
        comments = COMMENTS_DATABASE.get(item_id, [])
        return {"status": "success", "comments": comments}, 200

    @api.expect(comment_model)
    def post(self, item_id):
        data = request.get_json()
        username = data.get('username', 'Anonyme')
        text = data.get('text')
        if not text:
            return {"status": "error", "message": "Le commentaire ne peut pas être vide."}, 400
        if item_id not in COMMENTS_DATABASE:
            COMMENTS_DATABASE[item_id] = []
        COMMENTS_DATABASE[item_id].append({"username": username, "text": text})
        return {"status": "success", "comments": COMMENTS_DATABASE[item_id]}, 201

if __name__ == '__main__':
    app.run(debug=True, port=5000)
