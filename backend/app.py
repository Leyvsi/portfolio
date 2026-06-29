from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_restx import Api, Resource, fields

app = Flask(__name__)
CORS(app)

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
    },
    {
        "id": 3,
        "title": "Le Drame du Yogurt Shop : Justice et Erreurs à Austin",
        "summary": "Quatre adolescentes assassinées en 1991. Une affaire texane résolue en 2025/2026 qui met en lumière les failles du système.",
        "content": (
            "■ LA TRAGÉDIE ET LE SCANDALE\n"
            "Le 6 décembre 1991, quatre adolescentes sont exécutées dans une boutique de yaourts à Austin, le commerce étant ensuite incendié. "
            "La police subit une pression monumentale. En 1999, quatre jeunes suspects sont arrêtés. Deux sont condamnés à la prison à vie "
            "sur la base d'aveux controversés obtenus après des interrogatoires musclés de plus de 20 heures. En 2009, ils sont libérés suite à des doutes "
            "sur l'ADN, mais l'ombre du soupçon plane toujours. Le dénouement final survient via les techniques génétiques de pointe.\n\n"
            "■ LA SOUFFRANCE DES FAMILLES ET LES AVEUX DES PROCHES\n"
            "• Bob Ayers (Père d'Amy Ayers, victime) : « On nous a ballottés de tribunal en tribunal pendant trente ans. On nous a dit que les coupables "
            "étaient derrière les barreaux, puis qu'ils étaient innocents. Ce n'est pas une justice, c'est un calvaire sans fin. »\n"
            "• Un proche de Robert Brashers (Le véritable tueur identifié) : « Robert était un homme instable, violent, qui passait son temps à fuir "
            "la justice. Quand il s'est suicidé en 1999 lors d'un affrontement avec la police, nous savions qu'il cachait des choses horribles, mais "
            "personne n'imaginait qu'il était le monstre du Yogurt Shop. »\n\n"
            "■ LA PAROLE DE LA DEFENSE ET DE LA POLICE\n"
            "• L'Avocat des accusés à tort : « Mes clients ont eu leur vie brisée. Ils ont avoué sous la torture psychologique ce qu'ils n'avaient pas "
            "fait. Cette affaire est l'exemple parfait des dérives des faux aveux extorqués par la pression policière. »\n"
            "• Détective de la brigade criminelle d'Austin (Rapport de clôture) : « Le profil génétique extrait de la scène de crime correspond à 100% "
            "à l'ADN de Robert Brashers. L'analyse par cartographie chromosomique confirme sa présence active. Les suspects initiaux sont formellement "
            "et définitivement mis hors de cause. Ce dossier est officiellement clos. »\n\n"
            "■ LA DÉCISION DU JUGE\n"
            "• Le Juge fédéral (Clôturant l'affaire) : « Le tribunal ordonne l'effacement total des casiers et l'exonération pleine et entière des personnes "
            "injustement poursuivies. Que cette erreur serve de leçon mémorable à notre système judiciaire. »"
        ),
        "image_summary": "https://images.unsplash.com/photo-1543269664-76bc3997d9ea?w=500&q=80",
        "image_full": "https://images.unsplash.com/photo-1509248961158-e54f6934749c?w=800&q=80"
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
    },
    {
        "id": "cc3",
        "title": "Le Vol 814 : Le Passager Fantôme",
        "summary": "Un avion atterrit en 2011 avec un passager de moins à son bord. Les systèmes de sécurité n'indiquent aucune ouverture des portes en vol.",
        "content": (
            "■ L'IMPOSSIBLE DISPARITION\n"
            "Le 15 mai 2011, le vol charter 814 relie Lisbonne à Paris. À l'embarquement, la présence d'Arthur Vance est validée par les caméras et les agents de bord. "
            "Pourtant, à l'arrivée à Roissy, son siège est vide. Ses bagages à main sont toujours installés dans le compartiment supérieur.\n\n"
            "■ L'ENQUÊTE TECHNIQUE\n"
            "Les boîtes noires et les capteurs de pression certifient qu'aucune porte ni issue de secours n'a été manipulée durant les 2 heures et 15 minutes de trajet. "
            "Les toilettes et les espaces techniques ont été fouillés de fond en comble. Arthur Vance s'est littéralement volatilisé à 10 000 mètres d'altitude."
        ),
        "image": "https://images.unsplash.com/photo-1436491865332-7a61a109cc05?w=800&q=80"
    }
]

THEORIES_DATABASE = {
    "cc1": [
        {"id": 1, "text": "Disparition volontaire mise en scène. Le message sur le miroir servait à aiguiller les recherches sur une fausse piste mystique.", "likes": 12},
        {"id": 2, "text": "Accident de montagne nocturne. La neige a recouvert le corps dans une crevasse, et la veste a été déplacée plus tard par un rôdeur.", "likes": 5}
    ],
    "cc2": [
        {"id": 3, "text": "Un programme de protection de témoins qui a mal tourné ou une ancienne agente secrète laissée pour morte.", "likes": 24},
        {"id": 4, "text": "Les clés appartiennent à des casiers de stockage privés dans un port de plaisance hors de France.", "likes": 9}
    ],
    "cc3": [
        {"id": 5, "text": "Arthur Vance a utilisé une fausse identité et a réussi à s'échapper en s'habillant comme un membre du personnel navigant pendant l'escale ou avant le décollage.", "likes": 18},
        {"id": 6, "text": "Il s'est caché dans la trappe technique d'accès à la soute électronique sous la cabine avant l'atterrissage.", "likes": 14}
    ]
}

comment_model = api.model('Comment', {
    'username': fields.String(required=True, description="Nom de l'utilisateur"),
    'text': fields.String(required=True, description="Contenu du commentaire")
})

auth_model = api.model('UserAuth', {
    'username': fields.String(required=True, description="Nom d'utilisateur"),
    'password': fields.String(required=True, description="Mot de passe")
})

@api.route('/api/auth/register')
class UserRegister(Resource):
    @api.expect(auth_model)
    @api.response(201, 'Compte créé avec succès')
    @api.response(400, 'Nom d’utilisateur déjà existant ou invalide')
    def post(self):
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        
        if not username or not password:
            return {"status": "error", "message": "Tous les champs sont obligatoires."}, 400
            
        if username in ADMIN_CREDENTIALS or any(u['username'] == username for u in USERS_DATABASE):
            return {"status": "error", "message": "Ce nom d'utilisateur n'est pas disponible."}, 400
            
        USERS_DATABASE.append({"username": username, "password": password})
        return {"status": "success", "message": "Inscription réussie."}, 201

@api.route('/api/auth/login')
class UserLogin(Resource):
    @api.expect(auth_model)
    @api.response(200, 'Connexion réussie')
    @api.response(401, 'Identifiants invalides')
    def post(self):
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        
        user_match = next((u for u in USERS_DATABASE if u['username'] == username and u['password'] == password), None)
        
        if user_match:
            return {
                "status": "success", 
                "message": f"Bienvenue, session utilisateur activée pour {username}.",
                "role": "user"
            }, 200
            
        return {"status": "error", "message": "Identifiants invalides. Accès refusé."}, 401

@api.route('/api/admin/login')
class AdminLogin(Resource):
    @api.expect(auth_model)
    @api.response(200, 'Connexion réussie')
    @api.response(401, 'Identifiants invalides')
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if username in ADMIN_CREDENTIALS and ADMIN_CREDENTIALS[username] == password:
            return {
                "status": "success", 
                "message": f"Bienvenue, session admin activée pour {username}.",
                "token": "fake-jwt-token-for-portfolio-demonstration",
                "redirect": "admin-dashboard.html"
            }, 200
            
        return {"status": "error", "message": "Identifiants invalides. Accès refusé."}, 401

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

@api.route('/api/coldcases')
class ColdCasesList(Resource):
    def get(self):
        return {"status": "success", "cold_cases": COLD_CASES}, 200

@api.route('/api/theories/<string:case_id>')
class TheoriesHandler(Resource):
    def get(self, case_id):
        theories = THEORIES_DATABASE.get(case_id, [])
        return {"status": "success", "theories": theories}, 200

    def post(self, case_id):
        data = request.get_json()
        text = data.get('text', '').strip()
        if not text:
            return {"status": "error", "message": "Le texte ne peut pas être vide."}, 400
        if case_id not in THEORIES_DATABASE:
            THEORIES_DATABASE[case_id] = []
        
        new_id = len(THEORIES_DATABASE[case_id]) + 1
        THEORIES_DATABASE[case_id].append({"id": new_id, "text": text, "likes": 0})
        return {"status": "success", "theories": THEORIES_DATABASE[case_id]}, 201

@api.route('/api/theories/<string:case_id>/<int:theory_id>/like')
class LikeTheoryHandler(Resource):
    def post(self, case_id, theory_id):
        if case_id in THEORIES_DATABASE:
            for theory in THEORIES_DATABASE[case_id]:
                if theory['id'] == theory_id:
                    theory['likes'] += 1
                    return {"status": "success", "likes": theory['likes']}, 200
        return {"status": "error", "message": "Théorie introuvable."}, 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
