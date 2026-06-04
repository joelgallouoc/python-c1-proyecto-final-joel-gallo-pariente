import csv
import requests

import os
from dotenv import load_dotenv

load_dotenv()

ADMIN_URL = os.getenv("ADMIN_URL")
CITAS_URL = os.getenv("CITAS_URL")

def login():

    response = requests.post(
        f"{ADMIN_URL}/auth/login",
        json={
            "username": "admin",
            "password": "admin123"
        }
    )

    response.raise_for_status()

    return response.json()["data"]["access_token"]

def get_headers(token):

    return {
        "Authorization": f"Bearer {token}"
    }

def procesar_csv(
    fichero,
    endpoint,
    token,
    base_url
):

    with open(
        fichero,
        encoding="utf-8"
    ) as csv_file:

        reader = csv.DictReader(csv_file)

        for row in reader:

            response = requests.post(
                f"{base_url}{endpoint}",
                json=row,
                headers=get_headers(token)
            )

            print(
                endpoint,
                response.status_code
            )

            if response.status_code not in (
                200,
                201
            ):

                print(
                    response.text
                )

def cargar_centros(token):

    procesar_csv(
        "data/centros.csv",
        "/admin/centros",
        token,
        ADMIN_URL
    )

def cargar_doctores(token):

    procesar_csv(
        "data/doctores.csv",
        "/admin/doctores",
        token,
        ADMIN_URL
    )

def cargar_pacientes(token):

    procesar_csv(
        "data/pacientes.csv",
        "/admin/pacientes",
        token,
        ADMIN_URL
    )

def cargar_usuarios(token):

    procesar_csv(
        "data/usuarios.csv",
        "/admin/usuarios",
        token,
        ADMIN_URL
    )

def cargar_citas(token):

    with open(
        "data/citas.csv",
        encoding="utf-8"
    ) as csv_file:

        reader = csv.DictReader(csv_file)

        for row in reader:

            payload = {
                "fecha": row["fecha"],
                "motivo": row["motivo"],
                "id_paciente": int(
                    row["id_paciente"]
                ),
                "id_doctor": int(
                    row["id_doctor"]
                ),
                "id_centro": int(
                    row["id_centro"]
                )
            }

            response = requests.post(
                f"{CITAS_URL}/citas",
                json=payload,
                headers=get_headers(token)
            )

            print(
                "/citas",
                response.status_code
            )

            if response.status_code not in (
                200,
                201
            ):

                print(
                    response.text
                )

def main():

    token = login()

    print("Cargando centros...")
    cargar_centros(token)

    print("Cargando doctores...")
    cargar_doctores(token)

    print("Cargando pacientes...")
    cargar_pacientes(token)

    print("Cargando usuarios...")
    cargar_usuarios(token)

    print("Cargando citas...")
    cargar_citas(token)

    print("Carga completada")

if __name__ == "__main__":
    main()