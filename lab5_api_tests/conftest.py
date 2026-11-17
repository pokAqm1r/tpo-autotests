import pytest
import requests

BASE_URL = "https://jsonplaceholder.typicode.com"


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.fixture(scope="session")
def api():
    """Одна HTTP-сессия на все тесты: общие заголовки и keep-alive."""
    session = requests.Session()
    session.headers.update({"Content-Type": "application/json; charset=UTF-8"})
    yield session
    session.close()
