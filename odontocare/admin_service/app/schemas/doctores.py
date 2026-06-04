from . import PaginationSchema, NewBaseModel

class CreateDoctorSchema(NewBaseModel):
    username: str
    password: str

    nombre: str
    especialidad: str
    
class DoctorFiltersSchema(PaginationSchema):
    pass