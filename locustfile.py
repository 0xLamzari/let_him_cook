import time
from locust import HttpUser, task, between

user_counter = 0


class AuthUser(HttpUser):
    wait_time = between(1, 2)

    def on_start(self):
        global user_counter
        user_counter += 1

        timestamp = int(time.time())
        self.email = f"loadtest_{timestamp}_{user_counter}@example.com"
        self.password = "aVeryStrongLoadTestPassword123"
        self.name = "name"
        self.surname = "surname"

    @task(1)
    def register_and_login_no_2fa(self):
        """
        1. Register a new account without 2FA.
        2. Immediately log in to that new account.
        """
        with self.client.post(
                "/register",
                json={
                    "email": self.email,
                    "password": self.password,
                    "profile_data": {"name": self.name, "surname": self.surname},
                    "enable_2fa": False,
                },
                name="/register (no-2fa)",
                catch_response=True
        ) as response:
            if response.status_code != 201:
                response.failure(f"Failed to register user. Status: {response.status_code}, Text: {response.text}")
                return  # Stop if registration fails

        with self.client.post(
                "/login",
                json={"email": self.email, "password": self.password},
                name="/login (no-2fa)",
                catch_response=True
        ) as response:
            if response.status_code != 200:
                response.failure(f"Failed to log in. Status: {response.status_code}, Text: {response.text}")
                return

            try:
                json_response = response.json()
                if "token" not in json_response or json_response.get("token") is None:
                    response.failure(f"Login successful but no token received. Response: {json_response}")
            except Exception as e:
                response.failure(f"Could not parse login response JSON. Error: {e}")