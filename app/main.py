from app import dtos, database, auth, email_service
from fastapi import FastAPI, HTTPException, status
from typing import Dict, Any
import uvicorn

app = FastAPI(title='Let Him Cook')

@app.post("/register", response_model=dtos.UserInDB, status_code=status.HTTP_201_CREATED)
def register_user(user: dtos.RegistrationRequest) -> dtos.UserInDB:
    """
    Register a new user in the system.

    - **email**: The user's email address. Must be unique
    - **password**: The user's password. Will be securely hashed
    - **profile_data**: The user's name and surname
    - **enable_2fa**: A boolean to enable Two-Factor Authentication
    """

    db_user = database.get_user_by_email(email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    return database.create_user(user=user)


@app.post("/login", response_model=dtos.LoginResponse)
def login_user(req: dtos.LoginRequest) -> Dict[str, Any]:
    """
    Authenticate a user and return a JWT or a 2FA prompt if necessary

    - **email**: The user's email address
    - **password**: The user's password
    """
    user = auth.authenticate_user(req.email, req.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    if user.enable_2fa:
        otp = auth.generate_and_store_otp(user.email)
        email_service.send_otp_email(email=user.email, otp=otp)

        return {"message": "2FA required. Please verify OTP", "token": None}

    else:
        access_token = auth.create_access_token(data={"sub": user.email})
        return {"message": "Login successful", "token": dtos.Token(access_token=access_token, token_type="bearer")}

@app.post("/2-factor-auth", response_model=dtos.Token)
def verify_two_factor_auth(req: dtos.OTPRequest) -> Dict[str, Any]:
    """
    Verify the One-Time Password (OTP) for a 2FA-enabled login

    - **email**: The user's email
    - **otp**: The 6-digit code sent to the user's email
    """

    if not auth.verify_otp(email=req.email, input_otp=req.otp):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired OTP",
        )

    access_token = auth.create_access_token(data={"sub": req.email})

    database.delete_otp(email=req.email)

    return {"access_token": access_token, "token_type": "bearer"}


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)