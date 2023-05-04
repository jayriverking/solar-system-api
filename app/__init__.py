from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from dotenv import load_dotenv

import os

db = SQLAlchemy()
migrate = Migrate()

load_dotenv()

def create_app(test_config=None):
    app = Flask(__name__)

    #app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:postgres@localhost:5432/solar_system_development'

    if not test_config:
        # development environment configuration
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI")
    else:
        # test environment configuration
        # if there is a test_config passed in, this means
        # we're tyring to test the app,
        # configure the test settings
        app.config["TESTING"] = True
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_TEST_DATABASE_URI")


    db.init_app(app)
    migrate.init_app(app, db)

    from .routes import planets_bp
    app.register_blueprint(planets_bp)

    from .routes import moons_bp
    app.register_blueprint(moons_bp)

    from app.models.planet import Planet
    from app.models.moon import Moon


    return app
