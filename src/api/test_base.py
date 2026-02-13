"""
Base API test class with common assertions and utilities
"""

import logging
from typing import Any, Dict, Optional
from src.core.api_client import APIClient


logger = logging.getLogger(__name__)


class APITestBase:
    """Base class for API tests"""

    def __init__(self, api_client: APIClient):
        """
        Initialize API test base.

        Args:
            api_client: APIClient instance
        """
        self.api_client = api_client
        self.logger = logging.getLogger(self.__class__.__name__)

    async def assert_status_code(self, response: Dict[str, Any], expected_code: int) -> bool:
        """
        Assert response status code.

        Args:
            response: API response
            expected_code: Expected status code

        Returns:
            True if assertion passes

        Raises:
            AssertionError: If status code doesn't match
        """
        actual_code = response.get("status")
        assert actual_code == expected_code, \
            f"Expected status {expected_code}, got {actual_code}"
        return True

    async def assert_response_contains(
        self,
        response: Dict[str, Any],
        key: str,
        expected_value: Any = None
    ) -> bool:
        """
        Assert response contains key and optionally matches value.

        Args:
            response: API response
            key: Key to check
            expected_value: Optional expected value

        Returns:
            True if assertion passes

        Raises:
            AssertionError: If key not found or value doesn't match
        """
        body = response.get("body", {})
        assert key in body, f"Key '{key}' not found in response"

        if expected_value is not None:
            actual_value = body.get(key)
            assert actual_value == expected_value, \
                f"Expected {expected_value}, got {actual_value}"

        return True

    async def assert_response_structure(
        self,
        response: Dict[str, Any],
        expected_keys: list
    ) -> bool:
        """
        Assert response structure contains expected keys.

        Args:
            response: API response
            expected_keys: List of expected keys

        Returns:
            True if assertion passes

        Raises:
            AssertionError: If structure doesn't match
        """
        body = response.get("body", {})

        for key in expected_keys:
            assert key in body, f"Expected key '{key}' not found in response"

        return True

    async def assert_response_is_list(
        self,
        response: Dict[str, Any],
        min_length: Optional[int] = None
    ) -> bool:
        """
        Assert response body is a list.

        Args:
            response: API response
            min_length: Minimum expected list length

        Returns:
            True if assertion passes

        Raises:
            AssertionError: If body is not a list or length is too short
        """
        body = response.get("body")
        assert isinstance(body, list), "Response body is not a list"

        if min_length is not None:
            assert len(body) >= min_length, \
                f"Expected at least {min_length} items, got {len(body)}"

        return True

    async def assert_error_response(
        self,
        response: Dict[str, Any],
        expected_status: int,
        error_key: str = "error"
    ) -> bool:
        """
        Assert error response.

        Args:
            response: API response
            expected_status: Expected error status
            error_key: Key containing error message

        Returns:
            True if assertion passes

        Raises:
            AssertionError: If response doesn't contain error
        """
        await self.assert_status_code(response, expected_status)

        body = response.get("body", {})
        assert error_key in body or error_key in str(body), \
            f"Error key '{error_key}' not found in response"

        return True
