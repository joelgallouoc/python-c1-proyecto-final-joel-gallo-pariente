from flask import Flask, app

from flasgger import Swagger

from app.config import Config

from app.extensions import (
    db,
    jwt
)

from app.blueprints.citas_bp import citas_bp
from app.blueprints.system_bp import system_bp

import logging

from app.handlers.error_handlers import register_error_handlers
from app.monitoring.request_logging import register_request_logging

logger = logging.getLogger(__name__)

def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(citas_bp)
    app.register_blueprint(system_bp)
    
    register_request_logging(app)
    register_error_handlers(app)
    
    with app.app_context():
        db.create_all()

    swagger_config = {
        "swagger": "2.0",
        "info": {
            "title": "OdontoCare Citas Service",
            "description": "API de gestión de citas de OdontoCare",
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