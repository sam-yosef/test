
import os
import uuid
import tempfile
from telegram import Update, ReplyKeyboardMarkup, InputFile
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from utils import compress_video
from config import TOKEN, TEMP_DIR

if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        'أرسل إلي رابط الفيديو أو قم بتحميل الفيديو و سأقوم بضغط الفيديو لك.'
    )

def echo(update: Update, context: CallbackContext):
    message = update.message
    if message.video:
        video = message.video
        new_file = context.bot.get_file(video.file_id)
        temp_input_path = os.path.join(TEMP_DIR, f"{str(uuid.uuid4())}.mp4")

        new_file.download(temp_input_path)

        output_path= os.path.join(tempfile.gettempdir(), f"output_{str(uuid.uuid4())}.mp4")
        
        compress_video(temp_input_path, output_path)

        with open(output_path, "rb") as f:
            context.bot.send_video(chat_id=message.chat_id, video=InputFile(f))

        os.remove(temp_input_path)
        os.remove(output_path)

def main():
    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text | Filters.video, echo))
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
