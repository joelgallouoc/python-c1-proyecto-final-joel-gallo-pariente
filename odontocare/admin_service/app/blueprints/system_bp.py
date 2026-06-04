from flask import Blueprint

from sqlalchemy import text

from app.extensions import db

from app.utils.response import (
    success_response,
    error_response
)

system_bp = Blueprint(
    "system_bp",
    __name__
)

# Endpoint para obtener la version actual del servicio. En una implementación real se obtendría la versiónd esde un .env o control de versiones en BBDD
@system_bp.route("/version", methods=["GET"])
def version():

    return success_response(
        data={
            "service": "admin_service",
            "version": "1.0.0"
        })

# Endpoint usado para comprobar el estado del servicio
@system_bp.route("/health", methods=["GET"])
def health():

    return success_response(
        data={
            "service": "admin_service",
            "status": "UP"
        }
    )

# Endpoint usado para comprobar que el acceso a la Base de Datos está disponible
@system_bp.route("/ready", methods=["GET"])
def ready():

    try:

        db.session.execute(
            text("SELECT 1")
        )

        return success_response(
            data={
                "service": "admin_service",
                "database": "UP"
            }
        )

    except Exception:

        return error_response(
            "Database not available",
            status_code=503
        )
        
# Endpoint usado para comprobar el estado del servicio y la conexión a la base de datos
@system_bp.route("/health/deep", methods=["GET"])
def deep_health():

    try:

        db.session.execute(
            text("SELECT 1")
        )

        return success_response(
            data={
                "service": "admin_service",
                "database": "UP"
            }
        )

    except Exception:

        return error_response(
            "Database not available",
            status_code=503
        )