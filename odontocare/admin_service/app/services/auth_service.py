from app.models.usuario import Usuario

from flask import request

from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity
)

from app.extensions import db

import logging

logger = logging.getLogger(__name__)


def log_in():
   
    data = request.get_json()

    if not data:
        logger.warning("JSON requerido")
        return False, {"message": "JSON requerido"}

    username = data.get("username")
    password = data.get("password")

    usuario = Usuario.query.filter_by(
        username=username
    ).first()

    if not usuario:
        logger.warning(f"Usuario no encontrado: {username}")
        return False, {"message": "Usuario no encontrado", "status_code": 404}

    if not usuario.check_password(password):
        logger.warning(f"Credenciales incorrectas para el usuario: {username}")
        return False, {"message": "Credenciales incorrectas", "status_code": 401}

    token = create_access_token(
        identity=str(usuario.id_usuario),
        additional_claims={
            "username": usuario.username,
            "role": usuario.rol
        }
    )

    logger.info(f"Usuario autenticado: {username} (ID: {usuario.id_usuario})")

    return True, {"data": {"access_token": token}}

def obtain_me():
    user_id = int(get_jwt_identity())

    usuario = db.session.get(
        Usuario,
        user_id
    )

    if not usuario:
        logger.warning(f"Usuario no encontrado: {user_id}")
        return False,{"message": "Usuario no encontrado", "status_code": 404}
    
    logger.info(f"Obteniendo información del usuario: {user_id}")

    return True, {"data": usuario.to_dict()}