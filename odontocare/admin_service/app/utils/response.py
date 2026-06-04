from flask import jsonify


def success_response(
    data=None,
    message=None,
    pagination=None,
    status_code=200
):

    payload = {
        "success": True
    }

    if message:
        payload["message"] = message

    if data is not None:
        payload["data"] = data

    if pagination:
        payload["pagination"] = pagination

    return jsonify(payload), status_code


def error_response(
    message,
    status_code,
    data=None
):

    response = {
        "success": False,
        "message": message
    }

    if data is not None:

        response["data"] = data

    return jsonify(response), status_code