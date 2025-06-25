from fastapi import FastAPI, HTTPException, status
from . import dtos, database

app = FastAPI(title='Let Him Cook')

@app.get("/")
def read_root():
    return {"Hello": "World"}


# TODO: add documentation for endpoint (parameters, etc.)
@app.post("/register", response_model=dtos.UserInDB, status_code=status.HTTP_201_CREATED)
def register_user(user: dtos.UserRegistrationRequest) -> dtos.UserInDB:

    db_user = database.get_user_by_email(email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    stored_user = database.create_user(user=user)
    return stored_user
