from .base import PaginationSchema, NewBaseModel


"""
Esquema Pydantic para creación de pacientes.

Campos:
- username: str
- password: str
- nombre: str
- telefono: str

Utilizado por:
- POST /admin/pacientes
"""
class CreatePatientSchema(NewBaseModel):
    username: str
    password: str

    nombre: str
    telefono: str


"""
Esquema Pydantic para los query params del listado de pacientes.

Campos:
- page: Optional[int]
- size: Optional[int]

Utilizado por:
- GET /admin/pacientes
""" 
class PatientFiltersSchema(PaginationSchema):
    pass