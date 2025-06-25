#!/usr/bin/env python3
"""
Manual Test Script for MCP Server
This script demonstrates how to manually send JSON-RPC requests to the MCP server.
"""

import json
import subprocess
import sys
import time


def send_request_to_server(server_process, request):
    """Send a JSON-RPC request to the server and get the response."""
    request_json = json.dumps(request) + "\n"
    server_process.stdin.write(request_json.encode())
    server_process.stdin.flush()
    
    response_line = server_process.stdout.readline()
    return json.loads(response_line.decode().strip())


def main():
    """Manual testing of the MCP server."""
    print("=== Manual MCP Server Test ===\n")
    
    # Start the server
    server_process = subprocess.Popen(
        [sys.executable, "mcp_server.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=False
    )
    
    try:
        print("Server started. Sending requests...\n")
        
        # Test 1: Initialize
        print("1. Sending initialize request...")
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "manual-test", "version": "1.0.0"}
            }
        }
        
        print(f"Request: {json.dumps(init_request, indent=2)}")
        response = send_request_to_server(server_process, init_request)
        print(f"Response: {json.dumps(response, indent=2)}\n")
        
        # Test 2: List tools
        print("2. Sending tools/list request...")
        list_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {}
        }
        
        print(f"Request: {json.dumps(list_request, indent=2)}")
        response = send_request_to_server(server_process, list_request)
        print(f"Response: {json.dumps(response, indent=2)}\n")
        
        # Test 3: Call add tool
        print("3. Sending tools/call request (add 15 + 27)...")
        call_request = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "add",
                "arguments": {"a": 15, "b": 27}
            }
        }
        
        print(f"Request: {json.dumps(call_request, indent=2)}")
        response = send_request_to_server(server_process, call_request)
        print(f"Response: {json.dumps(response, indent=2)}\n")
        
        # Test 4: Invalid method
        print("4. Sending invalid method request...")
        invalid_request = {
            "jsonrpc": "2.0",
            "id": 4,
            "method": "invalid/method",
            "params": {}
        }
        
        print(f"Request: {json.dumps(invalid_request, indent=2)}")
        response = send_request_to_server(server_process, invalid_request)
        print(f"Response: {json.dumps(response, indent=2)}\n")
        
        print("Manual testing completed successfully!")
        
    except Exception as e:
        print(f"Error during testing: {e}")
    finally:
        # Clean up
        if server_process.stdin:
            server_process.stdin.close()
        server_process.terminate()
        server_process.wait()
        print("Server stopped.")


if __name__ == "__main__":
    main()