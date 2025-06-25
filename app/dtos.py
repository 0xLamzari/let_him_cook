from typing import Optional

from pydantic import BaseModel

class UserRequest(BaseModel):
    email: str
    password: str

class UserInDB(BaseModel):
    email: str
    hashed_password: str

class LoginResponse(BaseModel):
    message: str