"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User,Characters,Planets,Fav_Planets,Fav_Characters
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)



# [GET]Listar todos los usuarios.

@app.route('/user', methods=['GET'])
def get_user():
    all_users=User.query.all()
    results= list( map( lambda user:user.serialize(), all_users ))
 
  
    return jsonify( results), 200
   


#  ['GET']Listar todos los Characters.

@app.route('/Characters', methods=['GET'])
def get_Character():
    all_Characters=Characters.query.all()
    results= list( map( lambda Characters:Characters.serialize(), all_Characters ))
    
    return jsonify( results), 200

#  ['GET']Listar la información de un solo Character

@app.route('/Characters/<int:Character_id>', methods=['GET'])
def get_person(Character_id):
    person = Characters.query.get(Character_id)

    
    return jsonify(person.serialize()), 200

#  ['GET'] Listar todos los  characters favoritos.

@app.route('/fav_characters', methods=['GET'])
def get_fav_characters():
    fav_characters = Fav_Characters.query.all()
    results = list(map(lambda Characters: Characters.serialize(), fav_characters))

    return jsonify(results), 200


#  ['GET']Listar los registros de planets.

@app.route('/planets', methods=['GET'])
def get_planets():
    all_planets=Planets.query.all()
    results= list( map( lambda Planets:Planets.serialize(), all_planets ))
    
    return jsonify( results), 200

#  ['GET'] Listar la información de un solo planet

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planets.query.get(planet_id)


    return jsonify(planet.serialize()), 200

    #  ['GET'] Listar todos los  planets favoritos.

@app.route('/fav_planets', methods=['GET'])
def get_fav_planets():
    fav_planets = Fav_Planets.query.all()
    results = list(map(lambda Planets: Planets.serialize(), fav_planets))

    return jsonify(results), 200


#^[POST] añade un nuevo character

@app.route('/characters', methods=['POST'])
def add_new_character():

    request_body_character = request.get_json()

    new_character = Characters(
        name=request_body_character["name"],
        height=request_body_character["height"],
        mass=request_body_character["mass"],
        hair_color=request_body_character["hair_color"],
        skin_color=request_body_character["skin_color"], 
        eye_color=request_body_character["eye_color"], 
        birth_year=request_body_character["birth_year"],
        gender=request_body_character["gender"],
           )
    db.session.add(new_character)
    db.session.commit()

    return jsonify(request_body_character), 200

#^[POST] añade un nuevo planeta 

@app.route('/planets', methods=['POST'])
def add_new_planet():

    body = request.get_json()
    
    new_planet = Planets(
        name=body["name"],
        population=body["population"],
        terrain=body["terrain"],
        climate=body["climate"],
        diameter=body["diameter"]
    )
    
    db.session.add(new_planet)
    db.session.commit()

    return jsonify(body), 200

# [POST] Añade una nuevo Character favorito.

@app.route('/fav_characters', methods=['POST'])
def add_new_fav_character():

    request_body_fav_character = request.get_json()

    new_fav_character = Fav_Characters(
    character=request_body_fav_character["character"], 
    user=request_body_fav_character["user"]
    )
    db.session.add(new_fav_character)
    db.session.commit()

    return jsonify(request_body_fav_character), 200

# [POST] Añade un nuevo planet favorito .

@app.route('/fav_planets', methods=['POST'])
def add_new_fav_planet():

    request_body_fav_planet = request.get_json()

    new_fav_planet = Fav_Planets(
    planet=request_body_fav_planet["planet"], 
    user=request_body_fav_planet["user"])

    db.session.add(new_fav_planet)
    db.session.commit()

    return jsonify(request_body_fav_planet), 200

# [DELETE] Elimina un Character favorito.

@app.route('/fav_characters/<int:fav_characters_id>', methods=['DELETE'])
def delete_fav_character(fav_Characters_id):
    fav_character = Fav_Characters.query.get(fav_Characters_id)

    if not fav_character:
        return jsonify({'message': 'Fav Character not found'}), 404

    db.session.delete(fav_character)
    db.session.commit()

    return jsonify({'message': f'Fav character with ID {fav_Characters_id} deleted successfully'}), 200

# [DELETE] Elimina un planet favorito.

@app.route('/fav_planets/<int:fav_planets_id>', methods=['DELETE'])
def delete_fav_planet(fav_planets_id):
    fav_planet = Fav_Planets.query.get(fav_planets_id)

    if not fav_planet:
        return jsonify({'message': 'Fav planet not found'}), 404

    db.session.delete(fav_planet)
    db.session.commit()

    return jsonify({'message': f'Fav planet with ID {fav_planets_id} deleted successfully'}), 200













# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
