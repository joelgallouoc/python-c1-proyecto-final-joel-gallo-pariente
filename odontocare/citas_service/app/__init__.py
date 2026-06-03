from flask import Flask

from app.config import Config

from app.extensions import (
    db,
    jwt
)

from app.models import *

from app.blueprints.citas_bp import citas_bp
from app.blueprints.system_bp import system_bp


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(citas_bp)
    app.register_blueprint(system_bp)
    
    with app.app_context():
        db.create_all()

    return app