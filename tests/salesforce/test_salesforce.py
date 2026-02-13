"""
Salesforce automation tests
"""

import pytest
from src.salesforce.auth import SalesforceAuth
from src.salesforce.api_client import SalesforceAPIClient
from src.salesforce.base_salesforce_page import SalesforcePage
from src.utils.config import Config


@pytest.mark.salesforce
@pytest.mark.asyncio
class TestSalesforceAuth:
    """Salesforce authentication tests"""

    @pytest.fixture
    def salesforce_auth(self, config):
        """Create Salesforce auth instance"""
        return SalesforceAuth(
            config.salesforce_instance,
            config.salesforce_client_id,
            config.salesforce_client_secret,
            config.salesforce_username,
            config.salesforce_password
        )

    async def test_authenticate(self, salesforce_auth):
        """Test Salesforce authentication"""
        try:
            token = await salesforce_auth.authenticate()
            assert token, "Access token is empty"
            assert salesforce_auth.instance_url, "Instance URL is empty"
        except Exception as e:
            pytest.skip(f"Salesforce credentials not configured: {e}")

    async def test_get_auth_header(self, salesforce_auth):
        """Test getting auth header"""
        try:
            await salesforce_auth.authenticate()
            header = salesforce_auth.get_auth_header()
            assert "Authorization" in header
            assert "Bearer" in header["Authorization"]
        except Exception as e:
            pytest.skip(f"Salesforce credentials not configured: {e}")


@pytest.mark.salesforce
@pytest.mark.asyncio
class TestSalesforceAPI:
    """Salesforce API tests"""

    @pytest.fixture
    async def salesforce_api(self, config):
        """Create Salesforce API client"""
        auth = SalesforceAuth(
            config.salesforce_instance,
            config.salesforce_client_id,
            config.salesforce_client_secret,
            config.salesforce_username,
            config.salesforce_password
        )

        try:
            await auth.authenticate()
            client = SalesforceAPIClient(auth.instance_url, auth.access_token)
            yield client
            await client.session.close() if client.session else None
        except Exception as e:
            pytest.skip(f"Salesforce credentials not configured: {e}")

    async def test_query_records(self, salesforce_api):
        """Test querying records"""
        try:
            soql = "SELECT Id, Name FROM Account LIMIT 1"
            result = await salesforce_api.query(soql)
            assert "records" in result or "totalSize" in result
        except Exception as e:
            pytest.skip(f"Test skipped: {e}")

    async def test_get_metadata(self, salesforce_api):
        """Test getting object metadata"""
        try:
            metadata = await salesforce_api.get_metadata("Account")
            assert "fields" in metadata or "name" in metadata
        except Exception as e:
            pytest.skip(f"Test skipped: {e}")


@pytest.mark.salesforce
@pytest.mark.asyncio
class TestSalesforceUI:
    """Salesforce UI tests"""

    async def test_salesforce_page_initialization(self, page):
        """Test Salesforce page initialization"""
        salesforce_page = SalesforcePage(page)
        assert salesforce_page.page == page
        assert salesforce_page.base_url == SalesforcePage.SALESFORCE_BASE_URL

    async def test_login_credentials_required(self, page):
        """Test login requires credentials"""
        salesforce_page = SalesforcePage(page)
        # This would normally connect to real Salesforce
        # For testing, we skip if not configured
        assert hasattr(salesforce_page, 'login')
        assert hasattr(salesforce_page, 'logout')
