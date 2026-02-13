"""
Configuration management for the framework
"""

import os
import logging
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv
import yaml


logger = logging.getLogger(__name__)


class Config:
    """Configuration management class"""

    def __init__(self, env_file: Optional[str] = None):
        """
        Initialize configuration.

        Args:
            env_file: Path to .env file
        """
        if env_file and os.path.exists(env_file):
            load_dotenv(env_file)
        else:
            load_dotenv()

        self._load_config()

    def _load_config(self):
        """Load configuration from environment variables"""
        # Browser Configuration
        self.browser_type = os.getenv("BROWSER_TYPE", "chromium")
        self.headless = os.getenv("HEADLESS", "true").lower() == "true"
        self.base_url = os.getenv("BASE_URL", "http://localhost:3000")

        # API Configuration
        self.api_base_url = os.getenv("API_BASE_URL", "http://localhost:8000")
        self.api_timeout = int(os.getenv("API_TIMEOUT", "30"))

        # Salesforce Configuration
        self.salesforce_instance = os.getenv("SALESFORCE_INSTANCE", "https://login.salesforce.com")
        self.salesforce_client_id = os.getenv("SALESFORCE_CLIENT_ID", "")
        self.salesforce_client_secret = os.getenv("SALESFORCE_CLIENT_SECRET", "")
        self.salesforce_username = os.getenv("SALESFORCE_USERNAME", "")
        self.salesforce_password = os.getenv("SALESFORCE_PASSWORD", "")

        # Test Configuration
        self.test_timeout = int(os.getenv("TEST_TIMEOUT", "30000"))
        self.screenshot_on_failure = os.getenv("SCREENSHOT_ON_FAILURE", "true").lower() == "true"
        self.report_dir = os.getenv("REPORT_DIR", "./reports")

        # Playwright Configuration
        self.playwright_slow_mo = int(os.getenv("PLAYWRIGHT_SLOW_MO", "0"))
        self.playwright_viewport_width = int(os.getenv("PLAYWRIGHT_VIEWPORT_WIDTH", "1280"))
        self.playwright_viewport_height = int(os.getenv("PLAYWRIGHT_VIEWPORT_HEIGHT", "720"))

        logger.info("Configuration loaded")

    @staticmethod
    def load_yaml_config(file_path: str) -> dict:
        """
        Load YAML configuration file.

        Args:
            file_path: Path to YAML file

        Returns:
            Configuration dictionary
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Configuration file not found: {file_path}")

        with open(file_path, 'r') as f:
            return yaml.safe_load(f) or {}
