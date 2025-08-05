# Free Proxy Telegram Bot

A Telegram bot that provides free proxies from the [Proxy-Master](https://github.com/MuRongPIG/Proxy-Master) repository.

## Features

- Get random HTTP proxies
- Get random SOCKS5 proxies
- Get random proxies of any type
- Fancy formatted messages with proxy details
- Easy to use commands
- Secure environment variable management

## Setup

1. Clone this repository:
```bash
git clone <your-repo-url>
cd <your-repo-name>
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
   - Create a `.env` file in the root directory
   - Add your Telegram bot token (get it from [@BotFather](https://t.me/botfather) on Telegram):
   ```
   TELEGRAM_BOT_TOKEN=your_bot_token_here
   ```
   - The `.env` file is automatically ignored by git to keep your secrets safe
   - Never commit your actual `.env` file to version control

4. Run the bot:
```bash
python bot.py
```

## Running as a System Service

To run the bot as a systemd service on Linux:

1. Create the service file:
```bash
sudo nano /etc/systemd/system/free_vpn_bot.service
```

2. Add the following content (adjust paths according to your setup):
```ini
[Unit]
Description=Free VPN Telegram Bot Service
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/your/bot
Environment=PATH=/path/to/your/bot/venv/bin
ExecStart=/path/to/your/bot/venv/bin/python bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

3. Set up the service:
```bash
# Reload systemd daemon
sudo systemctl daemon-reload

# Enable service to start on boot
sudo systemctl enable free_vpn_bot.service

# Start the service
sudo systemctl start free_vpn_bot.service
```

4. Useful commands:
```bash
# Check service status
sudo systemctl status free_vpn_bot.service

# View logs
journalctl -u free_vpn_bot.service -f

# Stop service
sudo systemctl stop free_vpn_bot.service

# Restart service
sudo systemctl restart free_vpn_bot.service
```

## Usage

The bot supports the following commands:

- `/start` - Display welcome message and available commands
- `/http` - Get a random HTTP proxy
- `/socks5` - Get a random SOCKS5 proxy
- `/any` - Get any random proxy (either HTTP or SOCKS5)

## Security Notes

- Keep your `.env` file secure and never share it
- Don't commit the `.env` file to version control
- If you suspect your bot token has been compromised, generate a new one with @BotFather

## Credits

This bot uses proxy lists from [MuRongPIG/Proxy-Master](https://github.com/MuRongPIG/Proxy-Master).

## License

MIT License 