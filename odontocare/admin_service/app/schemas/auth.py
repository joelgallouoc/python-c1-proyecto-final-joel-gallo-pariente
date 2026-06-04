from app.schemas.base import NewBaseModel


"""
Esquema Pydantic para autenticación.

Campos:
- username: str
- password: str

Utilizado por:
- POST /auth/login
"""
class LoginSchema(NewBaseModel):
    username: str
    password: str