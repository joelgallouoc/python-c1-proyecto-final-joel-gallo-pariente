from flask import request

from flask_jwt_extended import (
    verify_jwt_in_request,
    get_jwt
)

import logging

logger = logging.getLogger(__name__)

def register_request_logging(app):

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