from flask import Flask

from app.config import Config

from app.extensions import (
    db,
    jwt
)

from app.models import *

from app.models.usuario import Usuario

from app.blueprints.auth_bp import auth_bp
from app.blueprints.admin_bp import admin_bp
from app.blueprints.system_bp import system_bp


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(system_bp)

    with app.app_context():

        db.create_all()

        if Usuario.query.count() == 0:

            admin = Usuario(
                username="admin",
                rol="ADMIN"
            )

            admin.set_password(
                "admin123"
            )

            db.session.add(admin)
            db.session.commit()

            print(
                "Usuario admin creado"
            )

    return app