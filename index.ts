import { server } from './server';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';

(async () => {
  const transport = new StdioServerTransport();
  await server.connect(transport);
})();
