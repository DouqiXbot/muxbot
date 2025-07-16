import os
import asyncio
import requests
from config.settings import DEFAULT_SETTINGS, FONT_URL, FONT_FILENAME
from utils.progress import monitor_ffmpeg_progress
import ffmpeg

def ensure_font_downloaded():
    """Ensure the font file is downloaded and available"""
    font_path = os.path.join(os.path.dirname(__file__), '..', 'fonts', FONT_FILENAME)
    os.makedirs(os.path.dirname(font_path), exist_ok=True)

    if not os.path.exists(font_path):
        response = requests.get(FONT_URL)
        with open(font_path, 'wb') as f:
            f.write(response.content)
    return font_path

async def process_video(
    user_id: int, 
    video_path: str, 
    sub_path: str, 
    output_path: str, 
    settings: dict,
    progress_message
):
    try:
        font_path = ensure_font_downloaded()

        # Get resolution
        probe = ffmpeg.probe(video_path)
        video_stream = next((s for s in probe['streams'] if s['codec_type'] == 'video'), None)

        if settings['resolution'] == 'original':
            width = video_stream['width']
            height = video_stream['height']
        else:
            res_map = {
                '1080p': (1920, 1080),
                '720p': (1280, 720),
                '480p': (854, 480)
            }
            width, height = res_map.get(settings['resolution'], (video_stream['width'], video_stream['height']))

        # FFmpeg args
        ffmpeg_cmd = [
            "ffmpeg",
            "-y",
            "-i", video_path,
            "-vf", f"subtitles='{sub_path}':force_style='FontName={font_path},Fontsize=24,PrimaryColour=&HFFFFFF&'"
                   + (f",scale={width}:{height}" if (width, height) != (video_stream['width'], video_stream['height']) else ""),
            "-vcodec", settings['codec'],
            "-crf", settings['crf'],
            "-preset", settings['preset'],
            "-progress", "pipe:1",
            "-f", "mp4"
        ]

        # Add bit depth support
        if settings['bit_depth'] == '10' and settings['codec'] in ['libx265', 'libvpx-vp9']:
            ffmpeg_cmd += ["-pix_fmt", "yuv420p10le"]
            if settings['codec'] == 'libx265':
                ffmpeg_cmd += ["-x265-params", "profile=main10"]

        # Output path
        ffmpeg_cmd.append(output_path)

        # Start process
        process = await asyncio.create_subprocess_exec(
            *ffmpeg_cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        # Monitor progress
        await monitor_ffmpeg_progress(process, progress_message)

        # Wait for process to finish
        await process.wait()

        await progress_message.edit("✅ **Processing complete!** Uploading now...")

    except Exception as e:
        await progress_message.edit(f"❌ **Error processing video:** `{str(e)}`")
        raise e

    finally:
        for f in [video_path, sub_path]:
            if os.path.exists(f):
                os.remove(f)
