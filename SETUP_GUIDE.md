# Samsung SmartThings MCP Server Setup Guide

This guide will walk you through setting up a Samsung SmartThings MCP (Model Context Protocol) server to control your Samsung TV through Claude Desktop.

## Prerequisites

- Python 3.8 or higher
- Samsung TV registered in SmartThings app
- SmartThings account
- Claude Desktop application

## Step 1: Prepare Your SmartThings Environment

### 1.1 Install SmartThings App
1. Download and install the SmartThings app on your phone from:
   - iOS: App Store
   - Android: Google Play Store

### 1.2 Add Your Samsung TV to SmartThings
1. Open the SmartThings app
2. Tap the "+" button to add a device
3. Select "Add device" → "By device type" → "TV/AV"
4. Follow the instructions to connect your Samsung TV
5. Ensure you can control the TV through the SmartThings app (test power, volume, etc.)

**Important**: Make sure you can successfully control your TV through the SmartThings app before proceeding. If the connection is inactive, remove and re-add the device.

### 1.3 Create a Personal Access Token (PAT)
1. Go to https://account.smartthings.com/tokens
2. Log in with the same credentials you used in the SmartThings app
3. Click "Generate new token"
4. Enter a token name (e.g., "Claude MCP Server")
5. Select the following scopes/permissions:
   - ✅ **Devices** → Read devices
   - ✅ **Devices** → Execute commands on devices
   - ✅ **Locations** → Read locations
6. Click "Generate token"
7. **IMPORTANT**: Copy the token immediately and save it securely. You won't be able to see it again!

## Step 2: Set Up the MCP Server

### 2.1 Create Project Directory
```bash
mkdir smartthings-mcp
cd smartthings-mcp
```

### 2.2 Create Virtual Environment
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 2.3 Install Dependencies
Create a `requirements.txt` file with the following content:
```
aiohttp>=3.8.0
mcp>=1.0.0
```

Then install the dependencies:
```bash
pip install -r requirements.txt
```

### 2.4 Save the MCP Server Code
Save the SmartThings MCP Server code as `smartthings_mcp.py` in your project directory.

### 2.5 Set Environment Variable
Set your SmartThings access token as an environment variable:

**Windows (Command Prompt):**
```cmd
set SMARTTHINGS_ACCESS_TOKEN=your_access_token_here
```

**Windows (PowerShell):**
```powershell
$env:SMARTTHINGS_ACCESS_TOKEN="your_access_token_here"
```

**macOS/Linux:**
```bash
export SMARTTHINGS_ACCESS_TOKEN="your_access_token_here"
```

### 2.6 Test the Server
Test that the server can connect to SmartThings:
```bash
python smartthings_mcp.py
```

You should see a message like: "Connected to SmartThings. Found X devices."

Press `Ctrl+C` to stop the test.

## Step 3: Configure Claude Desktop

### 3.1 Locate Claude Desktop Configuration
Find your Claude Desktop configuration file:

**Windows:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

**macOS:**
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Linux:**
```
~/.config/Claude/claude_desktop_config.json
```

### 3.2 Create or Edit Configuration File
If the file doesn't exist, create it. Add the following configuration:

```json
{
  "mcpServers": {
    "smartthings": {
      "command": "python",
      "args": ["/path/to/your/smartthings_mcp.py"],
      "env": {
        "SMARTTHINGS_ACCESS_TOKEN": "your_access_token_here"
      }
    }
  }
}
```

**Important**: Replace `/path/to/your/smartthings_mcp.py` with the actual full path to your script.

### 3.3 Example Configurations

**Windows Example:**
```json
{
  "mcpServers": {
    "smartthings": {
      "command": "python",
      "args": ["C:\\Users\\YourUsername\\smartthings-mcp\\smartthings_mcp.py"],
      "env": {
        "SMARTTHINGS_ACCESS_TOKEN": "your_token_here"
      }
    }
  }
}
```

**macOS/Linux Example:**
```json
{
  "mcpServers": {
    "smartthings": {
      "command": "python3",
      "args": ["/Users/YourUsername/smartthings-mcp/smartthings_mcp.py"],
      "env": {
        "SMARTTHINGS_ACCESS_TOKEN": "your_token_here"
      }
    }
  }
}
```

## Step 4: Start Claude Desktop

1. Close Claude Desktop if it's running
2. Start Claude Desktop again
3. The MCP server should automatically connect

## Step 5: Test the Integration

### 5.1 Find Your TV Device ID
In Claude Desktop, type:
```
List my TV devices
```

This will show all your TV devices with their IDs, names, and capabilities.

### 5.2 Test Basic Commands
Try these commands in Claude:

**Turn TV on/off:**
```
Turn on my Samsung TV (use device ID: your_device_id)
```

**Change volume:**
```
Set my TV volume to 25
```

**Mute/unmute:**
```
Mute my TV
```

**Change channel:**
```
Change my TV to channel 5
```

**Change input:**
```
Change my TV input to HDMI1
```

## Available Commands

The MCP server provides these tools:

1. **list_devices** - List all SmartThings devices
2. **list_tv_devices** - List only TV devices
3. **get_device_info** - Get detailed device information
4. **get_device_status** - Get current device status
5. **turn_tv_on_off** - Turn TV on or off
6. **change_tv_volume** - Set TV volume (0-100)
7. **mute_tv** - Mute or unmute TV
8. **change_tv_channel** - Change TV channel
9. **change_tv_input** - Change input source

## Troubleshooting

### Common Issues

**1. "SmartThings client not initialized"**
- Check that your access token is correct
- Verify the environment variable is set properly
- Ensure your token has the necessary permissions

**2. "Device not found"**
- Make sure your TV is connected to SmartThings
- Try refreshing the device list
- Check if the device ID is correct

**3. "API request failed"**
- Verify your internet connection
- Check if your access token has expired
- Ensure SmartThings servers are accessible

**4. MCP server not connecting to Claude**
- Verify the path to your Python script is correct
- Check that Python is in your system PATH
- Ensure the virtual environment is properly configured

### Token Expiration
Personal Access Tokens must have explicitly defined permissions and expire within 24 hours unless created before December 30, 2024. If your token expires, you'll need to create a new one following Step 1.3.

### Debugging
To enable debug logging, set the logging level in the script:
```python
logging.basicConfig(level=logging.DEBUG)
```

### Getting Help
- Check the SmartThings Community: https://community.smartthings.com/
- SmartThings Developer Documentation: https://developer.smartthings.com/
- Verify your devices support the capabilities you're trying to use

## Security Notes

- Keep your access token secure and never share it
- Consider using environment variables or secure storage for the token
- Regularly rotate your access tokens
- Only grant the minimum necessary permissions

## Advanced Usage

### Custom Commands
You can extend the MCP server to support additional SmartThings capabilities by:
1. Adding new tools to the `handle_list_tools()` function
2. Implementing the corresponding logic in `handle_call_tool()`
3. Using the appropriate SmartThings API capabilities

### Multiple Devices
To control multiple TVs or other devices, you can:
1. Use the `list_devices` command to see all available devices
2. Note the device IDs for each device you want to control
3. Use the device-specific commands with the appropriate device ID

### Automation
You can create complex automation by chaining commands:
```
Turn on my TV, set volume to 20, and change to HDMI1
```

Claude will execute these as separate API calls in sequence.

---

Your Samsung SmartThings MCP server is now ready! You can control your Samsung TV directly through Claude Desktop using natural language commands.