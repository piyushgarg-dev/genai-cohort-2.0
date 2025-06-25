# Simple MCP Server Example

This directory contains a simple implementation of a Model Context Protocol (MCP) server in Python that exposes an "add" tool for basic arithmetic operations.

## What is MCP?

Model Context Protocol (MCP) is a standardized way for AI assistants to connect with external data sources and tools. It allows AI models to access real-time information and perform actions through a structured, secure interface.

## Files

- `mcp_server.py` - The main MCP server implementation
- `client_example.py` - A simple client to test the server
- `manual_test.py` - Manual testing script showing raw JSON-RPC requests
- `README.md` - This documentation file

## Features

The MCP server implements:

- **Tool capability**: Exposes an "add" tool that can add two numbers
- **JSON-RPC protocol**: Communicates using JSON-RPC 2.0 over stdin/stdout
- **Error handling**: Proper error responses for invalid requests
- **Async support**: Built with asyncio for non-blocking operations

## How to Run

### Running the Server Directly

```bash
cd mcp_server
python3 mcp_server.py
```

The server will wait for JSON-RPC requests on stdin and respond on stdout.

### Testing with the Client Example

```bash
cd mcp_server
python3 client_example.py
```

This will start the server automatically and demonstrate:
1. Server initialization
2. Listing available tools
3. Calling the add tool with various inputs
4. Error handling

### Manual Testing with Raw JSON-RPC

```bash
cd mcp_server
python3 manual_test.py
```

This script shows exactly what JSON-RPC requests and responses look like, making it easier to understand the protocol.

## MCP Protocol Flow

1. **Initialize**: Client sends an `initialize` request to establish the connection
2. **List Tools**: Client requests available tools with `tools/list`
3. **Call Tool**: Client calls a specific tool with `tools/call`

### Example Requests/Responses

**Initialize Request:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2024-11-05",
    "capabilities": {},
    "clientInfo": {"name": "client", "version": "1.0.0"}
  }
}
```

**Initialize Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "protocolVersion": "2024-11-05",
    "capabilities": {"tools": {}},
    "serverInfo": {"name": "simple-math-server", "version": "1.0.0"}
  }
}
```

**Tool Call Request:**
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "add",
    "arguments": {"a": 5, "b": 3}
  }
}
```

**Tool Call Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "The sum of 5 and 3 is 8"
      }
    ],
    "isError": false
  }
}
```

## Extending the Server

To add more tools:

1. Define a new `Tool` object in the `__init__` method
2. Add a handler method (e.g., `_call_multiply_tool`)
3. Update the `handle_call_tool` method to route to your new handler

Example:
```python
# In __init__:
"multiply": Tool(
    name="multiply",
    description="Multiply two numbers",
    inputSchema={
        "type": "object",
        "properties": {
            "a": {"type": "number", "description": "First number"},
            "b": {"type": "number", "description": "Second number"}
        },
        "required": ["a", "b"]
    }
)

# Handler method:
async def _call_multiply_tool(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
    a = arguments.get("a")
    b = arguments.get("b")
    result = a * b
    return {
        "content": [{"type": "text", "text": f"{a} × {b} = {result}"}],
        "isError": False
    }
```

## Requirements

- Python 3.7 or higher
- No external dependencies (uses only standard library)

## Notes

- The server uses stdin/stdout for communication (standard for MCP servers)
- Error messages are logged to stderr
- The server runs indefinitely until interrupted (Ctrl+C)
- All communication follows the JSON-RPC 2.0 specification