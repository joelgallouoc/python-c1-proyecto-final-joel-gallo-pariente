from datetime import datetime

from pydantic import Field, field_validator

from .base import NewBaseModel, PaginationSchema

from typing import Optional

from app.utils.enums import EstadoCita


"""
Esquema Pydantic para creación de citas.

Campos:
- fecha: str
- motivo: str
- id_paciente: int
- id_doctor: int
- id_centro: int

Validaciones:
- IDs mayores que 0
- Formato fecha:
  YYYY-MM-DD HH:MM

Utilizado por:
- POST /citas
"""
class CreateCitaSchema(NewBaseModel):

    fecha: str
    motivo: str

    id_paciente: int = Field(
        default=1,
        gt=0
    )
    
    id_doctor: int = Field(
        default=1,
        gt=0
    )
    
    id_centro: int = Field(
        default=1,
        gt=0
    )
    
    @field_validator("fecha")
    @classmethod
    def validate_fecha(cls, value):

        try:

            datetime.strptime(
                value,
                "%Y-%m-%d %H:%M"
            )

        except ValueError:

            raise ValueError(
                "Date format must be YYYY-MM-DD HH:MM"
            )

        return value
   

"""
Esquema Pydantic para los filtros del listado de citas para usuarios con rol ADMIN.

Campos:
- fecha: str
- estado: EstadoCita
- id_paciente: int
- id_doctor: int
- id_centro: int

Validaciones:
- IDs mayores que 0
- Formato fecha:
  YYYY-MM-DD HH:MM
- Estado cita = 'PROGRAMADA' o 'CANCELADA'

Utilizado por:
- GET /citas
"""
class AdminCitaFiltersSchema(PaginationSchema):
    fecha: Optional[str] = None

    id_doctor: Optional[int] = Field(
        default=1,
        gt=0
    )
    
    id_paciente: Optional[int] = Field(
        default=1,
        gt=0
    )
    
    id_centro: Optional[int] = Field(
        default=1,
        gt=0
    )

    estado: Optional[EstadoCita] = None
    
    @field_validator("fecha")
    @classmethod
    def validate_fecha(cls, value):

        try:

            datetime.strptime(
                value,
                "%Y-%m-%d %H:%M"
            )

        except ValueError:

            raise ValueError(
                "Date format must be YYYY-MM-DD HH:MM"
            )

        return value
    

"""
Esquema Pydantic para los filtros del listado de citas para usuarios con rol SECRETARIA.

Campos:
- fecha: str

Validaciones:
- Formato fecha:
  YYYY-MM-DD HH:MM

Utilizado por:
- GET /citas
"""
class SecretariaAppointmentFiltersSchema(PaginationSchema):
    fecha: Optional[str] = None
    
    @field_validator("fecha")
    @classmethod
    def validate_fecha(cls, value):

        try:
            
            datetime.strptime(
                value,
                "%Y-%m-%d %H:%M"
            )

        except ValueError:

            raise ValueError(
                "Date format must be YYYY-MM-DD HH:MM"
            )

        return value


"""
Esquema Pydantic para los filtros del listado de citas para usuarios con rol DOCTOR.

Campos:
- fecha: str

Validaciones:
- Formato fecha:
  YYYY-MM-DD HH:MM

Utilizado por:
- GET /citas
"""
class DoctorAppointmentFiltersSchema(PaginationSchema):
    fecha: Optional[str] = None
    
    @field_validator("fecha")
    @classmethod
    def validate_fecha(cls, value):

        try:
            
            datetime.strptime(
                value,
                "%Y-%m-%d %H:%M"
            )

        except ValueError:

            raise ValueError(
                "Date format must be YYYY-MM-DD HH:MM"
            )

        return value