import pytest
from api.utils.api_client import PetstoreClient


@pytest.fixture(scope="session")
def client():
    return PetstoreClient()
