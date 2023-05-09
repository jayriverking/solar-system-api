from app import db
from app.models.planet import Planet
from app.models.moon import Moon

from flask import Blueprint, jsonify, abort, make_response, request
moons_bp = Blueprint("moons", __name__, url_prefix="/moons")

@moons_bp.route("", methods=["POST"])
def create_moon():


    request_body = request.get_json()
    new_moon = Moon(
        name= request_body["name"],
    )

    db.session.add(new_moon)
    db.session.commit()

    return make_response(jsonify(f"Moon {new_moon.name} successfully created"), 201)

@moons_bp.route("", methods=["GET"])
def read_all_moons():
    
    moons = Moon.query.all()

    moons_response = []
    for moon in moons:
        moons_response.append(
            {
                "name": moon.name,
                "planet": moon.planet
            }
        )
    return jsonify(moons_response)

planets_bp = Blueprint("planets", __name__, url_prefix="/planets")


@planets_bp.route("/<planet_id>/moons", methods = ["POST"])
def create_moon_by_planet_id(planet_id):
    planet = validate_model(Planet, planet_id)
    request_body = request.get_json()
    new_moon = Moon(
        name = request_body["name"],
        planet = planet
    )

    # add to the database
    db.session.add(new_moon)
    db.session.commit()

    return jsonify(f"Moon {new_moon.name} owned by {new_moon.planet.name} was successfully created."), 201


@planets_bp.route("/<planet_id>/moons", methods = ["GET"])
def get_all_moonss_with_planet_id(planet_id):
    planet = validate_model(Planet, planet_id)

    moons_response = []

    for moon in planet.moons:
        moons_response.append(moon.to_dict())
    
    return jsonify(moons_response), 200
# validate helper function
def validate_model(model_class, model_id):
    try:
        # getting id from url so its a string
        model_id = int(model_id)
    except:
        abort(make_response({"message": f"{model_id} is not a valid type ({type(model_id)}. Must be an integer)"}, 400))


    model = model_class.query.get(model_id)

    if not model:
        abort(make_response({"message": f"{model_class.__name__} {model_id} does not exist."}, 404))
    
    return model


@planets_bp.route("", methods=["POST"])
def make_a_planet():
    try:
        request_body = request.get_json()

        new_planet = Planet.from_dict(request_body)

        db.session.add(new_planet)
        db.session.commit()

        return jsonify(f"Yaaaaay planet {new_planet.name} has been made"), 201
    except KeyError as error:
        abort(make_response(f"{error.__str__()} is missing", 400))
    

@planets_bp.route("", methods=["GET"])
def get_all_planets():
    name_query = request.args.get("name")
    desc_query = request.args.get("description")

    query_map = {
        Planet.query.filter_by(name = name_query): name_query,
        Planet.query.filter_by(description = desc_query):desc_query
    }
    

    
    #planets = value
    #if name_query or desc_query:
    #   planets = Planet.query.filter_by(name=name_query, description = desc_query)
    #if  desc_query:
    #   planets = Planet.query.filter_by(description=desc_query)
    #else:
    #   planets = Planet.query.all()
    
    
    query_count = 0
    
    for key, value in query_map.items():
        if value:
            planets = key
            query_count += 1
    
    if query_count == 0:
        planets = Planet.query.all()
    
    planet_response = []

    for planet in planets:
        planet_response.append(planet.to_dict())
    return jsonify(planet_response)


@planets_bp.route("/<planet_id>", methods=["GET"])
def get_one_planet(planet_id):
    planet = validate_model(Planet,planet_id)

    return planet.to_dict()


@planets_bp.route("/<planet_id>", methods=["PUT"])
def update_planet(planet_id):
    planet = validate_model(Planet,planet_id)

    request_body = request.get_json()

    planet.name = request_body["name"]
    planet.description = request_body["description"]

    db.session.commit()
    return planet.to_dict()



@planets_bp.route("/<planet_id>", methods=["DELETE"])
def delete_planet(planet_id):
    planet = validate_model(Planet,planet_id)
    db.session.delete(planet)
    db.session.commit()
    return make_response(f"Planet {planet_id}: {planet.name} successfully deleted")




# class Moon:
#     def __init__(self, id, name):
#         self.id = id
#         self.name = name

# class Planet:
#     def __init__(self, id, name, description, moons):
#         self.id = id
#         self.name = name
#         self.description = description
#         self.moons = moons

# earth_moons =Moon(1, "Moon")
# mars_moons =[Moon(1, "Moon"), Moon(2, "Moon2")]

# planets = [
#     Planet(1, "Earth", "Our home planet Earth is a rocky, terrestrial plane", mars_moons),
#     Planet(2, "Mars", "A dusty, cold, desert world with a very thin atmosphere", mars_moons),
#     Planet(3, "Pluto", "Pluto is very small, only about half the width of the United States", mars_moons)
# ]

# def validate_planet(planet_id):
#     try:
#         planet_id = int(planet_id)
#     except:
#         abort(make_response({"message": f"planet {planet_id} is not a valid input type"}, 400))

#     for planet in planets:
#         if planet.id == planet_id:
#             return planet
    
#     abort(make_response({"message: " :f"planet id {planet_id} does not exist"}, 404))

# def handle_moons(planet_moons):
#     moons_response = []
#     for moon in planet_moons:
#         moons_response.append({
#             "id" : moon.id,
#             "name": moon.name
#         })
    
#     return moons_response
    


# @planets_bp.route("", methods=["GET"])
# def handle_planets():
#     planets_response = []
#     for planet in planets:
#         moons_response = handle_moons(planet.moons)

#         planets_response.append({
#             "id": planet.id,
#             "name": planet.name,
#             "description": planet.description,
#             #"moons": planet.moons
#             "moons" : moons_response
#         })
#     return jsonify(planets_response)

# # wave 02

# @planets_bp.route("/<planet_id>", methods = ["GET"])

# def handle_planet(planet_id):
#     planet = validate_planet(planet_id)
#     moons_response = handle_moons(planet.moons)
#     return {
#             "id": planet.id,
#             "name": planet.name,
#             "description": planet.description,
#             "moons": moons_response
#     }