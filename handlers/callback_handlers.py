from telethon import events, Button
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
    
    # Get current settings or default
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
