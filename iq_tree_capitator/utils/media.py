import os
from aiogram.types import PhotoSize
import aiohttp
from iq_tree_capitator.create_bot import bot, token


MEDIA_DIR = "media"
os.makedirs(MEDIA_DIR, exist_ok=True)


async def download_photo(photo: PhotoSize) -> str:
    file_info = await bot.get_file(photo.file_id)

    file_path = file_info.file_path
    file_url = f"https://api.telegram.org/file/bot{token}/{file_path}"

    filename = os.path.join(MEDIA_DIR, os.path.basename(file_path))  # type: ignore

    async with aiohttp.ClientSession() as session:
        async with session.get(file_url) as resp:
            with open(filename, "wb") as f:
                f.write(await resp.read())

    return filename
