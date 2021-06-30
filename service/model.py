from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    username: str
    password: str
    full_name: str
    disabled: bool

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None


class UserInDB(User):
    password: str
    disabled: bool

class News(BaseModel):
    id: int
    url_path: str
    url_image: str
    title: str
    subtitle: str
    time: str
    category: str