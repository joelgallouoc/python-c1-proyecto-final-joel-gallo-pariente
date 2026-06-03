from functools import wraps

from app.utils.enums import Roles

from flask import jsonify, request

from flask_jwt_extended import (
    verify_jwt_in_request,
    get_jwt
)

'''
Decoradores para verificar roles de usuario en rutas protegidas. El decorador `role_required` verifica el rol del usuario que realiza la peticióna través de los claims del JWT.

params:
- *roles: Lista de roles permitidos para la creación de usuarios (por ejemplo, "ADMIN", "SECRETARIA").

'''
def role_required(*roles):

    def decorator(fn):

        @wraps(fn)
        def wrapper(*args, **kwargs):

            verify_jwt_in_request()

            claims = get_jwt()

            if claims["role"] not in roles:

                return jsonify({
                    "success": False,
                    "message": "Access denied"
                }), 403

            return fn(*args, **kwargs)

        return wrapper

    return decorator

'''
Decorador para verificar roles específicos en la creación de usuarios. Este decorador se utiliza para validar que el rol proporcionado en el cuerpo de la petición sea uno de los roles 
permitidos (ADMIN o SECRETARIA) al crear un nuevo usuario.

params:
- *roles: Lista de roles permitidos para la creación de usuarios (por ejemplo, "ADMIN", "SECRETARIA").

'''
def user_role_required(*roles):

    def decorator(fn):

        @wraps(fn)
        def wrapper(*args, **kwargs):

            data = request.get_json()

            if data.get("role") not in roles:

                return jsonify({
                    "success": False,
                    "message": f"User role incorrect. Only {Roles.ADMIN.value} and {Roles.SECRETARIA.value} are allowed."
                }), 400


            return fn(*args, **kwargs)

        return wrapper

    return decorator