import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# 1. Flask সার্ভার - Render কে জাগায় রাখার জন্য
app = Flask(__name__)

@app.route('/')
def home():
    return "Sir AI Bot is Alive!"

def run_flask():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = threading.Thread(target=run_flask)
    t.start()

# 2. Telegram বটের ফাংশন
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('আসসালামু আলাইকুম ভাই! আমি Sir AI। আপনার বট এখন আপনার কন্ট্রোলে 🔥')

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    await update.message.reply_text(f'আপনি বলছেন: {user_message}')

# 3. মেইন ফাংশন - বট চালু করার জন্য
def main():
    # Render এর Environment থেকে টোকেন নিবে
    TOKEN = os.environ.get('BOT_TOKEN')
    
    if not TOKEN:
        print("ERROR: BOT_TOKEN নাই। Render এ Environment এ যোগ করেন।")
        return

    # Application বানান
    application = Application.builder().token(TOKEN).build()

    # কমান্ড হ্যান্ডলার যোগ করেন
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # বট চালু করেন
    print("///////////////////")
    print("Bot is starting polling...")
    application.run_polling()

if __name__ == '__main__':
    keep_alive()  # Flask আলাদা থ্রেডে চালু
    main()        # বট মেইন থ্রেডে চালু
