"""
FastMCP Echo Server
"""

import sys
from mcp.server.fastmcp import FastMCP

# Create server
mcp = FastMCP("Echo Server")


@mcp.tool()
def echo(text: str) -> str:
    """Echo the input text"""
    return "hola " + text


@mcp.tool()
def get_weather(location: str) -> dict:
    """Gets current weather for a location."""
    return {
        "temperature": 84.5,
        "conditions": "Sunny",
        "location": location
    }

if __name__ == "__main__":
    mcp.run()