import os
from telethon import TelegramClient, events
from handlers import message_handlers, callback_handlers
from database.db import db

# Bot configuration
API_ID = 123456  # Replace with your actual API ID
API_HASH = 'your_api_hash_here'  # Replace with your actual API hash
BOT_TOKEN = 'your_bot_token_here'  # Replace with your bot token

# Initialize the client
client = TelegramClient('hardmux_bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# /start command
@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await message_handlers.start_handler(event, client)

# /settings command (manual open settings)
@client.on(events.NewMessage(pattern='/settings'))
async def settings_command(event):
    await message_handlers.settings_command_handler(event, client)

# Handle video files (.mp4, .mkv)
@client.on(events.NewMessage(func=lambda e: e.file and e.file.name and e.file.name.lower().endswith(('.mp4', '.mkv'))))
async def video(event):
    await message_handlers.video_handler(event, client)

# Handle subtitle files (.srt, .ass)
@client.on(events.NewMessage(func=lambda e: e.file and e.file.name and e.file.name.lower().endswith(('.srt', '.ass'))))
async def subtitle(event):
    await message_handlers.subtitle_handler(event, client)

# Callback for back from settings
@client.on(events.CallbackQuery(data=b'settings_back'))
async def settings_back(event):
    await callback_handlers.settings_back_handler(event, client)

# Apply current settings
@client.on(events.CallbackQuery(data=b'apply_settings'))
async def apply_settings(event):
    await callback_handlers.apply_settings_handler(event)

# Reset to default settings
@client.on(events.CallbackQuery(data=b'reset_settings'))
async def reset_settings(event):
    await callback_handlers.reset_settings_handler(event, client)

# Set bit depth
@client.on(events.CallbackQuery(data=b'set_bitdepth'))
async def set_bitdepth(event):
    await callback_handlers.generic_setting_handler(event, client, 'bitdepth')

# Generic callback for all other settings
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

# Run the bot
if __name__ == '__main__':
    print("🤖 Bot started...")
    client.run_until_disconnected()
