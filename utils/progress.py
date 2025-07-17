import time
async def progress_bar(current, total, message, stage="Downloading"):
    percent = int(current * 100 / total)
    bar = "[" + "#" * (percent // 10) + "-" * (10 - percent // 10) + "]"
    await message.edit(f"{stage}...\n{bar} {percent}%")
