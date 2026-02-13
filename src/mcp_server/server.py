"""
MCP server implementation for Playwright
"""

import asyncio
from src.mcp_server import PlaywrightMCPServer


async def main():
    """Main entry point for MCP server"""
    server = PlaywrightMCPServer()

    # Print available tools
    print("Available Tools:")
    for tool in server.get_tools():
        print(f"  - {tool.name}: {tool.description}")

    # Server would normally run here
    print("\nMCP Server initialized successfully")


if __name__ == "__main__":
    asyncio.run(main())
