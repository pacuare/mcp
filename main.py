import os
import sys
from typing import Any
import asyncio

from mcp.server import Server
from mcp.types import Tool, TextContent
from mcp.server.stdio import stdio_server
from pacuare import Client


class PacuareMCPServer:
    """MCP Server for Pacuare database queries."""

    def __init__(self, api_key: str):
        """Initialize the Pacuare MCP server.

        Args:
            api_key: Pacuare API token for authentication
        """
        self.client = Client(api_key=api_key)
        self.server = Server("pacuare-mcp-server")

        # Register handlers
        self.server.list_tools()(self.list_tools)
        self.server.call_tool()(self.call_tool)

    async def list_tools(self) -> list[Tool]:
        """List available tools."""
        return [
            Tool(
                name="query_database",
                description=(
                    "Execute SQL queries against the Pacuare database. "
                    "This tool can be used for data retrieval, aggregations, and mathematical calculations. "
                    "For math operations, convert them to SQL queries (e.g., 'SELECT 5 + 3 AS result' for addition). "
                    "Returns results as a formatted table."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "sql": {
                            "type": "string",
                            "description": "SQL query to execute. Use standard SQL syntax. For math, use SELECT statements with arithmetic operators."
                        },
                        "params": {
                            "type": "array",
                            "description": "Optional query parameters for parameterized queries",
                            "items": {"type": "string"},
                            "default": []
                        }
                    },
                    "required": ["sql"]
                }
            )
        ]

    async def call_tool(self, name: str, arguments: Any) -> list[TextContent]:
        """Handle tool calls."""
        if name != "query_database":
            raise ValueError(f"Unknown tool: {name}")

        sql = arguments.get("sql")
        params = arguments.get("params", [])

        if not sql:
            raise ValueError("SQL query is required")

        try:
            # Execute query using Pacuare client
            result_df = self.client.query(sql=sql, params=params)

            # Format result as text
            if result_df.empty:
                result_text = "Query executed successfully. No rows returned."
            else:
                # Convert DataFrame to string with nice formatting
                result_text = f"Query returned {len(result_df)} row(s):\n\n{result_df.to_string(index=False)}"

            return [TextContent(type="text", text=result_text)]

        except Exception as e:
            error_msg = f"Error executing query: {str(e)}"
            return [TextContent(type="text", text=error_msg)]

    async def run(self):
        """Run the MCP server."""
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )


def main():
    """Main entry point for the Pacuare MCP server."""
    # Get API key from environment variable
    api_key = os.environ.get("PACUARE_API_KEY")

    if not api_key:
        print("Error: PACUARE_API_KEY environment variable is required", file=sys.stderr)
        print("Please set your Pacuare API token:", file=sys.stderr)
        print("  export PACUARE_API_KEY='your_api_key_here'", file=sys.stderr)
        sys.exit(1)

    # Create and run server
    server = PacuareMCPServer(api_key=api_key)
    asyncio.run(server.run())


if __name__ == "__main__":
    main()
