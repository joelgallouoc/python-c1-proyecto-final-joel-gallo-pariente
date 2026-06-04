from functools import wraps

from flask import request

from app.utils.response import error_response


"""
Decorador de validación de estructura de petición.

Permite controlar de forma genérica si un endpoint
acepta body, query params o ambos.

Funcionamiento:
- Comprueba la existencia de body.
- Comprueba la existencia de query params.
- Valida si son obligatorios.
- Valida si están permitidos.

Parámetros:
- allow_body:
  Indica si el endpoint admite body.

- allow_query:
  Indica si el endpoint admite query params.

- body_required:
  Indica si el body es obligatorio.

- query_required:
  Indica si los query params son obligatorios.

Ejemplos:

@validate_request_data()

No admite body ni query params.

@validate_request_data(
    allow_body=True,
    body_required=True
)

Body obligatorio.

@validate_request_data(
    allow_query=True
)

Query params opcionales.

Posibles respuestas:
- 422: Request body is required
- 422: Request body is not allowed
- 422: Query parameters are required
- 422: Query parameters are not allowed
"""
def validate_request_data(
    allow_query=False,
    allow_body=False,
    body_required=False,
    query_required=False
):

    def decorator(fn):

        @wraps(fn)
        def wrapper(*args, **kwargs):

            body = request.get_json(
                silent=True
            )

            query = request.args

            #
            # BODY
            #

            if body_required and body is None:

                return error_response(
                    message="Request body is required",
                    status_code=422
                )

            if (
                not allow_body and
                not body_required and
                body is not None
            ):

                return error_response(
                    message="Request body is not allowed for this endpoint",
                    status_code=422
                )

            #
            # QUERY PARAMS
            #

            if query_required and not query:

                return error_response(
                    message="Query parameters are required",
                    status_code=422
                )

            if (
                not allow_query and
                not query_required and
                query
            ):

                return error_response(
                    message="Query parameters are not allowed for this endpoint",
                    status_code=422
                )

            return fn(*args, **kwargs)

        return wrapper

    return decorator