from .base import PaginationSchema, NewBaseModel


"""
Esquema Pydantic para creación de doctores.

Campos:
- username: str
- password: str
- nombre: str
- especialidad: str

Utilizado por:
- POST /admin/doctores
"""
class CreateDoctorSchema(NewBaseModel):
    username: str
    password: str

    nombre: str
    especialidad: str


"""
Esquema Pydantic para los query params del listado de doctores.

Campos:
- page: Optional[int]
- size: Optional[int]

Utilizado por:
- GET /admin/doctores
""" 
class DoctorFiltersSchema(PaginationSchema):
    pass