from pyrogram import filters
from pyrogram.types import Message
from utils.keyboards import settings_keyboard
from database.db import get_user_settings, save_user_settings
import os

user_files = {}

def register(app):
    @app.on_message(filters.video)
    async def handle_video(client, message: Message):
        user_id = str(message.from_user.id)
        user_files[user_id] = {"video": message.video.file_id}
        await message.reply("Video received. Now send subtitle (.srt) file")

    @app.on_message(filters.document & filters.document.mime_type("text/plain"))
    async def handle_subtitle(client, message: Message):
        user_id = str(message.from_user.id)
        if user_id not in user_files:
            await message.reply("Send a video first.")
            return
        user_files[user_id]["subtitle"] = message.document.file_id
        settings = get_user_settings(user_id) or {
            "crf": "23", "codec": "libx264", "preset": "medium",
            "resolution": "720p", "fontsize": "24"
        }
        save_user_settings(user_id, settings)
        await message.reply("Files received. Choose settings:", reply_markup=settings_keyboard(settings))
