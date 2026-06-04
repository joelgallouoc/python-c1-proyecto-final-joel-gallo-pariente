from functools import wraps

from flask import jsonify

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