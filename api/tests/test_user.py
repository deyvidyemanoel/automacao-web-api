import random
import pytest

pytestmark = pytest.mark.api

SUFFIX = random.randint(1000, 9999)
USERNAME = f"testuser_{SUFFIX}"

USER_PAYLOAD = {
    "id": SUFFIX,
    "username": USERNAME,
    "firstName": "Test",
    "lastName": "User",
    "email": f"{USERNAME}@example.com",
    "password": "password123",
    "phone": "11999999999",
    "userStatus": 1,
}


@pytest.fixture(scope="module", autouse=True)
def cleanup(client):
    yield
    client.delete(f"/user/{USERNAME}")


class TestUser:
    def test_create_user(self, client):
        response = client.post("/user", json=USER_PAYLOAD)

        assert response.status_code == 200

    def test_login_user(self, client):
        response = client.get(
            "/user/login",
            params={"username": USERNAME, "password": "password123"},
        )

        assert response.status_code == 200
        assert "logged in" in response.json().get("message", "").lower()

    def test_get_user_by_username(self, client):
        response = client.get(f"/user/{USERNAME}")

        assert response.status_code == 200
        data = response.json()
        assert data["username"] == USERNAME
        assert data["email"] == USER_PAYLOAD["email"]

    def test_update_user(self, client):
        updated = {**USER_PAYLOAD, "firstName": "Updated", "lastName": "Name"}
        response = client.put(f"/user/{USERNAME}", json=updated)

        assert response.status_code == 200

        get_response = client.get(f"/user/{USERNAME}")
        assert get_response.json()["firstName"] == "Updated"

    def test_delete_user(self, client):
        response = client.delete(f"/user/{USERNAME}")

        assert response.status_code == 200

        get_response = client.get(f"/user/{USERNAME}")
        assert get_response.status_code == 404
