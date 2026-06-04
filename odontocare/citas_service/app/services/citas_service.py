from datetime import datetime, timedelta

from app.services.admin_client import (
    get_paciente,
    get_doctor,
    get_centro
)

from app.models.cita import Cita

from flask_jwt_extended import get_jwt, get_jwt_identity


from flask import request

from app.extensions import db

import logging

from app.utils.pagination import get_pagination

logger = logging.getLogger(__name__)


"""
Valida la existencia y estado de un paciente.

Parámetros:
- paciente_id: int
- token: str

Funcionamiento:
- Consulta el servicio de administración.
- Comprueba la existencia del paciente.
- Comprueba que se encuentre en estado ACTIVO.

Retorno:

Success:
(
    True,
    paciente
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


"""
Valida la existencia de un doctor

Parámetros:
- doctor_id: int
- token: str

Funcionamiento:
- Consulta el servicio de administración.
- Comprueba la existencia del doctor.

Retorno:

Success:
(
    True,
    response.json()["data"]
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


"""
Valida la existencia de un centro

Parámetros:
- centro_id: int
- token: str

Funcionamiento:
- Consulta el servicio de administración.
- Comprueba la existencia del centro.

Retorno:

Success:
(
    True,
    response.json()["data"]
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


"""
Comprueba si existe una cita para este doctor en el mismo horario

Parámetros:
- doctor_id: int
- fecha: str

Funcionamiento:
- Consulta las citas del doctor para esa fecha.
- Si obtiene alguna existe conflicto.

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


"""
Comprueba si existe una cita para este doctor en el mismo horario

Parámetros:
- data: any
- token: str

Responsabilidades:
- Validar paciente.
- Validar doctor.
- Validar centro.
- Comprobar disponibilidad del doctor.

Validaciones:
- El paciente debe existir.
- El paciente debe estar activo.
- El doctor debe existir.
- El centro debe existir.
- No debe existir conflicto horario.

Retorno:

Success:
(
    True,
    None
)

Error:
(
    ok, resultado
)
"""
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


"""
Servicio de creación de citas.

Responsabilidades:
- Obtener los datos de la petición.
- Validar paciente.
- Validar doctor.
- Validar centro.
- Comprobar disponibilidad del doctor.
- Registrar la cita en base de datos.

Validaciones:
- El paciente debe existir.
- El paciente debe estar activo.
- El doctor debe existir.
- El centro debe existir.
- No debe existir conflicto horario.

Retorno:

Success:
(
    True,
    {
        "data": cita.to_dict(),
        "status_code": 201
    }
)

Error:
(
    ok, 
    resultado
)
"""
def crear_cita():
    
    data = request.get_json()

    token = request.headers.get(
        "Authorization"
    ).replace(
        "Bearer ",
        ""
    )
    
    fecha = datetime.strptime(
        data["fecha"],
        "%Y-%m-%d %H:%M"
    )

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


"""
Servicio de consulta de citas.

Parámetros:
- id_cita: int

Responsabilidades:
- Obtener la cita que se indica.

Retorno:

Success:
(
    True,
    cita.to_dict()
    
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


"""
Servicio de listado de citas.

Responsabilidades:
- Obtener las cita que se indica.

Retorno:
(
    True, 
    {
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
)
"""
def obtener_listado_citas():

    claims = get_jwt()

    role = claims["role"]

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


"""
Servicio de cancelacion de citas.

Parámetros:
- id_cita: int

Responsabilidades:
- Cancelar la cita indicada.

Retorno:

Success:
(
    True,
    {
        "message" : str
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