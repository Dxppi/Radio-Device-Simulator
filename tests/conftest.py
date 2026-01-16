import pytest
from app import application

@pytest.fixture
def client():
    application.config["TESTING"] = True
    with application.test_client() as client:
        yield client
