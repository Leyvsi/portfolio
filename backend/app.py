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
