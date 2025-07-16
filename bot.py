import os
from telethon import TelegramClient, events
from handlers import (
    message_handlers,
    callback_handlers
)
from database.db import db
from config.settings import DEFAULT_SETTINGS

# Bot configuration
API_ID = id  # Replace with your API ID
API_HASH = 'hash'  # Replace with your API hash
BOT_TOKEN = 'Token'  # Replace with your bot token

# Initialize the client
client = TelegramClient('hardmux_bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)


# === COMMAND HANDLERS ===

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await message_handlers.start_handler(event, client)

@client.on(events.NewMessage(pattern='/settings'))
async def settings_command(event):
    """Manual command to open settings menu"""
    await message_handlers.settings_command_handler(event, client)


# === FILE HANDLERS ===

# ✅ Handle video files: .mp4 and .mkv
@client.on(events.NewMessage(func=lambda e: e.file and e.file.name and e.file.name.lower().endswith(('.mp4', '.mkv'))))
async def video(event):
    await message_handlers.video_handler(event, client)

# ✅ Handle subtitle files: .srt and .ass
@client.on(events.NewMessage(func=lambda e: e.file and e.file.name and e.file.name.lower().endswith(('.srt', '.ass'))))
async def subtitle(event):
    await message_handlers.subtitle_handler(event, client)


# === CALLBACK BUTTONS ===

@client.on(events.CallbackQuery(data=b'settings_back'))
async def settings_back(event):
    await callback_handlers.settings_back_handler(event, client)

@client.on(events.CallbackQuery(data=b'apply_settings'))
async def apply_settings(event):
    await callback_handlers.apply_settings_handler(event)

@client.on(events.CallbackQuery(data=b'reset_settings'))
async def reset_settings(event):
    await callback_handlers.reset_settings_handler(event, client)

@client.on(events.CallbackQuery(data=b'set_codec'))
async def set_codec(event):
    await callback_handlers.set_codec_handler(event, client)

@client.on(events.CallbackQuery(data=b'set_crf'))
async def set_crf(event):
    await callback_handlers.set_crf_handler(event, client)

@client.on(events.CallbackQuery(data=b'set_resolution'))
async def set_resolution(event):
    await callback_handlers.set_resolution_handler(event, client)

@client.on(events.CallbackQuery(data=b'set_quality'))
async def set_quality(event):
    await callback_handlers.set_quality_handler(event, client)

@client.on(events.CallbackQuery(data=b'set_preset'))
async def set_preset(event):
    await callback_handlers.set_preset_handler(event, client)

@client.on(events.CallbackQuery(data=b'set_bitdepth'))
async def set_bitdepth(event):
    await callback_handlers.set_bit_depth_handler(event, client)


# === SETTING VALUE CALLBACKS ===

@client.on(events.CallbackQuery())
async def callback(event):
    data = event.data.decode('utf-8')
    if data.startswith('codec_'):
        await callback_handlers.generic_setting_handler(event, client, 'codec')
    elif data.startswith('crf_'):
        await callback_handlers.generic_setting_handler(event, client, 'crf')
    elif data.startswith('resolution_'):
        await callback_handlers.generic_setting_handler(event, client, 'resolution')
    elif data.startswith('quality_'):
        await callback_handlers.generic_setting_handler(event, client, 'quality')
    elif data.startswith('preset_'):
        await callback_handlers.generic_setting_handler(event, client, 'preset')
    elif data.startswith('bitdepth_'):
        await callback_handlers.generic_setting_handler(event, client, 'bitdepth')


# === RUN THE BOT ===

if __name__ == '__main__':
    print("Bot started...")
    client.run_until_disconnected()
