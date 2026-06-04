from typing import Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    Field
)


"""
Esquema base que añade la restricción de recoger elementos no indicados en el esquema.

Utilizado por:
- Todos los endpoints.
"""
class NewBaseModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid"
    )


"""
Esquema base para paginación.

Campos:
- page: int > 0
- per_page: int > 0

Utilizado por:
- Todos los endpoints de listado.
"""
class PaginationSchema(NewBaseModel):
    
    page: Optional[int] = Field(
        default=1,
        gt=0
    )

    size: Optional[int] = Field(
        default=100,
        gt=0
    )