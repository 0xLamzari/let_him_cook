from app import dtos, database, auth
from fastapi import FastAPI, HTTPException, status
from typing import Dict, Any
import uvicorn

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


# TODO: add documentation for endpoint (parameters, etc.)
@app.post("/login", response_model=dtos.LoginResponse)
def login_user(user: dtos.UserRequest) -> Dict[str, Any]:
    user = auth.authenticate_user(user.email, user.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    access_token = auth.create_access_token(data={"sub": user.email})
    return {"message": "Login successful", "token": dtos.Token(access_token=access_token, token_type="bearer")}


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)