# Discord Airdrop Notifier - Windows Version

A Discord client that monitors channels for cryptocurrency airdrops and provides comprehensive Windows-specific notifications including sound alerts, text-to-speech, native Windows toast notifications, and message boxes.

## Features

- **Multi-modal Notifications**: Combines sound, speech, toast notifications, and message boxes
- **Cryptocurrency Detection**: Monitors for popular cryptocurrencies (BTC, ETH, DOGE, LTC, etc.)
- **Windows Integration**: Native Windows notifications with clickable message boxes
- **Audio Alerts**: Custom sound files with system sound fallback
- **Text-to-Speech**: Configurable speech announcements
- **Server Management**: Configurable muted servers and channels
- **Discord URI Support**: Click notifications to jump directly to the message

## Setup

### Requirements
- Windows OS (uses Windows-specific libraries)
- Python 3.7+ 
- Valid Discord user account token

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure your settings using the configuration file

### Configuration Setup

The application uses a `config.json` file for all settings. On first run, it will automatically create this file from the template.

**First-time setup:**
1. Run the application once - it will create `config.json` and exit
2. Edit `config.json` with your Discord token and preferences
3. Run the application again

**Manual setup:**
1. Copy `config.json.template` to `config.json`
2. Edit the configuration file with your settings

### How to Get Your Discord Token

⚠️ **Warning: Your Discord token is like a password. Never share it with anyone or post it publicly.**

1. **Open Discord in your web browser** (not the desktop app)
2. **Open Developer Tools**: Press `F12` or right-click and select "Inspect"
3. **Go to the Network tab** in Developer Tools
4. **Send any message** in any Discord channel
5. **Look for requests** starting with "messages" in the Network tab
6. **Click on one of these requests**
7. **Go to the Headers section** and find "Authorization"
8. **Copy the token** (it will be a long string of letters and numbers)
9. **Replace the token** in `airdropnotif.py` line 30

**Alternative Method:**
1. Press `Ctrl+Shift+I` in Discord web browser
2. Go to Console tab
3. Type: `(webpackChunkdiscord_app.push([[''],{},e=>{m=[];for(let c in e.c)m.push(e.c[c])}]),m).find(m=>m?.exports?.default?.getToken!==void 0).exports.default.getToken()`
4. Press Enter and copy the returned token

### Configuration Options

The `config.json` file contains the following settings:

```json
{
    "discord_token": "YOUR_DISCORD_TOKEN_HERE",
    "muted_servers": [server_id_1, server_id_2],
    "muted_channels": [channel_id_1, channel_id_2],
    "settings": {
        "tts_enabled": true,
        "tts_rate": 150,
        "tts_volume": 0.8,
        "sound_enabled": true,
        "notifications_enabled": true,
        "auto_open_discord": false
    }
}
```

**Configuration Details:**
- **discord_token**: Your Discord user account token
- **muted_servers**: List of server IDs to ignore (right-click server → Copy Server ID)
- **muted_channels**: List of channel IDs to ignore (right-click channel → Copy Channel ID)
- **tts_enabled**: Enable/disable text-to-speech announcements
- **tts_rate**: Speech speed in words per minute (100-300)
- **tts_volume**: Speech volume level (0.0 to 1.0)
- **sound_enabled**: Enable/disable sound notifications
- **notifications_enabled**: Enable/disable Windows toast notifications
- **auto_open_discord**: Automatically open Discord when airdrop detected

3. (Optional) Customize other settings in `config.json`

4. Run the notifier:
```bash
python airdropnotif.py
```

Or use the provided batch file:
```bash
run_windows.bat
```

## Building a Standalone Executable

You can create a self-contained executable that doesn't require Python to be installed on the target machine.

### Prerequisites for Building
- Windows OS
- Python 3.7+ installed
- All dependencies installed (`pip install -r requirements.txt`)

### Build Process

1. **Configure your Discord token** in `config.json` before building
2. **Run the build script**:
```bash
build_exe.bat
```

This will:
- Create a build virtual environment
- Install all required dependencies including PyInstaller
- Clean previous build artifacts
- Generate `DiscordAirdropNotifier.exe` in the `dist/` folder

### Build Output

- **Executable**: `dist/DiscordAirdropNotifier.exe` (~50-80MB)
- **Self-contained**: Includes Python, all libraries, and the audio file
- **No installation required**: Can run on any Windows machine
- **Portable**: Single file that can be distributed

### Important Notes for Executable

⚠️ **Security Warning**: The Discord token will be embedded in the executable. Never distribute an executable with your personal token.

📋 **Config File**: The executable will look for `config.json` in the same directory. If not found, it will create one from the bundled template.

🔧 **Build Requirements**:
- Building requires ~200MB of disk space
- Build process takes 2-5 minutes depending on your system
- Antivirus software may interfere with PyInstaller (temporarily disable if needed)

📁 **Distribution**: You only need to distribute the `.exe` file - the audio files and all dependencies are bundled inside.

## Audio Configuration

The notifier includes a bundled `cash-register-05.wav` file in the `audio/` directory. If this file is not found, it automatically falls back to Windows system notification sounds.

## Supported Cryptocurrencies

The bot detects airdrops for: BTC, LTC, DOGE, EOS, TRX, USDT, ETH, XNO, BCH, USDC, SHIB, MATIC, XRP, XLM, SOL

## Important Notes

⚠️ **This uses a regular Discord user account (not a bot token) which may violate Discord's Terms of Service. Use at your own risk.**

The application is designed to monitor only (never posts messages) but Discord's automation policies still apply.
