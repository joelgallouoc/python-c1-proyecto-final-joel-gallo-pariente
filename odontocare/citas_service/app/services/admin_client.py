import requests

import os
from dotenv import load_dotenv

load_dotenv()

ADMIN_URL = os.getenv("ADMIN_URL")

def get_paciente(
    paciente_id,
    token
):

    response = requests.get(
        f"{ADMIN_URL}/admin/pacientes/{paciente_id}",
        headers={
            "Authorization": f"Bearer {token}"
        },
        timeout=5
    )

    return response

def get_doctor(
    doctor_id,
    token
):

    response = requests.get(
        f"{ADMIN_URL}/admin/doctores/{doctor_id}",
        headers={
            "Authorization": f"Bearer {token}"
        },
        timeout=5
    )

    return response

def get_centro(
    centro_id,
    token
):

    response = requests.get(
        f"{ADMIN_URL}/admin/centros/{centro_id}",
        headers={
            "Authorization": f"Bearer {token}"
        },
        timeout=5
    )

    return response

def check_admin_service():

    try:

        response = requests.get(
            f"{ADMIN_URL}/health",
            timeout=3
        )

        return response.status_code == 200

    except Exception:

        return False