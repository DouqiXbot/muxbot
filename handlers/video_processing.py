import os
import ffmpeg
import asyncio
from typing import Dict, Callable, Optional
from config.settings import DEFAULT_SETTINGS, FONT_URL, FONT_FILENAME
from utils.progress import monitor_ffmpeg_progress
import requests

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
    settings: Dict,
    progress_message
):
    """Process video with subtitles using FFmpeg with real-time progress"""
    try:
        # Ensure font is available
        font_path = ensure_font_downloaded()
        
        # Get video info
        probe = ffmpeg.probe(video_path)
        video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
        
        # Set resolution
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
        
        # Build ffmpeg command
        input_video = ffmpeg.input(video_path)
        
        stream = input_video.filter(
            'subtitles', 
            sub_path,
            force_style=f"Fontname={font_path},Fontsize=24,PrimaryColour=&HFFFFFF&"
        )
        
        if (width, height) != (video_stream['width'], video_stream['height']):
            stream = stream.filter('scale', width, height)
        
        # Configure output
        output_args = {
            'vcodec': settings['codec'],
            'crf': settings['crf'],
            'preset': settings['preset'],
            **{'q:v': {'low': 28, 'medium': 23, 'high': 18, 'very high': 12}[settings['quality']]}
        }
        
        # Add 10-bit support
        if settings['bit_depth'] == '10':
            if settings['codec'] in ['libx265', 'libvpx-vp9']:
                output_args['pix_fmt'] = 'yuv420p10le'
                if settings['codec'] == 'libx265':
                    output_args['x265-params'] = 'profile=main10'
        
        # Run FFmpeg with progress monitoring
        process = (
            stream
            .output(output_path, **output_args)
            .global_args('-progress', 'pipe:1')  # Send progress to stdout
            .run_async(pipe_stdout=True, pipe_stderr=True, overwrite_output=True)
        )
        
        # Start progress monitoring
        progress_task = asyncio.create_task(
            monitor_ffmpeg_progress(process, progress_message)
        )
        
        # Wait for process to complete
        await process.wait()
        progress_task.cancel()
        
        # Final progress update
        try:
            await progress_message.edit("✅ **Processing complete!** Uploading now...")
        except:
            pass
        
        return True
    except Exception as e:
        try:
            await progress_message.edit(f"❌ **Error processing video:** {str(e)}")
        except:
            pass
        raise e
    finally:
        # Clean up temporary files
        for path in [video_path, sub_path]:
            if os.path.exists(path):
                os.remove(path)
