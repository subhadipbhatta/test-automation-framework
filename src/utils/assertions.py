"""
Assertion utilities for tests
"""

import logging
from typing import Any, List, Dict


logger = logging.getLogger(__name__)


class Assertions:
    """Common assertion utilities"""

    @staticmethod
    def assert_equal(actual: Any, expected: Any, message: str = "") -> bool:
        """
        Assert equal.

        Args:
            actual: Actual value
            expected: Expected value
            message: Custom message

        Returns:
            True if assertion passes

        Raises:
            AssertionError: If assertion fails
        """
        assert actual == expected, \
            message or f"Expected {expected}, got {actual}"
        return True

    @staticmethod
    def assert_not_equal(actual: Any, expected: Any, message: str = "") -> bool:
        """
        Assert not equal.

        Args:
            actual: Actual value
            expected: Expected value
            message: Custom message

        Returns:
            True if assertion passes
        """
        assert actual != expected, \
            message or f"Values should not be equal: {actual}"
        return True

    @staticmethod
    def assert_in(value: Any, container: Any, message: str = "") -> bool:
        """
        Assert value in container.

        Args:
            value: Value to check
            container: Container to search
            message: Custom message

        Returns:
            True if assertion passes
        """
        assert value in container, \
            message or f"{value} not found in {container}"
        return True

    @staticmethod
    def assert_not_none(value: Any, message: str = "") -> bool:
        """
        Assert not none.

        Args:
            value: Value to check
            message: Custom message

        Returns:
            True if assertion passes
        """
        assert value is not None, \
            message or "Value should not be None"
        return True

    @staticmethod
    def assert_true(condition: bool, message: str = "") -> bool:
        """
        Assert true.

        Args:
            condition: Condition to check
            message: Custom message

        Returns:
            True if assertion passes
        """
        assert condition, message or "Condition should be True"
        return True

    @staticmethod
    def assert_false(condition: bool, message: str = "") -> bool:
        """
        Assert false.

        Args:
            condition: Condition to check
            message: Custom message

        Returns:
            True if assertion passes
        """
        assert not condition, message or "Condition should be False"
        return True

    @staticmethod
    def assert_greater_than(actual: Any, expected: Any, message: str = "") -> bool:
        """
        Assert greater than.

        Args:
            actual: Actual value
            expected: Expected value
            message: Custom message

        Returns:
            True if assertion passes
        """
        assert actual > expected, \
            message or f"{actual} should be greater than {expected}"
        return True

    @staticmethod
    def assert_less_than(actual: Any, expected: Any, message: str = "") -> bool:
        """
        Assert less than.

        Args:
            actual: Actual value
            expected: Expected value
            message: Custom message

        Returns:
            True if assertion passes
        """
        assert actual < expected, \
            message or f"{actual} should be less than {expected}"
        return True
