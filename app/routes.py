from flask import Blueprint, jsonify, abort, make_response

# add moon class!

class Moon:
    def __init__(self, id, name):
        self.id = id
        self.name = name

class Planet:
    def __init__(self, id, name, description, moons):
        self.id = id
        self.name = name
        self.description = description
        self.moons = moons

earth_moons =[Moon(1, "Moon")]
mars_moons =[Moon(1, "Moon"), Moon(2, "Moon2")]

planets = [
    Planet(1, "Earth", "Our home planet Earth is a rocky, terrestrial plane", Moon(1, "Moon")),
    Planet(2, "Mars", "A dusty, cold, desert world with a very thin atmosphere", 2),
    Planet(3, "Pluto", "Pluto is very small, only about half the width of the United States", 5)
]

def validate_planet(planet_id):
    try:
        planet_id = int(planet_id)
    except:
        abort(make_response({"message": f"planet {planet_id} is not a valid input type"}, 400))

    for planet in planets:
        if planet.id == planet_id:
            return planet
    
    abort(make_response({"message: " :f"planet id {planet_id} does not exist"}, 404))

planets_bp = Blueprint("planets", __name__, url_prefix="/planets")

@planets_bp.route("", methods=["GET"])
def handle_planets():
    planets_response = []
    for planet in planets:
        planets_response.append({
            "id": planet.id,
            "name": planet.name,
            "description": planet.description,
            "moons": planet.moons
        })
    return jsonify(planets_response)

# wave 02

@planets_bp.route("/<planet_id>", methods = ["GET"])

def handle_planet(planet_id):
    planet = validate_planet(planet_id)

    return {
            "id": planet.id,
            "name": planet.name,
            "description": planet.description,
            "moons": planet.moons
    }