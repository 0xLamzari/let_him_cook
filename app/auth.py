import os, random
from datetime import timedelta, datetime, timezone
from jose import jwt
from . import database, hashing, dtos

OTP_EXPIRATION_MINUTES = int(os.getenv("OTP_EXPIRATION_MINUTES", 5))
ACCESS_TOKEN_EXPIRATION_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRATION_MINUTES", 30))
SECRET_KEY = os.getenv("SECRET_KEY", "a_secret_key_long_enough_to_let_him_cook_without_problems")
ALGORITHM = "HS256"

def create_access_token(data: dict) -> str:
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRATION_MINUTES)

    to_encode = data.copy()
    expires_at = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expires_at})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def authenticate_user(email: str, password: str) -> dtos.UserInDB | None:
    user = database.get_user_by_email(email)
    if not user:
        return None
    if not hashing.verify_password(password, user.hashed_password):
        return None
    return user


def generate_and_store_otp(email : str) -> str:
    otp = str(random.randint(100000, 999999))
    expires = timedelta(minutes=OTP_EXPIRATION_MINUTES)

    database.store_otp(email=email, otp=otp, expires_delta=expires)

    return otp


def verify_otp(email: str, input_otp: str) -> bool:
    stored_otp_data = database.get_stored_otp(email)
    if not stored_otp_data:
        return False

    if datetime.now(timezone.utc) > stored_otp_data["expires_at"]:
        database.delete_otp(email)
        return False

    return input_otp == stored_otp_data["otp"]