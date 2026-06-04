from flask import Blueprint

from flask_jwt_extended import jwt_required

from app.utils.response import (
    success_response,
    error_response
)

from app.services.citas_service import cancelacion_cita, crear_cita, obtener_listado_citas

import logging

from app.decorators.role_required import role_required
from app.decorators.request_data_validation import validate_request_data
from app.decorators.schema_validation import validate_body, validate_query
from app.schemas.citas import CreateAppointmentSchema, AppointmentFiltersSchema

logger = logging.getLogger(__name__)



citas_bp = Blueprint(
    "citas_bp",
    __name__,
    url_prefix="/citas"
)


@citas_bp.route("", methods=["POST"])
@jwt_required()
@role_required("ADMIN", "CLIENTE")
@validate_request_data(body_required=True)
@validate_body(CreateAppointmentSchema)
def agendar_cita():

  """
  Crear cita médica
  ---
  tags:
    - Citas

  consumes:
    - application/json

  security:
    - Bearer: []

  description: |
    Crea una nueva cita médica.

    Roles permitidos:
    - ADMIN
    - PACIENTE

  parameters:
    - in: body
      name: body
      required: true
      schema:
        properties:
          fecha:
            type: string
            example: 2026-07-01 09:00

          motivo:
            type: string
            example: Revisión anual

          id_paciente:
            type: integer
            example: 1

          id_doctor:
            type: integer
            example: 3

          id_centro:
            type: integer
            example: 1

  responses:
    201:
      description: Cita creada correctamente

    400:
      description: Datos inválidos

    404:
      description: Paciente, doctor o centro no encontrado

    409:
      description: Conflicto de agenda
  """ 

  ok, resultado = crear_cita()

  if not ok:
      return error_response(
                  resultado.get("message"),
                  resultado.get("status_code")
              )
  
  return success_response(data=resultado.get("data"), status_code=201)


@citas_bp.route("/<int:id_cita>", methods=["PUT"])
@jwt_required()
@role_required("ADMIN", "SECRETARIA")
@validate_request_data()
def cancelar_cita(id_cita):

  """
  Cancelar cita médica
  ---
  tags:
    - Citas

  security:
    - Bearer: []

  description: |
    Cancela una cita existente.

    Roles permitidos:
    - ADMIN
    - SECRETARIA

  parameters:
    - in: path
      name: id_cita
      required: true
      type: integer

  responses:
    200:
      description: Cita cancelada correctamente

    404:
      description: Cita no encontrada

    409:
      description: La cita ya estaba cancelada
  """

  ok, resultado = cancelacion_cita(
      id_cita
  )

  if not ok:
      return error_response(
          message=resultado.get("message"),
          status_code=resultado.get("status_code")
      )

  return success_response(
      message=resultado.get("message")
  )


@citas_bp.route("", methods=["GET"])
@jwt_required()
@role_required("ADMIN", "SECRETARIA", "MEDICO")
@validate_request_data(query_required=True)
@validate_query(AppointmentFiltersSchema)
def listar_citas():

  """
  Listar citas
  ---
  tags:
    - Citas

  security:
    - Bearer: []

  description: |
    Devuelve las citas según el rol del usuario.

    ADMIN:
    - Puede filtrar por doctor, paciente, centro, fecha o estado.
 
    SECRETARIA:
    - Puede filtrar por fecha.

    MEDICO:
    - Solo puede consultar sus propias citas.

    En caso de añadir filtros no disponibles para tu rol, se omitirán.

  parameters:
    - in: query
      name: fecha
      type: string

    - in: query
      name: id_doctor
      type: integer

    - in: query
      name: id_paciente
      type: integer

    - in: query
      name: id_centro
      type: integer

    - in: query
      name: estado
      type: string

    - in: query
      name: page
      type: integer

    - in: query
      name: per_page
      type: integer

  responses:
    200:
      description: Listado de citas
  """

  ok, resultado = obtener_listado_citas()

  if not ok:
      return error_response(
          message=resultado.get("message"),
          status_code=resultado.get("status_code")
      )

  return success_response(
      data=resultado.get("data"),
      pagination=resultado.get("pagination")
  )