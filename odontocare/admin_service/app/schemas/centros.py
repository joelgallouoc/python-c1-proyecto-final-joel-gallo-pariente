from . import PaginationSchema, NewBaseModel

class CreateCenterSchema(NewBaseModel):
    nombre: str
    direccion: str
    
class CenterFiltersSchema(PaginationSchema):
    pass