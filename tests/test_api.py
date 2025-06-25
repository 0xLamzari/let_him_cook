from fastapi.testclient import TestClient
from app.main import app
from app import database

test_client = TestClient(app)

def clean_in_memory_db():
    database.IN_MEMORY_USERS_DB.clear()

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