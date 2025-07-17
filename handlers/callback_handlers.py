from pyrogram import filters
from pyrogram.types import CallbackQuery
from utils.keyboards import settings_keyboard
from utils.ffmpeg_utils import process_video
from handlers.message_handlers import user_files
from database.db import get_user_settings, save_user_settings

def register(app):
    @app.on_callback_query(filters.regex(r"^set_(\w+)_(.+)"))
    async def update_setting(client, query: CallbackQuery):
        user_id = str(query.from_user.id)
        key, value = query.data.split("_", 2)[1:]
        settings = get_user_settings(user_id)
        settings[key] = value
        save_user_settings(user_id, settings)
        await query.edit_message_reply_markup(reply_markup=settings_keyboard(settings))

    @app.on_callback_query(filters.regex("start_encode"))
    async def encode(client, query: CallbackQuery):
        user_id = str(query.from_user.id)
        await query.message.reply("Encoding started...")
        await process_video(client, query.message.chat.id, user_files[user_id], get_user_settings(user_id))
