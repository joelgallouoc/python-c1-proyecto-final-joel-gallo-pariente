from functools import wraps

from flask import jsonify

from flask_jwt_extended import (
    verify_jwt_in_request,
    get_jwt
)

def role_required(*roles):

    def decorator(fn):

        @wraps(fn)
        def wrapper(*args, **kwargs):

            verify_jwt_in_request()

            claims = get_jwt()

            print(claims)
            print(roles)

            if claims["role"] not in roles:

                return jsonify({
                    "success": False,
                    "message": "Access denied"
                }), 403

            return fn(*args, **kwargs)

        return wrapper

    return decorator