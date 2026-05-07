import random
import pytest

pytestmark = pytest.mark.api

ORDER_ID = random.randint(1, 10)
PET_ID = random.randint(1_000_000, 9_999_999)

ORDER_PAYLOAD = {
    "id": ORDER_ID,
    "petId": PET_ID,
    "quantity": 1,
    "status": "placed",
    "complete": False,
}


@pytest.fixture(scope="module", autouse=True)
def cleanup(client):
    yield
    client.delete(f"/store/order/{ORDER_ID}")


class TestStore:
    def test_get_inventory(self, client):
        response = client.get("/store/inventory")

        assert response.status_code == 200
        assert isinstance(response.json(), dict)

    def test_place_order(self, client):
        response = client.post("/store/order", json=ORDER_PAYLOAD)

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == ORDER_ID
        assert data["status"] == "placed"

    def test_get_order_by_id(self, client):
        response = client.get(f"/store/order/{ORDER_ID}")

        assert response.status_code == 200
        assert response.json()["id"] == ORDER_ID

    def test_delete_order(self, client):
        response = client.delete(f"/store/order/{ORDER_ID}")

        assert response.status_code == 200

        get_response = client.get(f"/store/order/{ORDER_ID}")
        assert get_response.status_code == 404
