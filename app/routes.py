from app import db
from app.models.planet import Planet
from flask import Blueprint, jsonify, abort, make_response, request

planets_bp = Blueprint("planets", __name__, url_prefix="/planets")

# validate helper function
def validate_planet(planet_id):
    try:
        planet_id = int(planet_id)
    except:
        abort(make_response({"message": f"{planet_id} is not a valid type! {type(planet_id)} must be an integer"}, 400))
    
    planet = Planet.query.get(planet_id)
    if not planet:
        abort(make_response({"message": f"Planet {planet_id} does not exist."}, 404))

    return planet


@planets_bp.route("", methods=["POST"])
def make_a_planet():
    try:
        request_body = request.get_json()

        new_planet = Planet(
            name = request_body["name"],
            description =  request_body["description"]
        )

        db.session.add(new_planet)
        db.session.commit()

        return make_response(f"Yaaaaay planet {new_planet.name} has been made", 201)
    except KeyError as error:
        abort(make_response(f"{error.__str__()} is missing", 400))


@planets_bp.route("", methods=["GET"])
def get_all_planets():
    name_query = request.args.get("name")
    desc_query = request.args.get("description")

    if name_query:
        planets = Planet.query.filter_by(name=name_query) 
    if  desc_query:
        planets = Planet.query.filter_by(description=desc_query)
    
    planet_response = []
    planets = Planet.query.all()
    for planet in planets:
        planet_response.append({
            "id": planet.id,
            "name": planet.name,
            "description": planet.description
        })
    return jsonify(planet_response)


@planets_bp.route("/<planet_id>", methods=["GET"])
def get_one_planet(planet_id):
    planet = validate_planet(planet_id)

    return {
        "id": planet.id,
        "name": planet.name,
        "description": planet.description
    }


@planets_bp.route("/<planet_id>", methods=["PUT"])
def update_planet(planet_id):
    planet = validate_planet(planet_id)

    request_body = request.get_json()

    planet.name = request_body["name"]
    planet.description = request_body["description"]

    db.session.commit()
    return {
        "id": planet.id,
        "name": planet.name,
        "description": planet.description
    }



@planets_bp.route("/<planet_id>", methods=["DELETE"])
def delete_planet(planet_id):
    planet = validate_planet(planet_id)
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