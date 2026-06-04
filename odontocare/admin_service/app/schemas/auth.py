from pydantic import ConfigDict

from . import NewBaseModel

class LoginSchema(NewBaseModel):
    username: str
    password: str