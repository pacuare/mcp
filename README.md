# Pacuare MCP Server

An MCP (Model Context Protocol) server that provides access to the Pacuare database through SQL queries.

## Features

- Execute SQL queries against the Pacuare database
- Secure authentication using Pacuare API tokens
- Support for mathematical operations via SQL queries
- Returns formatted results as tables

## Installation

Install the required dependencies using uv or pip:

```bash
uv pip install -e .
```

Or with pip:

```bash
pip install -e .
```

## Configuration

Set your Pacuare API token as an environment variable:

```bash
export PACUARE_API_KEY='your_api_key_here'
```

## Usage

### Running the Server

Run the MCP server:

```bash
python main.py
```

Or with uv:

```bash
uv run python main.py
```

### Using with Claude Desktop

Add this server to your Claude Desktop configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "pacuare": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/pacuare/mcp",
        "run",
        "python",
        "main.py"
      ],
      "env": {
        "PACUARE_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

## Available Tools

### query_database

Execute SQL queries against the Pacuare database.

**Parameters:**
- `sql` (string, required): SQL query to execute
- `params` (array, optional): Query parameters for parameterized queries

**Examples:**

Query data:
```sql
SELECT * FROM users LIMIT 10
```

Mathematical operations:
```sql
SELECT 42 * 1.5 + 10 AS result
```

Aggregations:
```sql
SELECT COUNT(*) as total, AVG(price) as avg_price FROM products
```

## Security

- API tokens are required for all operations
- Tokens are passed via environment variables (never hardcoded)
- The server only supports read operations through SQL queries

## Development

Built with:
- [Pacuare SDK](https://pacuare.dev) - Database access
- [MCP Python SDK](https://modelcontextprotocol.io) - Model Context Protocol implementation
- Python 3.13+
