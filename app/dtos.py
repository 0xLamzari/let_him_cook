from typing import Optional

from pydantic import BaseModel

class UserRequest(BaseModel):
    email: str
    password: str

class UserInDB(BaseModel):
    email: str
    hashed_password: str

class Token(BaseModel):
    token_type: str
    access_token: str

class LoginResponse(BaseModel):
    message: str
    token: Optional[Token] = None