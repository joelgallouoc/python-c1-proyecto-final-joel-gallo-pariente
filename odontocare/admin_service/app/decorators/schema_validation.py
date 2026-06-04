from functools import wraps

from flask import request

from pydantic import ValidationError

from app.utils.response import error_response


"""
Decorador de validación de body mediante Pydantic.

Valida el contenido del body utilizando un esquema
Pydantic previamente definido.

Funcionamiento:
- Obtiene el JSON de la petición.
- Instancia el esquema recibido.
- Ejecuta las validaciones automáticas de Pydantic.

Parámetros:
- schema:
  Clase Pydantic utilizada para validar el body.

Ejemplo:

@validate_body(
    LoginSchema
)

@validate_body(
    CreateUserSchema
)

Posibles respuestas:
- 422: Validation error
"""
def validate_body(schema):

    def decorator(fn):

        @wraps(fn)
        def wrapper(*args, **kwargs):

            try:

                data = request.get_json()

                if data is None:

                    return error_response(
                        message="Request body is required",
                        status_code=422
                    )

                schema(**data)

            except ValidationError as e:

                return error_response(
                    message="Validation error",
                    data=e.errors(),
                    status_code=422
                )

            return fn(*args, **kwargs)

        return wrapper

    return decorator


"""
Decorador de validación de query params mediante Pydantic.

Valida los parámetros de consulta utilizando
un esquema Pydantic.

Funcionamiento:
- Obtiene request.args.
- Convierte los datos a diccionario.
- Ejecuta las validaciones definidas en el esquema.

Parámetros:
- schema:
  Esquema Pydantic utilizado para validar
  los query params.

Posibles respuestas:
- 422: Validation error
"""
def validate_query(schema):

    def decorator(fn):

        @wraps(fn)
        def wrapper(*args, **kwargs):

            try:

                schema(
                    **request.args.to_dict()
                )

            except ValidationError as e:

                return error_response(
                    message="Validation error",
                    data=e.errors(),
                    status_code=422
                )

            return fn(*args, **kwargs)

        return wrapper

    return decorator