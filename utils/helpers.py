from telethon import Button
from config.settings import (
    CODEC_OPTIONS, CRF_OPTIONS, RESOLUTION_OPTIONS,
    QUALITY_OPTIONS, PRESET_OPTIONS, BIT_DEPTH_OPTIONS
)

async def get_settings_markup(user_id, client, user_settings):
    """Generate inline keyboard for settings (without font options)"""
    settings = user_settings.get(user_id, DEFAULT_SETTINGS)
    
    buttons = [
        [Button.inline(f"Codec: {settings['codec']}", b'set_codec')],
        [Button.inline(f"CRF: {settings['crf']}", b'set_crf')],
        [Button.inline(f"Resolution: {settings['resolution']}", b'set_resolution')],
        [Button.inline(f"Quality: {settings['quality']}", b'set_quality')],
        [Button.inline(f"Preset: {settings['preset']}", b'set_preset')],
        [Button.inline(f"Bit Depth: {settings['bit_depth']}-bit", b'set_bitdepth')],
        [Button.inline("Apply These Settings", b'apply_settings')],
        [Button.inline("Reset to Default", b'reset_settings')]
    ]
    
    return buttons
