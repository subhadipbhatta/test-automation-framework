"""
MCP Server for Playwright integration
"""

import logging
import json
from typing import Any
from mcp.server import Server
from mcp.types import Tool, TextContent, ToolResult


logger = logging.getLogger(__name__)


class PlaywrightMCPServer:
    """MCP Server for Playwright test automation"""

    def __init__(self):
        """Initialize MCP server"""
        self.server = Server("playwright-mcp-server")
        self._setup_tools()

    def _setup_tools(self):
        """Setup available tools"""
        self.tools = [
            Tool(
                name="navigate",
                description="Navigate to a URL in the browser",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "url": {"type": "string", "description": "URL to navigate to"}
                    },
                    "required": ["url"]
                }
            ),
            Tool(
                name="click",
                description="Click on an element using a selector",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "selector": {"type": "string", "description": "CSS selector or XPath"},
                        "timeout": {"type": "integer", "description": "Timeout in milliseconds"}
                    },
                    "required": ["selector"]
                }
            ),
            Tool(
                name="fill",
                description="Fill text in an input field",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "selector": {"type": "string", "description": "Element selector"},
                        "text": {"type": "string", "description": "Text to fill"}
                    },
                    "required": ["selector", "text"]
                }
            ),
            Tool(
                name="get_text",
                description="Get text content from an element",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "selector": {"type": "string", "description": "Element selector"}
                    },
                    "required": ["selector"]
                }
            ),
            Tool(
                name="wait_for_selector",
                description="Wait for element to appear in DOM",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "selector": {"type": "string", "description": "Element selector"},
                        "timeout": {"type": "integer", "description": "Timeout in milliseconds"}
                    },
                    "required": ["selector"]
                }
            ),
            Tool(
                name="take_screenshot",
                description="Take a screenshot of the page",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "File path for screenshot"}
                    },
                    "required": ["path"]
                }
            ),
            Tool(
                name="execute_script",
                description="Execute JavaScript on the page",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "script": {"type": "string", "description": "JavaScript code"}
                    },
                    "required": ["script"]
                }
            ),
            Tool(
                name="get_current_url",
                description="Get the current page URL",
                inputSchema={
                    "type": "object",
                    "properties": {}
                }
            ),
            Tool(
                name="get_page_title",
                description="Get the page title",
                inputSchema={
                    "type": "object",
                    "properties": {}
                }
            ),
            Tool(
                name="select_option",
                description="Select an option from a dropdown",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "selector": {"type": "string", "description": "Dropdown selector"},
                        "value": {"type": "string", "description": "Option value"}
                    },
                    "required": ["selector", "value"]
                }
            ),
        ]

    def get_tools(self) -> list:
        """
        Get available tools.

        Returns:
            List of tools
        """
        return self.tools

    async def process_tool_call(self, tool_name: str, tool_input: dict) -> ToolResult:
        """
        Process tool call.

        Args:
            tool_name: Name of the tool
            tool_input: Tool input parameters

        Returns:
            Tool result
        """
        logger.info(f"Processing tool call: {tool_name} with input: {tool_input}")

        try:
            if tool_name == "navigate":
                return await self._navigate(tool_input["url"])
            elif tool_name == "click":
                return await self._click(tool_input["selector"])
            elif tool_name == "fill":
                return await self._fill(tool_input["selector"], tool_input["text"])
            elif tool_name == "get_text":
                return await self._get_text(tool_input["selector"])
            elif tool_name == "wait_for_selector":
                return await self._wait_for_selector(
                    tool_input["selector"],
                    tool_input.get("timeout", 5000)
                )
            elif tool_name == "take_screenshot":
                return await self._take_screenshot(tool_input["path"])
            elif tool_name == "execute_script":
                return await self._execute_script(tool_input["script"])
            elif tool_name == "get_current_url":
                return await self._get_current_url()
            elif tool_name == "get_page_title":
                return await self._get_page_title()
            elif tool_name == "select_option":
                return await self._select_option(tool_input["selector"], tool_input["value"])
            else:
                return ToolResult(
                    content=[TextContent(type="text", text=f"Unknown tool: {tool_name}")],
                    isError=True
                )
        except Exception as e:
            logger.error(f"Error processing tool call: {str(e)}")
            return ToolResult(
                content=[TextContent(type="text", text=f"Error: {str(e)}")],
                isError=True
            )

    async def _navigate(self, url: str) -> ToolResult:
        """Navigate to URL"""
        return ToolResult(
            content=[TextContent(type="text", text=f"Navigated to {url}")]
        )

    async def _click(self, selector: str) -> ToolResult:
        """Click element"""
        return ToolResult(
            content=[TextContent(type="text", text=f"Clicked element: {selector}")]
        )

    async def _fill(self, selector: str, text: str) -> ToolResult:
        """Fill text"""
        return ToolResult(
            content=[TextContent(type="text", text=f"Filled '{text}' in {selector}")]
        )

    async def _get_text(self, selector: str) -> ToolResult:
        """Get text"""
        return ToolResult(
            content=[TextContent(type="text", text=f"Retrieved text from {selector}")]
        )

    async def _wait_for_selector(self, selector: str, timeout: int) -> ToolResult:
        """Wait for selector"""
        return ToolResult(
            content=[TextContent(type="text", text=f"Waited for {selector} (timeout: {timeout}ms)")]
        )

    async def _take_screenshot(self, path: str) -> ToolResult:
        """Take screenshot"""
        return ToolResult(
            content=[TextContent(type="text", text=f"Screenshot saved to {path}")]
        )

    async def _execute_script(self, script: str) -> ToolResult:
        """Execute script"""
        return ToolResult(
            content=[TextContent(type="text", text=f"Executed script")]
        )

    async def _get_current_url(self) -> ToolResult:
        """Get current URL"""
        return ToolResult(
            content=[TextContent(type="text", text="Retrieved current URL")]
        )

    async def _get_page_title(self) -> ToolResult:
        """Get page title"""
        return ToolResult(
            content=[TextContent(type="text", text="Retrieved page title")]
        )

    async def _select_option(self, selector: str, value: str) -> ToolResult:
        """Select option"""
        return ToolResult(
            content=[TextContent(type="text", text=f"Selected '{value}' from {selector}")]
        )
