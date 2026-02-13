"""
API client for API automation
"""

import logging
from typing import Any, Dict, Optional, Union
import aiohttp
import json


logger = logging.getLogger(__name__)


class APIClient:
    """Base API client for handling HTTP requests"""

    def __init__(self, base_url: str = "", headers: Optional[Dict[str, str]] = None):
        """
        Initialize API client.

        Args:
            base_url: Base URL for API
            headers: Default headers for all requests
        """
        self.base_url = base_url
        self.headers = headers or {}
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()

    async def _request(
        self,
        method: str,
        endpoint: str,
        **kwargs: Any
    ) -> aiohttp.ClientResponse:
        """
        Make HTTP request.

        Args:
            method: HTTP method
            endpoint: API endpoint
            **kwargs: Additional arguments for request

        Returns:
            Response object
        """
        if not self.session:
            self.session = aiohttp.ClientSession()

        url = f"{self.base_url}{endpoint}" if self.base_url else endpoint
        headers = {**self.headers, **kwargs.get("headers", {})}

        logger.info(f"{method} request to {url}")
        
        response = await self.session.request(method, url, headers=headers, **kwargs)
        return response

    async def get(
        self,
        endpoint: str,
        headers: Optional[Dict[str, str]] = None,
        **kwargs: Any
    ) -> Dict[str, Any]:
        """
        Make GET request.

        Args:
            endpoint: API endpoint
            headers: Request headers
            **kwargs: Additional request arguments

        Returns:
            Response JSON
        """
        response = await self._request("GET", endpoint, headers=headers, **kwargs)
        return await self._handle_response(response)

    async def post(
        self,
        endpoint: str,
        data: Optional[Union[Dict, str]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs: Any
    ) -> Dict[str, Any]:
        """
        Make POST request.

        Args:
            endpoint: API endpoint
            data: Request body
            headers: Request headers
            **kwargs: Additional request arguments

        Returns:
            Response JSON
        """
        if isinstance(data, dict):
            kwargs["json"] = data
        else:
            kwargs["data"] = data

        response = await self._request("POST", endpoint, headers=headers, **kwargs)
        return await self._handle_response(response)

    async def put(
        self,
        endpoint: str,
        data: Optional[Union[Dict, str]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs: Any
    ) -> Dict[str, Any]:
        """
        Make PUT request.

        Args:
            endpoint: API endpoint
            data: Request body
            headers: Request headers
            **kwargs: Additional request arguments

        Returns:
            Response JSON
        """
        if isinstance(data, dict):
            kwargs["json"] = data
        else:
            kwargs["data"] = data

        response = await self._request("PUT", endpoint, headers=headers, **kwargs)
        return await self._handle_response(response)

    async def patch(
        self,
        endpoint: str,
        data: Optional[Union[Dict, str]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs: Any
    ) -> Dict[str, Any]:
        """
        Make PATCH request.

        Args:
            endpoint: API endpoint
            data: Request body
            headers: Request headers
            **kwargs: Additional request arguments

        Returns:
            Response JSON
        """
        if isinstance(data, dict):
            kwargs["json"] = data
        else:
            kwargs["data"] = data

        response = await self._request("PATCH", endpoint, headers=headers, **kwargs)
        return await self._handle_response(response)

    async def delete(
        self,
        endpoint: str,
        headers: Optional[Dict[str, str]] = None,
        **kwargs: Any
    ) -> Dict[str, Any]:
        """
        Make DELETE request.

        Args:
            endpoint: API endpoint
            headers: Request headers
            **kwargs: Additional request arguments

        Returns:
            Response JSON
        """
        response = await self._request("DELETE", endpoint, headers=headers, **kwargs)
        return await self._handle_response(response)

    async def _handle_response(self, response: aiohttp.ClientResponse) -> Dict[str, Any]:
        """
        Handle response.

        Args:
            response: Response object

        Returns:
            Parsed response
        """
        try:
            data = await response.json()
        except (json.JSONDecodeError, ValueError):
            data = await response.text()

        logger.info(f"Response status: {response.status}")

        if response.status >= 400:
            logger.error(f"Error response: {data}")

        return {
            "status": response.status,
            "body": data,
            "headers": dict(response.headers)
        }

    def set_auth_header(self, token: str, auth_type: str = "Bearer") -> None:
        """
        Set authorization header.

        Args:
            token: Auth token
            auth_type: Authorization type (Bearer, Basic, etc.)
        """
        self.headers["Authorization"] = f"{auth_type} {token}"
