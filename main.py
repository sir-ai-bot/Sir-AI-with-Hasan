import os
import logging
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Flask সার্ভার - Render কে খুশি রাখার জন্য
app = Flask('')

@app.route('/')
def home():
    return "Sir AI Bot is running!"

def run_flask():
  app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run_flask)
    t.start()

# লগিং সেটআপ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# আপনার বট টোকেন Environment থেকে নিবে
BOT_TOKEN = os.environ.get('BOT_TOKEN')

# /start কমান্ড
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("হ্যালো ভাই! আমি Sir AI Bot. আমি এখন Render এ লাইভ ❤️‍🔥")

# নরমাল মেসেজের রিপ্লাই
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    await update.message.reply_text(f"আপনি বললেন: {user_message}")

def main():
    # Flask সার্ভার চালু করেন
    keep_alive()
    
    # বট অ্যাপ্লিকেশন বানান
    application = Application.builder().token(BOT_TOKEN).build()

    # কমান্ড হ্যান্ডলার অ্যাড করেন
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # বট চালু করেন
    print("Bot is starting polling...")
    application.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
