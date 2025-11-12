pack: build
    bunx @anthropic-ai/mcpb pack bin pacuare-mcp.mcpb

build:
    bun build --compile --bytecode --outfile=bin/pacuare-mcp index.ts
