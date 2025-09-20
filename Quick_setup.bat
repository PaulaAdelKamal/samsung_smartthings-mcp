#!/bin/bash
# Quick Setup Script for Samsung SmartThings MCP Server
# This script automates the initial setup process

set -e

echo "🚀 Samsung SmartThings MCP Server Quick Setup"
echo "=============================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Create project directory
PROJECT_DIR="smartthings-mcp"
if [ -d "$PROJECT_DIR" ]; then
    echo "⚠️  Directory $PROJECT_DIR already exists. Remove it? (y/N)"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        rm -rf "$PROJECT_DIR"
    else
        echo "Exiting..."
        exit 1
    fi
fi

echo "📁 Creating project directory: $PROJECT_DIR"
mkdir "$PROJECT_DIR"
cd "$PROJECT_DIR"

# Create virtual environment
echo "🐍 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "⚡ Activating virtual environment..."
source venv/bin/activate

# Create requirements.txt
echo "📦 Creating requirements.txt..."
cat > requirements.txt << EOL
aiohttp>=3.8.0
mcp>=1.0.0
EOL

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Prompt for access token
echo ""
echo "🔑 SmartThings Access Token Setup"
echo "=================================="
echo "You need to create a Personal Access Token (PAT) for SmartThings."
echo ""
echo "Steps:"
echo "1. Go to https://account.smartthings.com/tokens"
echo "2. Log in with your SmartThings account"
echo "3. Click 'Generate new token'"
echo "4. Name: 'Claude MCP Server'"
echo "5. Select permissions:"
echo "   ✅ Devices → Read devices"
echo "   ✅ Devices → Execute commands on devices"  
echo "   ✅ Locations → Read locations"
echo "6. Click 'Generate token'"
echo "7. Copy the token (you won't see it again!)"
echo ""

read -p "Enter your SmartThings access token: " ACCESS_TOKEN

if [ -z "$ACCESS_TOKEN" ]; then
    echo "❌ No access token provided. Exiting..."
    exit 1
fi

# Create .env file
echo "📄 Creating .env file..."
cat > .env << EOL
SMARTTHINGS_ACCESS_TOKEN=$ACCESS_TOKEN
EOL

# Download the MCP server script (placeholder - you'd need to save this manually)
echo "📥 You need to save the SmartThings MCP server code as 'smartthings_mcp.py'"
echo "    The code is provided in the setup guide."

# Create a simple activation script
cat > activate.sh << 'EOL'
#!/bin/bash
source venv/bin/activate
source .env
export SMARTTHINGS_ACCESS_TOKEN
EOL

chmod +x activate.sh

# Create Windows activation script
cat > activate.bat << 'EOL'
@echo off
call venv\Scripts\activate.bat
for /f "tokens=*" %%a in (.env) do set %%a
EOL

echo ""
echo "🎉 Setup completed!"
echo ""
echo "Next steps:"
echo "1. Save the SmartThings MCP server code as 'smartthings_mcp.py' in this directory"
echo "2. Save the test script as 'test_smartthings.py' in this directory"
echo ""
echo "To activate the environment:"
echo "  Linux/macOS: source activate.sh"
echo "  Windows: activate.bat"
echo ""
echo "To test the connection:"
echo "  python test_smartthings.py"
echo ""
echo "Project directory: $(pwd)"

# Create a simple README
cat > README.md << 'EOL'
# SmartThings MCP Server

This directory contains your Samsung SmartThings MCP server setup.

## Files
- `smartthings_mcp.py` - Main MCP server (save the provided code here)
- `test_smartthings.py` - Test script (save the provided code here)
- `requirements.txt` - Python dependencies
- `.env` - Environment variables (contains your access token)
- `activate.sh` / `activate.bat` - Environment activation scripts

## Quick Start
1. Activate environment: `source activate.sh` (Linux/macOS) or `activate.bat` (Windows)
2. Test connection: `python test_smartthings.py`
3. Run server: `python smartthings_mcp.py`

## Configuration
Edit `.env` to update your access token if needed.

## Claude Desktop Configuration
Add this to your Claude Desktop config:
```json
{
  "mcpServers": {
    "smartthings": {
      "command": "python",
      "args": ["/full/path/to/smartthings_mcp.py"],
      "env": {
        "SMARTTHINGS_ACCESS_TOKEN": "your_token_from_env_file"
      }
    }
  }
}
```
EOL

echo "📚 README.md created with instructions"
echo ""
echo "⚠️  Remember to:"
echo "   - Keep your .env file secure (contains access token)"
echo "   - Add .env to .gitignore if using version control"
echo "   - Follow the complete setup guide for Claude Desktop integration"