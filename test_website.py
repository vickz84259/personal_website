import pytest
from website import app

@pytest.fixture(scope="module")
def initialize():
    app.testing = True
    return app.test_client()

def test_main_page(initialize):
    response = initialize.get('/')
    assert response.status_code == 200
