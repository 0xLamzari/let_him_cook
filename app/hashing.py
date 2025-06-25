#TODO:
# explain why I chose argon2:
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

hasher = PasswordHasher()

def hash_password(input_password: str) -> str:
    hashed_password = hasher.hash(input_password)
    # TODO: to be deleted
    print(hashed_password)
    return hashed_password

def verify_password(input_password: str, hashed_password: str) -> bool | None:
    try:
        hasher.verify(hashed_password, input_password)
        return True
    except VerifyMismatchError:
        return False
    except Exception as e:
        print(f"Unexpected error during psw verification: {e}")