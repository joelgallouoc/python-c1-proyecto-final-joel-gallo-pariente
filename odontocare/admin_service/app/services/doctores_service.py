from app.extensions import db

from app.models.doctor import Doctor

from app.utils.enums import Roles as roles, Estado as estado

from app.utils.pagination import get_pagination
from app.models.usuario import Usuario

from flask import request

import logging

logger = logging.getLogger(__name__)

def validar_nuevo_doctor(nombre):

    doctor_existente = Doctor.query.filter_by(
        nombre=nombre
    ).first()

    if doctor_existente:

        logger.warning(f"Doctor con nombre {nombre} ya existe")

        return (
            False,
            {
                "message": "El doctor ya existe",
                "status_code": 409
            }
        )

    return (
        True,
        None
    )

def crear_doctor():

    data = request.get_json()

    password = data.get("password")
    nombre = data.get("nombre")

    ok, resultado = validar_nuevo_doctor(nombre)

    if not ok:

        return (
            False,
            resultado
        )

    usuario = Usuario(
        username=data["username"],
        rol=roles.DOCTOR.value
    )

    usuario.set_password(password)

    db.session.add(usuario)
    db.session.flush()

    doctor = Doctor(
        id_usuario=usuario.id_usuario,
        nombre=nombre,
        especialidad=data["especialidad"]
    )

    db.session.add(doctor)
    db.session.commit()

    logger.info(f"Doctor creado: {doctor.nombre}")

    return (
        True,
        {
            "data": doctor.to_dict(),
            "status_code": 201
        }
    )

def listar_doctores():
    
    page, size = get_pagination()

    pagination = Doctor.query.paginate(page=page, per_page=size, error_out=False)

    logger.info(f"Listado de doctores obtenido: página {page}, tamaño {size}")

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

def obtener_doctor(id_doctor):

    doctor = Doctor.query.get(id_doctor)

    if not doctor:

        logger.warning(f"Intento de obtención de doctor no encontrado: {id_doctor}")

        return (
            False,
            {
                "message": "Doctor no encontrado",
                "status_code": 404
            }
        )

    logger.info(f"Doctor obtenido con nombre {doctor.nombre} e ID {doctor.id_doctor}")

    return (
        True,
        {
            "data": doctor.to_dict(),
            "status_code": 200
        }
    )