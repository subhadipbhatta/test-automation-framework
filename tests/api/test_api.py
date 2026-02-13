"""
API automation tests
"""

import pytest
from src.core.api_client import APIClient
from src.api.test_base import APITestBase
from src.utils.config import Config


@pytest.mark.api
@pytest.mark.asyncio
class TestAPI:
    """API tests"""

    @pytest.fixture
    async def api_client(self, config):
        """Create API client"""
        async with APIClient(config.api_base_url) as client:
            yield client

    async def test_get_request(self, api_client):
        """Test GET request"""
        response = await api_client.get("/health")
        assert response["status"] == 200

    async def test_post_request(self, api_client):
        """Test POST request"""
        data = {
            "username": "test_user",
            "email": "test@example.com"
        }
        response = await api_client.post("/users", data=data)
        assert response["status"] in [200, 201]

    async def test_put_request(self, api_client):
        """Test PUT request"""
        data = {
            "username": "updated_user"
        }
        response = await api_client.put("/users/1", data=data)
        assert response["status"] in [200, 204]

    async def test_delete_request(self, api_client):
        """Test DELETE request"""
        response = await api_client.delete("/users/1")
        assert response["status"] in [200, 204]

    async def test_set_auth_header(self, api_client):
        """Test setting authorization header"""
        api_client.set_auth_header("test_token")
        assert "Authorization" in api_client.headers
        assert api_client.headers["Authorization"] == "Bearer test_token"

    async def test_custom_auth_type(self, api_client):
        """Test custom authorization type"""
        api_client.set_auth_header("test_token", auth_type="Basic")
        assert api_client.headers["Authorization"] == "Basic test_token"


@pytest.mark.api
@pytest.mark.asyncio
class TestAPIAssertions:
    """API assertion tests"""

    @pytest.fixture
    async def api_test_base(self):
        """Create API test base"""
        async with APIClient("http://localhost:8000") as client:
            yield APITestBase(client)

    async def test_assert_status_code(self, api_test_base):
        """Test status code assertion"""
        response = {"status": 200, "body": {}}
        await api_test_base.assert_status_code(response, 200)

    async def test_assert_response_contains(self, api_test_base):
        """Test response contains assertion"""
        response = {"status": 200, "body": {"id": 1, "name": "test"}}
        await api_test_base.assert_response_contains(response, "id", 1)

    async def test_assert_response_structure(self, api_test_base):
        """Test response structure assertion"""
        response = {"status": 200, "body": {"id": 1, "name": "test"}}
        await api_test_base.assert_response_structure(response, ["id", "name"])

    async def test_assert_response_is_list(self, api_test_base):
        """Test response is list assertion"""
        response = {"status": 200, "body": [{"id": 1}, {"id": 2}]}
        await api_test_base.assert_response_is_list(response, min_length=2)
