import asyncio
import os
from utils.progress import progress_bar

async def process_video(client, chat_id, data, settings):
    video_msg = await client.send_message(chat_id, "Downloading video...")
    video_path = await client.download_media(data["video"], file_name=f"downloads/{chat_id}_video.mp4",
                                              progress=progress_bar, progress_args=(video_msg, "Downloading Video"))

    sub_msg = await client.send_message(chat_id, "Downloading subtitle...")
    subtitle_path = await client.download_media(data["subtitle"], file_name=f"downloads/{chat_id}_sub.srt",
                                                progress=progress_bar, progress_args=(sub_msg, "Downloading Subtitle"))

    out_path = f"downloads/{chat_id}_out.mp4"
    res_map = {"480p": "640x480", "720p": "1280x720", "1080p": "1920x1080"}
    font = "fonts/HelveticaRounded-Bold.ttf"

    encode_msg = await client.send_message(chat_id, "Encoding video...")
    cmd = [
        "ffmpeg", "-y", "-i", video_path,
        "-vf", f"subtitles='{subtitle_path}':force_style='FontName=HelveticaRounded-Bold,FontSize={settings['fontsize']}',scale={res_map[settings['resolution']]}",
        "-c:v", settings["codec"], "-preset", settings["preset"], "-crf", settings["crf"], "-c:a", "copy", out_path
    ]
    process = await asyncio.create_subprocess_exec(*cmd, stderr=asyncio.subprocess.PIPE)
    while True:
        line = await process.stderr.readline()
        if not line:
            break
        if b"frame=" in line:
            await encode_msg.edit(f"Encoding...\n{line.decode(errors='ignore')}")

    if process.returncode == 0:
        await client.send_document(chat_id, out_path, caption="✅ Encoding complete.")
    else:
        await client.send_message(chat_id, "❌ FFmpeg error occurred.")
