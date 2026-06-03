from enum import Enum

class Roles(Enum):
    ADMIN = "ADMIN"
    SECRETARIA = "SECRETARIA"
    DOCTOR = "DOCTOR"
    PACIENTE = "PACIENTE"

class Estado(Enum):
    ACTIVO = "ACTIVO"
    INACTIVO = "INACTIVO"