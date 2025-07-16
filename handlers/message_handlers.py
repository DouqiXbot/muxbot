import os
import time
from telethon import events, Button
from telethon.tl.types import DocumentAttributeVideo
from handlers.video_processing import process_video
from utils.helpers import get_settings_markup, clean_temp_files
from utils.progress import progress_bar
from config.settings import DEFAULT_SETTINGS
from constants import TEMP_FILE_PREFIX, OUTPUT_FILE_PREFIX, ERROR_MESSAGES, WELCOME_MESSAGE
from database.db import db

async def download_with_progress(client, event, file_path, download_type):
    """Download file with progress updates"""
    start_time = time.time()
    progress_message = await event.reply(f"Starting {download_type} download...")

    def callback(current, total):
        client.loop.create_task(
            progress_bar(
                current,
                total,
                f"Downloading {download_type}",
                progress_message,
                start_time
            )
        )

    downloaded_path = await event.download_media(
        file=file_path,
        progress_callback=callback
    )

    await progress_message.delete()
    return downloaded_path

async def video_handler(event, client):
    """Handle incoming video files"""
    user_id = event.sender_id

    # Store video file path with progress
    video_path = await download_with_progress(
        client,
        event,
        f"{TEMP_FILE_PREFIX}{user_id}_video.mp4",
        "video"
    )

    # Store in database
    db.put_video(user_id, video_path, event.file.name)

    # Only reply after download is complete
    await event.reply("✅ Video received. Now send the subtitle file (SRT or ASS format).")

async def subtitle_handler(event, client):
    """Handle incoming subtitle files"""
    user_id = event.sender_id

    if not db.check_video(user_id):
        await event.reply(ERROR_MESSAGES['no_video'])
        return

    try:
        # Download subtitle with progress
        sub_path = await download_with_progress(
            client,
            event,
            f"{TEMP_FILE_PREFIX}{user_id}_sub.srt",
            "subtitle"
        )

        # Store subtitle in database
        db.put_sub(user_id, sub_path)

        video_path = db.get_vid_filename(user_id)
        output_path = f"{OUTPUT_FILE_PREFIX}{user_id}.mp4"

        # Get settings from database or use defaults
        settings = db.get_settings(user_id) or DEFAULT_SETTINGS

        # Process video with FFmpeg progress
        progress_message = await event.reply("🎥 Starting video processing...")
        await process_video(
            user_id,
            video_path,
            sub_path,
            output_path,
            settings,
            progress_message
        )

        # Send the processed video with upload progress
        start_time = time.time()
        upload_message = await event.reply("📤 Uploading processed video...")

        await client.send_file(
            event.chat_id,
            output_path,
            supports_streaming=True,
            attributes=[DocumentAttributeVideo(
                duration=0,
                w=0,
                h=0
            )],
            caption=ERROR_MESSAGES['success'],
            progress_callback=lambda current, total: client.loop.create_task(
                progress_bar(
                    current,
                    total,
                    "Uploading Video",
                    upload_message,
                    start_time
                )
            )
        )

        await upload_message.delete()

    except Exception as e:
        await event.reply(ERROR_MESSAGES['error'].format(str(e)))
    finally:
        # Clean up
        db.erase(user_id)
        if os.path.exists(output_path):
            os.remove(output_path)

async def start_handler(event, client):
    """Handle /start command"""
    user_id = event.sender_id
    user_settings = db.get_settings(user_id) or DEFAULT_SETTINGS
    markup = await get_settings_markup(user_id, client, {user_id: user_settings})
    await event.respond(WELCOME_MESSAGE, buttons=markup)

# Optional: manual /settings command
async def settings_command_handler(event, client):
    user_id = event.sender_id
    user_settings = db.get_settings(user_id) or DEFAULT_SETTINGS
    markup = await get_settings_markup(user_id, client, {user_id: user_settings})
    await event.respond("⚙️ Current Settings:", buttons=markup)
