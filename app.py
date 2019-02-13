from flask import Flask
from flask_restplus import Api, Resource, fields
from expert import InreferenceEngine, Personne

app = Flask(__name__)
api = Api(app, version='1.0', title='System Ekspercki Api', \
          description='Dostęp przez interfejs RESTFul API do systemu eksperckiego',
          default="Wywołanie modelu",
          default_label="Przestrzeń podstawowa")

# {
#   "age": 5,
#   "glycemia": 11,
#   "shakiness": false,
#   "hunger": false,
#   "sweating": false,
#   "headach": false,
#   "diabetic_parents": true,
#   "pale": false,
#   "urination": true,
#   "thirst": true,
#   "blurred_vision": false,
#   "dry_mouth": false,
#   "smelling_breath": false,
#   "shortness_of_breath": false
# }

person_model = api.model('person', {
    'age': fields.Integer(2, description='Wiek pacjenta', required=True, min=1, max=90),
    'glycemia': fields.Integer(5, description='Poziom glukozy', required=True, min=3, max=7),
    'shakiness': fields.Boolean('False', description='Drgawki', required=True),
    'hunger': fields.Boolean('False', description='Wzmożone łaknienie', required=True),
    'sweating': fields.Boolean('False', description='Wzmożona potliwość', required=True),
    'headach': fields.Boolean('False', description='Częste bóle głowy', required=True),
    'diabetic_parents': fields.Boolean('True', description='Rodzice z cukrzycą', required=True),
    'pale': fields.Boolean('Flase', description='Bladość skóry', required=True),
    'urination': fields.Boolean('True', description='Wzmożone wydalanie moczu', required=True),
    'thirst': fields.Boolean('True', description='Nadmierne pragnienie', required=True),
    'blurred_vision': fields.Boolean('False', description='Występuje nieostre widzenie', required=True),
    'dry_mouth': fields.Boolean('True', description='Suchość ust', required=True),
    'smelling_breath': fields.Boolean('False', description='Nieświeży oddech', required=True),
    'shortness_of_breath': fields.Boolean('False', description='Krótki oddech', required=True)
})

@api.route('/diagnoza')
class AllBooks(Resource):

    @api.expect(person_model)
    def post(self):
        """
        dodaj dane z wywiadu o pacjencie
        """
        new_data = api.payload
        print(api.payload)
        expert = InreferenceEngine()
        expert.reset()
        expert.declare(Personne(age=int(new_data['age']),
                                glycemie=int(new_data['glycemia']),
                                shakiness=bool(new_data['shakiness']),
                                hunger=bool(new_data['hunger']),
                                sweating=bool(new_data['sweating']),
                                headach=bool(new_data['headach']),
                                diabetic_parents=bool(new_data['diabetic_parents']),
                                pale=bool(new_data['pale']),
                                urination=bool(new_data['urination']),
                                thirst=bool(new_data['thirst']),
                                blurred_vision=bool(new_data['blurred_vision']),
                                dry_mouth=bool(new_data['dry_mouth']),
                                smelling_breath=bool(new_data['smelling_breath']),
                                shortness_of_breath=bool(new_data['shortness_of_breath']),
                                ))
        expert.run()
        result = expert.get_effect()
        object = expert.facts
        if len(result):
            result
        else:
            result=['Brak ostrzeżeń']
        #print(result)
        #print(object)
        # all_books.append(new_book)
        return {'diagnoza': result}, 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=80)
