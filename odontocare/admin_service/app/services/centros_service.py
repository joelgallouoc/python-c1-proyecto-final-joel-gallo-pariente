from flask import request

from app.extensions import db

from app.models.centro import Centro

from app.utils.enums import Roles as roles, Estado as estado

from app.utils.pagination import get_pagination

import logging

logger = logging.getLogger(__name__)

def validar_nuevo_centro(nombre):

    centro_existente = Centro.query.filter_by(
        nombre=nombre
    ).first()

    if centro_existente:

        logger.warning(f"Centro ya existe: {nombre}")

        return (
            False,
            {
                "message": "El centro ya existe",
                "status_code": 409
            }
        )

    return (
        True,
        None
    )

def crear_centro():
    data = request.get_json()

    nombre = data.get("nombre")
    direccion = data.get("direccion")

    ok, resultado = validar_nuevo_centro(nombre)

    if not ok:
        return (
            False,
            resultado
        )

    centro = Centro(
        nombre=nombre,
        direccion=direccion
    )

    db.session.add(centro)
    db.session.commit()

    logger.info(f"Centro creado: {centro.nombre} en {centro.direccion}")

    return (
        True,
        {
            "data": centro.to_dict(),
            "status_code": 201
        }
    )

def obtener_centro(id_centro):
    centro = Centro.query.get(id_centro)

    if not centro:

        logger.warning(f"Centro no encontrado: ID {id_centro}")

        return (
            False,
            {
                "message": "Centro no encontrado",
                "status_code": 404
            }
        )

    logger.info(f"Centro obtenido con nombre {centro.nombre} e ID {centro.id_centro}")

    return (
        True,
        {
            "data": centro.to_dict(),
            "status_code": 200
        }
    )

def listar_centros():
    page, size = get_pagination()

    pagination = Centro.query.paginate(page=page, per_page=size, error_out=False)

    centros = pagination.items

    logger.info(f"Listado de centros obtenido: {len(centros)} centros en la página {page} con tamaño {size}")

    return (
        True,
        {
            "data": [c.to_dict() for c in centros],
            "pagination": {
                "total": pagination.total,
                "pages": pagination.pages,
                "current_page": pagination.page,
                "per_page": pagination.per_page
            },
            "status_code": 200
        }
    )