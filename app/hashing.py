#TODO:
# explain why I chose argon2:
from argon2 import PasswordHasher

hasher = PasswordHasher()

def hash_password(input_password: str) -> str:
    hashed_password = hasher.hash(input_password)
    # TODO: to be deleted
    print(hashed_password)
    return hashed_password