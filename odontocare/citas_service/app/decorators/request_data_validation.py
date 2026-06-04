from functools import wraps

from flask import request

from app.utils.response import error_response


def validate_request_data(
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