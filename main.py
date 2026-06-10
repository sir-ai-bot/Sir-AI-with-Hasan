import os
import threading
from flask import Flask
from telegram.ext import Updater, CommandHandler

# 1. Render থেকে BOT_TOKEN নেওয়া
TOKEN = os.environ.get('BOT_TOKEN')

# 2. Flask সার্ভার - Render কে খুশি রাখার জন্য
app = Flask(__name__)

@app.route('/')
def home():
    return "Sir AI Bot is Alive!"

def run_flask():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = threading.Thread(target=run_flask)
    t.start()

# 3. Telegram বটের কমান্ড
def start(update, context):
    user = update.effective_user
    update.message.reply_text(f"Hello {user.first_name}! Sir AI Bot is live on Render ❤️‍🔥")

def main():
    # Flask চালু করেন ব্যাকগ্রাউন্ডে
    keep_alive()
    
    # v13 এর Updater দিয়ে বট চালু করেন
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    
    # কমান্ড অ্যাড করেন
    dp.add_handler(CommandHandler("start", start))
    
    # বট স্টার্ট
    updater.start_polling()
    print("Bot is starting polling...")
    updater.idle()

if __name__ == '__main__':
    main()
