from flask import Flask

from flasgger import Swagger

from app.config import Config

from app.extensions import (
    db,
    jwt
)

from app.models.usuario import Usuario

from app.blueprints.auth_bp import auth_bp
from app.blueprints.admin_bp import admin_bp
from app.blueprints.system_bp import system_bp
from app.handlers.error_handlers import register_error_handlers
from app.monitoring.request_logging import register_request_logging

import logging

logger = logging.getLogger(__name__)

def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(system_bp)

    register_request_logging(app)
    register_error_handlers(app)

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

            logger.info(
                "Usuario admin básico creado with username admin and password admin123"
            )

    swagger_config = {
        "swagger": "2.0",
        "info": {
            "title": "OdontoCare Admin Service",
            "description": "API de administración de OdontoCare",
            "version": "1.0.0"
        },
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "JWT Authorization header. Ejemplo: Bearer eyJ..."
            }
        }
    }

    Swagger(
        app,
        template=swagger_config
    )

    return app

