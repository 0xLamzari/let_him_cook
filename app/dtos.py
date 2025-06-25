from pydantic import BaseModel

class UserRegistrationRequest(BaseModel):
    email: str
    password: str

class UserInDB(BaseModel):
    email: str
    hashed_password: str