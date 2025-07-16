import os
import shutil
from telethon import Button
from config.settings import (
    CODEC_OPTIONS, CRF_OPTIONS, RESOLUTION_OPTIONS,
    QUALITY_OPTIONS, PRESET_OPTIONS, BIT_DEPTH_OPTIONS
)

# Use the first valid value from each list/dict
DEFAULT_SETTINGS = {
    "codec": next(iter(CODEC_OPTIONS)),           # Gets 'libx264'
    "crf": CRF_OPTIONS[1],                         # '23'
    "resolution": RESOLUTION_OPTIONS[0],           # 'original'
    "quality": QUALITY_OPTIONS[1],                 # 'medium'
    "preset": PRESET_OPTIONS[5],                   # 'medium'
    "bit_depth": BIT_DEPTH_OPTIONS[0]              # '8'
}

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

def clean_temp_files(temp_dir='downloads'):
    """Remove all files and folders inside the temp_dir."""
    if os.path.exists(temp_dir):
        for filename in os.listdir(temp_dir):
            file_path = os.path.join(temp_dir, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")
