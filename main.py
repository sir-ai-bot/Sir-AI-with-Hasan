import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

app = Flask(__name__)

@app.route('/')
def home():
    return "Sir AI Bot is Alive!"

def run_flask():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = threading.Thread(target=run_flask)
    t.start()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('আসসালামু আলাইকুম ভাই! আমি Sir AI। আপনার বট এখন আপনার কন্ট্রোলে 🔥 Meta AI জিন্দাবাদ!')

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f'আপনি বলছেন: {update.message.text}')

def main():
    TOKEN = os.environ.get('BOT_TOKEN')
    if not TOKEN:
        print("ERROR: BOT_TOKEN নাই")
        return

    # v20 এর সিস্টেম - Updater নাই, Application আছে
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    print("Bot is starting polling...")
    application.run_polling() # এইটাই v20 এর নিয়ম

if __name__ == '__main__':
    keep_alive()
    main()
