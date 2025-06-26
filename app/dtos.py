from pydantic import BaseModel, EmailStr


class Profile(BaseModel):
    name: str
    surname: str

class RegistrationRequest(BaseModel):
    email: EmailStr
    password: str
    profile_data: Profile
    enable_2fa: bool = False

class UserInDB(BaseModel):
    email: EmailStr
    hashed_password: str
    enable_2fa: bool

class Token(BaseModel):
    token_type: str
    access_token: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    message: str
    token: Token | None = None

class OTPRequest(BaseModel):
    email: EmailStr
    otp: str