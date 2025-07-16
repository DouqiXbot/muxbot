# Font configuration
FONT_URL = "https://github.com/DevXkirito/Vidburner/raw/main/fonts/HelveticaRounded-Bold.ttf"
FONT_FILENAME = "HelveticaRounded-Bold.ttf"

# Default settings for the bot
DEFAULT_SETTINGS = {
    'codec': 'libx264',
    'crf': '23',
    'resolution': 'original',
    'quality': 'medium',
    'preset': 'medium',
    'bit_depth': '8'
}

# Available options (removed font options)
CODEC_OPTIONS = {
    'libx264': {'bit_depth': ['8']},
    'libx265': {'bit_depth': ['8', '10']},
    'libvpx': {'bit_depth': ['8']},
    'libvpx-vp9': {'bit_depth': ['8', '10']}
}
CRF_OPTIONS = ['18', '23', '28', '33']
RESOLUTION_OPTIONS = ['original', '1080p', '720p', '480p']
QUALITY_OPTIONS = ['low', 'medium', 'high', 'very high']
PRESET_OPTIONS = ['ultrafast', 'superfast', 'veryfast', 'faster', 'fast', 'medium', 'slow', 'slower', 'veryslow']
BIT_DEPTH_OPTIONS = ['8', '10']
