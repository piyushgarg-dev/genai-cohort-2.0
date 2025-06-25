#!/usr/bin/env python3
"""
Simple MCP Client Example
This client demonstrates how to interact with the MCP server.
"""

import asyncio
import json
import subprocess
import sys
from typing import Any, Dict


class MCPClient:
    """Simple MCP Client implementation."""
    
    def __init__(self, server_command: list):
        self.server_command = server_command
        self.process = None
        self.request_id = 0
    
    async def start_server(self):
        """Start the MCP server process."""
        self.process = await asyncio.create_subprocess_exec(
            *self.server_command,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        print("MCP Server started")
    
    async def send_request(self, method: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Send a request to the MCP server."""
        if not self.process or not self.process.stdin or not self.process.stdout:
            raise RuntimeError("Server not started or streams not available")
        
        self.request_id += 1
        request = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": method,
            "params": params or {}
        }
        
        # Send request
        request_json = json.dumps(request) + "\n"
        self.process.stdin.write(request_json.encode())
        await self.process.stdin.drain()
        
        # Read response
        response_line = await self.process.stdout.readline()
        response = json.loads(response_line.decode().strip())
        
        return response
    
    async def initialize(self):
        """Initialize the MCP connection."""
        response = await self.send_request("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {
                "name": "simple-client",
                "version": "1.0.0"
            }
        })
        print("Initialization response:", response)
        return response
    
    async def list_tools(self):
        """List available tools."""
        response = await self.send_request("tools/list")
        print("Available tools:", response)
        return response
    
    async def call_add_tool(self, a: float, b: float):
        """Call the add tool with two numbers."""
        response = await self.send_request("tools/call", {
            "name": "add",
            "arguments": {"a": a, "b": b}
        })
        print(f"Add tool result: {response}")
        return response
    
    async def close(self):
        """Close the connection and terminate the server."""
        if self.process:
            if self.process.stdin:
                self.process.stdin.close()
            await self.process.wait()
            print("MCP Server stopped")


async def main():
    """Main example function."""
    print("=== MCP Client Example ===\n")
    
    # Initialize client with server command
    client = MCPClient([sys.executable, "mcp_server.py"])
    
    try:
        # Start the server
        await client.start_server()
        
        # Initialize the connection
        print("1. Initializing connection...")
        await client.initialize()
        print()
        
        # List available tools
        print("2. Listing available tools...")
        await client.list_tools()
        print()
        
        # Test the add tool with different inputs
        print("3. Testing the add tool...")
        test_cases = [
            (5, 3),
            (10.5, 2.7),
            (-5, 8),
            (0, 0),
            (100, -50)
        ]
        
        for a, b in test_cases:
            await client.call_add_tool(a, b)
        print()
        
        print("4. Testing error handling...")
        # This will demonstrate error handling (missing arguments)
        response = await client.send_request("tools/call", {
            "name": "add",
            "arguments": {"a": 5}  # Missing 'b'
        })
        print(f"Error case result: {response}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())