from pydantic import BaseModel, ConfigDict

from . import NewBaseModel, PaginationSchema

from typing import Optional

class CreateAppointmentSchema(NewBaseModel):

    fecha: str
    motivo: str

    id_paciente: int
    id_doctor: int
    id_centro: int
    
class AppointmentFiltersSchema(PaginationSchema):

    fecha: Optional[str] = None

    id_doctor: Optional[int] = None
    id_paciente: Optional[int] = None
    id_centro: Optional[int] = None

    estado: Optional[str] = None