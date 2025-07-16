import math
import time
import re
from typing import Optional, Dict

async def progress_bar(current, total, text, message, start):
    """Generic progress bar for downloads/uploads"""
    now = time.time()
    diff = now - start

    if (round(diff) % 5 == 0) or (current == total):
        percentage = (current / total) * 100
        speed = current / diff if diff > 0 else 0
        elapsed_ms = int(diff * 1000)
        eta_ms = int(((total - current) / speed) * 1000) if speed > 0 else 0
        total_eta = eta_ms + elapsed_ms

        bar_filled = math.floor(percentage / 5)
        bar_empty = 20 - bar_filled
        bar = "█" * bar_filled + "░" * bar_empty

        formatted = (
            f"`[{bar}]`\n\n"
            f"**Progress:** {round(percentage, 2)}%\n"
            f"**Done:** {humanbytes(current)} of {humanbytes(total)}\n"
            f"**Speed:** {humanbytes(speed)}/s\n"
            f"**Elapsed:** {TimeFormatter(elapsed_ms)}\n"
            f"**ETA:** {TimeFormatter(total_eta)}"
        )

        try:
            await message.edit(text=f"**{text}**\n\n{formatted}")
        except:
            pass

def parse_ffmpeg_progress(line: str) -> Optional[Dict]:
    """Parse FFmpeg progress output"""
    progress_pattern = re.compile(r'(frame|fps|size|time|bitrate|speed)\s*=\s*(\S+)')
    items = {key: value for key, value in progress_pattern.findall(line)}
    return items if items else None

async def readlines(stream):
    """Async generator to read lines from stream"""
    pattern = re.compile(br'[\r\n]+')
    data = bytearray()
    while not stream.at_eof():
        lines = pattern.split(data)
        data[:] = lines.pop(-1)
        for line in lines:
            yield line
        data.extend(await stream.read(1024))

async def monitor_ffmpeg_progress(process, msg):
    """Monitor FFmpeg progress and update message"""
    last_edit_time = 0
    async for line in readlines(process.stderr):
        line = line.decode('utf-8', errors='ignore')
        progress = parse_ffmpeg_progress(line)
        if progress:
            now = time.time()
            if now - last_edit_time >= 5:  # Update every 5 seconds
                text = '🎥 **Hardmux Progress**\n\n'
                text += f"📦 **Size:** `{progress.get('size', 'N/A')}`\n"
                text += f"⏱️ **Time:** `{progress.get('time', 'N/A')}`\n"
                text += f"⚡ **Speed:** `{progress.get('speed', 'N/A')}`\n"
                text += f"📊 **FPS:** `{progress.get('fps', 'N/A')}`"
                try:
                    await msg.edit(text)
                    last_edit_time = now
                except:
                    pass

def humanbytes(size):
    """Convert bytes to human-readable format"""
    if size is None:
        return "0 B"
    power = 2**10
    n = 0
    Dic_powerN = {0: '', 1: 'Ki', 2: 'Mi', 3: 'Gi', 4: 'Ti'}
    while size >= power and n < 4:
        size /= power
        n += 1
    return f"{round(size, 2)} {Dic_powerN[n]}B"

def TimeFormatter(ms: int) -> str:
    """Format milliseconds to human-readable time"""
    seconds, ms = divmod(ms, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    parts = []
    if days: parts.append(f"{days}d")
    if hours: parts.append(f"{hours}h")
    if minutes: parts.append(f"{minutes}m")
    if seconds: parts.append(f"{seconds}s")
    if ms: parts.append(f"{ms}ms")
    return ", ".join(parts) if parts else "0s"
