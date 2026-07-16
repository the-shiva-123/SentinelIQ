import pytest
from fastapi.testclient import TestClient

from copilot.api import app


@pytest.mark.parametrize("origin", ["http://localhost:3000", "http://localhost:5173"])
def test_api_allows_frontend_origin_for_preflight(origin):
    client = TestClient(app)
    response = client.options(
        "/api/v1/query",
        headers={
            "Origin": origin,
            "Access-Control-Request-Method": "POST",
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == origin
