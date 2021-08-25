from sql.schemas.user import UserOut
from pydantic import BaseModel


class TokenUser(BaseModel):
    token: str
    user: UserOut


class Settings(BaseModel):
    authjwt_secret_key: str = "secret"
