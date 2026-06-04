from enum import Enum

class Roles(Enum):
    ADMIN = "ADMIN"
    SECRETARIA = "SECRETARIA"
    DOCTOR = "DOCTOR"
    PACIENTE = "PACIENTE"

class EstadoCita(Enum):
    PROGRAMADA = "PROGRAMADA"
    CANCELADA = "CANCELADA"