#!/usr/bin/env python3
"""
Test script for SmartThings MCP Server
This script helps verify that your SmartThings connection is working properly.
"""

import asyncio
import json
import os
import sys
from smartthings_mcp import SmartThingsClient

async def test_connection():
    """Test SmartThings connection and list devices"""
    
    # Get access token from environment
    access_token = os.getenv("SMARTTHINGS_ACCESS_TOKEN")
    if not access_token:
        print("❌ ERROR: SMARTTHINGS_ACCESS_TOKEN environment variable not set")
        print("\nPlease set your access token:")
        print("Windows: set SMARTTHINGS_ACCESS_TOKEN=your_token_here")
        print("macOS/Linux: export SMARTTHINGS_ACCESS_TOKEN=\"your_token_here\"")
        sys.exit(1)
    
    print("🔧 Testing SmartThings connection...")
    
    # Initialize client
    client = SmartThingsClient(access_token)
    
    try:
        # Test basic connection
        print("📡 Fetching devices...")
        devices = await client.get_devices()
        print(f"✅ Successfully connected! Found {len(devices)} devices.\n")
        
        if not devices:
            print("⚠️  No devices found. Make sure your devices are added to SmartThings app.")
            return
        
        # List all devices
        print("📱 All devices:")
        print("-" * 50)
        for i, device in enumerate(devices, 1):
            name = device.get("name", "Unknown")
            device_id = device.get("deviceId", "Unknown")
            device_type = device.get("type", "Unknown")
            print(f"{i}. {name}")
            print(f"   ID: {device_id}")
            print(f"   Type: {device_type}")
            
            # Show capabilities
            components = device.get("components", [])
            if components:
                capabilities = components[0].get("capabilities", [])
                cap_names = [cap.get("id", "") for cap in capabilities]
                print(f"   Capabilities: {', '.join(cap_names[:5])}")
                if len(cap_names) > 5:
                    print(f"                 ... and {len(cap_names) - 5} more")
            print()
        
        # Find and highlight TV devices
        print("📺 TV devices:")
        print("-" * 50)
        tv_devices = await client.get_tv_devices()
        
        if tv_devices:
            for i, tv in enumerate(tv_devices, 1):
                name = tv.get("name", "Unknown")
                device_id = tv.get("deviceId", "Unknown")
                print(f"{i}. {name} (ID: {device_id})")
                
                # Test getting device status
                try:
                    print("   🔍 Testing device status...")
                    status = await client.get_device_status(device_id)
                    if status:
                        components = status.get("components", {})
                        main_component = components.get("main", {})
                        
                        # Check power status
                        switch_status = main_component.get("switch", {})
                        if switch_status:
                            power_state = switch_status.get("switch", {}).get("value", "unknown")
                            print(f"   ⚡ Power: {power_state}")
                        
                        # Check volume if available
                        volume_status = main_component.get("audioVolume", {})
                        if volume_status:
                            volume = volume_status.get("volume", {}).get("value", "unknown")
                            mute = volume_status.get("mute", {}).get("value", "unknown")
                            print(f"   🔊 Volume: {volume}, Muted: {mute}")
                        
                        print("   ✅ Device status retrieved successfully")
                    else:
                        print("   ⚠️  Could not retrieve device status")
                except Exception as e:
                    print(f"   ❌ Error getting device status: {e}")
                print()
        else:
            print("⚠️  No TV devices found.")
            print("   Make sure your Samsung TV is:")
            print("   - Connected to your SmartThings app")
            print("   - Powered on and connected to the same network")
            print("   - Properly paired with SmartThings")
        
        print("\n🎉 Connection test completed!")
        print("\nNext steps:")
        print("1. Note the device IDs for your TVs above")
        print("2. Configure Claude Desktop with the MCP server")
        print("3. Test commands like 'List my TV devices' in Claude")
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("\nTroubleshooting:")
        print("1. Check your access token is correct")
        print("2. Ensure your token has the right permissions:")
        print("   - Devices → Read devices")
        print("   - Devices → Execute commands on devices")
        print("   - Locations → Read locations")
        print("3. Verify your internet connection")
        print("4. Check SmartThings service status")

if __name__ == "__main__":
    print("🧪 SmartThings MCP Server Test")
    print("=" * 40)
    asyncio.run(test_connection())