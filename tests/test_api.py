from fastapi.testclient import TestClient
from app.main import app
from app import database

test_client = TestClient(app)

def clean_in_memory_db():
    database.IN_MEMORY_USERS_DB.clear()
    database.IN_MEMORY_OTP_DB.clear()

def test_register_user_success():
    clean_in_memory_db()
    response = test_client.post(
        "/register",
        json={
            "email": "test@example.com",
            "password": "strongpassword",
        },
    )

    data = response.json()

    assert response.status_code == 201
    assert data["email"] == "test@example.com"


def test_register_user_duplicate_email():
    clean_in_memory_db()
    # First registration should succeed
    test_client.post(
        "/register",
        json={
            "email": "test@example.com",
            "password": "strongpassword",
        },
    )
    # Second registration with the same email should fail
    response = test_client.post(
        "/register",
        json={
            "email": "test@example.com",
            "password": "anotherpassword",
        },
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Email already registered"}


def test_login_success():
    clean_in_memory_db()
    # Register user first
    test_register_user_success()

    response = test_client.post(
        "/login",
        json={"email": "test@example.com", "password": "strongpassword"},
    )
    data = response.json()
    assert response.status_code == 200
    assert data["message"] == "Login successful"
    assert "access_token" in data["token"]


def test_login_wrong_password():
    clean_in_memory_db()
    test_register_user_success()

    response = test_client.post(
        "/login",
        json={"email": "test@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect email or password"}


def test_2fa_success():
    clean_in_memory_db()
    test_login_2fa_triggers_otp()

    stored_otp = database.get_stored_otp("2fa-user@example.com")["otp"]

    response = test_client.post(
        "/2-factor-auth",
        json={"email": "2fa-user@example.com", "otp": stored_otp},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert "2fa-user@example.com" not in database.IN_MEMORY_OTP_DB


def test_login_2fa_triggers_otp():
    clean_in_memory_db()
    test_client.post(
        "/register",
        json={
            "email": "2fa-user@example.com",
            "password": "securepassword123",
            "enable_2fa": True,
        },
    )

    response = test_client.post(
        "/login",
        json={"email": "2fa-user@example.com", "password": "securepassword123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "2FA required. Please verify OTP"
    assert data["token"] is None
    assert "2fa-user@example.com" in database.IN_MEMORY_OTP_DB

def test_2fa_invalid_otp():
    clean_in_memory_db()
    test_login_2fa_triggers_otp()

    response = test_client.post(
        "/2-factor-auth",
        json={"email": "2fa-user@example.com", "otp": "000000"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid or expired OTP"}
    assert "2fa-user@example.com" in database.IN_MEMORY_OTP_DB