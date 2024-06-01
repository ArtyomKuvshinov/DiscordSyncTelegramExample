import config
import asyncio
import aiohttp

from aiogram import Bot, Dispatcher, types
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import URLInputFile

import discord
from discord.ext import commands

# Telegram Bot Setup
tbot = Bot(token=config.TELEGRAM_BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# Discord Bot Setup
intents = discord.Intents.default()
intents.message_content = True
dclient = commands.Bot(command_prefix='!', intents=intents)

async def send_media_to_discord(channel, username, avatar_url, media_url=None, content=""):
    webhook = await channel.create_webhook(name=username)
    async with aiohttp.ClientSession() as session:
        webhook_send = discord.Webhook.from_url(webhook.url, session=session)
        await webhook_send.send(
            content=media_url if media_url else content,
            username=username,
            avatar_url=avatar_url if avatar_url else None
        )
    await webhook.delete()

async def get_avatar_url(user_id):
    user_photos = await tbot.get_user_profile_photos(user_id, limit=1)
    if user_photos.total_count > 0:
        file_id = user_photos.photos[0][0].file_id
        file = await tbot.get_file(file_id)
        return f"https://api.telegram.org/file/bot{config.TELEGRAM_BOT_TOKEN}/{file.file_path}"
    return None

@dp.message()
async def handle_telegram_message(message: types.Message):
    if message.chat.id != config.TELEGRAM_GROUP_ID:
        return

    channel = dclient.get_channel(config.DISCORD_CHANNEL_ID)
    if not channel:
        return

    avatar_url = await get_avatar_url(message.from_user.id)

    # Handle text
    if message.text:
        await send_media_to_discord(channel, message.from_user.full_name, avatar_url, content=message.text)
    if message.caption:
        await send_media_to_discord(channel, message.from_user.full_name, avatar_url, content=message.caption)

    # Handle media
    if message.photo:
        file_id = message.photo[-1].file_id
        file = await tbot.get_file(file_id)
        media_url = f"https://api.telegram.org/file/bot{config.TELEGRAM_BOT_TOKEN}/{file.file_path}"
        await send_media_to_discord(channel, message.from_user.full_name, avatar_url, media_url)
    if message.sticker:
        file_id = message.sticker.file_id
        file = await tbot.get_file(file_id)
        media_url = f"https://api.telegram.org/file/bot{config.TELEGRAM_BOT_TOKEN}/{file.file_path}"
        await send_media_to_discord(channel, message.from_user.full_name, avatar_url, media_url)
    if message.animation:
        file_id = message.animation.file_id
        file = await tbot.get_file(file_id)
        media_url = f"https://api.telegram.org/file/bot{config.TELEGRAM_BOT_TOKEN}/{file.file_path}"
        await send_media_to_discord(channel, message.from_user.full_name, avatar_url, media_url)

@dclient.event
async def on_ready():
    print(f'Discord bot has logged in')

@dclient.event
async def on_message(message):
    if message.author == dclient.user or message.webhook_id:
        return

    if message.channel.id == config.DISCORD_CHANNEL_ID:
        if message.content:
            await tbot.send_message(
                config.TELEGRAM_GROUP_ID,
                f"<b>{message.author.name}:</b>\n{message.content}"
            )

        #Send media
        for attachment in message.attachments:
            async with aiohttp.ClientSession() as session:
                async with session.get(attachment.url) as resp:
                    if resp.status == 200:
                        data = URLInputFile(
                            attachment.url,
                            filename="attachment.png"
                        )
                        await tbot.send_photo(config.TELEGRAM_GROUP_ID, data, caption=f"<b>{message.author.name}:</b>")

    await dclient.process_commands(message)

# Launching
async def telegram_main():
    await dp.start_polling(tbot)

async def main():
    await asyncio.gather(
        telegram_main(),
        dclient.start(config.DISCORD_BOT_TOKEN)
    )

if __name__ == '__main__':
    asyncio.run(main())