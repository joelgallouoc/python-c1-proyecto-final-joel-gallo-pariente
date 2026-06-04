from typing import Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    Field
)

class NewBaseModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid"
    )

class PaginationSchema(NewBaseModel):
    
    page: Optional[int] = Field(
        default=1,
        gt=0
    )

    per_page: Optional[int] = Field(
        default=100,
        gt=0
    )