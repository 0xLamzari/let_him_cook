from datetime import timedelta, datetime, timezone
from typing import Dict

from pydantic import EmailStr

from . import dtos, hashing

# key: email, value: UserInDB
IN_MEMORY_USERS_DB: Dict[EmailStr, dtos.UserInDB] = {}

# key: email, value: dict[otp, expiration]
IN_MEMORY_OTP_DB: Dict[EmailStr, dict] = {}


def get_user_by_email(email: EmailStr) -> dtos.UserInDB | None:
    return IN_MEMORY_USERS_DB.get(email)


def create_user(user: dtos.RegistrationRequest) -> dtos.UserInDB:
    hashed_password = hashing.hash_password(user.password)

    user_in_db = dtos.UserInDB(
        email=user.email,
        hashed_password=hashed_password,
        enable_2fa=user.enable_2fa,
    )

    IN_MEMORY_USERS_DB[user.email] = user_in_db
    return user_in_db


def store_otp(email: EmailStr, otp: str, expires_delta: timedelta):
    expires_at = datetime.now(timezone.utc) + expires_delta
    IN_MEMORY_OTP_DB[email] = {"otp": otp, "expires_at": expires_at}


def get_stored_otp(email: EmailStr) -> Dict | None:
    return IN_MEMORY_OTP_DB.get(email)


def delete_otp(email: EmailStr):
    if email in IN_MEMORY_OTP_DB:
        del IN_MEMORY_OTP_DB[email]