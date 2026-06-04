import logging

from app.utils.response import error_response

logger = logging.getLogger(__name__)


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