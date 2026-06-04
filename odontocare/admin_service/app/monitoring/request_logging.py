from flask import request

from flask_jwt_extended import (
    verify_jwt_in_request,
    get_jwt
)

import logging

logger = logging.getLogger(__name__)


"""
Middleware de monitorización de peticiones y respuestas
"""
def register_request_logging(app):

    """
    Middleware de monitorización de peticiones.

    Registra información de entrada para cada petición.

    Información registrada:
    - Usuario autenticado.
    - Método HTTP.
    - Endpoint.
    - Query params.
    - Payload recibido.

    Objetivo:
    - Trazabilidad.
    - Auditoría.
    - Diagnóstico de errores.
    """

    @app.before_request
    def before_request_logging():

        username = "anonymous"

        try:

            verify_jwt_in_request(optional=True)

            claims = get_jwt()

            username = claims.get(
                "username",
                "anonymous"
            )

        except Exception:
            pass

        logger.info(
            "REQUEST | user=%s | method=%s | path=%s | query=%s | payload=%s",
            username,
            request.method,
            request.path,
            dict(request.args),
            request.get_json(silent=True)
        )
     
    
    """
    Middleware de monitorización de respuestas.

    Registra información de salida para cada petición.

    Información registrada:
    - Dirección IP.
    - Método HTTP.
    - Endpoint.
    - Código de respuesta.

    Objetivo:
    - Seguimiento de actividad.
    - Diagnóstico de incidencias.
    - Monitorización del servicio.
    """    
    @app.after_request
    def after_request_logging(response):

        logger.info(
            "RESPONSE | ip=%s | method=%s | path=%s | status=%s",
            request.remote_addr,
            request.method,
            request.path,
            response.status_code
        )

        return response