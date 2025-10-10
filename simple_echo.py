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
    return text


if __name__ == "__main__":
    mcp.run()