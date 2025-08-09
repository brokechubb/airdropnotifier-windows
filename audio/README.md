# Audio Files

This directory contains audio files used by the Discord Airdrop Notifier for sound notifications.

## Included Files

- `cash-register-05.wav` - Default notification sound that plays when an airdrop is detected

## How It Works

The airdrop notifier will automatically:
1. Look for `cash-register-05.wav` in this directory
2. Play this file when an airdrop is detected (using Windows `winsound` module)
3. If the file is not found, fall back to Windows system notification sound ("SystemExclamation")

## Customization

You can replace `cash-register-05.wav` with your own audio file:
- Keep the same filename: `cash-register-05.wav`
- Use WAV format for best Windows compatibility
- Recommended duration: 1-3 seconds for quick notifications

## Troubleshooting

If audio doesn't play:
- Ensure the file exists in this directory
- Check that your system audio is not muted
- Verify the WAV file is not corrupted
- The system will show a yellow warning message if audio fails
