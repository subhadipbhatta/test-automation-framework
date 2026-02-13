"""
Wait utilities for test automation
"""

import logging
import asyncio
from typing import Callable, Any, TypeVar, Coroutine
import time


logger = logging.getLogger(__name__)

T = TypeVar('T')


class WaitUtils:
    """Utility class for wait operations"""

    @staticmethod
    async def wait_until(
        condition: Callable[..., Coroutine[Any, Any, bool]],
        timeout: int = 10,
        poll_interval: float = 0.5,
        message: str = "Condition not met"
    ) -> bool:
        """
        Wait until a condition is met.

        Args:
            condition: Async callable that returns boolean
            timeout: Timeout in seconds
            poll_interval: Polling interval in seconds
            message: Error message

        Returns:
            True if condition is met

        Raises:
            TimeoutError: If condition is not met within timeout
        """
        start_time = time.time()
        last_error = None

        while time.time() - start_time < timeout:
            try:
                if await condition():
                    return True
            except Exception as e:
                last_error = e

            await asyncio.sleep(poll_interval)

        error_msg = f"{message} (timeout: {timeout}s)"
        if last_error:
            error_msg += f": {str(last_error)}"

        logger.error(error_msg)
        raise TimeoutError(error_msg)

    @staticmethod
    async def wait_for_element_state(
        element_locator: Callable[..., Coroutine[Any, Any, Any]],
        state: str,
        timeout: int = 10
    ) -> bool:
        """
        Wait for element to reach a specific state.

        Args:
            element_locator: Async callable that returns element
            state: State to wait for (visible, hidden, stable, etc.)
            timeout: Timeout in seconds

        Returns:
            True if element reached state

        Raises:
            TimeoutError: If timeout exceeded
        """
        async def check_state():
            element = await element_locator()
            if state == "visible":
                return await element.is_visible()
            elif state == "hidden":
                return not await element.is_visible()
            elif state == "enabled":
                return await element.is_enabled()
            elif state == "disabled":
                return not await element.is_enabled()
            return False

        return await WaitUtils.wait_until(
            check_state,
            timeout=timeout,
            message=f"Element did not reach state: {state}"
        )

    @staticmethod
    async def wait_for_text(
        element_locator: Callable[..., Coroutine[Any, Any, Any]],
        text: str,
        timeout: int = 10,
        partial: bool = False
    ) -> bool:
        """
        Wait for element to contain specific text.

        Args:
            element_locator: Async callable that returns element
            text: Text to wait for
            timeout: Timeout in seconds
            partial: If True, checks if text is contained

        Returns:
            True if text is found

        Raises:
            TimeoutError: If timeout exceeded
        """
        async def check_text():
            element = await element_locator()
            element_text = await element.text_content()
            if partial:
                return text in (element_text or "")
            else:
                return element_text == text

        return await WaitUtils.wait_until(
            check_text,
            timeout=timeout,
            message=f"Text '{text}' not found"
        )
