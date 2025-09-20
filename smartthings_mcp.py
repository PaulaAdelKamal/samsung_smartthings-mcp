#!/usr/bin/env python3
"""
Samsung SmartThings MCP Server
A Model Context Protocol server for controlling Samsung SmartThings devices,
specifically Samsung TVs.
"""

import asyncio
import json
import logging
import os
import sys
from typing import Any, Dict, List, Optional, Sequence
from urllib.parse import urljoin

import aiohttp
from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListToolsRequest,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("smartthings-mcp")

class SmartThingsClient:
    """Client for Samsung SmartThings API"""
    
    def __init__(self, access_token: str):
        self.access_token = access_token
        self.base_url = "https://api.smartthings.com/v1"
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
    
    async def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict:
        """Make an HTTP request to the SmartThings API"""
        url = urljoin(self.base_url, endpoint)
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.request(
                    method, url, headers=self.headers, json=data
                ) as response:
                    response.raise_for_status()
                    return await response.json()
            except aiohttp.ClientError as e:
                logger.error(f"API request failed: {e}")
                raise
    
    async def get_devices(self) -> List[Dict]:
        """Get all devices from SmartThings"""
        try:
            response = await self._make_request("GET", "/devices")
            return response.get("items", [])
        except Exception as e:
            logger.error(f"Failed to get devices: {e}")
            return []
    
    async def get_device(self, device_id: str) -> Optional[Dict]:
        """Get a specific device"""
        try:
            return await self._make_request("GET", f"/devices/{device_id}")
        except Exception as e:
            logger.error(f"Failed to get device {device_id}: {e}")
            return None
    
    async def get_device_status(self, device_id: str) -> Optional[Dict]:
        """Get device status"""
        try:
            return await self._make_request("GET", f"/devices/{device_id}/status")
        except Exception as e:
            logger.error(f"Failed to get device status for {device_id}: {e}")
            return None
    
    async def send_device_command(self, device_id: str, commands: List[Dict]) -> Dict:
        """Send command to device"""
        try:
            data = {"commands": commands}
            return await self._make_request("POST", f"/devices/{device_id}/commands", data)
        except Exception as e:
            logger.error(f"Failed to send command to device {device_id}: {e}")
            raise
    
    async def get_tv_devices(self) -> List[Dict]:
        """Get all TV devices"""
        devices = await self.get_devices()
        tv_devices = []
        
        for device in devices:
            # Check if device has TV-related capabilities
            capabilities = device.get("components", [{}])[0].get("capabilities", [])
            capability_names = [cap.get("id", "") for cap in capabilities]
            
            if any(cap in capability_names for cap in [
                "switch", "audioVolume", "mediaInputSource", "tvChannel"
            ]):
                tv_devices.append(device)
        
        return tv_devices

class SmartThingsMCPServer:
    """MCP Server for SmartThings"""
    
    def __init__(self):
        self.server = Server("smartthings-mcp")
        self.client: Optional[SmartThingsClient] = None
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Setup MCP server handlers"""
        
        @self.server.list_tools()
        async def handle_list_tools() -> List[Tool]:
            """List available tools"""
            return [
                Tool(
                    name="list_devices",
                    description="List all SmartThings devices",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                ),
                Tool(
                    name="list_tv_devices",
                    description="List all TV devices in SmartThings",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                ),
                Tool(
                    name="get_device_info",
                    description="Get detailed information about a specific device",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "device_id": {
                                "type": "string",
                                "description": "The device ID"
                            }
                        },
                        "required": ["device_id"]
                    }
                ),
                Tool(
                    name="get_device_status",
                    description="Get the current status of a device",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "device_id": {
                                "type": "string",
                                "description": "The device ID"
                            }
                        },
                        "required": ["device_id"]
                    }
                ),
                Tool(
                    name="turn_tv_on_off",
                    description="Turn Samsung TV on or off",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "device_id": {
                                "type": "string",
                                "description": "The TV device ID"
                            },
                            "action": {
                                "type": "string",
                                "enum": ["on", "off"],
                                "description": "Turn the TV on or off"
                            }
                        },
                        "required": ["device_id", "action"]
                    }
                ),
                Tool(
                    name="change_tv_volume",
                    description="Change Samsung TV volume",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "device_id": {
                                "type": "string",
                                "description": "The TV device ID"
                            },
                            "volume": {
                                "type": "integer",
                                "minimum": 0,
                                "maximum": 100,
                                "description": "Volume level (0-100)"
                            }
                        },
                        "required": ["device_id", "volume"]
                    }
                ),
                Tool(
                    name="mute_tv",
                    description="Mute or unmute Samsung TV",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "device_id": {
                                "type": "string",
                                "description": "The TV device ID"
                            },
                            "mute": {
                                "type": "boolean",
                                "description": "True to mute, False to unmute"
                            }
                        },
                        "required": ["device_id", "mute"]
                    }
                ),
                Tool(
                    name="change_tv_channel",
                    description="Change Samsung TV channel",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "device_id": {
                                "type": "string",
                                "description": "The TV device ID"
                            },
                            "channel": {
                                "type": "string",
                                "description": "Channel number or name"
                            }
                        },
                        "required": ["device_id", "channel"]
                    }
                ),
                Tool(
                    name="change_tv_input",
                    description="Change Samsung TV input source",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "device_id": {
                                "type": "string",
                                "description": "The TV device ID"
                            },
                            "input_source": {
                                "type": "string",
                                "description": "Input source (e.g., 'HDMI1', 'HDMI2', 'USB', etc.)"
                            }
                        },
                        "required": ["device_id", "input_source"]
                    }
                )
            ]
        
        @self.server.call_tool()
        async def handle_call_tool(
            name: str, arguments: dict
        ) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
            """Handle tool calls"""
            
            if not self.client:
                return [TextContent(
                    type="text",
                    text="SmartThings client not initialized. Please check your access token."
                )]
            
            try:
                if name == "list_devices":
                    devices = await self.client.get_devices()
                    return [TextContent(
                        type="text",
                        text=json.dumps(devices, indent=2)
                    )]
                
                elif name == "list_tv_devices":
                    tv_devices = await self.client.get_tv_devices()
                    return [TextContent(
                        type="text",
                        text=json.dumps(tv_devices, indent=2)
                    )]
                
                elif name == "get_device_info":
                    device_id = arguments["device_id"]
                    device_info = await self.client.get_device(device_id)
                    if device_info:
                        return [TextContent(
                            type="text",
                            text=json.dumps(device_info, indent=2)
                        )]
                    else:
                        return [TextContent(
                            type="text",
                            text=f"Device {device_id} not found"
                        )]
                
                elif name == "get_device_status":
                    device_id = arguments["device_id"]
                    status = await self.client.get_device_status(device_id)
                    if status:
                        return [TextContent(
                            type="text",
                            text=json.dumps(status, indent=2)
                        )]
                    else:
                        return [TextContent(
                            type="text",
                            text=f"Could not get status for device {device_id}"
                        )]
                
                elif name == "turn_tv_on_off":
                    device_id = arguments["device_id"]
                    action = arguments["action"]
                    
                    commands = [{
                        "component": "main",
                        "capability": "switch",
                        "command": action
                    }]
                    
                    result = await self.client.send_device_command(device_id, commands)
                    return [TextContent(
                        type="text",
                        text=f"TV turned {action}. Result: {json.dumps(result, indent=2)}"
                    )]
                
                elif name == "change_tv_volume":
                    device_id = arguments["device_id"]
                    volume = arguments["volume"]
                    
                    commands = [{
                        "component": "main",
                        "capability": "audioVolume",
                        "command": "setVolume",
                        "arguments": [volume]
                    }]
                    
                    result = await self.client.send_device_command(device_id, commands)
                    return [TextContent(
                        type="text",
                        text=f"Volume set to {volume}. Result: {json.dumps(result, indent=2)}"
                    )]
                
                elif name == "mute_tv":
                    device_id = arguments["device_id"]
                    mute = arguments["mute"]
                    
                    commands = [{
                        "component": "main",
                        "capability": "audioVolume",
                        "command": "mute" if mute else "unmute"
                    }]
                    
                    result = await self.client.send_device_command(device_id, commands)
                    return [TextContent(
                        type="text",
                        text=f"TV {'muted' if mute else 'unmuted'}. Result: {json.dumps(result, indent=2)}"
                    )]
                
                elif name == "change_tv_channel":
                    device_id = arguments["device_id"]
                    channel = arguments["channel"]
                    
                    commands = [{
                        "component": "main",
                        "capability": "tvChannel",
                        "command": "setTvChannel",
                        "arguments": [channel]
                    }]
                    
                    result = await self.client.send_device_command(device_id, commands)
                    return [TextContent(
                        type="text",
                        text=f"Channel changed to {channel}. Result: {json.dumps(result, indent=2)}"
                    )]
                
                elif name == "change_tv_input":
                    device_id = arguments["device_id"]
                    input_source = arguments["input_source"]
                    
                    commands = [{
                        "component": "main",
                        "capability": "mediaInputSource",
                        "command": "setInputSource",
                        "arguments": [input_source]
                    }]
                    
                    result = await self.client.send_device_command(device_id, commands)
                    return [TextContent(
                        type="text",
                        text=f"Input changed to {input_source}. Result: {json.dumps(result, indent=2)}"
                    )]
                
                else:
                    return [TextContent(
                        type="text",
                        text=f"Unknown tool: {name}"
                    )]
            
            except Exception as e:
                logger.error(f"Error in tool {name}: {e}")
                return [TextContent(
                    type="text",
                    text=f"Error executing {name}: {str(e)}"
                )]
    
    async def run(self):
        """Run the MCP server"""
        # Get access token from environment
        access_token = os.getenv("SMARTTHINGS_ACCESS_TOKEN")
        if not access_token:
            logger.error("SMARTTHINGS_ACCESS_TOKEN environment variable not set")
            sys.exit(1)
        
        # Initialize SmartThings client
        self.client = SmartThingsClient(access_token)
        
        # Test connection
        try:
            devices = await self.client.get_devices()
            logger.info(f"Connected to SmartThings. Found {len(devices)} devices.")
        except Exception as e:
            logger.error(f"Failed to connect to SmartThings: {e}")
            sys.exit(1)
        
        # Run server
        from mcp.server.stdio import stdio_server
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="smartthings-mcp",
                    server_version="1.0.0",
                    capabilities=self.server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={},
                    ),
                ),
            )

async def main():
    """Main entry point"""
    server = SmartThingsMCPServer()
    await server.run()

if __name__ == "__main__":
    asyncio.run(main())