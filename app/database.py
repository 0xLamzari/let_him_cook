from typing import Dict, Optional
from . import dtos, hashing

# key: email, value: UserInDB
IN_MEMORY_USERS_DB: Dict[str, dtos.UserInDB] = {}

def get_user_by_email(email: str) -> Optional[dtos.UserInDB]:
    return IN_MEMORY_USERS_DB.get(email)


def create_user(user: dtos.UserRequest) -> dtos.UserInDB:
    hashed_password = hashing.hash_password(user.password)

    user_in_db = dtos.UserInDB(
        email=user.email,
        hashed_password=hashed_password,
    )

    IN_MEMORY_USERS_DB[user.email] = user_in_db
    return user_in_db