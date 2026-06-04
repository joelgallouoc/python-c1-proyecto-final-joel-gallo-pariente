from app.utils.enums import Roles

from .base import PaginationSchema, NewBaseModel


"""
Esquema Pydantic para creación de usuarios.

Campos:
- username: str
- password: str
- role: str

Utilizado por:
- POST /admin/usuarios
- POST /admin/pacientes
- POST /admin/doctores
"""
class CreateUserSchema(NewBaseModel):
    username: str
    password: str
    role: Roles


"""
Esquema Pydantic para los query params del listado de usuarios.

Campos:
- page: Optional[int]
- size: Optional[int]

Utilizado por:
- GET /admin/usuarios
"""
class UserListFiltersSchema(PaginationSchema):
    pass