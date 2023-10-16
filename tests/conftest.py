import pytest

from main import bootstrap


@pytest.fixture(scope="session", autouse=True)
def app_bootstrap():
    bootstrap()
