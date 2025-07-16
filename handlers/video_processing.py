import os
import asyncio
import ffmpeg
from utils.progress import monitor_ffmpeg_progress

async def process_video(
    user_id: int,
    video_path: str,
    sub_path: str,
    output_path: str,
    settings: dict,
    progress_message
):
    try:
        font_path = os.path.join("fonts", "HelveticaRounded-Bold.ttf")
        if not os.path.exists(font_path):
            await progress_message.edit("❌ Font not found!")
            return

        # Check resolution
        probe = ffmpeg.probe(video_path)
        video_stream = next((s for s in probe['streams'] if s['codec_type'] == 'video'), None)

        if not video_stream:
            await progress_message.edit("❌ Could not read video stream.")
            return

        width, height = video_stream['width'], video_stream['height']
        if settings['resolution'] != 'original':
            res_map = {
                '1080p': (1920, 1080),
                '720p': (1280, 720),
                '480p': (854, 480)
            }
            width, height = res_map.get(settings['resolution'], (width, height))

        # Prepare subtitle filter (escaped path)
        escaped_sub = sub_path.replace(":", "\\:").replace("'", "\\'")
        subtitle_filter = (
            f"subtitles='{escaped_sub}':force_style="
            f"'FontName=HelveticaRounded-Bold,FontSize=24,PrimaryColour=&HFFFFFF&'"
        )

        if (width, height) != (video_stream['width'], video_stream['height']):
            subtitle_filter += f",scale={width}:{height}"

        ffmpeg_cmd = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-vf", subtitle_filter,
            "-vcodec", settings['codec'],
            "-crf", settings['crf'],
            "-preset", settings['preset'],
            "-r", "30",
            "-pix_fmt", "yuv420p",  # Safe default
            "-progress", "pipe:1",
            output_path
        ]

        # Add 10-bit support
        if settings['bit_depth'] == '10' and settings['codec'] in ['libx265', 'libvpx-vp9']:
            ffmpeg_cmd += ["-pix_fmt", "yuv420p10le"]
            if settings['codec'] == 'libx265':
                ffmpeg_cmd += ["-x265-params", "profile=main10"]

        process = await asyncio.create_subprocess_exec(
            *ffmpeg_cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        await monitor_ffmpeg_progress(process, progress_message)
        await process.wait()

        if process.returncode != 0:
            stderr = (await process.stderr.read()).decode()
            raise RuntimeError(f"FFmpeg failed with code {process.returncode}.\n\nStderr:\n{stderr.strip()}")

        await progress_message.edit("✅ **Processing complete!** Uploading now...")

    except Exception as e:
        await progress_message.edit(f"❌ **Error processing video:** `{str(e)}`")
        raise e

    finally:
        for f in [video_path, sub_path]:
            if os.path.exists(f):
                os.remove(f)
