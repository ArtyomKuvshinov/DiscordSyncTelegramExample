# FormFun

This project is a bridge bot that forwards messages and media between a Telegram group and a Discord channel. It uses `aiogram` for the Telegram bot and `discord.py` for the Discord bot.

## Features

- Forwards text messages from Telegram to Discord and vice versa.
- Forwards media files (photos, stickers, animations) from Telegram to Discord.
- Forwards media attachments from Discord to Telegram.

## Requirements

- Python 3.8 or higher

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/ArtyomKuvshinov/DiscordSyncTelegramExample.git
    cd DiscordSyncTelegramExample
    ```

2. Create and activate a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up your environment variables::

    ```bash
    export DISCORD_BOT_TOKEN='your-discord-bot-token'
    export TELEGRAM_BOT_TOKEN='your-telegram-bot-token'
    export DISCORD_CHANNEL_ID='your-discord-channel-id'
    export TELEGRAM_GROUP_ID='your-telegram-group-id'
    ```

## Usage

Run the bot with:

```bash
python main.py
```
