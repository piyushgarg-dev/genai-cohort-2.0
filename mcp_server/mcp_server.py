#!/usr/bin/env python3
"""
Simple MCP (Model Context Protocol) Server Example
This server exposes a simple "add" tool that performs basic arithmetic addition.
"""

import asyncio
import json
import sys
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, asdict


@dataclass
class Tool:
    """Represents a tool that can be called by the client."""
    name: str
    description: str
    inputSchema: Dict[str, Any]


@dataclass
class ToolCallRequest:
    """Represents a request to call a tool."""
    name: str
    arguments: Dict[str, Any]


@dataclass
class ToolCallResult:
    """Represents the result of a tool call."""
    content: List[Dict[str, Any]]
    isError: bool = False


class MCPServer:
    """Simple MCP Server implementation."""
    
    def __init__(self):
        self.tools = {
            "add": Tool(
                name="add",
                description="Add two numbers together",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "a": {
                            "type": "number",
                            "description": "First number to add"
                        },
                        "b": {
                            "type": "number",
                            "description": "Second number to add"
                        }
                    },
                    "required": ["a", "b"]
                }
            )
        }
    
    async def handle_initialize(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle initialization request."""
        return {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {}
            },
            "serverInfo": {
                "name": "simple-math-server",
                "version": "1.0.0"
            }
        }
    
    async def handle_list_tools(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tools/list request."""
        return {
            "tools": [asdict(tool) for tool in self.tools.values()]
        }
    
    async def handle_call_tool(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tools/call request."""
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        if tool_name == "add":
            return await self._call_add_tool(arguments)
        else:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Unknown tool: {tool_name}"
                    }
                ],
                "isError": True
            }
    
    async def _call_add_tool(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the add tool."""
        try:
            a = arguments.get("a")
            b = arguments.get("b")
            
            if a is None or b is None:
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": "Missing required arguments 'a' and/or 'b'"
                        }
                    ],
                    "isError": True
                }
            
            result = a + b
            
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"The sum of {a} and {b} is {result}"
                    }
                ],
                "isError": False
            }
            
        except Exception as e:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Error performing addition: {str(e)}"
                    }
                ],
                "isError": True
            }
    
    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming MCP request."""
        method = request.get("method")
        params = request.get("params", {})
        
        if method == "initialize":
            result = await self.handle_initialize(params)
        elif method == "tools/list":
            result = await self.handle_list_tools(params)
        elif method == "tools/call":
            result = await self.handle_call_tool(params)
        else:
            result = {
                "error": {
                    "code": -32601,
                    "message": f"Method not found: {method}"
                }
            }
        
        return {
            "jsonrpc": "2.0",
            "id": request.get("id"),
            "result": result
        }
    
    async def run(self):
        """Run the MCP server."""
        print("MCP Server starting...", file=sys.stderr)
        print("Server capabilities: tools (add)", file=sys.stderr)
        
        try:
            while True:
                # Read JSON-RPC request from stdin
                line = await asyncio.get_event_loop().run_in_executor(
                    None, sys.stdin.readline
                )
                
                if not line:
                    break
                
                try:
                    request = json.loads(line.strip())
                    response = await self.handle_request(request)
                    
                    # Send response to stdout
                    print(json.dumps(response))
                    sys.stdout.flush()
                    
                except json.JSONDecodeError as e:
                    print(f"JSON decode error: {e}", file=sys.stderr)
                except Exception as e:
                    print(f"Error processing request: {e}", file=sys.stderr)
                    
        except KeyboardInterrupt:
            print("Server shutting down...", file=sys.stderr)


async def main():
    """Main entry point."""
    server = MCPServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())