from functools import wraps

import logging

logger = logging.getLogger(__name__)


def handle_exceptions(fn):

    @wraps(fn)
    def wrapper(*args, **kwargs):

        try:

            return fn(*args, **kwargs)

        except Exception as e:

            logger.exception(
                f"Unhandled exception in {fn.__name__}"
            )

            return {
                "success": False,
                "message": "Internal server error"
            }, 500

    return wrapper