from .base import PaginationSchema, NewBaseModel


"""
Esquema Pydantic para creación de centros.

Campos:
- nombre: str
- direccion: str

Utilizado por:
- POST /admin/centros
"""
class CreateCenterSchema(NewBaseModel):
    nombre: str
    direccion: str

"""
Esquema Pydantic para los query params del listado de centros.

Campos:
- page: Optional[int]
- size: Optional[int]

Utilizado por:
- GET /admin/centros
""" 
class CenterFiltersSchema(PaginationSchema):
    pass