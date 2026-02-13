"""
Salesforce REST API client
"""

import logging
from typing import Dict, Any, Optional
from src.core.api_client import APIClient


logger = logging.getLogger(__name__)


class SalesforceAPIClient(APIClient):
    """Salesforce REST API client"""

    def __init__(self, instance_url: str, access_token: str):
        """
        Initialize Salesforce API client.

        Args:
            instance_url: Salesforce instance URL
            access_token: OAuth2 access token
        """
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

        base_url = f"{instance_url}/services/data/v57.0"
        super().__init__(base_url, headers)
        self.instance_url = instance_url

    async def create_record(self, object_type: str, data: Dict[str, Any]) -> str:
        """
        Create a record.

        Args:
            object_type: Object type (e.g., 'Account', 'Contact')
            data: Record data

        Returns:
            Record ID
        """
        response = await self.post(
            f"/sobjects/{object_type}",
            data=data
        )

        record_id = response["body"].get("id")
        logger.info(f"Record created: {record_id}")
        return record_id

    async def get_record(self, object_type: str, record_id: str) -> Dict[str, Any]:
        """
        Get a record.

        Args:
            object_type: Object type
            record_id: Record ID

        Returns:
            Record data
        """
        response = await self.get(
            f"/sobjects/{object_type}/{record_id}"
        )

        return response["body"]

    async def update_record(
        self,
        object_type: str,
        record_id: str,
        data: Dict[str, Any]
    ) -> None:
        """
        Update a record.

        Args:
            object_type: Object type
            record_id: Record ID
            data: Updated data
        """
        await self.patch(
            f"/sobjects/{object_type}/{record_id}",
            data=data
        )

        logger.info(f"Record updated: {record_id}")

    async def delete_record(self, object_type: str, record_id: str) -> None:
        """
        Delete a record.

        Args:
            object_type: Object type
            record_id: Record ID
        """
        await self.delete(f"/sobjects/{object_type}/{record_id}")
        logger.info(f"Record deleted: {record_id}")

    async def query(self, soql: str) -> Dict[str, Any]:
        """
        Execute SOQL query.

        Args:
            soql: SOQL query string

        Returns:
            Query results
        """
        response = await self.get(
            "/query",
            params={"q": soql}
        )

        return response["body"]

    async def get_metadata(self, object_type: str) -> Dict[str, Any]:
        """
        Get object metadata.

        Args:
            object_type: Object type

        Returns:
            Object metadata
        """
        response = await self.get(f"/sobjects/{object_type}/describe")
        return response["body"]
