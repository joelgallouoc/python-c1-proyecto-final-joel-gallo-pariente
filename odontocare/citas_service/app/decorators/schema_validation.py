from functools import wraps

from flask import request

from pydantic import ValidationError

from app.utils.response import error_response


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