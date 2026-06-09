import os
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Flask app - Render কে খুশি রাখার জন্য
app = Flask(__name__)

@app.route('/')
def home():
    return "Sir AI is Running..."

def run_flask():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

# Telegram Bot Functions
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Assalamu Alaikum Sir Hasan! Bot is Live 🔥")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ami Sir AI. Apnar jonno ready!")

# Main function
def main():
    # Environment Variable থেকে টোকেন নেন
    TOKEN = os.environ.get("BOT_TOKEN")
    
    if not TOKEN:
        print("Error: BOT_TOKEN environment variable not set!")
        return

    # Application build করেন v20 স্টাইলে
    application = ApplicationBuilder().token(TOKEN).build()

    # Command handlers add করেন
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # Flask অন্য Thread এ চালান
    Thread(target=run_flask).start()
    
    # Bot polling শুরু করেন
    print("Sir AI is Running...")
    application.run_polling()

if __name__ == '__main__':
    main()
