from flask import Blueprint

from flask_jwt_extended import jwt_required

from app.utils.response import (
    success_response,
    error_response
)
from app.services.auth_service import log_in, obtain_me

import logging

from app.decorators.schema_validation import validate_body
from app.schemas.auth import LoginSchema
from app.decorators.request_data_validation import validate_request_data

logger = logging.getLogger(__name__)


auth_bp = Blueprint(
    "auth_bp",
    __name__,
    url_prefix="/auth"
)


@auth_bp.route("/login", methods=["POST"])
@validate_request_data(body_required=True)
@validate_body(LoginSchema)
def login():

  """
  Login de usuario
  ---
  tags:
  - Auth

  consumes:
    - application/json

  parameters:
    - in: body
      name: body
      required: true
      schema:
        properties:
          username:
            type: string
            example: admin
          password:
            type: string
            example: admin123

  responses:
    200:
      description: Login correcto

    401:
      description: Credenciales inválidas

    404:
      description: Usuario no encontrado
  """ 

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
@validate_request_data()
def me():

  """
  Información del usuario autenticado
  ---
  tags:
    - Auth

  security:
    - Bearer: []

  responses:
    200:
      description: Usuario autenticado

    404:
      description: Usuario no encontrado
  """

  ok, resultado = obtain_me()

  if not ok:
      return error_response(
          resultado["message"],
          resultado["status_code"]
      )

  return success_response(
      data=resultado["data"]
  )