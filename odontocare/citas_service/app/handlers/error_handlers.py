import logging

from app.utils.response import error_response

logger = logging.getLogger(__name__)


"""
Manejador global de excepciones.

Captura excepciones no controladas producidas
durante el procesamiento de una petición.

Funcionamiento:
- Registra la excepción mediante logging.
- Devuelve una respuesta uniforme.
- Evita la exposición de trazas internas al cliente.

Respuestas:
- 500: Internal server error
"""
def register_error_handlers(app):

    @app.errorhandler(Exception)
    def handle_unexpected_exception(error):

        logger.exception(
            f"Unhandled exception: {error}"
        )

        return error_response(
            message="Internal server error",
            status_code=500
        )