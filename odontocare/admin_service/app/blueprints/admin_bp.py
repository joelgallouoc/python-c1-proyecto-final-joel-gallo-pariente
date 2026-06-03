from flask import Blueprint

from flask_jwt_extended import jwt_required

from app.decorators.role_required import (
    role_required,
    user_role_required
)

from app.utils.response import (
    success_response,
    error_response
)

from app.services.usuarios_service import crear_usuario, listar_usuarios, obtener_usuario
from app.services.doctores_service import crear_doctor, listar_doctores, obtener_doctor
from app.services.pacientes_service import crear_paciente, listar_pacientes, obtener_paciente
from app.services.centros_service import crear_centro, listar_centros, obtener_centro

admin_bp = Blueprint(
    "admin_bp",
    __name__,
    url_prefix="/admin"
)



@admin_bp.route("/usuarios", methods=["POST"])
@jwt_required()
@role_required("ADMIN")
@user_role_required("ADMIN", "SECRETARIA")
def creacion_usuario():

    ok, resultado = crear_usuario()

    if not ok:
        return error_response(
                    resultado.get("message"),
                    resultado.get("status_code")
                )

    return success_response(data=resultado.get("data"), status_code=201)


@admin_bp.route("/usuarios", methods=["GET"])
@jwt_required()
@role_required("ADMIN")
def listado_de_usuarios():

    user_list = listar_usuarios()

    return success_response(
        data=user_list.get("data"),
        pagination=user_list.get("pagination")
    )


@admin_bp.route("/usuarios/<int:id_usuario>", methods=["GET"])
@jwt_required()
@role_required("ADMIN")
def obtencion_usuario(id_usuario):

    ok, resultado = obtener_usuario(id_usuario)

    if not ok:
        return error_response(
            resultado.get("message"),
            resultado.get("status_code")
        )

    return success_response(data=resultado.get("data"), status_code=resultado.get("status_code"))




@admin_bp.route("/pacientes", methods=["POST"])
@jwt_required()
@role_required("ADMIN")
def creacion_paciente():

    ok, resultado = crear_paciente()

    if not ok:
        return error_response(
            resultado.get("message"),
            resultado.get("status_code")
        )

    return success_response(data=resultado.get("data"), status_code=resultado.get("status_code"))


@admin_bp.route("/pacientes/<int:id_paciente>", methods=["GET"])
@jwt_required()
@role_required("ADMIN")
def obtencion_paciente(id_paciente):

    ok, resultado = obtener_paciente(id_paciente)

    if not ok:
        return error_response(
            resultado.get("message"),
            resultado.get("status_code")
        )
    
    return success_response(data=resultado.get("data"), status_code=resultado.get("status_code"))


@admin_bp.route("/pacientes", methods=["GET"])
@jwt_required()
@role_required("ADMIN")
def listado_pacientes():

    listado_pacientes = listar_pacientes()

    return success_response(
        data=listado_pacientes.get("data"), 
        pagination=listado_pacientes.get("pagination")
    )



@admin_bp.route("/doctores", methods=["POST"])
@jwt_required()
@role_required("ADMIN")
def creacion_doctor():

    ok, resultado = crear_doctor()

    if not ok:
        return error_response(
            resultado.get("message"),
            resultado.get("status_code")
        )
    
    return success_response(data=resultado.get("data"), status_code=resultado.get("status_code"))


@admin_bp.route("/doctores/<int:id_doctor>", methods=["GET"])
@jwt_required()
@role_required("ADMIN")
def obtencion_doctor(id_doctor):

    ok, resultado = obtener_doctor(id_doctor)

    if not ok:
        return error_response(
            resultado.get("message"),
            resultado.get("status_code")
        )

    return success_response(data=resultado.get("data"), status_code=resultado.get("status_code"))


@admin_bp.route("/doctores", methods=["GET"])
@jwt_required()
@role_required("ADMIN")
def listado_doctores():

    doctor_list = listar_doctores()

    return success_response(
        data=doctor_list.get("data"),
        pagination=doctor_list.get("pagination") 
        )




@admin_bp.route("/centros", methods=["POST"])
@jwt_required()
@role_required("ADMIN")
def creacion_centro():

    ok, resultado = crear_centro()

    if not ok:
        return error_response(
            resultado.get("message"),
            resultado.get("status_code")
        )
    
    return success_response(data=resultado.get("data"), status_code=resultado.get("status_code"))


@admin_bp.route("/centros/<int:id_centro>", methods=["GET"])
@jwt_required()
@role_required("ADMIN")
def obtencion_centro(id_centro):

    ok, resultado = obtener_centro(id_centro)

    if not ok:
        return error_response(
            resultado.get("message"),
            resultado.get("status_code")
        )

    return success_response(data=resultado.get("data"), status_code=resultado.get("status_code"))


@admin_bp.route("/centros", methods=["GET"])
@jwt_required()
@role_required("ADMIN")
def listado_centros():

    ok, resultado = listar_centros()

    if not ok:
        return error_response(
            resultado.get("message"),
            resultado.get("status_code")
        )

    return success_response(
        data=resultado.get("data"),
        pagination=resultado.get("pagination")
    )
