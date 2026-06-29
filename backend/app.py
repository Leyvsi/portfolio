from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_restx import Api, Resource, fields

app = Flask(__name__)
CORS(app)

# Simple English comments for documentation
# Security authorization description for Swagger
authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': "Ajoutez votre jeton sous la forme : Bearer <votre_token>"
    }
}

api = Api(
    app, 
    version='1.0', 
    title='API Les Petits Enquêteurs',
    description='Documentation interactive (Swagger) pour le portfolio. Testez les accès utilisateurs et admin ici.',
    doc='/swagger/',
    authorizations=authorizations
)

# Simulated in-memory databases
USERS_DATABASE = []
VISITS_COUNT = 0

ADMIN_CREDENTIALS = {
    "Leyvsi": "sylvie",
    "Melissa": "melissa123"
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
        "title": "L'Affaire Kouri Richins : Le Poison des Mots",
        "summary": "Une autrice de livres sur le deuil démasquée pour l'empoisonnement de son époux. Plongez au cœur des témoignages et du procès.",
        "content": (
            "■ LE CONTEXTE ET LE DRAME\n"
            "En mars 2022, à Kamas dans l'Utah, Eric Richins, un père de famille sans problème de santé, est retrouvé sans vie au pied de son lit. "
            "L'autopsie révèle l'impensable : une concentration massive de fentanyl, équivalente à cinq fois la dose létale, administrée par voie orale. "
            "Quelques mois plus tard, sa veuve Kouri Richins publie un livre pour enfants pour surmonter le deuil. Elle écume les plateaux TV, "
            "s'affichant en mère courage.\n\n"
            "■ LES PAROLES DES PROCHES ET TÉMOINS\n"
            "• Amy Richins (Sœur de la victime) : « Dès le premier jour, nous avons su que quelque chose ne collait pas. Eric nous avait dit peu avant "
            "sa mort que si quelque chose lui arrivait, Kouri en serait responsable. Elle avait déjà tenté de l'empoisonner lors d'un voyage en Grèce "
            "et à la Saint-Valentin. »\n"
            "• Un ami proche de Kouri (Sous anonymat) : « On la voyait à la télévision pleurer son mari, et le lendemain, elle organisait des fêtes "
            "pour célébrer la signature de ses contrats immobiliers. C'était un double visage terrifiant. »\n\n"
            "■ L'ENQUÊTE ET LA PAROLE DES POLICIERS\n"
            "• Détective principal du comté de Summit : « L'analyse technique de son téléphone a été le point de rupture. Nous avons découvert des "
            "recherches Google explicites : 'La police peut-elle analyser le fentanyl dans une autopsie ?' ou encore 'Comment obtenir un certificat de "
            "décès rapidement'. En remontant ses messages supprimés, nous avons trouvé ses échanges avec un revendeur local, C.L., à qui elle avait "
            "acheté des pilules de fentanyl pour 900 dollars juste avant la mort d'Eric. »\n\n"
            "■ LE CHOC DU PROCÈS : AVOCATS ET JUGES\n"
            "• Le Procureur lors de sa plaidoirie finale : « L'accusée a transformé le meurtre de son mari en une opération marketing. Elle a "
            "secrètement modifié les polices d'assurance-vie à son nom et a empoisonné son époux pour financer son train de vie. Sa cupidité n'a eu aucune limite. »\n"
            "• L'Avocat de la défense : « Ce dossier ne repose que sur des spéculations et des preuves de moralité. Il n'y a aucune preuve physique "
            "directe montrant Kouri en train de glisser ce produit dans le verre d'Eric cette nuit-là. »\n"
            "• Le Juge (Prononçant le maintien en détention et validant le verdict) : « Les preuves numériques et les témoignages concordants présentent "
            "un danger manifeste pour la société et une préméditation froide. »"
        ),
        "image_summary": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=500&q=80",
        "image_full": "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?w=800&q=80"
    },
    {
        "id": 2,
        "title": "Le Tueur des Tueuses : L'Affaire Bruce Lindahl",
        "summary": "Le calvaire de Kathy Halle en 1979 résolu 45 ans plus tard. Découvrez les déclarations poignantes de sa famille et des scientifiques.",
        "content": (
            "■ UN COLD CASE DE 45 ANS\n"
            "Le 29 mars 1979, Kathy Halle, 19 ans, quitte son appartement de North Aurora pour se rendre à son travail. Elle n'y arrivera jamais. "
            "Son corps est retrouvé des semaines plus tard dans la rivière Fox. L'enquête piétine, laissant une famille brisée dans l'ignorance. "
            "Fin 2024, la science bouleverse le dossier grâce à la généalogie génétique.\n\n"
            "■ LE CRI DU CŒUR DE LA FAMILLE\n"
            "• Communiqué officiel de la Famille Halle (Fin 2024) : « Pendant quarante-cinq ans, nous avons vécu avec un espace vide dans nos cœurs "
            " et une question constante : pourquoi ? Nous pensions mourir sans savoir. Ce soulagement est immense, même si la douleur de sa perte "
            "ne s'effacera jamais. Kathy était une jeune fille pleine de vie. »\n\n"
            "■ LES EXPLICATIONS DES SCIENTIFIQUES ET ENQUÊTEURS\n"
            "• L'expert légiste de DNA Labs International : « Nous avons utilisé des technologies d'enrichissement d'ADN qui n'existaient pas il y a dix ans. "
            "À partir d'une micro-trace prélevée sur les scellés textiles de 1979, nous avons extrait un marqueur parfait. Ce marqueur a été intégré aux "
            "bases généalogiques publiques, construisant un arbre familial qui convergeait vers un seul homme. »\n"
            "• Le Chef de la Police de North Aurora : « Bruce Lindahl était un monstre. Il est mort en 1981 en poignardant un jeune homme, se tuant "
            "accidentellement avec son propre couteau lors de la lutte. Grâce à la résolution du dossier Kathy Halle, nous l'avons relié à au moins quatre "
            "autres meurtres commis à la fin des années 70. Il a emporté ses secrets dans la tombe, mais la science l'a démasqué. »\n\n"
            "■ LE POINT DE VUE DE LA JUSTICE\n"
            "• Le Procureur du comté de Kane : « Si Bruce Lindahl était vivant aujourd'hui, nos services auraient requis la peine maximale sans "
            "la moindre hésitation. Ce dossier prouve qu'aucun criminel ne peut définitivement dormir sur ses deux oreilles : le temps n'efface pas les preuves. »"
        ),
        "image_summary": "https://images.unsplash.com/photo-1530210124550-912dc1381cb8?w=500&q=80",
        "image_full": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=800&q=80"
    }
]

COLD_CASES = [
    {
        "id": "cc1",
        "title": "Le Mystère d'Anthonioz : Les Empreintes de la Nuit",
        "summary": "En 1994, un étudiant sans histoire disparaît d'une petite station alpine. Seuls sa veste et un message cryptique sur un miroir ont été retrouvés.",
        "content": (
            "■ LES FAITS\n"
            "Le 12 janvier 1994, par une nuit de tempête à Les Carroz, Marc Anthonioz, 21 ans, quitte son studio pour acheter des cigarettes. "
            "Il ne reviendra jamais. Le lendemain, la police découvre sa veste de ski à trois kilomètres de là, pliée soigneusement sur un banc de pierre, "
            "sans aucune trace de pas autour à cause de la neige fraîche.\n\n"
            "■ LES INDICES TROUVÉS\n"
            "Dans sa chambre, les enquêteurs relèvent une inscription tracée à la craie sur le miroir de la salle de bain : 'Le chiffre 7 sait'. "
            "Aucun retrait bancaire n'a été effectué, et ses papiers d'identité sont restés dans son portefeuille sur la table."
        ),
        "image": "https://images.unsplash.com/photo-1518241353330-0f7941c2d9b5?w=800&q=80"
    },
    {
        "id": "cc2",
        "title": "L'Inconnue de la Plage de Noirval",
        "summary": "Une femme retrouvée inconsciente sur le sable en 2003 avec des clés uniques mais sans aucun souvenir ni identité. Le mystère reste entier.",
        "content": (
            "■ L'AUBE DU MYSTÈRE\n"
            "Le 4 août 2003, des pêcheurs découvrent une femme d'environ 30 ans gisant sur une plage isolée de Normandie. "
            "Elle survit mais souffre d'une amnésie rétrograde totale et absolue. Elle ne reconnaît aucun nom, aucun visage, et parle trois langues sans accent distinct.\n\n"
            "■ LE SEUL INDICE PHYSIQUE\n"
            "Dans sa poche, un trouseau de trois clés anciennes numérotées '102', '104' et '108'. Toutes les recherches menées auprès des hôtels, "
            "des banques et des consignes de gares de la région n'ont jamais permis de trouver les serrures correspondantes."
        ),
        "image": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800&q=80"
    }
]

THEORIES_DATABASE = {
    "cc1": [
        {"id": 1, "text": "Disparition volontaire mise en scène. Le message sur le miroir servait à aiguiller les recherches.", "likes": 12, "liked_by": []},
        {"id": 2, "text": "Accident de montagne nocturne. La neige a recouvert le corps dans une crevasse.", "likes": 5, "liked_by": []}
    ],
    "cc2": [
        {"id": 3, "text": "Un programme de protection de témoins qui a mal tourné.", "likes": 24, "liked_by": []}
    ]
}

# Swagger data validation models
comment_model = api.model('Comment', {
    'username': fields.String(required=True, description="Nom de l'utilisateur"),
    'text': fields.String(required=True, description="Contenu du commentaire")
})

auth_model = api.model('UserAuth', {
    'username': fields.String(required=True, description="Nom d'utilisateur"),
    'password': fields.String(required=True, description="Mot de passe")
})

change_password_model = api.model('ChangePassword', {
    'username': fields.String(required=True, description="Nom de l'utilisateur"),
    'current_password': fields.String(required=True, description="Ancien mot de passe"),
    'new_password': fields.String(required=True, description="Nouveau mot de passe")
})

register_model = api.model('UserRegister', {
    'username': fields.String(required=True, description="Nom d'utilisateur"),
    'email': fields.String(required=True, description="Adresse mail"),
    'password': fields.String(required=True, description="Mot de passe")
})

like_model = api.model('LikeTheory', {
    'username': fields.String(required=True, description="Nom de l'utilisateur qui vote")
})

@api.route('/api/auth/register')
class UserRegister(Resource):
    @api.expect(register_model)
    def post(self):
        # Handles user registration with max 50 chars validation
        data = request.get_json()
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()
        
        if not username or not password or not email:
            return {"status": "error", "message": "Tous les champs sont obligatoires."}, 400
            
        if len(username) > 50:
            return {"status": "error", "message": "Le nom d'utilisateur ne doit pas dépasser 50 caractères."}, 400
            
        if username in ADMIN_CREDENTIALS or any(u['username'] == username for u in USERS_DATABASE):
            return {"status": "error", "message": "Ce nom d'utilisateur n'est pas disponible."}, 400
            
        USERS_DATABASE.append({"username": username, "email": email, "password": password})
        return {"status": "success", "message": "Inscription réussie."}, 201

@api.route('/api/auth/login')
class UserLogin(Resource):
    @api.expect(auth_model)
    def post(self):
        # Authenticates regular users
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        user_match = next((u for u in USERS_DATABASE if u['username'] == username and u['password'] == password), None)
        if user_match:
            return {"status": "success", "message": f"Bienvenue {username}.", "role": "user"}, 200
        return {"status": "error", "message": "Identifiants invalides."}, 401

@api.route('/api/admin/login')
class AdminLogin(Resource):
    @api.expect(auth_model)
    def post(self):
        # Authenticates system administrators
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        if username in ADMIN_CREDENTIALS and ADMIN_CREDENTIALS[username] == password:
            return {"status": "success", "message": f"Bienvenue Admin {username}.", "token": "fake-jwt-token", "redirect": "admin-dashboard.html"}, 200
        return {"status": "error", "message": "Accès refusé."}, 401

@api.route('/api/user/profile/<string:username>')
class UserProfile(Resource):
    def get(self, username):
        # Returns specific user profile details
        user_match = next((u for u in USERS_DATABASE if u['username'] == username), None)
        if user_match:
            return {
                "status": "success",
                "profile": {
                    "username": user_match["username"],
                    "email": user_match.get("email", "Non renseignée")
                }
            }, 200
        return {"status": "error", "message": "Utilisateur introuvable."}, 404

@api.route('/api/user/change-password')
class ChangePassword(Resource):
    @api.expect(change_password_model)
    def post(self):
        # Handles secure password modifications
        data = request.get_json()
        username = data.get('username')
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        user_match = next((u for u in USERS_DATABASE if u['username'] == username), None)
        if not user_match:
            return {"status": "error", "message": "Utilisateur introuvable."}, 404
        if user_match["password"] != current_password:
            return {"status": "error", "message": "L'ancien mot de passe est incorrect."}, 400
        user_match["password"] = new_password
        return {"status": "success", "message": "Mot de passe modifié avec succès !"}, 200

@api.route('/api/coldcases')
class ColdCasesList(Resource):
    def get(self):
        # Lists all available cold cases
        return {"status": "success", "cold_cases": COLD_CASES}, 200

@api.route('/api/coldcases/<string:case_id>')
class ColdCaseDetail(Resource):
    def get(self, case_id):
        # Fetches details for a specific single cold case
        case_match = next((c for c in COLD_CASES if c['id'] == case_id), None)
        if case_match:
            return {"status": "success", "cold_case": case_match}, 200
        return {"status": "error", "message": "Affaire introuvable."}, 404

@api.route('/api/theories/<string:case_id>')
class TheoriesHandler(Resource):
    def get(self, case_id):
        # Returns public theories related to a case
        theories = THEORIES_DATABASE.get(case_id, [])
        return {"status": "success", "theories": theories}, 200

@api.route('/api/theories/<string:case_id>/<int:theory_id>/like')
class LikeTheoryHandler(Resource):
    @api.expect(like_model)
    def post(self, case_id, theory_id):
        # Adds a unique like per user to a selected case theory
        data = request.get_json() or {}
        username = data.get('username', '').strip()
        
        if not username:
            return {"status": "error", "message": "Vous devez être connecté pour aimer une théorie."}, 401

        if case_id in THEORIES_DATABASE:
            for theory in THEORIES_DATABASE[case_id]:
                if theory['id'] == theory_id:
                    if "liked_by" not in theory:
                        theory["liked_by"] = []
                    
                    if username in theory["liked_by"]:
                        return {"status": "error", "message": "Vous avez déjà voté pour cette théorie !"}, 400
                    
                    theory["liked_by"].append(username)
                    theory['likes'] += 1
                    return {"status": "success", "likes": theory['likes']}, 200
        return {"status": "error", "message": "Théorie introuvable."}, 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
