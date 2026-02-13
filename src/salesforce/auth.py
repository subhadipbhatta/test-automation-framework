"""
Salesforce OAuth2 authentication handler
"""

import logging
import aiohttp
import json
from typing import Dict, Any, Optional
import urllib.parse


logger = logging.getLogger(__name__)


class SalesforceAuth:
    """Handle Salesforce OAuth2 authentication"""

    def __init__(
        self,
        instance: str,
        client_id: str,
        client_secret: str,
        username: str,
        password: str
    ):
        """
        Initialize Salesforce authentication.

        Args:
            instance: Salesforce instance URL
            client_id: OAuth2 client ID
            client_secret: OAuth2 client secret
            username: Salesforce username
            password: Salesforce password
        """
        self.instance = instance
        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        self.password = password
        self.access_token: Optional[str] = None
        self.instance_url: Optional[str] = None

    async def authenticate(self) -> str:
        """
        Authenticate with Salesforce using OAuth2.

        Returns:
            Access token

        Raises:
            Exception: If authentication fails
        """
        auth_url = f"{self.instance}/services/oauth2/token"

        data = {
            "grant_type": "password",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "username": self.username,
            "password": self.password,
        }

        logger.info(f"Authenticating with Salesforce: {auth_url}")

        async with aiohttp.ClientSession() as session:
            async with session.post(auth_url, data=data) as response:
                if response.status != 200:
                    error_text = await response.text()
                    logger.error(f"Authentication failed: {error_text}")
                    raise Exception(f"Authentication failed: {error_text}")

                result = await response.json()
                self.access_token = result["access_token"]
                self.instance_url = result["instance_url"]

                logger.info(f"Authentication successful. Instance: {self.instance_url}")

        return self.access_token

    def get_auth_header(self) -> Dict[str, str]:
        """
        Get authorization header.

        Returns:
            Authorization header
        """
        if not self.access_token:
            raise RuntimeError("Not authenticated. Call authenticate() first.")

        return {"Authorization": f"Bearer {self.access_token}"}
