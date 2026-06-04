from functools import wraps

from app.utils.enums import Roles

from flask import jsonify, request

from flask_jwt_extended import (
    verify_jwt_in_request,
    get_jwt
)

"""
Decorador de autorización basado en roles.

Verifica que el usuario autenticado mediante JWT posea
uno de los roles permitidos para acceder al endpoint.

Funcionamiento:
- Comprueba la existencia de un JWT válido.
- Obtiene los claims del token.
- Valida que el rol contenido en el claim 'role'
  pertenezca a la lista de roles permitidos.

Parámetros:
- *roles:
  Lista variable de roles autorizados.

Ejemplo:
@role_required("ADMIN")

@role_required(
    "ADMIN",
    "SECRETARIA"
)

Posibles respuestas:
- 403: Access denied
"""
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


"""
Decorador de validación de roles de usuario.

Se utiliza durante la creación de usuarios para validar
que el rol recibido en el body de la petición sea uno de
los permitidos. Pensando en una aplicacion profesional podría ser usada en futuros endpoints, por ello se ha decidido generar un decorador.

Funcionamiento:
- Obtiene el body de la petición.
- Comprueba el campo 'role'.
- Valida que pertenezca a los roles permitidos.

Parámetros:
- *roles:
  Roles permitidos para el usuario a crear.

Ejemplo:
@user_role_required(
    "ADMIN",
    "SECRETARIA"
)

Posibles respuestas:
- 400: User role incorrect
"""
def user_role_required(*roles):

    def decorator(fn):

        @wraps(fn)
        def wrapper(*args, **kwargs):

            data = request.get_json()

            if data.get("rol") not in roles:

                return jsonify({
                    "success": False,
                    "message": f"User role incorrect. Only {Roles.ADMIN.value} and {Roles.SECRETARIA.value} are allowed."
                }), 400


            return fn(*args, **kwargs)

        return wrapper

    return decorator