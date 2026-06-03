from enum import Enum

class UserRole(Enum):
    ADMIN = "ADMIN"
    SECRETARIA = "SECRETARIA"
    DOCTOR = "DOCTOR"
    PACIENTE = "PACIENTE"