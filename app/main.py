import uvicorn
from fastapi import FastAPI, HTTPException, status, Depends
from typing import Dict, Any
from fastapi.security import OAuth2PasswordRequestForm

from app import dtos, database, hashing

app = FastAPI(title='Let Him Cook')

@app.get("/")
def read_root():
    return {"Hello": "World"}


# TODO: add documentation for endpoint (parameters, etc.)
@app.post("/register", response_model=dtos.UserInDB, status_code=status.HTTP_201_CREATED)
def register_user(user: dtos.UserRequest) -> dtos.UserInDB:

    db_user = database.get_user_by_email(email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    stored_user = database.create_user(user=user)
    return stored_user


@app.post("/login", response_model=dtos.LoginResponse)
def login_user(user: dtos.UserRequest) -> dtos.LoginResponse:
    user = authenticate_user(user.email, user.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    return dtos.LoginResponse(message="Successful login")


def authenticate_user(email: str, password: str) -> dtos.UserInDB | None:
    user = database.get_user_by_email(email)
    if not user:
        return None
    if not hashing.verify_password(password, user.hashed_password):
        return None
    return user


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)