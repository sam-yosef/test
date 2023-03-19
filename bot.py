
import os
import sys
from urllib.parse import urlparse

import ffmpeg
import telegram
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Updater, CommandHandler, 
    MessageHandler, Filters,
    CallbackQueryHandler,
    CallbackContext,
)

# set your token here:
BOT_TOKEN = "5668946955:AAEvNEb5tvSImKyskVq-jc36MlgnYhst8v8"


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="أهلا! أنا بوت تليجرام لضغط الفيديو. أرسل لي رابط أو ملف فيديو.")


def video(update: Update, context: CallbackContext):
    message = update.effective_message
    video_url = message.text

    file = urlparse(video_url)
    local_filename = os.path.basename(file.path)
    
    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton("libx264", callback_data=f"codec,libx264,{local_filename}"),
        InlineKeyboardButton("libx265", callback_data=f"codec,libx265,{local_filename}")
    ]])

    message.reply_text("اختر الكوديك:", reply_markup=keyboard)


def codec_selection(update: Update, context: CallbackContext):
    query = update.callback_query
    codec, selected_codec, local_filename = query.data.split(",")
    query.message.reply_text(f'تم اختيار الكوديك: {selected_codec}')

    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton("360p", callback_data=f"size,360,{selected_codec},{local_filename}"),
        InlineKeyboardButton("480p", callback_data=f"size,480,{selected_codec},{local_filename}"),
        InlineKeyboardButton("720p", callback_data=f"size,720,{selected_codec},{local_filename}"),
    ]])

    query.message.reply_text("اختر دقة الفيديو:", reply_markup=keyboard)


def size_selection(update: Update, context: CallbackContext):
    query = update.callback_query
    size, selected_size, selected_codec, local_filename = query.data.split(",")

    query.message.reply_text(f'تم اختيار دقة الفيديو: {selected_size}')

    compressed_filename = f"compressed_{local_filename}"
    video_stream = ffmpeg.input(local_filename)
    video_stream = video_stream.output(
        compressed_filename,
        codec=selected_codec,
        vf=f"scale=-1:{selected_size}",
    )
    process = video_stream.run_async()
    process.wait()
    query.message.reply_video(
        video=open(compressed_filename, "rb"),
        filename=compressed_filename,
        caption="ها هو الفيديو المضغوط:",
        timeout=1200,
    )


def error_handler(update, context):
    print(f'Update "{update}" caused error "{context.error}"')


def main():
    updater = Updater(token=BOT_TOKEN)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.video_file | Filters.entity("url"), video))
    dispatcher.add_handler(CallbackQueryHandler(pattern="codec,", callback=codec_selection))
    dispatcher.add_handler(CallbackQueryHandler(pattern="size,", callback=size_selection))
    dispatcher.add_error_handler(error_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
