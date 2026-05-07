import random
import pytest

pytestmark = pytest.mark.api

PET_ID = random.randint(1_000_000, 9_999_999)

PET_PAYLOAD = {
    "id": PET_ID,
    "name": "Rex",
    "status": "available",
    "category": {"id": 1, "name": "Dogs"},
    "photoUrls": ["https://example.com/rex.jpg"],
    "tags": [{"id": 1, "name": "playful"}],
}


@pytest.fixture(scope="module", autouse=True)
def cleanup(client):
    yield
    client.delete(f"/pet/{PET_ID}")


class TestPet:
    def test_create_pet(self, client):
        response = client.post("/pet", json=PET_PAYLOAD)

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == PET_ID
        assert data["name"] == "Rex"
        assert data["status"] == "available"

    def test_get_pet_by_id(self, client):
        response = client.get(f"/pet/{PET_ID}")

        assert response.status_code == 200
        assert response.json()["id"] == PET_ID

    def test_update_pet(self, client):
        updated = {**PET_PAYLOAD, "name": "Rex Updated", "status": "sold"}
        response = client.put("/pet", json=updated)

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Rex Updated"
        assert data["status"] == "sold"

    def test_find_pets_by_status(self, client):
        response = client.get("/pet/findByStatus", params={"status": "available"})

        assert response.status_code == 200
        pets = response.json()
        assert isinstance(pets, list)
        assert all(p["status"] == "available" for p in pets)

    def test_delete_pet(self, client):
        response = client.delete(f"/pet/{PET_ID}")

        assert response.status_code == 200

        get_response = client.get(f"/pet/{PET_ID}")
        assert get_response.status_code == 404
