from telethon import Button
from config.settings import (
    CODEC_OPTIONS, CRF_OPTIONS, RESOLUTION_OPTIONS,
    QUALITY_OPTIONS, PRESET_OPTIONS, BIT_DEPTH_OPTIONS, DEFAULT_SETTINGS
)
from utils.helpers import get_settings_markup
from constants import ERROR_MESSAGES
from database.db import db


async def settings_back_handler(event, client):
    """Handle back button in settings"""
    user_id = event.sender_id
    current_settings = db.get_settings(user_id) or DEFAULT_SETTINGS
    await event.edit(
        "⚙️ Settings:",
        buttons=await get_settings_markup(user_id, client, {user_id: current_settings})
    )


async def apply_settings_handler(event):
    """Handle apply settings button"""
    await event.answer(ERROR_MESSAGES['settings_applied'], alert=False)


async def reset_settings_handler(event, client):
    """Handle reset settings button"""
    user_id = event.sender_id
    db.put_settings(user_id, DEFAULT_SETTINGS)
    await event.edit(
        ERROR_MESSAGES['settings_reset'],
        buttons=await get_settings_markup(user_id, client, {user_id: DEFAULT_SETTINGS})
    )


async def generic_setting_handler(event, client, setting_type):
    """Generic handler for setting changes"""
    user_id = event.sender_id
    data = event.data.decode('utf-8')

    current_settings = db.get_settings(user_id) or DEFAULT_SETTINGS.copy()

    setting_map = {
        'codec': ('codec_', 'codec'),
        'crf': ('crf_', 'crf'),
        'resolution': ('resolution_', 'resolution'),
        'quality': ('quality_', 'quality'),
        'preset': ('preset_', 'preset'),
        'bitdepth': ('bitdepth_', 'bit_depth')
    }

    prefix, setting_key = setting_map[setting_type]

    if data.startswith(prefix):
        new_value = data[len(prefix):]
        current_settings[setting_key] = new_value
        db.put_settings(user_id, current_settings)
        await event.edit(
            f"✅ `{setting_key.replace('_', ' ').title()}` set to: `{new_value}`",
            buttons=await get_settings_markup(user_id, client, {user_id: current_settings})
        )


# === Specific Setting Handlers with ✅ Buttons ===

async def set_codec_handler(event, client):
    user_id = event.sender_id
    current_settings = db.get_settings(user_id) or DEFAULT_SETTINGS.copy()

    buttons = []
    for codec in CODEC_OPTIONS:
        label = f"{codec}" + (" ✅" if current_settings.get('codec') == codec else "")
        buttons.append([Button.inline(label, f"codec_{codec}".encode())])

    buttons.append([Button.inline("⬅️ Back", b'settings_back')])

    await event.edit("🎞 Choose Codec:", buttons=buttons)


async def set_crf_handler(event, client):
    user_id = event.sender_id
    current_settings = db.get_settings(user_id) or DEFAULT_SETTINGS.copy()

    buttons = []
    for crf in CRF_OPTIONS:
        label = f"CRF {crf}" + (" ✅" if current_settings.get('crf') == crf else "")
        buttons.append([Button.inline(label, f"crf_{crf}".encode())])

    buttons.append([Button.inline("⬅️ Back", b'settings_back')])

    await event.edit("🎚 Choose CRF (Quality Factor):", buttons=buttons)


async def set_resolution_handler(event, client):
    user_id = event.sender_id
    current_settings = db.get_settings(user_id) or DEFAULT_SETTINGS.copy()

    buttons = []
    for res in RESOLUTION_OPTIONS:
        label = res.upper() + (" ✅" if current_settings.get('resolution') == res else "")
        buttons.append([Button.inline(label, f"resolution_{res}".encode())])

    buttons.append([Button.inline("⬅️ Back", b'settings_back')])

    await event.edit("📐 Choose Resolution:", buttons=buttons)


async def set_quality_handler(event, client):
    user_id = event.sender_id
    current_settings = db.get_settings(user_id) or DEFAULT_SETTINGS.copy()

    buttons = []
    for quality in QUALITY_OPTIONS:
        label = quality.title() + (" ✅" if current_settings.get('quality') == quality else "")
        buttons.append([Button.inline(label, f"quality_{quality}".encode())])

    buttons.append([Button.inline("⬅️ Back", b'settings_back')])

    await event.edit("🎛 Choose Encoding Quality:", buttons=buttons)


async def set_preset_handler(event, client):
    user_id = event.sender_id
    current_settings = db.get_settings(user_id) or DEFAULT_SETTINGS.copy()

    buttons = []
    for preset in PRESET_OPTIONS:
        label = preset.title() + (" ✅" if current_settings.get('preset') == preset else "")
        buttons.append([Button.inline(label, f"preset_{preset}".encode())])

    buttons.append([Button.inline("⬅️ Back", b'settings_back')])

    await event.edit("⚡️ Choose Encoding Speed (Preset):", buttons=buttons)


async def set_bit_depth_handler(event, client):
    user_id = event.sender_id
    current_settings = db.get_settings(user_id) or DEFAULT_SETTINGS.copy()

    buttons = []
    for depth in BIT_DEPTH_OPTIONS:
        label = f"{depth}-bit" + (" ✅" if current_settings.get('bit_depth') == depth else "")
        buttons.append([Button.inline(label, f"bitdepth_{depth}".encode())])

    buttons.append([Button.inline("⬅️ Back", b'settings_back')])

    await event.edit("🧠 Choose Bit Depth:", buttons=buttons)
