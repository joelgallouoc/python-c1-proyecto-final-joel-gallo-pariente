from flask import request

from app.extensions import db

from app.models.usuario import Usuario

from app.utils.pagination import get_pagination

import logging

logger = logging.getLogger(__name__)


"""
Valida la existencia de un usuario

Parámetros:
- username: int

Funcionamiento:
- Comprueba la existencia de un usuario.

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
def validar_nuevo_usuario(username):

    usuario_existente = Usuario.query.filter_by(
        username=username
    ).first()

    if usuario_existente:

        logger.warning(f"Usuario ya existe: {username}")

        return (
            False,
            {
                "message": "El usuario ya existe",
                "status_code": 409
            }
        )

    return (
        True,
        None
    )


"""
Servicio de creación de usuarios.

Responsabilidades:
- Obtener los datos de la petición.
- Validar usuario.
- Registrar el usuario en base de datos.

Validaciones:
- No debe existir el usuario.

Retorno:

Success:
(
    True,
    {
        "data": usuario.to_dict(),
        "status_code": 201
    }
)

Error:
(
    ok, 
    resultado
)
"""
def crear_usuario():

    data = request.get_json()

    username = data.get("username")
    password = data.get("password")
    rol = data.get("rol")

    ok, resultado = validar_nuevo_usuario(username)

    if not ok:
        return (
            False,
            resultado
        )

    usuario = Usuario(
        username=username,
        rol=rol
    )

    usuario.set_password(password)

    db.session.add(usuario)
    db.session.commit()

    logger.info(f"Usuario creado: {usuario.username} con rol {usuario.rol}")

    return (
        True,
        {
            "data": usuario.to_dict(),
            "status_code": 201
        }
    )


"""
Servicio de listado de usuarios.

Responsabilidades:
- Obtener los usuarios que se indican.

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
def listar_usuarios():
    
    page, size = get_pagination()

    pagination = Usuario.query.paginate(page=page, per_page=size, error_out=False)

    logger.info(f"Listado de usuarios obtenido: página {pagination.page} de {pagination.pages}, total de usuarios {pagination.total}")

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
Servicio de consulta de usuarios.

Parámetros:
- id_usuario: int

Responsabilidades:
- Obtener el usuario que se indica.

Retorno:

Success:
(
    True,
    {
        "data": usuario.to_dict(),
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
def obtener_usuario(id_usuario):
    usuario = Usuario.query.get(id_usuario)

    if not usuario:

        logger.warning(f"Intento de obtención de usuario no encontrado: {id_usuario}")

        return (
            False,
            {
                "message": "Usuario no encontrado",
                "status_code": 404
            }
        )

    logger.info(f"Usuario obtenido con nombre {usuario.username} e ID {usuario.id_usuario}")

    return (
        True,
        {
            "data": usuario.to_dict(),
            "status_code": 200
        }
    )