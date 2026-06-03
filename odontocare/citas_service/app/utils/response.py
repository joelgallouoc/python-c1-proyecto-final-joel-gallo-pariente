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
    status_code=400
):

    return jsonify({
        "success": False,
        "message": message
    }), status_code