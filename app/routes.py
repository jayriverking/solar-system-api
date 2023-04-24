from flask import Blueprint, jsonify

# add moon class!

class Planet:
    def __init__(self, id, name, description, moons):
        self.id = id
        self.name = name
        self.description = description
        self.moons = moons

planets = [
    Planet(1, "Earth", "Our home planet Earth is a rocky, terrestrial plane", 1),
    Planet(2, "Mars", "A dusty, cold, desert world with a very thin atmosphere", 2),
    Planet(3, "Pluto", "Pluto is very small, only about half the width of the United States", 5)
]
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