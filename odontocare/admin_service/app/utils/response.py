from flask import jsonify


"""
Servicio de formateo de mensajes de respuesta correctos.

Campos:
- data
- message
- pagination
- status_code=200 (valor default)

Utilizado por todos los endpoints
"""
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


"""
Servicio de formateo de mensajes de error.

Campos:
- message
- status_code=400(Default)
- data

Utilizado por todos los endpoints
"""
def error_response(
    message,
    status_code=400,
    data=None
):

    response = {
        "success": False,
        "message": message
    }

    if data is not None:

        response["data"] = data

    return jsonify(response), status_code