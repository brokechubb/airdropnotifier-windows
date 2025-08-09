# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['airdropnotif.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('audio/cash-register-05.wav', 'audio'),
        ('audio/README.md', 'audio'),
        ('config.json.template', '.'),
    ],
    hiddenimports=[
        'discord',
        'discord.ext',
        'discord.ext.commands',
        'win32api',
        'win32gui',
        'win32con',
        'winsound',
        'plyer.platforms.win.notification',
        'pyttsx3.drivers',
        'pyttsx3.drivers.sapi5',
        'rich.console',
        'rich.text',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='DiscordAirdropNotifier',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # You can add an .ico file here if you have one
)
