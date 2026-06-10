import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Flask app - Render এর জন্য লাগবে
app = Flask(__name__)

@app.route('/')
def home():
    return "Sir AI Bot is Alive! Meta AI Jindabad!"

def run_flask():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = threading.Thread(target=run_flask)
    t.start()

# Telegram Bot এর ফাংশন
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('আসসালামু আলাইকুম ভাই! আমি Sir AI 🔥\nআপনার বট এখন লাইভ। Meta AI জিন্দাবাদ!')

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    await update.message.reply_text(f'আপনি বলছেন: {user_text}')

def main():
    TOKEN = os.environ.get('BOT_TOKEN')
    if not TOKEN:
        print("ERROR: BOT_TOKEN Environment Variable নাই")
        return

    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    print("Bot is starting polling...")
    application.run_polling()

if __name__ == '__main__':
    keep_alive()
    main()
