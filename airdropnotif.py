import discord  # install 'discord.py-self', not 'discord'
import os
import re
import sys
import subprocess
import webbrowser
import platform
import json
import shutil

from rich import print
from rich.text import Text
from rich.console import Console

# Windows-specific imports
try:
    import winsound  # For playing sounds on Windows
    import win32api  # For Windows notifications (install pywin32)
    from plyer import notification  # Cross-platform notifications (install plyer)
    import pyttsx3  # Text-to-speech for Windows (install pyttsx3)
except ImportError as e:
    print(f"[red]Missing Windows dependencies: {e}")
    print("[yellow]Please install required packages:")
    print("pip install pywin32 plyer pyttsx3")
    sys.exit(1)

console = Console(soft_wrap=False)

#import logging
#logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

def load_config():
    """Load configuration from config.json file"""
    config_file = 'config.json'
    template_file = 'config.json.template'
    
    # Check if config file exists, if not create from template
    if not os.path.exists(config_file):
        if os.path.exists(template_file):
            print(f"[yellow]Config file not found. Creating {config_file} from template...")
            shutil.copy(template_file, config_file)
            print(f"[red]Please edit {config_file} and add your Discord token before running again!")
            sys.exit(1)
        else:
            print(f"[red]Neither {config_file} nor {template_file} found!")
            print("[yellow]Creating default config file...")
            default_config = {
                "discord_token": "YOUR_DISCORD_TOKEN_HERE",
                "muted_servers": [587764595888881670, 110175050006577152, 889596056550125608],
                "muted_channels": [],
                "settings": {
                    "tts_enabled": True,
                    "tts_rate": 150,
                    "tts_volume": 0.8,
                    "sound_enabled": True,
                    "notifications_enabled": True,
                    "auto_open_discord": False
                }
            }
            with open(config_file, 'w') as f:
                json.dump(default_config, f, indent=4)
            print(f"[red]Please edit {config_file} and add your Discord token before running again!")
            sys.exit(1)
    
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        # Validate required fields
        if config.get('discord_token') == 'YOUR_DISCORD_TOKEN_HERE' or not config.get('discord_token'):
            print(f"[red]Please set your Discord token in {config_file}")
            sys.exit(1)
        
        return config
    except json.JSONDecodeError as e:
        print(f"[red]Error parsing {config_file}: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"[red]Error loading config: {e}")
        sys.exit(1)

# Load configuration
config = load_config()
discord_token = config['discord_token']
muted_servers = set(config.get('muted_servers', []))
muted_channels = set(config.get('muted_channels', []))

class MyClient(discord.Client):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Load settings from config
        self.settings = config.get('settings', {})
        
        # Initialize text-to-speech engine
        if self.settings.get('tts_enabled', True):
            try:
                self.tts_engine = pyttsx3.init()
                self.tts_engine.setProperty('rate', self.settings.get('tts_rate', 150))
                self.tts_engine.setProperty('volume', self.settings.get('tts_volume', 0.8))
            except:
                self.tts_engine = None
                print("[yellow]Warning: Text-to-speech not available")
        else:
            self.tts_engine = None
            print("[cyan]Text-to-speech disabled in config")

    async def on_ready(self):
        # Set window title (Windows command)
        os.system('title "tip.cc airdrop notifier: not a bot"')
        banner = f"""[dark_orange]
  ████████╗██╗██████╗  ██████╗ ██████╗     █████╗ ██╗██████╗ ██████╗ ██████╗  ██████╗ ██████╗
  ╚══██╔══╝██║██╔══██╗██╔════╝██╔════╝    ██╔══██╗██║██╔══██╗██╔══██╗██╔══██╗██╔═══██╗██╔══██╗
     ██║   ██║██████╔╝██║     ██║         ███████║██║██████╔╝██║  ██║██████╔╝██║   ██║██████╔╝
     ██║   ██║██╔═══╝ ██║     ██║         ██╔══██║██║██╔══██╗██║  ██║██╔══██╗██║   ██║██╔═══╝
     ██║   ██║██║██╗  ╚██████╗╚██████╗    ██║  ██║██║██║  ██║██████╔╝██║  ██║╚██████╔╝██║
     ╚═╝   ╚═╝╚═╝╚═╝   ╚═════╝ ╚═════╝    ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝

                   ███╗   ██╗ ██████╗ ████████╗██╗███████╗██╗███████╗██████╗
                   ████╗  ██║██╔═══██╗╚══██╔══╝██║██╔════╝██║██╔════╝██╔══██╗
                   ██╔██╗ ██║██║   ██║   ██║   ██║█████╗  ██║█████╗  ██████╔╝
                   ██║╚██╗██║██║   ██║   ██║   ██║██╔══╝  ██║██╔══╝  ██╔══██╗
                   ██║ ╚████║╚██████╔╝   ██║   ██║██║     ██║███████╗██║  ██║
                   ╚═╝  ╚═══╝ ╚═════╝    ╚═╝   ╚═╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝
                  Created by @brokechubb on Discord  |  https://t.me/codestats2
                        SOL: FVDejAWbUGsgnziRvFi4eGkJZuH6xuLviuTdi2g4Ut3o
        [/dark_orange]"""
        print(banner)
        print(f'[yellow]Logged on as {self.user.name}! (Windows Version)[/yellow]')

    def play_notification_sound(self):
        """Play notification sound on Windows"""
        if not self.settings.get('sound_enabled', True):
            return
            
        try:
            # Try to play the bundled sound file if it exists
            script_dir = os.path.dirname(os.path.abspath(__file__))
            bundled_sound_path = os.path.join(script_dir, "audio", "cash-register-05.wav")
            
            if os.path.exists(bundled_sound_path):
                winsound.PlaySound(bundled_sound_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
            else:
                # Fall back to system sound if bundled audio not found
                print(f"[yellow]Bundled audio file not found at: {bundled_sound_path}")
                print("[yellow]Using system sound instead")
                winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS | winsound.SND_ASYNC)
        except Exception as e:
            print(f"[yellow]Warning: Could not play sound: {e}")

    def speak_text(self, text):
        """Use text-to-speech to announce the airdrop"""
        if self.tts_engine and self.settings.get('tts_enabled', True):
            try:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            except Exception as e:
                print(f"[yellow]Warning: Text-to-speech failed: {e}")

    def show_windows_notification(self, title, message, discord_uri):
        """Show Windows toast notification"""
        if not self.settings.get('notifications_enabled', True):
            return
            
        try:
            # Use plyer for cross-platform notifications
            notification.notify(
                title=title,
                message=message,
                app_name="Discord Airdrop",
                timeout=30,  # 30 seconds
                toast=True
            )
            
            # Also try to use Windows native notifications if available
            try:
                import win32gui
                import win32con
                # Show a simple message box as backup
                result = win32gui.MessageBox(0, 
                                           f"{message}\n\nClick OK to open Discord", 
                                           title, 
                                           win32con.MB_OKCANCEL | win32con.MB_ICONINFORMATION | win32con.MB_TOPMOST)
                if result == win32con.IDOK or self.settings.get('auto_open_discord', False):
                    # Open Discord URI
                    webbrowser.open(discord_uri)
            except:
                # Auto-open if enabled and message box failed
                if self.settings.get('auto_open_discord', False):
                    webbrowser.open(discord_uri)
                
        except Exception as e:
            print(f"[yellow]Warning: Could not show notification: {e}")
            # Fallback: just print to console
            print(f"[bold cyan]NOTIFICATION: {title}")
            print(f"[cyan]{message}")

    async def on_message(self, message):
        if message.guild:  # Check if the message is from a guild
            guild_id = message.guild.id
            message_txt = message.content
            user = message.author.name
            if guild_id not in muted_servers and message.channel.id not in muted_channels:
                console.print(f'  [bright_black]{message.guild.name} (#{message.channel.name})[/bright_black]')
                console.print(f'[magenta]>> [/magenta][orange1]{message.author.name}[/orange1][bright_black]:[/bright_black] {message.content}')
                if message.content.startswith('$airdrop') or message.content.startswith('$triviadrop'):
                    good_coins = r"\b(ltc|LTC|btc|BTC|D$|Ð|doge|DOGE|d|D|eos|EOS|trx|TRX|usdt|USDT|eth|ETH|xno|XNO|bch|BCH|usdc|USDC|shib|SHIB|matic|MATIC|xrp|XRP|xlm|XLM|sol|SOL)\b"
                    thats_money = re.search(good_coins, message.content)
                    if thats_money:
                        print(f'[bold][bright_red]----------------- AIRDROP DETECTED -----------------[/bright_red]')

                        # Text-to-speech announcement
                        self.speak_text("An airdrop appears")
                        
                        # Play notification sound
                        self.play_notification_sound()

                        # Construct the Discord message URI using the discord:// scheme
                        discord_message_uri = f"discord://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id}"

                        # Show Windows notification
                        notification_title = "Discord Airdrop Detected!"
                        notification_message = f"{user}: {message_txt}\n{message.guild.name} (#{message.channel.name})"
                        
                        self.show_windows_notification(notification_title, notification_message, discord_message_uri)

                        try:
                            # Automatically open Discord (optional - comment out if you don't want this)
                            # webbrowser.open(discord_message_uri)
                            print(f"[cyan]Discord URI: {discord_message_uri}")
                            
                        except Exception as e:
                            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    print("[cyan]Starting Discord Airdrop Notifier (Windows Version)...")
    print("[yellow]Make sure you have installed required dependencies:")
    print("pip install discord.py-self rich pywin32 plyer pyttsx3")
    print()
    
    client = MyClient()
    client.run(discord_token)
