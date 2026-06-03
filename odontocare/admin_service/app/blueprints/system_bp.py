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

@system_bp.route("/version", methods=["GET"])
def version():

    return success_response(
        data={
            "service": "admin_service",
            "version": "1.0.0"
        })

@system_bp.route("/health", methods=["GET"])
def health():

    return success_response(
        data={
            "service": "admin_service",
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
                "service": "admin_service",
                "status": "READY"
            }
        )

    except Exception as e:

        return error_response(
            "Service not ready",
            status_code=503
        )

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

    except Exception as e:

        return error_response(
            "Database not available",
            status_code=503
        )