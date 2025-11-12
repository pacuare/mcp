import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { Client } from "@pacuare/sdk";
import { z } from "zod"

// Create an MCP server
export const server = new McpServer({
  name: 'pacuare-mcp-server',
  version: '1.0.0',
});

// Add an addition tool
server.registerTool(
  'query',
  {
    title: 'Query Database',
    description: `
      Execute SQL queries against the Pacuare database.
      This tool can be used for data retrieval, aggregations, and mathematical calculations.
      For math operations, convert them to SQL queries (e.g., 'SELECT 5 + 3 AS result' for addition).
      This is a PostgreSQL database. Use examples from https://pacuare.dev/en/latest/useful-queries.html to help write queries.
      Most data is in the pacuare_raw table.
      Avoid writing data if at all possible.
      Returns results as a formatted table.
      For parameterized queries, send the (PostgreSQL-formatted) statement to be prepared in 'sql', and the parameters in 'params'.
    `,
    inputSchema: { sql: z.string(), params: z.array(z.string()) },
    outputSchema: { result: z.object({ columns: z.array(z.string()), values: z.array(z.array(z.any())) }) }
  },
  async ({ sql, params }, { requestInfo }) => {
    try {
      const output = { result: await new Client((requestInfo ?? console.log('no request info'))?.headers['x-api-key'] as string ?? process.env.PACUARE_API_KEY ?? "").query(sql, params) };
      return {
        content: [{ type: 'text', text: JSON.stringify(output) }],
        structuredContent: output
      };
    } catch (e: any) {
      throw `query returned status ${e.status}`;
    }
  }
);
