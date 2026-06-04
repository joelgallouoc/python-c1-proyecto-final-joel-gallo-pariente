from . import PaginationSchema, NewBaseModel

class CreatePatientSchema(NewBaseModel):
    username: str
    password: str

    nombre: str
    telefono: str


class PatientFiltersSchema(PaginationSchema):
    pass