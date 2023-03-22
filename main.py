
import logging
from compress_video import compress_video
from aiogram import Bot, Dispatcher, types
from bot.settings import API_TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(regexp=("^.*(mp4|mkv|mov)$"), content_types=types.ContentTypes.VIDEO | types.ContentTypes.DOCUMENT)
async def handle_video(message: types.Message):
    video_to_compress = message.video or message.document
    video_to_compress_file_id = video_to_compress.file_id
    output_file_name = "compressed_" + video_to_compress.file_name

    video_file_path = await bot.get_file(file_id=video_to_compress_file_id)
    video_file = await bot.download_file(file_path=video_file_path.file_path)

    with open(video_to_compress.file_name, "wb") as file:
        file.write(video_file.read())

    try:
        compressed_video_file = compress_video(video_to_compress.file_name, output_file_name)
        with open(compressed_video_file, "rb") as video:
            await bot.send_video(chat_id=message.chat.id, video=video)
    except Exception as e:
        await bot.send_message(chat_id=message.chat.id, text=str(e))

@dp.message_handler(commands=['start', 'help'])
async def handle_start_help(message: types.Message):
    start_message = (
        "Welcome to the Video Compression Bot!\n\n"
        "This bot compresses video files using the libx265 codec. "
        "Just send me a video file or a direct link, and I'll compress it for you.\n\n"
        "You can set advanced options by interacting with the bot."
    )
    await message.reply_text(start_message)


if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp)
