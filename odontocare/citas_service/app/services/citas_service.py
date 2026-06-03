from datetime import datetime, timedelta

from app.services.admin_client import (
    get_paciente,
    get_doctor,
    get_centro
)

from app.models.cita import Cita

from flask_jwt_extended import get_jwt_identity


from flask import request

from app.extensions import db

import logging

from app.utils.pagination import get_pagination

logger = logging.getLogger(__name__)


def validar_paciente(
    paciente_id,
    token
):

    response = get_paciente(
        paciente_id,
        token
    )

    if response.status_code != 200:

        return (
            False,
            {
                "message": "Paciente no existe",
                "status_code": 404
            }
        )

    paciente = response.json()["data"]

    if paciente["estado"] != "ACTIVO":

        return (
            False,
            {
                "message": "Paciente inactivo",
                "status_code": 409
            }
        )

    return (
        True,
        paciente
    )

def validar_doctor(
    doctor_id,
    token
):

    response = get_doctor(
        doctor_id,
        token
    )

    if response.status_code != 200:

        return (
            False,
            {
                "message": "Doctor no existe",
                "status_code": 404
            }
        )

    return (
        True,
        response.json()["data"]
    )

def validar_centro(
    centro_id,
    token
):

    response = get_centro(
        centro_id,
        token
    )

    if response.status_code != 200:

        return (
            False,
            {
                "message": "Centro no existe",
                "status_code": 404
            }
        )

    return (
        True,
        response.json()["data"]
    )

def existe_conflicto(
    doctor_id,
    fecha
):

    conflicto = Cita.query.filter_by(
        id_doctor=doctor_id,
        fecha=fecha
    ).first()

    if conflicto:

        return (
            False,
            {
                "message": "El doctor ya tiene una cita programada para esa fecha y hora",
                "status_code": 409
            }
        )

    return (
        True,
        None
    )

def validar_nueva_cita(
    data,
    token
):
    fecha = datetime.strptime(
        data["fecha"],
        "%Y-%m-%d %H:%M"
    )

    ok, resultado = validar_paciente(
        data["id_paciente"],
        token
    )

    if not ok:
        return ok, resultado

    ok, resultado = validar_doctor(
        data["id_doctor"],
        token
    )

    if not ok:
        return ok, resultado

    ok, resultado = validar_centro(
        data["id_centro"],
        token
    )

    if not ok:
        return ok, resultado

    ok, resultado = existe_conflicto(
        data["id_doctor"],
        fecha
    )

    if not ok:
        return ok, resultado

    return (
        True,
        None
    )

def crear_cita(
    data,
    token
):
    fecha = datetime.strptime(
        data["fecha"],
        "%Y-%m-%d %H:%M"
    )

    # Validación de nueva cita. Se comprueba que el paciente, doctor y centro existen, que el doctor está disponible a esa hora, etc... 
    # Se usa un booleano 'ok' para indicar si la validación ha sido correcta o no, y un diccionario 'resultado' para almacenar el mensaje de error o los datos de la cita creada.
    # En caso de que alguna validación falle, se devuelve un error con el mensaje correspondiente.
    ok, resultado = validar_nueva_cita(
        data,
        token
    )

    if not ok:
        return ok, resultado

    cita = Cita(
        fecha=fecha,
        motivo=data["motivo"],
        estado="PROGRAMADA",
        id_paciente=data["id_paciente"],
        id_doctor=data["id_doctor"],
        id_centro=data["id_centro"],
        id_usuario_registra=int(
            get_jwt_identity()
        )
    )

    db.session.add(cita)
    db.session.commit()

    logger.info(f"Cita creada: {cita.id_cita} para paciente {cita.id_paciente} con doctor {cita.id_doctor} en centro {cita.id_centro} a las {cita.fecha}")

    return True, { "data": cita.to_dict(), "status_code": 201 }

def consultar_cita(
    id_cita
):

    cita = db.session.get(
        Cita,
        id_cita
    )

    if not cita:

        return False,
        {     
            "message": "Cita no encontrada",
            "status_code": 404
        }

    return (
        True,
        cita.to_dict()
    )

def obtener_listado_citas(
    role
):

    page, size = get_pagination()

    query = Cita.query

    if role == "ADMIN":

        doctor = request.args.get(
            "doctor"
        )

        paciente = request.args.get(
            "paciente"
        )

        centro = request.args.get(
            "centro"
        )

        estado = request.args.get(
            "estado"
        )

        fecha = request.args.get(
            "fecha"
        )

        if doctor:
            query = query.filter_by(
                id_doctor=doctor
            )

        if paciente:
            query = query.filter_by(
                id_paciente=paciente
            )

        if centro:
            query = query.filter_by(
                id_centro=centro
            )

        if estado:
            query = query.filter_by(
                estado=estado
            )

        if fecha:

            fecha_inicio = datetime.strptime(
                fecha,
                "%Y-%m-%d"
            )

            fecha_fin = fecha_inicio + timedelta(days=1)

            query = query.filter(
                Cita.fecha >= fecha_inicio,
                Cita.fecha < fecha_fin
            )

    elif role == "SECRETARIA":

        fecha = request.args.get(
            "fecha"
        )

        if fecha:

            fecha_inicio = datetime.strptime(
                fecha,
                "%Y-%m-%d"
            )

            fecha_fin = fecha_inicio + timedelta(days=1)

            query = query.filter(
                Cita.fecha >= fecha_inicio,
                Cita.fecha < fecha_fin
            )

    elif role == "MEDICO":

        user_id = int(get_jwt_identity())

        query = query.filter(
                Cita.id_doctor == user_id
            )

    pagination = query.paginate(page=page, per_page=size, error_out=False)

    return True, {
        "data": [
            cita.to_dict()
            for cita in pagination.items
        ],
        "pagination": {
            "page": pagination.page,
            "size": pagination.per_page,
            "total_items": pagination.total,
            "total_pages": pagination.pages
        }
    }

def cancelacion_cita(
    id_cita
):

    cita = db.session.get(
        Cita,
        id_cita
    )

    if not cita:

        return False, {
            "message": "Cita no encontrada",
            "status_code": 404
        }

    if cita.estado == "CANCELADA":

        return False, {
            "message": "La cita ya está cancelada",
            "status_code": 409
        }

    cita.estado = "CANCELADA"

    db.session.commit()

    return True, {
        "message": "Cita cancelada correctamente"
    }