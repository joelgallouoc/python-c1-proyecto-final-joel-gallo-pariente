from flask import Blueprint

from flask_jwt_extended import jwt_required

from app.utils.enums import Roles

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
from app.decorators.schema_validation import validate_body, validate_query
from app.decorators.request_data_validation import validate_request_data
from app.schemas.usuarios import CreateUserSchema, UserListFiltersSchema
from app.schemas.base import PaginationSchema
from app.schemas.pacientes import CreatePatientSchema, PatientFiltersSchema
from app.schemas.doctores import CreateDoctorSchema, DoctorFiltersSchema
from app.schemas.centros import CenterFiltersSchema, CreateCenterSchema

admin_bp = Blueprint(
    "admin_bp",
    __name__,
    url_prefix="/admin"
)


"""
Creación de usuarios
---
tags:
  - Usuarios

security:
  - Bearer: []

description: |
  Crea un usuario nuevo.

  Roles permitidos:
  - ADMIN

  Roles permitidos del usuario a crear:
  - ADMIN
  - SECRETARIA

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
          example: secretaria1

        password:
          type: string
          example: secretaria123

        role:
          type: string
          example: SECRETARIA

responses:
  201:
    description: Usuario creado correctamente

  400:
    description: Rol inválido

  403:
    description: Acceso denegado

  409:
    description: Usuario ya existe

  422:
    description: Error de validación
"""
@admin_bp.route("/usuarios", methods=["POST"])
@jwt_required()
@role_required("ADMIN")
@user_role_required("ADMIN", "SECRETARIA")
@validate_request_data(body_required=True)
@validate_body(CreateUserSchema)
def creacion_usuario(): 

    ok, resultado = crear_usuario()

    if not ok:
        return error_response(
                    resultado.get("message"),
                    resultado.get("status_code")
                )

    return success_response(data=resultado.get("data"), status_code=201)


"""
Listado de usuarios
---
tags:
  - Usuarios

security:
  - Bearer: []

description: |
  Devuelve un listado paginado de usuarios.

  Roles permitidos:
  - ADMIN

parameters:
  - in: query
    name: page
    required: false
    type: integer
    example: 1

  - in: query
    name: per_page
    required: false
    type: integer
    example: 10

responses:
  200:
    description: Listado de usuarios

  403:
    description: Acceso denegado

  422:
    description: Parámetros de consulta inválidos
"""
@admin_bp.route("/usuarios", methods=["GET"])
@jwt_required()
@role_required("ADMIN")
@validate_request_data(allow_query=True)
@validate_query(UserListFiltersSchema)
def listado_de_usuarios():

    user_list = listar_usuarios()

    return success_response(
        data=user_list.get("data"),
        pagination=user_list.get("pagination")
    )

"""
Obtención de usuario
---
tags:
  - Usuarios

security:
  - Bearer: []

description: |
  Obtiene un usuario por su identificador.

  Roles permitidos:
  - ADMIN

parameters:
  - in: path
    name: id_usuario
    required: true
    type: integer
    example: 1

responses:
  200:
    description: Usuario encontrado

  403:
    description: Acceso denegado

  404:
    description: Usuario no encontrado

  422:
    description: El endpoint no admite body ni query params
"""
@admin_bp.route("/usuarios/<int:id_usuario>", methods=["GET"])
@jwt_required()
@role_required("ADMIN")
@validate_request_data()
def obtencion_usuario(id_usuario):

    ok, resultado = obtener_usuario(id_usuario)

    if not ok:
        return error_response(
            resultado.get("message"),
            resultado.get("status_code")
        )

    return success_response(data=resultado.get("data"), status_code=resultado.get("status_code"))


"""
Creación de pacientes
---
tags:
  - Pacientes

security:
  - Bearer: []

description: |
  Crea un paciente nuevo.

  Roles permitidos:
  - ADMIN

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
          example: juan.perez

        password:
          type: string
          example: paciente123

        nombre:
          type: string
          example: Juan Pérez

        telefono:
          type: string
          example: 612345678

responses:
  201:
    description: Paciente creado correctamente

  403:
    description: Acceso denegado

  409:
    description: Paciente ya existe

  422:
    description: Error de validación
"""
@admin_bp.route("/pacientes", methods=["POST"])
@jwt_required()
@role_required("ADMIN")
@validate_request_data(body_required=True)
@validate_body(CreatePatientSchema)
def creacion_paciente():

    ok, resultado = crear_paciente()

    if not ok:
        return error_response(
            resultado.get("message"),
            resultado.get("status_code")
        )

    return success_response(data=resultado.get("data"), status_code=resultado.get("status_code"))


"""
Listado de pacientes
---
tags:
  - Pacientes

security:
  - Bearer: []

description: |
  Devuelve un listado paginado de pacientes.

  Roles permitidos:
  - ADMIN

parameters:
  - in: query
    name: page
    required: false
    type: integer
    example: 1

  - in: query
    name: per_page
    required: false
    type: integer
    example: 10

responses:
  200:
    description: Listado de pacientes

  403:
    description: Acceso denegado

  422:
    description: Parámetros de consulta inválidos
"""
@admin_bp.route("/pacientes", methods=["GET"])
@jwt_required()
@role_required("ADMIN")
@validate_request_data(allow_query=True)
@validate_query(PatientFiltersSchema)
def listado_pacientes():

    listado_pacientes = listar_pacientes()

    return success_response(
        data=listado_pacientes.get("data"),
        pagination=listado_pacientes.get("pagination")
    )


"""
Obtención de paciente
---
tags:
  - Pacientes

security:
  - Bearer: []

description: |
  Obtiene un paciente por su identificador.

  Roles permitidos:
  - ADMIN

parameters:
  - in: path
    name: id_paciente
    required: true
    type: integer
    example: 1

responses:
  200:
    description: Paciente encontrado

  403:
    description: Acceso denegado

  404:
    description: Paciente no encontrado

  422:
    description: El endpoint no admite body ni query params
"""
@admin_bp.route("/pacientes/<int:id_paciente>", methods=["GET"])
@jwt_required()
@role_required("ADMIN")
@validate_request_data()
def obtencion_paciente(id_paciente):

    ok, resultado = obtener_paciente(id_paciente)

    if not ok:
        return error_response(
            resultado.get("message"),
            resultado.get("status_code")
        )

    return success_response(data=resultado.get("data"), status_code=resultado.get("status_code"))


"""
Creación de doctores
---
tags:
  - Doctores

security:
  - Bearer: []

description: |
  Crea un doctor nuevo.

  Roles permitidos:
  - ADMIN

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
          example: doctor.garcia

        password:
          type: string
          example: doctor123

        nombre:
          type: string
          example: María García

        especialidad:
          type: string
          example: Ortodoncia

responses:
  201:
    description: Doctor creado correctamente

  403:
    description: Acceso denegado

  409:
    description: Doctor ya existe

  422:
    description: Error de validación
"""
@admin_bp.route("/doctores", methods=["POST"])
@jwt_required()
@role_required("ADMIN")
@validate_request_data(body_required=True)
@validate_body(CreateDoctorSchema)
def creacion_doctor():

    ok, resultado = crear_doctor()

    if not ok:
        return error_response(
            resultado.get("message"),
            resultado.get("status_code")
        )

    return success_response(data=resultado.get("data"), status_code=resultado.get("status_code"))


"""
Obtención de doctor
---
tags:
  - Doctores

security:
  - Bearer: []

description: |
  Obtiene un doctor por su identificador.

  Roles permitidos:
  - ADMIN

parameters:
  - in: path
    name: id_doctor
    required: true
    type: integer
    example: 1

responses:
  200:
    description: Doctor encontrado

  403:
    description: Acceso denegado

  404:
    description: Doctor no encontrado

  422:
    description: El endpoint no admite body ni query params
"""
@admin_bp.route("/doctores/<int:id_doctor>", methods=["GET"])
@jwt_required()
@role_required("ADMIN")
@validate_request_data()
def obtencion_doctor(id_doctor):

    ok, resultado = obtener_doctor(id_doctor)

    if not ok:
        return error_response(
            resultado.get("message"),
            resultado.get("status_code")
        )

    return success_response(data=resultado.get("data"), status_code=resultado.get("status_code"))


"""
Listado de doctores
---
tags:
  - Doctores

security:
  - Bearer: []

description: |
  Devuelve un listado paginado de doctores.

  Roles permitidos:
  - ADMIN

parameters:
  - in: query
    name: page
    required: false
    type: integer
    example: 1

  - in: query
    name: per_page
    required: false
    type: integer
    example: 10

responses:
  200:
    description: Listado de doctores

  403:
    description: Acceso denegado

  422:
    description: Parámetros de consulta inválidos
"""
@admin_bp.route("/doctores", methods=["GET"])
@jwt_required()
@role_required("ADMIN")
@validate_request_data(allow_query=True)
@validate_query(DoctorFiltersSchema)
def listado_doctores():

    doctor_list = listar_doctores()

    return success_response(
        data=doctor_list.get("data"),
        pagination=doctor_list.get("pagination")
        )



"""
Creación de centros
---
tags:
  - Centros

security:
  - Bearer: []

description: |
  Crea un centro nuevo.

  Roles permitidos:
  - ADMIN

consumes:
  - application/json

parameters:
  - in: body
    name: body
    required: true

    schema:
      properties:

        nombre:
          type: string
          example: Clínica Dental Centro

        direccion:
          type: string
          example: Calle Mayor 25, Madrid

responses:
  201:
    description: Centro creado correctamente

  403:
    description: Acceso denegado

  409:
    description: Centro ya existe

  422:
    description: Error de validación
"""
@admin_bp.route("/centros", methods=["POST"])
@jwt_required()
@role_required("ADMIN")
@validate_request_data(body_required=True)
@validate_body(CreateCenterSchema)
def creacion_centro():

    ok, resultado = crear_centro()

    if not ok:
        return error_response(
            resultado.get("message"),
            resultado.get("status_code")
        )

    return success_response(data=resultado.get("data"), status_code=resultado.get("status_code"))


"""
Listado de centros
---
tags:
  - Centros

security:
  - Bearer: []

description: |
  Devuelve un listado paginado de centros.

  Roles permitidos:
  - ADMIN

parameters:
  - in: query
    name: page
    required: false
    type: integer
    example: 1

  - in: query
    name: per_page
    required: false
    type: integer
    example: 10

responses:
  200:
    description: Listado de centros

  403:
    description: Acceso denegado

  422:
    description: Parámetros de consulta inválidos
"""
@admin_bp.route("/centros", methods=["GET"])
@jwt_required()
@role_required("ADMIN")
@validate_request_data(allow_query=True)
@validate_query(CenterFiltersSchema)
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
    

"""
Obtención de centro
---
tags:
  - Centros

security:
  - Bearer: []

description: |
  Obtiene un centro por su identificador.

  Roles permitidos:
  - ADMIN

parameters:
  - in: path
    name: id_centro
    required: true
    type: integer
    example: 1

responses:
  200:
    description: Centro encontrado

  403:
    description: Acceso denegado

  404:
    description: Centro no encontrado

  422:
    description: El endpoint no admite body ni query params
"""
@admin_bp.route("/centros/<int:id_centro>", methods=["GET"])
@jwt_required()
@role_required("ADMIN")
@validate_request_data()
def obtencion_centro(id_centro):

    ok, resultado = obtener_centro(id_centro)

    if not ok:
        return error_response(
            resultado.get("message"),
            resultado.get("status_code")
        )

    return success_response(data=resultado.get("data"), status_code=resultado.get("status_code"))

