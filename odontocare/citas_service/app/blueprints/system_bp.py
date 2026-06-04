from flask import Blueprint

from sqlalchemy import text

from app.extensions import db

from app.services.health_service import (
    check_database
)

from app.services.admin_client import (
    check_admin_service
)

from app.utils.response import (
    success_response,
    error_response
)

import logging

logger = logging.getLogger(__name__)

system_bp = Blueprint(
    "system_bp",
    __name__
)

@system_bp.route("/version", methods=["GET"])
def version():

    return success_response(
        data={
            "service": "citas_service",
            "version": "1.0.0"
        }
    )

@system_bp.route("/health", methods=["GET"])
def health():

    return success_response(
        data={
            "service": "citas_service",
            "status": "UP"
        }
    )

@system_bp.route("/ready", methods=["GET"])
def ready():

    try:

        db.session.execute(
            text("SELECT 1")
        )

        return success_response(
            data={
                "service": "citas_service",
                "status": "READY"
            }
        )

    except Exception as e:

        return error_response(
            "Servicio no listo",
            503
        )
    
@system_bp.route("/health/deep")
def deep_health():

    database_ok = check_database()

    admin_ok = check_admin_service()

    healthy = (
        database_ok
        and
        admin_ok
    )

    logging.info(
        f"Health check - Database: {'UP' if database_ok else 'DOWN'}, Admin Service: {'UP' if admin_ok else 'DOWN'}"
    )

    if healthy:

        return success_response(
            data={

                "service": "citas_service",

                "healthy": healthy,

                "dependencies": {

                    "database":
                        "UP",

                    "admin_service":
                        "UP"
                }

            }
        )
    else:
        return error_response(
            "Algunos sistemas no operativos",
            503
        )