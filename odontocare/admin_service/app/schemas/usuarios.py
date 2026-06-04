from app.utils.enums import Roles

from . import PaginationSchema, NewBaseModel

class CreateUserSchema(NewBaseModel):
    username: str
    password: str
    role: Roles
    
class UserListFiltersSchema(PaginationSchema):
    pass