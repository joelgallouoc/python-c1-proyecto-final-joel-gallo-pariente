from enum import Enum


"""
Enum que contiene los roles de usuario.
"""
class Roles(Enum):
    ADMIN = "ADMIN"
    SECRETARIA = "SECRETARIA"
    DOCTOR = "DOCTOR"
    PACIENTE = "PACIENTE"


"""
Enum que contiene el estado de los pacientes.
"""
class Estado(Enum):
    ACTIVO = "ACTIVO"
    INACTIVO = "INACTIVO"