from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def settings_keyboard(settings):
    def row(key, options):
        return [InlineKeyboardButton(f"{key.upper()}: {val}" + (" ✅" if settings[key] == val else ""), callback_data=f"set_{key}_{val}") for val in options]

    keyboard = [
        row("crf", ["18", "23", "28"]),
        row("codec", ["libx264", "libx265"]),
        row("preset", ["ultrafast", "medium", "slow"]),
        row("resolution", ["480p", "720p", "1080p"]),
        row("fontsize", ["16", "24", "32"]),
        [InlineKeyboardButton("✅ Start Encoding", callback_data="start_encode")]
    ]
    return InlineKeyboardMarkup(keyboard)
