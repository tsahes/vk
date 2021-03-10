import pytest

from main import setup_app


@pytest.fixture()
def app():
    return setup_app()

@pytest.fixture()
async def cli(aiohttp_client, app):
    client = await aiohttp_client(app)
    yield client