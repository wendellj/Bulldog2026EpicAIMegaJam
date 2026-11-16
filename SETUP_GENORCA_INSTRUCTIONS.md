# Bulldog MegaJam - GenOrca/UnrealMCPython Setup Instructions

**For team members setting up the project with AI assistance**

## Prerequisites

- **Unreal Engine 5.8** installed
- **Git** installed
- **Python 3.11** (not 3.15 - compatibility issue with pydantic)
- **uv** (Python package manager) - https://docs.astral.sh/uv/
- **Claude Desktop** or **Claude Code CLI**

## Step 1: Install Meta XR Plugin (REQUIRED for Quest 3 VR)

**The Meta XR plugin is NOT included with Unreal Engine and must be installed manually.**

1. Go to: https://developer.oculus.com/downloads/package/unreal-engine-5-integration/
2. Download the **"Unreal Meta XR plugin"** (top right button)
3. **Close Unreal Editor if it's running**
4. Navigate to your UE 5.8 plugins folder:
   ```
   C:\Program Files\Epic Games\UE_5.8\Engine\Plugins\Marketplace
   ```
   - Create the `Marketplace` folder if it doesn't exist

5. Extract the downloaded .zip file into the `Marketplace` folder
   - You should have: `C:\Program Files\Epic Games\UE_5.8\Engine\Plugins\Marketplace\MetaXR\`

6. Launch Unreal Engine
7. Go to **Edit** → **Plugins** and search for **"Meta XR"**
8. Enable it (checkmark) and restart the editor when prompted

**Why this is required:**
- Hand tracking components (OculusXRHandComponent)
- Controller visualization (OculusXRController)
- Quest 3 specific features

Without this plugin, you'll get "Component class not found" errors when creating VR pawns.

## Step 2: Clone the Repository

```bash
git clone https://github.com/wendellj/Bulldog2026EpicAIMegaJam.git
cd Bulldog2026EpicAIMegaJam/Game
```

## Step 3: Install UnrealMCPython Plugin

The plugin is already in the repo at `Game/Plugins/UnrealMCPython/`.

**Verify it's there:**
```bash
ls Game/Plugins/UnrealMCPython/UnrealMCPython.uplugin
```

If missing, download from: https://fab.com/s/aed5f75d50b2

## Step 4: Install MCP Server Dependencies

```bash
cd Game/mcp-server
uv sync
```

This installs the GenOrca UnrealMCPython MCP server and dependencies.

## Step 5: Configure Claude Code/Desktop

**For Claude Code CLI** (recommended):

Create or edit: `C:\Bulldog\Game\.mcp.json`

```json
{
  "mcpServers": {
    "unreal-mcpython": {
      "command": "C:\\Users\\YOUR_USERNAME\\.local\\bin\\uv.exe",
      "args": [
        "--directory",
        "C:/Bulldog/Game/mcp-server",
        "run",
        "--python",
        "3.11",
        "src/unreal_mcp/main.py"
      ]
    }
  }
}
```

**Replace `YOUR_USERNAME` with your Windows username.**

**For Claude Desktop:**

Edit: `%APPDATA%\Claude\claude_desktop_config.json`

Add the same `mcpServers` block.

## Step 6: Launch Unreal Editor with MCP

**Option A - Use the launch script (Windows):**

```bash
cd C:\Bulldog\Game
LaunchEditor.bat
```

This automatically:
- Sets Android SDK environment variables
- Starts the MCP server on port 12029
- Launches Unreal Engine 5.8

**Option B - Manual launch:**

1. Start the MCP server manually:
```bash
cd C:\Bulldog\Game\mcp-server
uv run --python 3.11 src/unreal_mcp/main.py
```

2. Launch Unreal Editor and open `BulldogMegaJam.uproject`

## Step 7: Verify Plugin is Enabled

In Unreal Editor:
1. Edit → Plugins
2. Search for "UnrealMCPython"
3. Verify it's **enabled** (checkmark)
4. If not, enable it and **restart the editor**

## Step 8: Test Claude Integration

**In Claude Code or Claude Desktop, paste this:**

```
I'm working on the Bulldog MegaJam Unreal project. Can you:
1. List all actors in the current level
2. Check if the UnrealMCPython MCP server is connected
3. Show me what tools are available from GenOrca
```

**Claude should respond with level info if everything is working.**

## Troubleshooting

### "MCP server not found"
- Check that `uv` is installed: `uv --version`
- Verify Python 3.11: `python --version` or `py -3.11 --version`
- Check `.mcp.json` path matches your actual project location

### "Plugin failed to load"
- Right-click `BulldogMegaJam.uproject` → "Generate Visual Studio project files"
- Open the `.sln` file in Visual Studio
- Build → Build Solution
- Launch from Visual Studio (F5)

### "Port 12029 already in use"
- Check if another instance is running: `netstat -ano | findstr 12029`
- Kill the process or restart your computer

### "Python version mismatch"
The MCP server requires **Python 3.11-3.13** (NOT 3.15).

Check your version:
```bash
python --version
```

If you have Python 3.15, install Python 3.11 from python.org and use:
```bash
uv run --python 3.11 src/unreal_mcp/main.py
```

## What You Get

Once configured, Claude can:
- ✅ Create/modify Blueprints
- ✅ Spawn/edit actors in levels
- ✅ Manage materials and textures
- ✅ Create UI widgets (UMG)
- ✅ Configure animation blueprints
- ✅ Script gameplay logic
- ✅ **191 total Unreal actions across 16 namespaces**

Full docs: https://github.com/GenOrca/unreal-mcpython

## Resources

- **Project GitHub**: https://github.com/wendellj/Bulldog2026EpicAIMegaJam
- **GenOrca GitHub**: https://github.com/GenOrca/unreal-mcpython
- **GenOrca Fab Page**: https://fab.com/s/aed5f75d50b2
- **Video Demo**: https://youtu.be/V7KyjzFlBLk

## Getting Help

**Ten Minute Rule:**
- 0-10 min: Try to solve it yourself
- 10-20 min: Ask Claude (paste error messages)
- 20-30 min: Post in Discord #general
- 30+ min: Tag @Wendell for help

Don't sit stuck in silence - ask early, ask often.

---

**Ready to build?** Start with the daily standup at 11am. See you there!
