from flask import Blueprint

from flask_jwt_extended import jwt_required

from app.utils.response import (
    success_response,
    error_response
)
from app.services.auth_service import log_in, obtain_me

import logging

logger = logging.getLogger(__name__)


auth_bp = Blueprint(
    "auth_bp",
    __name__,
    url_prefix="/auth"
)



@auth_bp.route("/login", methods=["POST"])
def login():

    ok, resultado = log_in()

    if not ok:
        return error_response(
            resultado["message"],
            resultado["status_code"]
        )

    return success_response(data={
        "access_token": resultado["data"]["access_token"]
    })


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():

    ok, resultado = obtain_me()

    if not ok:
        return error_response(
            resultado["message"],
            resultado["status_code"]
        )
    
    return success_response(
        data=resultado["data"]
    )