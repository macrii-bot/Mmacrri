import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import yt_dlp

BOT_TOKEN = "BOT_TOKEN_HERE"  # ഇതിൽ നിന്റെ ടോകൺ ചേർക്കൂ

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Macrii Downloader ബോട്ടിലേയ്ക്ക് സ്വാഗതം! /download <link> കൊടുക്കൂ.")

async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("ഒരു ലിങ്ക് കൊടുക്കൂ.")
        return

    url = context.args[0]
    await update.message.reply_text("ഡൗൺലോഡ് തുടങ്ങുന്നു...")

    try:
        ydl_opts = {
            'outtmpl': '%(title)s.%(ext)s',
            'format': 'bestvideo+bestaudio/best',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        await update.message.reply_video(video=open(filename, 'rb'))
        os.remove(filename)

    except Exception as e:
        await update.message.reply_text(f"എരർ: {str(e)}")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("download", download))

app.run_polling()
