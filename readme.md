# Samsung SmartThings MCP Server

<div align="center">

![SmartThings](https://img.shields.io/badge/SmartThings-1C1E23?style=for-the-badge&logo=smartthings&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![MCP](https://img.shields.io/badge/MCP-FF6B35?style=for-the-badge&logo=anthropic&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)

**Control your Samsung TV through Claude Desktop using natural language commands**

[Features](#features) • [Installation](#installation) • [Usage](#usage) • [Configuration](#configuration) • [Contributing](#contributing)

</div>

---

## Overview

Samsung SmartThings MCP Server is a Model Context Protocol (MCP) server that enables Claude Desktop to control Samsung SmartThings devices, with a focus on Samsung TVs. Use natural language to turn your TV on/off, change channels, adjust volume, switch inputs, and more!

> **What is MCP?** The Model Context Protocol allows AI assistants like Claude to interact with external systems and services through standardized interfaces.

## Features

🔌 **Device Control**
- Turn Samsung TV on/off
- Change volume (0-100) and mute/unmute
- Switch TV channels
- Change input sources (HDMI1, HDMI2, USB, etc.)

📱 **Device Management**
- List all SmartThings devices
- Filter and display TV devices specifically
- Get detailed device information and status
- Real-time device state monitoring

🤖 **Natural Language Interface**
- Control devices using conversational commands
- "Turn on my Samsung TV"
- "Set volume to 25"
- "Change to HDMI1"
- "Mute the TV"

🛡️ **Secure & Reliable**
- Secure authentication using SmartThings Personal Access Tokens
- Comprehensive error handling and logging
- Async operations for responsive performance
- Built-in connection testing and diagnostics


## Prerequisites

- Python 3.8 or higher
- Samsung TV connected to SmartThings
- SmartThings account with Personal Access Token (this token should be updated every 24 hours)
- Claude Desktop application

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/PaulaAdelKamal/samsung_smartthings-mcp.git
cd smartthings-mcp-server
```

### 2. Set Up Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure SmartThings

#### Create Personal Access Token
1. Visit [SmartThings Token Manager](https://account.smartthings.com/tokens)
2. Log in with your SmartThings account
3. Click "Generate new token"
4. Name: "Claude MCP Server"
5. Select permissions:
   - ✅ **Devices** → Read devices
   - ✅ **Devices** → Execute commands on devices
   - ✅ **Locations** → Read locations
6. Copy the token (save it securely!)

#### Set Environment Variable
```bash
# Windows
set SMARTTHINGS_ACCESS_TOKEN=your_token_here

# macOS/Linux
export SMARTTHINGS_ACCESS_TOKEN="your_token_here"
```

### 5. Test Connection

```bash
python test_smartthings.py
```

You should see your connected devices listed, including your Samsung TV.

## Configuration

### Claude Desktop Setup

Add the MCP server to your Claude Desktop configuration:

#### Windows
Edit `%APPDATA%\Claude\claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "smartthings": {
      "command": "C:\\path\\to\\smartthings-mcp-server/venv/Scripts/python.exe",
      "args": ["C:\\path\\to\\smartthings-mcp-server\\smartthings_mcp.py"],
      "env": {
        "SMARTTHINGS_ACCESS_TOKEN": "your_token_here"
      }
    }
  }
}
```

#### macOS
Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "smartthings": {
      "command": "python3",
      "args": ["/path/to/smartthings-mcp-server/smartthings_mcp.py"],
      "env": {
        "SMARTTHINGS_ACCESS_TOKEN": "your_token_here"
      }
    }
  }
}
```

#### Linux
Edit `~/.config/Claude/claude_desktop_config.json` with the same configuration as macOS.

## Usage

Once configured, restart Claude Desktop and try these commands:

### Basic Commands

**List your devices:**
```
Show me my SmartThings devices
List my TV devices
```

**TV Control:**
```
Turn on my Samsung TV
Turn off the TV
Set TV volume to 30
Mute my TV
Change to channel 5
Switch TV input to HDMI1
```

**Device Information:**
```
What's the status of my TV?
Show me device information for [device_id]
```

### Example Conversation

```
You: "Turn on my Samsung TV and set volume to 25"

Claude: I'll help you turn on your Samsung TV and set the volume to 25.

First, let me turn on your TV:
✅ TV turned on successfully.

Now setting the volume to 25:
✅ Volume set to 25.

Your Samsung TV is now on with volume set to 25!
```

## Available Tools

| Tool | Description |
|------|-------------|
| `list_devices` | List all SmartThings devices |
| `list_tv_devices` | List TV devices only |
| `get_device_info` | Get detailed device information |
| `get_device_status` | Get current device status |
| `turn_tv_on_off` | Turn TV on or off |
| `change_tv_volume` | Set volume (0-100) |
| `mute_tv` | Mute or unmute TV |
| `change_tv_channel` | Change TV channel |
| `change_tv_input` | Change input source |

## Troubleshooting

### Common Issues

**"SmartThings client not initialized"**
- Verify your access token is correct
- Check environment variable is set
- Ensure token has necessary permissions

**"Device not found"**
- Confirm TV is connected to SmartThings app
- Verify you can control the TV through the SmartThings mobile app
- Check device ID is correct

**"API request failed"**
- Check internet connection
- Verify SmartThings service status
- Ensure access token hasn't expired

**MCP server not connecting**
- Verify Python script path in Claude config
- Check Python is in system PATH
- Ensure virtual environment is activated

### Debug Mode

Enable debug logging by modifying `smartthings_mcp.py`:

```python
logging.basicConfig(level=logging.DEBUG)
```

### Getting Help

- 📖 [SmartThings Developer Documentation](https://developer.smartthings.com/)
- 💬 [SmartThings Community](https://community.smartthings.com/)
- 🐛 [Report Issues](https://github.com/yourusername/smartthings-mcp-server/issues)

## Project Structure

```
smartthings-mcp-server/
├── smartthings_mcp.py      # Main MCP server
├── test_smartthings.py     # Connection test utility
├── requirements.txt        # Python dependencies
├── Quick_setup.bat              # Quick setup script (Windows)
├── SETUP_GUIDE.md         # Detailed setup instructions
└── README.md              # This file
```

## API Reference

### SmartThings Capabilities Used

- **switch**: Turn devices on/off
- **audioVolume**: Control volume and muting
- **tvChannel**: Change TV channels
- **mediaInputSource**: Switch input sources

### Authentication

Uses SmartThings Personal Access Tokens (PAT) with OAuth2 Bearer authentication.

**Required Scopes:**
- `r:devices:*` - Read device information
- `x:devices:*` - Execute device commands
- `r:locations:*` - Read location information

## Security

- 🔒 Access tokens are stored as environment variables
- 🛡️ No sensitive data is logged or persisted
- 🔑 Tokens can be rotated without code changes
- 📋 Follows SmartThings security best practices

**Security Best Practices:**
- Keep your access token secure
- Don't commit tokens to version control
- Regularly rotate access tokens
- Use environment variables for configuration

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Add tests if applicable
5. Commit: `git commit -m 'Add amazing feature'`
6. Push: `git push origin feature/amazing-feature`
7. Open a Pull Request

### Running Tests

```bash
# Test SmartThings connection
python test_smartthings.py

# Run the MCP server in test mode
python smartthings_mcp.py --test
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- 🏠 Samsung SmartThings for the comprehensive IoT platform
- 🤖 Anthropic for Claude and the MCP protocol
- 🐍 Python community for excellent async libraries

## Support

If you find this project helpful, please:
- ⭐ Star the repository
- 🐛 Report bugs via [Issues](https://github.com/yourusername/smartthings-mcp-server/issues)
- 💡 Suggest features or improvements
- 🔄 Share with others who might benefit

---

<div align="center">
Made with ❤️ for the smart home community

[⬆ Back to Top](#samsung-smartthings-mcp-server)
</div>