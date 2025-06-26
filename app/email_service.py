from pydantic import EmailStr


def send_otp_email(email: EmailStr, otp: str):
    print("!-----------------------!")
    print("-------------------------")
    print(f"For email: {email} - Your OTP is: {otp}")
    print("-------------------------")
    print("!-----------------------!")
