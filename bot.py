import os
from pyrogram import Client
from handlers import message_handlers, callback_handlers
from database.db import init_db

API_ID = int(os.getenv("API_ID", "1234567"))
API_HASH = os.getenv("API_HASH", "your_api_hash")
BOT_TOKEN = os.getenv("BOT_TOKEN", "your_bot_token")

app = Client("subtitle_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

message_handlers.register(app)
callback_handlers.register(app)
init_db()

if __name__ == "__main__":
    os.makedirs("downloads", exist_ok=True)
    os.makedirs("fonts", exist_ok=True)
    app.run()
