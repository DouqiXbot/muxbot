# Constants for the bot
TEMP_FILE_PREFIX = "temp_"
OUTPUT_FILE_PREFIX = "output_"

# Messages
WELCOME_MESSAGE = """
Welcome to Hardmux Bot! Send me a video file and a subtitle file to hardmux them together.

You can customize the settings below:
"""

ERROR_MESSAGES = {
    'no_video': "Please send the video file first.",
    'processing': "Processing your request...",
    'error': "Error processing video: {}",
    'success': "Here's your video with hardmuxed subtitles!",
    'settings_applied': "Settings applied!",
    'settings_reset': "Settings reset to default."
}
