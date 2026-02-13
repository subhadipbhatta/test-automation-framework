"""
Data generators and test data utilities
"""

import random
import string
from datetime import datetime, timedelta
from typing import Dict, Any


class DataGenerator:
    """Utility class for generating test data"""

    @staticmethod
    def generate_string(length: int = 10, prefix: str = "") -> str:
        """
        Generate random string.

        Args:
            length: Length of string
            prefix: Prefix for string

        Returns:
            Random string
        """
        random_part = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        return f"{prefix}{random_part}"

    @staticmethod
    def generate_email(domain: str = "test.com") -> str:
        """
        Generate random email.

        Args:
            domain: Email domain

        Returns:
            Random email
        """
        username = DataGenerator.generate_string(10)
        return f"{username}@{domain}"

    @staticmethod
    def generate_phone_number(country_code: str = "+1") -> str:
        """
        Generate random phone number.

        Args:
            country_code: Country code

        Returns:
            Random phone number
        """
        number = ''.join(random.choices(string.digits, k=10))
        return f"{country_code}{number}"

    @staticmethod
    def generate_username(prefix: str = "user_") -> str:
        """
        Generate random username.

        Args:
            prefix: Username prefix

        Returns:
            Random username
        """
        return DataGenerator.generate_string(8, prefix)

    @staticmethod
    def generate_password(length: int = 12) -> str:
        """
        Generate random password.

        Args:
            length: Password length

        Returns:
            Random password
        """
        characters = string.ascii_letters + string.digits + "!@#$%^&*"
        return ''.join(random.choices(characters, k=length))

    @staticmethod
    def generate_date(days_offset: int = 0, format_str: str = "%Y-%m-%d") -> str:
        """
        Generate date string.

        Args:
            days_offset: Days offset from today
            format_str: Date format string

        Returns:
            Formatted date string
        """
        target_date = datetime.now() + timedelta(days=days_offset)
        return target_date.strftime(format_str)

    @staticmethod
    def generate_user_data() -> Dict[str, Any]:
        """
        Generate complete user data.

        Returns:
            User data dictionary
        """
        return {
            "first_name": DataGenerator.generate_string(6),
            "last_name": DataGenerator.generate_string(6),
            "email": DataGenerator.generate_email(),
            "username": DataGenerator.generate_username(),
            "password": DataGenerator.generate_password(),
            "phone": DataGenerator.generate_phone_number(),
        }
