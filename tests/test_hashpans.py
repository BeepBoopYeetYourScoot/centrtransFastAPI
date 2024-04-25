from unittest.mock import patch

from fastapi.testclient import TestClient

from api.routers.hashpans import HASHPAN_PREFIX, hashpan_router
from api.utils import templates

client = TestClient(hashpan_router)


@patch("api.utils.templates.TemplateResponse")
def test_read_main_page(template="main.html"):
    response = client.get(HASHPAN_PREFIX)
    assert response.status_code == 200
    # assert mock_template_response.status_code == 200
