from app.extensions import db

from app.models.paciente import Paciente

from app.utils.enums import Roles as roles, Estado as estado

from app.utils.pagination import get_pagination
from app.models.usuario import Usuario

from flask import request

import logging

logger = logging.getLogger(__name__)


"""
Valida la existencia de un paciente

Parámetros:
- nombre: int

Funcionamiento:
- Comprueba la existencia de un paciente.

Retorno:

Success:
(
    True,
    None
)

Error:
(
    False,
    {
        "message": str,
        "status_code": int
    }
)
"""
def validar_nuevo_paciente(nombre):

    paciente_existente = Paciente.query.filter_by(
        nombre=nombre,
        estado=estado.ACTIVO.value
    ).first()

    if paciente_existente:

        logger.warning(f"Paciente con nombre {nombre} ya existe")

        return (
            False,
            {
                "message": "El paciente ya existe",
                "status_code": 409
            }
        )

    paciente_existente = Paciente.query.filter_by(
        nombre=nombre
    ).first()

    if paciente_existente:

        logger.warning(f"Paciente con nombre {nombre} y estado {paciente_existente.estado} ya existe")

        return (
            False,
            {
                "message": "El paciente ya existe. Está inactivo, por favor reactívelo en lugar de crear uno nuevo.",
                "status_code": 409
            }
        )

    return (
        True,
        None
    )


"""
Servicio de creación de pacientes.

Responsabilidades:
- Obtener los datos de la petición.
- Validar paciente.
- Registrar el paciente en base de datos.

Validaciones:
- No debe existir el paciente.

Retorno:

Success:
(
    True,
    {
        "data": paciente.to_dict(),
        "status_code": 201
    }
)

Error:
(
    ok, 
    resultado
)
"""
def crear_paciente():

    data = request.get_json()

    username = data.get("username")
    password = data.get("password")
    nombre = data.get("nombre")

    ok, resultado = validar_nuevo_paciente(nombre)

    if not ok:
        return (
            False,
            resultado
        )

    usuario = Usuario(
        username=username,
        rol=roles.PACIENTE.value
    )

    usuario.set_password(password)

    db.session.add(usuario)
    db.session.flush()

    paciente = Paciente(
        id_usuario=usuario.id_usuario,
        nombre=nombre,
        telefono=data["telefono"],
        estado=estado.ACTIVO.value
    )

    db.session.add(paciente)
    db.session.commit()

    logger.info(f"Paciente creado: {paciente.nombre}")

    return (
        True,
        {
            "data": paciente.to_dict(),
            "status_code": 201
        }
    )


"""
Servicio de listado de pacientes.

Responsabilidades:
- Obtener los pacientes que se indican.

Retorno:
(
    True, 
    {
        "data": [
            u.to_dict()
            for u in pagination.items
        ],
        "pagination": {
            "page": pagination.page,
            "size": pagination.per_page,
            "total_items": pagination.total,
            "total_pages": pagination.pages
        }
    }
)
"""
def listar_pacientes():
    
    page, size = get_pagination()

    pagination = Paciente.query.paginate(page=page, per_page=size, error_out=False)
    
    logger.info(f"Listado de pacientes obtenido: página {page}, tamaño {size}")

    return {
        "data": [
            u.to_dict()
            for u in pagination.items
        ],
        "pagination": {
            "page": pagination.page,
            "size": pagination.per_page,
            "total_items": pagination.total,
            "total_pages": pagination.pages
        }
    }


"""
Servicio de consulta de pacientes.

Parámetros:
- id_paciente: int

Responsabilidades:
- Obtener el paciente que se indica.

Retorno:

Success:
(
    True,
    {
        "data": paciente.to_dict(),
        "status_code": 200
    }
    
)

Error:
(
    False,
    {
        "message": str,
        "status_code": int
    }
)
"""
def obtener_paciente(id_paciente):
    paciente = Paciente.query.get(id_paciente)

    if not paciente:

        logger.warning(f"Intento de obtención de paciente no encontrado: {id_paciente}")

        return (
            False,
            {
                "message": "Paciente no encontrado",
                "status_code": 404
            }
        )

    logger.info(f"Paciente obtenido con nombre {paciente.nombre} e ID {paciente.id_paciente}")

    return (
        True,
        {
            "data": paciente.to_dict(),
            "status_code": 200
        }
    )