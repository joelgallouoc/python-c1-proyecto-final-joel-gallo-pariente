from flask import (
    Blueprint,
    request
)

from flask_jwt_extended import (
    jwt_required,
    get_jwt
)

from app.utils.response import (
    success_response,
    error_response
)

from app.services.citas_service import cancelacion_cita, crear_cita, obtener_listado_citas

import logging

from app.decorators.role_required import role_required

logger = logging.getLogger(__name__)



citas_bp = Blueprint(
    "citas_bp",
    __name__,
    url_prefix="/citas"
)


@citas_bp.route("", methods=["POST"])
@jwt_required()
@role_required("ADMIN", "CLIENTE")
def agendar_cita():

    data = request.get_json()

    token = request.headers.get(
        "Authorization"
    ).replace(
        "Bearer ",
        ""
    )

    ok, resultado = crear_cita(
        data,
        token
    )

    if not ok:
        return error_response(
                    resultado.get("message"),
                    resultado.get("status_code")
                )
    
    return success_response(data=resultado.get("data"), status_code=201)


@citas_bp.route("/<int:id_cita>", methods=["PUT"])
@jwt_required()
@role_required("ADMIN", "SECRETARIA")
def cancelar_cita(id_cita):

    claims = get_jwt()

    ok, resultado = cancelacion_cita(
        id_cita,
        claims["role"]
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
def listar_citas():

    claims = get_jwt()

    role = claims["role"]

    ok, resultado = obtener_listado_citas(
        role
    )

    if not ok:
        return error_response(
            message=resultado.get("message"),
            status_code=resultado.get("status_code")
        )

    return success_response(
        data=resultado.get("data"),
        pagination=resultado.get("pagination")
    )